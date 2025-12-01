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

### Step 1: Prepare GitHub Token (Lina's Task)

You need a GitHub token with write access to the BWIB repository.

1. Go to [GitHub Settings → Personal Access Tokens](https://github.com/settings/tokens)
2. Click "Generate new token" (Classic)
3. Give it a name like `BWIB Cross-Post Token`
4. Select scopes:
   - `repo` (full control of private repositories)
5. Generate and copy the token

### Step 2: Store the Secret (Lina's Task)

In **your** (Lina's) repository settings:

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

### Step 3: Grant GitHub Actions Permissions (Lina's Task)

The workflow needs write permissions to open PRs:

1. Go to **Settings → Actions → General** (in your repository)
2. Under "Workflow permissions", select:
   - ☑ **Read and write permissions**
   - ☑ **Allow GitHub Actions to create and approve pull requests**
3. Save

### Step 4: Install GitHub CLI (Lina's Task - Optional)

The `crosspost_to_bwib.py` script uses the GitHub CLI to open PRs. Install it if you want to run cross-posts locally:

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

### Step 5: Test the Setup (Lina's Task - Optional)

You can test the transformation script manually:

```bash
# From the repository root
python3 scripts/transform_to_astro.py _posts/2025-11-27-thanksgiving-in-biotech.md --config scripts/crosspost_config.json
```

This will output the transformed Astro markdown to stdout.

### Step 6: Manual Trigger (Lina's Task - Optional)

To manually cross-post a specific post:

1. Go to **Actions → Cross-post to BWIB Webpage** (in your repository)
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

### PR Review & Merge Process (Sammy's Task)

When a cross-post PR is opened on the BWIB repository, Sammy will:

1. Review the auto-generated fields (see [BWIB_PR_REVIEW_GUIDE.md](BWIB_PR_REVIEW_GUIDE.md) for detailed checklist)
2. Adjust any fields that need customization:
   - **excerpt**: May need to be more specific than auto-generated
   - **image**: Download/upload image to `public/blog_images/` and update path
   - **tags**: Add additional relevant tags
   - **category**: Confirm the category is appropriate
3. Upload featured image to `public/blog_images/` folder (optional but recommended)
4. Edit the markdown content if needed
5. Once approved, merge the PR

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

## Customization (Lina's Tasks)

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

Add more authors if you have guest posts.

### Update Category Mapping

If you use different categories in your Jekyll posts, update the mapping in `scripts/crosspost_config.json`:

```json
"category_mapping": {
  "biotech": "Deep Dive",
  "bioinformatics": "Deep Dive",
  "career": "Career"
}
```

Make sure the values match the categories available in the BWIB Astro site.

### Update PR Template

The PR description is customizable in `scripts/crosspost_config.json`:

```json
"pr_description_template": "## Cross-Post from Lina's Blog\n..."
```

### Change Attribution Link

By default, posts include an attribution link at the end: `*Originally posted on [Lina L. Faller's blog](URL)*`

To customize:

1. Edit `scripts/transform_to_astro.py`
2. Find the `content_with_attribution` section
3. Modify the attribution text

## Troubleshooting (Lina's Tasks)

### PR Not Opening

**Problem**: Workflow runs but PR doesn't open

**Solutions**:
- Check that `CROSSPOST_GH_TOKEN` is set correctly in your repo secrets
- Verify the token has `repo` scope
- Check GitHub Actions workflow logs: **Actions → Cross-post to BWIB Webpage → [Latest run]**
- Ensure GitHub CLI is installed and authenticated: `gh auth status`

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

Some posts may not be suitable for cross-posting. If you want to exclude a post:

- Very personal posts about your own journey
- Posts with site-specific references
- Posts that are already published on BWIB
- Posts that are outdated or deprecated

You can selectively publish by using the manual workflow trigger instead of pushing all posts to the `_posts/` folder.

## Image Handling

### How Images Work

The transformation script **extracts the image path** from your Jekyll post but does **not automatically copy** the image file. This allows flexibility:

**Option A: Sammy hosts the images** (recommended)
- Sammy downloads your image from `https://linafaller.github.io/assets/images/posts/{filename}`
- Uploads to her repo's `public/blog_images/` folder
- Updates the image path in the PR to `/blog_images/{filename}`

**Option B: Link directly to your blog**
- Leave the path as-is or update to full URL: `https://linafaller.github.io/assets/images/posts/{filename}`
- Works fine, but your blog is the source of truth for images

**Option C: Use external CDN**
- Sammy can host images on Cloudinary, Imgix, or similar
- Update paths accordingly

### What You Should Do

Make sure your Jekyll posts include a featured image using markdown image syntax:

```markdown
![Image alt text](/assets/images/posts/2025-11-27-thanksgiving-in-biotech.png)
```

The transformation script will:
- Extract this image and its alt text
- Put the path in the `image` field
- Put the alt text in the `imageAlt` field

Sammy will then decide in the PR review how to handle the image file.

## Advanced: Running Locally (Lina's Task)

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

**For Lina**: If the workflow isn't working:
1. Check the troubleshooting section above
2. Review the GitHub Actions logs
3. Verify your secrets are set correctly
4. Re-check that the workflow file permissions are correct

**For Sammy**: Questions about the PR review process are in [BWIB_PR_REVIEW_GUIDE.md](BWIB_PR_REVIEW_GUIDE.md)

**For both**: If you need to pause cross-posting, Lina can set `"enabled": false` in `scripts/crosspost_config.json` and push the change.

---

**Version**: 1.0
**Last Updated**: December 2025
