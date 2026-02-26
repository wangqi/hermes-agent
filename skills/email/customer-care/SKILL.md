---
name: customer-care
description: Manage Privacy AI customer care emails — read support emails, draft professional replies using product knowledge, and send only after user approval. Triggers on "customer email", "support email", "reply to customer", "customer care", "support inbox", "read support", "customer reply".
---

# Customer Care Email Management

Handle customer support emails for **Privacy AI**. The workflow is always:

1. **Read** — fetch and summarize unread/recent support emails
2. **Draft** — compose a reply informed by Privacy AI product knowledge
3. **Present** — show the draft to the user for review
4. **Send** — only after explicit approval

**NEVER send any email without showing the draft first and receiving explicit confirmation.**

---

## Account Setup

### Configure a Dedicated Support Account

If a separate customer care email account exists (e.g. `support@privacyai.app`), add it to himalaya:

```bash
himalaya account configure
```

This opens an interactive wizard. When done, the account will appear in:

```bash
himalaya account list
```

Use `--account support` (replace with actual account name) for all customer care operations:

```bash
himalaya --account support envelope list
```

If no separate account is configured yet, ask the user for the account details before proceeding.

### Identify the Support Account

```bash
himalaya account list
```

Look for the account associated with the customer care address. Use that account name in all commands below.

---

## Workflow

### Step 1 — Read Unread Support Emails

```bash
# List unread emails (adjust account name as needed)
himalaya --account support envelope list --output json

# Or list with filter for unread
himalaya --account support envelope list unseen
```

Summarize for the user:
- Sender name and email
- Subject
- Date received
- One-line summary of content

### Step 2 — Read Full Email

```bash
himalaya --account support message read <EMAIL_ID>
```

Note the following for drafting:
- The user's exact question or complaint
- Any product features or issues mentioned
- Tone (frustrated, confused, friendly)
- Whether it requires a direct answer, escalation, or follow-up

### Step 3 — Draft the Reply

Before drafting, consult the Privacy AI knowledge base at `/Users/wangqi/disk/projects/acmeup_privacyai/knowledge/` for accurate product information:

- `features.json` — feature list and descriptions
- `description_v*.md` — app descriptions
- `whats_new.md` — recent updates
- `user_instruction*.txt` — how-to guides for users
- `manual/` — detailed user manual
- `review_reply_*.md` — example review reply tone and style

**Tone guidelines** (aligned with Aria's persona):
- Professional, warm, and reassuring
- Clear and jargon-free — the customer may not be technical
- Empathetic when addressing problems or complaints
- Accurate — never guess at product behavior; look it up first
- Concise — get to the answer quickly, then offer further help

**Draft format:**

```
Subject: Re: [Original Subject]

Hi [Customer Name / "there" if unknown],

[Empathetic opening if needed — acknowledge their issue]

[Direct answer to their question / solution to their problem]

[Optional: additional tip or next step]

If you have any other questions, feel free to reach out — we're happy to help!

Best regards,
Privacy AI Support Team
```

### Step 4 — Present Draft for Approval

Always show the full draft to the user before sending:

```
📧 Draft reply ready — please review:

**To:** sender@example.com
**Subject:** Re: [subject]

---
[full draft body]
---

Send this reply? (yes / edit / cancel)
```

Wait for explicit confirmation. If the user wants edits, incorporate them and show the revised draft again before sending.

### Step 5 — Send on Approval

Once approved, send using himalaya's non-interactive pipe method:

```bash
# Get the reply template (preserves In-Reply-To and References headers)
himalaya --account support template reply <EMAIL_ID>
```

Then send with the approved body:

```bash
cat << 'EOF' | himalaya --account support template send
From: support@privacyai.app
To: customer@example.com
Subject: Re: Original Subject
In-Reply-To: <original-message-id>
References: <original-message-id>

Hi [Name],

[Approved reply body here]

Best regards,
Privacy AI Support Team
EOF
```

After sending, confirm to the user with the timestamp and recipient.

### Step 6 — Optional: Archive / Label

After replying, optionally move the email to an "Answered" or archive folder:

```bash
himalaya --account support message move <EMAIL_ID> "Archive"
```

---

## Searching Support Emails

Find emails from a specific sender:

```bash
himalaya --account support envelope list from customer@example.com
```

Search by subject keyword:

```bash
himalaya --account support envelope list subject "Privacy AI"
```

Search with date range:

```bash
himalaya --account support envelope list since 2024-01-01
```

---

## Handling Common Scenarios

### Refund Requests
- Acknowledge the request warmly
- Explain the refund process (check `manual/` for current policy)
- Direct them to the App Store refund flow if applicable
- Escalate to the user if a manual refund is needed

### Bug Reports
- Thank them for the report
- Ask for device, iOS version, and steps to reproduce if not provided
- Confirm the team is looking into it
- Do NOT promise specific fix timelines

### Feature Requests
- Acknowledge the idea positively
- Let them know feedback is valued
- Avoid committing to roadmap items

### Angry / Frustrated Customers
- Lead with empathy, not defensiveness
- Acknowledge the frustration specifically ("I completely understand how frustrating that must be")
- Move quickly to a solution or next step
- Offer a direct channel (email thread) for follow-up

---

## Tips

- Always read the original email fully before drafting — do not assume from the subject line alone
- If the email is in a language other than English, reply in the same language
- Check `review_reply_*.md` in the knowledge base for tone examples on sensitive topics
- If uncertain about a product fact, say "let me verify this" and look it up before drafting
- For complex multi-part questions, address each point in a numbered list
