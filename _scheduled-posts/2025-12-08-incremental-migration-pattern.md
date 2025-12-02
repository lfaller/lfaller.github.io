---
layout: post
author: lina
title:  "The Incremental Migration Pattern (Or: How to Rebuild the Plane While Flying It)"
date:   2025-12-08 08:00:00 -0500
categories: software-engineering
---

![This is where you place your routing layer.](/assets/images/posts/2025-12-08-incremental-migration-pattern.png)

**The Incremental Migration Pattern (Or: How to Rebuild the Plane While Flying It)**

Your data pipeline is a mess of Jupyter notebooks held together with cron jobs and hope.

You know you need to rebuild it. But you can't stop it - scientists depend on those weekly reports.

**This is the migration paradox that kills most refactoring efforts**.

## The All-or-Nothing Trap

Here's what doesn't work:

- "We'll rebuild everything in parallel and switch over when it's ready"
- Six months later, the new system is 80% done
- The old system has evolved
- The new system is already outdated
- Nobody wants to switch
- **The project dies**

I've seen this pattern destroy good engineering work at every company I've worked at.

## The Incremental Migration Pattern

Here's what actually works:

**Step 1**: Add a routing layer

Create a thin abstraction that decides which system handles each request. Start with everything going to the old system.

**Step 2**: Migrate one small piece

Pick the simplest, most stable component. Build the new version. Route just that piece to the new system.

**Step 3**: Run both in parallel

For a few weeks, run both old and new versions. Compare outputs. Build confidence.

**Step 4**: Cut over one component

Once you trust the new version, route all traffic there. **Celebrate the small win**.

**Step 5**: Repeat

Each cycle gets faster because you're learning and building confidence.

## Real Example: The NGS QC Pipeline

At one company, we migrated a genomic quality control pipeline:

- Week 1: Routing layer added (3 days of work)
- Week 2: FastQC step migrated (1 new component)
- Week 3: Validation in parallel
- Week 4: Cut over FastQC
- Week 6: Adapter trimming migrated
- Week 10: Entire pipeline running on new system

**Total migration**: 10 weeks while the old system kept running.

If we'd tried to rebuild everything at once? We'd still be working on it.

## The Key Insight

**You don't need to rebuild the whole plane. You need to replace one rivet at a time.**

The routing layer is your safety net. It lets you:

- Test in production without risk
- Roll back instantly if something breaks
- Maintain one system instead of two (eventually)
- Show progress every sprint

## When This Pattern Applies

Use incremental migration when:

- The old system can't be turned off
- The new system will take months to build
- Requirements are still evolving
- You need to show progress to leadership

Don't use it when:

- The old system is truly broken and needs emergency replacement
- The architecture is so different that no incremental path exists
- You have the luxury of parallel development time

## The Question Nobody Asks

"What's the smallest piece we could migrate first?"

That's your starting point.

<!-- #SoftwareEngineering #DataEngineering #Refactoring #TechnicalDebt -->
