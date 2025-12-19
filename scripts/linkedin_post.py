#!/usr/bin/env python3
"""
LinkedIn-only posting script for GitHub Actions

This script reads a Jekyll markdown post and posts it to LinkedIn.
"""

import sys
import os
import re
import requests
import json
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

def text_to_unicode_bold(text):
    """Convert ASCII text to Unicode bold sans-serif"""
    # Unicode bold sans-serif mapping
    bold_map = {
        'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛',
        'I': '𝗜', 'J': '𝗝', 'K': '𝗞', 'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣',
        'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨', 'V': '𝗩', 'W': '𝗪', 'X': '𝗫',
        'Y': '𝗬', 'Z': '𝗭', 'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳',
        'g': '𝗴', 'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸', 'l': '𝗹', 'm': '𝗺', 'n': '𝗻',
        'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃',
        'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇', '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯',
        '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'
    }
    return ''.join(bold_map.get(c, c) for c in text)

def extract_html_comment_hashtags(content):
    """Extract hashtags from HTML comments like <!-- #DataScience #AI -->"""
    hashtags = []
    # Find all HTML comments
    comments = re.findall(r'<!--\s*(.*?)\s*-->', content, re.DOTALL)
    for comment in comments:
        # Extract hashtags from comment
        tags = re.findall(r'#\w+', comment)
        hashtags.extend(tags)
    return hashtags

def extract_image_paths(content, post_file_path):
    """Extract image paths from markdown and convert to absolute paths"""
    images = []

    # Find markdown image syntax: ![alt](path)
    matches = re.findall(r'!\[.*?\]\(([^\)]+)\)', content)

    for match in matches:
        image_path = match.strip()

        # Convert Jekyll asset paths to absolute file paths
        if image_path.startswith('/assets/'):
            # /assets/images/posts/example.png -> /Users/.../lfaller.github.io/assets/images/posts/example.png
            repo_root = Path(post_file_path).parent.parent
            abs_path = repo_root / image_path.lstrip('/')
            if abs_path.exists():
                images.append(str(abs_path))
        elif image_path.startswith('http'):
            # Skip external URLs for now
            pass
        else:
            # Relative path from post directory
            post_dir = Path(post_file_path).parent
            abs_path = (post_dir / image_path).resolve()
            if abs_path.exists():
                images.append(str(abs_path))

    return images

def markdown_to_linkedin(content):
    """Convert markdown to LinkedIn-friendly plain text with Unicode formatting"""

    # Extract hashtags from HTML comments before removing them
    html_hashtags = extract_html_comment_hashtags(content)

    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # Remove image references (markdown and Jekyll asset paths)
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    content = re.sub(r'^/assets/.*$', '', content, flags=re.MULTILINE)

    # Convert bold (**text** or __text__) to Unicode bold
    def bold_replacer(match):
        return text_to_unicode_bold(match.group(1))

    content = re.sub(r'\*\*(.+?)\*\*', bold_replacer, content)
    content = re.sub(r'__(.+?)__', bold_replacer, content)

    # Convert italic (*text* or _text_) - remove formatting for now
    content = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', content)
    content = re.sub(r'_(.+?)_', r'\1', content)

    # Convert inline code (`code`) - remove backticks
    content = re.sub(r'`([^`]+)`', r'\1', content)

    # Convert links [text](url) to just the URL
    content = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'\2', content)

    # Convert headers (## Header) to Unicode bold
    def header_replacer(match):
        return text_to_unicode_bold(match.group(1))

    content = re.sub(r'^#{1,6}\s+(.+)$', header_replacer, content, flags=re.MULTILINE)

    # Clean up bullet points
    content = re.sub(r'^\s*[-*+]\s+', '• ', content, flags=re.MULTILINE)

    # Remove extra blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content.strip(), html_hashtags

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

def extract_summary_from_metadata(metadata):
    """Extract summary from post metadata.

    Posts should include a 'summary:' field in frontmatter for LinkedIn posts.
    This gives authors full control over the 1-2 sentence summary posted to LinkedIn.

    Example frontmatter:
        ---
        title: "My Post Title"
        summary: "Brief 1-2 sentence summary for LinkedIn. Should be under 280 characters."
        ---
    """
    return metadata.get('summary', None)

def generate_blog_url(post_filename, base_url='https://linafaller.com'):
    """Generate the full blog URL from post filename.

    Post format: YYYY-MM-DD-slug.md
    URL format: https://domain/category/year/month/day/slug
    """
    # Parse filename: 2025-12-04-five-signals-hire-data-person-now.md
    match = re.match(r'(\d{4})-(\d{2})-(\d{2})-(.+)\.md', post_filename)
    if not match:
        return None

    year, month, day, slug = match.groups()

    # We need the category from metadata, so we'll build a simple version
    # and let the caller pass category if needed
    # For now, return parts that can be assembled with category
    return {
        'year': year,
        'month': month,
        'day': day,
        'slug': slug,
        'base_url': base_url
    }

def build_blog_url(url_parts, category=''):
    """Build the full URL from url_parts dict and category."""
    if category:
        # Remove spaces/special chars from category for URL
        category = category.strip().lower().replace(' ', '-')
        return f"{url_parts['base_url']}/{category}/{url_parts['year']}/{url_parts['month']}/{url_parts['day']}/{url_parts['slug']}/"
    else:
        # Fallback without category
        return f"{url_parts['base_url']}/{url_parts['year']}/{url_parts['month']}/{url_parts['day']}/{url_parts['slug']}/"

def register_image_upload(author_id, access_token):
    """Step 1: Register an image upload with LinkedIn"""
    url = "https://api.linkedin.com/v2/assets?action=registerUpload"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    payload = {
        "registerUploadRequest": {
            "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
            "owner": author_id,
            "serviceRelationships": [{
                "relationshipType": "OWNER",
                "identifier": "urn:li:userGeneratedContent"
            }]
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        upload_url = data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
        asset = data['value']['asset']
        return True, upload_url, asset
    else:
        return False, None, f"Error {response.status_code}: {response.text}"

def upload_image_binary(upload_url, image_path, access_token):
    """Step 2: Upload the actual image binary to LinkedIn"""
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    with open(image_path, 'rb') as f:
        image_data = f.read()

    response = requests.post(upload_url, headers=headers, data=image_data)

    if response.status_code in [200, 201]:
        return True, "Image uploaded successfully"
    else:
        return False, f"Error {response.status_code}: {response.text}"

def post_to_linkedin(author_id, access_token, text, image_assets=None):
    """Step 3: Post text content (with optional images) to LinkedIn"""
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
    }

    # Base payload structure
    share_content = {
        "shareCommentary": {
            "text": text
        }
    }

    # Add images if provided
    if image_assets and len(image_assets) > 0:
        share_content["shareMediaCategory"] = "IMAGE"
        share_content["media"] = []

        for asset in image_assets:
            share_content["media"].append({
                "status": "READY",
                "media": asset
            })
    else:
        share_content["shareMediaCategory"] = "NONE"

    payload = {
        "author": author_id,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": share_content
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        data = response.json()
        post_id = data.get('id')
        # LinkedIn returns the ID as a share URN like "urn:li:share:1234567890"
        # The comments API expects this share URN directly
        post_urn = post_id if post_id else None
        return True, "Post published successfully!", post_urn
    else:
        return False, f"Error {response.status_code}: {response.text}", None


def is_tuesday_tactics_post(title, filename):
    """Check if this is a Tuesday Tactics post (should skip comments)"""
    return 'tuesday' in title.lower() or 'tuesday-tactics' in filename.lower()

def validate_post_length(text, limit=3000):
    """Validate post text length against LinkedIn's character limit.

    Args:
        text: The post text to validate
        limit: Character limit (default 3000 for LinkedIn)

    Returns:
        Tuple of (is_valid: bool, char_count: int, over_by: int or None)
    """
    char_count = len(text)
    is_valid = char_count <= limit
    over_by = None if is_valid else (char_count - limit)
    return is_valid, char_count, over_by

def build_hybrid_linkedin_post(full_content, summary, blog_url, categories, html_hashtags=None):
    """Build LinkedIn post text using hybrid approach.

    Strategy:
    1. Try full converted content + hashtags first
    2. If exceeds 3000 chars and summary exists, fall back to summary + hashtags
    3. If still too long, truncate intelligently

    Args:
        full_content: Full markdown converted to LinkedIn format
        summary: Summary from frontmatter (if available)
        blog_url: The full blog URL
        categories: Categories string for hashtag extraction
        html_hashtags: List of hashtags from HTML comments

    Returns:
        Tuple of (post_text: str, used_full_content: bool, char_count: int)
    """
    if html_hashtags is None:
        html_hashtags = []

    # Collect and deduplicate all hashtags
    all_hashtags = []
    seen = set()

    # Add HTML comment hashtags first
    for tag in html_hashtags:
        tag_lower = tag.lower()
        if tag_lower not in seen:
            all_hashtags.append(tag)
            seen.add(tag_lower)

    # Add category hashtags
    category_hashtags = extract_category_hashtags(categories)
    for tag in category_hashtags:
        tag_lower = tag.lower()
        if tag_lower not in seen:
            all_hashtags.append(tag)
            seen.add(tag_lower)

    hashtags_str = " ".join(all_hashtags)

    # Try full content first
    if full_content:
        full_post = full_content
        if blog_url:
            full_post += f"\n\nRead the whole story here:\n{blog_url}"
        if hashtags_str:
            full_post += f"\n\n{hashtags_str}"

        is_valid, char_count, _ = validate_post_length(full_post)
        if is_valid:
            return full_post, True, char_count

    # Fall back to summary if full content is too long
    if summary:
        summary_post = summary
        if blog_url:
            summary_post += f"\n\nRead the whole story here:\n{blog_url}"
        if hashtags_str:
            summary_post += f"\n\n{hashtags_str}"

        is_valid, char_count, _ = validate_post_length(summary_post)
        if is_valid:
            return summary_post, False, char_count

        # If summary is still too long, just use summary + hashtags without URL
        summary_only = summary
        if hashtags_str:
            summary_only += f"\n\n{hashtags_str}"
        is_valid, char_count, _ = validate_post_length(summary_only)
        if is_valid:
            return summary_only, False, char_count

    # Last resort: just hashtags (shouldn't reach here in normal cases)
    fallback = hashtags_str if hashtags_str else "Post content too long for LinkedIn"
    is_valid, char_count, _ = validate_post_length(fallback)
    return fallback, False, char_count

def main():
    if len(sys.argv) < 2:
        print("Usage: python linkedin_post.py POST_FILE.md")
        sys.exit(1)

    post_file = sys.argv[1]
    post_filename = Path(post_file).name

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

    # Generate blog URL (will be included in post body)
    url_parts = generate_blog_url(post_filename)
    blog_url = None
    if url_parts:
        blog_url = build_blog_url(url_parts, categories)

    # Extract images before converting content
    image_paths = extract_image_paths(content, post_file)
    if image_paths:
        print(f"\nFound {len(image_paths)} image(s):")
        for img in image_paths:
            print(f"  - {img}")

    # Convert full markdown content to LinkedIn format
    full_linkedin_content, html_hashtags = markdown_to_linkedin(content)
    if full_linkedin_content:
        print(f"\n✓ Converted markdown content ({len(full_linkedin_content)} chars)")
    if html_hashtags:
        print(f"✓ Found HTML comment hashtags: {' '.join(html_hashtags)}")

    # Extract summary for LinkedIn post (fallback if full content is too long)
    summary = extract_summary_from_metadata(metadata)
    if summary:
        print(f"✓ Summary from frontmatter: {summary[:100]}...")
    else:
        print(f"⚠ No 'summary:' field in frontmatter (will use full content if it fits)")

    # Build LinkedIn post using hybrid approach
    linkedin_text, used_full, char_count = build_hybrid_linkedin_post(
        full_linkedin_content, summary, blog_url, categories, html_hashtags
    )

    # Show which version was used
    content_type = "Full content" if used_full else "Summary"
    print(f"\nBuilding LinkedIn post...")
    print(f"  Using: {content_type}")
    print(f"  Characters: {char_count}/3000")
    if char_count > 2700:
        print(f"  ⚠ Warning: Post is getting close to character limit")

    print(f"\nLinkedIn post preview:")
    print("-" * 60)
    print(linkedin_text)
    print("-" * 60)

    # Upload images to LinkedIn
    image_assets = []
    if image_paths:
        print(f"\nUploading {len(image_paths)} image(s) to LinkedIn...")
        for idx, img_path in enumerate(image_paths, 1):
            print(f"  [{idx}/{len(image_paths)}] Registering upload for {Path(img_path).name}...")

            # Step 1: Register upload
            success, upload_url, asset = register_image_upload(author_id, access_token)
            if not success:
                print(f"    ✗ Failed to register: {asset}")
                continue

            print(f"    ✓ Upload registered: {asset}")

            # Step 2: Upload binary
            print(f"    Uploading image binary...")
            success, message = upload_image_binary(upload_url, img_path, access_token)
            if not success:
                print(f"    ✗ Upload failed: {message}")
                continue

            print(f"    ✓ {message}")
            image_assets.append(asset)

        print(f"\n✓ Successfully uploaded {len(image_assets)} image(s)")

    # Post to LinkedIn
    print("\nPosting to LinkedIn...")
    success, message, post_urn = post_to_linkedin(author_id, access_token, linkedin_text, image_assets)

    if success:
        print(f"✓ {message}")
        if image_assets:
            print(f"✓ Posted with {len(image_assets)} image(s)")
    else:
        print(f"✗ {message}")
        sys.exit(1)

if __name__ == '__main__':
    main()
