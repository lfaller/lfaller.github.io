# Boston Women in Bioinformatics (BWIB) Cross-Post Setup Guide

This guide explains how to set up automated cross-posting from Lina's blog to the BWIB webpage.

## Overview

The cross-posting system automatically:
1. Detects when new blog posts are pushed to Lina's repository
2. Transforms Jekyll posts to Astro format
3. Commits the transformed posts to the BWIB webpage repository
4. Opens a PR for review and manual adjustments

## Components

- **`transform_to_astro.py`**: Python script that transforms Jekyll markdown to Astro format
- **`crosspost_to_bwib.py`**: Main cross-posting script that handles repo operations and PR creation
- **`crosspost_config.json`**: Configuration file with field mappings and templates
- **`bwib-crosspost.yml`**: GitHub Actions workflow that triggers the cross-posting process

## Setup Instructions

### Step 1: Prepare GitHub Token (For Lina)

You need a GitHub token with write access to the BWIB repository.

1. Go to [GitHub Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token" (Classic)
3. Give it a name like `BWIB Cross-Post Token`
4. Select scopes:
   - `repo` (full control of private repositories)
5. Generate and copy the token

### Step 2: Store the Secret (For Lina)

In your repository settings:

1. Go to **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `CROSSPOST_GH_TOKEN`
4. Value: Paste the token from Step 1
5. Click **Add secret**

Also add the target repository info:

1. Click **New repository secret**
2. Name: `CROSSPOST_TARGET_REPO`
3. Value: `Boston-area-Women-in-Bioinformatics/webpage`
4. Click **Add secret**

### Step 3: Grant GitHub Actions Permissions

The workflow needs write permissions:

1. Go to **Settings → Actions → General**
2. Under "Workflow permissions", select:
   - ☑ **Read and write permissions**
   - ☑ **Allow GitHub Actions to create and approve pull requests**
3. Save

### Step 4: Install GitHub CLI (For Running Locally)

The `crosspost_to_bwib.py` script uses the GitHub CLI to open PRs. Install it:

```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh

# Or download from https://cli.github.com/
```

Then authenticate:
```bash
gh auth login
```

### Step 5: Test the Setup (Optional)

You can test the transformation script manually:

```bash
# From the repository root
python3 scripts/transform_to_astro.py _posts/2025-11-27-thanksgiving-in-biotech.md --config scripts/crosspost_config.json
```

This will output the transformed Astro markdown to stdout.

### Step 6: Manual Trigger (Optional)

To manually cross-post a specific post:

1. Go to **Actions → Cross-post to BWIB Webpage**
2. Click **Run workflow**
3. Choose your branch (main)
4. Optionally specify a post file
5. Click **Run workflow**

## How It Works

### Automatic Trigger

When you push new posts to the `_posts/` directory:

1. GitHub Actions detects the change
2. The workflow runs `crosspost_to_bwib.py`
3. The script transforms your Jekyll post to Astro format
4. It clones the BWIB repository (using the `CROSSPOST_GH_TOKEN`)
5. Creates a feature branch: `cross-post/{slug}`
6. Commits the transformed post
7. Pushes the branch
8. Opens a PR with a review checklist

### PR Review Process

When a cross-post PR is opened on the BWIB repository:

1. Your friend reviews the auto-generated fields
2. She adjusts any fields that need customization:
   - **excerpt**: May need to be more specific than auto-generated
   - **image**: Verify the image path works in her repository
   - **tags**: Add additional relevant tags
   - **category**: Confirm the category is appropriate
3. She can edit the markdown content if needed
4. Once approved, she merges the PR

## Field Mapping Reference

| Your Field | Her Field | Notes |
|-----------|-----------|-------|
| `layout` | — | Removed in Astro |
| `author: "lina"` | `authors: [{name: "...", link: "..."}]` | Mapped to author object |
| `title` | `title` | Direct copy |
| `date` | `publishDate` | Converted to ISO 8601 format |
| `categories` | `category` + `tags` | categories → category + tags |
| — | `slug` | Auto-generated from filename |
| — | `excerpt` | Auto-generated from first paragraph (can be customized in PR) |
| — | `image` | Auto-detected from first markdown image in post |
| — | `imageAlt` | Auto-detected from image alt text |
| — | `imagePosition` | Default: `top` (can be adjusted in PR) |
| — | `metadata` | Auto-generated SEO metadata with canonical link |

## Customization

### Update Author Mapping

In `scripts/crosspost_config.json`, the `author_mapping` section maps Jekyll authors to Astro authors:

```json
"author_mapping": {
  "lina": {
    "name": "Lina L. Faller, PhD",
    "linkedin": "https://linkedin.com/in/linafaller"
  }
}
```

Add more authors if needed.

### Update Category Mapping

If you use different categories, update the mapping:

```json
"category_mapping": {
  "biotech": "Deep Dive",
  "bioinformatics": "Deep Dive",
  "career": "Career"
}
```

### Update PR Template

The PR description is customizable in `crosspost_config.json`:

```json
"pr_description_template": "## Cross-Post from Lina's Blog\n..."
```

### Change Attribution Link

By default, posts include an attribution link at the end. To customize:

1. Edit `scripts/transform_to_astro.py`
2. Find the `include_attribution` parameter
3. Modify the attribution text in the `content_with_attribution` section

## Troubleshooting

### PR Not Opening

**Problem**: Workflow runs but PR doesn't open

**Solutions**:
- Check that `CROSSPOST_GH_TOKEN` is set correctly
- Verify the token has `repo` scope
- Check GitHub Actions workflow logs: **Actions → Cross-post to BWIB Webpage → [Latest run]**
- Ensure GitHub CLI is installed and authenticated: `gh auth status`

### Image Paths Not Working

**Problem**: Images don't display after cross-posting

**Solutions**:
- Images are extracted from your posts but **not automatically copied** to BWIB repo
- Your friend needs to:
  - Either download the images and add them to her repo
  - Or update the image paths to point to your blog
  - Or update the image paths to point to a CDN/external location

The PR will flag this in the review checklist.

### Transform Script Errors

**Problem**: `transform_to_astro.py` fails with YAML errors

**Solutions**:
- Ensure your Jekyll frontmatter is valid YAML
- Check for special characters that need escaping
- Verify post file is UTF-8 encoded

### Workflow Doesn't Trigger

**Problem**: Workflow doesn't run when you push new posts

**Solutions**:
- Check the workflow file syntax (run through GitHub's YAML validator)
- Verify the path filter matches: `_posts/**`
- Check that changes are committed to `main` branch
- Go to **Settings → Actions → General** and ensure workflows are enabled

## What Not to Cross-Post

Some posts may not be suitable for cross-posting:

- Very personal posts about your own journey
- Posts with site-specific references
- Posts that are already published on BWIB
- Posts that are outdated or deprecated

You can selectively publish by using the manual workflow trigger instead of pushing posts to the main folder.

## Advanced: Running Locally

If you want to test or run cross-posting from your machine:

```bash
# From scripts directory
python3 crosspost_to_bwib.py ../_posts/2025-11-27-thanksgiving-in-biotech.md

# Set environment variables first
export GH_TOKEN=your_github_token
export CROSSPOST_TARGET_REPO=Boston-area-Women-in-Bioinformatics/webpage
python3 crosspost_to_bwib.py ../_posts/2025-11-27-thanksgiving-in-biotech.md
```

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review the GitHub Actions logs
3. Check the PR that was opened (if it got that far)
4. Contact Lina or create an issue in the repository

---

**Version**: 1.0
**Last Updated**: December 2025
