---
layout: post
title:  "The Post-Mortem No One Wants to Do (But Everyone Should)"
date:   2025-08-21 8:00:00 -0500
categories: software-engineering
---

![Continuous Learning Cycle.](/assets/images/posts/2025-08-21-the-post-mortem-no-one-wants-to-do.png)

Something breaks. Data pipeline fails. Analysis crashes. Dashboard goes down.

Your first instinct? Fix it fast and move on. Nobody wants to dwell on what went wrong.

But here's what I've learned: the 30 minutes you spend on a post-mortem can save you 30 hours of future firefighting.

THE NATURAL RESPONSE: When things break, we're frustrated. We want to forget it happened and get back to "real work." The failure feels like a setback, so we rush to put it behind us.

I get it. Post-mortems feel like dwelling on negative things when you could be building new features.

WHAT POST-MORTEMS ACTUALLY DO:

➡️ Identify systemic issues (not just the immediate bug)

➡️ Reveal process gaps you didn't know existed

➡️ Prevent the same failure from happening again

➡️ Make your systems more robust by addressing root causes

➡️ Turn failures into learning opportunities for the whole team

A REAL EXAMPLE: Our visualization dashboard went down because a scientist uploaded a malformed CSV. Easy fix: validate the file format.

Post-mortem revealed the real issue: we had no systematic way to communicate data formatting requirements to scientists. The CSV was just the symptom.

Solution: Built an automated data validation step with clear error messages that taught scientists the expected format.

Result: Turned a one-off failure into a system improvement that prevented dozens of future issues.

THE PROCESS THAT WORKS:

1️⃣ Designate someone to lead the investigation (don't let it fall through the cracks)

2️⃣ Focus on systems, not blame (what failed, not who failed)

3️⃣ Include relevant stakeholders (the people who were affected need to understand what happened)

4️⃣ Document actionable improvements (not just "be more careful next time")

THE MANAGEMENT CHALLENGE: Here's the tricky part: post-mortems require time that doesn't immediately show ROI.

If leadership just wants to "move fast and fix things," it's hard to justify spending time on "what went wrong" instead of "what's next."

But here's the business case: every failure that repeats is time stolen from innovation. Post-mortems are an investment in not having the same conversation again in three months.

THE BRIDGE BUILDER PERSPECTIVE: Post-mortems aren't just technical exercises—they're communication opportunities. They help teams understand how their work interconnects and where the fragile points are.

When you include stakeholders in post-mortems, you're not just fixing systems—you're building shared understanding of how your infrastructure works and why certain practices matter.

Have you found effective ways to make time for post-mortems? How do you convince leadership that this "backward-looking" work is actually forward-thinking?