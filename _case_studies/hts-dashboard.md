---
layout: case-study
title: "From 8 Hours to 45 Minutes: Democratizing High-Throughput Screening Data"
client_type: "Series B RNA Therapeutics Company"
timeline: "6 weeks from discovery to deployment"
technologies: ["Python", "Streamlit", "AWS (EC2, S3)", "PostgreSQL", "PositConnect"]
impact_metric: "94% time reduction (8-12 hrs → 45 min per week)"
impact_metrics:
  - "94% time reduction in weekly reporting (8-12 hours → 45 minutes)"
  - "2,000 hours saved annually across team"
  - "ROI achieved in under 2 months"
  - "Enabled real-time decision making in meetings"
problem_statement: "5-person HTS team spending 8-12 hours/week on manual data reporting (CSV → Prism → PowerPoint)"
date: 2024-11-24
featured: true
description: "How I transformed a biotech company's high-throughput screening workflow from a 12-hour manual process into a 45-minute self-service dashboard, freeing up 2,000 hours annually and enabling real-time scientific collaboration."
---

## Case Study: From 8 Hours to 45 Minutes - Democratizing High-Throughput Screening Data

### The Problem Nobody Knew They Could Solve

When I joined the company, I discovered the HTS team's workflow through casual conversations - the kind you have over coffee or passing in the hallway. Five scientists were spending 8-12 hours per week on what should have been straightforward: reporting their experimental results.

Their process was brutally manual:
1. Download CSV files from the database
2. Copy data into Prism for visualization 
3. Copy those visualizations into PowerPoint for presentations
4. Repeat for each experiment (managing data from up to 12 plates with 384 wells each)

The kicker? They'd accepted this as "just how it is." They didn't think the company cared about fixing it. They didn't realize there was another way.

### The Hidden Costs

As I dug deeper, I realized the time drain wasn't even the worst part:

**Error-prone processes**: Manual copy-pasting across 4,608 data points per experiment meant mistakes were inevitable. One misplaced decimal could derail weeks of work.

**No institutional memory**: Scientists couldn't easily compare results across experiments. Some kept personal Excel spreadsheets, but tracking patterns across dozens of plates was nearly impossible.

**Computational bottleneck**: When scientists got stuck, they'd have to request help from the computational team, creating dependencies and delays.

### Building the Solution (Together)

I chose Streamlit for rapid iteration - we could build something, show it to users within days, get feedback, and refine. The goal wasn't perfection; it was usefulness.

We worked iteratively with the HTS team, building features based on what they actually needed rather than what I thought they should want. The dashboard pulled data directly from our database, generated visualizations automatically, and allowed scientists to filter, compare, and download results in minutes.

**Technical Stack**: Python, Streamlit, AWS (EC2, S3), PostgreSQL, PositConnect

#### Workflow Transformation Visualization

{% include_relative ../assets/case-studies/hts-dashboard.html %}

### The Challenges Nobody Expected

**1. The Data Access Panic**

Once the dashboard went live and people across the company could suddenly see "all the data," leadership panicked. In their enthusiasm to approve the project, nobody had mapped out exactly how much data existed or who should access what.

The irony wasn't lost on me - we'd built a tool so effective that it revealed gaps in our data governance.

**Solution**: We implemented a quick password fix, then worked with IT to integrate the dashboard into our SSO framework. This let IT handle user management (which they preferred) and gave leadership the control they needed.

**2. The Territorial Culture**

Some wetlab scientists felt protective of "their" data. They'd generated it, so they felt they should control who saw it. This clashed with leadership's vision of data transparency but was a real cultural reality.

**Solution**: This required conversations, not code. We got everyone in a room to discuss data ownership, scientific collaboration, and company goals. It took time for some people to come around, and honestly, a few stayed resentful for a while. Change management is messy.

**3. The Misinterpretation Problem**

With easier access came a new risk: people viewing data without full context and drawing wrong conclusions, then communicating those misinterpretations downstream.

**Solution**: We added detailed titles, legends, and contextual information to every downloadable figure. We also created documentation explaining what each metric meant and when to consult the original experimenters.

### The Impact

**Time Savings**: 8-12 hours per week per scientist → 45 minutes
- 5 scientists × 8 hours/week × 50 weeks = 2,000 hours annually freed up
- ROI on development time achieved in under 2 months

**Qualitative Changes**:
- **Real-time decision making**: Scientists could pull up the dashboard in meetings and answer questions on the spot
- **Collaborative debugging**: More people could review data when experiments looked suspicious, speeding up troubleshooting
- **Reduced dependencies**: Scientists could self-serve instead of waiting for computational support
- **Pattern recognition**: Easy cross-experiment comparison revealed insights that were invisible in isolated spreadsheets

### What I Learned

**1. Listen to what people have accepted**: The most impactful improvements often address pain points people have stopped complaining about because they've resigned themselves to the status quo.

**2. Build fast, iterate faster**: Streamlit's rapid development cycle let us show value quickly, which built trust and momentum for addressing harder problems like data governance.

**3. Technical solutions reveal organizational issues**: Sometimes the reason a problem hasn't been solved isn't technical - it's cultural, political, or structural. Be ready to navigate those waters.

**4. Democratization has consequences**: Making data accessible is powerful, but it requires parallel work on governance, training, and culture. You can't just throw open the gates and walk away.

**5. Success creates new problems**: When tools work well, they get used in ways you didn't anticipate. Build with extensibility in mind.
