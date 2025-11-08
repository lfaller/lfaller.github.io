# LinkedIn-Jekyll Cross-Posting Automation Project

## Project Overview
Automate the posting workflow for content that currently goes to both LinkedIn (1-2x per week) and personal website (linafaller.com, a Jekyll site hosted on GitHub Pages).

## Current Manual Process
1. Write post content
2. Post to LinkedIn with:
   - Hashtags (e.g., #datascience)
   - Picture/image
   - Unicode formatted text
3. Post to Jekyll website with:
   - Same content in Markdown format
   - Frontmatter (YAML header)
   - Category tags (e.g., "data-science" or "software-engineering")
   - NO hashtags
   - Same picture/image

## Problem
Doing this manually for each post is tedious and error-prone. Need automation.

## Research Findings

### LinkedIn API Capabilities
- **Official API exists**: LinkedIn provides OAuth 2.0 authenticated API endpoints
- **Personal profile posting**: Supported via `w_member_social` scope
- **Rate limits**: 25 posts per 24-hour period for personal profiles (more than sufficient for 1-2/week)
- **Token expiration**: Access tokens expire after 60 days, requiring refresh
- **Setup requirements**: 
  - Must create LinkedIn Developer App
  - Requires association with a LinkedIn Company Page (even for personal posting)
  - Need to verify the app
  - Request "Share on LinkedIn" product access

### Existing Solutions Evaluated
1. **IFTTT/Zapier**: Too limited - can only share article links, not full text posts with custom formatting
2. **n8n**: More flexible open-source automation, but overkill for this simple use case
3. **Jekyll social plugins**: Focus on RSS-based sharing, don't handle the markdown→unicode conversion or hashtag logic

### Decision: Custom Python Script
**Why custom code wins:**
- Full control over markdown→unicode conversion
- Handle hashtag removal/addition logic
- Category mapping between platforms
- Bidirectional workflow options
- Only needed for 1-2 posts/week (simple requirements)

## Implementation Plan

### Repository Structure
**Decision**: Keep in existing website repo (https://github.com/lfaller/lfaller.github.io)
**Reasoning**: 
- Natural coupling with _posts/ directory
- Simpler workflow
- Easier path management
- No cross-repo complexity needed

### Proposed Directory Structure
```
lfaller.github.io/
├── _posts/                    # Existing Jekyll posts
├── _config.yml               # Existing Jekyll config
├── scripts/                  # NEW - Automation scripts
│   ├── cross_poster.py       # Main posting script
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Template for credentials
│   └── README.md             # Usage documentation
├── .gitignore               # Update to exclude .env
└── ... (rest of Jekyll site)
```

### Technical Architecture

#### Option A: LinkedIn → Jekyll (Recommended)
**Workflow:**
1. Write post in simple text/markdown file or interactive prompt
2. Python script posts to LinkedIn (with hashtags, unicode formatting)
3. Same script creates Jekyll post (markdown, frontmatter, no hashtags)
4. Optionally auto-commit to Git

#### Option B: Jekyll → LinkedIn
**Workflow:**
1. Create Jekyll post with special frontmatter fields for LinkedIn
2. Script detects new post (Git hook or manual trigger)
3. Converts markdown to plain text/unicode
4. Adds hashtags from frontmatter
5. Posts to LinkedIn

**Recommendation**: Start with Option A (LinkedIn first) as it's simpler and matches current mental workflow.

### Core Script Components

```python
# Pseudo-code structure
class CrossPoster:
    def __init__(self, access_token, author_id):
        """Initialize with LinkedIn credentials"""
        
    def post_to_linkedin(self, text, image_path=None, hashtags=[]):
        """
        - Convert markdown to plain text
        - Add hashtags at end
        - Upload image if provided
        - Make API POST request
        - Return LinkedIn post URL
        """
        
    def create_jekyll_post(self, title, content, category, image_path=None):
        """
        - Generate frontmatter with date, title, categories
        - Remove hashtags from content
        - Keep markdown formatting
        - Save to _posts/ with proper naming (YYYY-MM-DD-title.md)
        """
        
    def cross_post(self, title, content, category, image_path, hashtags):
        """
        - Post to LinkedIn first
        - Create Jekyll post
        - Return both URLs/paths
        """
```

### Required Python Libraries
- `requests` - LinkedIn API calls
- `python-frontmatter` - Jekyll YAML frontmatter handling
- `python-dotenv` - Environment variable management
- `Pillow` (optional) - Image processing if needed
- `markdown` (optional) - Markdown to HTML/text conversion

### LinkedIn API Setup Steps
1. Go to LinkedIn Developer Portal
2. Create new app
3. Create/associate LinkedIn Company Page (requirement)
4. Request "Share on LinkedIn" product access
5. Verify app in settings
6. Get Client ID and Client Secret
7. Generate OAuth 2.0 access token with scopes: `openid`, `profile`, `w_member_social`
8. Get your LinkedIn author ID (via API call to `/v2/userinfo`)
9. Store credentials securely in .env file

### Security Considerations
- **Never commit credentials**: Add `.env` to `.gitignore`
- **Token storage**: Use environment variables
- **Token refresh**: Build in 60-day token refresh reminder/automation
- **API rate limits**: Built-in checks to stay under 25/day

### Content Format Mappings

#### LinkedIn Format
- Plain text or unicode formatting
- Hashtags included (#datascience #machinelearning)
- Images attached via API
- Emojis and unicode characters allowed

#### Jekyll Format
```yaml
---
layout: post
title: "Post Title Here"
date: 2025-11-08 14:30:00 -0500
categories: [data-science]
image: /assets/images/2025-11-08-post-image.jpg
---

Post content here in Markdown format.
No hashtags included.
```

## Next Steps for Implementation

1. **Setup Phase**:
   - Create `scripts/` directory in lfaller.github.io repo
   - Set up LinkedIn Developer App
   - Obtain API credentials
   - Create `.env.example` template

2. **Core Development**:
   - Write `cross_poster.py` with basic functionality
   - Implement LinkedIn API authentication
   - Build post creation functions
   - Add image handling

3. **Testing**:
   - Test with sample posts (not published)
   - Verify markdown→plain text conversion
   - Test Jekyll file creation with proper frontmatter
   - Validate image uploads

4. **Documentation**:
   - Write README with usage instructions
   - Document credential setup
   - Add example commands

5. **Enhancement** (Optional Future):
   - Add CLI arguments for easier use
   - Build interactive prompt mode
   - Add draft/scheduled posting
   - GitHub Actions integration

## Key Technical Details from Research

### LinkedIn API Endpoints
- Authentication: `https://www.linkedin.com/oauth/v2/authorization`
- Token exchange: `https://www.linkedin.com/oauth/v2/accessToken`
- Get author ID: `https://api.linkedin.com/v2/userinfo`
- Post creation: `https://api.linkedin.com/v2/ugcPosts` (older API) or `https://api.linkedin.com/rest/posts` (newer)
- Required headers: `Authorization: Bearer {token}`, `Content-Type: application/json`

### Sample LinkedIn API Post Request
```json
{
  "author": "urn:li:person:{AUTHOR_ID}",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {
        "text": "Post content here #hashtag"
      },
      "shareMediaCategory": "NONE"
    }
  },
  "visibility": {
    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
  }
}
```

## Questions to Resolve During Development
1. How to handle image uploads to LinkedIn API?
2. Should we store post history/mapping between LinkedIn and Jekyll?
3. Interactive mode vs. file-based input?
4. Auto-commit to Git or leave manual?
5. Error handling for API failures?

## Success Criteria
- Can post to LinkedIn and create Jekyll file with single command
- Proper hashtag handling (included on LinkedIn, removed from Jekyll)
- Correct markdown/unicode conversion
- Images properly handled on both platforms
- Credentials stored securely
- Simple enough to use regularly (1-2x per week)

## References
- GitHub Repo: https://github.com/lfaller/lfaller.github.io
- Website: https://linafaller.com
- LinkedIn Developer Portal: https://www.linkedin.com/developers/
- Jekyll Documentation: https://jekyllrb.com/docs/posts/
