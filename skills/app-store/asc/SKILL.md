---
name: asc
description: App Store Connect CLI (asc) — authenticate, manage apps/builds/TestFlight, submit for review, handle signing, metadata, analytics, IAP, and subscriptions. Unofficial AI-friendly CLI built on top of the App Store Connect API.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [App Store Connect, iOS, macOS, TestFlight, Signing, Builds, Metadata, Analytics, IAP]
    related_skills: []
---

# App Store Connect CLI (asc)

`asc` is a fast, AI-friendly CLI for App Store Connect. All output is JSON by default.
Full reference: `asc --help` and `asc <command> --help` (always the source of truth).

## Authentication

Credentials are resolved in this order:
1. Named profile (`--profile NAME` or `ASC_PROFILE`)
2. System keychain
3. Config file (`~/.asc/config.json` or `./.asc/config.json` in the repo)
4. Environment variables

```bash
# Check current auth status
asc auth status

# Run diagnostics (JSON output)
asc doctor --output json

# Login with an API key
asc auth login

# Switch between profiles
asc auth switch

# Logout
asc auth logout
```

Environment variables for auth (useful in CI):
```
ASC_KEY_ID        - API key ID
ASC_ISSUER_ID     - Issuer ID
ASC_PRIVATE_KEY   - Private key content (inline PEM)
ASC_KEY_FILE      - Path to private key .p8 file
ASC_STRICT_AUTH=true  - Fail if credentials come from mixed sources
ASC_BYPASS_KEYCHAIN=1 - Skip keychain, use config/env only
```

## Key Principles

- Always use explicit flags: `--app "APP_ID"` not positional args
- Set `ASC_APP_ID` env var to avoid repeating `--app` on every command
- IDs are App Store Connect resource IDs — use list commands to find them
- `--paginate` fetches all pages automatically
- `--output json|table|markdown` controls format; `--pretty` for readable JSON
- Destructive operations require `--confirm`
- `--debug` and `--api-debug` for troubleshooting

## Workflow: Find App ID and Builds

```bash
# List all apps
asc apps

# Set for session
export ASC_APP_ID="<APP_ID>"

# Recent builds
asc builds list --app "$ASC_APP_ID" --sort -uploadedDate --limit 5
```

## Workflow: Submit for App Store Review

```bash
# 1. Find the version
asc versions list --app "$ASC_APP_ID"

# 2. Attach a build
asc versions attach-build --version-id "VERSION_ID" --build "BUILD_ID"

# 3. Submit
asc submit create --app "$ASC_APP_ID" --version "1.0.0" --build "BUILD_ID" --confirm

# One-step publish (handles attaching + submitting)
asc publish app-store --app "$ASC_APP_ID" --build "BUILD_ID" --confirm
```

## Workflow: TestFlight Distribution

```bash
# List beta groups
asc testflight beta-groups list --app "$ASC_APP_ID"
asc testflight beta-groups list --app "$ASC_APP_ID" --internal

# Add build to a beta group
asc builds add-groups --build "BUILD_ID" --group "GROUP_ID"

# Publish to TestFlight (handles group assignment)
asc publish testflight --app "$ASC_APP_ID" --build "BUILD_ID" --confirm
```

## Workflow: Release Status Dashboard

```bash
asc status --app "$ASC_APP_ID"
```

## Workflow: Metadata

```bash
# Pull, edit, validate, push
asc metadata pull --app "$ASC_APP_ID" --path ./metadata
# ... edit files ...
asc metadata validate --app "$ASC_APP_ID" --path ./metadata
asc metadata push --app "$ASC_APP_ID" --path ./metadata --confirm

# Migrate from fastlane
asc migrate validate --fastlane-dir ./metadata
asc migrate import --app "$ASC_APP_ID" --fastlane-dir ./metadata
```

## Workflow: Signing

```bash
# List certificates
asc certificates list

# List provisioning profiles
asc profiles list

# Download a profile
asc profiles download --profile "PROFILE_ID" --path ./profiles

# Manage bundle IDs and capabilities
asc bundle-ids list
asc bundle-ids capabilities list --bundle-id "BUNDLE_ID"
```

## Workflow: Analytics & Insights

```bash
# Weekly insights
asc insights weekly --app "$ASC_APP_ID" --source analytics --week "2025-01-06"

# Download analytics report
asc analytics get --app "$ASC_APP_ID" --date "2025-01-01" --frequency DAILY

# Performance metrics
asc performance metrics --app "$ASC_APP_ID"
```

## Workflow: Finance Reports

```bash
# Download financial report
asc finance download --vendor "VENDOR_NUMBER" --report-type FINANCIAL --region ZZ --period "2025-01"

# See available regions
asc finance regions
```

## Workflow: In-App Purchases & Subscriptions

```bash
# List IAPs
asc iap list --app "$ASC_APP_ID"

# List subscription groups
asc subscriptions groups list --app "$ASC_APP_ID"
```

## Workflow: Xcode Cloud

```bash
# List workflows
asc xcode-cloud workflows list --app "$ASC_APP_ID"

# Trigger a build
asc xcode-cloud builds create --workflow "WORKFLOW_ID" --confirm
```

## Global Flags (available on all commands)

| Flag | Description |
|---|---|
| `--api-debug` | HTTP request/response logging (redacts secrets) |
| `--debug` | Debug logging to stderr |
| `--profile NAME` | Use named auth profile |
| `--output json\|table\|markdown` | Output format |
| `--pretty` | Pretty-print JSON |
| `--paginate` | Fetch all pages |
| `--limit N` | Max results per page |
| `--confirm` | Required for destructive operations |
| `--strict-auth` | Fail on mixed credential sources |
| `--report junit` | CI report output |

## Environment Variables

| Variable | Purpose |
|---|---|
| `ASC_APP_ID` | Default app ID (skip `--app` on every command) |
| `ASC_PROFILE` | Default auth profile name |
| `ASC_TIMEOUT` | API request timeout in seconds |
| `ASC_SPINNER_DISABLED=1` | Disable interactive spinner (good for CI/logs) |
| `ASC_STRICT_AUTH=true` | Fail if credentials from multiple sources |
| `ASC_BYPASS_KEYCHAIN=1` | Skip keychain lookup |
| `ASC_DEBUG=api` | Enable HTTP debug logging |
| `ASC_MAX_RETRIES` | Max retry attempts for 429/503 |
| `ASC_BASE_DELAY` | Retry base delay in ms |

## Getting Help

```bash
asc --help                          # All command groups
asc <command> --help                # Subcommands for a group
asc <command> <subcommand> --help   # Flags for a specific command
asc docs show reference             # Full offline command reference
asc docs show api-notes             # API quirks and tips
asc init                            # Generate ASC.md reference in current repo
```

See `references/command-reference.md` for the full command catalog.
See `references/api-notes.md` for API quirks, date formats, and edge cases.
