---
layout: post
author: lina
title:  "I Fixed The Same Bug Three Times (No One Noticed)"
date:   2025-11-20 08:00:00 -0500
categories: biotech
---

![The Groundhog Day Cycle.](/assets/images/posts/2025-11-20-i-fixed-the-same-bug-three-times.png)

**I Fixed The Same Bug Three Times (No One Noticed)**

The third time the data pipeline failed the exact same way, I realized: we have institutional amnesia.

## The Pattern

Month 1: The pipeline breaks because a scientist uploaded a file with inconsistent sample IDs. I spend 4 hours debugging. I fix it. I document the issue in Confluence.

No one reads the documentation.

Month 4: Different scientist, same problem. Different file, same inconsistent sample IDs. Another 4 hours debugging.

I update the documentation. I send a Slack reminder about file naming conventions.

Month 7: New hire. Same problem. Same 4 hours.

This time I realize: the people celebrating the "quick fix" weren't here for failures one and two. To them, I'm showing initiative by solving this so fast.

To me, I'm stuck in Groundhog Day.

## Why This Happens

**Institutional amnesia has root causes:**

Turnover erases memory. In small biotech, a 6-month tenure makes you a veteran. The people who lived through the first failure are gone. The people fixing it now think they're solving a novel problem.

Documentation doesn't survive in the wild. I wrote it down. I put it in Confluence, in the README, in Slack. But if no one reads documentation before they act, it might as well not exist.

Prevention is invisible. No one sees the failures that didn't happen. The alerts I built that catch bad files before they enter the pipeline? Silent successes. The validation I added that prevents the bug? No one knows it's working.

Firefighting is visible. When the pipeline breaks and someone stays late to fix it, that gets noticed. That gets Slack reactions. That gets mentioned in standups as "great ownership."

The incentive structure is backwards.

## The Cost

This isn't just frustrating—it's expensive:

**Time compounds:** 4 hours times 3 incidents is 12 hours spent on the same problem. That's a day and a half of engineering time solving something that should have been fixed once.

**Trust erodes:** Scientists start to think the infrastructure is fragile because "it keeps breaking." They don't know it's the same break. They just know they can't rely on it.

**Burnout accelerates:** There's a special kind of exhaustion that comes from solving the same problem repeatedly while people treat it as fresh heroics each time.

**Technical debt compounds:** Each time you fix it reactively instead of preventing it systematically, you're making a choice. The quick manual fix is faster than building validation, adding tests, creating clear error messages. But you pay interest on that choice every time it breaks again.

## The Truth About Prevention

Here's what I've learned about prevention work in small biotech:

It's invisible until something doesn't break. Then people assume nothing was ever going to break.

It requires institutional memory that most startups don't have. When your entire team turns over in 18 months, the context for why certain safeguards exist disappears.

It's harder to justify than firefighting. "I want to spend a week preventing a problem that might happen" is a tough sell when the CEO is changing priorities every week and everyone is underwater.

It's lonely work. You're often the only person who remembers the pattern. You're the one saying "we've seen this before" to people who weren't there.

## What I Do Now

I'm not going to pretend I solved this. But here's what I try:

**I write post-mortems even for "small" incidents.** Not to assign blame—to create a searchable record. When the same failure happens, I can link to the previous post-mortem and show the pattern.

**I build prevention into the urgent fix.** When I'm firefighting, I spend an extra 30 minutes adding validation that catches this class of problem. I can't always get a week to build comprehensive safeguards, but I can get 30 minutes while the pain is fresh.

**I make prevention visible through metrics.** "Prevented 47 bad files from entering the pipeline this month" is more visible than "pipeline ran smoothly." Count what didn't go wrong.

**I recognize when the organization isn't ready.** Sometimes the company culture just doesn't value this work yet. That's frustrating but real. You can't force institutional memory on an organization that's optimizing for speed over stability.

## The Unglamorous Reality

Prevention is infrastructure work.

It's boring. It's invisible when it works. It doesn't generate good standup updates.

But it's the difference between a team that's constantly firefighting and a team that has space to build new things.

The irony? The better you are at prevention, the less anyone knows you're doing it.

There's no glory in the disasters that never happen.

**Have you fixed the same problem multiple times while people treated it as a fresh issue? How do you make prevention work visible in your organization?**

<!-- #Biotech #DataEngineering #Bioinformatics #TechnicalDebt #SoftwareEngineering -->