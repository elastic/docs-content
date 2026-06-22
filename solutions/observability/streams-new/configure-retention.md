---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: Learn how to configure data retention policies for your streams.
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

# Configure retention

**Goal**: Each stream has an appropriate lifecycle policy. Storage costs are controlled and/or aligned with regulatory / compliance retention requirements.

User sets retention periods per stream. For wired streams, parent retention cascades to children, override at child level when needed.

**Why Streams**: Replaces a fragmented setup (data stream lifecycle, ILM, index templates, index settings) with a single tab. Shows storage size, ingestion averages, and tier distribution in one view.
