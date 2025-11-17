---
layout: post
author: lina
title:  "Write the Test First (Even for Your Science)"
date:   2025-11-17 08:00:00 -0500
categories: software-engineering
---

![Test-driven development to the rescue.](/assets/images/posts/2025-11-17-write-the-test-first-even-for-your-science.png)

**Write the Test First (Even for Your Science)**

"I spent three days debugging. Turned out I was normalizing AFTER filtering instead of before. Results looked plausible for weeks."

We've all been there.

Here's what software engineers figured out decades ago with Test-Driven Development (TDD): **Ask "How will I know if this is correct?" BEFORE you start coding.**

## The Scientific Version

Before you write that filtering script or ML model:

- Create a toy dataset where you know the answer (3 samples, obvious differences)
- Define what "correct" looks like
- Run your code
- If it fails on 3 samples, you caught your bug early
- If it passes, scale up with confidence

## Why This Matters

**Traditional:** Write custom script → Run on real data → Get plausible results → Find bug 6 months later

**TDD:** Create toy example → Build simplest version → Catch bugs at 3 samples, not 300

## Real Example

Building a sample quality filtering script, I created synthetic data first: 10 samples where 3 should clearly fail, 7 should clearly pass.

Found my threshold logic was backwards immediately 🐛 - when debugging meant 10 samples, not 10,000.

By the time I ran production data, I had confidence. Not hope. 🎯

## Start Tomorrow

Next time you write custom code:

- Make one toy dataset first
- Looking for upregulated genes? Make 3 genes go UP
- Filtering samples by quality? Make 2 pass, 1 fail
- Does your code do what you expect?

Yes = Trust it on real data

No = You just saved yourself from bad science

**The best time to catch bugs is when your dataset is small enough to debug by hand.**

What's your "found the bug too late" horror story?

<!-- #SoftwareEngineering #DataScience #Bioinformatics #ResearchMethods #QualityControl -->