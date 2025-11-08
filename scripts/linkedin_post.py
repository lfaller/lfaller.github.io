#!/usr/bin/env python3
"""
LinkedIn-only posting script for GitHub Actions

This script reads a Jekyll markdown post and posts it to LinkedIn.
"""

import sys
import os
import re
import requests
from pathlib import Path
from dotenv import load_dotenv

def extract_frontmatter_and_content(file_path):
    """Extract frontmatter and content from a Jekyll markdown file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and content
    parts = content.split('---', 2)
    if len(parts) < 3:
        raise ValueError("Invalid markdown file: missing frontmatter")

    frontmatter = parts[1].strip()
    body = parts[2].strip()

    # Parse frontmatter
    metadata = {}
    for line in frontmatter.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            metadata[key.strip()] = value.strip().strip('"')

    return metadata, body

def markdown_to_linkedin(content):
    """Convert markdown to LinkedIn-friendly plain text"""
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Convert bold (**text** or __text__)
    content = re.sub(r'\*\*(.+?)\*\*', r'*\1*', content)
    content = re.sub(r'__(.+?)__', r'*\1*', content)

    # Convert italic (*text* or _text_)
    content = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', content)
    content = re.sub(r'_(.+?)_', r'\1', content)

    # Convert inline code (`code`)
    content = re.sub(r'`([^`]+)`', r'\1', content)

    # Convert links [text](url) to just the URL
    content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'\2', content)

    # Convert headers (## Header) to just text
    content = re.sub(r'^#{1,6}\s+(.+)$', r'\1', content, flags=re.MULTILINE)

    # Clean up bullet points
    content = re.sub(r'^\s*[-*+]\s+', '• ', content, flags=re.MULTILINE)

    # Remove extra blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip()

def extract_category_hashtags(categories):
    """Convert categories to hashtags"""
    if not categories:
        return []

    # Split by comma or space
    cat_list = re.split(r'[,\s]+', categories)

    # Convert to hashtags
    hashtags = []
    for cat in cat_list:
        cat = cat.strip()
        if cat:
            # Remove hyphens and make camelCase
            words = cat.split('-')
            hashtag = ''.join(word.capitalize() for word in words)
            hashtags.append(f'#{hashtag}')

    return hashtags

def post_to_linkedin(author_id, access_token, text):
    """Post text content to LinkedIn"""
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    payload = {
        "author": author_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        return True, "Post published successfully!"
    else:
        return False, f"Error {response.status_code}: {response.text}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python linkedin_post.py POST_FILE.md")
        sys.exit(1)

    post_file = sys.argv[1]

    # Load environment variables
    load_dotenv()
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    author_id = os.getenv('LINKEDIN_AUTHOR_ID')

    if not access_token or not author_id:
        print("Error: Missing LinkedIn credentials in environment variables")
        print("Required: LINKEDIN_ACCESS_TOKEN and LINKEDIN_AUTHOR_ID")
        sys.exit(1)

    # Extract post content
    print(f"Reading post: {post_file}")
    metadata, content = extract_frontmatter_and_content(post_file)

    title = metadata.get('title', 'Untitled')
    categories = metadata.get('categories', '')

    print(f"Title: {title}")
    print(f"Categories: {categories}")

    # Convert to LinkedIn format
    linkedin_text = markdown_to_linkedin(content)

    # Add hashtags
    hashtags = extract_category_hashtags(categories)
    if hashtags:
        linkedin_text += "\n\n" + " ".join(hashtags)

    print(f"\nLinkedIn post preview:")
    print("-" * 60)
    print(linkedin_text)
    print("-" * 60)

    # Post to LinkedIn
    print("\nPosting to LinkedIn...")
    success, message = post_to_linkedin(author_id, access_token, linkedin_text)

    if success:
        print(f"✓ {message}")
    else:
        print(f"✗ {message}")
        sys.exit(1)

if __name__ == '__main__':
    main()
