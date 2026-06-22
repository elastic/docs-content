---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
description: Learn how to monitor data quality and fix failed or degraded documents in your streams.
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

# Manage data quality

**Goal**: User knows when data health degrades and can fix issues without having to pivot elsewhere in the product.

User monitors the quality score, reviews degraded/failed documents, and fixes issues by testing against actual failing documents with real-time validation.

**Why Streams**: Failed documents are preserved in the failure store, not dropped. The quality tab shows what's broken, why, and since when. Fixes can be validated against real data before deployment. No separate infrastructure needed.

This is where the "why care about data quality" narrative lives, data only brings value when it's correct. Streams binds the insight (something is wrong) with the ability to fix it (test and deploy a fix).
