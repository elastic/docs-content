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
:description: Elasticsearch, Kibana, Logstash, and Beats, also known as the ELK Stack, work together to ingest, store, search, and visualize data at scale. Run the stack as a managed service or in your own environment.
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
:intro: Release notes for Elasticsearch, Kibana, Logstash, Observability, and Security.

:::{link-card}
title: Elasticsearch
link: elasticsearch://release-notes/index.md
icon: elasticsearch
description: Elasticsearch release notes.
:::

:::{link-card}
title: Kibana
link: kibana://release-notes/index.md
icon: kibana
description: Kibana release notes.
:::

:::{link-card}
title: Logstash
link: logstash://release-notes/index.md
icon: logstash
description: Logstash release notes.
:::

:::{link-card}
title: Observability
link: /release-notes/elastic-observability/index.md
icon: observability
description: Observability solution release notes.
:::

:::{link-card}
title: Security
link: /release-notes/elastic-security/index.md
icon: security
description: Security solution release notes.
:::
::::

::::{card-group}
:title: Solutions
:id: solutions
:variant: solutions
:intro: Purpose-built experiences on the Elastic Stack for search, observability, and security.

:::{link-card}
title: Elasticsearch
link: /solutions/elasticsearch-solution-project.md
icon: elasticsearch
variant: es
links:
  - label: Solution overview
    url: /solutions/elasticsearch-solution-project.md
  - label: Get started
    url: /solutions/elasticsearch-solution-project/get-started.md
  - label: Elasticsearch docs hub
    url: /products/elasticsearch.md
:::

:::{link-card}
title: Observability
link: /solutions/observability.md
icon: observability
variant: obs
links:
  - label: Solution overview
    url: /solutions/observability.md
  - label: Get started
    url: /solutions/observability/get-started.md
  - label: Observability release notes
    url: /release-notes/elastic-observability/index.md
:::

:::{link-card}
title: Security
link: /solutions/security.md
icon: security
variant: sec
links:
  - label: Solution overview
    url: /solutions/security.md
  - label: Get started
    url: /solutions/security/get-started.md
  - label: Security release notes
    url: /release-notes/elastic-security/index.md
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
title: Product hubs
links:
  - label: Elasticsearch
    url: /products/elasticsearch.md
  - label: Kibana
    url: /products/kibana.md
  - label: Logstash
    url: /products/logstash.md
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
:title: Deploy and install
:id: deploy

:::{link-card}
title: Elastic Cloud
link: /deploy-manage/deploy/elastic-cloud.md
description: Managed Elasticsearch and Kibana, with no local install.
links:
  - label: Elastic Cloud overview
    url: /deploy-manage/deploy/elastic-cloud.md
  - label: Serverless
    url: /deploy-manage/deploy/elastic-cloud/serverless.md
  - label: Start a free trial
    url: https://cloud.elastic.co/registration
:::

:::{link-card}
title: Self-managed
link: /deploy-manage/deploy/self-managed/installing-elasticsearch.md
description: Install stack components on your own infrastructure, in this order.
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
link: /deploy-manage/deploy/cloud-on-k8s.md
description: Run the stack with Kubernetes or Elastic Cloud Enterprise.
links:
  - label: Elastic Cloud on Kubernetes (ECK)
    url: /deploy-manage/deploy/cloud-on-k8s.md
  - label: Elastic Cloud Enterprise (ECE)
    url: /deploy-manage/deploy/cloud-enterprise.md
:::
::::

::::{card-group}
:title: Upgrade
:id: upgrade

:::{link-card}
title: Plan an upgrade
link: /deploy-manage/upgrade.md
description: Prepare a stack upgrade, then upgrade the cluster and ingest components.
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
::::

::::{card-group}
:title: Main components
:id: components

:::{link-card}
title: Elasticsearch
link: /products/elasticsearch.md
description: The distributed search and analytics engine at the heart of the stack.
links:
  - label: Elasticsearch docs hub
    url: /products/elasticsearch.md
  - label: How Elasticsearch fits in the stack
    url: /get-started/the-stack.md#stack-components-elasticsearch
:::

:::{link-card}
title: Kibana
link: /products/kibana.md
description: The UI for exploring data, building dashboards, and managing the stack.
links:
  - label: Kibana docs hub
    url: /products/kibana.md
  - label: How Kibana fits in the stack
    url: /get-started/the-stack.md#stack-components-kibana
:::

:::{link-card}
title: Elastic Agent
link: /reference/fleet/index.md
description: A single agent to collect logs, metrics, and traces, managed from Kibana.
links:
  - label: Fleet and Elastic Agent
    url: /reference/fleet/index.md
  - label: Install Elastic Agent
    url: /reference/fleet/install-elastic-agents.md
:::

:::{link-card}
title: Logstash
link: /products/logstash.md
description: Server-side pipelines for collecting, transforming, and shipping events.
links:
  - label: Logstash docs hub
    url: /products/logstash.md
  - label: How Logstash fits in the stack
    url: /get-started/the-stack.md#stack-components-logstash
:::

:::{link-card}
title: Beats and OpenTelemetry
link: beats://reference/index.md
description: Lightweight shippers and OpenTelemetry distributions for ingest.
links:
  - label: Beats
    url: beats://reference/index.md
  - label: Elastic Distributions of OpenTelemetry
    url: opentelemetry://reference/index.md
:::
::::

:::::
