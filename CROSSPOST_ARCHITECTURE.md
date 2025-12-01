# Cross-Posting Architecture: Blog Automation Solution

## Current Situation

### Your Site (Lina's Blog)
- **Platform**: Jekyll
- **Post Location**: `_posts/`
- **Front Matter Format**: Simple YAML
  - `layout`, `author`, `title`, `date`, `categories`

### Her Site (Boston Women in Bioinformatics)
- **Platform**: Astro 4.0 + Tailwind CSS
- **Post Location**: `src/content/post/`
- **Front Matter Format**: Detailed YAML with:
  - `publishDate`, `slug`, `excerpt`, `image`, `imageAlt`, `imagePosition`
  - `author`/`authors` (with LinkedIn URLs), `category`, `tags`
  - `metadata` (SEO: title, description, canonical URL)
  - `listeningTime` (optional, for podcasts)

---

## Two Possible Approaches

### Option 1: GitHub Actions Workflow (Recommended for Automation)

Extend your existing cross-posting infrastructure to automatically create PRs on her repository.

**Flow:**
1. New post is pushed to your `_posts/` directory
2. GitHub Actions workflow detects the change
3. Python script parses your Jekyll front matter + markdown content
4. Transforms it to Astro format
5. Creates a commit in her repo with the transformed post
6. Opens a PR for her review and manual adjustments

**Pros:**
- Fully automated, requires minimal manual work
- Builds on your existing workflow patterns
- She gets a PR to review and customize before publishing
- Clear audit trail of what was auto-generated vs. manually adjusted

**Cons:**
- Requires GitHub token with write access to her repository
- More setup complexity (authentication, API calls)
- Requires coordination on her end initially

**Best For:** Regular content sharing with occasional customization

---

### Option 2: Shared Content Source (Alternative - Single Source of Truth)

Instead of cross-posting to her repository, create a canonical content source that she pulls from.

**Flow:**
1. You maintain posts in your repo
2. Export/expose posts in a standardized format (JSON feed, shared directory, or API)
3. She sets up a GitHub Action on her end that:
   - Periodically pulls your posts (or triggers on your push)
   - Transforms them to Astro format
   - Creates a PR or auto-commits on her repo

**Pros:**
- Single source of truth = no duplicate maintenance
- Cleaner separation of concerns
- She has full control over transformation on her end
- No need to give access to her repository

**Cons:**
- Requires setup work on her side
- Slightly more latency between your post and her availability
- Requires her to maintain the pull/transform logic

**Best For:** Long-term scalability, multiple cross-posting destinations, if she wants ownership of the process

---

## Recommended Solution: Option 1 with GitHub App

Combines automation with security best practices.

### Field Mapping

| Your Post | Her Post | Notes |
|-----------|----------|-------|
| `layout` | — | Not needed in Astro |
| `author: "lina"` | `authors: [{name: "...", linkedin: "..."}]` | Convert to author object with LinkedIn URL |
| `title` | `title` | Direct copy |
| `date` | `publishDate` | Convert to ISO 8601 format with Z (e.g., `2025-11-27T08:00:00Z`) |
| `categories` | `category` | Pick primary category (single value in her system) |
| — | `slug` | Generate from filename (e.g., `2025-11-27-thanksgiving-in-biotech`) |
| — | `excerpt` | **PR default**: Auto-extract first paragraph or ~150 chars; she edits in PR |
| — | `image` | **PR default**: Placeholder path (e.g., `/images/posts/...`); she confirms/adjusts |
| — | `imageAlt` | **PR default**: Placeholder based on filename; she provides descriptive text |
| — | `imagePosition` | **PR default**: `"top"`; she can adjust to `"center"` or `"bottom"` |
| — | `tags` | **PR default**: Generated from `categories` + keywords; she refines |
| — | `metadata` | Auto-generated: title, description (from excerpt), canonical URL to your post |

### Implementation Components

#### 1. Python Transformation Script

```python
# scripts/transform_post.py
# Reads Jekyll post → outputs Astro markdown with transformed front matter
# Handles:
#   - YAML parsing and field mapping
#   - Date format conversion
#   - Author object creation
#   - Slug generation from filename
#   - Auto-excerpt generation
#   - Image path handling
```

#### 2. GitHub Actions Workflow

**Trigger**: Push to `_posts/` directory
**Steps**:
1. Checkout your repo
2. Setup Python + dependencies
3. Detect changed post files
4. Transform each post with Python script
5. Authenticate with her repo (GitHub token/app)
6. Commit transformed post to her repo
7. Open PR with:
   - Post file
   - PR description explaining auto-generated fields
   - Checklist of fields for her to review/adjust

#### 3. Configuration

**Secrets needed in your repo:**
- `GITHUB_TOKEN` with write access to her repo (or use GitHub App)
- `WEBPAGE_REPO_OWNER` (e.g., `Boston-area-Women-in-Bioinformatics`)
- `WEBPAGE_REPO_NAME` (e.g., `webpage`)
- `WEBPAGE_BOT_BRANCH_PREFIX` (e.g., `cross-post/` for branch naming)

**Configuration file** (optional YAML for customization):
```yaml
cross_post:
  enabled: true
  target_repo: "Boston-area-Women-in-Bioinformatics/webpage"
  target_path: "src/content/post/"
  author_mapping:
    lina:
      name: "Lina L. Faller, PhD"
      linkedin: "https://linkedin.com/in/linafaller"
  category_mapping:
    biotech: "Deep Dive"
    bioinformatics: "Deep Dive"
```

---

## PR Review Checklist

When a PR is opened on her repository, it will include a checklist like:

```markdown
## Cross-Post Review Checklist

- [ ] Excerpt is appropriate and engaging
- [ ] Category is correct (current: "Deep Dive")
- [ ] Tags are relevant
- [ ] Featured image path is correct
- [ ] Image alt text is descriptive
- [ ] Canonical link points to original post
- [ ] Author information is accurate
```

---

## Initial Setup Requirements

### For Your Repository
1. Create Python transformation script
2. Add new GitHub Actions workflow (or extend existing)
3. Store secrets: GitHub token for her repo
4. Test with a manual workflow dispatch

### For Her Repository
1. **Optional**: Create a branch protection rule allowing cross-post PRs
2. **Optional**: Set up a CODEOWNERS file or auto-assign reviewer
3. **Optional**: Document her review expectations for these PRs

### For Ongoing Maintenance
- She reviews and merges PRs as they arrive
- She can edit front matter in PR or ask for changes
- Every 6-12 months: review field mappings if either platform updates

---

## Alternative: Minimal Implementation

If full automation feels like overkill:

**Manual Script Option**: Create a Python CLI tool that:
- Takes your post file as input
- Outputs the transformed Astro markdown
- She manually commits/PRs to her repo

```bash
python scripts/transform_post.py _posts/2025-11-27-thanksgiving-in-biotech.md --output-dir ~/webpage/src/content/post/
```

This removes the GitHub Actions complexity while still automating the transformation work.

---

## Questions to Discuss

1. **Frequency**: How often will new posts be shared? (Weekly? Sporadic?)
2. **Approval**: Does she want to review/adjust before publishing, or auto-merge?
3. **Attribution**: Should posts link back to your blog as canonical source?
4. **Images**: Do images need to be copied to her repo, or can they link to yours?
5. **Metadata**: What are her must-have fields vs. nice-to-haves?
6. **Authentication**: Is she comfortable with a GitHub token, or should we explore GitHub App?

---

## Recommendation Summary

**Start with Option 1** (GitHub Actions + PR workflow) because:
- ✅ Leverages your existing infrastructure
- ✅ Automates 80% of the work
- ✅ Keeps her in the loop with PR review
- ✅ Easily extendable to other platforms later
- ✅ No duplicate content maintenance

**Timeline to MVP**: 2-3 hours for implementation + testing
