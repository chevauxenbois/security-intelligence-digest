# 🤝 Contributing to Security Intelligence Digest

Thank you for your interest in contributing! This project aims to be the **best open-source security digest tool**, and your contributions help make that happen.

## Ways to Contribute

### 1. Add Data Sources
Know a great security RSS feed or API? Add it to `config.yaml`:

```yaml
rss_feeds:
  - url: https://example.com/security-feed.xml
    category: News
    name: Example Security Blog
    priority: high
```

### 2. Improve AI Prompts
Help make the AI summaries more useful by improving prompts in `security_digest.py`.

### 3. Add Features
- Email notifications
- Slack integration
- Custom filtering rules
- Weekly reports

### 4. Fix Bugs
Check the [Issues](../../issues) tab for known bugs.

### 5. Improve Documentation
- Add screenshots
- Clarify setup steps
- Translate to other languages

## Development Setup

1. Fork and clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your keys
4. Run locally: `python security_digest.py`

## Pull Request Process

1. Create a new branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Test thoroughly
4. Commit with clear message: `git commit -m "Add: New RSS feed for X"`
5. Push and create PR

## Code Style

- Python: Follow PEP 8
- Comments: Explain "why", not "what"
- Functions: Single responsibility principle
- Keep it simple and readable

## Questions?

Open a [Discussion](../../discussions) or ask in an issue!

---

**Thank you for contributing! 🙏**
