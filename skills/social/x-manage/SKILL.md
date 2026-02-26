---
name: x-manage
description: Manage X (Twitter) account using xurl CLI. Post tweets, reply, like, repost, search, read timeline, send DMs, follow/unfollow, and more. Triggers on "post tweet", "tweet", "reply to tweet", "x post", "x reply", "twitter", "like tweet", "repost", "x timeline", "x mentions", "x dm", "manage x", "x account".
---

# X Account Management via xurl

Use the `xurl` CLI tool (installed at `/opt/homebrew/bin/xurl`) to interact with the X API directly. xurl handles OAuth authentication and provides a clean interface for all X operations.

## Prerequisites: First-Time Setup

Before any X operations work, the user must authenticate xurl with their X API credentials.

### Step 1: Get X API Credentials

The user needs a developer app at https://developer.x.com:
1. Create a project and app
2. Enable OAuth 2.0 with User Authentication
3. Set callback URL to `http://localhost:8080/callback`
4. Copy **Client ID** and **Client Secret**

Ask the user for their Client ID and Client Secret using `AskUserQuestion`.

### Step 2: Register the App

```bash
xurl auth apps add my-app --client-id CLIENT_ID --client-secret CLIENT_SECRET
```

### Step 3: Authenticate (opens browser)

```bash
xurl auth login
```

This opens a browser for OAuth login. The user must complete it.

### Step 4: Verify

```bash
xurl whoami
```

Should show the authenticated user's profile. If it works, setup is complete.

---

## Commands Reference

### Post & Interact

```bash
# Post a new tweet
xurl post "Hello world!"

# Reply to a tweet (need tweet ID from URL)
xurl reply TWEET_ID "Your reply here"

# Quote a tweet with comment
xurl quote TWEET_ID "Your comment"

# Like a tweet
xurl like TWEET_ID

# Unlike a tweet
xurl unlike TWEET_ID

# Repost (retweet)
xurl repost TWEET_ID

# Undo repost
xurl unrepost TWEET_ID

# Delete your own tweet
xurl delete TWEET_ID
```

### Read & Search

```bash
# Read a specific tweet
xurl read TWEET_ID

# Search recent posts
xurl search "search query" -n 20

# Show home timeline
xurl timeline

# Show your mentions
xurl mentions

# Show your profile
xurl whoami

# Look up a user
xurl user @username
```

### Social

```bash
# Follow a user
xurl follow @username

# Unfollow a user
xurl unfollow @username

# List followers
xurl followers

# List following
xurl following

# Mute a user
xurl mute @username

# Block a user
xurl block @username
```

### Direct Messages

```bash
# Send a DM
xurl dm @username "Your message"

# List recent DMs
xurl dms
```

### Bookmarks

```bash
# Bookmark a tweet
xurl bookmark TWEET_ID

# List bookmarks
xurl bookmarks

# Remove bookmark
xurl unbookmark TWEET_ID
```

---

## Extracting Tweet IDs

Tweet IDs come from the URL:
- `https://x.com/user/status/1234567890` → ID is `1234567890`
- `https://twitter.com/user/status/1234567890` → ID is `1234567890`

When the user provides a URL, extract the numeric ID at the end.

---

## Handling Responses

xurl returns JSON. Parse and present results in a readable way. For example:

- After `xurl post`, confirm with the tweet URL: `https://x.com/i/web/status/TWEET_ID`
- After `xurl whoami`, show name, handle, and follower count
- After `xurl timeline`, summarize recent posts
- After `xurl mentions`, list who mentioned the user and what they said

---

## Multiple Apps / Accounts

```bash
# List registered apps
xurl auth apps list

# Use a specific app for one request
xurl --app my-other-app post "Hello"

# Set a different default app
xurl auth default my-other-app
```

---

## Troubleshooting

- **Auth error**: Run `xurl auth login` again to refresh tokens
- **Rate limit**: X API has rate limits; wait and retry
- **App not found**: Run `xurl auth apps list` to see registered apps
- **xurl not found**: Install with `brew install --cask xdevplatform/tap/xurl`
