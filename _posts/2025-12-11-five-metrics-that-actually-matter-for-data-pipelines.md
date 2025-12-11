---
layout: post
author: lina
title:  "The Only Five Metrics That Actually Matter for Data Pipelines"
date:   2025-12-11 08:00:00 -0500
categories: data-engineering
summary: "Most dashboards have 50 metrics. You look at 5. After building monitoring systems at four biotech companies, I learned that these five metrics actually matter:

1. **Data Freshness** - When was this data last updated?
2. **Row Count Delta** - Did we get the expected amount of data?
3. **Critical Column Null Rate** - Are we missing essential data?
4. **Schema Drift Detection** - Did someone change the upstream format?
5. **End-to-End Latency** - How long until scientists can use it?

These catch 80% of problems. Everything else is noise. Read the full breakdown on the blog."
---

![Simple dashboard, with metrics that matter](/assets/images/posts/2025-12-11-five-metrics-that-actually-matter-for-data-pipelines.png)

**The Only Five Metrics That Actually Matter for Data Pipelines**

You've got a dashboard with 47 different pipeline metrics. Nobody looks at 46 of them.

I've built monitoring systems at four biotech companies. Here's what I learned: **most metrics don't matter until something breaks**.

## The Metric Graveyard

Metrics that seemed important but weren't:

- Average processing time (unless it suddenly spikes)
- Memory utilization (unless you're hitting limits)
- Number of files processed (unless you expect a specific count)
- CPU percentage (cool graph, zero insight)

These metrics exist because they're easy to collect, not because they're useful.

## The Five Metrics That Actually Matter

### 1. Data Freshness

**"When was this data last updated?"**

This is the metric scientists care about most. If your Monday morning report shows Friday's data, they notice.

**How to measure**: Timestamp of last successful update compared to expected schedule.

**Alert threshold**: Data more than 2x expected interval old.

### 2. Row Count Delta

**"Did we get the expected amount of data?"**

Sudden drops or spikes indicate upstream problems. A 90% drop in daily samples? Something broke.

**How to measure**: Compare today's row count to 7-day moving average.

**Alert threshold**: Outside 2 standard deviations of recent average.

### 3. Critical Column Null Rate

**"Are we missing data we absolutely need?"**

Not all columns matter equally. Sample ID can't be null. Optional metadata can be.

**How to measure**: Null percentage for each critical column.

**Alert threshold**: Any nulls in critical columns, or >20% increase in optional columns.

### 4. Schema Drift Detection

**"Did someone change the upstream data format?"**

New columns appear, data types change, field names get renamed. Your pipeline needs to know before it breaks.

**How to measure**: Hash of column names and types compared to last run.

**Alert threshold**: Any schema change without documented migration.

### 5. End-to-End Latency

**"How long from data generation to scientist access?"**

Not the same as processing time. This measures the user experience: how long until they can actually use the data.

**How to measure**: Timestamp when data enters the system to timestamp when it's queryable.

**Alert threshold**: Exceeds SLA by 50%.

## What to Do With These Metrics

### Daily Checks

Look at data freshness and row counts every morning. These catch 80% of problems.

### Weekly Reviews

Check null rates and schema drift during weekly team sync. These indicate data quality trends.

### Monthly Analysis

Review end-to-end latency trends. This shows if your pipeline is scaling with data growth.

## The Real Example: Catching a Silent Failure

At one company, our monitoring showed:

- Processing time: Normal ✓
- Error logs: Clean ✓
- Row count: Normal ✓
- **Null rate in "assay_result" column: Jumped from 2% to 89%**

The pipeline "worked." But the data was useless.

Turned out an upstream system changed their API response format. Our ETL still parsed it, but extracted nulls instead of values.

**Without the null rate metric, this would have gone unnoticed for weeks**.

## Start Simple

If you're building monitoring from scratch:

**Week 1**: Just add data freshness  
**Week 2**: Add row count tracking  
**Week 3**: Add null rate for top 5 critical columns

That's 80% of the value with 20% of the complexity.

## The Monitoring Principle

**Good metrics answer the question: "Can scientists trust this data right now?"**

Everything else is noise.

<!-- #DataEngineering #Monitoring #DataQuality #Observability -->
