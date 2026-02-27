#!/usr/bin/env python3
"""
Transcription Tools Module

Provides speech-to-text transcription using multiple providers:
- Groq (free, fast) - whisper-large-v3-turbo
- OpenAI - whisper-1, gpt-4o-mini-transcribe, gpt-4o-transcribe

Used by the messaging gateway to automatically transcribe voice messages
sent by users on Telegram, Discord, WhatsApp, and Slack.

Supported input formats: mp3, mp4, mpeg, mpga, m4a, wav, webm, ogg

Usage:
    from tools.transcription_tools import transcribe_audio

    result = transcribe_audio("/path/to/audio.ogg")
    if result["success"]:
        print(result["transcript"])
"""

import logging
import os
import yaml
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

# Default STT models per provider
DEFAULT_MODELS = {
    "groq": "whisper-large-v3-turbo",
    "openai": "whisper-1",
}

# API base URLs per provider
API_BASE_URLS = {
    "groq": "https://api.groq.com/openai/v1",
    "openai": "https://api.openai.com/v1",
}


def _load_stt_config() -> dict:
    """Load STT configuration from config.yaml"""
    config_path = Path.home() / ".hermes" / "config.yaml"
    default_config = {
        "enabled": True,
        "provider": "groq",
        "model": None,
    }
    
    if not config_path.exists():
        return default_config
    
    try:
        with open(config_path) as f:
            config = yaml.safe_load(f)
        
        stt_config = config.get("stt", {})
        return {**default_config, **stt_config}
    except Exception as e:
        logger.warning(f"Failed to load STT config: {e}")
        return default_config


def _get_api_key(provider: str) -> Optional[str]:
    """Get API key for the specified provider"""
    if provider == "groq":
        # Try GROQ_API_KEY first, then .env file
        key = os.getenv("GROQ_API_KEY")
        if not key:
            env_path = Path.home() / ".hermes" / ".env"
            if env_path.exists():
                with open(env_path) as f:
                    for line in f:
                        if line.startswith("GROQ_API_KEY="):
                            key = line.strip().split("=", 1)[1]
                            break
        return key
    elif provider == "openai":
        return os.getenv("VOICE_TOOLS_OPENAI_KEY") or os.getenv("OPENAI_API_KEY")
    return None


def transcribe_audio(file_path: str, model: Optional[str] = None, provider: Optional[str] = None) -> dict:
    """
    Transcribe an audio file using the configured STT provider.

    Args:
        file_path: Absolute path to the audio file to transcribe.
        model:     STT model to use. Defaults to config or provider default.
        provider:  STT provider ("groq" or "openai"). Defaults to config.

    Returns:
        dict with keys:
          - "success" (bool): Whether transcription succeeded
          - "transcript" (str): The transcribed text (empty on failure)
          - "error" (str, optional): Error message if success is False
    """
    # Load config
    stt_config = _load_stt_config()
    
    # Determine provider (config > parameter > default)
    if provider is None:
        provider = stt_config.get("provider", "groq")
    
    # Get API key
    api_key = _get_api_key(provider)
    if not api_key:
        return {
            "success": False,
            "transcript": "",
            "error": f"{provider.upper()}_API_KEY not set",
        }

    audio_path = Path(file_path)
    if not audio_path.is_file():
        return {
            "success": False,
            "transcript": "",
            "error": f"Audio file not found: {file_path}",
        }

    # Determine model (parameter > config > provider default)
    if model is None:
        model = stt_config.get("model") or DEFAULT_MODELS.get(provider, "whisper-1")

    base_url = API_BASE_URLS.get(provider, "https://api.openai.com/v1")

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url=base_url)

        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=model,
                file=audio_file,
                response_format="text",
            )

        # The response is a plain string when response_format="text"
        transcript_text = str(transcription).strip()

        logger.info(f"Transcribed {audio_path.name} ({len(transcript_text)} chars) via {provider}")

        return {
            "success": True,
            "transcript": transcript_text,
        }

    except Exception as e:
        logger.error(f"Transcription error ({provider}): {e}")
        return {
            "success": False,
            "transcript": "",
            "error": str(e),
        }
