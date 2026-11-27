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
:::

:::{on-this-page}
:::

:::{get-started}
title: Get started with the Elastic Stack
steps:
  - title: Run Elasticsearch and Kibana
    options:
      - label: Try for free on Elastic Cloud
        description: Get an Elastic Stack running in a few minutes with no setup needed.
        url: https://cloud.elastic.co/registration
        url-label: Start a free trial
      - label: Run locally
        description: Spin up Elasticsearch and Kibana on your machine for development with `start-local`.
        code: curl -fsSL https://elastic.co/start-local | sh
        language: sh
  - title: Add your data
    description: Bring in your data with Elastic Agent, a language client, or a connector.
    link: /manage-data/ingest.md
    link-label: See ingest options
  - title: Explore and visualize
    description: Query your data in Discover, or start building charts.
    link: /explore-analyze/kibana-data-exploration-learning-tutorial.md
    link-label: Start the tutorial
:::

::::{card-group}
:title: Elastic Stack components
:id: components
:intro: The Elastic Stack, also known as the ELK Stack, is made of Elasticsearch, Kibana, Logstash, Elastic Agent, and Beats. They power [Elastic solutions](#solutions), and you have several ways to [deploy and manage them](#deploy).

:::{link-card}
title: Elasticsearch
icon: elasticsearch
links:
  - label: Elasticsearch docs hub
    url: /products/elasticsearch.md
  - label: Release notes
    url: elasticsearch://release-notes/index.md
  - label: Serverless release notes
    url: /release-notes/elastic-cloud-serverless/index.md
  - label: Elasticsearch reference
    url: elasticsearch://reference/index.md
:::

:::{link-card}
title: Kibana
icon: kibana
links:
  - label: Kibana docs hub
    url: /products/kibana.md
  - label: Release notes
    url: kibana://release-notes/index.md
  - label: Serverless release notes
    url: /release-notes/elastic-cloud-serverless/index.md
  - label: Kibana reference
    url: kibana://reference/index.md
:::

:::{link-card}
title: Logstash
icon: logstash
links:
  - label: Logstash docs hub
    url: /products/logstash.md
  - label: Release notes
    url: logstash://release-notes/index.md
  - label: Logstash reference
    url: logstash://reference/index.md
:::

:::{link-card}
title: Elastic Agent
icon: elastic-agent
links:
  - label: Fleet and Elastic Agent
    url: /reference/fleet/index.md
  - label: Release notes
    url: elastic-agent://release-notes/index.md
  - label: Elastic Agent as an OpenTelemetry Collector
    url: elastic-agent://reference/edot-collector/index.md
:::

:::{link-card}
title: Beats
icon: beats
links:
  - label: Beats reference
    url: beats://reference/index.md
  - label: Release notes
    url: beats://release-notes/index.md
  - label: Filebeat
    url: beats://reference/filebeat/index.md
  - label: Metricbeat
    url: beats://reference/metricbeat/index.md
:::
::::

::::{card-group}
:title: Elastic solutions
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

::::{card-group}
:title: Deploy your Elastic Stack
:id: deploy
:intro: Choose where to run the Elastic Stack: as a managed service, on Kubernetes, or on your own hosts. [Compare deployment types](/deploy-manage/deploy/deployment-comparison.md).

:::{link-card}
title: Elastic Cloud Serverless
description: Fully managed projects. Elastic runs the infrastructure and the upgrades.
links:
  - label: Overview
    url: /deploy-manage/deploy/elastic-cloud/serverless.md
  - label: Create a project
    url: /deploy-manage/deploy/elastic-cloud/create-serverless-project.md
  - label: Project settings
    url: /deploy-manage/deploy/elastic-cloud/project-settings.md
:::

:::{link-card}
title: Elastic Cloud Hosted
description: Managed deployments on AWS, Azure, or Google Cloud, with version control.
links:
  - label: Overview
    url: /deploy-manage/deploy/elastic-cloud/cloud-hosted.md
  - label: Create a deployment
    url: /deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md
  - label: Configure a deployment
    url: /deploy-manage/deploy/elastic-cloud/configure.md
  - label: Upgrade
    url: /deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md
:::

:::{link-card}
title: Elastic Cloud on Kubernetes
description: Run the stack on your own Kubernetes clusters with the ECK operator.
links:
  - label: Overview
    url: /deploy-manage/deploy/cloud-on-k8s.md
  - label: Install ECK
    url: /deploy-manage/deploy/cloud-on-k8s/install.md
  - label: Configure ECK
    url: /deploy-manage/deploy/cloud-on-k8s/configure.md
  - label: Upgrade
    url: /deploy-manage/upgrade/deployment-or-cluster/upgrade-on-eck.md
:::

:::{link-card}
title: Elastic Cloud Enterprise
description: Run your own Elastic Cloud on any infrastructure.
links:
  - label: Overview
    url: /deploy-manage/deploy/cloud-enterprise.md
  - label: Install ECE
    url: /deploy-manage/deploy/cloud-enterprise/install.md
  - label: Configure ECE
    url: /deploy-manage/deploy/cloud-enterprise/configure.md
  - label: Upgrade
    url: /deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ece.md
:::

:::{link-card}
title: Self-managed
description: Install and operate the stack yourself on your own hosts.
links:
  - label: Overview
    url: /deploy-manage/deploy/self-managed.md
  - label: Install Elasticsearch
    url: /deploy-manage/deploy/self-managed/installing-elasticsearch.md
  - label: Configure Elasticsearch
    url: /deploy-manage/deploy/self-managed/configure-elasticsearch.md
  - label: Upgrade
    url: /deploy-manage/upgrade/deployment-or-cluster/self-managed.md
:::
::::

:::::{explore}
:id: explore
:title: Explore the Elastic Stack
:mode: first
:intro: Find documentation for upgrading, monitoring, and securing the Elastic Stack.

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
