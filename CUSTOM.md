# Hermes Customizations

This document tracks all customizations made on top of upstream Hermes Agent.

---

## 1. LLM Provider — Z.ai (glm-5)

Hermes is configured to use a Z.ai custom endpoint instead of the default provider.

**Config (`.env`):**
```
OPENAI_BASE_URL=https://api.z.ai/api/coding/paas/v4
OPENAI_API_KEY=<z.ai key>
LLM_MODEL=glm-5
```

`cli-config.yaml` is left at defaults — all effective config lives in `.env`.

---

## 2. Persona — Aria (`~/.hermes/SOUL.md`)

A custom persona file replaces the default Hermes identity.

- **Name:** Aria
- **Role:** Senior female director, mobile app marketing expert
- **Expertise:** App Store dynamics, ASO, user acquisition, AI/Privacy AI products
- **Tone:** Professional, witty, warm, direct — not a generic assistant
- **Knowledge base:** Points to `/Users/wangqi/disk/projects/acmeup_privacyai/knowledge/`
  for Privacy AI product docs (manual, App Store copy, features, review replies)

The agent reads knowledge files on demand via `read_file` / `search_files` tools.

---

## 3. Gateway — Improved Tool Previews in Telegram

**Commit:** `c217feb` — `feat(gateway): show execute_code preview in Telegram progress messages`
**Files:** `agent/display.py`, `gateway/run.py`

Changes:
- `agent/display.py`: added `execute_code` handler in `build_tool_preview()` that extracts
  the first non-blank, non-comment line of code as the preview text
- `gateway/run.py`:
  - Added 🐍 emoji for `execute_code` tool progress messages
  - Added 🔀 emoji for `delegate_task` tool progress messages
  - Raised preview truncation limit from default to 80 chars for `execute_code`
    so a full line of code is readable instead of a truncated label

---

## 4. STT — speaches (local, OpenAI-compatible)

**Commits:**
- `2e0aa38` — `feat(stt): add Groq provider support for voice transcription` (refactored the
  whole STT module into a multi-provider abstraction; Groq was the first new provider)
- Current (unstaged) — switched default provider to speaches

**File:** `tools/transcription_tools.py`

The STT module supports multiple providers via an OpenAI-compatible API. speaches is a
self-hosted Whisper server running in Docker at `http://localhost:8000`.

Provider config added:
```python
DEFAULT_MODELS  = { ..., "speaches": "Systran/faster-whisper-large-v3" }
API_BASE_URLS   = { ..., "speaches": "http://localhost:8000/v1" }
# _get_api_key() returns "local" for speaches (no real key required)
```

`stt.base_url` in `~/.hermes/config.yaml` overrides the endpoint for all providers.

**Active config (`~/.hermes/config.yaml`):**
```yaml
stt:
  enabled: true
  provider: speaches
  model: Systran/faster-whisper-large-v3
```

**Running speaches:**
```bash
docker run --rm --detach \
  --publish 8000:8000 \
  --name speaches \
  --volume hf-hub-cache:/home/ubuntu/.cache/huggingface/hub \
  ghcr.io/speaches-ai/speaches:latest-cpu
```

The `Systran/faster-whisper-large-v3` model is downloaded once and cached in the
`hf-hub-cache` Docker volume (persists across container restarts).

---

## 5. Skills

All custom skills live under `skills/` and are synced to `~/.hermes/skills/` on startup
via `tools/skills_sync.py`.

### 5a. App Store Connect (`skills/app-store/asc/`)

**Commit:** `157af0d` — `feat(skills): add App Store Connect (asc) skill`

Skill for managing iOS/macOS apps via the `asc` CLI tool. Covers:
- Authentication and session management
- App submission and TestFlight distribution
- Metadata and screenshots management
- Code signing and provisioning profiles
- Analytics and sales reports
- In-App Purchases

Includes generated reference files from `asc docs show reference/api-notes`.

### 5b. X / Twitter Management (`skills/social/x-manage/`)

**Commit:** `c4938d9` — `feat(skills): add x-manage skill for X (Twitter) via xurl CLI`

Skill for managing X (Twitter) via the `xurl` CLI. Covers:
- Post, reply, quote, like, repost
- Search and timeline browsing
- Mentions and DMs
- Bookmarks
- Follow/unfollow
- Multi-account management

### 5c. Customer Care Email (`skills/email/customer-care/`)

**Commits:**
- `7969cbe` — `feat(skills): add customer-care email management skill`
- `4d8171b` — `fix(skills): update customer-care skill with correct himalaya account`

Skill for managing Privacy AI support emails via the `himalaya` CLI. Covers:
- Reading and summarizing unread support emails from the `customercare` account
- Drafting replies informed by the Privacy AI knowledge base
- Handling refunds, bug reports, feature requests, and difficult customers
- Always presents draft for human approval before sending
- Tone aligned with Aria's professional/warm persona

Uses account name `customercare` with correct himalaya flag syntax (`-a` on subcommands).

---

## 6. Startup Script (`scripts/hermes-start`)

**Status:** Untracked (not yet committed)

A bash script that replaces `uv run python cli.py` as the standard way to start Hermes.

**What it does:**
1. Checks if Docker is available
2. Starts the speaches Docker container if not already running, waits up to 30s for health
3. Stops any existing Hermes process (SIGTERM → 5s grace → SIGKILL) to prevent duplicates
4. Launches Hermes via `uv run python cli.py`, forwarding all arguments

**Usage:**
```bash
./scripts/hermes-start            # interactive mode
./scripts/hermes-start --gateway  # gateway mode
```
