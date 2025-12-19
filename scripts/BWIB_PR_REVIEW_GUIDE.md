# BWIB Cross-Post PR Review Guide

This guide is for the BWIB web development team when reviewing cross-posted PRs from Lina's blog.

## About Cross-Posts

Cross-posted PRs are automatically opened by Lina's blog GitHub Actions workflow. They transform Jekyll blog posts into Astro format with auto-generated metadata.

**Your role (BWIB web development team tasks)**:
- Review the transformation and auto-generated fields
- Adjust/customize fields for BWIB's audience
- Download and upload featured images to `public/blog_images/`
- Ensure quality before merging

## PR Structure

Each PR includes:

1. **Transformed post file**: Located in `src/content/post/{slug}.md`
2. **Auto-generated fields**: Marked in the PR description
3. **Review checklist**: Things to verify before merging
4. **Original URL**: Link to the original post for reference

## Review Checklist

### Front Matter Fields

#### ✅ Excerpt
- Should be compelling and ~150 characters max
- Should summarize the post, not just be the first sentence
- **If needed**: Edit in the PR to improve

Example of auto-generated (may need work):
```
"Thanksgiving in Biotech: A Survival Guide"
```

Better excerpt:
```
"Learn how to explain your biotech job to family at the dinner table - and why it's great training for cross-functional communication."
```

#### ✅ Category
- BWIB's categories are different from Lina's Jekyll categories
- Default for cross-posts: **"Quick Take"** (unless a different category is more appropriate)
- Common categories: "Quick Take", "Deep Dive", "Career", "Tools & Resources", "Podcast", "Video"
- **Action**: Verify/set the appropriate category

#### ✅ Tags
- Auto-populated from Lina's Jekyll categories (converted to tags)
- Usually 3-5 tags total
- Use lowercase with dashes (e.g., `data-science` not `Data Science`)
- Should match BWIB's existing tags where possible
- **Action**: Review auto-generated tags and add/remove as needed

Example of auto-generated tags from Jekyll categories:
```yaml
tags:
  - biotech          # from Jekyll "biotech" category
  - data-science     # from Jekyll "data-science" category or added manually
  - career
```

#### ✅ Featured Image

**Current state in PR**: The image path will show the original path from Lina's blog (e.g., `/assets/images/posts/2025-11-27-thanksgiving-in-biotech.png`)

**Your job (Sammy)**:
1. **Download the image**: Go to `https://linafaller.github.io/assets/images/posts/{filename}` and save it
2. **Upload to your repo**:
   - Go to `public/blog_images/` in the BWIB repo
   - Upload the image file
   - Note the filename
3. **Update the image path** in the PR to: `/blog_images/{filename}`
4. **Commit the change** to the PR branch

**Example**:
- Original: `/assets/images/posts/2025-11-27-thanksgiving-in-biotech.png`
- After upload to `public/blog_images/`: `/blog_images/2025-11-27-thanksgiving-in-biotech.png`

**Alternative** (if you prefer not to copy images):
- Update path to full URL: `https://linafaller.github.io/assets/images/posts/2025-11-27-thanksgiving-in-biotech.png`
- This links directly to Lina's blog (works fine, but less ideal for independence)

#### ✅ Image Alt Text
- Should be descriptive and accessible
- Typically under 125 characters
- Should describe the image's purpose for someone who can't see it
- **If unclear**: Improve the alt text

Examples:
- ❌ "image"
- ❌ "thanksgiving"
- ✅ "A plate of pie next to a laptop with code"

#### ✅ Author Information
- Verify author name and LinkedIn URL are correct
- Should match the format:
  ```yaml
  authors:
    - name: "Lina L. Faller, PhD"
      link: "https://linkedin.com/in/linafaller"
  ```

#### ✅ Metadata (SEO)
- **Title**: Should match the post title
- **Description**: Should be clear and searchable
- **Canonical**: Should point back to Lina's original post
- Usually auto-generated correctly; adjust if needed

### Content Fields

#### ✅ Post Content
- Verify the markdown formatting is correct
- Check that code blocks and emphasis are preserved
- Verify images render properly (may need path updates)
- Look for any broken links

#### ✅ Attribution & Canonical Link
- The `canonical` link in metadata automatically points back to Lina's original post
- This provides proper attribution and SEO credit
- No need to add a manual attribution link in the post content

## Common Issues & Fixes (Sammy's Troubleshooting)

### Issue: Image Not Found

**Symptom**: Image shows broken link icon when you preview/publish

**Fix Options**:
1. **Copy image to BWIB repo** (recommended):
   - Download from `https://linafaller.github.io/assets/images/posts/{filename}`
   - Upload to `public/blog_images/` folder
   - Update image path to `/blog_images/{filename}`

2. **Link directly to Lina's blog** (simpler alternative):
   - Update path to `https://linafaller.github.io/assets/images/posts/{filename}`
   - Include full URL instead of relative path
   - Works fine, just depends on Lina's site for images

### Issue: Category Not Recognized

**Symptom**: Build error or category doesn't display

**Fix**:
- Check what categories your Astro setup supports
- Update the category field to match available options
- Common: "Deep Dive", "Career", "Tools & Resources", "Podcast", "Event"

### Issue: Excerpt Seems Off

**Symptom**: Auto-generated excerpt doesn't capture the essence

**Fix**:
- Write a custom excerpt (1-2 sentences, ~150 chars)
- Make it compelling for your audience
- Think: "What would make someone click on this post?"

### Issue: Too Many/Too Few Tags

**Symptom**: Tags don't match BWIB's style

**Fix**:
- Look at existing posts and match tag style
- Aim for 3-5 tags
- Should be lowercase with hyphens (e.g., `data-science` not `Data Science`)

## Quick Approval Workflow

For a standard cross-post PR:

1. **2 min**: Check front matter fields against checklist
2. **2 min**: Verify image path and download/update if needed
3. **2 min**: Skim content for any obvious issues
4. **1 min**: Request changes OR approve
5. **1 min**: Merge and monitor build

**Total**: ~5-10 minutes per post

## Making Changes in the PR (Web Development Team Tasks)

You can make changes in several ways:

### Direct Edits (For small changes)
1. Click the file (`src/content/post/{slug}.md`)
2. Click the edit button (✏️)
3. Make your changes (edit front matter fields, excerpt, etc.)
4. Commit to the PR branch with a message like "Update excerpt" or "Fix category"

### Image Uploads
1. Go to `public/blog_images/` folder
2. Click "Add files" → "Upload files"
3. Select Lina's image and upload
4. This commit will be added to the PR

### Requesting Changes
1. Click **Review changes**
2. Select **Request changes**
3. Comment on specific lines with suggestions
4. Submit review (Lina can then make changes)

## Merging (Web Development Team Task)

Once you're happy with all changes:

1. Click **Merge pull request**
2. Choose merge strategy (usually "Create a merge commit" is fine)
3. Delete the branch (recommended)
4. Verify the build runs successfully in GitHub Actions
5. Post should appear on BWIB website!

## Questions to Ask Lina (if needed)

If a cross-post has issues that need her attention:

- "Can you provide the high-res image?"
- "What category does this belong in for BWIB?"
- "Should this post really be cross-posted?"
- "Can you update the image URLs in your Jekyll post?"
- "Can you clarify the excerpt for BWIB's audience?"

## If You Want to Pause Cross-Posts

Contact Lina and she can:
- Disable the workflow temporarily in GitHub Actions
- Update `scripts/crosspost_config.json` and set `"enabled": false`
- Re-enable whenever you're ready

## Reference

- **Astro Docs**: https://docs.astro.build/
- **BWIB Repo**: https://github.com/Boston-area-Women-in-Bioinformatics/webpage
- **Lina's Blog Repo**: https://github.com/lfaller/lfaller.github.io
- **Contact**: Lina or create an issue in the BWIB repo

---

**Tips for Success**:
- ✅ Keep excerpts engaging and unique to BWIB audience
- ✅ Download and include images when possible (better UX)
- ✅ Adjust categories to match BWIB's taxonomy
- ✅ Add tags that help discoverability
- ✅ Always keep the attribution link
- ❌ Don't change the core post content without asking Lina

---

**Version**: 1.0
**Last Updated**: December 2025
