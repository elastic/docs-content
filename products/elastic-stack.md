---
layout: hub
navigation_title: Elastic Stack
description: Elastic Stack documentation, also known as the ELK Stack. Elasticsearch, Kibana, Logstash, and Beats work together to ingest, store, search, and visualize data.
products:
  - id: elastic-stack
---

:::{hero}
:icon: elastic-stack
:title: Elastic Stack documentation hub
:description: Elasticsearch, Kibana, Logstash, and Beats, also known as the Elastic Stack or ELK Stack, work together to ingest, store, search, and visualize data at scale. Run the stack as a managed service or in your own environment.
:primary-action: [Get started](#get-started)
:secondary-action: [What's new](#whats-new)
:tertiary-action: [Explore Elastic Stack docs](#explore)
:::

:::{get-started}
title: Get started in 3 steps
intro: Start a local development environment or a free Elastic Cloud trial, then ingest data and explore it in Kibana.
steps:
  - title: Run Elasticsearch and Kibana
    options:
      - label: Run locally
        description: Spin up Elasticsearch and Kibana on your machine for development with `start-local`.
        code: curl -fsSL https://elastic.co/start-local | sh
        language: sh
      - label: Try on Cloud
        description: Start a free Elastic Cloud trial. No local setup needed.
        url: https://cloud.elastic.co/registration
        url-label: Start a free trial
  - title: Ingest your data
    description: Send documents to Elasticsearch using the APIs, ingest pipelines, Elastic Agent, Logstash, or a language client.
    link: /manage-data/ingest.md
    link-label: Ingest your data
  - title: Explore and visualize
    description: Open Discover, then build your first chart and dashboard.
    link: /explore-analyze/kibana-data-exploration-learning-tutorial.md
    link-label: Start the tutorial
:::

::::{card-group}
:title: What's new
:id: whats-new
:intro: Release notes for Elasticsearch, Kibana, Elastic Agent, Logstash, and Beats.

:::{link-card}
title: Elasticsearch
link: elasticsearch://release-notes/index.md
icon: elasticsearch
:::

:::{link-card}
title: Kibana
link: kibana://release-notes/index.md
icon: kibana
:::

:::{link-card}
title: Elastic Agent
link: elastic-agent://release-notes/index.md
:::

:::{link-card}
title: Logstash
link: logstash://release-notes/index.md
icon: logstash
:::

:::{link-card}
title: Beats
link: beats://release-notes/index.md
:::
::::

::::{card-group}
:title: Solutions
:id: solutions
:variant: solutions
:intro: Solutions are packages of Elastic capabilities optimized for certain use cases. All solutions include the core storage, querying, and analytics capabilities of Elasticsearch and Kibana.

:::{link-card}
title: Elasticsearch
icon: elasticsearch
variant: es
links:
  - label: Overview
    url: /solutions/elasticsearch-solution-project.md
  - label: Get started
    url: /solutions/elasticsearch-solution-project/get-started.md
  - label: Agent Builder
    url: /explore-analyze/ai-features/elastic-agent-builder.md
  - label: Query rules
    url: /solutions/elasticsearch-solution-project/query-rules-ui.md
  - label: Content connectors
    url: elasticsearch://reference/search-connectors/index.md
  - label: Index management
    url: /manage-data/data-store/perform-index-operations.md
:::

:::{link-card}
title: Vector Database
icon: vectordb
variant: es
links:
  - label: Overview
    url: /solutions/vector-database.md
  - label: Get started
    url: /solutions/vector-database/get-started.md
  - label: Vector and full-text search
    url: /solutions/vector-database/vector-full-text-search.md
  - label: RAG
    url: /solutions/search/rag.md
  - label: Hybrid search
    url: /solutions/search/hybrid-search.md
  - label: Semantic search
    url: /solutions/search/semantic-search.md
:::

:::{link-card}
title: Observability
icon: observability
variant: obs
links:
  - label: Overview
    url: /solutions/observability.md
  - label: Get started
    url: /solutions/observability/get-started.md
  - label: APM
    url: /solutions/observability/apm/index.md
  - label: Logs
    url: /solutions/observability/logs.md
  - label: Infrastructure
    url: /solutions/observability/infra-and-hosts.md
  - label: Synthetics
    url: /solutions/observability/synthetics/index.md
:::

:::{link-card}
title: Security
icon: security
variant: sec
links:
  - label: Overview
    url: /solutions/security.md
  - label: Get started
    url: /solutions/security/get-started.md
  - label: SIEM
    url: /solutions/security/get-started/get-started-detect-with-siem.md
  - label: Detection rules
    url: /solutions/security/detect-and-alert/manage-detection-rules.md
  - label: Elastic Defend
    url: /solutions/security/configure-elastic-defend.md
  - label: Cases
    url: /solutions/security/investigate/security-cases.md
:::
::::

:::::{explore}
:id: explore
:title: Explore the Elastic Stack
:intro: Find documentation for deploying, upgrading, and operating the products that make up the stack.

::::{card-group}
:title: Quick links
:id: quick-links

:::{link-card}
title: How the stack fits together
links:
  - label: Stack components
    url: /get-started/the-stack.md
  - label: Deployment options
    url: /get-started/deployment-options.md
  - label: Versioning and availability
    url: /get-started/versioning-availability.md
:::

:::{link-card}
title: Get started locally
links:
  - label: Local development quickstart
    url: /deploy-manage/deploy/self-managed/local-development-installation-quickstart.md
  - label: Ingest your data
    url: /manage-data/ingest.md
:::
::::

::::{card-group}
:title: Elastic Stack components
:id: components

:::{link-card}
title: Elasticsearch
links:
  - label: Elasticsearch docs hub
    url: /products/elasticsearch.md
  - label: How Elasticsearch fits in the stack
    url: /get-started/the-stack.md#stack-components-elasticsearch
:::

:::{link-card}
title: Kibana
links:
  - label: Kibana docs hub
    url: /products/kibana.md
  - label: How Kibana fits in the stack
    url: /get-started/the-stack.md#stack-components-kibana
:::

:::{link-card}
title: Elastic Agent
links:
  - label: Fleet and Elastic Agent
    url: /reference/fleet/index.md
  - label: Integrations
    url: /reference/fleet/manage-integrations.md
  - label: Install Elastic Agent
    url: /reference/fleet/install-elastic-agents.md
:::

:::{link-card}
title: Logstash
links:
  - label: Logstash docs hub
    url: /products/logstash.md
  - label: How Logstash fits in the stack
    url: /get-started/the-stack.md#stack-components-logstash
:::

:::{link-card}
title: Beats and OpenTelemetry
links:
  - label: Beats
    url: beats://reference/index.md
  - label: Elastic Distributions of OpenTelemetry
    url: opentelemetry://reference/index.md
:::
::::

::::{card-group}
:title: Deploy and install
:id: deploy

:::{link-card}
title: Plan your deployment
links:
  - label: Production guidance
    url: /deploy-manage/production-guidance.md
  - label: Reference architectures
    url: /deploy-manage/reference-architectures.md
:::

:::{link-card}
title: Elastic Cloud
links:
  - label: Elastic Cloud overview
    url: /deploy-manage/deploy/elastic-cloud.md
  - label: Elastic Cloud Hosted
    url: /deploy-manage/deploy/elastic-cloud/cloud-hosted.md
  - label: Serverless
    url: /deploy-manage/deploy/elastic-cloud/serverless.md
  - label: Start a free trial
    url: https://cloud.elastic.co/registration
:::

:::{link-card}
title: Self-managed
links:
  - label: Install Elasticsearch
    url: /deploy-manage/deploy/self-managed/installing-elasticsearch.md
  - label: Install Kibana
    url: /deploy-manage/deploy/self-managed/install-kibana.md
  - label: Install Logstash
    url: logstash://reference/installing-logstash.md
  - label: Install Elastic Agent
    url: /reference/fleet/install-elastic-agents.md
:::

:::{link-card}
title: Orchestrators
links:
  - label: Elastic Cloud on Kubernetes (ECK)
    url: /deploy-manage/deploy/cloud-on-k8s.md
  - label: Elastic Cloud Enterprise (ECE)
    url: /deploy-manage/deploy/cloud-enterprise.md
:::
::::

::::{card-group}
:title: Operate and manage
:id: operate

:::{link-card}
title: Upgrade
links:
  - label: Upgrade overview
    url: /deploy-manage/upgrade.md
  - label: Plan your upgrade
    url: /deploy-manage/upgrade/plan-upgrade.md
  - label: Upgrade the deployment or cluster
    url: /deploy-manage/upgrade/deployment-or-cluster.md
  - label: Upgrade ingest components
    url: /deploy-manage/upgrade/ingest-components.md
:::

:::{link-card}
title: Monitor and maintain
links:
  - label: Monitor the stack
    url: /deploy-manage/monitor.md
  - label: Maintenance and restarts
    url: /deploy-manage/maintenance.md
  - label: Protect and recover data
    url: /deploy-manage/tools.md
  - label: Licenses and subscriptions
    url: /deploy-manage/license.md
:::

:::{link-card}
title: Secure and authenticate
links:
  - label: Secure the stack
    url: /deploy-manage/security.md
  - label: Authentication and users
    url: /deploy-manage/users-roles.md
  - label: API keys
    url: /deploy-manage/api-keys.md
:::
::::

:::::
