---
layout: post
author: lina
title: "Testing BWIB Cross-Posting: A Quick Example"
date: 2025-12-22 10:00:00 -0500
categories:
  - biotech
  - testing
---

![A celebration of successful automation](/assets/images/posts/cross-post-test.png)

## Testing BWIB Cross-Posting

This is a test post to verify our new cross-posting automation system works correctly.

The key features we're testing:
- Slug generation in the new format: `YYYYMMDD_{description}_{author}`
- Date conversion to ISO 8601 with timezone preservation
- Excerpt extraction from the first substantial paragraph
- Image detection and metadata extraction
- Category to tags mapping
- Canonical URL attribution

If you're seeing this post on the BWIB website, it means the automation worked! The post was automatically transformed from Jekyll format to Astro format and a PR was opened for review.

## What Happens Next

The BWIB web development team will:
1. Review the auto-generated fields
2. Adjust the excerpt or category if needed
3. Download and host the featured image
4. Merge the PR when ready

This workflow ensures content is properly formatted and reviewed before it appears on the BWIB site.

## Questions?

Feel free to check out the [cross-posting documentation](https://github.com/lfaller/lfaller.github.io/tree/feature/bwib-crosspost/scripts) for more details.
