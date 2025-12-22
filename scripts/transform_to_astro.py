#!/usr/bin/env python3
"""
Transform Jekyll blog posts to Astro format for cross-posting.

This script reads a Jekyll markdown post and transforms it to Astro format
with appropriate front matter mapping, field generation, and attribution.
"""

import sys
import os
import re
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Tuple, List
import yaml

# Custom YAML dumper to handle unquoted date strings
class UnquotedDumper(yaml.SafeDumper):
    """Custom YAML dumper that outputs date strings without quotes."""
    pass

def unquoted_str_representer(dumper, data):
    """Represent strings - let plain ISO dates stay unquoted."""
    # Check if string looks like an ISO 8601 datetime (starts with digit)
    # These should be output as plain scalars without quotes
    if data and isinstance(data, str) and data[0].isdigit():
        # Use style=None for plain scalar (no quotes)
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style=None)
    # For other strings, use default quoting
    return dumper.represent_scalar('tag:yaml.org,2002:str', data)

UnquotedDumper.add_representer(str, unquoted_str_representer)

def extract_frontmatter_and_content(file_path: str) -> Tuple[Dict, str]:
    """Extract frontmatter and content from a Jekyll markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split frontmatter and content
    parts = content.split('---', 2)
    if len(parts) < 3:
        raise ValueError("Invalid markdown file: missing frontmatter")

    frontmatter_text = parts[1].strip()
    body = parts[2].strip()

    # Parse YAML frontmatter
    try:
        frontmatter = yaml.safe_load(frontmatter_text)
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML frontmatter: {e}")

    return frontmatter, body


def generate_slug(file_path: str, author: str = 'lina') -> str:
    """
    Generate slug from filename in format: YYYYMMDD_{description}_{author}

    Handles both formats:
    - Old Jekyll format: 2025-11-27-thanksgiving-in-biotech.md
      → 20251127_thanksgiving-in-biotech_lina
    - New format: 20251127_thanksgiving-in-biotech_lina.md
      → 20251127_thanksgiving-in-biotech_lina
    """
    filename = Path(file_path).stem

    # Check if it's already in new format
    if '_' in filename and len(filename.split('_')[0]) == 8:
        # Already in new format (YYYYMMDD_...)
        return filename

    # Convert from Jekyll format: YYYY-MM-DD-slug-name
    parts = filename.split('-', 3)  # Split into [YYYY, MM, DD, rest]

    if len(parts) >= 4 and parts[0].isdigit() and len(parts[0]) == 4:
        # Valid Jekyll date format
        year = parts[0]
        month = parts[1]
        day = parts[2]
        description = parts[3]  # Everything after the date

        # Convert to new format
        return f"{year}{month}{day}_{description}_{author}"

    # Fallback: return as-is if we can't parse it
    return filename


def extract_excerpt(content: str, max_length: int = 200, post_title: str = None) -> str:
    """
    Extract excerpt from post content.
    Takes first real paragraph (skipping images and title duplicates) and truncates to max_length.
    """
    # Remove image markdown syntax
    content_no_images = re.sub(r'!\[.*?\]\(.*?\)', '', content)

    # Split by paragraphs
    paragraphs = [p.strip() for p in content_no_images.split('\n\n') if p.strip()]

    if not paragraphs:
        return "Check out this post"

    excerpt = None
    for para in paragraphs:
        # Remove markdown formatting to get plain text for comparison
        cleaned = re.sub(r'\*\*([^*]+)\*\*', r'\1', para)  # Remove bold
        cleaned = re.sub(r'[*_`~]', '', cleaned).strip()  # Remove other markdown

        # Skip if paragraph is empty or is just the post title
        if not cleaned:
            continue
        if post_title and cleaned.lower() == post_title.lower():
            continue
        # Skip if it's just a list item continuation
        if cleaned.startswith('-'):
            continue
        # Use this paragraph if it's substantial
        if len(cleaned) > 15:
            excerpt = para
            break

    if not excerpt:
        excerpt = paragraphs[0]

    # Remove markdown formatting
    excerpt = re.sub(r'\*\*([^*]+)\*\*', r'\1', excerpt)  # Remove bold
    excerpt = re.sub(r'[*_`~]', '', excerpt)  # Remove other markdown emphasis
    excerpt = excerpt.replace('\n', ' ')  # Replace newlines with spaces
    excerpt = re.sub(r'\s+', ' ', excerpt).strip()  # Collapse whitespace

    # Truncate to max_length
    if len(excerpt) > max_length:
        excerpt = excerpt[:max_length].rsplit(' ', 1)[0] + '…'

    return excerpt


def extract_first_image(content: str, post_date: str = None) -> Tuple[str, str]:
    """
    Extract first image from content.
    Returns (image_path, image_alt_text).
    """
    # Look for markdown image syntax: ![alt](path)
    match = re.search(r'!\[([^\]]*)\]\(([^\)]+)\)', content)

    if match:
        alt_text = match.group(1) or "Featured image"
        image_path = match.group(2)

        # If path starts with /, keep as-is, otherwise adjust
        # Convert paths like /assets/images/posts/... to relative paths for Astro
        if image_path.startswith('/'):
            # For now, keep the original path - she'll need to handle image migration
            pass

        return image_path, alt_text

    # Fallback if no image found
    if post_date:
        return f"/images/posts/{post_date}-featured.png", "Featured image"
    return "/images/posts/featured.png", "Featured image"


def convert_date_format(jekyll_date: str) -> str:
    """
    Convert Jekyll date format to ISO 8601 with timezone offset.
    Jekyll: "2025-11-27 08:00:00 -0500"
    Astro: "2025-11-27T08:00:00-05:00"
    """
    try:
        # Jekyll format: "YYYY-MM-DD HH:MM:SS ±HHMM"
        # Example: "2025-11-27 08:00:00 -0500"
        parts = jekyll_date.strip().split()

        if len(parts) >= 3:
            date_part = parts[0]  # "2025-11-27"
            time_part = parts[1]  # "08:00:00"
            tz_part = parts[2]    # "-0500"

            # Convert timezone format from "-0500" to "-05:00"
            if tz_part.startswith('-') or tz_part.startswith('+'):
                sign = tz_part[0]
                tz_hours = tz_part[1:3]
                tz_mins = tz_part[3:5] if len(tz_part) > 3 else '00'
                tz_formatted = f"{sign}{tz_hours}:{tz_mins}"
                return f"{date_part}T{time_part}{tz_formatted}"

        # Fallback: just ensure it's ISO format with Z (UTC)
        date_part = jekyll_date.split()[0]
        time_part = jekyll_date.split()[1] if len(jekyll_date.split()) > 1 else '00:00:00'
        return f"{date_part}T{time_part}Z"
    except Exception as e:
        # Ultimate fallback
        date_part = jekyll_date.split()[0]
        time_part = jekyll_date.split()[1] if len(jekyll_date.split()) > 1 else '00:00:00'
        return f"{date_part}T{time_part}Z"


def transform_to_astro(
    jekyll_frontmatter: Dict,
    content: str,
    config: Dict = None,
    include_attribution: bool = True
) -> str:
    """
    Transform Jekyll post to Astro format.
    Returns the complete Astro markdown file content.
    """
    if config is None:
        config = {}

    # Extract key fields
    author_key = jekyll_frontmatter.get('author', 'unknown')
    title = jekyll_frontmatter.get('title', 'Untitled')
    date = jekyll_frontmatter.get('date', datetime.now().isoformat())
    categories = jekyll_frontmatter.get('categories', [])

    # Generate/extract fields
    # Map author first so we can use it for slug generation
    author_key = jekyll_frontmatter.get('author', 'unknown')
    author_mapping = config.get('author_mapping', {})
    if author_key in author_mapping:
        author_info = author_mapping[author_key]
        author_name = author_info.get('name', 'Lina L. Faller, PhD')
        author_linkedin = author_info.get('linkedin', '')
    else:
        author_name = 'Lina L. Faller, PhD'
        author_linkedin = config.get('default_linkedin_url', '')

    # Generate slug with author
    slug = generate_slug(config.get('source_file', ''), author=author_key)
    excerpt = extract_excerpt(content, post_title=title)
    image_path, image_alt = extract_first_image(content, slug.split('_')[0])
    publish_date = convert_date_format(date)

    # Build authors list
    authors = [{"name": author_name}]
    if author_linkedin:
        authors[0]['link'] = author_linkedin

    # Map categories to tags (Jekyll categories become BWIB tags)
    # Default category is "Quick Take"
    tags = []
    if isinstance(categories, list) and categories:
        # Convert each Jekyll category to a tag (lowercase with dashes)
        tags = [cat.lower().replace(' ', '-') for cat in categories]
    elif isinstance(categories, str) and categories:
        tags = [categories.lower().replace(' ', '-')]

    # If no tags extracted, use empty list
    if not tags:
        tags = []

    # Default category for cross-posts
    category = config.get('default_category', 'Quick Take')

    # Generate metadata
    metadata = {
        "title": title,
        "description": excerpt,
        "canonical": config.get('canonical_url_template', '').format(slug=slug) if config.get('canonical_url_template') else ''
    }

    # Build Astro frontmatter
    frontmatter = {
        "publishDate": publish_date,
        "title": title,
        "slug": slug,
        "excerpt": excerpt,
        "image": image_path,
        "imageAlt": image_alt,
        "imagePosition": "top",
        "authors": authors,
        "category": category,
        "tags": tags,
        "metadata": metadata
    }

    # Attribution is handled via canonical link in metadata, not in post content
    # The canonical URL in the frontmatter provides proper attribution and SEO credit

    # Convert frontmatter to YAML using our custom dumper to output dates unquoted
    yaml_output = yaml.dump(frontmatter, Dumper=UnquotedDumper, default_flow_style=False, sort_keys=False, allow_unicode=True)

    # Post-process to remove quotes from publishDate if it looks like an ISO 8601 date
    # This ensures Astro parses it as a date object, not a string
    yaml_output = re.sub(
        r"publishDate: '[^']*(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[+-]\d{2}:\d{2})[^']*'",
        r"publishDate: \1",
        yaml_output
    )

    # Build complete file
    astro_markdown = f"---\n{yaml_output}---\n\n{content}"

    return astro_markdown


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: transform_to_astro.py <jekyll_post_path> [--config config.json] [--output output.md]")
        sys.exit(1)

    jekyll_post_path = sys.argv[1]
    config_path = None
    output_path = None

    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--config' and i + 1 < len(sys.argv):
            config_path = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--output' and i + 1 < len(sys.argv):
            output_path = sys.argv[i + 1]
            i += 2
        else:
            i += 1

    # Load config if provided
    config = {}
    if config_path and os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)

    # Add source file to config for slug generation
    config['source_file'] = jekyll_post_path

    # Extract frontmatter and content
    try:
        frontmatter, content = extract_frontmatter_and_content(jekyll_post_path)
    except Exception as e:
        print(f"Error reading post: {e}", file=sys.stderr)
        sys.exit(1)

    # Transform to Astro format
    try:
        astro_markdown = transform_to_astro(frontmatter, content, config, include_attribution=True)
    except Exception as e:
        print(f"Error transforming post: {e}", file=sys.stderr)
        sys.exit(1)

    # Output result
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(astro_markdown)
        print(f"Transformed post written to {output_path}")
    else:
        print(astro_markdown)


if __name__ == '__main__':
    main()
