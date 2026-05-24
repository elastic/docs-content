---
navigation_title: Basic concepts
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

# Streams basic concepts

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


