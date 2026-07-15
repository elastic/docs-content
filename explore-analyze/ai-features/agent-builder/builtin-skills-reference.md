---
navigation_title: "Built-in skills"
description: "Reference of all built-in skills available in Elastic Agent Builder."
applies_to:
  stack: ga 9.4+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# {{agent-builder}} built-in skills reference

This page lists all built-in skills available in {{agent-builder}}. Skills give agents domain-specific knowledge and tools for common task types. Built-in skills are read-only: you can't modify or delete them.

:::{tip}
For an overview of how skills work in {{agent-builder}}, refer to [Skills in {{agent-builder}}](skills.md).
:::

## Availability

Skills are solution-scoped: the set of available built-in skills depends on your deployment type. Platform skills are available across all deployments. Observability, Security, and Elasticsearch skills are available in their respective serverless projects or solution views.

Some skills are in technical preview or require an [advanced setting](kibana://reference/advanced-settings.md#kibana-general-settings) or experimental feature flag to be turned on before they appear. These requirements are called out in each skill's entry.

## Platform skills

Platform skills are available across all deployment types. They cover core capabilities such as visualizations, dashboards, cases, alerting rules, streams, significant events, and workflows.

### Core skills

$$$agent-builder-visualization-creation-skill$$$ `visualization-creation` {applies_to}`stack: ga 9.4+`
:   Creates standalone or reusable Lens visualizations from index and field context. Use when a user asks for a chart, metric, trend, or breakdown visualization, or wants to update an existing one.

    :::{dropdown} Assigned tools
    `platform.core.generate_esql`, `platform.core.execute_esql`, `platform.core.create_visualization`

    :::

$$$agent-builder-graph-creation-skill$$$ `graph-creation` {applies_to}`stack: ga 9.4+`
:   Creates graph attachments by transforming relationship data into nodes and edges rendered inline in the conversation. Use for topology, dependency, or entity-link visualizations.

$$$agent-builder-dashboard-management-skill$$$ `dashboard-management` {applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview`
:   Composes and updates in-memory {{kib}} dashboards. Use when a user asks to find, create, or modify a dashboard, add or remove panels, or edit existing panel visualizations.

    :::{dropdown} Assigned tools
    A skill-scoped inline tool for generating and updating dashboards.

    :::

$$$agent-builder-discover-data-analysis-skill$$$ `discover-data-analysis` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Analyzes {{esql}} query results in {{kib}} **Discover**, identifying patterns, trends, and anomalies by running aggregation queries against the full dataset. The skill receives the current query, columns, sample rows, and time range as an attachment, then runs 2 to 3 focused aggregation queries, renders an inline visualization for the main finding, and proposes drill-down queries. When the active [context-aware profile](/explore-analyze/discover/discover-get-started.md#context-aware-discover) is logs, metrics, or traces, the skill receives shape-specific guidance. For example, it uses the {{esql}} `TS` source command for time series metrics.

    :::{dropdown} Assigned tools
    `platform.core.generate_esql`, `platform.core.execute_esql`, `platform.core.search`, `platform.core.list_indices`, `platform.core.product_documentation`, `platform.core.create_visualization`

    :::

    **How to activate:** Activates from the [standard activation methods](skills.md#how-skills-are-invoked) when the conversation is started from a Discover session tab that is in {{esql}} mode and has loaded results. The current query, columns, sample rows, and time range are automatically attached to the conversation, so the agent has the context it needs to run the analysis. Refer to [Analyze your data with AI](/explore-analyze/discover/discover-get-started.md#analyze-with-ai) for the full workflow.

$$$agent-builder-traces-skill$$$ `agent-builder-traces` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Answers questions about {{agent-builder}} OpenTelemetry (OTel) traces and activity, including token usage, model and provider breakdowns, conversation and agent latency, tool-call volume, and error rates, and can help build dashboards from that trace data. The skill queries the {{agent-builder}} OTel traces with {{esql}} and is part of the default Elastic AI Agent.

    :::{dropdown} Assigned tools
    `platform.core.execute_esql`, plus an internal {{esql}} generation tool scoped to trace data.

    :::

    **Prerequisites:** Controlled by the `agentBuilder:tracing:enabled` [advanced setting](kibana://reference/advanced-settings.md#kibana-general-settings), which is on by default.

### Cases and alerting

$$$agent-builder-cases-management-skill$$$ `cases-management` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Manages investigation and incident cases across {{elastic-sec}}, {{observability}}, and Stack Management. Covers creating, updating, searching, and enriching cases with comments, alerts, events, and observables such as indicators of compromise.

    :::{dropdown} Assigned tools
    `platform.core.cases`, `platform.core.cases.manage`, `platform.core.cases.attachments`, `platform.core.cases.observables`

    :::

$$$agent-builder-rule-management-skill$$$ `rule-management` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Composes, discovers, and modifies alerting rules and action policies from within a conversation.

    :::{dropdown} Assigned tools
    `platform.alerting.manage_rule`, `platform.alerting.manage_action_policy`

    :::

### Streams and significant events

$$$agent-builder-streams-management-skill$$$ `streams-management` {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga`
:   Explores and manages {{es}} streams. Use when a user mentions streams, stream names such as `logs.ecs` or `logs.otel`, data quality, processing pipelines, or ingestion failures. The skill can inspect stream definitions, schema, quality, lifecycle, and documents, and can modify processing, retention, partitions, field mappings, the failure store, and descriptions. This skill replaces the earlier `streams-exploration` skill and adds the ability to modify stream configuration.

    :::{dropdown} Assigned tools
    `platform.streams.inspect_streams`, `platform.streams.diagnose_stream`, `platform.streams.query_documents`, `platform.streams.design_pipeline`, `platform.streams.list_ilm_policies`, `platform.streams.update_stream`, `platform.streams.create_partition`, `platform.streams.delete_stream`

    :::

$$$agent-builder-streams-exploration-skill$$$ `streams-exploration` {applies_to}`stack: ga 9.4, removed 9.5`
:   Discovers, inspects, and queries {{es}} streams. Use when a user wants to list available streams, understand a stream's schema, check data quality or retention, or sample documents from a stream. This is a read-only skill: it cannot create, update, or delete streams or modify stream configuration. In 9.5, this skill is replaced by [`streams-management`](#agent-builder-streams-management-skill), which adds stream modification capabilities.

$$$agent-builder-significant-events-management-skill$$$ `significant-events-management` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Searches, creates, and updates significant events for Streams, with guidance to avoid duplicates and keep event lifecycle state accurate.

    :::{dropdown} Assigned tools
    `platform.sig_events.event_search`, `platform.sig_events.event_create`, `platform.sig_events.event_status_update`

    :::

$$$agent-builder-significant-events-onboarding-skill$$$ `significant-events-onboarding` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Interviews the user to build a mental model of their system for significant events analysis. Use when a user wants to describe their architecture, deployment infrastructure, observability setup, or other operational context that should be remembered for root cause analysis and remediation.

    :::{dropdown} Assigned tools
    Significant events memory tools for reading, writing, and searching the significant events knowledge base.

    :::

    **Prerequisites:** Significant events memory must be enabled in the deployment.

$$$agent-builder-knowledge-indicators-management-skill$$$ `knowledge-indicators-management` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Discovers and manages Streams Knowledge Indicators (KIs). Searches existing indicators to avoid duplicates and creates feature or query KIs with built-in confirmation.

    :::{dropdown} Assigned tools
    `platform.sig_events.ki_search`, `platform.sig_events.ki_feature_create`, `platform.sig_events.ki_query_create`

    :::

$$$agent-builder-ki-identification-management-skill$$$ `ki-identification-management` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Starts, monitors, and cancels stream KI identification background tasks. Triggers KI identification, surfaces a tracking link to the **Significant Events** page, checks task status and results, and cancels in-progress runs.

    :::{dropdown} Assigned tools
    Internal tools to start, check the status of, and cancel KI identification tasks.

    :::

$$$agent-builder-streams-investigation-management-skill$$$ `streams-investigation-management` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Triggers a root cause analysis workflow for an observability issue, significant event, or alert, checks the status of a running investigation, and summarizes the structured findings once complete. Use when a user asks to investigate an incident, error, or anomaly, optionally scoped to specific data streams.

    :::{dropdown} Assigned tools
    `platform.core.execute_workflow`, `platform.core.get_workflow_execution_status`, `platform.core.generate_esql`, `platform.core.execute_esql`, `platform.sig_events.event_investigation_attach`

    :::

$$$agent-builder-streams-gap-detection-skill$$$ `streams-gap-detection` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Audits the significant events memory knowledge base against a set of required knowledge dimensions and writes a structured gaps page that lists everything that is unknown, ambiguous, or missing.

    :::{dropdown} Assigned tools
    Significant events memory tools, `platform.sig_events.ki_search`, and `platform.streams.inspect_streams`.

    :::

    **Prerequisites:** Significant events memory must be enabled in the deployment.

### Workflows

$$$agent-builder-workflow-authoring-skill$$$ `workflow-authoring` {applies_to}`stack: ga 9.5+, preview =9.4` {applies_to}`serverless: ga`
:   Provides Elastic Workflows knowledge and discovery, covering YAML syntax, Liquid templating, trigger event schemas, step and connector inspection, validation error debugging, and execution debugging. Use this skill when a user asks how workflows work, requests advanced syntax help, debugs an execution, or asks to inspect the step, connector, or example libraries. This skill is not required to create, edit, or run workflows: the agent calls the workflow generation and execution tools directly.

    :::{dropdown} Assigned tools
    `platform.workflows.get_step_definitions`, `platform.workflows.get_trigger_definitions`, `platform.workflows.validate_workflow`, `platform.workflows.get_examples`, `platform.workflows.get_connectors`, `platform.workflows.workflow_execute_step`, `platform.core.generate_workflow`, `platform.core.execute_workflow`

    :::

    **Prerequisites:** [Elastic Workflows](/explore-analyze/workflows.md) enabled in the deployment, with the privileges required to create and run workflows.

    :::{dropdown} Behavior in 9.4
    In 9.4, this skill creates, modifies, and validates Elastic Workflows YAML definitions from natural language input. It covers step types, triggers, Liquid templating, connector integrations, and validation, and validates the generated or modified YAML before proposing the change so the user can accept or decline it. The `agentBuilder:experimentalFeatures` [advanced setting](kibana://reference/advanced-settings.md#kibana-general-settings) must be turned on for the skill to appear. **Assigned tools:** lookup tools (`platform.workflows.get_step_definitions`, `platform.workflows.get_trigger_definitions`, `platform.workflows.get_examples`, `platform.workflows.get_connectors`, `platform.workflows.validate_workflow`) and edit tools (`platform.workflows.workflow_set_yaml`, `platform.workflows.workflow_insert_step`, `platform.workflows.workflow_modify_step`, `platform.workflows.workflow_modify_step_property`, `platform.workflows.workflow_modify_property`, `platform.workflows.workflow_delete_step`).
    :::

    :::{note}
    Without this skill, the agent can still check the status of a workflow execution and resume a paused workflow that is waiting for human input, using the [`platform.core.get_workflow_execution_status`](tools/builtin-tools-reference.md) and [`platform.core.resume_workflow_execution`](tools/builtin-tools-reference.md) tools. To trigger a specific workflow from a conversation, configure a [workflow tool](tools/workflow-tools.md) and assign it to the agent.
    :::

### Agent and skill authoring

$$$agent-builder-skill-management-skill$$$ `skill-management` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Authors and edits {{agent-builder}} skills from a chat description. Use when a user asks to create, build, generate, design, or modify a skill, capability, or expertise area for an agent.

    :::{dropdown} Assigned tools
    Internal tools to list available tools and existing skills, and to propose, load, and patch a skill definition.

    :::

$$$agent-builder-connector-authoring-skill$$$ `connector-authoring` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Sets up a {{kib}} connector from chat. Use when a user wants to add, connect, set up, or integrate an external system such as GitHub, Slack, PagerDuty, or Notion so the agent can act on it. Also use when a user mentions giving the agent access to a tool, repository, or data source, even if they do not use the word connector.

    :::{dropdown} Assigned tools
    Internal tools to list connector types and to propose a connector.

    :::

## Observability skills
```{applies_to}
serverless:
  observability: ga
```

$$$agent-builder-observability-investigation-skill$$$ `observability.investigation` {applies_to}`stack: ga 9.4+`
:   Answers observability questions, lists and diagnoses observability alerts, and investigates service or infrastructure issues. Covers APM, logs, metrics, threshold, SLO burn rate, uptime and synthetics, and infrastructure alerts. Use when a user asks about alerts, service health, error rates, latency, failed transactions, topology, traces, log patterns, SLO breaches, or infrastructure issues.

    :::{dropdown} Assigned tools
    All [Observability tools](tools/builtin-tools-reference.md#observability-tools).

    :::

$$$agent-builder-observability-rca-skill$$$ `observability.rca` {applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview`
:   Performs structured root cause analysis for incidents, outages, errors, and service degradations. Use when a user asks why something is broken, failing, or slow, when an alert fires or an SLA is breached, when they need to understand what happened during an outage or performance regression, or when they need to trace a cascading failure across services.

    :::{dropdown} Assigned tools
    Observability log analysis tools, `platform.core.generate_esql`, `platform.core.execute_esql`, and significant events knowledge indicator search.

    :::

$$$agent-builder-observability-service-map-skill$$$ `observability.service-map` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Shows a service map when a user asks to see or visualize a service map, service topology, or service dependencies in an APM or observability context. Use for questions about how services connect or their upstream and downstream dependencies.

    :::{dropdown} Assigned tools
    `observability.get_service_topology`, `observability.get_services`

    :::

## Security skills
```{applies_to}
serverless:
  security: ga
```

$$$agent-builder-alert-analysis-skill$$$ `alert-analysis` {applies_to}`stack: ga 9.4+`
:   Investigates {{elastic-sec}} alerts and recommends a disposition. Fetches alert context, finds related alerts that share entities (`host.name`, `user.name`, `source.ip`, `destination.ip`), correlates with {{elastic-sec}} Labs threat intelligence, and assesses entity risk. Use when investigating a specific alert, triaging alert queues, or understanding alert context.

    :::{dropdown} Assigned tools
    `security.alerts`, `security.security_labs_search`, `security.entity_risk_score`

    :::

    **Prerequisites:** [Entity risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md) enabled so risk scores are available for involved hosts and users. To use threat intelligence correlation, install **Security Labs** documentation from [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).

    **How to activate:** In addition to the [standard activation methods](skills.md#how-skills-are-invoked), this skill activates automatically when you attach an alert from the alert flyout in {{elastic-sec}}, which provides the alert context the skill needs.

$$$agent-builder-entity-analytics-skill$$$ `entity-analytics` {applies_to}`stack: ga 9.4+`
:   Finds and investigates security entities including hosts, users, services, and generic entities. Analyzes entity risk scores, asset criticality, and historical behavior, including signals from Security {{ml-app}} anomaly detection jobs. Use to discover risky entities or profile a specific entity by ID.

    :::{dropdown} Assigned tools
    `security.get_entity`, `security.search_entities`

    :::

    {applies_to}`stack: ga 9.5+` From 9.5, the skill can also list watchlists to discover watchlist names and members (`security.list_watchlists`) and set entity asset criticality (`security.set_asset_criticality`).

    **Prerequisites:** [Entity risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md) enabled and the [entity store](/solutions/security/advanced-entity-analytics/entity-store.md) populated.

    **Related skills:** [`find-security-ml-jobs`](#agent-builder-find-security-ml-jobs-skill) for deeper investigation of anomalies surfaced during entity analysis. [`manage-watchlists`](#agent-builder-manage-watchlists-skill) to create and modify watchlists.

$$$agent-builder-entity-analytics-leads-skill$$$ `entity-analytics-leads` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Surfaces AI-generated threat hunting leads for security entities. Use when a user asks to review, list, show, triage, dismiss, or generate threat hunting leads, or wants to find proactive threat hunting opportunities surfaced from entity data.

    :::{dropdown} Assigned tools
    `security.list_leads`, `security.generate_leads`, `security.dismiss_lead`

    :::

$$$agent-builder-manage-watchlists-skill$$$ `manage-watchlists` {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga`
:   Manages Entity Analytics watchlists. Creates, updates, and deletes watchlists and adds or removes entity membership. Resolves watchlist names to IDs by discovering existing watchlists. All mutating actions require explicit user confirmation before running. For read-only questions about which watchlists exist, the [`entity-analytics`](#agent-builder-entity-analytics-skill) skill also applies.

    :::{dropdown} Assigned tools
    `security.list_watchlists`, `security.create_watchlist`, `security.update_watchlist`, `security.delete_watchlist`, `security.add_entities_to_watchlist`, `security.remove_entities_from_watchlist`

    :::

$$$agent-builder-find-security-ml-jobs-skill$$$ `find-security-ml-jobs` {applies_to}`stack: ga 9.4+`
:   Investigates atypical behavior detected by {{ml-app}} jobs, including unusual or first-time access patterns, access outside working hours, privileged accounts with unusual command patterns, logins from unexpected geographic locations, lateral movement, and large or unusual data transfers.

    :::{dropdown} Assigned tools
    `platform.core.execute_esql`, `platform.core.generate_esql`, `security.get_entity`, plus internal tools to discover Security {{ml-app}} jobs.

    :::

    **Prerequisites:** Relevant Security {{ml-app}} jobs installed and running. For guidance, refer to [Machine learning job and rule requirements](/solutions/security/advanced-entity-analytics/machine-learning-job-rule-requirements.md).

$$$agent-builder-threat-hunting-skill$$$ `threat-hunting` {applies_to}`stack: ga 9.4+`
:   Runs hypothesis-driven threat hunts using iterative {{esql}} exploration. Covers IOC search, anomaly identification, baseline behavioral comparison, lateral movement tracking, and converting hunt findings into actionable intelligence. Use when investigating suspected threats, running proactive hunts, or analyzing suspicious activity patterns.

    :::{dropdown} Assigned tools
    `platform.core.generate_esql`, `platform.core.execute_esql`, `platform.core.search`, `platform.core.list_indices`, `platform.core.get_index_mapping`, `platform.core.cases`

    :::

$$$agent-builder-detection-rule-edit-skill$$$ `detection-rule-edit` {applies_to}`stack: ga 9.4+`
:   Creates and edits {{elastic-sec}} detection rules. Supports {{esql}} rule type only. Use when a user asks to build a rule from natural language or edit rule fields such as severity, tags, MITRE ATT&CK mappings, schedule, or query.

    :::{dropdown} Assigned tools
    `security.create_detection_rule`, `security.security_labs_search`, `platform.core.generate_esql`, `platform.core.product_documentation`

    :::

    **Prerequisites:** To ground rule drafting in threat research, install **Security Labs** documentation from [**GenAI Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md).

    **How to activate:** This skill is attachment-driven and activates when a rule attachment is present in the conversation. You can start a rule attachment from the rule creation form, the rule details page, or by asking the agent to "create a detection rule" in chat. The skill creates the attachment and renders an **Apply to creation** or **Update rule** button so you can save the change to the rule form.

$$$agent-builder-recommend-prebuilt-rules-skill$$$ `recommend-prebuilt-rules` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Discovers and recommends Elastic prebuilt detection rules to install on the deployment. Handles install recommendations and browse or coverage questions about the installable catalog, filtered by tag, MITRE technique, rule type, integration, or keyword. This is a read-only skill.

    :::{dropdown} Assigned tools
    Internal tools to find prebuilt rules, read the user data inventory, inspect the installable catalog, and check installed rule MITRE coverage.

    :::

    **Prerequisites:** The `dexAiSkillRecommendPrebuiltRules` {{elastic-sec}} [experimental feature flag](kibana://reference/configuration-reference/security-solution-settings.md#experimental-features) must be enabled.

$$$agent-builder-find-security-rules-skill$$$ `find-security-rules` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Discovers, lists, ranks, and counts {{elastic-sec}} detection rules. Filters by tag, MITRE technique, severity, rule type, name, or enabled state. This is a read-only skill.

    :::{dropdown} Assigned tools
    `security.alerts`, plus internal tools to find rules and discover rule tags.

    :::

    **Prerequisites:** The `dexAiSkillFindRules` {{elastic-sec}} [experimental feature flag](kibana://reference/configuration-reference/security-solution-settings.md#experimental-features) must be enabled.

$$$agent-builder-pci-compliance-skill$$$ `pci-compliance` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Runs PCI DSS v4.0.1 compliance assessments with violation detection, confidence scoring, data quality preflight checks, and visual audit reporting. Use when a user asks about PCI compliance, PCI DSS requirements, compliance audits, or cardholder data security.

    :::{dropdown} Assigned tools
    `security.pci_scope_discovery`, `security.pci_compliance`, `security.pci_field_mapper`, `platform.core.generate_esql`, `platform.core.execute_esql`

    :::

    **Prerequisites:** The `pciComplianceAgentBuilder` {{elastic-sec}} [experimental feature flag](kibana://reference/configuration-reference/security-solution-settings.md#experimental-features) must be enabled.

$$$agent-builder-siem-readiness-skill$$$ `siem-readiness` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Assesses SIEM readiness across four dimensions: coverage (data ingested per category), quality (ECS field compatibility), continuity (ingest pipeline health), and retention (data retention compliance). Use when a user asks about SIEM health, readiness, data coverage, pipeline failures, ECS quality, or retention compliance.

    :::{dropdown} Assigned tools
    `security.siem_readiness.get_coverage`, `security.siem_readiness.get_quality`, `security.siem_readiness.get_continuity`, `security.siem_readiness.get_retention`

    :::

$$$agent-builder-automatic-troubleshooting-skill$$$ `automatic_troubleshooting` {applies_to}`stack: ga 9.5+, preview =9.4` {applies_to}`serverless: ga`
:   Diagnoses [{{elastic-defend}}](/solutions/security/configure-elastic-defend.md) endpoint configuration issues such as endpoints not reporting, policy response failures, agent enrollment problems, or incompatible antivirus software. Queries endpoint data, inspects package configuration, and produces structured findings with specific endpoint IDs and remediation steps.

    :::{dropdown} Assigned tools
    `platform.core.search`, `platform.core.get_document_by_id`, `platform.core.integration_knowledge`

    :::

    **Prerequisites:** [{{elastic-defend}}](/solutions/security/configure-elastic-defend.md) deployed and reporting.

    {applies_to}`stack: preview =9.4` In this version, the `automaticTroubleshootingSkill` [experimental feature flag](kibana://reference/configuration-reference/security-solution-settings.md#experimental-features) must be enabled for the skill to appear.

## Elasticsearch skills
```{applies_to}
serverless:
  elasticsearch: ga
```

$$$agent-builder-search-elasticsearch-onboarding-skill$$$ `search.elasticsearch-onboarding` {applies_to}`stack: ga 9.4+`
:   Guides developers through building a complete search experience on {{es}}, from understanding requirements and designing an index mapping to generating and testing API snippets in Dev Tools. Use for end-to-end onboarding rather than a single narrow API answer.

$$$agent-builder-search-elasticsearch-tutorial-skill$$$ `search.elasticsearch-tutorial` {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview`
:   Runs a topic-driven, hands-on {{es}} tutorial in the {{kib}} Dev Console. Use when a user asks you to walk them through, teach, or give a tutorial on an {{es}} or {{kib}} search concept such as mappings, analyzers, bool queries, `semantic_text`, kNN, reciprocal rank fusion (RRF), aggregations, ingest pipelines, or {{esql}}. Tutorials use sample data on isolated resources, present each step as a snippet to run in Dev Tools, and end with cleanup and pointers to documentation.

$$$agent-builder-search-keyword-search-skill$$$ `search.keyword-search` {applies_to}`stack: ga 9.4+`
:   Guides agents through building keyword and full-text search solutions on {{es}}. Use for text matching, filters, faceted search, autocomplete, or traditional search functionality.

$$$agent-builder-search-vector-hybrid-search-skill$$$ `search.vector-hybrid-search` {applies_to}`stack: ga 9.5+`
:   Guides agents through building vector search, hybrid search, and using {{es}} as a vector database. Covers `semantic_text`, `dense_vector`, embedding strategies, hybrid search that combines BM25 and kNN with reciprocal rank fusion (RRF), reranking, and production optimization. In 9.5, this skill consolidates the former `search.hybrid-search`, `search.semantic-search`, and `search.vector-database` skills.

$$$agent-builder-search-hybrid-search-skill$$$ `search.hybrid-search` {applies_to}`stack: ga 9.4, removed 9.5`
:   Guides agents through building hybrid search solutions that combine keyword and semantic search. In 9.5, this skill is consolidated into [`search.vector-hybrid-search`](#agent-builder-search-vector-hybrid-search-skill).

$$$agent-builder-search-semantic-search-skill$$$ `search.semantic-search` {applies_to}`stack: ga 9.4, removed 9.5`
:   Guides agents through building semantic and vector search solutions on {{es}}. In 9.5, this skill is consolidated into [`search.vector-hybrid-search`](#agent-builder-search-vector-hybrid-search-skill).

$$$agent-builder-search-vector-database-skill$$$ `search.vector-database` {applies_to}`stack: ga 9.4, removed 9.5`
:   Guides agents through using {{es}} as a vector database. In 9.5, this skill is consolidated into [`search.vector-hybrid-search`](#agent-builder-search-vector-hybrid-search-skill).

$$$agent-builder-search-rag-chatbot-skill$$$ `search.rag-chatbot` {applies_to}`stack: ga 9.4+`
:   Guides agents through building retrieval-augmented generation (RAG) chatbots and question-and-answer systems on {{es}}. Use when a developer wants to build a chatbot, question-and-answer system, or AI assistant that answers questions from their own data.

$$$agent-builder-search-catalog-ecommerce-skill$$$ `search.catalog-ecommerce` {applies_to}`stack: ga 9.4+`
:   Guides agents through building catalog and e-commerce search solutions on {{es}}. Use for product search, faceted navigation, autocomplete, "did you mean" suggestions, or shopping-oriented search experiences.

$$$agent-builder-search-use-case-library-skill$$$ `search.use-case-library` {applies_to}`stack: ga 9.4+`
:   Presents a library of {{es}} use cases when users want to explore what they can build, need help identifying which category their project falls into, or are looking for inspiration. Covers product search, knowledge base search, AI assistants, recommendations, customer support, location-based search, log and event search, and vector database use cases.

## Related pages

- [Skills in {{agent-builder}}](skills.md)
- [Custom skills](custom-skills.md)
- [Skill creation guidelines](skill-creation-guidelines.md)
- [Tools in {{agent-builder}}](tools.md)
- [Built-in tools reference](tools/builtin-tools-reference.md)
- [Custom agents](custom-agents.md)
