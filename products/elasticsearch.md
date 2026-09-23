---
layout: hub
navigation_title: Elasticsearch
description: Elasticsearch documentation. Index, search, and analyze data at any scale. Run it as a managed service or in your own environment.
products:
  - id: elasticsearch
---

:::{hero}
:icon: elasticsearch
:title: Elasticsearch documentation hub
:description: The distributed search and analytics engine at the heart of the Elastic platform. Index, search, and analyze data at any scale, build semantic and vector search experiences, and power applications. Run it as a managed service or in your own environment.
:primary-action: [Get started](#get-started)
:secondary-action: [What's new](#whats-new)
:tertiary-action: [Explore Elasticsearch docs](#explore)
:::

:::{get-started}
title: Get started in 3 steps
intro: Start a local development environment or a free Elastic Cloud trial, then run your first queries.
steps:
  - title: Run Elasticsearch
    options:
      - label: Run locally
        description: Spin up Elasticsearch on your machine for development with `start-local`.
        code: curl -fsSL https://elastic.co/start-local | sh
        language: sh
      - label: Try on Cloud
        description: Start a free Elastic Cloud trial. No local setup needed.
        url: https://cloud.elastic.co/registration
        url-label: Start a free trial
  - title: Ingest your data into Elasticsearch
    description: Send documents to Elasticsearch using the APIs, ingest pipelines, connectors, or a language client.
    link: /manage-data/ingest.md
    link-label: Ingest your data
  - title: Search your data
    description: Build queries to find, rank, and analyze your documents.
    link: /solutions/search/querying-for-search.md
    link-label: Build search queries
:::

:::{whats-new}
:product: elasticsearch
:::

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

::::{card-group}
:title: Get hands-on with Elasticsearch
:id: hands-on
:intro: New to Elasticsearch? Follow a guided quickstart to index and search your first data set.

:::{link-card}
title: Search fundamentals
links:
  - label: Index and search basics
    url: /solutions/search/get-started/index-basics.md
  - label: Build your first query with Python
    url: /solutions/search/get-started/keyword-search-python.md
:::

:::{link-card}
title: Semantic search and ES|QL
links:
  - label: Get started with semantic search
    url: /solutions/search/get-started/semantic-search.md
  - label: ES|QL tutorials
    url: elasticsearch://reference/query-languages/esql/esql-examples.md
:::

:::{link-card}
title: Specialized quickstarts
links:
  - label: Time series data stream basics
    url: /manage-data/data-store/data-streams/quickstart-tsds.md
  - label: Browse all quickstarts
    url: /solutions/search/get-started/quickstarts.md
:::
::::

:::::{explore}
:id: explore
:title: Explore Elasticsearch
:intro: Find the Elasticsearch documentation you need, organized by task, from deploying and ingesting to searching, securing, and operating.

::::{card-group}
:title: Quick links
:id: quick-links

:::{link-card}
title: Releases and APIs
links:
  - label: Release notes
    url: elasticsearch://release-notes/index.md
  - label: Elasticsearch API docs
    url: https://www.elastic.co/docs/api/doc/elasticsearch
  - label: Language clients
    url: /reference/elasticsearch-clients/index.md
:::

:::{link-card}
title: Configuration
links:
  - label: Configure Elastic Stack settings
    url: /deploy-manage/stack-settings.md
  - label: Cluster configuration reference
    url: elasticsearch://reference/elasticsearch/configuration-reference/index.md
  - label: Index settings
    url: elasticsearch://reference/elasticsearch/index-settings/index.md
:::

:::{link-card}
title: Operations
links:
  - label: Production guidance
    url: /deploy-manage/production-guidance/elasticsearch-in-production-environments.md
  - label: Upgrade Elasticsearch
    url: /deploy-manage/upgrade/deployment-or-cluster.md
  - label: Technical reference
    url: elasticsearch://reference/elasticsearch/index.md
:::
::::

::::{card-group}
:title: Deploy and manage
:id: deploy

:::{link-card}
title: Use Elastic Cloud
links:
  - label: Serverless
    url: /deploy-manage/deploy/elastic-cloud/serverless.md
  - label: Elastic Cloud Hosted
    url: /deploy-manage/deploy/elastic-cloud/cloud-hosted.md
:::

:::{link-card}
title: Deploy with an orchestrator
links:
  - label: Elastic Cloud on Kubernetes (ECK)
    url: /deploy-manage/deploy/cloud-on-k8s.md
  - label: Elastic Cloud Enterprise (ECE)
    url: /deploy-manage/deploy/cloud-enterprise.md
:::

:::{link-card}
title: Run Elasticsearch yourself
links:
  - label: Choose an install method
    url: /deploy-manage/deploy/self-managed/installing-elasticsearch.md
  - label: Docker
    url: /deploy-manage/deploy/self-managed/install-elasticsearch-with-docker.md
  - label: Debian / Ubuntu
    url: /deploy-manage/deploy/self-managed/install-elasticsearch-with-debian-package.md
  - label: RPM
    url: /deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md
  - label: Packages and archives
    url: /deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos.md
  - label: Configure Elasticsearch
    url: /deploy-manage/deploy/self-managed/configure-elasticsearch.md
:::

:::{link-card}
title: Design your deployment
links:
  - label: Distributed architecture
    url: /deploy-manage/distributed-architecture.md
  - label: Production guidance
    url: /deploy-manage/production-guidance/elasticsearch-in-production-environments.md
  - label: Reference architectures
    url: /deploy-manage/reference-architectures.md
:::
:::{link-card}
title: Operate and maintain
links:
  - label: Monitor Elasticsearch
    url: /deploy-manage/monitor.md
  - label: Autoscaling
    url: /deploy-manage/autoscaling.md
  - label: Maintenance and restarts
    url: /deploy-manage/maintenance.md
  - label: Upgrade Elasticsearch
    url: /deploy-manage/upgrade/deployment-or-cluster.md
:::
::::

::::{card-group}
:title: Prepare and index data
:id: ingest

:::{link-card}
title: Index data
links:
  - label: Index API
    url: https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-index
  - label: Bulk API
    url: https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk
  - label: Indices and data streams
    url: /manage-data/data-store.md
:::

:::{link-card}
title: Transform and enrich
links:
  - label: Ingest pipelines
    url: /manage-data/ingest/transform-enrich/ingest-pipelines.md
  - label: Enrich data
    url: /manage-data/ingest/transform-enrich/data-enrichment.md
  - label: Ingest processors
    url: elasticsearch://reference/elasticsearch/ingest-processing/index.md
:::

:::{link-card}
title: Map fields
links:
  - label: Mappings
    url: /manage-data/data-store/mapping.md
  - label: Field types
    url: elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md
  - label: Runtime fields
    url: /manage-data/data-store/mapping/runtime-fields.md
:::

:::{link-card}
title: Analyze text
links:
  - label: Text analysis
    url: /manage-data/data-store/text-analysis.md
  - label: Configure analyzers
    url: /manage-data/data-store/text-analysis/configure-text-analysis.md
:::

:::{link-card}
title: Ingestion tools
link: /manage-data/ingest.md
links:
  - label: Choose an ingest method
    url: /manage-data/ingest.md
  - label: Fleet and Elastic Agent
    url: /reference/fleet/index.md
  - label: Logstash
    url: logstash://reference/index.md
  - label: Beats
    url: beats://reference/index.md
  - label: Elastic Distributions of OpenTelemetry
    url: opentelemetry://reference/index.md
:::
::::

::::{card-group}
:title: Search and analyze data
:id: search

:::{link-card}
title: Search with the Search API
links:
  - label: Search API
    url: https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search
  - label: Query DSL
    url: elasticsearch://reference/query-languages/query-dsl/full-text-queries.md
  - label: Retrievers
    url: elasticsearch://reference/elasticsearch/rest-apis/retrievers.md
  - label: Aggregations
    url: /explore-analyze/query-filter/aggregations.md
:::

:::{link-card}
title: ES|QL
links:
  - label: Get started with ES|QL
    url: elasticsearch://reference/query-languages/esql/esql-getting-started.md
  - label: Syntax reference
    url: elasticsearch://reference/query-languages/esql/esql-syntax-reference.md
  - label: ES|QL for search
    url: /solutions/search/esql-for-search.md
:::

:::{link-card}
title: Search across clusters and projects
links:
  - label: Cross-cluster search
    url: /explore-analyze/cross-cluster-search.md
  - label: Cross-project search
    url: /explore-analyze/cross-project-search.md
:::
::::

::::{card-group}
:title: Vector database
:id: vector

:::{link-card}
title: Semantic and vector search
links:
  - label: Semantic search
    url: /solutions/search/semantic-search.md
  - label: Vector search
    url: /solutions/search/vector.md
  - label: Hybrid search
    url: /solutions/search/hybrid-search.md
:::

:::{link-card}
title: Inference
links:
  - label: Inference API
    url: https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-inference
  - label: Semantic search with inference
    url: /solutions/search/semantic-search/semantic-search-inference.md
:::
::::

::::{card-group}
:title: Build applications
:id: build

:::{link-card}
title: APIs, clients, and examples
links:
  - label: Elasticsearch API docs
    url: https://www.elastic.co/docs/api/doc/elasticsearch
  - label: Language clients
    url: /reference/elasticsearch-clients/index.md
  - label: REST API examples
    url: elasticsearch://reference/elasticsearch/rest-apis/api-examples.md
:::

:::{link-card}
title: Painless scripting
links:
  - label: Write Painless scripts
    url: /explore-analyze/scripting/modules-scripting-painless.md
  - label: Language specification
    url: elasticsearch://reference/scripting-languages/painless/painless-language-specification.md
:::
::::

::::{card-group}
:title: Manage the data lifecycle
:id: lifecycle

:::{link-card}
title: Choose a strategy
links:
  - label: Data lifecycle overview
    url: /manage-data/lifecycle.md
:::

:::{link-card}
title: Data stream lifecycle
links:
  - label: Data stream lifecycle
    url: /manage-data/lifecycle/data-stream.md
:::

:::{link-card}
title: Index lifecycle management
links:
  - label: Index lifecycle management (ILM)
    url: /manage-data/lifecycle/index-lifecycle-management.md
:::

:::{link-card}
title: Back up and restore
links:
  - label: Protect and recover data
    url: /deploy-manage/tools/snapshot-and-restore.md
  - label: Cross-cluster replication
    url: /deploy-manage/tools/cross-cluster-replication.md
:::
::::

::::{card-group}
:title: Secure Elasticsearch
:id: security
:::{link-card}
title: Get started with security
links:
  - label: Security overview
    url: /deploy-manage/security.md
:::

:::{link-card}
title: Protect data and connections
links:
  - label: Initial security setup
    url: /deploy-manage/security/secure-your-cluster-deployment.md
  - label: TLS encryption
    url: /deploy-manage/security/secure-cluster-communications.md
  - label: Network security
    url: /deploy-manage/security/network-security.md
:::

:::{link-card}
title: Authenticate users
link: /deploy-manage/users-roles.md
links:
  - label: Cluster-level authentication
    url: /deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md
  - label: Cloud organization SSO
    url: /deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md
:::

:::{link-card}
title: Control access
links:
  - label: User roles
    url: /deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md
  - label: Serverless custom roles
    url: /deploy-manage/users-roles/serverless-custom-roles.md
  - label: API keys
    url: /deploy-manage/api-keys.md
  - label: Field and document-level security
    url: /deploy-manage/users-roles/cluster-or-deployment-auth/controlling-access-at-document-field-level.md
  - label: Audit logging
    url: /deploy-manage/security/logging-configuration/security-event-audit-logging.md
:::

::::

::::{card-group}
:title: Troubleshoot
:id: troubleshoot

:::{link-card}
title: Cluster health and availability
links:
  - label: Cluster issues
    url: /troubleshoot/elasticsearch/clusters.md
:::

:::{link-card}
title: Indexing and search
links:
  - label: Troubleshoot search
    url: /troubleshoot/elasticsearch/troubleshooting-searches.md
:::

:::{link-card}
title: Snapshot and restore
links:
  - label: Snapshot problems
    url: /troubleshoot/elasticsearch/snapshot-and-restore.md
:::

:::{link-card}
title: Clients and diagnostics
links:
  - label: Client problems
    url: /troubleshoot/elasticsearch/clients.md
  - label: Capture diagnostics
    url: /troubleshoot/elasticsearch/diagnostic.md
:::
::::

::::{card-group}
:title: Reference
:id: reference

:::{link-card}
title: Elasticsearch reference
links:
  - label: Cluster configuration
    url: elasticsearch://reference/elasticsearch/configuration-reference/index.md
  - label: Index settings
    url: elasticsearch://reference/elasticsearch/index-settings/index.md
  - label: Mapping
    url: elasticsearch://reference/elasticsearch/mapping-reference/index.md
  - label: Aggregations
    url: elasticsearch://reference/aggregations/index.md
  - label: Text analysis
    url: elasticsearch://reference/elasticsearch/analysis-reference/index.md
  - label: Ingest processors
    url: elasticsearch://reference/elasticsearch/ingest-processing/index.md
:::

:::{link-card}
title: APIs and query languages
links:
  - label: REST APIs and conventions
    url: elasticsearch://reference/elasticsearch/rest-apis/index.md
  - label: Query DSL
    url: elasticsearch://reference/query-languages/query-dsl/full-text-queries.md
  - label: ES|QL
    url: elasticsearch://reference/query-languages/esql/esql-getting-started.md
  - label: Elasticsearch SQL
    url: elasticsearch://reference/query-languages/esql/elasticsearch-sql.md
:::
:::{link-card}
title: Clients and tools
links:
  - label: Language clients
    url: /reference/elasticsearch-clients/index.md
  - label: Elastic CLI
    url: cli://index.md
  - label: Command-line tools
    url: elasticsearch://reference/elasticsearch/command-line-tools/index.md
  - label: Plugins
    url: /deploy-manage/deploy/self-managed/plugins.md
:::
::::

:::::
