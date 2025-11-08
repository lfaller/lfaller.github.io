# LinkedIn-Jekyll Cross-Posting Automation

Automate posting content to both LinkedIn and your Jekyll website. This tool handles format conversion, hashtag management, and image uploads.

## Features

- **GitHub Actions Integration**: Automatically post to LinkedIn when you push to main
- Post to LinkedIn and Jekyll simultaneously (manual mode)
- Automatic markdown to plain text conversion for LinkedIn
- Smart hashtag handling (included on LinkedIn, removed from Jekyll)
- Image upload support for both platforms
- Category-based post organization
- Secure credential management
- CLI interface for easy use

## Automated Workflow (Recommended)

The easiest way to use this tool is via GitHub Actions:

1. Write your Jekyll post in `_posts/` with frontmatter
2. Commit and push to the `main` branch
3. GitHub Actions automatically:
   - Deploys to GitHub Pages
   - Posts to LinkedIn with proper formatting

### Setup GitHub Actions

1. Go to your repository Settings → Secrets and variables → Actions
2. Add the following secrets:
   - `LINKEDIN_ACCESS_TOKEN`: Your LinkedIn OAuth token
   - `LINKEDIN_AUTHOR_ID`: Your LinkedIn member URN (format: `urn:li:member:123456`)

The workflow will automatically trigger when you push changes to `_posts/` directory.

## Manual Usage

## Setup

### 1. Install Python Dependencies

**Option A: Quick Setup (Recommended)**

Run the automated setup script:

```bash
cd scripts
./setup.sh
```

This will create a virtual environment, install all dependencies, and provide next steps.

**Option B: Manual Setup**

```bash
cd scripts

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Important:** Always activate the virtual environment before using the cross-poster:
```bash
cd scripts
source venv/bin/activate  # You'll see (venv) in your prompt
```

To deactivate when done:
```bash
deactivate
```

### 2. Configure LinkedIn API Access

#### Create a LinkedIn Developer App

1. Go to [LinkedIn Developer Portal](https://www.linkedin.com/developers/apps)
2. Click "Create app"
3. Fill in the required information:
   - App name: "Personal Blog Cross-Poster" (or your choice)
   - LinkedIn Page: You must create/associate a LinkedIn Company Page
   - App logo (optional)
4. After creation, go to the "Products" tab
5. Request access to "Share on LinkedIn" product
6. Wait for approval (usually instant for verified apps)

#### Get Your Credentials

1. Go to the "Auth" tab in your app
2. Copy your **Client ID** and **Client Secret**
3. Add `http://localhost:8000/callback` to "Redirect URLs" (for local OAuth flow)

#### Generate an Access Token

You need to generate an OAuth 2.0 access token with the following scopes:
- `openid`
- `profile`
- `w_member_social`

**Option A: Use LinkedIn's OAuth Playground** (Easiest)
1. Use a tool like [LinkedIn OAuth Token Generator](https://www.linkedin.com/developers/tools/oauth)
2. Select the required scopes
3. Authorize and copy the access token

**Option B: Manual OAuth Flow**
1. Construct authorization URL:
```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8000/callback&scope=openid%20profile%20w_member_social
```
2. Visit the URL in a browser and authorize
3. Copy the `code` from the redirect URL
4. Exchange code for token:
```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -d grant_type=authorization_code \
  -d code=YOUR_AUTH_CODE \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d redirect_uri=http://localhost:8000/callback
```

#### Get Your LinkedIn Author ID

```bash
curl -X GET https://api.linkedin.com/v2/userinfo \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

The response will include your `sub` field - this is your author ID. Convert it to URN format: `urn:li:person:YOUR_SUB_VALUE`

### 3. Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and fill in your credentials:
```bash
# Required
LINKEDIN_ACCESS_TOKEN=your_access_token_here
LINKEDIN_AUTHOR_ID=urn:li:person:your_id_here

# Optional (for token refresh)
LINKEDIN_CLIENT_ID=your_client_id_here
LINKEDIN_CLIENT_SECRET=your_client_secret_here
```

**Important:** Never commit your `.env` file to Git. It's already included in `.gitignore`.

## Usage

### Basic Examples

#### Post to both LinkedIn and Jekyll:

```bash
python cross_poster.py \
  --title "My First Post" \
  --content "This is my post content with **markdown** formatting." \
  --category data-science \
  --hashtags datascience machinelearning ai
```

#### Post from a markdown file:

```bash
python cross_poster.py \
  --title "Advanced ML Techniques" \
  --file my-draft.md \
  --category data-science \
  --image ./images/ml-diagram.png \
  --hashtags machinelearning deeplearning
```

#### Post to LinkedIn only:

```bash
python cross_poster.py \
  --title "Quick LinkedIn Update" \
  --content "Check out this insight!" \
  --category software-engineering \
  --hashtags coding \
  --linkedin-only
```

#### Create Jekyll post only:

```bash
python cross_poster.py \
  --title "Blog Post" \
  --file post-draft.md \
  --category leadership \
  --image header.jpg \
  --jekyll-only
```

### Command-Line Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--title` | Yes | Post title |
| `--content` | Either this or `--file` | Post content as string |
| `--file` | Either this or `--content` | Path to markdown file with content |
| `--category` | Yes | Jekyll category: `data-science`, `software-engineering`, `career`, or `leadership` |
| `--image` | No | Path to image file (will be uploaded to both platforms) |
| `--hashtags` | No | Space-separated hashtags for LinkedIn (without `#`) |
| `--linkedin-only` | No | Only post to LinkedIn, skip Jekyll |
| `--jekyll-only` | No | Only create Jekyll post, skip LinkedIn |

### Example Workflow

1. **Write your content in a markdown file:**

```markdown
# My Post Title

This is the introduction with **bold text** and *italics*.

Here's a key insight about data science...

## Key Points

- Point one
- Point two
- Point three
```

2. **Prepare your image (optional):**
   - Save it in a convenient location
   - Recommended: 1200x630px for optimal LinkedIn display

3. **Run the cross-poster:**

```bash
python cross_poster.py \
  --title "My Post Title" \
  --file draft.md \
  --category data-science \
  --image post-image.jpg \
  --hashtags datascience analytics insights
```

4. **Review the output:**
   - LinkedIn post URL (if successful)
   - Jekyll post file path
   - Any errors or warnings

5. **Commit and push to GitHub (for Jekyll site):**

```bash
cd ..  # Back to repo root
git add _posts/*.md assets/images/*
git commit -m "Add new post: My Post Title"
git push
```

## How It Works

### Format Conversion

**LinkedIn:**
- Markdown formatting is converted to plain text
- Links `[text](url)` become `text (url)`
- Bold/italic markers are removed
- Hashtags are appended at the end

**Jekyll:**
- Content remains in full markdown format
- Hashtag lines are removed
- Frontmatter is automatically generated
- Images are copied to `assets/images/`

### Image Handling

**LinkedIn:**
- Images are uploaded via LinkedIn's Asset API
- Registered as feed-share images
- Attached to the post

**Jekyll:**
- Images are copied to `assets/images/YYYY-MM-DD-slug.ext`
- Relative path is added to frontmatter
- Referenced in post automatically

### Generated Jekyll Post Format

```yaml
---
layout: post
title: "My Post Title"
date: 2025-11-08 14:30:00 -0500
categories: [data-science]
image: /assets/images/2025-11-08-my-post-title.jpg
---

Post content here in markdown format.
No hashtags included.
```

## Troubleshooting

### "Missing LinkedIn credentials" Error

Make sure you:
1. Created a `.env` file (copy from `.env.example`)
2. Added your `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_AUTHOR_ID`
3. Are running the script from the `scripts/` directory or using the correct path

### LinkedIn API Errors

**401 Unauthorized:**
- Your access token may have expired (tokens last 60 days)
- Generate a new access token following the setup steps

**403 Forbidden:**
- Your app may not have "Share on LinkedIn" product access
- Check your app's Products tab in the Developer Portal

**Rate Limit Errors:**
- LinkedIn allows 25 posts per 24 hours
- Wait before posting again

### Image Upload Failures

- Check that the image file exists and path is correct
- Ensure image is a common format (JPG, PNG)
- Very large images may fail - try resizing to <5MB

### Jekyll Post Not Created

- Check that `_posts/` directory exists in your repo root
- Verify write permissions
- Check that category is one of the allowed values

## Token Refresh

LinkedIn access tokens expire after **60 days**. When your token expires:

1. Follow the "Generate an Access Token" steps again
2. Update `LINKEDIN_ACCESS_TOKEN` in your `.env` file
3. Continue posting

**Future Enhancement:** Automatic token refresh using refresh tokens (not yet implemented).

## Security Best Practices

- Never commit your `.env` file
- Keep your access token secure
- Rotate tokens periodically
- Use environment variables, not hardcoded credentials
- Review LinkedIn API permissions regularly

## Advanced Usage

### Custom Post Directory

Override the default Jekyll directories in `.env`:

```bash
JEKYLL_POSTS_DIR=_posts
JEKYLL_ASSETS_DIR=assets/images
```

### Scripting / Automation

You can call the script from other scripts or automate it:

```bash
#!/bin/bash
# Example: Post from a drafts directory

for file in drafts/*.md; do
    python scripts/cross_poster.py \
        --title "$(basename "$file" .md)" \
        --file "$file" \
        --category data-science \
        --hashtags datascience
done
```

### Integration with Git Hooks

Add to `.git/hooks/post-commit` to auto-post when committing new content:

```bash
#!/bin/bash
# Example: Auto-post new Jekyll posts
# (Use with caution - you may want manual control)

git diff --name-only HEAD HEAD~1 | grep "^_posts/" | while read file; do
    # Extract title and post to LinkedIn
    # (Implementation left as exercise)
done
```

## Contributing

Found a bug or have a feature request? Please open an issue in the GitHub repository.

## License

This project is part of the [lfaller.github.io](https://github.com/lfaller/lfaller.github.io) repository.

## Support

For questions or issues:
1. Check the troubleshooting section above
2. Review the [LinkedIn API documentation](https://docs.microsoft.com/en-us/linkedin/)
3. Open an issue on GitHub

---

**Happy posting!** 🎉
