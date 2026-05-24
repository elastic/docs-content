---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Streams

Stop spending weeks on pipeline setup and data engineering before you can start investigating. Streams handles the heavy lifting — automatically parsing, structuring, and organizing your log data so you can query it immediately, without writing Grok expressions or maintaining custom pipelines.

When an incident hits, Streams gets you to answers faster. AI-powered detection continuously scans your logs for critical signals and surfaces what matters, so instead of manually sifting through thousands of log lines, you have a prioritized list of issues to act on — turning logs from a last resort into your most valuable first signal.

:::{image} ../../images/streams-overview.png
:screenshot:
:alt: Streams overview
:width: 900px
:::

**Use Streams to...**

Log data holds the answers to most production incidents, but raw logs are noisy, expensive, and
hard to query. Streams addresses each of these challenges:

**Organize logs automatically**
:   Streams uses AI to partition your log data by source and component, without manual regex rules or
pipeline configuration. As new log formats arrive, Streams continues to learn and extend its
partitioning automatically.

**Get meaning from logs**
:   The AI-powered processing pipeline detects log formats (including custom ones like Apache Spark)
and generates parsing rules that extract structured fields from unstructured text. You get clean,
queryable data without writing a single GROK expression.

**Solve incidents in minutes, not hours**
:   Significant Events detection continuously scans your streams for critical signals: out-of-memory
errors, crash loops, certificate expirations, and anomalies. Instead of manually scanning
thousands of log lines, you get a prioritized list of what matters.

**Reduce time spent on managing pipelines**
:   Streams uses AI to simplify parsing, enrichment, partitioning, and schema updates, removing the need to maintain complex Grok patterns or custom pipelines. SREs can begin investigating issues within minutes, rather than spending weeks on pipeline setup and data engineering.

**Control storage costs**
:   By surfacing the most critical logs and automatically structuring data for efficient storage, Streams allows SREs to retain high-value data without discarding important information, reducing overall storage costs.

