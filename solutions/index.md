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

Elastic helps you build applications for three main use cases: search, observability, and security. You can work directly with platform capabilities through APIs, use pre-built solutions with integrated UIs, or combine both approaches.

## Choose your path

| Your use case | What to use | Description |
| --- | --- | --- |
| Building search-powered applications | 1. [Core search capabilities](/solutions/search.md)<br><br> 2. [Elasticsearch solution](/solutions/elasticsearch-solution-project.md) | 1. Core {{es}} search features available across all deployment types, solutions, and project types<br><br>2. Additional UI tools that complement the core search features |
| Monitoring applications or infrastructure | [Observability solution](/solutions/observability.md) | Monitor and troubleshoot with logs, metrics, and traces |
| Protecting against threats | [Security solution](/solutions/security.md) | Detect and respond to security threats |

::::{tip}
Not sure which to choose? Start with the {{es}} solution, if you don't need the additional features in {{product.observability}} or {{product.security}}.
::::

## About solutions and project types

- On {{serverless-full}}, select a solution as your project type when creating a project.
- On {{ech}}, ECE, ECK, and self-managed clusters, select a default solution view when creating a deployment, or configure per [space](/deploy-manage/manage-spaces.md).

## Bare URL examples

This section demonstrates valid and invalid bare URLs for testing purposes.

### Valid bare URLs

These URLs should be detected and potentially converted to proper links:

- https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html
- https://github.com/elastic/elasticsearch
- https://developer.mozilla.org/en-US/docs/Web/HTTP
- Visit https://www.elastic.co for more information.
- Documentation is available at https://docs.elastic.co/search.

### Invalid patterns

- Port in URL: https://elasticsearch.example.co:9200/api
- Localhost: https://localhost:5601/app/kibana
- IP address: http://127.0.0.1:9200/_cluster/health
- Example domain: https://example.com/path/to/resource
- Subdomain of example: https://api.example.org/v1/endpoint
- Template placeholder: https://{{deployment_id}}.us-east-1.aws.found.io
- Broken AsciiDoc link: https://elastic.co/guide[broken
