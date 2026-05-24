---
navigation_title: Use cases
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

# Streams use cases

## Incident investigation

An SRE receives an alert that a trading application is down. Instead of manually searching through
millions of log lines, they open Streams, where Significant Events has already surfaced a Java
out-of-memory error with the relevant context. In minutes — not hours — they identify the root
cause, escalate to the right team, and restore service.

## High-volume log management for platform team

A platform team ingests logs from dozens of microservices and needs to control costs without losing
context. Using Streams, they set per-stream retention policies, route high-value logs to longer
retention tiers, and use the failure store to catch and investigate parsing errors — all from a
single UI.


## Who Streams is for


:::::{tab-set}
::::{tab-item} Novice user
If you're new to log management or to Elastic, start with the **Streams UI** and let AI do the
heavy lifting:

- Use the **Streams** navigation entry in {{kib}} as your home base.
- Accept AI-suggested partitions and parsing rules to get structured data quickly.
- Use the **Significant Events** view to understand what's happening before diving into raw logs.
- Explore individual streams using **Discover** to build familiarity with ES|QL queries.
::::

::::{tab-item} Expert user
If you already manage {{es}} data pipelines and want full control:

- Use [Wired streams](./wired-streams.md) to build a parent-child stream hierarchy with inherited
  mappings, lifecycle settings, and processors.
- Automate stream configuration with the [Streams API]({{kib-apis}}group/endpoint-streams) to
  integrate Streams into your infrastructure-as-code workflows.
- Define advanced ILM policies and failure store management for fine-grained cost and quality
  control.
- Use the [**Advanced** tab](./management/advanced.md) to inspect and manage underlying
  {{es}} components when needed.
::::
:::::

