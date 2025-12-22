---
layout: post
author: lina
title: "Image Handling in Cross-Posts: Making Sure Everything Works"
date: 2025-12-22 20:30:00 -0500
categories:
  - testing
  - images
---

![The bioinformatics triangle showing relationships](/assets/images/posts/2025-07-15-the-bioinformatics-triangle.png)

## Testing Image Extraction and Transfer

One of the key features of the cross-posting system is properly handling images from Jekyll posts.

### How Images Are Handled

When you publish a post with an image:

1. **The transformation script detects the image** in your Jekyll markdown
2. **Extracts the image path and alt text** from the markdown syntax
3. **Includes the image metadata** in the Astro frontmatter
4. **The BWIB team reviews the image path** in the PR
5. **They decide how to handle the image** (copy to their repo, link to yours, etc.)

### Why This Matters

Images are critical to engagement. By including the image path in the frontmatter:
- The BWIB team knows exactly which image goes with the post
- They have the original alt text for accessibility
- They can host the image however makes sense for their workflow

### The Test

This post uses a real image from your existing posts to verify the entire system works end-to-end:
- Image extraction: ✓
- Image metadata in frontmatter: ✓
- PR with image details: ✓
- Ready for BWIB team to handle the image: ✓

Let's see how it shows up in the PR!
