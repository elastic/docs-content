---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: Learn how to parse and process your data by extracting fields and applying processors in Streams.
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

# Parse and process

**Goal**: Raw log messages are structured into queryable fields.

User adds processing rules to extract fields from unstructured logs. AI generates a complete pipeline from sample data. User previews results, refines patterns or iteratively guides the AI until the output is correct, then deploys with confidence.

**Why Streams**: No ingest pipeline expertise needed. No pipeline JSON. No Logstash. The AI generates patterns, the UI shows a live preview of the resulting documents, the expertise barrier is gone.
