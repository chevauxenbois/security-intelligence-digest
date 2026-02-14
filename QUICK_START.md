# ⚡ Quick Start Guide

## 🎉 What You Have

A complete, production-ready security intelligence platform that will automatically deliver daily digests to Notion!

## 📁 Your Files

```
security-intelligence-digest/
├── README.md                  # Full documentation
├── SETUP.md                   # Detailed setup instructions
├── PROJECT_SUMMARY.md         # What this project does
├── QUICK_START.md            # This file
├── security_digest.py         # Main Python script
├── requirements.txt           # Python dependencies
├── config.yaml                # Configuration
├── .env.example               # Environment template
├── notion_database_schema.md  # Notion database design
├── .github/workflows/
│   └── daily-digest.yml       # GitHub Actions workflow
├── LICENSE                    # MIT License
└── CONTRIBUTING.md            # How to contribute
```

## 🚀 Next Steps (Choose Your Path)

### Path 1: Quick Deploy (20 minutes)
**Goal**: Get it running today

1. **Read**: `SETUP.md` (start to finish)
2. **Get keys**: Groq + Notion API keys
3. **Create**: Notion database using schema
4. **Fork**: This repo on GitHub
5. **Configure**: Add secrets to GitHub
6. **Test**: Run workflow manually
7. **Done**: Check Notion for entries!

### Path 2: Understand First (45 minutes)
**Goal**: Learn how everything works

1. **Read**: `PROJECT_SUMMARY.md` (overview)
2. **Read**: `README.md` (features & architecture)
3. **Review**: `security_digest.py` (the code)
4. **Review**: `notion_database_schema.md` (database design)
5. **Follow**: Path 1 above

### Path 3: Customize Before Deploy (60 minutes)
**Goal**: Tailor it to your needs

1. **Follow**: Path 2 above
2. **Edit**: `config.yaml` (add your RSS feeds)
3. **Edit**: `security_digest.py` (customize AI prompts)
4. **Edit**: `.github/workflows/daily-digest.yml` (change schedule)
5. **Deploy**: Follow Path 1

## 🔑 Required API Keys

### 1. Groq (Free, No Credit Card)
- **Get it**: [console.groq.com](https://console.groq.com/)
- **Used for**: AI-powered summaries
- **Free tier**: ~500K tokens/day (you'll use ~15K/day)

### 2. Notion (Free)
- **Get it**: [notion.so/my-integrations](https://www.notion.so/my-integrations)
- **Used for**: Creating digest entries
- **Free tier**: Generous limits for personal use

### 3. NVD (Optional, Recommended)
- **Get it**: [nvd.nist.gov/developers/request-an-api-key](https://nvd.nist.gov/developers/request-an-api-key)
- **Used for**: CVE data (higher rate limits)
- **Free**: Unlimited

## 💰 Total Cost

**$0/month** - Everything runs on free tiers!

- GitHub Actions: Free (2000 min/month, use ~5 min/month)
- Groq API: Free (~500K tokens/day)
- Notion: Free (personal plan)
- All data sources: Free (public APIs and RSS)

## ⏰ Time Investment

- **Setup**: 15-20 minutes (one-time)
- **Daily reading**: 10 minutes (automated delivery)
- **Maintenance**: 0 minutes (it just works!)

## 📱 How to Use (After Setup)

### Daily Routine

1. **Morning**: Open Notion mobile app
2. **Check**: "Today's Digest" view
3. **Read**: 10-15 items with AI summaries
4. **Mark**: Important items with Status
5. **Done**: Back to work, fully updated!

### Weekly Routine

1. **Review**: "This Week" view
2. **Archive**: Mark old items as Done
3. **Adjust**: Add/remove RSS feeds if needed

### Monthly Routine

1. **Review**: Monthly trends view
2. **Clean up**: Archive old entries
3. **Optimize**: Tweak AI prompts if needed

## 🆘 If You Get Stuck

### Quick Fixes

**"Notion API error"**
→ Check database ID and integration connection

**"Groq API error"**
→ Verify API key in GitHub Secrets

**"No items collected"**
→ Try running again (sources might be temporarily down)

### Get Help

1. **Check logs**: Actions tab → Failed run → View logs
2. **Read troubleshooting**: See SETUP.md section
3. **Search issues**: Check if solved before
4. **Ask community**: Open a GitHub Discussion
5. **Report bug**: Create an Issue with logs

## 🎯 Success Checklist

Before you start, make sure you have:

- [ ] GitHub account
- [ ] Notion account
- [ ] 20 minutes of uninterrupted time
- [ ] Basic understanding of API keys

After setup, you should see:

- [ ] Green checkmark on GitHub Actions
- [ ] 10-15 entries in Notion database
- [ ] AI-generated summaries for each entry
- [ ] "Why it matters" section with persona insights

## 🎁 What You'll Get

**Daily** (automatically):
- 10-15 curated security items
- High/Critical CVEs only
- AI-powered contextual summaries
- Persona-based insights (Security/GRC/Privacy)
- Beautiful Notion entries
- 10-minute reading time

**Weekly**:
- ~70-100 items
- Searchable archive
- Trend visibility
- Continuous learning

**Monthly**:
- ~300-400 items
- Comprehensive security knowledge
- Market awareness
- Career growth

## 🚀 Ready?

**Start with SETUP.md and you'll be running in 20 minutes!**

Questions? Open the README.md for full documentation.

---

**You've got this! 💪**
