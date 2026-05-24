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

Streams is a centralized {{kib}} feature that uses AI to turn raw, unstructured log data into actionable insights.

Streams brings AI-assisted parsing, intelligent logs organization, and proactive event detection into a simple, intuitive workflow, so you can focus on solving problems, not wrangling pipelines.

SREs are drowning in alerts and brittle pipelines because the "why" behind most incidents is buried in chaotic, context-rich logs. Streams turns that chaos into clarity in minutes, giving you the answers you need to make logs your first stop for investigations.

From raw logs to real answers
From ingest to investigation, Streams simplifies and automates the work of building custom pipelines and manually extracting fields, giving you clean, structured, high-fidelity data and helping you find the needle in the haystack.

Log management made easy
Forget grepping through petabytes of logs. Streams detects patterns humans can't see, parsing, partitioning, and structuring logs, and surfacing significant events with AI.


Unlike traditional observability solutions that treat logs as secondary to metrics and traces, Streams makes logs a primary signal for both detection and investigation, helping you get to resolution faster. AI-driven workflows make logs usable and actionable, highlighting the "why" that's missing from traditional observability tools so SREs can resolve incidents faster, without having to spend weeks on data engineering and building complex pipelines.

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

