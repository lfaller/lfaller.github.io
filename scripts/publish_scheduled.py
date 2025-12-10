#!/usr/bin/env python3
"""
Scheduled post publisher for GitHub Actions

This script runs daily at 8am ET and:
1. Checks all posts in _scheduled-posts/
2. Publishes posts with dates <= today to LinkedIn
3. Moves published posts to _posts/ for Jekyll
"""

import os
import sys
import shutil
from pathlib import Path
from datetime import datetime, timezone
import pytz
import subprocess
from dotenv import load_dotenv

# Load .env file if running locally
load_dotenv(Path(__file__).parent / '.env')

# Import our LinkedIn posting function
sys.path.insert(0, str(Path(__file__).parent))
from linkedin_post import (
    extract_frontmatter_and_content,
    extract_image_paths,
    markdown_to_linkedin,
    extract_category_hashtags,
    extract_html_comment_hashtags,
    register_image_upload,
    upload_image_binary,
    post_to_linkedin,
    extract_summary_from_metadata,
    generate_blog_url,
    build_blog_url,
    create_comment_on_post,
    is_tuesday_tactics_post
)

def parse_post_date(date_str):
    """Parse date from Jekyll frontmatter"""
    # Format: 2025-11-08 08:00:00 -0500
    # or: 2025-11-08 08:00:00
    try:
        # Try with timezone
        if '-0500' in date_str or '+' in date_str or '-' in date_str[-6:]:
            dt = datetime.strptime(date_str.rsplit(' ', 1)[0], '%Y-%m-%d %H:%M:%S')
            # Assume ET timezone
            et = pytz.timezone('America/New_York')
            dt = et.localize(dt)
        else:
            # No timezone, assume ET
            dt = datetime.strptime(date_str.strip(), '%Y-%m-%d %H:%M:%S')
            et = pytz.timezone('America/New_York')
            dt = et.localize(dt)
        return dt
    except Exception as e:
        print(f"Error parsing date '{date_str}': {e}")
        return None

def should_publish(post_date, now):
    """Check if post should be published (date/time <= now in ET)"""
    if post_date is None:
        return False

    # Both dates should be timezone-aware
    return post_date <= now

def publish_post_to_linkedin(post_path, access_token, author_id):
    """Publish a single post to LinkedIn"""
    try:
        # Extract content
        metadata, content = extract_frontmatter_and_content(post_path)
        title = metadata.get('title', 'Untitled')
        categories = metadata.get('categories', '')
        post_filename = Path(post_path).name

        print(f"  Processing: {title}")

        # Check if this is a Tuesday Tactics post (skip comments for those)
        is_tt = is_tuesday_tactics_post(title, post_filename)
        should_add_comment = not is_tt
        blog_url = None

        if should_add_comment:
            # Generate blog URL for the comment
            url_parts = generate_blog_url(post_filename)
            if url_parts:
                blog_url = build_blog_url(url_parts, categories)

        # Extract images
        image_paths = extract_image_paths(content, post_path)
        if image_paths:
            print(f"    Found {len(image_paths)} image(s)")

        # Extract summary for LinkedIn post (if adding comment)
        if should_add_comment:
            summary = extract_summary_from_metadata(metadata)
            if summary:
                linkedin_text = summary
            else:
                print(f"    ⚠ No 'summary:' field in frontmatter - will use full content")
                linkedin_text, _ = markdown_to_linkedin(content)
        else:
            # Full content for Tuesday Tactics (they're short)
            linkedin_text, _ = markdown_to_linkedin(content)

        # Collect hashtags
        all_hashtags = []
        category_hashtags = extract_category_hashtags(categories)
        all_hashtags.extend(category_hashtags)

        # Remove duplicates
        seen = set()
        unique_hashtags = []
        for tag in all_hashtags:
            if tag.lower() not in seen:
                seen.add(tag.lower())
                unique_hashtags.append(tag)

        if unique_hashtags:
            linkedin_text += "\n\n" + " ".join(unique_hashtags)

        # Upload images
        image_assets = []
        if image_paths:
            print(f"    Uploading {len(image_paths)} image(s)...")
            for img_path in image_paths:
                success, upload_url, asset = register_image_upload(author_id, access_token)
                if not success:
                    print(f"      ✗ Failed to register: {asset}")
                    continue

                success, message = upload_image_binary(upload_url, img_path, access_token)
                if not success:
                    print(f"      ✗ Upload failed: {message}")
                    continue

                image_assets.append(asset)

            print(f"    ✓ Uploaded {len(image_assets)} image(s)")

        # Post to LinkedIn
        print(f"    Posting to LinkedIn...")
        success, message, post_urn = post_to_linkedin(author_id, access_token, linkedin_text, image_assets)

        if success:
            print(f"    ✓ {message}")

            # Create comment with link to full post (if applicable)
            if should_add_comment and blog_url and post_urn:
                print(f"    Adding comment with blog link...")
                comment_text = f"Read the full story on my blog:\n{blog_url}"
                success, msg = create_comment_on_post(post_urn, author_id, access_token, comment_text)
                if success:
                    print(f"    ✓ {msg}")
                else:
                    print(f"    ✗ {msg}")
                    # Don't fail publish on comment failure

            return True
        else:
            print(f"    ✗ {message}")
            return False

    except Exception as e:
        print(f"    ✗ Error publishing post: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("Scheduled LinkedIn Post Publisher")
    print("=" * 60)

    # Get credentials
    access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
    author_id = os.getenv('LINKEDIN_AUTHOR_ID')

    if not access_token or not author_id:
        print("\n✗ Error: Missing LinkedIn credentials")
        print("Required environment variables:")
        print("  - LINKEDIN_ACCESS_TOKEN")
        print("  - LINKEDIN_AUTHOR_ID")
        sys.exit(1)

    # Get current time in ET
    et = pytz.timezone('America/New_York')
    now = datetime.now(et)

    print(f"\nCurrent time (ET): {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # Find repository root
    repo_root = Path(__file__).parent.parent
    scheduled_dir = repo_root / '_scheduled-posts'
    posts_dir = repo_root / '_posts'

    if not scheduled_dir.exists():
        print(f"\n✓ No scheduled posts directory found. Nothing to do.")
        sys.exit(0)

    # Find all markdown files in scheduled posts
    scheduled_posts = list(scheduled_dir.glob('*.md'))

    # Exclude README
    scheduled_posts = [p for p in scheduled_posts if p.name != 'README.md']

    if not scheduled_posts:
        print(f"\n✓ No scheduled posts found. Nothing to do.")
        sys.exit(0)

    print(f"\nFound {len(scheduled_posts)} scheduled post(s)")
    print("-" * 60)

    published_count = 0

    for post_path in sorted(scheduled_posts):
        try:
            # Extract frontmatter to get date
            metadata, _ = extract_frontmatter_and_content(str(post_path))
            date_str = metadata.get('date', '')

            if not date_str:
                print(f"\n⚠ Skipping {post_path.name}: No date in frontmatter")
                continue

            post_date = parse_post_date(date_str)

            if post_date is None:
                print(f"\n⚠ Skipping {post_path.name}: Could not parse date '{date_str}'")
                continue

            print(f"\n📅 {post_path.name}")
            print(f"   Scheduled: {post_date.strftime('%Y-%m-%d %H:%M:%S %Z')}")

            if should_publish(post_date, now):
                print(f"   ✓ Ready to publish!")

                # Publish to LinkedIn
                success = publish_post_to_linkedin(str(post_path), access_token, author_id)

                if success:
                    # Move to _posts directory
                    dest_path = posts_dir / post_path.name
                    print(f"   Moving to {dest_path.relative_to(repo_root)}...")
                    shutil.move(str(post_path), str(dest_path))
                    print(f"   ✓ Published and moved!")
                    published_count += 1
                else:
                    print(f"   ✗ Failed to publish - keeping in scheduled posts")
            else:
                print(f"   ⏳ Not yet time to publish")

        except Exception as e:
            print(f"\n✗ Error processing {post_path.name}: {e}")
            continue

    print("\n" + "=" * 60)
    print(f"Published {published_count} post(s)")
    print("=" * 60)

if __name__ == '__main__':
    main()
