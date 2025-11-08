# Scheduled LinkedIn Posting Guide

This guide explains how to schedule posts to publish automatically at 8am ET on specific dates.

## How It Works

The automated scheduling system:

1. **You write** a post with a future date in `_scheduled-posts/`
2. **GitHub Actions runs** daily at 8am ET
3. **Script checks** all posts in `_scheduled-posts/`
4. **Posts with dates ≤ today** are published to LinkedIn
5. **Published posts** are moved to `_posts/` for Jekyll to display

## Creating a Scheduled Post

### Step 1: Write Your Post

Create a markdown file in `_scheduled-posts/`:

```bash
_scheduled-posts/2025-11-15-my-future-post.md
```

### Step 2: Set the Date/Time

In your frontmatter, set the `date` field to when you want it published:

```yaml
---
layout: post
author: lina
title:  "My Scheduled Post"
date:   2025-11-15 08:00:00 -0500
categories: data-science
---

Your content here...
```

**Important:**
- Date format: `YYYY-MM-DD HH:MM:SS -0500`
- Time should be `08:00:00` (8am) for consistency
- Include `-0500` for Eastern Time
- Posts publish when current time ≥ scheduled time

### Step 3: Commit and Push

```bash
git add _scheduled-posts/2025-11-15-my-future-post.md
git commit -m "Schedule post for Nov 15"
git push
```

That's it! The post will automatically publish at 8am ET on the scheduled date.

## What Happens on Publish Day

At 8am ET every day, GitHub Actions:

1. ✅ Checks all posts in `_scheduled-posts/`
2. ✅ Identifies posts with `date ≤ current date/time`
3. ✅ Uploads images to LinkedIn
4. ✅ Posts to LinkedIn with formatting and hashtags
5. ✅ Moves the post file from `_scheduled-posts/` to `_posts/`
6. ✅ Commits the change back to GitHub
7. ✅ Jekyll rebuilds and deploys your site

**Result:** Your post appears on both LinkedIn and your website at 8am ET!

## Checking Scheduled Posts

To see what's scheduled:

```bash
ls -la _scheduled-posts/
```

Or view on GitHub:
```
https://github.com/YOUR_USERNAME/lfaller.github.io/tree/main/_scheduled-posts
```

## Manual Publishing

You can also manually trigger the scheduler:

1. Go to GitHub Actions tab
2. Select "Scheduled LinkedIn Posts" workflow
3. Click "Run workflow"
4. Click "Run workflow" button

This will immediately check and publish any posts that are due.

## Time Zone Notes

**All times are in Eastern Time (ET):**
- EST (Standard): UTC-5 (November - March)
- EDT (Daylight): UTC-4 (March - November)

The script automatically handles daylight saving time transitions.

**Scheduling at 8am ET:**
```yaml
date: 2025-11-15 08:00:00 -0500  # 8am ET (Standard Time)
```

## Examples

### Example 1: Schedule for Next Week

```yaml
---
layout: post
author: lina
title:  "Q4 Data Insights"
date:   2025-11-15 08:00:00 -0500
categories: data-science analytics
---

Here are the key trends we've observed...

<!-- #DataAnalytics #BusinessIntelligence -->
```

Save as: `_scheduled-posts/2025-11-15-q4-data-insights.md`

**Result:** Posts to LinkedIn on Nov 15 at 8am ET, then appears on website.

### Example 2: Schedule Multiple Posts

You can schedule as many posts as you want:

```bash
_scheduled-posts/
├── 2025-11-15-post-one.md
├── 2025-11-18-post-two.md
├── 2025-11-22-post-three.md
└── 2025-12-01-december-post.md
```

Each will publish on its scheduled date.

### Example 3: Post with Image

```yaml
---
layout: post
author: lina
title:  "Visualization Best Practices"
date:   2025-11-20 08:00:00 -0500
categories: data-visualization
---

Check out these **data visualization** tips:

![Chart Example](/assets/images/posts/2025-11-20-chart.png)

- Use clear labels
- Choose appropriate chart types
- Maintain consistency

<!-- #DataViz #Charts #Analytics -->
```

Image will be uploaded to LinkedIn when the post publishes!

## Editing Scheduled Posts

You can edit scheduled posts anytime before they publish:

1. Edit the file in `_scheduled-posts/`
2. Commit and push changes
3. Changes will be included when the post publishes

## Canceling a Scheduled Post

To cancel a scheduled post:

1. Delete the file from `_scheduled-posts/`
2. Commit and push

The post will never publish.

## Moving a Scheduled Post to Immediate

To publish a scheduled post immediately:

**Option A: Change the date**
```yaml
date: 2025-11-08 08:00:00 -0500  # Set to today or earlier
```
Push changes, then manually trigger the workflow.

**Option B: Publish manually**
```bash
# Move to _posts manually
mv _scheduled-posts/2025-11-15-my-post.md _posts/

# Publish to LinkedIn manually
cd scripts
source venv/bin/activate
python linkedin_post.py ../_posts/2025-11-15-my-post.md

# Commit
git add -A
git commit -m "Publish post immediately"
git push
```

## Troubleshooting

### Post didn't publish on schedule

**Check:**
1. Date format is correct: `YYYY-MM-DD HH:MM:SS -0500`
2. Date is today or earlier
3. GitHub Actions workflow completed successfully
4. LinkedIn credentials are set in GitHub Secrets

**View logs:**
1. Go to GitHub Actions tab
2. Click on the latest "Scheduled LinkedIn Posts" run
3. Review the output

### Post published but not on website

The post should have moved to `_posts/`. Check:
1. File was moved successfully (check GitHub commit)
2. Jekyll deployment completed
3. Clear browser cache

### Image didn't upload

Check:
1. Image path is correct in markdown
2. Image file exists in repository
3. Image is under 8MB
4. Check GitHub Actions logs for upload errors

## Best Practices

1. **Consistent timing**: Always use 8:00:00 for consistency
2. **Include timezone**: Always include `-0500` in dates
3. **Test first**: Try scheduling a post for tomorrow to test the system
4. **Plan ahead**: Schedule posts at least a day in advance
5. **Review before publishing**: Double-check content before the publish date
6. **Monitor Actions**: Occasionally review GitHub Actions logs

## Workflow Details

**Cron schedule:** `0 13 * * *` (13:00 UTC = 8am EST / 9am EDT)

**Note:** The workflow uses 13:00 UTC which equals 8am EST. During daylight saving time (EDT), this becomes 9am. If you need exact 8am year-round, you may need to adjust the cron schedule seasonally.

**Files involved:**
- `.github/workflows/scheduled-linkedin-post.yml` - GitHub Actions workflow
- `scripts/publish_scheduled.py` - Publishing script
- `_scheduled-posts/` - Directory for future-dated posts
- `_posts/` - Directory for published posts

## FAQ

**Q: Can I schedule posts for specific times other than 8am?**
A: Currently, the workflow runs once daily at 8am ET. Posts with times after 8am will publish the next day at 8am.

**Q: What happens if two posts have the same date?**
A: Both will publish on the same day at 8am. They'll appear in the order processed.

**Q: Can I schedule posts months in advance?**
A: Yes! Schedule as far ahead as you want.

**Q: Will old drafts in _scheduled-posts automatically publish?**
A: No. Only posts with `date ≤ current date/time` publish. Past dates publish immediately on the next run.

**Q: Does this work for posts without images?**
A: Yes! Image upload is optional.
