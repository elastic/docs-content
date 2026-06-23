---
applies_to:
  serverless: preview
  stack: preview 9.1+
description: Define periodic queries that surface important events from a stream using custom filters or AI-generated suggestions.
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

# Add significant events to Streams [streams-significant-events]

Significant Events periodically runs a query on your stream to find important events. Use it to create significant-event queries from AI suggestions or custom filters, and to surface errors, exceptions, or other log messages that matter to you.

To define significant events, either:

- **Generate significant events with AI:** Requires a [Generative AI connector](kibana://reference/connectors-kibana/gen-ai-connectors.md). If you don't know what you're looking for, let AI suggest queries based on your data. This works by using the previously identified [features](./advanced.md#streams-advanced-features) in your Stream to create specific queries based on the data you have in your Stream. Then, select the suggestions that make sense to you.
- **Create significant events from a query:** If you know what you're looking for, write your own query to find important events.
