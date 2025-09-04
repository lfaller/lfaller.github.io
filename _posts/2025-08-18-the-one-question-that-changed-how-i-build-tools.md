---
layout: post
author: lina
title:  "The One Question That Changed How I Build Tools"
date:   2025-08-18 8:00:00 -0500
categories: data-science
---

![One research question can lead to different tool outcomes.](/assets/images/posts/2025-08-18-the-one-question-that-changed-how-i-build-tools.png)

"Can you make a dashboard for our RNA-seq data?"

I used to jump straight into requirements gathering. What data? Which visualizations? How many samples?

Now I ask one question first: "What does success look like?"

THE SAME REQUEST, DIFFERENT SUCCESS CRITERIA:

Scenario: "We need an RNA-seq dashboard"

⭐ If you're the Lab Manager: Success = "I can quickly spot failed experiments before they waste downstream resources." → Build: QC-focused dashboard with clear pass/fail indicators

⭐ If you're the Principal Investigator: Success = "I can confidently present these results to the grant committee next week." → Build: Publication-ready visualizations with statistical annotations

⭐ If you're the Postdoc: Success = "I can explore the data myself without bothering the bioinformatics team every time I have a question." → Build: Interactive exploration tool with multiple filtering options

Same request. Three completely different tools.

WHY REQUIREMENTS AREN'T ENOUGH: Requirements tell you WHAT to build. Success criteria tell you WHY you're building it.

➡️ "Show differentially expressed genes" is a requirement.

➡️ "Help me identify the top 3 pathways to focus our next experiments on" is a success criterion.

The second one tells you that you need statistical significance, pathway enrichment, and probably some way to rank or prioritize results.

THE POWER OF STARTING WITH OUTCOMES: When you start with success criteria:

➡️ You build tools people actually use

➡️ You avoid feature creep (if it doesn't serve the success criteria, it's not essential)

➡️ You can make trade-offs confidently

➡️ You know when you're done

A REAL EXAMPLE: 

Scientist: "I need a way to visualize our compound screening data."

Me: "What does success look like?"

Scientist: "I want to walk into Monday's meeting and confidently say 'these 5 compounds are worth pursuing' and defend that decision."

Suddenly I'm not building a generic visualization tool. I'm building a decision-support system with confidence intervals, statistical significance testing, and clear ranking criteria.

THE BRIDGE BUILDER INSIGHT: Different stakeholders define success differently, even for identical requests. Your job isn't just to translate requirements -- it's to uncover and align success criteria.

Sometimes the real win is realizing that three different stakeholders need three different tools, not one "comprehensive" solution that satisfies nobody.

What's your experience with this? Do you find that starting with outcomes changes what you build?