---
name: upstream-sync
description: Sync a forked repo with upstream — fetch remote changes, merge them, resolve conflicts intelligently, update WHATSNEW.md with a summary of new changes, then commit and push. Triggers on "sync upstream", "merge upstream", "pull upstream changes", "update from upstream", "sync fork".
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Git, GitHub, Fork, Upstream, Merge, Sync]
    related_skills: [github-auth, github-pr-workflow]
---

# Upstream Sync Skill

Merge upstream changes into a forked repository, resolve conflicts, write a WHATSNEW.md
summary, and push. Always requires the user to confirm before pushing.

---

## Step 1 — Confirm the repo and upstream remote

```bash
# Check we're in the right repo
git remote -v

# If 'upstream' remote is missing, add it
git remote add upstream https://github.com/NousResearch/Hermes-Agent.git
```

For the Hermes fork:
- **origin** → `https://github.com/wangqi/hermes-agent.git`
- **upstream** → `https://github.com/NousResearch/Hermes-Agent.git`

---

## Step 2 — Check for new upstream commits

```bash
git fetch upstream

# Show what's new
git log main..upstream/main --oneline
```

If there are no new commits, report that and stop. No action needed.

---

## Step 3 — Merge upstream into main

```bash
git merge upstream/main --no-edit
```

If there are **no conflicts**, skip to Step 5.

If the merge fails with conflicts, proceed to Step 4.

---

## Step 4 — Resolve conflicts

### Check what conflicted

```bash
git status
# Look for "both modified:" entries
```

### Conflict resolution rules for this fork

Each conflicted file has a known rule. Apply the rule, then `git add <file>`.

#### `tools/transcription_tools.py`
**Always keep HEAD (our version).**
Our version has the full multi-provider STT abstraction (speaches, Groq, OpenAI) with
config loading. Upstream periodically simplifies this to a single `os.getenv()` call,
which would break speaches/Groq support. Remove the conflict markers and keep the HEAD block.

```python
# KEEP this (HEAD) — discard the upstream block:
    stt_config = _load_stt_config()
    if provider is None:
        provider = stt_config.get("provider", "groq")
    api_key = _get_api_key(provider)
```

#### `gateway/run.py`
**Keep HEAD for our custom lines; accept upstream for everything else.**
Our changes in this file:
1. `history_offset = len(agent_history)` before `agent.run_conversation()` — keep it
2. `new_messages = result.get("messages", [])[history_offset:]` in the MEDIA scanner — keep it
3. TTS instruction in the voice transcription context string — keep it
4. 🐍 emoji for `execute_code`, 🔀 for `delegate_task`, 80-char truncation — keep them

For any other conflicts in this file, prefer upstream.

#### All other files
**Prefer upstream** — upstream changes are improvements we want to adopt. Only reject
upstream if it clearly conflicts with a known customization listed in CUSTOM.md.

### After resolving each file

```bash
git add <resolved_file>
```

### Complete the merge

```bash
git merge --continue
# Accept the auto-generated merge commit message
```

---

## Step 5 — Identify what actually changed

Collect the upstream commits that were just merged:

```bash
# List new upstream commits (everything upstream had that we didn't before the merge)
git log --oneline ORIG_HEAD..HEAD --no-merges
```

For each commit, read what changed using `git show <hash> --stat` and `git show <hash>`
to understand the actual diff. Focus on:
- New features and capabilities
- Security fixes
- Breaking changes or config changes required
- New skills added
- Important bug fixes affecting daily use

Group findings into these categories:
1. New Features
2. Security Fixes
3. Bug Fixes (Daily Use)
4. Config Changes to Review
5. New Skills

---

## Step 6 — Update WHATSNEW.md

Overwrite (do not append to) `WHATSNEW.md` at the project root with a fresh document
covering the newly merged changes. Use the template below.

Include only significant items — skip pure test additions, trivial docs, CI tweaks,
and README badge updates unless they signal something meaningful.

For each item, include:
- What it does in plain language
- Why it matters for a personal gateway/assistant setup
- Any action required (new config key, new env var, etc.)

### WHATSNEW.md template

```markdown
# What's New — Upstream Merge (<Month> <Year>)

Changes merged from [NousResearch/Hermes-Agent](https://github.com/NousResearch/Hermes-Agent).

---

## New Features

### <Feature Name> (`<commit hash>`)
<2–4 sentence description. What it does, why it matters, how to configure if needed.>

---

## Security Fixes

### <Fix Name> (`<commit hash>`)
<What the vulnerability was, what was fixed, whether action is required.>

---

## Bug Fixes — Daily Use

| Commit | Fix |
|---|---|
| `<hash>` | <one-line description> |

---

## Config Changes to Review

<List any new config keys, env vars, or default behaviour changes.
If nothing changed, omit this section.>

---

## New Skills

<List new skills with a one-line description each.
If none were added, omit this section.>
```

---

## Step 7 — Commit and push

```bash
git add WHATSNEW.md

git commit -m "docs: update WHATSNEW.md for upstream sync $(date +%Y-%m)"

git push origin main
```

Show the user the list of commits that were pushed and confirm success.

---

## Guardrails

- **Never force-push.** If push is rejected, report the error and ask the user.
- **Never merge if on a branch other than main.** Confirm the branch first.
- **Always show the user the WHATSNEW.md content before committing** and ask for approval
  if any of the upstream changes look breaking or require user action.
- **Do not resolve conflicts by simply choosing one side blindly** for files not listed
  in the rules above. Read the diff, understand both sides, and make an informed choice.
  If uncertain, show the conflict to the user and ask which version to keep.
