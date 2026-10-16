---
navigation_title: Claude Platform
description: Send OpenTelemetry traces from the Claude Platform, including Messages API requests and Claude Managed Agents sessions, to Elastic Observability through the Elastic Cloud Managed OTLP Endpoint.
applies_to:
  serverless:
    observability: ga
  deployment:
    ech: ga
products:
  - id: observability
  - id: cloud-serverless
  - id: cloud-hosted
---

# Send Claude Platform traces to Elastic

Anthropic can send OpenTelemetry traces of your Claude API usage straight to Elastic. After a Claude Console admin adds Elastic as a destination, traces for Messages API requests and Claude Managed Agents sessions start arriving in your Elastic project. You don't need to change your code or run an OpenTelemetry Collector.
