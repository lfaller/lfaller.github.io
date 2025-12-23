---
layout: case-study
title: "AI Readiness Starts with Knowing What You Have"
client_type: "Large Pharma Company"
timeline: "6 weeks"
technologies: ["Python", "Streamlit", "SQLite", "Docker", "YAML"]
impact_metric: "90% reduction in data discovery time (30-60 min → 2-5 min)"
impact_metrics:
  - "90% reduction in data discovery time (30-60 min → 2-5 min)"
  - "~15,000 samples samples across nearly 30 datasets cataloged"
  - "6 modalities searchable for the first time"
  - "New datasets onboarded in under 5 minutes"
problem_statement: "Multi-modal discovery data scattered across teams with no catalog, inconsistent metadata, and knowledge locked in individuals"
date: 2025-01-06
featured: true
description: "How I helped a large pharma company build the foundation for AI readiness by cataloging scattered multi-modal data, normalizing metadata, and transforming institutional knowledge from personal asset to organizational asset."
---

## Case Study: AI Readiness Starts with Knowing What You Have

### The Problem Everyone Was Working Around

The company wanted to become "AI Ready" for multi-modal discovery. They had rich datasets across six modalities: scRNAseq, CyTOF, Olink, bulk RNAseq, Luminex, and scATAC-seq. The kind of data that makes ML researchers excited.

But there was a more fundamental problem: nobody knew what data existed, who owned it, or how it connected.

Finding a dataset meant playing detective. For every modality × project combination, I had to track down two people: one who knew the modality, one who knew the disease area. Manually poking around file systems. Sending messages on Teams. Waiting for email replies. 30-60 minutes per search - if you were lucky.

And when people left the company? Their knowledge left with them.

### The Hidden Costs

**The detective tax**: Every person who needed data paid the same discovery cost. There was no institutional memory - just individual knowledge scattered across the organization.

**Inconsistent metadata blocking analysis**: Even when data was found, the same concept appeared a dozen different ways. "Healthy," "healthy," "healthy control," "Healthy Control," "HEALTHY," "H." Same with sex/gender: "F," "M," "Female," "Male," "female," "male." You can't train a model on data where the same label has six different spellings.

**No visibility into completeness**: Nobody could easily answer "what samples do we have for Project X?" or "which datasets are missing clinical metadata?" These questions required manual investigation every time.

**AI ambitions stalled at the starting line**: The company wanted to do sophisticated multi-modal discovery, but they couldn't get past the foundation: knowing what they had.

### Building the Solution (Together)

I partnered closely with a wetlab scientist who knew the data landscape. Every conversation with a domain expert taught me something new - they were busy, especially during the a busy season, but getting on their calendars was essential.

Together, we designed a pragmatic system:

- **Standardized file structure** that encodes metadata in the path itself
- **YAML configuration** for each dataset with core metadata fields (sample ID, processing date)
- **CSV-based ingestion** with normalization rules for inconsistent values
- **SQLite database** with JSON arrays for flexible technical/clinical metadata
- **Streamlit app** for search and export, deployed in Docker

Why SQLite? It's lightweight and perfect for a proof of concept. Why JSON arrays for metadata? The organization didn't have enough structure yet to define rigid schemas - flexibility was more valuable than query speed at this stage.

**Technical Stack**: Python, Streamlit, SQLite, Docker, YAML

### Workflow Transformation Visualization

{% include case-studies/data-catalog-flow.html %}

### The Reality Check

**The data wasn't in easy-to-access places.** For each modality, I had to talk to a different wetlab person to get the data, metadata, and mapping information. Six weeks was enough to build the system and catalog what we could access - but we could have gone further if a standardized file structure had already been in place.

**People were tired.** They'd heard about efforts like these before. Everyone had a full plate, and me coming to ask for information was "yet another thing." This wasn't resistance exactly - just the weight of competing priorities and past initiatives that hadn't stuck.

**SQLite got slow towards the end.** With ~15,000 samples samples and 185 metadata fields, query performance started to degrade. Good enough for the MVP, but a clear signal that the next phase needs a different backend.

### The Impact

**Time Savings**: 30-60 minutes per data search → 2-5 minutes (90%+ reduction)

**What's Now Possible**:
- **Multi-modal search**: For the first time, someone can search across all modalities by sample ID, project, or disease area
- **Metadata completeness at a glance**: Instantly see which datasets are missing key fields
- **Normalized values**: "Healthy" is now "Healthy" everywhere - no more six spellings of the same concept
- **Institutional memory**: Knowledge that used to live in people's heads is now queryable by anyone

**By the Numbers**:
- 6 modalities supported
- Nearly 30 datasets cataloged
- ~15,000 samples samples indexed
- 185 metadata fields normalized
- 80% of samples linked to source files
- New datasets onboarded in under 5 minutes

### What Comes Next

This was an MVP - a foundation to build on. The roadmap includes:

- **Different database backend**: SQLite did its job, but scale demands something faster
- **Self-service onboarding**: A no-code form so wetlab scientists can add datasets without running scripts
- **Richer multi-modal viewer**: Beyond "data exists" to actually previewing and comparing across modalities
- **Standardized analysis pipelines**: Incorporate minimally processed outputs (count files, etc.)
- **Experimental design capture**: Currently this only lives in PowerPoint files

### What I Learned

**1. AI readiness is a data management problem first**: Before you can train models, you need to know what data exists, where it lives, and what it means. The unsexy work of cataloging and normalization isn't a detour - it's the path.

**2. Bridge-building is the real work**: Every modality required a different conversation with a different expert. The technical system was straightforward; getting the information to populate it required patience and relationship-building.

**3. Pragmatic beats perfect**: SQLite and JSON arrays aren't elegant at scale, but they let us prove value in 6 weeks. Now there's momentum and evidence to justify a more robust solution.

**4. Personal assets become institutional assets**: The most important transformation wasn't technical - it was converting knowledge that could "walk out the door" into something the organization owns permanently.

**5. Past failures create skepticism**: When people have seen similar initiatives fizzle, they're hesitant to invest energy in the next one. Quick wins and visible progress are essential to rebuilding trust.