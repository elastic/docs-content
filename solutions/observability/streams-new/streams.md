---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: Streams provides a centralized UI for extracting fields, setting retention, routing data, and managing Elasticsearch data streams.
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

# Streams-new

Streams allows you to automatically parse, structure, and organize your log data so you can query it immediately, without writing Grok expressions or maintaining custom pipelines.

When an incident hits, Streams gets you to answers faster. AI-powered detection continuously scans your logs for critical signals and surfaces what matters. Instead of manually scanning thousands of log lines, you get a prioritized list of what matters.

:::{image} ../../images/streams-overview.png
:screenshot:
:alt: Streams overview
:width: 900px
:::

:::{dropdown} Basic concepts
A Stream is defined by three intrinsic properties: where data comes from (sources), what happens to it in transit (pipeline), and where it ends up (destinations). These aren't separate systems — they're built into the stream itself.

**Sources**

:   Sources define how data enters a stream. Elastic supports two models:

    - **Push (OpenTelemetry, Syslog, _bulk, Splunk)**: external systems send data to Elastic endpoints. Built for high-volume, continuous telemetry with strong buffering and queuing guarantees.
    - **Pull (S3, Kafka, SaaS APIs)**: Elastic fetches data on a schedule. Ideal for audit logs, SaaS integrations, and historical ingestion.
The underlying mechanism — Fleet agent, Agentless, Cloud forwarder — is invisible to the user. Adding a source means data starts flowing immediately. Multiple sources can feed the same stream simultaneously, letting diverse telemetry types converge naturally.

**Pipelines**

:   A pipeline is not an external system — it's a property of the stream, expressed through Streamlang (with OTTL available for advanced cases). Pipelines handle filtering, enrichment, field extraction, and conditional routing. They're stateless by default, with stateful processing reserved for specialized cases like tail-based sampling.

**Destinations**

:   A destination is itself a stream, making the model inherently composable. Routing is many-to-many: one stream can fan out to multiple destinations, and one destination can receive from multiple upstream streams. Destinations are queryable via ESQL views. Unlike today's implicit default storage, the unified model makes every routing decision explicit and visible.
:::

:::{dropdown} Use Streams to...
**Organize logs automatically**
:   Streams uses AI to partition your log data by source and component, without manual regex rules or pipeline configuration. As new log formats arrive, Streams continues to learn and extend its partitioning automatically.

**Get meaning from logs**
:   The AI-powered processing pipeline detects log formats and generates parsing rules that extract structured fields from unstructured text. You get clean, queryable data without writing a single GROK expression.

**Solve incidents in minutes, not hours**
:   Significant Events detection continuously scans your streams for critical signals: out-of-memory errors, crash loops, certificate expirations, and anomalies. 

**Reduce time spent on managing pipelines**
:   Streams uses AI to simplify parsing, enrichment, partitioning, and schema updates. You can start investigating issues within minutes, rather than spending weeks on pipeline setup and data engineering.

**Control storage costs**
:   By surfacing the most critical logs and automatically structuring data for efficient storage, Streams allows you to retain high-value data without discarding important information, reducing overall storage costs.
:::

% ::::::{dropdown} Who Streams is for
%
% :::::{tab-set}
% ::::{tab-item} Novice user
% If you're new to log management or to Elastic, start with the **Streams UI** and let AI do the
% heavy lifting:
%
% - Use the **Streams** navigation entry in {{kib}} as your home base.
% - Accept AI-suggested partitions and parsing rules to get structured data quickly.
% - Use the **Significant Events** view to understand what's happening before diving into raw logs.
% - Explore individual streams using **Discover** to build familiarity with ES|QL queries.
% ::::
%
% ::::{tab-item} Expert user
% If you already manage {{es}} data pipelines and want full control:
%
% - Use [Wired streams](./classic-wired-streams.md#streams-wired-streams) to build a parent-child stream hierarchy with inherited
%   mappings, lifecycle settings, and processors.
% - Automate stream configuration with the [Streams API]({{kib-apis}}group/endpoint-streams) to
%   integrate Streams into your infrastructure-as-code workflows.
% - Define advanced ILM policies and failure store management for fine-grained cost and quality
%   control.
% - Use the [**Advanced** tab](./management/advanced.md) to inspect and manage underlying
%   {{es}} components when needed.
% ::::
% :::::
% ::::::