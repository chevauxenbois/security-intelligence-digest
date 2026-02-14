# 🛡️ Security Intelligence Digest

> **Stay ahead in cybersecurity with AI-powered daily digests of CVEs, security news, and AI regulations - delivered straight to your Notion workspace.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Notion API](https://img.shields.io/badge/Notion-API-black.svg)](https://developers.notion.com/)
[![Powered by Groq](https://img.shields.io/badge/AI-Groq-orange.svg)](https://groq.com/)

## 🌟 What Makes This Special?

Unlike traditional security newsletters that just dump headlines, **Security Intelligence Digest** provides:

✅ **AI-Powered Contextual Summaries** - Not just "what happened", but "why it matters to YOU"

✅ **Persona-Based Insights** - Tailored explanations for Security Engineers, GRC, and Data Privacy teams

✅ **100% Free & Open Source** - No subscriptions, no limits, runs on free tiers

✅ **Zero Setup Complexity** - GitHub Actions handles everything automatically

✅ **Beautiful Notion Integration** - Mobile-friendly, searchable, organized

✅ **Comprehensive Coverage** - CVEs, cloud security, AI regulations, compliance news

## 🎯 Perfect For

- **Security Engineers** - Stay updated on critical vulnerabilities and exploits
- **Founders & CTOs** - Monitor security landscape for your startup
- **GRC Professionals** - Track compliance requirements and regulations
- **Data Privacy Officers** - Keep up with privacy laws (GDPR, DPDPA, etc.)
- **Anyone in Cybersecurity** - Continuous learning and market awareness

## 🚀 Quick Start (5 Minutes)

### Prerequisites

- GitHub account (free)
- Notion account (free)
- Groq API key (free, no credit card)

### Setup Steps

1. **Fork this repository** and clone it locally

2. **Get your API keys**:
   - **Notion**: Create integration at notion.so/my-integrations
   - **Groq**: Sign up at console.groq.com
   - **NVD** (optional): Request at nvd.nist.gov/developers/request-an-api-key

3. **Create Notion database** using schema from `notion_database_schema.md`

4. **Configure GitHub Secrets** with your API keys

5. **Run workflow** manually from Actions tab

6. **Check Notion** for your digest ✨

**Full setup guide**: See `SETUP.md`

## 🏗️ Architecture

```
GitHub Actions (Free, runs daily)
        ↓
Data Collection (NVD, RSS feeds, GitHub Advisories)
        ↓
AI Summarization (Groq - Mixtral-8x7B)
        ↓
Notion Database (Beautiful, organized, searchable)
```

## 📊 Data Sources

**CVEs**: NVD, GitHub Advisory Database, CISA KEV

**News**: Krebs, BleepingComputer, The Hacker News, Dark Reading

**Cloud**: AWS, GCP, Azure security bulletins

**Research**: arXiv, Exploit-DB, CERT

**50+ sources total** - see docs for full list

## 🤖 AI Summarization

Powered by **Groq** (free) using **Mixtral-8x7B**:
- 128K context window
- Sub-second inference
- ~500K tokens/day free
- No credit card required

Each entry includes:
- What happened (plain language)
- Why it matters for Security Engineers
- Why it matters for GRC teams  
- Why it matters for Data Privacy
- Actionable next steps

## 📝 License

MIT License - Free to use, modify, and distribute.

## 🙏 Credits

Built with Notion API, Groq AI, NVD, and GitHub Actions.

**Made with ❤️ for the security community**

---

⭐ **Star this repo** if you find it useful!
