---
navigation_title: Automatic import
description: Automatic Import helps you parse, ingest, and create ECS mappings for data without a prebuilt integration—see the full guide for Elastic Security.
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Automatic import [security-automatic-import]

Automatic Import helps you quickly parse, ingest, and create [ECS mappings](https://www.elastic.co/elasticsearch/common-schema) for data from sources that don’t yet have prebuilt Elastic integrations. You can use it with {{elastic-sec}}, {{observability}}, and other Elastic solutions that rely on {{agent}} and integrations, so you can cover custom or niche data sources without building a full integration by hand. Automatic Import uses a large language model (LLM) with specialized instructions to quickly analyze your source data and create a custom integration.

While Elastic has 400+ [prebuilt data integrations](https://docs.elastic.co/en/integrations), Automatic Import helps you extend data coverage when you need logs or events from technologies that don’t have a dedicated integration yet. Elastic integrations (including those created by Automatic Import) normalize data to [the Elastic Common Schema (ECS)](ecs://reference/index.md), which creates uniformity across dashboards, search, alerts, machine learning, and more.

Refer to [Automatic Import](/explore-analyze/ai-features/automatic-import.md) for requirements, supported sample formats, recommended models, and step-by-step instructions.
