---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-getting-started-solutions.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-hosted
description: Learn about Elastic solutions for search, observability, and security
  use cases. Get started with ready-to-use implementations and discover how to build
  custom applications.
---

# Solutions and use cases

:::{tip}
New to Elastic? Refer to [Elastic Fundamentals](/get-started/index.md) to understand the {{stack}}, its components, and your deployment options.
:::

Elastic helps you build applications for three main use cases: search, observability, and security. You can use platform-level capabilities through APIs, pre-built solutions with integrated UIs, or combine both approaches.

The documentation is organized to distinguish between platform-level search capabilities available to all deployments and solution-specific features and workflows.

## Search use case

The [Search use case](/solutions/search.md) documents core {{es}} search capabilities. These capabilities work identically across all Elastic [deployment types](/deploy-manage/deploy.md#choosing-your-deployment-type) and are accessed through {{es}} APIs and client libraries. You can build custom implementations using Elastic's APIs and features without using solutions.

## Solutions and project types

Solutions and project types provide pre-built UI tools and workflows with sensible defaults for specific use cases.

On {{ech}} and self-managed deployments, solutions are configured in your deployment settings. On {{serverless-full}}, you select a project type when creating your project.

| Solution/Project | Description | Get started |
| --- | --- | --- |
| **Elasticsearch** | UI tools for building search applications | [Elasticsearch solution](/solutions/elasticsearch-solution-project.md) |
| **Observability** | Monitor and troubleshoot applications and infrastructure | [Observability solution](/solutions/observability.md) |
| **Security** | Protect applications and infrastructure from threats | [Security solution](/solutions/security.md) |
