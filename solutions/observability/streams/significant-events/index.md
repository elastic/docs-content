---
navigation_title: Significant Events
description: Significant Events automatically correlates signals from your log streams into prioritized incidents using a combination of deterministic detection and AI-powered investigation.
applies_to:
  serverless: experimental
  stack: experimental 9.5+
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

Significant Events continuously converts raw log data into a ranked feed of incidents. The pipeline moves from broad to narrow. Many alerts fire, an AI agent narrows these down into findings, and the most important ones are surfaced as Significant Events.

For example: you onboard a stream, Significant Events extracts what's in it ("this stream contains a Python gRPC service called `recommendationservice` running on GKE"), generates targeted detection rules ("detect gRPC connection failures"), and runs those rules continuously. Results flow through discovery and surface as correlated Significant Events across your entire environment.

## Before you get started [sig-events-prerequisites]

Significant Events requires an **Enterprise license** or an active Enterprise trial.

To use Significant Events you also need a [Generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md), which routes LLM calls.

## How the pipeline works [sig-events-pipeline]

The pipeline runs in sequential phases that build on the output of the previous phase. Knowledge Indicator (KI) extraction and rule generation prepare your streams for detection and run on your schedule. Detection and discovery run continuously in the background after you enable Significant Events.

### 1. Knowledge indicator extraction [sig-events-phase-ki]

An LLM analyzes log samples from your streams and extracts services, infrastructure, dependencies, and failure patterns as Knowledge Indicators (KIs). Deterministic generators run in parallel to produce dataset statistics, log patterns, and error samples.

### 2. Rule generation [sig-events-phase-rules]

An LLM converts KIs into {{esql}} alerting rules scoped to the services and failure modes present in each stream. Generated rules are saved as stream assets. Lower-severity rules stay unbacked until you review and promote them; high-severity detections are promoted automatically and begin running right away.

### 3. Rule execution and detection [sig-events-phase-detection]

Promoted rules execute on a specified schedule against stream logs and record a count of matches per time bucket to the `.rule-events` index. A Detection workflow runs change point aggregation against those per-rule counts and writes a detection record whenever the aggregation finds a statistically significant shift.

### 4. Discovery [sig-events-phase-discovery]

Two agents run in sequence. The [Discovery agent](./how-it-works.md#sig-events-hiw-discovery-agent) reads detection records, correlates signals across rules and streams, and writes discovery records. The [Judge agent](./how-it-works.md#sig-events-hiw-triage) independently verifies each discovery and sets its status to open, closed, or dismissed.

## Learn more [sig-events-nav]

Refer to the following pages for more information on Significant Events:

- [Operator guide](./operator-guide.md): Learn more about system impact, cost drivers, and operational procedures
- [How Significant Events works](./how-it-works.md): Understand how Significant Events processes data, what runs where, and how to trace results across the system
- [Knowledge Indicators](./knowledge-indicators.md): Get an in-depth overview of how KIs work
