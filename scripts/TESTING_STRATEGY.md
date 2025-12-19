# BWIB Cross-Posting System - Testing Strategy

## Overview

This document outlines the testing strategy for the automated cross-posting system that transforms Jekyll blog posts into Astro format and opens PRs on the BWIB webpage repository.

## Testing Phases

### Phase 1: Unit Testing (Local, No External Dependencies)
Test individual components in isolation to verify transformation logic.

#### 1.1 Slug Generation Tests
**Goal**: Verify slug format conversion from Jekyll to Sammy's format

```bash
# Test case 1: Jekyll format conversion
Input:  2025-11-27-thanksgiving-in-biotech.md (author: lina)
Expected: 20251127_thanksgiving-in-biotech_lina

# Test case 2: Already in new format (idempotent)
Input:  20251127_thanksgiving-in-biotech_lina.md
Expected: 20251127_thanksgiving-in-biotech_lina

# Test case 3: Different author
Input:  2025-12-01-sample-post.md (author: guest)
Expected: 20251201_sample-post_guest

# Test case 4: Slug with multiple hyphens
Input:  2025-12-15-very-long-post-title.md (author: lina)
Expected: 20251215_very-long-post-title_lina
```

**Validation**: Print slug output and verify format matches `YYYYMMDD_{description}_{author}`

#### 1.2 Date Format Conversion Tests
**Goal**: Verify Jekyll date → ISO 8601 with timezone offset

```bash
# Test case 1: Standard Jekyll format with negative timezone
Input:  "2025-11-27 08:00:00 -0500"
Expected: "2025-11-27T08:00:00-05:00"

# Test case 2: Positive timezone
Input:  "2025-12-01 14:30:00 +0100"
Expected: "2025-12-01T14:30:00+01:00"

# Test case 3: Midnight
Input:  "2025-12-15 00:00:00 -0500"
Expected: "2025-12-15T00:00:00-05:00"

# Test case 4: Single digit timezone (rare)
Input:  "2025-11-27 08:00:00 -0500"
Expected: "2025-11-27T08:00:00-05:00"
```

**Validation**: Verify output matches ISO 8601 format with timezone offset

#### 1.3 Excerpt Extraction Tests
**Goal**: Verify intelligent excerpt generation

```bash
# Test case 1: Post with image + title + content
Input: "![alt](url)\n\n**Title**\n\nFirst paragraph here."
Expected: "First paragraph here." (skips image and title)

# Test case 2: Long paragraph truncation
Input: "This is a very long paragraph that goes on and on..."
Expected: Truncated to 200 chars with "…"

# Test case 3: Multiple paragraphs
Input: "Para 1\n\nPara 2\n\nPara 3"
Expected: "Para 1" (first non-empty, substantial paragraph)

# Test case 4: Content with markdown formatting
Input: "This **bold** and *italic* text."
Expected: "This bold and italic text." (formatting removed)

# Test case 5: Empty or minimal content
Input: "" or "   "
Expected: "Check out this post" (fallback)
```

**Validation**: Check excerpt length ≤ 200 chars, no markdown, no HTML

#### 1.4 Image Detection Tests
**Goal**: Verify image extraction from markdown

```bash
# Test case 1: Image at start
Input: "![Alt text](/images/photo.png)\n\nContent"
Expected: image="/images/photo.png", imageAlt="Alt text"

# Test case 2: Image with long alt text
Input: "![Very long descriptive alt text here](/img.png)"
Expected: image="/img.png", imageAlt="Very long..." (preserved)

# Test case 3: No image in post
Input: "Just text content"
Expected: image="/images/posts/featured.png", imageAlt="Featured image" (fallback)

# Test case 4: Multiple images (should use first)
Input: "![First](/1.png)\n\n![Second](/2.png)"
Expected: Uses first image at index
```

**Validation**: Verify image path extracted correctly, alt text preserved

#### 1.5 Category → Tags Conversion Tests
**Goal**: Verify Jekyll categories become BWIB tags

```bash
# Test case 1: Single category
Input: categories: "biotech"
Expected: tags: ["biotech"], category: "Quick Take"

# Test case 2: Multiple categories (list)
Input: categories: ["biotech", "data-science"]
Expected: tags: ["biotech", "data-science"], category: "Quick Take"

# Test case 3: Category with spaces
Input: categories: "data science"
Expected: tags: ["data-science"], category: "Quick Take"

# Test case 4: No categories
Input: categories: []
Expected: tags: [], category: "Quick Take"

# Test case 5: Category with mixed case
Input: categories: "BioTech"
Expected: tags: ["biotech"], category: "Quick Take"
```

**Validation**: Tags should be lowercase with dashes, category always "Quick Take"

#### 1.6 Full Transformation Tests
**Goal**: Verify end-to-end transformation

```bash
# Test with actual Jekyll post
Input: _posts/2025-11-27-thanksgiving-in-biotech.md
Command: python3 scripts/transform_to_astro.py <file> --config scripts/crosspost_config.json

Verification checklist:
✓ Slug: 20251127_thanksgiving-in-biotech_lina
✓ publishDate: 2025-11-27T08:00:00-05:00
✓ title: "Thanksgiving in Biotech: A Survival Guide"
✓ excerpt: Starts with "Explaining what you do..." (not title)
✓ image: Extracted from markdown
✓ imageAlt: Extracted correctly
✓ category: "Quick Take"
✓ tags: ["biotech"]
✓ authors: [{name: "Lina L. Faller, PhD", link: "https://linkedin.com/in/linafaller"}]
✓ metadata.canonical: https://linafaller.github.io/posts/20251127_thanksgiving-in-biotech_lina/
✓ No attribution link in post content (handled by canonical)
✓ Content unchanged (except for frontmatter)
```

---

### Phase 2: Integration Testing (Script-Level)
Test the complete transformation pipeline without external API calls.

#### 2.1 Configuration Loading Tests
**Goal**: Verify config file parsing and defaults

```bash
# Test: Load and validate crosspost_config.json
Expected:
✓ author_mapping loaded correctly
✓ default_category = "Quick Take"
✓ PR description template exists and has placeholders
✓ canonical_url_template uses {slug}
```

#### 2.2 Multiple Post Processing
**Goal**: Verify batch processing of posts

```bash
# Test: Process multiple posts in sequence
python3 scripts/crosspost_to_bwib.py \
  _posts/2025-11-27-thanksgiving-in-biotech.md \
  _posts/2025-12-19-tool-consolidation-paradox.md

Expected:
✓ Both posts transformed
✓ Different slugs generated
✓ No cross-contamination of metadata
```

#### 2.3 Error Handling Tests
**Goal**: Verify graceful error handling

```bash
# Test case 1: Invalid YAML frontmatter
Input: Post with malformed YAML
Expected: Error message, exit code 1

# Test case 2: Missing required field (title)
Input: Post without title
Expected: Uses default "Untitled", exits gracefully

# Test case 3: File not found
Input: Non-existent file path
Expected: Error message, exit code 1

# Test case 4: Invalid config file
Input: Malformed JSON in config
Expected: Error message, exit code 1
```

---

### Phase 3: GitHub Actions Workflow Testing

#### 3.1 Manual Workflow Trigger (Pre-deployment)
**Goal**: Test workflow without deploying to main

```bash
# On feature/bwib-crosspost branch:

1. Go to GitHub: Actions → Cross-post to BWIB Webpage
2. Click "Run workflow"
3. Select branch: feature/bwib-crosspost
4. Leave post_file blank (uses latest)
5. Click "Run workflow"

Expected:
✓ Workflow starts
✓ Python dependencies installed
✓ Script runs successfully
✓ Logs show transformation details
✓ No actual PR created (because CROSSPOST_GH_TOKEN may not be set)
```

#### 3.2 Secret Configuration Testing
**Goal**: Verify GitHub secrets are properly configured

```bash
# Check in your repository settings:

1. Settings → Secrets and variables → Actions
2. Verify these secrets exist:
   - CROSSPOST_GH_TOKEN (should be set)
   - CROSSPOST_TARGET_REPO (should be: Boston-area-Women-in-Bioinformatics/webpage)

Expected:
✓ Both secrets present
✓ Token has correct permissions (repo scope)
✓ Token is not expired
```

#### 3.3 Workflow Permissions Testing
**Goal**: Verify GitHub Actions has write permissions

```bash
# Check in repository settings:

1. Settings → Actions → General
2. Workflow permissions should have:
   - ☑ Read and write permissions
   - ☑ Allow GitHub Actions to create and approve pull requests

Expected:
✓ Both options enabled
✓ Workflow can create branches and PRs
```

---

### Phase 4: End-to-End Testing (With External Dependencies)
**⚠️ CAREFUL**: Only do this when ready for production

#### 4.1 Test with Real BWIB Repo Access
**Prerequisites:**
- Valid GitHub token with write access to BWIB repo
- CROSSPOST_GH_TOKEN secret configured
- Workflow permissions granted

**Steps:**

```bash
# Option A: Manual local test
export GH_TOKEN="your_github_token"
export CROSSPOST_TARGET_REPO="Boston-area-Women-in-Bioinformatics/webpage"
python3 scripts/crosspost_to_bwib.py _posts/2025-11-27-thanksgiving-in-biotech.md

Expected:
✓ Script creates feature branch on BWIB repo
✓ Post file committed to src/content/post/{slug}.md
✓ PR opened with review checklist
✓ PR title: "Cross-post: Thanksgiving in Biotech: A Survival Guide"
✓ PR includes checklist with all fields

# Option B: GitHub Actions workflow trigger
1. Merge feature/bwib-crosspost to main
2. Create a test post or modify existing one
3. Push to main
4. Workflow triggers automatically
5. Check BWIB repo for new PR
```

#### 4.2 PR Review & Validation
**In BWIB Repository:**

```markdown
PR Checklist:
☑ Slug format: 20251127_thanksgiving-in-biotech_lina
☑ Category: "Quick Take" (default, can be changed)
☑ Tags: ["biotech"] (auto-generated from Jekyll categories)
☑ Image path: /assets/images/posts/... (needs to be updated to /blog_images/...)
☑ Image alt text: Present and descriptive
☑ Canonical URL: Points back to original blog
☑ Content: Unchanged from original
☑ No attribution link in post content (handled by canonical metadata)
☑ PR description has complete checklist
☑ Can be merged without errors
```

---

## Testing Checklist

### Before Merging to Main
- [ ] All unit tests pass (Phase 1)
- [ ] Integration tests pass (Phase 2)
- [ ] Manual workflow trigger works (Phase 3.1)
- [ ] Secrets configured (Phase 3.2)
- [ ] Permissions granted (Phase 3.3)
- [ ] Documentation reviewed and accurate

### After Merging to Main
- [ ] Create test post or push existing post
- [ ] Verify workflow triggers automatically
- [ ] Check for PR on BWIB repo
- [ ] Validate PR contents against checklist
- [ ] Test PR review workflow with Sammy
- [ ] Merge test PR and verify build succeeds

### Production Deployment
- [ ] All testing phases completed
- [ ] Sammy reviews and approves setup
- [ ] Test with 1-2 real posts before full automation
- [ ] Monitor first 5-10 cross-posts closely
- [ ] Adjust configuration based on feedback

---

## Quick Test Commands

Run these locally to verify the system:

```bash
# Test 1: Transform a sample post
python3 scripts/transform_to_astro.py _posts/2025-11-27-thanksgiving-in-biotech.md \
  --config scripts/crosspost_config.json > /tmp/test_output.md

# Test 2: Check slug format
grep "^slug:" /tmp/test_output.md
# Expected: slug: 20251127_thanksgiving-in-biotech_lina

# Test 3: Check date format
grep "^publishDate:" /tmp/test_output.md
# Expected: publishDate: '2025-11-27T08:00:00-05:00'

# Test 4: Check category
grep "^category:" /tmp/test_output.md
# Expected: category: Quick Take

# Test 5: Check tags (from Jekyll categories)
grep -A 1 "^tags:" /tmp/test_output.md
# Expected: tags:
#           - biotech

# Test 6: Verify no attribution in content
grep -c "Originally posted on" /tmp/test_output.md
# Expected: 0 (zero - attribution should be in metadata, not content)

# Test 7: Verify canonical URL
grep "canonical:" /tmp/test_output.md
# Expected: canonical: https://linafaller.github.io/posts/20251127_thanksgiving-in-biotech_lina/
```

---

## Known Limitations & Edge Cases

1. **Image Migration**: Images are not automatically copied. BWIB team must handle this.
2. **Special Characters**: URLs and titles with special characters may need escaping.
3. **Code Blocks**: Markdown code blocks are preserved but not syntax-highlighted differently.
4. **HTML in Posts**: If Jekyll posts have embedded HTML, it will be passed through as-is.
5. **Author Mapping**: Only authors in `crosspost_config.json` will be properly mapped.

---

## Success Criteria

The system is considered successful when:

✓ 100% of unit tests pass
✓ All integration tests pass
✓ GitHub Actions workflow completes without errors
✓ PRs open correctly on BWIB repo with proper format
✓ Sammy can merge PRs without manual fixes needed
✓ Posts publish correctly on BWIB site
✓ Attribution link works in canonical metadata
✓ No manual intervention required per post (after initial setup)

---

## Questions for Sammy

Before full deployment, ask Sammy:

1. Can you successfully merge the test PR?
2. Do the auto-generated fields match your preferences?
3. Is the slug format (YYYYMMDD_{description}_{author}) clear?
4. Are the tags derived from Jekyll categories useful?
5. Should we adjust anything in the default category or tags?
6. Any issues with image path placeholders?

---

**Version**: 1.0
**Created**: December 2025
**Last Updated**: December 2025
