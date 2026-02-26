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

## Account

The dedicated customer care account is named **`customercare`** in himalaya.

All commands use `-a customercare` on the subcommand (not on `himalaya` itself):

```bash
himalaya envelope list -a customercare
himalaya message read -a customercare <ID>
himalaya template reply -a customercare <ID>
himalaya template send -a customercare
```

### Available Folders

- `INBOX` — incoming support emails
- `Sent Items` — sent replies
- `Archive` — processed/closed threads
- `Drafts` — saved drafts
- `Junk E-mail` — spam

---

## Workflow

### Step 1 — List Unread Support Emails

```bash
himalaya envelope list -a customercare --output json
```

Summarize for the user:
- Sender name and email
- Subject
- Date received
- One-line summary of content (read the message if needed)

### Step 2 — Read Full Email

```bash
himalaya message read -a customercare <EMAIL_ID>
```

Note for drafting:
- The user's exact question or complaint
- Any product features or issues mentioned
- Tone (frustrated, confused, friendly)
- Language of the email

### Step 3 — Draft the Reply

Before drafting, consult the Privacy AI knowledge base at `/Users/wangqi/disk/projects/acmeup_privacyai/knowledge/` for accurate product information:

- `features.json` — feature list and descriptions
- `description_v*.md` — app descriptions
- `whats_new.md` — recent updates
- `user_instruction*.txt` — how-to guides for users
- `manual/` — detailed user manual
- `review_reply_*.md` — tone and style examples for sensitive topics

**Never guess at product behavior — always look it up first.**

**Tone guidelines** (aligned with Aria's persona):
- Professional, warm, and reassuring
- Clear and jargon-free — the customer may not be technical
- Empathetic when addressing problems or complaints
- Concise — answer directly, then offer further help
- If the email is not in English, reply in the same language

**Draft format:**

```
Subject: Re: [Original Subject]

Hi [Customer Name / "there" if unknown],

[Empathetic opening if needed — acknowledge their issue]

[Direct answer / solution]

[Optional: additional tip or next step]

If you have any other questions, feel free to reach out — we're happy to help!

Best regards,
Privacy AI Support Team
```

### Step 4 — Present Draft for Approval

Always show the full draft before sending:

```
📧 Draft reply ready — please review:

To: sender@example.com
Subject: Re: [subject]

---
[full draft body]
---

Send this reply? (yes / edit / cancel)
```

Wait for explicit confirmation. If the user requests edits, update the draft and show it again before sending.

### Step 5 — Send on Approval

Get the reply template first (preserves `In-Reply-To` and `References` headers for proper threading):

```bash
himalaya template reply -a customercare <EMAIL_ID>
```

Then pipe the approved content to send:

```bash
cat << 'EOF' | himalaya template send -a customercare
From: <customercare address>
To: customer@example.com
Subject: Re: Original Subject
In-Reply-To: <original-message-id>
References: <original-message-id>

Hi [Name],

[Approved reply body]

Best regards,
Privacy AI Support Team
EOF
```

Confirm to the user after sending: recipient, subject, timestamp.

### Step 6 — Archive (Optional)

After replying, move the thread to Archive:

```bash
himalaya message move -a customercare <EMAIL_ID> "Archive"
```

---

## Searching Emails

```bash
# By sender
himalaya envelope list -a customercare from customer@example.com

# By subject keyword
himalaya envelope list -a customercare subject "Privacy AI"

# Unread only
himalaya envelope list -a customercare unseen
```

---

## Handling Common Scenarios

### Refund Requests
- Acknowledge warmly
- Check `manual/` for current refund policy
- Direct to App Store refund flow if applicable
- Escalate to the user if manual action is needed

### Bug Reports
- Thank them for the report
- If details are missing, ask for: device model, iOS version, steps to reproduce
- Confirm the team is investigating
- Do NOT promise specific fix timelines

### Feature Requests
- Acknowledge the idea positively
- Let them know feedback is valued
- Do not commit to roadmap items

### Angry / Frustrated Customers
- Lead with empathy, not defensiveness
- Acknowledge the frustration specifically
- Move quickly to a concrete solution or next step
- Offer the email thread as a direct follow-up channel

---

## Tips

- Read the full email before drafting — never assume from the subject line alone
- For multi-part questions, address each point in a numbered list
- If uncertain about a product fact, look it up in the knowledge base before writing
- Check `review_reply_*.md` for tone examples on difficult or sensitive topics
