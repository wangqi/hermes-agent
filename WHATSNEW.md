# What's New — Upstream Merge (Feb 2026)

Changes merged from [NousResearch/Hermes-Agent](https://github.com/NousResearch/Hermes-Agent) into this fork.

---

## New Features

### Session Reset Policy (`588cdac`)

The gateway now automatically clears conversation context based on inactivity or a daily
schedule. Without this, context grows indefinitely, burning tokens.

**Defaults:** resets after 24 hours of idle time OR at 4 AM daily.

**Smart save:** before wiping context, the agent gets one turn to save important facts to
persistent memory — so key information survives the reset.

Configure in `~/.hermes/config.yaml`:
```yaml
session_reset:
  mode: both          # "both" | "idle" | "daily" | "none"
  idle_minutes: 1440  # 24 hours
  at_hour: 4          # 4 AM for daily reset
```

---

### OCR and Document Extraction Skill (`19abbff`)

New skill: `skills/ocr-and-documents/` — extract text from PDFs, scanned documents, and
images. Two backend options:

| Backend | Size | Best for |
|---|---|---|
| `pymupdf` | ~25 MB | Fast, text-based PDFs |
| `marker-pdf` | ~5 GB | Full OCR, equations, forms, 90+ languages |

The `web_extract` tool now also handles PDF URLs directly.

---

### arXiv Skill Enhancements (`26a6da2`, `445d264`)

- BibTeX generation from arXiv metadata
- Version numbers shown in results (v1, v2…) to prevent citation drift
- Detection and warning for withdrawn/retracted papers

---

### Gateway Auto-Restart on Updates (`b267e34`)

When Hermes updates itself, the gateway service now automatically restarts. No manual
`launchctl stop/start` needed after an update.

---

### Pairing Store and Event Hook System (`fec5d59`)

New code-based user authorization and event hooks in the gateway. Foundation for
custom workflow triggers. No config change needed for current usage.

---

## Security Fixes

### Shell Injection via Sudo Password (`547ba73`)

If `SUDO_PASSWORD` contained shell metacharacters (`$()`, backticks, quotes), they were
executed. Fixed with `shlex.quote()`. **Important if you set `SUDO_PASSWORD` in `.env`.**

### macOS Symlink Bypass on Write Deny List (`0909be3`)

On macOS, `/etc` is a symlink to `/private/etc`. The write deny list checks didn't resolve
symlinks consistently, so writing to `/etc/passwd`, `/etc/sudoers`, etc. was not blocked.
Fixed with `os.path.realpath()` on all deny list entries at load time.

### Cron Prompt Injection Bypass (`1522718`)

The regex detecting "ignore prior instructions" in cron job payloads only matched
single-word gaps, so variants like "ignore ALL prior instructions" bypassed the scanner.
Fixed with a broader pattern.

### Recursive Delete False Positives (`3227cc6`)

`rm requirements.txt` was incorrectly flagged as a recursive delete because the `-r` flag
detection had an optional dash. The dash is now required, so innocent `rm` commands no
longer trigger approval prompts.

---

## Bug Fixes — Daily Use

### Six Core Agent Fixes (`c77f3da`)

Critical reliability fixes for the main agent loop:

1. **Session flush off-by-one** — one message per flush was being skipped, silently
   corrupting session history
2. **Stale interrupt state** — previous interrupt flags could bleed into the next turn,
   causing spurious early exits
3. **Tool crash resilience** — unhandled exceptions in tool calls no longer kill the
   entire conversation
4. **Memory flush sentinel** — replaced fragile identity checks with explicit markers
5. **Retry loop off-by-one** — was retrying 7 times when 6 was intended
6. **Dead import cleanup**

### WhatsApp Multi-User Sessions (`80ad657`)

Fixed session isolation between multiple WhatsApp contacts — each user now gets a
separate conversation context.

### CLI Fixes

| Commit | Fix |
|---|---|
| `1362f92` | `/config` command now shows the correct config file path |
| `9061c03` | Multi-line input no longer falsely flagged as a paste |
| `ae8d25f` | `--max-turns` flag respected even when it equals the default value |
| `8174f5a` | No crash when `model` in config.yaml is stored as a string |
| `715825e` | Local models via `OPENAI_BASE_URL` recognized without requiring an API key |
| `b281ecd` | `/skills` command rendering fixed |
| `43f2321` | Reduced spinner flickering in the CLI |

### Terminal and Environment

- **FileOps on macOS** (`0cce536`) — fixed file operation bugs specific to macOS
- **SSH backend check** (`fed9f06`) — SSH terminal backend no longer silently disabled
- **Config→env sync** (`0a231c0`) — `cli-config.yaml` terminal settings now properly
  written through to the environment seen by `terminal_tool`
- **Signal handler race** (`2972f98`) — eliminated spurious traceback on Ctrl+C exit
- **Install script** (`9eabdb6`) — no more silent abort when piping install via `curl | bash`

---

## Config Changes to Review

### New `session_reset` section

Add to `~/.hermes/config.yaml` to control or disable automatic resets:
```yaml
session_reset:
  mode: none   # disable if you don't want automatic resets
```

### Voice tools API key change (`a5ea272`)

Upstream simplified TTS/STT key lookup to **only** read `VOICE_TOOLS_OPENAI_KEY` —
the fallback to `OPENAI_API_KEY` was removed. **This does not affect our setup** because
we use speaches (no key) and Edge TTS (no key). Only relevant if you switch to OpenAI
TTS/STT.

---

## Test Coverage

210 new unit tests added across previously untested modules: cron scheduling, memory tool
security scanner, toolset resolution, file operations/deny list, session DB, model metadata.
Total suite: ~380 tests.
