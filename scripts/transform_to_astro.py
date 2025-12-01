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


def generate_slug(file_path: str) -> str:
    """
    Generate slug from filename.
    Example: 2025-11-27-thanksgiving-in-biotech.md -> 2025-11-27-thanksgiving-in-biotech
    """
    filename = Path(file_path).stem
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
    Convert Jekyll date format to ISO 8601 with timezone.
    Jekyll: "2025-11-27 08:00:00 -0500"
    Astro: "2025-11-27T08:00:00Z"
    """
    try:
        # Parse Jekyll date format
        dt = datetime.strptime(jekyll_date.split('-0')[0].split('-0500')[0].split('-')[0], '%Y-%m-%d %H:%M:%S' if 'T' not in jekyll_date else '%Y-%m-%dT%H:%M:%S')
        # For simplicity, convert to ISO format with Z
        # If it had timezone info, we'd preserve it, but Jekyll format loses it in conversion
        dt_str = jekyll_date.split()[0] + 'T' + jekyll_date.split()[1] + 'Z'
        return dt_str
    except Exception as e:
        # Fallback: just ensure it's ISO format
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
    slug = generate_slug(config.get('source_file', ''))
    excerpt = extract_excerpt(content, post_title=title)
    image_path, image_alt = extract_first_image(content, slug.split('-')[0])
    publish_date = convert_date_format(date)

    # Map author
    author_mapping = config.get('author_mapping', {})
    if author_key in author_mapping:
        author_info = author_mapping[author_key]
        author_name = author_info.get('name', 'Lina L. Faller, PhD')
        author_linkedin = author_info.get('linkedin', '')
    else:
        author_name = 'Lina L. Faller, PhD'
        author_linkedin = config.get('default_linkedin_url', '')

    # Build authors list
    authors = [{"name": author_name}]
    if author_linkedin:
        authors[0]['link'] = author_linkedin

    # Map category
    category_mapping = config.get('category_mapping', {})
    if isinstance(categories, list) and categories:
        category = category_mapping.get(categories[0], categories[0])
    elif isinstance(categories, str):
        category = category_mapping.get(categories, categories)
    else:
        category = "Deep Dive"

    # Generate tags from categories
    tags = []
    if isinstance(categories, list):
        tags = [category_mapping.get(cat, cat) for cat in categories]
    elif categories:
        tags = [category_mapping.get(categories, categories)]

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

    # Add attribution link if requested
    content_with_attribution = content
    if include_attribution:
        original_url = config.get('original_post_url_template', '').format(slug=slug)
        if original_url:
            attribution = f"\n\n---\n\n*Originally posted on [Lina L. Faller's blog]({original_url})*"
            content_with_attribution = content + attribution

    # Convert frontmatter to YAML
    yaml_output = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False, allow_unicode=True)

    # Build complete file
    astro_markdown = f"---\n{yaml_output}---\n\n{content_with_attribution}"

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
