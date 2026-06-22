---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: Learn how to organize your data streams using routing and partitioning.
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

# Organize your data

**Goal**: Logs are separated into logical groups that can be managed independently.
User partitions their wired stream into child streams, by team, service, technology, or environment. Manual rules or AI-suggested groupings.

**Why Streams**: No external routing infrastructure (no Logstash, no third-party tools). Child streams inherit everything from the parent. Config changes propagate automatically through the hierarchy.

Skip this step if: using classic streams, or all logs need identical treatment.
