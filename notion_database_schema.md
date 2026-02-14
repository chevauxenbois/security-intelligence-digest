# Notion Database Schema for Security Digest

## Database: "Security Intelligence Feed"

### Properties (Columns)

| Property Name | Type | Description | Purpose |
|--------------|------|-------------|---------|
| **Title** | Title | Headline of the item | Main identifier |
| **Date** | Date | Publication/discovery date | Sorting & filtering |
| **Category** | Select | CVE / AI Security / News / Regulation / Cloud / GRC | Quick filtering |
| **Severity** | Select | 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low | Priority indication |
| **Source** | URL | Link to original article/CVE | Reference |
| **What** | Rich Text | Plain description of what happened | Context |
| **Why It Matters** | Rich Text | AI-generated relevance for personas | Key insight |
| **For Security Engineer** | Checkbox | Relevant to founding security engineer | Persona filter |
| **For GRC** | Checkbox | Relevant to GRC persona | Persona filter |
| **For Data Privacy** | Checkbox | Relevant to data privacy persona | Persona filter |
| **Tags** | Multi-select | AWS, Azure, GCP, India, EU, AI, LLM, etc. | Detailed filtering |
| **CVE ID** | Text | CVE identifier if applicable | Quick lookup |
| **CVSS Score** | Number | CVSS score if applicable | Risk assessment |
| **Status** | Select | 🆕 New / 👁️ Read / ⭐ Important / ✅ Done | Workflow |
| **Region** | Multi-select | Global, India, EU, US, China, UK | Geographic filter |
| **Estimated Read Time** | Text | "2 min" / "5 min" | Time management |
| **AI Summary Quality** | Select | ⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐ | Quality control |
| **Created** | Created time | Auto-generated timestamp | Tracking |
| **Digest Date** | Date | Which daily digest this belongs to | Batching |

---

## View Configurations

### 1. **Today's Digest** (Default View)
- **Filter**: Digest Date = Today
- **Sort**: Severity (Critical first), then Date (newest first)
- **Group by**: Category
- **Properties shown**: Title, Category, Severity, Why It Matters, Source

### 2. **By Persona - Security Engineer**
- **Filter**: For Security Engineer = ✓
- **Sort**: Date (newest first)
- **Group by**: Category
- **Properties shown**: Title, Severity, What, Why It Matters, Tags

### 3. **By Persona - GRC**
- **Filter**: For GRC = ✓
- **Sort**: Date (newest first)
- **Group by**: Region
- **Properties shown**: Title, Category, What, Why It Matters, Region

### 4. **By Persona - Data Privacy**
- **Filter**: For Data Privacy = ✓
- **Sort**: Date (newest first)
- **Group by**: Region
- **Properties shown**: Title, Category, What, Why It Matters, Region

### 5. **Critical Items Only**
- **Filter**: Severity = Critical OR CVSS Score >= 9.0
- **Sort**: Date (newest first)
- **Properties shown**: All

### 6. **AI Governance & Regulations**
- **Filter**: Category = Regulation OR Tags contains "AI Act"
- **Sort**: Date (newest first)
- **Group by**: Region
- **Properties shown**: Title, What, Why It Matters, Region, Source

### 7. **India-Specific**
- **Filter**: Region contains "India" OR Tags contains any of [DPDPA, RBI, SEBI, CERT-In]
- **Sort**: Date (newest first)
- **Properties shown**: Title, Category, What, Why It Matters, Source

### 8. **Reading List**
- **Filter**: Status = New OR Status = Important
- **Sort**: Severity, then Date
- **Properties shown**: Title, Category, Estimated Read Time, Why It Matters

### 9. **Archive - All Items**
- **Filter**: None (show all)
- **Sort**: Date (newest first)
- **Properties shown**: Title, Date, Category, Status

---

## Sample Entry

**Title**: CVE-2026-1234: Critical RCE in AWS Lambda Runtime

**Date**: 2026-02-14

**Category**: CVE

**Severity**: 🔴 Critical

**Source**: https://aws.amazon.com/security/security-bulletins/...

**What**:
A critical remote code execution vulnerability (CVSS 9.8) has been discovered in AWS Lambda's Python runtime versions 3.9-3.11. The vulnerability allows attackers to execute arbitrary code by exploiting a deserialization flaw in the Lambda event processing pipeline. AWS has released patches for all affected runtime versions.

**Why It Matters**:
- **For Security Engineers at guard0.ai**: If you're using AWS Lambda with Python runtimes for any of your security workflows, data processing, or API endpoints, this is an immediate action item. The RCE nature means attackers could potentially access your Lambda execution environment, including environment variables (which often contain secrets), access to AWS services via Lambda's IAM role, and potentially pivot to other resources. Action: Audit all Lambda functions using Python 3.9-3.11, update runtimes immediately, rotate any secrets that were accessible to these functions.

- **For GRC Teams**: This is a P0 incident requiring immediate disclosure assessment. Check if any Lambda functions process customer data or PII. If yes, this may trigger breach notification requirements under DPDPA (India) or GDPR (EU) depending on your deployment regions. Document the patch timeline for compliance audits.

- **For Data Privacy Officers**: High risk of data exfiltration if Lambda functions process sensitive data. Recommend immediate log analysis to detect any suspicious invocations in the past 30 days (estimated exposure window). May need to notify data subjects if evidence of exploitation is found.

**For Security Engineer**: ✓
**For GRC**: ✓
**For Data Privacy**: ✓

**Tags**: AWS, Lambda, Python, RCE, Cloud Security

**CVE ID**: CVE-2026-1234

**CVSS Score**: 9.8

**Status**: 🆕 New

**Region**: Global

**Estimated Read Time**: 3 min

**AI Summary Quality**: ⭐⭐⭐⭐⭐

**Digest Date**: 2026-02-14

---

## Mobile UX Considerations

### Notion Mobile App Optimizations:
1. **Title property**: Keep concise (under 80 chars) for mobile readability
2. **Why It Matters**: Use paragraphs with clear headings (bolded) for each persona
3. **Collapsible sections**: Use toggles in rich text for detailed technical info
4. **Quick filters**: Pre-configured views accessible via mobile sidebar
5. **Offline reading**: Notion syncs for offline access

### Reading Flow:
1. Open "Today's Digest" view
2. Scan titles + severity indicators
3. Open item → Read "Why It Matters" first
4. Click Source if need more detail
5. Mark Status as Read/Important

---

## API Integration Structure

### Notion Database Creation (Python)
```python
database = {
    "parent": {"page_id": parent_page_id},
    "title": [{"text": {"content": "Security Intelligence Feed"}}],
    "properties": {
        "Title": {"title": {}},
        "Date": {"date": {}},
        "Category": {
            "select": {
                "options": [
                    {"name": "CVE", "color": "red"},
                    {"name": "AI Security", "color": "purple"},
                    {"name": "News", "color": "blue"},
                    {"name": "Regulation", "color": "yellow"},
                    {"name": "Cloud", "color": "orange"},
                    {"name": "GRC", "color": "green"}
                ]
            }
        },
        "Severity": {
            "select": {
                "options": [
                    {"name": "🔴 Critical", "color": "red"},
                    {"name": "🟠 High", "color": "orange"},
                    {"name": "🟡 Medium", "color": "yellow"},
                    {"name": "🟢 Low", "color": "green"}
                ]
            }
        },
        "Source": {"url": {}},
        "What": {"rich_text": {}},
        "Why It Matters": {"rich_text": {}},
        "For Security Engineer": {"checkbox": {}},
        "For GRC": {"checkbox": {}},
        "For Data Privacy": {"checkbox": {}},
        "Tags": {
            "multi_select": {
                "options": [
                    {"name": "AWS", "color": "orange"},
                    {"name": "Azure", "color": "blue"},
                    {"name": "GCP", "color": "red"},
                    {"name": "India", "color": "default"},
                    {"name": "EU", "color": "blue"},
                    {"name": "AI", "color": "purple"},
                    {"name": "LLM", "color": "purple"},
                    {"name": "DPDPA", "color": "green"},
                    {"name": "RBI", "color": "green"},
                    {"name": "SEBI", "color": "green"}
                ]
            }
        },
        "CVE ID": {"rich_text": {}},
        "CVSS Score": {"number": {}},
        "Status": {
            "select": {
                "options": [
                    {"name": "🆕 New", "color": "blue"},
                    {"name": "👁️ Read", "color": "gray"},
                    {"name": "⭐ Important", "color": "yellow"},
                    {"name": "✅ Done", "color": "green"}
                ]
            }
        },
        "Region": {
            "multi_select": {
                "options": [
                    {"name": "Global", "color": "default"},
                    {"name": "India", "color": "orange"},
                    {"name": "EU", "color": "blue"},
                    {"name": "US", "color": "red"},
                    {"name": "China", "color": "red"},
                    {"name": "UK", "color": "purple"}
                ]
            }
        },
        "Estimated Read Time": {"rich_text": {}},
        "AI Summary Quality": {
            "select": {
                "options": [
                    {"name": "⭐⭐⭐⭐⭐", "color": "green"},
                    {"name": "⭐⭐⭐⭐", "color": "yellow"},
                    {"name": "⭐⭐⭐", "color": "orange"}
                ]
            }
        },
        "Created": {"created_time": {}},
        "Digest Date": {"date": {}}
    }
}
```

---

## Storage Considerations

### Space Calculation (Daily):
- **Entries per day**: 10-15 items
- **Average content size**: ~2KB per entry (title + summaries + metadata)
- **Daily storage**: ~30KB
- **Monthly storage**: ~900KB
- **Yearly storage**: ~11MB

### Notion Free Tier:
- **Block limit**: Not character-based; each page entry = multiple blocks
- **Realistic capacity**: 1000+ entries before hitting practical limits
- **Estimated runway**: 60-100 days of daily digests (manageable)

### Cleanup Strategy:
- **Archive old entries**: Move items older than 90 days to separate "Archive" database
- **Delete low-priority**: Remove "Low" severity items after 30 days
- **Keep critical**: Retain Critical/High items indefinitely

---

## Why This Schema Works

✅ **Readable in 10 minutes**: "Why It Matters" section is concise and persona-focused
✅ **Actionable**: Clear indication of who should care and why
✅ **Filterable**: Multiple views for different use cases
✅ **Mobile-friendly**: Notion app provides excellent mobile UX
✅ **Scalable**: Easy to archive and manage storage
✅ **Searchable**: Full-text search across all properties
✅ **Shareable**: Can share specific views with team members

This schema provides the foundation for a world-class security intelligence platform! 🚀
