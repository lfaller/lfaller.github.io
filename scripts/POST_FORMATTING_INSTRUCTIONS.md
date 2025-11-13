# LinkedIn-Jekyll Post Formatting Instructions

Use these instructions when converting a LinkedIn post draft into a properly formatted Jekyll markdown file for the lfaller.github.io blog.

## Required Frontmatter Format

Start the file with YAML frontmatter in **exactly** this format:

```yaml
---
layout: post
author: lina
title:  "Post Title Here"
date:   YYYY-MM-DD 08:00:00 -0500
categories: category-name
---
```

**Important frontmatter rules:**
- Field order MUST be: layout, author, title, date, categories
- Use **two spaces** after `title:` and `date:` before the value
- Date format: `YYYY-MM-DD 08:00:00 -0500` (always 8am Eastern Time)
- Title: Use double quotes around the title
- Categories: Use lowercase with hyphens (e.g., `data-engineering`, `data-science`)
- No extra blank lines within frontmatter

## Content Formatting

### Bold Text
- Use `**text**` for bold (converts to Unicode bold on LinkedIn)
- Apply bold to:
  - Key concepts and important phrases
  - Section headers (if not using `##` headers)
  - Emphasis points

### Headers
- Use `##` for section headers
- Headers convert to Unicode bold on LinkedIn
- No `#` (h1) headers - the title is h1

### Lists
Use markdown list format with hyphens:

```markdown
- First point
- Second point
- Third point
```

**Not:**
- ❌ Numbered lists (use hyphens instead)
- ❌ Asterisks (*) or plus signs (+)
- ✅ Hyphens (-) only

### Links
Keep markdown link format:
```markdown
[link text](https://example.com)
```

On LinkedIn, only the URL will show. On Jekyll, it renders as a proper hyperlink.

### Images

Add image reference after frontmatter:

```markdown
---
frontmatter here
---

![Alt text description](/assets/images/posts/YYYY-MM-DD-post-slug.png)

Rest of content...
```

**Image path format:**
- Always use: `/assets/images/posts/YYYY-MM-DD-descriptive-name.png`
- Match the date to your post date
- Use descriptive filename matching the post slug
- Alt text should describe the image content

### Hashtags

Place hashtags at the **very end** of the post in an HTML comment:

```markdown
Your post content here...

Last paragraph of content.

<!-- #HashTag1 #HashTag2 #HashTag3 -->
```

**Hashtag rules:**
- Must be inside HTML comment: `<!-- hashtags here -->`
- Use PascalCase (capitalize each word, no spaces)
- 3-5 hashtags recommended
- Common tags: `#DataEngineering` `#DataScience` `#Bioinformatics` `#MachineLearning` `#AI`

## Complete Example

```markdown
---
layout: post
author: lina
title:  "Data Pipelines That Scientists Can Debug"
date:   2025-11-13 08:00:00 -0500
categories: data-engineering
---

![Pipeline debugging workflow comparison](/assets/images/posts/2025-11-13-data-pipelines-scientists-can-debug.png)

**Data Pipelines That Scientists Can Debug (Without Calling You at 9 PM)**

"Hey, the pipeline failed again. Can you take a look?"

## The Problem

This Slack message means your next hour is gone. You'll dig through logs and discover:

- A sample ID mismatch
- A missing metadata field
- A file in the wrong format

The scientist could have fixed it in 30 seconds—if the error message had told them **what to look for**.

## The Solution

Here's what I now build into every production pipeline:

- Error messages that say what AND why
- Data quality checks that explain failures in scientific terms
- Logging that tells a story
- Retry logic that makes sense for biological data
- Clear next steps in every failure

**The best pipeline is one that makes both teams successful.**

<!-- #DataEngineering #Bioinformatics #Biotech #DataScience -->
```

## Filename Convention

Save the file as:
```
YYYY-MM-DD-short-descriptive-slug.md
```

Examples:
- `2025-11-13-data-pipelines-scientists-can-debug.md`
- `2025-11-15-machine-learning-production.md`
- `2025-11-20-database-design-patterns.md`

## Checklist Before Saving

- [ ] Frontmatter has correct field order and spacing
- [ ] Date is 8am ET (`08:00:00 -0500`)
- [ ] Title in double quotes
- [ ] Image path added (if post includes image)
- [ ] Bold formatting applied to key concepts
- [ ] Lists use hyphens (-)
- [ ] Hashtags in HTML comment at end
- [ ] Filename matches date and has descriptive slug
- [ ] No extra blank lines at start or end

## Where to Save

- **For immediate posting:** Save to `_posts/` directory
- **For scheduled posting:** Save to `_scheduled-posts/` directory (will auto-post at 8am ET on the scheduled date)

## Common Mistakes to Avoid

❌ **Wrong:**
```yaml
---
title: "Post Title"
date: 2025-11-13
layout: post
---
```

✅ **Correct:**
```yaml
---
layout: post
author: lina
title:  "Post Title"
date:   2025-11-13 08:00:00 -0500
categories: data-science
---
```

❌ **Wrong hashtags:**
```markdown
#DataScience #AI
```

✅ **Correct hashtags:**
```markdown
<!-- #DataScience #AI -->
```

❌ **Wrong lists:**
```markdown
* First item
* Second item
```

✅ **Correct lists:**
```markdown
- First item
- Second item
```

## Notes

- The system automatically converts `**bold**` to Unicode bold (𝗯𝗼𝗹𝗱) on LinkedIn
- Images automatically upload to LinkedIn
- Hashtags hidden from Jekyll site, visible on LinkedIn
- Posts in `_scheduled-posts/` publish automatically at 8am ET on their date
