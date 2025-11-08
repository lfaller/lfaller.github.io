# LinkedIn Cross-Posting Formatting Guide

This guide explains how to format your Jekyll markdown posts for automatic cross-posting to LinkedIn.

## Bold Text

**In Markdown:**
```markdown
You can use **bold text** like this.
```

**On LinkedIn:**
The script converts bold markdown to Unicode bold sans-serif characters:
- `**bold text**` → 𝗯𝗼𝗹𝗱 𝘁𝗲𝘅𝘁

This maintains visual emphasis on LinkedIn while using plain text formatting.

## Headers

**In Markdown:**
```markdown
## Section Header
```

**On LinkedIn:**
Headers are converted to Unicode bold and placed on their own line:
- `## Section Header` → 𝗦𝗲𝗰𝘁𝗶𝗼𝗻 𝗛𝗲𝗮𝗱𝗲𝗿

## Images

**In Markdown:**
```markdown
![Alt text](/assets/images/posts/my-image.png)
```

**On LinkedIn:**
Images are automatically uploaded to LinkedIn and attached to your post!

The script:
1. Detects image references in your markdown
2. Uploads each image to LinkedIn's media servers
3. Attaches the uploaded images to your post
4. Removes the image path text from the post content

**On Jekyll:**
Images display normally using your Jekyll asset paths.

**Supported Image Paths:**
- Absolute Jekyll paths: `/assets/images/posts/image.png`
- Relative paths: `../images/image.png`
- Multiple images in a single post are supported

**Image Format Requirements:**
- PNG, JPG, GIF formats supported
- Maximum file size: 8MB per image
- Recommended dimensions: 1200x627px (LinkedIn's optimal size)

## Links

**In Markdown:**
```markdown
[link text](https://example.com)
```

**On LinkedIn:**
Links are converted to plain URLs:
- `[link text](https://example.com)` → `https://example.com`

LinkedIn will automatically make the URL clickable.

## Bullet Points

**In Markdown:**
```markdown
- First point
- Second point
- Third point
```

**On LinkedIn:**
Converted to Unicode bullet points:
```
• First point
• Second point
• Third point
```

## Hashtags

You have two options for adding hashtags:

### Option 1: Category-Based (Automatic)

**In Frontmatter:**
```yaml
categories: data-science machine-learning
```

**On LinkedIn:**
Automatically converted to hashtags at the end of the post:
```
#DataScience #MachineLearning
```

**On Jekyll:**
Used as standard Jekyll categories (no hashtags shown).

### Option 2: HTML Comments (Recommended for Additional Hashtags)

**In Markdown:**
```markdown
This is my post content.

<!-- #AI #DeepLearning #NeuralNetworks -->
```

**On LinkedIn:**
Hashtags are extracted and added to the post:
```
#AI #DeepLearning #NeuralNetworks
```

**On Jekyll:**
HTML comments are completely invisible - they won't show up in your published post.

### Combining Both Methods

You can use both methods together. The script will:
1. Extract hashtags from categories
2. Extract hashtags from HTML comments
3. Remove duplicates
4. Append all unique hashtags to the LinkedIn post

**Example:**
```yaml
---
categories: data-science
---

My post about machine learning.

<!-- #MachineLearning #AI #DataScience -->
```

**Result on LinkedIn:**
```
#DataScience #MachineLearning #AI
```

(Note: `#DataScience` appears only once even though it's in both categories and HTML comments)

## Complete Example

**Markdown File:**
```markdown
---
layout: post
author: lina
title:  "Understanding Neural Networks"
date:   2025-11-08 14:30:00 -0500
categories: machine-learning
---

Neural networks are **revolutionizing** the field of artificial intelligence.

## Key Concepts

Here are the fundamental principles:
- **Layers**: Input, hidden, and output layers
- **Weights**: Connections between neurons
- **Activation**: Non-linear transformation functions

Learn more at [my website](https://example.com).

![Neural Network Diagram](/assets/images/nn-diagram.png)

<!-- #DeepLearning #AI #NeuralNetworks -->
```

**LinkedIn Output:**
```
Neural networks are 𝗿𝗲𝘃𝗼𝗹𝘂𝘁𝗶𝗼𝗻𝗶𝘇𝗶𝗻𝗴 the field of artificial intelligence.

𝗞𝗲𝘆 𝗖𝗼𝗻𝗰𝗲𝗽𝘁𝘀

Here are the fundamental principles:
• 𝗟𝗮𝘆𝗲𝗿𝘀: Input, hidden, and output layers
• 𝗪𝗲𝗶𝗴𝗵𝘁𝘀: Connections between neurons
• 𝗔𝗰𝘁𝗶𝘃𝗮𝘁𝗶𝗼𝗻: Non-linear transformation functions

Learn more at https://example.com.

#MachineLearning #DeepLearning #AI #NeuralNetworks
```

**Jekyll Output:**
Displays exactly as written in markdown (with proper rendering of bold, links, images, etc.) - no hashtags visible, no HTML comments shown.

## Best Practices

1. **Use bold sparingly** - Unicode bold is very prominent on LinkedIn
2. **Keep hashtags relevant** - LinkedIn recommends 3-5 hashtags per post
3. **Test locally first** - Run the script manually to preview the LinkedIn output:
   ```bash
   cd scripts
   source venv/bin/activate
   python linkedin_post.py ../_posts/your-post.md
   ```
4. **Images** - For now, remove image references if they're critical to the post content, or describe them in text
5. **Links** - Keep link text descriptive since only the URL will show on LinkedIn

## Formatting Not Supported

The following markdown features are simplified for LinkedIn:

- **Italic text** - Removed (no Unicode italic equivalent)
- **Inline code** - Backticks removed, displays as plain text
- **Code blocks** - Currently not preserved (consider using screenshots for code)
- **Tables** - Not converted (LinkedIn doesn't support tables)
- **Blockquotes** - Converted to plain text

For these features, consider whether the content makes sense on LinkedIn or if the post should be Jekyll-only.
