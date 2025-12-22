---
layout: post
author: lina
title: "Image Copy Test: Automatic Image Transfer"
date: 2025-12-22 21:00:00 -0500
categories:
  - testing
  - images
---

![The bioinformatics triangle showing relationships](/assets/images/posts/2025-07-15-the-bioinformatics-triangle.png)

## Testing Automatic Image Transfer

This post verifies that images are automatically copied to the BWIB repo during cross-posting.

### What Should Happen

1. **Image Detection**: The system detects the featured image in the markdown
2. **File Lookup**: Finds the image file in your blog's assets directory
3. **Image Copy**: Copies the image to `public/blog_images/` in the BWIB repo
4. **Path Update**: Updates the frontmatter to point to the new location: `/blog_images/{filename}`
5. **Git Commit**: Commits both the post and the image in the PR

### The Result

The image should now be:
- ✓ Automatically copied to BWIB's repo
- ✓ Available in `public/blog_images/`
- ✓ Referenced with the new path
- ✓ Ready to be merged with the post

This eliminates manual image handling for the BWIB team!
