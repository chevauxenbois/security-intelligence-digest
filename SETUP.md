# 📖 Complete Setup Guide

This guide will walk you through setting up your Security Intelligence Digest in about 15-20 minutes.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: Get API Keys](#step-1-get-api-keys)
3. [Step 2: Create Notion Database](#step-2-create-notion-database)
4. [Step 3: Fork and Configure Repository](#step-3-fork-and-configure-repository)
5. [Step 4: Test Your Setup](#step-4-test-your-setup)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- GitHub account (free)
- Notion account (free)
- 15-20 minutes of setup time

---

## Step 1: Get API Keys

### 1.1 Groq API Key (Required, Free)

1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Sign up with Google/GitHub (no credit card needed)
3. Click "API Keys" in left sidebar
4. Click "Create API Key"
5. Copy the key (starts with `gsk_...`)

**Important**: Save this key somewhere safe - you won't be able to see it again!

### 1.2 Notion API Key (Required, Free)

1. Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Click "+ New integration"
3. Name it "Security Digest" (or anything you like)
4. Select your workspace
5. Click "Submit"
6. Copy the "Internal Integration Token" (starts with `secret_...`)

### 1.3 NVD API Key (Optional, Recommended)

Without this key, you're limited to 5 requests per 30 seconds. With the key, you get 50 requests per 30 seconds.

1. Go to [https://nvd.nist.gov/developers/request-an-api-key](https://nvd.nist.gov/developers/request-an-api-key)
2. Enter your email address
3. Check your email for the API key
4. Copy the key

---

## Step 2: Create Notion Database

### 2.1 Create New Database

1. Open Notion
2. Click "+ New page" in your sidebar
3. Type `/database` and select "Database - Full page"
4. Name it "Security Intelligence Feed" (or your preference)

### 2.2 Configure Database Properties

You need to add these properties (columns):

**Basic Properties**:
- Title (already exists)
- Date (type: Date)
- Category (type: Select)
- Severity (type: Select)
- Source (type: URL)

**Content Properties**:
- What (type: Text)
- Why It Matters (type: Text)

**Filtering Properties**:
- For Security Engineer (type: Checkbox)
- For GRC (type: Checkbox)
- For Data Privacy (type: Checkbox)
- Tags (type: Multi-select)
- Region (type: Multi-select)

**CVE Properties**:
- CVE ID (type: Text)
- CVSS Score (type: Number)

**Status Properties**:
- Status (type: Select)
- Digest Date (type: Date)
- Estimated Read Time (type: Text)
- AI Summary Quality (type: Select)
- Created (type: Created time)

**Detailed schema**: See `notion_database_schema.md` for exact configuration including Select options and colors.

### 2.3 Share Database with Integration

1. Click "..." (three dots) at top-right of your database
2. Scroll down to "Connections"
3. Click "+ Add connections"
4. Find and select "Security Digest" (your integration name)
5. Click "Confirm"

### 2.4 Get Database ID

1. Copy the URL of your database page
2. The database ID is the 32-character code between the workspace name and the `?v=`:

```
https://www.notion.so/myworkspace/DATABASE_ID_IS_HERE?v=...
                                 ^^^^^^^^^^^^^^^^^^^^
```

Example:
```
https://www.notion.so/harsh/a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6?v=123
                         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                         This is your database ID
```

Copy just the 32-character ID (no dashes in between).

---

## Step 3: Fork and Configure Repository

### 3.1 Fork the Repository

1. Go to the repository: `https://github.com/YOUR_USERNAME/security-intelligence-digest`
2. Click "Fork" button (top-right)
3. Select your account
4. Wait for fork to complete

### 3.2 Add GitHub Secrets

1. Go to your forked repository
2. Click "Settings" tab
3. Click "Secrets and variables" → "Actions" in left sidebar
4. Click "New repository secret"

Add these secrets one by one:

**Secret 1: NOTION_API_KEY**
- Name: `NOTION_API_KEY`
- Value: Your Notion integration token (starts with `secret_`)

**Secret 2: NOTION_DATABASE_ID**
- Name: `NOTION_DATABASE_ID`
- Value: Your 32-character database ID

**Secret 3: GROQ_API_KEY**
- Name: `GROQ_API_KEY`
- Value: Your Groq API key (starts with `gsk_`)

**Secret 4: NVD_API_KEY** (Optional)
- Name: `NVD_API_KEY`
- Value: Your NVD API key (if you got one)

### 3.3 Verify Secrets

After adding all secrets, you should see them listed (values are hidden for security).

---

## Step 4: Test Your Setup

### 4.1 Run Workflow Manually

1. Go to "Actions" tab in your repository
2. Click "Daily Security Intelligence Digest" workflow
3. Click "Run workflow" dropdown (right side)
4. Click green "Run workflow" button
5. Wait 2-3 minutes for completion

### 4.2 Check Results

**In GitHub**:
- Workflow should show green checkmark ✅
- Click on the run to see logs

**In Notion**:
- Open your "Security Intelligence Feed" database
- You should see 10-15 new entries!
- Each entry should have:
  - Title, Date, Category, Severity
  - "What" section with description
  - "Why It Matters" section with persona insights
  - Source URL
  - Tags and other metadata

### 4.3 Celebrate! 🎉

If you see entries in Notion with AI-generated summaries, you're all set!

The workflow will now run automatically every day at 6:00 AM IST (00:30 UTC).

---

## Step 5: Customize (Optional)

### 5.1 Change Schedule

Edit `.github/workflows/daily-digest.yml`:

```yaml
schedule:
  - cron: '30 0 * * *'  # 6:00 AM IST
```

Use [crontab.guru](https://crontab.guru/) to generate different schedules.

### 5.2 Add More RSS Feeds

Edit `config.yaml` to add your preferred sources:

```yaml
rss_feeds:
  - url: https://example.com/feed.xml
    category: News
    name: Example Source
    priority: high
```

### 5.3 Customize AI Prompts

Edit `security_digest.py` and modify the `SUMMARY_PROMPT_TEMPLATE` to change how AI generates summaries.

---

## Troubleshooting

### "Notion API error: Invalid database ID"

**Solution**: Double-check your database ID. Make sure:
- It's exactly 32 characters
- No dashes, no extra spaces
- You've shared the database with your integration

### "Groq API error: Unauthorized"

**Solution**: Your Groq API key might be incorrect.
- Go to console.groq.com and generate a new key
- Update the `GROQ_API_KEY` secret in GitHub

### "No items collected"

**Solution**: This can happen if:
- No new security news in the last 24 hours (unlikely but possible)
- RSS feeds are temporarily down
- Try running the workflow again in a few hours

### Workflow fails with timeout

**Solution**: 
- NVD API might be slow without an API key
- Add the optional `NVD_API_KEY` secret
- Or disable NVD in config.yaml temporarily

### AI summaries are low quality

**Solution**:
- Groq free tier is usually excellent
- If you notice consistent issues, try:
  - Changing the model in config.yaml
  - Adjusting the temperature (lower = more consistent)
  - Modifying the prompt in security_digest.py

### Getting rate limited

**Solution**:
- Add NVD_API_KEY for higher CVE API limits
- Reduce number of RSS feeds in config.yaml
- Increase GitHub Actions schedule interval

---

## Getting Help

If you're stuck:

1. **Check the logs**: Actions tab → Click on failed run → View logs
2. **Search issues**: Check if someone else had the same problem
3. **Open an issue**: Provide logs and describe what you tried
4. **Community**: Ask in Discussions tab

---

## Next Steps

✅ Setup complete! Here's what to do next:

1. **Create Custom Views** in Notion:
   - View by Persona (Security / GRC / Privacy)
   - View by Severity (Critical only)
   - View by Region (India-specific)

2. **Set up Notion Mobile App**:
   - Download Notion app
   - Add "Security Intelligence Feed" to favorites
   - Read during commute or coffee breaks

3. **Share with Team**:
   - Share Notion database with colleagues
   - Assign different views to different roles

4. **Customize for Your Needs**:
   - Add industry-specific RSS feeds
   - Tweak AI prompts for your domain
   - Adjust categories and tags

---

**Enjoy your daily security digest! 🚀**
