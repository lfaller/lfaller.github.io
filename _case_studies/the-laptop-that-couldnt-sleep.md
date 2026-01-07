---
layout: case-study
title: "The Laptop That Couldn't Sleep: Scaling Plasmid Build QC"
client_type: "Series B Synthetic Biology Company"
timeline: "8 weeks (side project; ~4 weeks if dedicated)"
technologies: ["Python", "AWS Batch", "Docker", "BLAST", "GitHub", "Internal UI framework"]
impact_metric: "Overnight runs → 30-40 seconds per sample"
impact_metrics:
  - "Overnight laptop runs → 30-40 seconds per sample"
  - "1 sample at a time → 90+ samples in parallel"
  - "Single person dependency → self-service for entire team"
problem_statement: "Plasmid QC workflow running on a single scientist's MacBook overnight, creating bottlenecks and single-person dependency"
date: 2026-01-07
featured: false
description: "How I transformed a bottlenecked genome QC process from an overnight laptop run into a scalable, self-service system handling 90+ samples in parallel on AWS Batch."
---

## Case Study: The Laptop That Couldn't Sleep

### The Problem That Ran Overnight

The company engineered plasmids at scale - inserting genes into E. coli and other microbes to produce valuable proteins. High-throughput meant hundreds of builds, and biology being biology, not all of them worked.

When a build failed - no gene expression, no protein production - scientists needed to troubleshoot. The process: sequence the organism, assemble the reads into a genome, call genes, then BLAST to check if what you put in actually showed up.

One scientist on the Genome Engineering team had built a workaround. He was a Research Associate with coding chops, and he'd cobbled together a Jupyter notebook and some bash scripts that could run the analysis.

The catch? It ran on his MacBook. For hours. He'd installed an app called "Caffeine" to keep his laptop from sleeping, start the analysis at the end of the day, and let it churn overnight. A handful of samples would be ready by morning - if nothing crashed.

### The Hidden Costs

**The single point of failure was a person.** He was the only one who could run the QC workflow. When he was on vacation, sick, or busy with other priorities, troubleshooting stalled. In a high-throughput environment, that meant cascading delays.

**The knowledge lived in one place.** The workflow existed as scripts on his laptop. No version control. No documentation beyond what was in his head.

**Others couldn't help.** Another scientist on the team wanted to run the analysis himself. But the Jupyter notebook was fragile, the bash scripts were finicky, and debugging required computational skills he was still developing. He had to wait.

**Then the original developer left the company.** Halfway through my project, he moved on to a new role. The process became virtually unusable.

### Building the Solution (Together)

I partnered with another scientist on the Genome Engineering team who became my primary stakeholder. He committed to regular testing and iteration, which gave us good development momentum even though this was a side project squeezed between other priorities.

The technical approach was straightforward:

- **Automated the workflow in Python** and deployed it on AWS Batch - our existing compute infrastructure that could scale virtually infinitely
- **Built a self-service UI** so scientists could submit jobs without touching the command line
- **Results uploaded automatically to LIMS** - no more emailing files around, and everything backed up centrally
- **Code tracked in GitHub** - version control, code reviews from the software team, and documentation

The key insight: this tool slotted neatly into our existing self-service catalog. Scientists already knew how to use that interface. No training required - just a new option in a familiar menu.

**Technical Stack:** Python, AWS Batch, Docker, BLAST, GitHub

### Workflow Transformation Visualization

{% include case-studies/laptop-qc-flow.html %}

### Workflow Transformation

#### BEFORE: The Overnight Laptop

1. Scientist starts Jupyter notebook at end of day
2. "Caffeine" app keeps MacBook awake
3. Analysis runs overnight (hours for a handful of samples)
4. Manual intervention required if anything crashes
5. Results emailed to whoever needed them
6. ⚠️ If he's unavailable → process stops

#### AFTER: Self-Service at Scale

1. Scientist opens internal UI
2. Submits samples (up to 90+ in parallel)
3. AWS Batch processes in ~30-40 seconds per sample
4. Results automatically uploaded to LIMS with visualizations
5. ✓ Anyone can run it, anytime

### Why This One Worked

Not every project goes smoothly. This one did.

**The pain was acute and obvious.** Everyone on the Genome Engineering team knew the QC process was a bottleneck. When the original developer left, it became urgent. There was no resistance to change because the status quo had become untenable.

**The infrastructure already existed.** AWS Batch was already running other workflows. The self-service UI framework was already built. I wasn't inventing new systems - I was plugging into proven ones.

**The stakeholder was invested.** My partner on the science side didn't just want this to work - he needed it to work. He tested every iteration, gave fast feedback, and championed adoption with his team.

**The scope was contained.** This was a well-defined problem: take an existing workflow, make it robust, make it scalable, make it self-service. No ambiguity about what "done" looked like.

### The Impact

**Speed:** Overnight runs → 30-40 seconds per sample

**Scale:** Sequential processing on one laptop → 90+ samples in parallel on AWS Batch

**Independence:** One person who could run QC → entire team self-serving

**Resilience:** When the original developer left, the team didn't skip a beat. The institutional knowledge was now in the system, not in someone's head.

**Qualitative changes:**

- Scientists could troubleshoot failed builds immediately instead of waiting
- Results centralized in LIMS instead of scattered across email threads
- Code reviewed, tested, and documented - maintainable by anyone on the software team

### What I Learned

**1. Side projects can have outsized impact.** This wasn't my main focus - it was squeezed into gaps between other work. But solving a painful bottleneck, even part-time, created real value for the team.

**2. Build on what exists.** The fastest path to adoption was plugging into infrastructure scientists already trusted. A new UI would have required training and behavior change. A new menu item in a familiar tool required nothing.

**3. The bus factor is real.** "What happens if this person leaves?" isn't a hypothetical. The original developer leaving mid-project proved the point: knowledge that lives in one person's head is organizational risk.

**4. Smooth adoption is possible when pain is obvious.** Not every change requires change management. When people are desperate for a solution and you hand them one that works, they'll use it.

**5. Stakeholder commitment matters more than stakeholder seniority.** My stakeholder wasn't a manager or a decision-maker. But his commitment to testing and iterating made the project successful.

### Future Directions

- **Long-read sequencing support:** Oxford Nanopore reads are long enough to capture an entire plasmid (~10kb) without assembly. This could simplify the pipeline further, though error rates require different handling.
- **Intelligent failure summarization:** Currently scientists review every visualization. Pattern recognition could flag the worst failures automatically.
- **Circular plasmid visualization:** The current output is linear; circular visualization would better match the biology.
