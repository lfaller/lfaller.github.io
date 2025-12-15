---
layout: post
author: lina
title:  "Software Doesn't Age Like Wine: Why Your Data Tools Need Maintenance"
date:   2025-12-15 08:00:00 -0500
categories: data-engineering
summary: Wetlab scientists expect software to work like a microscope—implement once, use for decades. But software lives in a constantly shifting ecosystem that requires ongoing maintenance, especially in fast-moving fields like computational biology.
---

![Software maintenance lifecycle comparison](/assets/images/posts/2025-12-15-software-maintenance-biotech.png)

**Software Doesn't Age Like Wine: Why Your Data Tools Need Maintenance (And What That Really Means)**

A scientist once told me: "We implemented that pipeline three years ago. Why doesn't it work anymore? We haven't changed anything."

That's when I realized there was a disconnect.

## The Mental Model Gap

When you buy a microscope, it works for years. Maybe decades. Same with a thermocycler, a centrifuge, or a spectrophotometer. You calibrate occasionally, replace parts when they break, but the core functionality stays stable.

So when wetlab scientists think about software, they unconsciously apply the same mental model: implement once, use indefinitely.

**But software lives in an ecosystem that's constantly shifting underneath it.**

## What Actually Happens Over Three Years

That pipeline you implemented? Here's what changed while you "didn't change anything":

- The cloud provider deprecated the API version you're using
- Security patches broke backward compatibility
- The reference genome you mapped against got updated
- Python 2.7 reached end-of-life 🐍 🪦
- Your data volume grew 10x and the original architecture can't scale
- The vendor whose tool you depend on got acquired and shut down their service
- File format specifications evolved
- Your regulatory requirements changed

**None of these are your fault. But all of them affect your tools.**

## Why Science Moves Especially Fast

Wetlab equipment is built on physics and chemistry - fundamental principles that don't change. A centrifuge in 2025 works on the same principle as one from 1985.

But computational biology is built on:

- Evolving file formats
- Constantly updating databases
- Dependencies on third-party services
- Security standards that must adapt to new threats
- Scientific understanding that improves the methods themselves

**The field is learning and changing faster than your software can stay static.**

## What Maintenance Actually Means

It's not about the code being "broken." It's about the world around it changing.

Think of it like maintaining a vivarium for a model organism. The organism didn't change, but you still need to:

- Monitor conditions daily
- Replace consumables
- Adjust protocols as suppliers change
- Update to better practices as the field learns
- Respond when something in the supply chain shifts

**Software maintenance is similar: keeping the ecosystem healthy so your tools continue to function.**

## The Real Cost of "Set and Forget"

When organizations treat software as equipment instead of living systems, they end up with:

- Emergency fixes when something critical breaks at the worst moment
- Data scientists spending 50% of their time on "keep the lights on" work
- Projects that take 3x longer because infrastructure is crumbling
- Institutional amnesia as people leave and no one knows how things work
- "We can't upgrade because everything will break" paralysis

**The cheapest maintenance is the kind you plan for.**

## What This Means for Biotech

If you're a Series A/B company, you're about to feel this acutely. That scrappy pipeline your first computational hire built? It probably needs thoughtful maintenance planning now that you've scaled.

Options:

- Budget for ongoing maintenance (15-20% of development time)
- Build with maintenance in mind from the start
- Accept that "temporary" solutions need replacement timelines
- Document so future maintainers aren't starting from scratch

**The goal isn't perfect software. It's sustainable software.**

## The Bridge We Need to Build

This isn't about wetlab scientists being naive or computational folks being demanding. It's about having different mental models shaped by different domains.

The solution? Better translation:

- Computational folks: explain maintenance in terms scientists already understand (calibration, consumables, ecosystem health)
- Scientists: budget time and resources for maintenance like you budget for reagents
- Leadership: recognize that sustainable infrastructure requires ongoing investment

**Software doesn't age like wine. It ages like a garden: without tending, it becomes overgrown.**

What patterns have you seen around software maintenance expectations? How do you help teams understand this dynamic?

<!-- #DataEngineering #Bioinformatics #TechnicalDebt #Biotech #DataScience -->
