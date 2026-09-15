---
layout: hub
navigation_title: Kibana
description: Kibana documentation. Explore and visualize your data, build dashboards, set up alerts, automate tasks with AI, and use purpose-built solutions for Search, Observability, and Security.
products:
  - id: kibana
---

:::{hero}
:icon: kibana
:title: Kibana documentation hub
:description: The UI for the Elasticsearch platform. Explore and visualize your data, build dashboards, set up alerts, automate tasks with AI, and use purpose-built solutions for Search, Observability, and Security.
:primary-action: [Get started](#get-started)
:secondary-action: [What's new](#whats-new)
:tertiary-action: [Explore Kibana docs](#explore)
:::

:::{get-started}
title: Get started with Kibana
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
  - title: Add data in Kibana
    description: Upload a file, add an integration, or use sample data so you have something to explore.
    link: /manage-data/ingest.md
    link-label: See ingest options
  - title: Explore and visualize
    description: Open Discover, then build your first chart and dashboard.
    link: /explore-analyze/kibana-data-exploration-learning-tutorial.md
    link-label: Start the tutorial
:::

:::{whats-new}
:product: kibana
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
:::
::::

:::::{explore}
:id: explore
:title: Explore Kibana
:intro: Find the Kibana app or task you need, whether you're querying data, building a dashboard, or managing the stack.

::::{card-group}
:title: Quick links
:id: quick-links

:::{link-card}
title: Find your way around
links:
  - label: The Kibana interface
    url: /explore-analyze/find-and-organize/kibana-interface.md
  - label: Find apps and objects
    url: /explore-analyze/find-and-organize/find-apps-and-objects.md
  - label: Customize navigation
    url: /explore-analyze/find-and-organize/customize-navigation.md
:::

:::{link-card}
title: Release notes
links:
  - label: Kibana
    url: kibana://release-notes/index.md
  - label: Serverless
    url: /release-notes/elastic-cloud-serverless/index.md
  - label: Breaking changes
    url: kibana://release-notes/breaking-changes.md
:::

:::{link-card}
title: APIs
links:
  - label: Kibana API
    url: https://www.elastic.co/docs/api/doc/kibana
  - label: Serverless Kibana API
    url: https://www.elastic.co/docs/api/doc/serverless-kibana
:::

:::{link-card}
title: Configuration
links:
  - label: Configuration reference
    url: kibana://reference/configuration-reference.md
  - label: Advanced settings
    url: kibana://reference/advanced-settings.md
  - label: Security settings
    url: kibana://reference/configuration-reference/security-settings.md
:::
::::

::::{card-group}
:title: Deploy and manage
:id: deploy

:::{link-card}
title: Managed on Elastic Cloud
description: Run Kibana as a hosted deployment or a serverless project.
links:
  - label: Elastic Cloud Hosted
    url: /deploy-manage/deploy/elastic-cloud/access-kibana.md
  - label: Serverless
    url: /deploy-manage/deploy/elastic-cloud/serverless.md
:::

:::{link-card}
title: Self-orchestrated
description: Deploy and manage Kibana with Elastic Cloud on Kubernetes or Elastic Cloud Enterprise.
links:
  - label: Elastic Cloud on Kubernetes (ECK)
    url: /deploy-manage/deploy/cloud-on-k8s/kibana-configuration.md
  - label: Elastic Cloud Enterprise (ECE)
    url: /deploy-manage/deploy/cloud-enterprise/access-kibana.md
:::

:::{link-card}
title: Self-managed
description: Install and run Kibana on your own infrastructure.
links:
  - label: Install Kibana
    url: /deploy-manage/deploy/self-managed/install-kibana.md
  - label: Docker
    url: /deploy-manage/deploy/self-managed/install-kibana-with-docker.md
  - label: Configure (kibana.yml)
    url: /deploy-manage/deploy/self-managed/configure-kibana.md
:::

:::{link-card}
title: Maintain and monitor
description: Production guidance, upgrades, and logging for Kibana itself. Monitor the rest of the stack from Manage data and Kibana.
links:
  - label: Run in production
    url: /deploy-manage/production-guidance/kibana-in-production-environments.md
  - label: Upgrade Kibana
    url: /deploy-manage/upgrade/deployment-or-cluster.md
  - label: Logging
    url: /deploy-manage/monitor/logging-configuration/kibana-logging.md
:::
::::

::::{card-group}
:title: Manage data and Kibana
:id: stack-management

:::{link-card}
title: Data and indices
description: Manage Elasticsearch indices, data streams, ingest pipelines, and transforms from Kibana.
links:
  - label: Index management
    url: /manage-data/lifecycle/index-lifecycle-management/index-management-in-kibana.md
  - label: Data streams
    url: /manage-data/data-store/data-streams/manage-data-stream.md
  - label: Transforms
    url: /explore-analyze/transforms/transform-setup.md
:::

:::{link-card}
title: Integrations and Fleet
description: Browse and install integrations, then deploy and manage Elastic Agents from Kibana.
links:
  - label: Integrations
    url: /reference/fleet/manage-integrations.md
  - label: Fleet
    url: /reference/fleet/index.md
  - label: Manage agents
    url: /reference/fleet/manage-elastic-agents-in-fleet.md
:::

:::{link-card}
title: Stack Monitoring
description: Monitor the health of Elasticsearch, Kibana, Logstash, and Beats from a single Kibana app.
links:
  - label: Kibana monitoring data
    url: /deploy-manage/monitor/stack-monitoring/kibana-monitoring-data.md
  - label: Configure Stack Monitoring
    url: /deploy-manage/monitor/stack-monitoring.md
  - label: Stack monitoring alerts
    url: /deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md
:::

:::{link-card}
title: Spaces and saved objects
description: Organize work into spaces. Manage dashboards, visualizations, and other Kibana objects, including export, import, and migration.
links:
  - label: Spaces
    url: /deploy-manage/manage-spaces.md
  - label: Manage saved objects
    url: /explore-analyze/find-and-organize/saved-objects.md
  - label: Tags
    url: /explore-analyze/find-and-organize/tags.md
:::
::::

::::{card-group}
:title: Explore, visualize, and analyze
:id: visualize

:::{link-card}
title: Discover
description: Browse documents, filter, and query your indices in real time.
links:
  - label: Discover overview
    url: /explore-analyze/discover.md
  - label: Get started with Discover
    url: /explore-analyze/discover/discover-get-started.md
  - label: Data views
    url: /explore-analyze/find-and-organize/data-views.md
  - label: Query with KQL
    url: /explore-analyze/query-filter/languages/kql.md
  - label: Query with ES|QL
    url: /explore-analyze/discover/try-esql.md
:::

:::{link-card}
title: Dashboards
description: Combine visualizations, controls, and context in an interactive view.
links:
  - label: Dashboards overview
    url: /explore-analyze/dashboards.md
  - label: Get started with Dashboards
    url: /explore-analyze/dashboards/tutorials.md
  - label: Ways to create a dashboard
    url: /explore-analyze/dashboards/building.md
  - label: Add controls
    url: /explore-analyze/visualize/dashboard-controls.md
  - label: Best practices
    url: /explore-analyze/dashboards/arrange-panels.md
:::

:::{link-card}
title: Visualizations
description: Create charts and visual panels with Lens, ES|QL, Vega, or a custom HTML panel.
links:
  - label: Visualizations overview
    url: /explore-analyze/visualize.md
  - label: Create visualizations
    url: /explore-analyze/visualize/lens.md
  - label: Create visualizations with ES|QL
    url: /explore-analyze/visualize/esorql.md
  - label: Vega
    url: /explore-analyze/visualize/custom-visualizations-with-vega.md
  - label: Custom panels
    url: /explore-analyze/visualize/custom-panels.md
:::

:::{link-card}
title: Machine learning
description: Detect anomalies, forecast trends, and run data frame analytics.
links:
  - label: Machine learning overview
    url: /explore-analyze/machine-learning/machine-learning-in-kibana.md
  - label: Get started with Machine learning
    url: /explore-analyze/machine-learning/anomaly-detection/ml-getting-started.md
  - label: Anomaly detection
    url: /explore-analyze/machine-learning/anomaly-detection.md
  - label: Data frame analytics
    url: /explore-analyze/machine-learning/data-frame-analytics.md
  - label: NLP
    url: /explore-analyze/machine-learning/nlp.md
:::
::::

::::{card-group}
:title: Alerting and incident response
:id: alerting

:::{link-card}
title: Kibana alerting
description: Detect conditions with built-in rule types and send notifications through connectors.
links:
  - label: Kibana alerting overview
    url: /explore-analyze/alerting/alerts.md
  - label: Get started with Kibana alerting
    url: /explore-analyze/alerting/alerts/alerting-getting-started.md
  - label: Create and manage rules
    url: /explore-analyze/alerting/alerts/create-manage-rules.md
  - label: View alerts
    url: /explore-analyze/alerting/alerts/view-alerts.md
:::

:::{link-card}
title: Alerting V2
description: Watch data with ES|QL rules, track alert episodes, and send notifications.
links:
  - label: Alerting V2 overview
    url: /explore-analyze/alerting/system-overview.md
  - label: Get started with Alerting V2
    url: /explore-analyze/alerting/experimental-alerting-system/get-started.md
  - label: Rules
    url: /explore-analyze/alerting/experimental-alerting-system/rules.md
  - label: Alert episodes
    url: /explore-analyze/alerting/experimental-alerting-system/alerts.md
:::

:::{link-card}
title: Alerting connectors
description: Send alerts and case updates to Slack, Jira, PagerDuty, and other incident-management tools.
links:
  - label: Alerting connectors overview
    url: kibana://reference/connectors-kibana/alerting-cases-connectors.md
  - label: Slack
    url: kibana://reference/connectors-kibana/slack-action-type.md
  - label: Jira
    url: kibana://reference/connectors-kibana/jira-action-type.md
  - label: PagerDuty
    url: kibana://reference/connectors-kibana/pagerduty-action-type.md
:::
::::

::::{card-group}
:title: AI and Workflows
:id: ai-automation

:::{link-card}
title: Agent Builder
description: Build custom AI agents that reason over your Elasticsearch data using LLMs and tools.
links:
  - label: Agent Builder overview
    url: /explore-analyze/ai-features/elastic-agent-builder.md
  - label: Get started with Agent Builder
    url: /explore-analyze/ai-features/agent-builder/get-started.md
  - label: Agents
    url: /explore-analyze/ai-features/agent-builder/agent-builder-agents.md
  - label: Custom tools
    url: /explore-analyze/ai-features/agent-builder/tools/custom-tools.md
:::

:::{link-card}
title: Workflows
description: Automate tasks with sequences that chain Kibana actions, HTTP calls, and AI agents.
links:
  - label: Workflows overview
    url: /explore-analyze/workflows.md
  - label: Get started with Workflows
    url: /explore-analyze/workflows/get-started.md
  - label: Use cases
    url: /explore-analyze/workflows/use-cases.md
  - label: Triggers
    url: /explore-analyze/workflows/triggers.md
:::

:::{link-card}
title: AI Agent chat
description: Chat with agents from the Kibana header to ask questions and take action on your data.
links:
  - label: AI Agent chat overview
    url: /explore-analyze/ai-features/agent-builder/chat.md
  - label: Get started with Agent Builder
    url: /explore-analyze/ai-features/agent-builder/get-started.md
  - label: Build dashboards in chat
    url: /explore-analyze/ai-features/agent-builder/agent-builder-dashboards-and-visualizations.md
  - label: Chat UI modes
    url: /explore-analyze/ai-features/agent-builder/standalone-and-flyout-modes.md
:::

:::{link-card}
title: Context connectors
description: Give agents access to external data and tools, such as Slack and GitHub.
links:
  - label: Slack
    url: kibana://reference/connectors-kibana/slack-v2-action-type.md
  - label: GitHub
    url: kibana://reference/connectors-kibana/github-action-type.md
  - label: Google Drive
    url: kibana://reference/connectors-kibana/google-drive-action-type.md
  - label: View all connectors
    url: kibana://reference/connectors-kibana.md
:::
::::

::::{card-group}
:title: Query data in Kibana
:id: query-data

:::{link-card}
title: Query languages
description: Languages you can use in Kibana to search, filter, and analyze Elasticsearch data.
links:
  - label: Kibana Query Language (KQL)
    url: /explore-analyze/query-filter/languages/kql.md
  - label: ES|QL
    url: /explore-analyze/query-filter/languages/esql-kibana.md
  - label: Query DSL
    url: /explore-analyze/query-filter/languages/querydsl.md
  - label: Elasticsearch SQL
    url: /explore-analyze/query-filter/languages/sql.md
:::

:::{link-card}
title: Developer tools
description: Run API requests, profile queries, and debug patterns and scripts from Kibana.
links:
  - label: Console
    url: /explore-analyze/query-filter/tools/console.md
  - label: Search Profiler
    url: /explore-analyze/query-filter/tools/search-profiler.md
  - label: Grok Debugger
    url: /explore-analyze/query-filter/tools/grok-debugger.md
  - label: Painless Lab
    url: /explore-analyze/scripting/painless-lab.md
:::

:::{link-card}
title: Search across clusters
description: Run a search across remote clusters or linked serverless projects.
links:
  - label: Cross-cluster search
    url: /explore-analyze/cross-cluster-search.md
  - label: Remote clusters
    url: /deploy-manage/remote-clusters.md
  - label: Cross-project search
    url: /explore-analyze/cross-project-search.md
  - label: Compare CCS and CPS
    url: /explore-analyze/cross-project-search/cps-compared-to-ccs.md
:::
::::

::::{card-group}
:title: Secure Kibana
:id: security

:::{link-card}
title: Authenticate users
links:
  - label: Kibana authentication (SSO, SAML, OIDC)
    url: /deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md
  - label: User roles
    url: /deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md
:::

:::{link-card}
title: Authorize access
links:
  - label: Kibana privileges
    url: /deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md
  - label: Spaces
    url: /deploy-manage/manage-spaces.md
:::

:::{link-card}
title: Protect data and audit
links:
  - label: Secure saved objects
    url: /deploy-manage/security/secure-saved-objects.md
  - label: Kibana and Elasticsearch mutual TLS
    url: /deploy-manage/security/kibana-es-mutual-tls.md
  - label: Enable audit logging
    url: /deploy-manage/security/logging-configuration/enabling-audit-logs.md
:::
::::

::::{card-group}
:title: Troubleshoot
:id: troubleshoot

:::{link-card}
title: Diagnose common issues
links:
  - label: Kibana troubleshooting
    url: /troubleshoot/kibana.md
  - label: Alerts
    url: /troubleshoot/kibana/alerts.md
:::

:::{link-card}
title: Capture diagnostics
links:
  - label: Capture Kibana diagnostics
    url: /troubleshoot/kibana/capturing-diagnostics.md
  - label: Server logs
    url: /troubleshoot/kibana/using-kibana-server-logs.md
:::
::::

::::{card-group}
:title: Reference
:id: reference

:::{link-card}
title: Configuration and settings
description: All kibana.yml settings and UI-configurable advanced settings.
links:
  - label: Configuration reference
    url: kibana://reference/configuration-reference.md
  - label: General
    url: kibana://reference/configuration-reference/general-settings.md
  - label: Alerting
    url: kibana://reference/configuration-reference/alerting-settings.md
  - label: Security
    url: kibana://reference/configuration-reference/security-settings.md
  - label: Advanced settings (UI)
    url: kibana://reference/advanced-settings.md
:::

:::{link-card}
title: Release notes
description: What's new, deprecated, and fixed in each Kibana release.
links:
  - label: Kibana
    url: kibana://release-notes/index.md
  - label: Known issues
    url: kibana://release-notes/known-issues.md
  - label: Breaking changes
    url: kibana://release-notes/breaking-changes.md
  - label: Deprecations
    url: kibana://release-notes/deprecations.md
:::

:::{link-card}
title: Related release notes
description: Release notes for the rest of the Elastic Stack and solutions.
links:
  - label: Elasticsearch
    url: elasticsearch://release-notes/index.md
  - label: Security
    url: /release-notes/elastic-security/index.md
  - label: Observability
    url: /release-notes/elastic-observability/index.md
  - label: Serverless
    url: /release-notes/elastic-cloud-serverless/index.md
:::

::::
:::::
