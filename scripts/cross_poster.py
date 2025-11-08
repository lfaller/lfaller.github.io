#!/usr/bin/env python3
"""
LinkedIn-Jekyll Cross-Posting Automation

This script automates posting content to both LinkedIn and a Jekyll website.
It handles format conversion, hashtag management, and image uploads.

Usage:
    python cross_poster.py --title "My Post" --content "Content here" --category data-science --hashtags datascience machinelearning
    python cross_poster.py --file post.md --category software-engineering --image image.jpg --hashtags coding python

Author: Lina Faller
"""

import os
import sys
import re
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict, Tuple
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class CrossPoster:
    """Handles cross-posting between LinkedIn and Jekyll website"""

    def __init__(self, validate_credentials: bool = True):
        """Initialize with credentials from environment variables

        Args:
            validate_credentials: If True, raise error if LinkedIn credentials missing
        """
        self.access_token = os.getenv('LINKEDIN_ACCESS_TOKEN')
        self.author_id = os.getenv('LINKEDIN_AUTHOR_ID')
        self.client_id = os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = os.getenv('LINKEDIN_CLIENT_SECRET')

        # Directory paths (relative to repo root)
        self.repo_root = Path(__file__).parent.parent
        self.posts_dir = self.repo_root / os.getenv('JEKYLL_POSTS_DIR', '_posts')
        self.assets_dir = self.repo_root / os.getenv('JEKYLL_ASSETS_DIR', 'assets/images')

        # LinkedIn API endpoints
        self.linkedin_api_base = "https://api.linkedin.com"
        self.linkedin_post_endpoint = f"{self.linkedin_api_base}/v2/ugcPosts"
        self.linkedin_asset_endpoint = f"{self.linkedin_api_base}/v2/assets"

        # Validate credentials if requested
        if validate_credentials and (not self.access_token or not self.author_id):
            raise ValueError(
                "Missing LinkedIn credentials. Please set LINKEDIN_ACCESS_TOKEN and "
                "LINKEDIN_AUTHOR_ID in your .env file."
            )

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for LinkedIn API requests"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }

    def _markdown_to_plain_text(self, text: str) -> str:
        """
        Convert markdown to plain text suitable for LinkedIn.
        Preserves basic formatting using unicode characters.
        """
        # Convert markdown bold to unicode bold (simplified - just remove markdown syntax)
        # LinkedIn accepts plain text, so we'll keep it simple
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Remove bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)  # Remove italic
        text = re.sub(r'`(.+?)`', r'\1', text)  # Remove code formatting

        # Convert markdown links [text](url) to "text (url)"
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1 (\2)', text)

        # Remove markdown headers
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)

        return text.strip()

    def _upload_image_to_linkedin(self, image_path: str) -> Optional[str]:
        """
        Upload an image to LinkedIn and return the asset URN.

        Args:
            image_path: Path to the image file

        Returns:
            Asset URN string or None if upload fails
        """
        try:
            # Step 1: Register upload
            register_upload_url = f"{self.linkedin_api_base}/v2/assets?action=registerUpload"

            register_payload = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": self.author_id,
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }

            response = requests.post(
                register_upload_url,
                headers=self._get_headers(),
                json=register_payload
            )
            response.raise_for_status()

            upload_data = response.json()
            upload_url = upload_data['value']['uploadMechanism'][
                'com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            asset_urn = upload_data['value']['asset']

            # Step 2: Upload the image binary
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

            upload_headers = {
                'Authorization': f'Bearer {self.access_token}'
            }

            upload_response = requests.put(
                upload_url,
                headers=upload_headers,
                data=image_data
            )
            upload_response.raise_for_status()

            print(f"Image uploaded successfully: {asset_urn}")
            return asset_urn

        except requests.exceptions.RequestException as e:
            print(f"Error uploading image to LinkedIn: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None

    def post_to_linkedin(
        self,
        text: str,
        image_path: Optional[str] = None,
        hashtags: Optional[List[str]] = None
    ) -> Optional[str]:
        """
        Post content to LinkedIn.

        Args:
            text: Post content (markdown will be converted to plain text)
            image_path: Optional path to image file
            hashtags: Optional list of hashtags (without # symbol)

        Returns:
            LinkedIn post URL or None if posting fails
        """
        try:
            # Convert markdown to plain text
            plain_text = self._markdown_to_plain_text(text)

            # Add hashtags at the end
            if hashtags:
                hashtag_string = ' '.join([f'#{tag}' for tag in hashtags])
                plain_text = f"{plain_text}\n\n{hashtag_string}"

            # Build the post payload
            post_payload = {
                "author": self.author_id,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": plain_text
                        },
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            # Handle image upload if provided
            if image_path and os.path.exists(image_path):
                asset_urn = self._upload_image_to_linkedin(image_path)
                if asset_urn:
                    post_payload["specificContent"]["com.linkedin.ugc.ShareContent"].update({
                        "shareMediaCategory": "IMAGE",
                        "media": [
                            {
                                "status": "READY",
                                "description": {
                                    "text": "Post image"
                                },
                                "media": asset_urn,
                                "title": {
                                    "text": "Image"
                                }
                            }
                        ]
                    })

            # Post to LinkedIn
            response = requests.post(
                self.linkedin_post_endpoint,
                headers=self._get_headers(),
                json=post_payload
            )
            response.raise_for_status()

            # Extract post ID from response
            post_id = response.headers.get('X-RestLi-Id', 'unknown')

            print(f"Successfully posted to LinkedIn!")
            print(f"Post ID: {post_id}")

            # LinkedIn post URLs are not directly returned, but we can construct an approximate one
            # Note: The actual URL may differ slightly
            return f"https://www.linkedin.com/feed/update/{post_id}"

        except requests.exceptions.RequestException as e:
            print(f"Error posting to LinkedIn: {e}")
            if hasattr(e.response, 'text'):
                print(f"Response: {e.response.text}")
            return None

    def _remove_hashtags(self, text: str) -> str:
        """Remove hashtags from text for Jekyll posts"""
        # Remove hashtags (lines that are primarily hashtags)
        lines = text.split('\n')
        filtered_lines = []

        for line in lines:
            # Skip lines that are only hashtags
            if line.strip() and not re.match(r'^[\s#\w]+$', line.strip()):
                filtered_lines.append(line)
            elif line.strip() and '#' not in line:
                filtered_lines.append(line)

        return '\n'.join(filtered_lines).strip()

    def _copy_image_to_assets(self, image_path: str, post_slug: str) -> Optional[str]:
        """
        Copy image to Jekyll assets directory.

        Args:
            image_path: Source image path
            post_slug: Slug for the post (used in image filename)

        Returns:
            Relative path to image from site root, or None if copy fails
        """
        try:
            # Create assets directory if it doesn't exist
            self.assets_dir.mkdir(parents=True, exist_ok=True)

            # Get file extension
            ext = Path(image_path).suffix

            # Create new filename with date and slug
            date_str = datetime.now().strftime('%Y-%m-%d')
            new_filename = f"{date_str}-{post_slug}{ext}"
            dest_path = self.assets_dir / new_filename

            # Copy file
            import shutil
            shutil.copy2(image_path, dest_path)

            # Return relative path from site root
            relative_path = f"/assets/images/{new_filename}"
            print(f"Image copied to: {dest_path}")

            return relative_path

        except Exception as e:
            print(f"Error copying image: {e}")
            return None

    def create_jekyll_post(
        self,
        title: str,
        content: str,
        category: str,
        image_path: Optional[str] = None
    ) -> Optional[str]:
        """
        Create a Jekyll post file.

        Args:
            title: Post title
            content: Post content in markdown
            category: Category (e.g., 'data-science', 'software-engineering')
            image_path: Optional path to post image

        Returns:
            Path to created post file, or None if creation fails
        """
        try:
            # Create posts directory if it doesn't exist
            self.posts_dir.mkdir(parents=True, exist_ok=True)

            # Generate slug from title
            slug = re.sub(r'[^\w\s-]', '', title.lower())
            slug = re.sub(r'[-\s]+', '-', slug).strip('-')

            # Generate filename with date
            date_str = datetime.now().strftime('%Y-%m-%d')
            filename = f"{date_str}-{slug}.md"
            filepath = self.posts_dir / filename

            # Remove hashtags from content
            clean_content = self._remove_hashtags(content)

            # Build frontmatter manually to preserve order
            # Format: YYYY-MM-DD HH:MM:SS -0500 (Eastern Time)
            date_formatted = datetime.now().strftime('%Y-%m-%d %H:%M:%S -0500')

            # Start with required fields in the correct order
            frontmatter_lines = [
                '---',
                'layout: post',
                'author: lina',
                f'title:  "{title}"',
                f'date:   {date_formatted}',
                f'categories: {category}'
            ]

            # Handle image if provided
            if image_path and os.path.exists(image_path):
                image_url = self._copy_image_to_assets(image_path, slug)
                if image_url:
                    frontmatter_lines.append(f'image: {image_url}')

            frontmatter_lines.append('---')

            # Combine frontmatter and content
            full_content = '\n'.join(frontmatter_lines) + '\n\n' + clean_content

            # Write to file
            with open(filepath, 'w') as f:
                f.write(full_content)

            print(f"Jekyll post created: {filepath}")
            return str(filepath)

        except Exception as e:
            print(f"Error creating Jekyll post: {e}")
            return None

    def cross_post(
        self,
        title: str,
        content: str,
        category: str,
        image_path: Optional[str] = None,
        hashtags: Optional[List[str]] = None,
        linkedin_only: bool = False,
        jekyll_only: bool = False
    ) -> Tuple[Optional[str], Optional[str]]:
        """
        Post to both LinkedIn and Jekyll (or one platform only).

        Args:
            title: Post title
            content: Post content
            category: Jekyll category
            image_path: Optional image path
            hashtags: Optional list of hashtags for LinkedIn
            linkedin_only: Only post to LinkedIn
            jekyll_only: Only create Jekyll post

        Returns:
            Tuple of (linkedin_url, jekyll_path)
        """
        linkedin_url = None
        jekyll_path = None

        if not jekyll_only:
            print("\n--- Posting to LinkedIn ---")
            linkedin_url = self.post_to_linkedin(content, image_path, hashtags)

            if linkedin_url:
                print(f"LinkedIn URL: {linkedin_url}")
            else:
                print("LinkedIn posting failed!")

        if not linkedin_only:
            print("\n--- Creating Jekyll Post ---")
            jekyll_path = self.create_jekyll_post(title, content, category, image_path)

            if jekyll_path:
                print(f"Jekyll post: {jekyll_path}")
            else:
                print("Jekyll post creation failed!")

        return linkedin_url, jekyll_path


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Cross-post content to LinkedIn and Jekyll website'
    )

    # Content input options
    content_group = parser.add_mutually_exclusive_group(required=True)
    content_group.add_argument(
        '--content',
        help='Post content as string'
    )
    content_group.add_argument(
        '--file',
        help='Path to file containing post content (markdown)'
    )

    # Required arguments
    parser.add_argument(
        '--title',
        required=True,
        help='Post title'
    )
    parser.add_argument(
        '--category',
        required=True,
        choices=['data-science', 'software-engineering', 'career', 'leadership'],
        help='Post category for Jekyll'
    )

    # Optional arguments
    parser.add_argument(
        '--image',
        help='Path to image file'
    )
    parser.add_argument(
        '--hashtags',
        nargs='+',
        help='Hashtags for LinkedIn (without # symbol)'
    )

    # Platform selection
    parser.add_argument(
        '--linkedin-only',
        action='store_true',
        help='Only post to LinkedIn'
    )
    parser.add_argument(
        '--jekyll-only',
        action='store_true',
        help='Only create Jekyll post'
    )

    args = parser.parse_args()

    # Get content from file or string
    if args.file:
        try:
            with open(args.file, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            sys.exit(1)
    else:
        content = args.content

    # Validate image path if provided
    if args.image and not os.path.exists(args.image):
        print(f"Warning: Image file not found: {args.image}")
        args.image = None

    # Initialize cross-poster
    # Only validate credentials if we need to post to LinkedIn
    validate_creds = not args.jekyll_only
    try:
        poster = CrossPoster(validate_credentials=validate_creds)
    except ValueError as e:
        print(f"Error: {e}")
        print("\nPlease ensure you have:")
        print("1. Copied scripts/.env.example to scripts/.env")
        print("2. Filled in your LinkedIn credentials in scripts/.env")
        sys.exit(1)

    # Perform cross-posting
    print(f"\n{'='*60}")
    print(f"Cross-Posting: {args.title}")
    print(f"{'='*60}")

    linkedin_url, jekyll_path = poster.cross_post(
        title=args.title,
        content=content,
        category=args.category,
        image_path=args.image,
        hashtags=args.hashtags,
        linkedin_only=args.linkedin_only,
        jekyll_only=args.jekyll_only
    )

    # Summary
    print(f"\n{'='*60}")
    print("Summary:")
    print(f"{'='*60}")

    if linkedin_url:
        print(f"LinkedIn: {linkedin_url}")
    elif not args.jekyll_only:
        print("LinkedIn: Failed")

    if jekyll_path:
        print(f"Jekyll: {jekyll_path}")
    elif not args.linkedin_only:
        print("Jekyll: Failed")

    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
