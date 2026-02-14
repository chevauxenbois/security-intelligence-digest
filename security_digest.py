#!/usr/bin/env python3
"""
Security Intelligence Digest - Daily Security & AI News Aggregator
Fetches CVEs, security news, and AI regulations, then creates Notion entries with AI-powered summaries
"""

import os
import sys
import json
import yaml
import hashlib
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Set
import feedparser
import requests
from notion_client import Client

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
NVD_API_KEY = os.getenv('NVD_API_KEY', '')

# Load config.yaml
try:
    with open('config.yaml', 'r') as f:
        CONFIG = yaml.safe_load(f)
except Exception as e:
    logger.warning(f"Could not load config.yaml: {e}. Using defaults.")
    CONFIG = {
        'ai': {
            'model': 'llama-3.3-70b-versatile',
            'fallback_models': ['llama-3.1-70b-versatile', 'mixtral-8x7b-32768'],
            'temperature': 0.3,
            'max_tokens': 2000
        }
    }

# AI Configuration with fallbacks
GROQ_MODELS = [CONFIG['ai']['model']] + CONFIG['ai'].get('fallback_models', [])
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Persona-based prompt for AI summarization
SUMMARY_PROMPT_TEMPLATE = """Analyze this security/technology news item and create a comprehensive summary.

Article Title: {title}
Source: {source}
Content: {content}

Provide:

1. **WHAT** (2-3 sentences): Describe what happened in plain language. Include key technical details.

2. **WHY IT MATTERS** - Provide specific, actionable insights for each persona:

**For a Security Engineer (AI security company or focussed on AI)**:
- How does this impact AI security products, cloud infrastructure, or security engineering practices?
- What immediate actions should be taken?
- What are the technical implications?

**For a GRC (Governance, Risk, Compliance) Professional**:
- What are the compliance implications (GDPR, DPDPA, ISO 27001, SOC 2, etc.)?
- Does this require incident reporting or documentation?
- What audit trail or policy changes are needed?

**For a Data Privacy Officer**:
- What are the data protection implications?
- Does this affect PII/sensitive data handling?
- Are there breach notification requirements?

3. **ESTIMATED READ TIME**: Estimate how long it would take to read the original article (e.g., "3 min")

Format your response as JSON:
{{
  "what": "2-3 sentence description",
  "why_it_matters_security": "Detailed paragraph for security engineers",
  "why_it_matters_grc": "Detailed paragraph for GRC",
  "why_it_matters_privacy": "Detailed paragraph for data privacy",
  "estimated_read_time": "X min",
  "for_security_engineer": true/false,
  "for_grc": true/false,
  "for_data_privacy": true/false,
  "tags": ["tag1", "tag2", "tag3"],
  "region": ["Global", "India", "EU", "US", etc.]
}}

Be specific and actionable. Focus on "so what?" insights."""


class SecurityDigestCollector:
    """Main class for collecting and processing security intelligence"""

    def __init__(self):
        self.notion = Client(auth=NOTION_API_KEY) if NOTION_API_KEY else None
        self.groq_headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        self.seen_items: Set[str] = set()
        self.items: List[Dict] = []

    def generate_item_hash(self, title: str, source: str) -> str:
        """Generate unique hash for deduplication"""
        content = f"{title}{source}".lower().strip()
        return hashlib.md5(content.encode()).hexdigest()

    def fetch_rss_feed(self, url: str, category: str, source_name: str) -> List[Dict]:
        """Fetch and parse RSS feed"""
        logger.info(f"Fetching RSS feed: {source_name}")
        items = []

        try:
            feed = feedparser.parse(url)

            for entry in feed.entries[:5]:
                published = getattr(entry, 'published_parsed', None)
                if published:
                    pub_date = datetime(*published[:6])
                else:
                    pub_date = datetime.now()

                if (datetime.now() - pub_date).days > 1:
                    continue

                item = {
                    'title': entry.title,
                    'url': entry.link,
                    'content': entry.get('summary', entry.get('description', '')),
                    'published': pub_date.isoformat(),
                    'source': source_name,
                    'category': category
                }

                item_hash = self.generate_item_hash(item['title'], item['url'])
                if item_hash not in self.seen_items:
                    self.seen_items.add(item_hash)
                    items.append(item)

        except Exception as e:
            logger.error(f"Error fetching RSS feed {source_name}: {e}")

        logger.info(f"Fetched {len(items)} new items from {source_name}")
        return items

    def fetch_github_advisories(self) -> List[Dict]:
        """Fetch recent security advisories from GitHub"""
        logger.info("Fetching GitHub Security Advisories")
        items = []

        try:
            url = "https://api.github.com/advisories"
            params = {'per_page': 10, 'sort': 'published', 'direction': 'desc'}
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            advisories = response.json()

            for advisory in advisories:
                published = datetime.fromisoformat(advisory['published_at'].replace('Z', '+00:00'))
                if (datetime.now(published.tzinfo) - published).days > 1:
                    continue

                severity = advisory.get('severity', 'unknown').upper()
                if severity not in ['HIGH', 'CRITICAL']:
                    continue

                item = {
                    'title': f"{advisory.get('ghsa_id', 'GHSA')}: {advisory.get('summary', '')[:80]}",
                    'url': advisory.get('html_url', ''),
                    'content': advisory.get('description', ''),
                    'published': advisory['published_at'],
                    'source': 'GitHub Advisory',
                    'category': 'CVE',
                    'severity': f"{'🔴 Critical' if severity == 'CRITICAL' else '🟠 High'}"
                }

                item_hash = self.generate_item_hash(item['title'], item['url'])
                if item_hash not in self.seen_items:
                    self.seen_items.add(item_hash)
                    items.append(item)

        except Exception as e:
            logger.error(f"Error fetching GitHub advisories: {e}")

        logger.info(f"Fetched {len(items)} advisories from GitHub")
        return items

    def generate_ai_summary(self, item: Dict) -> Optional[Dict]:
        """Generate AI-powered summary using Groq with fallback models"""
        logger.info(f"Generating AI summary for: {item['title'][:50]}...")

        prompt = SUMMARY_PROMPT_TEMPLATE.format(
            title=item['title'],
            source=item['source'],
            content=item['content'][:2000]
        )

        # Try each model in order until one succeeds
        for model in GROQ_MODELS:
            try:
                logger.info(f"Trying model: {model}")
                
                payload = {
                    "model": model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a cybersecurity and AI governance expert. Provide detailed, actionable insights for security professionals, GRC teams, and data privacy officers."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": CONFIG['ai'].get('temperature', 0.3),
                    "max_tokens": CONFIG['ai'].get('max_tokens', 2000)
                }

                response = requests.post(
                    GROQ_API_URL,
                    headers=self.groq_headers,
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()

                result = response.json()
                content = result['choices'][0]['message']['content']

                # Parse JSON response
                if '```json' in content:
                    content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    content = content.split('```')[1].split('```')[0].strip()

                summary = json.loads(content)
                logger.info(f"✅ Successfully generated summary with model: {model}")
                return summary

            except requests.exceptions.HTTPError as e:
                logger.warning(f"Model {model} failed with HTTP error: {e}. Trying next model...")
                continue
            except Exception as e:
                logger.warning(f"Model {model} failed: {e}. Trying next model...")
                continue

        # If all models failed
        logger.error(f"All models failed to generate summary for: {item['title'][:50]}")
        return None

    def create_notion_entry(self, item: Dict, summary: Dict):
        """Create Notion database entry"""
        if not self.notion:
            logger.warning("Notion client not initialized, skipping entry creation")
            return

        logger.info(f"Creating Notion entry: {item['title'][:50]}...")

        try:
            why_it_matters = ""
            if summary.get('why_it_matters_security'):
                why_it_matters += f"**For Security Engineers:**\n{summary['why_it_matters_security']}\n\n"
            if summary.get('why_it_matters_grc'):
                why_it_matters += f"**For GRC Teams:**\n{summary['why_it_matters_grc']}\n\n"
            if summary.get('why_it_matters_privacy'):
                why_it_matters += f"**For Data Privacy Officers:**\n{summary['why_it_matters_privacy']}"

            properties = {
                "Title": {"title": [{"text": {"content": item['title'][:100]}}]},
                "Date": {"date": {"start": datetime.fromisoformat(item['published'].replace('Z', '+00:00')).strftime('%Y-%m-%d')}},
                "Category": {"select": {"name": item['category']}},
                "Source": {"url": item['url']},
                "Status": {"select": {"name": "🆕 New"}},
                "Digest Date": {"date": {"start": datetime.now().strftime('%Y-%m-%d')}},
                "For Security Engineer": {"checkbox": summary.get('for_security_engineer', True)},
                "For GRC": {"checkbox": summary.get('for_grc', False)},
                "For Data Privacy": {"checkbox": summary.get('for_data_privacy', False)},
                "Estimated Read Time": {"rich_text": [{"text": {"content": summary.get('estimated_read_time', '3 min')}}]}
            }

            if item.get('severity'):
                properties["Severity"] = {"select": {"name": item['severity']}}

            if summary.get('tags'):
                properties["Tags"] = {"multi_select": [{"name": tag} for tag in summary['tags'][:5]]}

            if summary.get('region'):
                properties["Region"] = {"multi_select": [{"name": region} for region in summary['region']]}

            children = [
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"type": "text", "text": {"content": "What Happened"}}]}
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": summary.get('what', 'No summary available')}}]}
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {"rich_text": [{"type": "text", "text": {"content": "Why It Matters"}}]}
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {"rich_text": [{"type": "text", "text": {"content": why_it_matters[:2000]}}]}
                }
            ]

            self.notion.pages.create(
                parent={"database_id": NOTION_DATABASE_ID},
                properties=properties,
                children=children
            )

            logger.info(f"✅ Created Notion entry successfully")

        except Exception as e:
            logger.error(f"Error creating Notion entry: {e}")

    def collect_all_sources(self):
        """Collect from all configured sources"""
        logger.info("=" * 50)
        logger.info("Starting Security Intelligence Collection")
        logger.info("=" * 50)

        rss_feeds = [
            ("https://krebsonsecurity.com/feed/", "News", "Krebs on Security"),
            ("https://www.bleepingcomputer.com/feed/", "News", "BleepingComputer"),
            ("https://feeds.feedburner.com/TheHackersNews", "News", "The Hacker News"),
            ("https://www.darkreading.com/rss.xml", "News", "Dark Reading"),
            ("https://cloud.google.com/feeds/kubernetes-engine-security-bulletins.xml", "Cloud", "GCP Security"),
        ]

        for url, category, source_name in rss_feeds:
            items = self.fetch_rss_feed(url, category, source_name)
            self.items.extend(items)

        gh_items = self.fetch_github_advisories()
        self.items.extend(gh_items)

        logger.info(f"\n{'=' * 50}")
        logger.info(f"Total items collected: {len(self.items)}")
        logger.info(f"{'=' * 50}\n")

    def process_and_publish(self):
        """Process items with AI and publish to Notion"""
        logger.info("Processing items with AI summarization...")

        items_to_process = self.items[:15]
        processed_count = 0

        for item in items_to_process:
            summary = self.generate_ai_summary(item)

            if summary:
                self.create_notion_entry(item, summary)
                processed_count += 1
            else:
                logger.warning(f"Skipping item due to summary generation failure: {item['title'][:50]}")

        logger.info(f"\n{'=' * 50}")
        logger.info(f"✅ Successfully processed {processed_count} items")
        logger.info(f"{'=' * 50}")

    def run(self):
        """Main execution method"""
        try:
            self.collect_all_sources()

            if not self.items:
                logger.info("No new items found. Exiting.")
                return

            self.process_and_publish()

        except Exception as e:
            logger.error(f"Fatal error in main execution: {e}")
            sys.exit(1)


if __name__ == "__main__":
    if not NOTION_API_KEY:
        logger.error("NOTION_API_KEY environment variable not set")
        sys.exit(1)

    if not NOTION_DATABASE_ID:
        logger.error("NOTION_DATABASE_ID environment variable not set")
        sys.exit(1)

    if not GROQ_API_KEY:
        logger.error("GROQ_API_KEY environment variable not set")
        sys.exit(1)

    collector = SecurityDigestCollector()
    collector.run()

    logger.info("\n🎉 Security Intelligence Digest completed successfully!")
