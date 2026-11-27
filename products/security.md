---
layout: hub
navigation_title: Elastic Security
description: Elastic Security documentation. Detect, investigate, and respond to threats with SIEM, endpoint protection, cloud security, and AI features that help you work through alerts.
products:
  - id: security
---

:::{hero}
:icon: security
:title: Elastic Security documentation hub
:description: Detect, investigate, and respond to threats across your hosts, cloud services, and networks. Elastic Security brings SIEM, endpoint protection, and cloud security together, with AI features that help you work through alerts.
:::

:::{on-this-page}
:::

:::{get-started}
title: Get started with Elastic Security
steps:
  - title: Run Elastic Security
    options:
      - label: Try for free on Elastic Cloud
        description: Create an Elastic Security Serverless project in a few minutes with no setup needed.
        url: https://cloud.elastic.co/serverless-registration?onboarding_token=security
        url-label: Start a free trial
      - label: Run locally
        description: Spin up Elasticsearch and Kibana on your machine for development with `start-local`.
        code: curl -fsSL https://elastic.co/start-local | sh
        language: sh
  - title: Add your data
    description: Collect security data with an Elastic integration, or build a custom one with Automatic Import.
    link: /solutions/security/get-started/ingest-data-to-elastic-security.md
    link-label: See ingest options
  - title: Turn on detections
    description: Install Elastic prebuilt rules to start finding threats in your data.
    link: /solutions/security/detect-and-alert/install-prebuilt-rules.md
    link-label: Install prebuilt rules
  - title: Follow a quickstart
    description: Complete a core task for SIEM, endpoint security, or cloud security.
    link: /solutions/security/get-started/quickstarts.md
    link-label: Browse quickstarts
:::

:::{whats-new}
:product: security
:::

::::{card-group}
:title: Elastic Security capabilities
:id: capabilities
:intro: Use these capabilities together or start with one. They all run on Elasticsearch and Kibana, so you can search, correlate, and visualize your security data in one place.

:::{link-card}
title: SIEM
description: Detect threats with prebuilt and custom rules, then triage and investigate the alerts.
links:
  - label: Get started with SIEM
    url: /solutions/security/get-started/get-started-detect-with-siem.md
  - label: Prebuilt rules
    url: /solutions/security/detect-and-alert/prebuilt-rules.md
  - label: Author rules
    url: /solutions/security/detect-and-alert/author-rules.md
  - label: Manage alerts
    url: /solutions/security/detect-and-alert/manage-detection-alerts.md
  - label: Cases
    url: /solutions/security/investigate/security-cases.md
:::

:::{link-card}
title: Endpoint security
description: Prevent malware, ransomware, and malicious behavior on your hosts with Elastic Defend.
links:
  - label: Get started with endpoint security
    url: /solutions/security/get-started/get-started-endpoint-security.md
  - label: Install Elastic Defend
    url: /solutions/security/configure-elastic-defend/install-elastic-defend.md
  - label: Elastic Defend policies
    url: /solutions/security/manage-elastic-defend/policies.md
  - label: Response actions
    url: /solutions/security/endpoint-response-actions.md
  - label: Isolate a host
    url: /solutions/security/endpoint-response-actions/isolate-host.md
:::

:::{link-card}
title: Cloud posture and vulnerability management
description: Find misconfigurations in cloud accounts and Kubernetes clusters, and vulnerabilities in cloud VMs.
links:
  - label: Get started with cloud security
    url: /solutions/security/get-started/get-started-cloud-security.md
  - label: Cloud security overview
    url: /solutions/security/cloud.md
  - label: CSPM
    url: /solutions/security/cloud/cloud-security-posture-management.md
  - label: KSPM
    url: /solutions/security/cloud/kubernetes-security-posture-management.md
  - label: CNVM
    url: /solutions/security/cloud/cloud-native-vulnerability-management.md
:::

:::{link-card}
title: Cloud workload protection
description: Protect Linux VMs and Kubernetes containers while they run.
links:
  - label: Cloud workload protection overview
    url: /solutions/security/manage/manage-cloud-workload-protection.md
  - label: Protect Linux VMs
    url: /solutions/security/cloud/cloud-workload-protection-for-vms.md
  - label: Protect Kubernetes containers
    url: /solutions/security/cloud/d4c/d4c-overview.md
  - label: Get started with Kubernetes workload protection
    url: /solutions/security/cloud/d4c/get-started-with-d4c.md
:::

:::{link-card}
title: AI-assisted operations
description: Triage alerts, investigate attacks, and write detection rules with AI.
links:
  - label: AI in Elastic Security
    url: /solutions/security/ai.md
  - label: Agent Builder
    url: /solutions/security/ai/agent-builder/agent-builder.md
  - label: Attack Discovery
    url: /solutions/security/ai/attack-discovery/index.md
  - label: Security use cases for Agent Builder
    url: /solutions/security/ai/agent-builder/skills-use-cases.md
  - label: Set up AI features
    url: /solutions/security/ai/set-up-ai-features.md
:::

:::{link-card}
title: Migrate from another SIEM
description: Translate your detection rules and dashboards, and bring in data that has no integration.
links:
  - label: Automatic Migration
    url: /solutions/security/get-started/automatic-migration.md
  - label: Automatic Import
    url: /solutions/security/get-started/automatic-import.md
  - label: Ingest third-party security data
    url: /solutions/security/integrations/ingest-third-party-security-data.md
:::
::::

:::::{explore}
:id: explore
:title: Explore Elastic Security docs
:mode: first
:intro: Find the page you need, whether you're tuning a detection rule, responding to an attack, or managing endpoints.

::::{card-group}
:title: Quick links
:id: quick-links

:::{link-card}
title: Find your way around
links:
  - label: Elastic Security overview
    url: /solutions/security.md
  - label: The Elastic Security UI
    url: /solutions/security/get-started/elastic-security-ui.md
  - label: Requirements
    url: /solutions/security/get-started/elastic-security-requirements.md
  - label: Serverless feature tiers
    url: /solutions/security/security-serverless-feature-tiers.md
:::

:::{link-card}
title: Release notes
links:
  - label: Elastic Security
    url: /release-notes/elastic-security/index.md
  - label: Serverless
    url: /release-notes/elastic-cloud-serverless/index.md
  - label: Known issues
    url: /release-notes/elastic-security/known-issues.md
  - label: Breaking changes
    url: /release-notes/elastic-security/breaking-changes.md
:::

:::{link-card}
title: APIs
links:
  - label: Elastic Security APIs
    url: /solutions/security/apis.md
  - label: Detections API
    url: https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-detections-api
  - label: Endpoint management API
    url: https://www.elastic.co/docs/api/doc/kibana/group/endpoint-security-endpoint-management-api
  - label: Serverless Kibana API
    url: https://www.elastic.co/docs/api/doc/serverless
:::

:::{link-card}
title: Reference
links:
  - label: Prebuilt detection rules reference
    url: detection-rules://index.md
  - label: Elastic Defend integration
    url: integration-docs://reference/endpoint/index.md
  - label: Elastic Common Schema (ECS)
    url: ecs://reference/index.md
:::
::::
:::::

:::::{explore}
:id: use-security
:title: Use Elastic Security
:level: 3
:intro: Detect threats, respond to alerts, investigate incidents, and hunt across your data.

::::{card-group}
:title: Detect and alert
:id: detect

:::{link-card}
title: Prebuilt rules
links:
  - label: About prebuilt rules
    url: /solutions/security/detect-and-alert/prebuilt-rules.md
  - label: Install prebuilt rules
    url: /solutions/security/detect-and-alert/install-prebuilt-rules.md
  - label: Update prebuilt rules
    url: /solutions/security/detect-and-alert/update-prebuilt-rules.md
  - label: Customize prebuilt rules
    url: /solutions/security/detect-and-alert/customize-prebuilt-rules.md
  - label: MITRE ATT&CK coverage
    url: /solutions/security/detect-and-alert/mitre-attack-coverage.md
:::

:::{link-card}
title: Author rules
links:
  - label: Author rules overview
    url: /solutions/security/detect-and-alert/author-rules.md
  - label: Choose the right rule type
    url: /solutions/security/detect-and-alert/choose-the-right-rule-type.md
  - label: Rule types
    url: /solutions/security/detect-and-alert/rule-types.md
  - label: ES|QL rules
    url: /solutions/security/detect-and-alert/esql.md
  - label: Validate and test rules
    url: /solutions/security/detect-and-alert/validate-and-test-rules.md
:::

:::{link-card}
title: Manage and monitor rules
links:
  - label: Manage detection rules
    url: /solutions/security/detect-and-alert/manage-detection-rules.md
  - label: Monitor rule executions
    url: /solutions/security/detect-and-alert/monitor-rule-executions.md
  - label: Fill rule gaps
    url: /solutions/security/detect-and-alert/fill-rule-gaps.md
  - label: Rule changes history
    url: /solutions/security/detect-and-alert/view-rule-changes-history.md
:::

:::{link-card}
title: Reduce noise
links:
  - label: Reduce noise and false positives
    url: /solutions/security/detect-and-alert/reduce-noise-and-false-positives.md
  - label: Tune detection rules
    url: /solutions/security/detect-and-alert/tune-detection-rules.md
  - label: Rule exceptions
    url: /solutions/security/detect-and-alert/rule-exceptions.md
  - label: Alert suppression
    url: /solutions/security/detect-and-alert/alert-suppression.md
:::
::::

::::{card-group}
:title: Respond and contain
:id: respond

:::{link-card}
title: Alerts
links:
  - label: Manage detection alerts
    url: /solutions/security/detect-and-alert/manage-detection-alerts.md
  - label: View alert details
    url: /solutions/security/detect-and-alert/view-detection-alert-details.md
  - label: Visualize alerts
    url: /solutions/security/detect-and-alert/visualize-detection-alerts.md
:::

:::{link-card}
title: Endpoint response actions
links:
  - label: Response actions overview
    url: /solutions/security/endpoint-response-actions.md
  - label: Isolate a host
    url: /solutions/security/endpoint-response-actions/isolate-host.md
  - label: Automated response actions
    url: /solutions/security/endpoint-response-actions/automated-response-actions.md
  - label: Third-party response actions
    url: /solutions/security/endpoint-response-actions/third-party-response-actions.md
  - label: Response actions history
    url: /solutions/security/endpoint-response-actions/response-actions-history.md
:::
::::

::::{card-group}
:title: Investigate
:id: investigate

:::{link-card}
title: Investigation tools
links:
  - label: Timeline
    url: /solutions/security/investigate/timeline.md
  - label: Visual event analyzer
    url: /solutions/security/investigate/visual-event-analyzer.md
  - label: Session View
    url: /solutions/security/investigate/session-view.md
  - label: Indicators of compromise
    url: /solutions/security/investigate/indicators-of-compromise.md
  - label: Cases
    url: /solutions/security/investigate/security-cases.md
:::

:::{link-card}
title: Query and explore data
links:
  - label: Explore security data in Discover
    url: /solutions/security/investigate/discover-security.md
  - label: ES|QL for security
    url: /solutions/security/esql-for-security.md
  - label: Threat hunting with ES|QL
    url: /solutions/security/esql-for-security/esql-threat-hunting-tutorial.md
  - label: Explore host, user, and network data
    url: /solutions/security/advanced-entity-analytics/explore.md
:::

:::{link-card}
title: Osquery
links:
  - label: Osquery overview
    url: /solutions/security/investigate/osquery.md
  - label: Run Osquery from alerts
    url: /solutions/security/investigate/run-osquery-from-alerts.md
  - label: Add Osquery response actions
    url: /solutions/security/investigate/add-osquery-response-actions.md
  - label: Examine Osquery results
    url: /solutions/security/investigate/examine-osquery-results.md
:::
::::

::::{card-group}
:title: Hunt and assess posture
:id: hunt

:::{link-card}
title: Dashboards
links:
  - label: Dashboards overview
    url: /solutions/security/dashboards.md
  - label: Overview dashboard
    url: /solutions/security/dashboards/overview-dashboard.md
  - label: Detection & Response dashboard
    url: /solutions/security/dashboards/detection-response-dashboard.md
  - label: Data Quality dashboard
    url: /solutions/security/dashboards/data-quality-dashboard.md
:::

:::{link-card}
title: Cloud security posture
links:
  - label: Cloud security overview
    url: /solutions/security/cloud.md
  - label: CSPM findings
    url: /solutions/security/cloud/findings-page.md
  - label: KSPM findings
    url: /solutions/security/cloud/findings-page-2.md
  - label: CNVM findings
    url: /solutions/security/cloud/findings-page-3.md
  - label: Asset discovery
    url: /solutions/security/cloud/asset-disc.md
:::

:::{link-card}
title: Entity analytics
links:
  - label: Entity analytics overview
    url: /solutions/security/advanced-entity-analytics.md
  - label: Entity store
    url: /solutions/security/advanced-entity-analytics/entity-store.md
  - label: Entity risk scoring
    url: /solutions/security/advanced-entity-analytics/entity-risk-scoring.md
  - label: Privileged user monitoring
    url: /solutions/security/advanced-entity-analytics/privileged-user-monitoring.md
  - label: Behavioral detections
    url: /solutions/security/advanced-entity-analytics/advanced-behavioral-detections.md
:::
::::

::::{card-group}
:title: AI-assisted operations
:id: ai

:::{link-card}
title: Agent Builder
links:
  - label: Agent Builder for Elastic Security
    url: /solutions/security/ai/agent-builder/agent-builder.md
  - label: Agents, skills, and tools
    url: /solutions/security/ai/agent-builder/skills-model.md
  - label: Security use cases
    url: /solutions/security/ai/agent-builder/skills-use-cases.md
  - label: Security skills reference
    url: /explore-analyze/ai-features/agent-builder/builtin-skills-reference.md#security-skills
:::

:::{link-card}
title: Attack Discovery
links:
  - label: Attack Discovery overview
    url: /solutions/security/ai/attack-discovery/index.md
  - label: Run Attack Discovery
    url: /solutions/security/ai/attack-discovery/run-attack-discovery.md
  - label: Triage findings
    url: /solutions/security/ai/attack-discovery/triage-attack-discovery-findings.md
  - label: Manage saved discoveries
    url: /solutions/security/ai/attack-discovery/manage-saved-discoveries.md
:::

:::{link-card}
title: Set up AI
links:
  - label: Set up AI features
    url: /solutions/security/ai/set-up-ai-features.md
  - label: LLM performance matrix
    url: /solutions/security/ai/large-language-model-performance-matrix.md
  - label: AI use cases
    url: /solutions/security/ai/use-cases.md
:::
::::

::::{card-group}
:title: AlertZero
:id: alertzero

:::{link-card}
title: Work with AlertZero
links:
  - label: AlertZero overview
    url: /solutions/security/alertzero/index.md
  - label: Set up AlertZero
    url: /solutions/security/alertzero/set-up-alertzero.md
  - label: Work in AlertZero
    url: /solutions/security/alertzero/work-in-alertzero.md
  - label: Manage AlertZero
    url: /solutions/security/alertzero/manage-alertzero.md
:::
::::
:::::

:::::{explore}
:id: set-up-security
:title: Set up and manage Elastic Security
:level: 3
:intro: Deploy Elastic Security, bring in your data, and manage endpoints, access, and settings.

::::{card-group}
:title: Set up
:id: set-up

:::{link-card}
title: Deploy
links:
  - label: Set up Elastic Security
    url: /solutions/security/set-up.md
  - label: Create a Serverless project
    url: /deploy-manage/deploy/elastic-cloud/create-serverless-project.md
  - label: Create a Cloud Hosted deployment
    url: /deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md
  - label: Self-managed deployments
    url: /deploy-manage/deploy/self-managed.md
:::

:::{link-card}
title: Elastic Defend
links:
  - label: Configure Elastic Defend
    url: /solutions/security/configure-elastic-defend.md
  - label: Elastic Defend requirements
    url: /solutions/security/configure-elastic-defend/elastic-defend-requirements.md
  - label: Install Elastic Defend
    url: /solutions/security/configure-elastic-defend/install-elastic-defend.md
  - label: Air-gapped environments
    url: /solutions/security/configure-elastic-defend/configure-offline-endpoints-air-gapped-environments.md
:::

:::{link-card}
title: Cloud security
links:
  - label: Set up cloud security
    url: /solutions/security/set-up/set-up-cloud-security.md
  - label: CSPM for AWS
    url: /solutions/security/cloud/get-started-with-cspm-for-aws.md
  - label: CSPM for GCP
    url: /solutions/security/cloud/get-started-with-cspm-for-gcp.md
  - label: CSPM for Azure
    url: /solutions/security/cloud/get-started-with-cspm-for-azure.md
  - label: KSPM
    url: /solutions/security/cloud/get-started-with-kspm.md
:::

:::{link-card}
title: Feature requirements
links:
  - label: Entity analytics requirements
    url: /solutions/security/advanced-entity-analytics/entity-analytics-requirements.md
  - label: Machine learning job and rule requirements
    url: /solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md
  - label: Turn on detections
    url: /solutions/security/detect-and-alert/turn-on-detections.md
:::
::::

::::{card-group}
:title: Ingest data
:id: ingest

:::{link-card}
title: Bring in security data
links:
  - label: Ingest data
    url: /solutions/security/get-started/ingest-data-to-elastic-security.md
  - label: Third-party security data
    url: /solutions/security/integrations/ingest-third-party-security-data.md
  - label: Automatic Import
    url: /solutions/security/get-started/automatic-import.md
  - label: Threat intelligence integrations
    url: /solutions/security/get-started/enable-threat-intelligence-integrations.md
:::
::::

::::{card-group}
:title: Manage
:id: manage

:::{link-card}
title: Manage Elastic Defend
links:
  - label: Manage Elastic Defend
    url: /solutions/security/manage-elastic-defend.md
  - label: Endpoints
    url: /solutions/security/manage-elastic-defend/endpoints.md
  - label: Configure an integration policy
    url: /solutions/security/configure-elastic-defend/configure-an-integration-policy-for-elastic-defend.md
  - label: Endpoint artifacts
    url: /solutions/security/manage-elastic-defend/endpoint-artifacts.md
  - label: Automatic troubleshooting
    url: /solutions/security/manage-elastic-defend/automatic-troubleshooting.md
:::

:::{link-card}
title: Access control
links:
  - label: Access control overview
    url: /solutions/security/manage/access-control.md
  - label: Elastic Security Kibana privileges
    url: /solutions/security/manage/security-kibana-privileges.md
  - label: Detections privileges
    url: /solutions/security/detect-and-alert/detections-privileges.md
  - label: Elastic Defend feature privileges
    url: /solutions/security/configure-elastic-defend/elastic-defend-feature-privileges.md
:::

:::{link-card}
title: Workspace settings
links:
  - label: Configure workspace settings
    url: /solutions/security/manage/configure-workspace-settings.md
  - label: Spaces
    url: /solutions/security/get-started/spaces-elastic-security.md
  - label: Data views
    url: /solutions/security/get-started/data-views-elastic-security.md
  - label: Runtime fields
    url: /solutions/security/get-started/create-runtime-fields-in-elastic-security.md
:::
::::

::::{card-group}
:title: Troubleshoot
:id: troubleshoot

:::{link-card}
title: Diagnose common issues
links:
  - label: Troubleshoot Elastic Security
    url: /troubleshoot/security.md
  - label: Detection rules
    url: /troubleshoot/security/detection-rules.md
  - label: Elastic Defend
    url: /troubleshoot/security/elastic-defend.md
  - label: Indicators of compromise
    url: /troubleshoot/security/indicators-of-compromise.md
:::
::::
:::::
