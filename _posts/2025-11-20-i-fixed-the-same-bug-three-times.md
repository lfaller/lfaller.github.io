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

Month 1: Pipeline breaks. I debug for 4 hours, document it, fix it. No one reads the docs.

Month 4: Different scientist, same problem. Another 4 hours debugging.

Month 7: New hire, same issue, same 4 hours.

The people celebrating the "quick fix" weren't here for failures one and two. To them, I'm showing initiative. To me, I'm stuck in Groundhog Day.

**Why This Happens:**

- Turnover erases memory. After 18 months, people who lived through the first failure are gone.
- Prevention is invisible. The validation I built that prevents the bug? No one knows it's working.
- Firefighting is visible. Quick fixes get noticed. Prevention work doesn't.

**The Cost:**

12 hours solving the same problem. Trust erodes—scientists think infrastructure is fragile. Burnout accelerates. Technical debt compounds.

**What Works:**

Write post-mortems for searchable records. Build prevention into urgent fixes—even just 30 minutes of validation. Make prevention visible through metrics: "Prevented 47 bad files this month" beats "pipeline ran smoothly."

**The Truth:**

Prevention is infrastructure work. It's boring, invisible when it works, and generates no standup updates. But it's the difference between teams constantly firefighting and teams that have space to build.

The better you are at prevention, the less anyone knows you're doing it. There's no glory in disasters that never happen.

Have you fixed the same problem repeatedly? How do you make prevention work visible?

<!-- #Biotech #DataEngineering #Bioinformatics #TechnicalDebt #SoftwareEngineering -->