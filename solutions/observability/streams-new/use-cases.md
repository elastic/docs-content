---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: Explore common use cases for Streams.
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

# Use cases

**Incident investigation**

An SRE receives an alert that a trading application is down. Instead of manually searching through
millions of log lines, they open Streams, where Significant Events has already surfaced a Java
out-of-memory error with the relevant context. In minutes — not hours — they identify the root
cause, escalate to the right team, and restore service.

**High-volume log management for platform team**

A platform team ingests logs from dozens of microservices and needs to control costs without losing
context. Using Streams, they set per-stream retention policies, route high-value logs to longer
retention tiers, and use the failure store to catch and investigate parsing errors — all from a
single UI.