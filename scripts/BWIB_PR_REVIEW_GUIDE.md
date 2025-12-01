# BWIB Cross-Post PR Review Guide

This guide is for the BWIB webpage maintainer when reviewing cross-posted PRs from Lina's blog.

## About Cross-Posts

Cross-posted PRs are automatically opened by Lina's blog workflow. They transform Jekyll blog posts into Astro format with auto-generated metadata.

**Your role**: Review the transformation, adjust fields as needed, and ensure quality before merging.

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
- Verify it matches BWIB's available categories
- Common categories: "Deep Dive", "Career", "Tools & Resources", "Podcast"
- **If wrong**: Change from the auto-generated value

#### ✅ Tags
- Should be relevant to the post content
- Usually 3-5 tags
- Should match BWIB's existing tags where possible
- **If needed**: Add or remove tags

Example:
```yaml
tags:
  - biotech
  - career
  - data-science
  - communication
```

#### ✅ Featured Image
- Verify the image path is correct
- Check if image needs to be copied to BWIB repo or external URL
- Common scenarios:
  - **If**: `/assets/images/posts/2025-11-27-thanksgiving-in-biotech.png`
  - **Then**: You may need to:
    - Download the image from Lina's blog and add to `public/images/`
    - OR update the URL to point to Lina's blog
    - OR point to a CDN

**Action**: Update the image path as appropriate for BWIB

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

#### ✅ Attribution Link
- Every cross-posted post includes a link back to the original:
  ```
  *Originally posted on [Lina L. Faller's blog](URL)*
  ```
- This is automatic and should be kept

## Common Issues & Fixes

### Issue: Image Not Found

**Symptom**: Image shows broken link icon when you preview/publish

**Fix Options**:
1. **Copy the image to BWIB repo**:
   - Download from `https://linafaller.github.io/assets/images/posts/{filename}`
   - Add to `public/images/posts/` in BWIB repo
   - Update frontmatter image path to `/images/posts/{filename}`

2. **Link directly to Lina's blog** (simpler):
   - Update path to `https://linafaller.github.io/assets/images/posts/{filename}`
   - Include full URL instead of relative path

3. **Use external CDN**:
   - If you have another image hosting service, add there and link accordingly

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

## Making Changes

You can edit files directly in the PR:

1. Click the file (`src/content/post/{slug}.md`)
2. Click the edit button (✏️)
3. Make your changes
4. Commit to the PR branch

Or request changes:

1. Click **Review changes**
2. Select **Request changes**
3. Comment on specific lines with suggestions
4. Submit review

## Merging

Once approved:

1. Click **Merge pull request**
2. Choose merge strategy (usually "Create a merge commit" is fine)
3. Delete the branch (recommended)
4. Verify the build runs successfully

## Questions to Ask Lina

If a cross-post has issues:

- "Can you provide the high-res image?"
- "What category does this belong in?"
- "Should this post really be cross-posted?"
- "Can you update the image URLs in your Jekyll post?"

## Disabling Cross-Posts

If you want to pause cross-posting temporarily or permanently:

Contact Lina and she can:
- Disable the workflow in GitHub Actions
- Update the configuration in `scripts/crosspost_config.json`
- Set `"enabled": false` to stop processing

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
