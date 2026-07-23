---
navigation_title: Significant Events
description: Significant Events automatically correlates signals from your log streams into prioritized incidents using a combination of deterministic detection and AI-powered investigation.
applies_to:
  serverless: beta
  stack: beta 9.5+
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

# Significant Events [streams-sig-events-overview]

Significant Events continuously converts raw log data into a ranked feed of incidents. The pipeline moves from broad to narrow: many alerting rule executions produce fewer statistical detections, which an AI agent correlates into even fewer discoveries, which a judge reviews and surfaces as Significant Events.

For example: you onboard a stream, Significant Events extracts what's in it ("this stream contains a Python gRPC service called `recommendationservice` running on GKE"), generates targeted detection rules ("detect gRPC connection failures"), and runs those rules continuously. Results flow through discovery and surface as correlated Significant Events across your entire environment.

## Before you get started [sig-events-prerequisites]

Significant Events requires an **Enterprise license** or an active Enterprise trial.

To use Significant Events you also need:

- The `streams.significantEventsAvailable: true` feature flag enabled in your {{kib}} configuration.
- The `observability:streamsSigEventsScheduledDiscoveryEnabled` {{kib}} setting enabled (required for the detection, discovery, and triage workflows).
- A [Generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md), which routes LLM calls and incurs additional costs.

## How the pipeline works [sig-events-pipeline]

The pipeline runs in sequential phases that build on the output of the previous phase. KI extraction and rule generation prepare your streams for detection and run on your schedule. Detection and discovery run continuously in the background after you enable Significant Events.

### 1. Knowledge indicator extraction [sig-events-phase-ki]

An LLM analyzes log samples from your streams and extracts services, infrastructure, dependencies, and failure patterns as Knowledge Indicators (KIs). Deterministic generators run in parallel to produce dataset statistics, log patterns, and error samples.

### 2. Rule generation [sig-events-phase-rules]

An LLM converts KIs into {{esql}} alerting rules scoped to the services and failure modes present in each stream. Generated rules are saved as unbacked stream assets — you review and promote them before they start running.

### 3. Rule execution and detection [sig-events-phase-detection]

Promoted rules run against stream data on a per-rule schedule and write matching events to the alerts index. A detection workflow runs `change_point` analysis across those results every minute and writes detection records for statistically significant transitions.

### 4. Discovery [sig-events-phase-discovery]

Two agents run in sequence. The Discovery agent reads detection records, correlates signals across rules and streams, and writes discovery records. The Judge agent independently verifies each discovery and promotes, acknowledges, or dismisses it as a Significant Event.

## Learn more [sig-events-nav]

Refer to the following pages for more information on Significant Events:

- [Operator guide](./operator-guide.md): Learn more about system impact, cost drivers, and operational procedures
- [How Significant Events works](./how-it-works.md): Understand how Significant Events processes data, what runs where, and how to trace results across the system
- [Knowledge Indicators](./knowledge-indicators.md): Get an in-depth overview of how KIs work
