---
layout: post
author: lina
title:  "Design Docs for Bioinformatics"
date:   2025-07-24 12:00:00 -0500
categories: research
---

![Scope creep is real](/assets/images/posts/2025-07-24-design-docs-for-bioinformatics.png)

I learned about "Design Docs" from software engineers, and it completely changed how I approach bioinformatics projects.

The concept: sit down, think it through, write it up, gather feedback, iterate... BEFORE you touch the keyboard.

My favorite section? "Out of scope."

Because every bioinformatician knows this story: "Can you do a quick analysis?" turns into a three-month odyssey with no clear endpoint. The project balloons because nobody defined what we're NOT doing.

Here's why design docs could transform bioinformatics:

1️⃣ CRYSTALLIZE THE ACTUAL GOAL Instead of "analyze the RNA-seq data," you write: "Identify differentially expressed genes between treatment groups, focusing on immune pathways, to inform our next compound selection."

2️⃣ SURFACE DEPENDENCIES EARLY "This analysis depends on completed sample QC and assumes we're using the latest genome build." No more surprises halfway through.

3️⃣ CREATE SHARED UNDERSTANDING When the wetlab scientist, the PI, and you all agree on the written scope, everyone's expectations are aligned.

Yes, it feels slower at first. "Wait, you want feedback on my half-baked idea?!"

But here's what actually happens: your half-baked idea becomes almost-fully-baked before you spend weeks implementing it. You catch scope creep before it catches you.

The design doc becomes your north star when stakeholders inevitably ask, "While you're at it, could you also..." You can point to the doc and say, "That's out of scope for this analysis, but let's discuss it for the next one."

I wish they would teach us this in school. It would have saved me from so many "quick analyses" that turned into month-long rabbit holes.

Do you use any formal planning processes for your bioinformatics work? What keeps your analyses focused and scoped?
