#!/usr/bin/env python3
"""
Cross-post Jekyll posts to the BWIB webpage repository.

This script:
1. Takes Jekyll posts as input
2. Transforms them to Astro format
3. Clones/updates the target BWIB repo
4. Commits the transformed posts
5. Opens a PR for review
"""

import sys
import os
import json
import subprocess
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
import time

from transform_to_astro import (
    extract_frontmatter_and_content,
    transform_to_astro,
    generate_slug
)


def run_command(cmd: list, cwd: str = None, capture_output: bool = False) -> str:
    """Run a shell command and return output if capture_output is True."""
    try:
        # Always capture output so we can show error messages
        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=True)
        if capture_output:
            return result.stdout.strip()
        else:
            return ""
    except subprocess.CalledProcessError as e:
        print(f"Error running command {' '.join(cmd)}: {e.stderr}")
        raise


def load_config(config_path: str = None) -> dict:
    """Load cross-post configuration."""
    if config_path is None:
        config_path = Path(__file__).parent / 'crosspost_config.json'

    with open(config_path, 'r') as f:
        return json.load(f)


def clone_or_update_target_repo(repo_url: str, target_dir: str, gh_token: str = None) -> None:
    """Clone target repo (assumes directory is clean)."""
    print(f"Cloning repo to {target_dir}")
    run_command(['git', 'clone', repo_url, target_dir])

    # Git may strip credentials from origin remote after cloning for security
    # Restore the authenticated URL so push operations work
    if 'x-access-token' in repo_url:
        print(f"Configuring git remote with authentication")
        run_command(['git', 'remote', 'set-url', 'origin', repo_url], cwd=target_dir)
        print(f"Git remote configured successfully")


def create_feature_branch(repo_dir: str, slug: str) -> str:
    """Create a feature branch for this cross-post."""
    # Configure git user for commits
    run_command(['git', 'config', 'user.email', 'noreply@bwib.github.io'], cwd=repo_dir)
    run_command(['git', 'config', 'user.name', 'BWIB Cross-Post Bot'], cwd=repo_dir)

    # Ensure we're on main and up-to-date
    run_command(['git', 'checkout', 'main'], cwd=repo_dir)
    run_command(['git', 'pull', 'origin', 'main'], cwd=repo_dir)

    # Create feature branch from main
    branch_name = f"cross-post/{slug}"

    # Create a fresh local branch from main (without tracking remote)
    try:
        run_command(['git', 'checkout', '-b', branch_name, 'main'], cwd=repo_dir)
    except subprocess.CalledProcessError:
        # Branch might already exist locally, delete and recreate
        run_command(['git', 'branch', '-D', branch_name], cwd=repo_dir)
        run_command(['git', 'checkout', '-b', branch_name, 'main'], cwd=repo_dir)

    return branch_name


def commit_post_to_repo(
    repo_dir: str,
    post_content: str,
    post_slug: str,
    author_name: str = "BWIB Cross-Post Bot"
) -> str:
    """Commit the transformed post to the repo."""
    # Determine target file path
    target_file = Path(repo_dir) / 'src' / 'content' / 'post' / f"{post_slug}.md"
    target_file.parent.mkdir(parents=True, exist_ok=True)

    # Write the post
    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(post_content)

    print(f"Written post to {target_file}")

    # Stage and commit
    run_command(['git', 'add', str(target_file)], cwd=repo_dir)

    commit_message = f"Cross-post: {post_slug}"
    run_command(
        ['git', 'commit', '-m', commit_message, '--author', f'{author_name} <noreply@bwib.github.io>'],
        cwd=repo_dir
    )

    print(f"Committed post with message: {commit_message}")
    return target_file


def copy_image_to_repo(
    repo_dir: str,
    image_path: str,
    jekyll_post_path: str,
    post_slug: str
) -> str:
    """
    Copy featured image from Jekyll post to BWIB repo's public/blog_images/ directory.
    Returns the new image path relative to repo root, or original path if copy fails.
    """
    if not image_path or image_path.startswith('http'):
        # Don't copy external URLs or empty paths
        return image_path

    # Determine source file path
    if image_path.startswith('/'):
        # Absolute path from Jekyll - need to find the file in the blog
        jekyll_post_dir = Path(jekyll_post_path).parent.parent  # Go up to repo root
        source_file = jekyll_post_dir / image_path.lstrip('/')
    else:
        # Relative path
        source_file = Path(jekyll_post_path).parent / image_path

    if not source_file.exists():
        print(f"Warning: Image file not found at {source_file}, keeping original path")
        return image_path

    try:
        # Extract just the filename from the original path
        filename = Path(image_path).name

        # Ensure blog_images directory exists
        target_dir = Path(repo_dir) / 'public' / 'blog_images'
        target_dir.mkdir(parents=True, exist_ok=True)

        # Copy the image file
        target_file = target_dir / filename
        shutil.copy2(source_file, target_file)
        print(f"Copied image to {target_file}")

        # Return the new path (relative to repo root)
        new_path = f"/blog_images/{filename}"
        return new_path

    except Exception as e:
        print(f"Warning: Could not copy image: {e}, keeping original path")
        return image_path


def update_image_path_in_content(
    astro_content: str,
    original_path: str,
    new_path: str
) -> str:
    """Update the image path in the Astro frontmatter and content."""
    if not original_path or original_path == new_path:
        return astro_content

    # Update in frontmatter (image: field)
    astro_content = astro_content.replace(f"image: {original_path}", f"image: {new_path}")
    astro_content = astro_content.replace(f"image: '{original_path}'", f"image: {new_path}")
    astro_content = astro_content.replace(f'image: "{original_path}"', f"image: {new_path}")

    return astro_content


def format_with_prettier(repo_dir: str, file_path: str) -> None:
    """Format file with prettier using the repo's config."""
    try:
        # Check if prettier is available
        run_command(['which', 'prettier'], capture_output=True)
    except subprocess.CalledProcessError:
        print(f"Warning: prettier not found, skipping formatting")
        return

    try:
        # Install npm dependencies in repo if package.json exists
        # This ensures prettier plugins like prettier-plugin-astro are available
        package_json = os.path.join(repo_dir, 'package.json')
        if os.path.exists(package_json):
            print(f"Installing npm dependencies for prettier plugins...")
            try:
                run_command(['npm', 'install'], cwd=repo_dir)
                print(f"npm dependencies installed")
            except subprocess.CalledProcessError as e:
                print(f"Warning: npm install failed, attempting prettier anyway: {e}")
                # Continue - prettier might still work with global installation

        # Convert file_path to relative path from repo root if it's absolute
        if os.path.isabs(file_path):
            file_path = os.path.relpath(file_path, repo_dir)

        # Run prettier on the file (run from repo_dir so it finds .prettierrc.cjs)
        run_command(['prettier', '--write', file_path], cwd=repo_dir)
        print(f"Formatted {file_path} with prettier")

        # Stage the formatted changes
        run_command(['git', 'add', file_path], cwd=repo_dir)

        # Check if there are changes to commit
        # If git diff --cached --quiet returns non-zero, there are changes
        try:
            run_command(['git', 'diff', '--cached', '--quiet'], cwd=repo_dir, capture_output=False)
        except subprocess.CalledProcessError:
            # There are changes, commit them
            run_command(
                ['git', 'commit', '-m', 'Prettier formatting', '--author', 'BWIB Cross-Post Bot <noreply@bwib.github.io>'],
                cwd=repo_dir
            )
            print(f"Committed prettier formatting")
    except subprocess.CalledProcessError as e:
        print(f"Warning: prettier formatting failed: {e}")
        # Continue anyway - formatting is nice to have but not critical


def push_branch(repo_dir: str, branch_name: str, repo_url: str = None) -> None:
    """Push feature branch to remote."""
    # Always push to origin - authentication should be configured in the repo
    # Use force-with-lease to handle cases where remote branch exists from previous attempts
    run_command(['git', 'push', '--force-with-lease', 'origin', branch_name], cwd=repo_dir)
    print(f"Pushed branch {branch_name}")


def open_pr(
    config: dict,
    repo: str,
    head_branch: str,
    base_branch: str = 'main',
    title: str = None,
    body: str = None
) -> str:
    """Open a PR using GitHub CLI."""
    # Use gh CLI if available
    try:
        cmd = [
            'gh', 'pr', 'create',
            '--repo', repo,
            '--head', head_branch,
            '--base', base_branch,
            '--title', title,
            '--body', body
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        pr_url = result.stdout.strip()
        print(f"Opened PR: {pr_url}")
        return pr_url
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else e.stdout
        print(f"Error opening PR: {error_msg}")
        print(f"Branch {head_branch} was successfully pushed to {repo}")
        print(f"You may need to open the PR manually or check gh authentication")
        raise
    except FileNotFoundError:
        print("GitHub CLI (gh) not found. Please install it: https://cli.github.com/")
        raise


def format_pr_description(config: dict, jekyll_frontmatter: dict, astro_metadata: dict, original_url: str) -> str:
    """Format the PR description using the template."""
    template = config.get('pr_description_template', '')

    # Prepare format values
    format_values = {
        'title': jekyll_frontmatter.get('title', 'Untitled'),
        'category': astro_metadata.get('category', 'Deep Dive'),
        'tags': ', '.join(astro_metadata.get('tags', [])) or 'None',
        'image': astro_metadata.get('image', '/images/posts/featured.png'),
        'original_url': original_url
    }

    return template.format(**format_values)


def crosspost_single_post(
    jekyll_post_path: str,
    config: dict,
    temp_repo_dir: str = None
) -> bool:
    """Cross-post a single Jekyll post to BWIB repo."""
    print(f"\n{'='*60}")
    print(f"Cross-posting: {jekyll_post_path}")
    print(f"{'='*60}\n")

    # Extract and transform post
    try:
        jekyll_frontmatter, jekyll_content = extract_frontmatter_and_content(jekyll_post_path)
    except Exception as e:
        print(f"Error reading post: {e}")
        return False

    # Generate slug
    slug = generate_slug(jekyll_post_path)
    print(f"Generated slug: {slug}")

    # Transform to Astro format
    try:
        astro_content = transform_to_astro(jekyll_frontmatter, jekyll_content, config, include_attribution=True)
    except Exception as e:
        print(f"Error transforming post: {e}")
        return False

    # Prepare repository
    target_repo = config.get('target_repo')
    gh_token = os.getenv('GH_TOKEN')

    if not gh_token:
        print("Error: CROSSPOST_GH_TOKEN not set in secrets")
        return False

    if not target_repo:
        print("Error: CROSSPOST_TARGET_REPO not set in config")
        return False

    # Use temp directory or create one
    if temp_repo_dir is None:
        temp_repo_dir = tempfile.mkdtemp(prefix='bwib_crosspost_')
    else:
        # If temp directory exists, remove it to ensure clean clone
        if os.path.exists(temp_repo_dir):
            shutil.rmtree(temp_repo_dir)
        os.makedirs(temp_repo_dir, exist_ok=True)

    repo_url = f"https://x-access-token:{gh_token}@github.com/{target_repo}.git"

    try:
        # Clone/update target repo
        clone_or_update_target_repo(repo_url, temp_repo_dir, gh_token)

        # Create feature branch
        branch_name = create_feature_branch(temp_repo_dir, slug)

        # Parse Astro metadata from generated content
        # Extract the YAML frontmatter from astro_content
        astro_lines = astro_content.split('\n')
        astro_metadata = {}
        if astro_lines[0] == '---':
            in_fm = True
            for line in astro_lines[1:]:
                if line == '---':
                    break
                # Basic parsing (simplified, not full YAML)
                if ':' in line and not in_fm is False:
                    key, value = line.split(':', 1)
                    astro_metadata[key.strip()] = value.strip().strip('"\'')

        # Commit post
        target_file = commit_post_to_repo(temp_repo_dir, astro_content, slug)

        # Extract image path from frontmatter before copying
        image_path = None
        for line in astro_content.split('\n'):
            if line.startswith('image:'):
                # Extract the image path from the line
                image_path = line.split(':', 1)[1].strip().strip('"\'')
                break

        # Copy image to repo if it exists locally
        new_image_path = image_path
        if image_path:
            new_image_path = copy_image_to_repo(temp_repo_dir, image_path, jekyll_post_path, slug)

            # If image path changed, update the post content and re-commit
            if new_image_path != image_path:
                astro_content = update_image_path_in_content(astro_content, image_path, new_image_path)

                # Re-write the post with updated image path
                with open(target_file, 'w', encoding='utf-8') as f:
                    f.write(astro_content)
                print(f"Updated image path from {image_path} to {new_image_path}")

                # Add the updated post file to staging
                run_command(['git', 'add', str(target_file)], cwd=temp_repo_dir)

                # Commit the updated post with new image path
                try:
                    run_command(
                        ['git', 'commit', '-m', 'Update image path', '--author', 'BWIB Cross-Post Bot <noreply@bwib.github.io>'],
                        cwd=temp_repo_dir
                    )
                    print(f"Committed updated image path")
                except subprocess.CalledProcessError:
                    # No changes to commit
                    pass

        # Stage and commit the image files
        image_files = list(Path(temp_repo_dir).glob('public/blog_images/*'))
        if image_files:
            for img_file in image_files:
                run_command(['git', 'add', str(img_file)], cwd=temp_repo_dir)

            # Commit the image
            try:
                run_command(
                    ['git', 'commit', '-m', 'Add featured image', '--author', 'BWIB Cross-Post Bot <noreply@bwib.github.io>'],
                    cwd=temp_repo_dir
                )
                print(f"Committed image files")
            except subprocess.CalledProcessError:
                # No image changes to commit (image already existed)
                pass

        # Format with prettier to match BWIB repo's code style
        format_with_prettier(temp_repo_dir, str(target_file))

        # Get original URL
        original_url_template = config.get('original_post_url_template', '')
        original_url = original_url_template.format(slug=slug) if original_url_template else ''

        # Format PR description
        pr_title = config.get('pr_title_template', 'Cross-post: {title}').format(title=jekyll_frontmatter.get('title', 'Post'))
        pr_body = format_pr_description(config, jekyll_frontmatter, astro_metadata, original_url)

        # Push branch
        push_branch(temp_repo_dir, branch_name)

        # Open PR
        try:
            pr_url = open_pr(config, target_repo, branch_name, 'main', pr_title, pr_body)
            print(f"✓ Successfully cross-posted to PR: {pr_url}")
            return True
        except Exception as e:
            print(f"✗ Failed to open PR: {e}")
            print(f"  Branch {branch_name} is ready in {target_repo}, but PR creation failed")
            return False

    except Exception as e:
        print(f"✗ Error during cross-post: {e}")
        return False
    finally:
        # Clean up temp directory if we created it
        if temp_repo_dir and temp_repo_dir.startswith(tempfile.gettempdir()):
            try:
                shutil.rmtree(temp_repo_dir)
                print(f"Cleaned up temp directory")
            except Exception as e:
                print(f"Warning: Could not clean up temp directory: {e}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: crosspost_to_bwib.py <post1.md> [post2.md ...]")
        sys.exit(1)

    # Load configuration
    try:
        config = load_config()
    except FileNotFoundError:
        print("Error: crosspost_config.json not found")
        sys.exit(1)

    if not config.get('enabled'):
        print("Cross-posting is disabled in configuration")
        sys.exit(0)

    # Process each post
    posts = sys.argv[1:]
    success_count = 0
    failure_count = 0

    # Create a shared temp directory for all posts in this run
    temp_repo_dir = tempfile.mkdtemp(prefix='bwib_crosspost_')

    try:
        for post_path in posts:
            try:
                if crosspost_single_post(post_path, config, temp_repo_dir):
                    success_count += 1
                else:
                    failure_count += 1
            except Exception as e:
                print(f"Exception processing {post_path}: {e}")
                failure_count += 1

        # Summary
        print(f"\n{'='*60}")
        print(f"Cross-post Summary")
        print(f"{'='*60}")
        print(f"Successful: {success_count}")
        print(f"Failed: {failure_count}")
        print(f"{'='*60}\n")

        sys.exit(0 if failure_count == 0 else 1)

    finally:
        # Clean up temp directory
        try:
            shutil.rmtree(temp_repo_dir)
            print(f"Cleaned up temp directory")
        except Exception as e:
            print(f"Warning: Could not clean up temp directory: {e}")


if __name__ == '__main__':
    main()
