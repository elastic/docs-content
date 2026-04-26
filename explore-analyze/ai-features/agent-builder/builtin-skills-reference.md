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

## Platform skills

$$$agent-builder-visualization-creation-skill$$$ `visualization-creation` {applies_to}`stack: ga 9.4+`
:   Creates standalone or reusable Lens visualizations from index and field context. Use when a user asks for a chart, metric, trend, or breakdown visualization, or wants to update an existing one.

$$$agent-builder-graph-creation-skill$$$ `graph-creation` {applies_to}`stack: ga 9.4+`
:   Creates graph attachments by transforming relationship data into nodes and edges rendered inline in the conversation. Use for topology, dependency, or entity-link visualizations.

$$$agent-builder-dashboard-management-skill$$$ `dashboard-management` {applies_to}`stack: preview 9.4` {applies_to}`serverless: preview`
:   Composes and updates in-memory {{kib}} dashboards. Use when a user asks to find, create, or modify a dashboard, add or remove panels, or edit existing panel visualizations.

$$$agent-builder-streams-exploration-skill$$$ `streams-exploration` {applies_to}`stack: ga 9.4+`
:   Discovers, inspects, and queries {{es}} streams. Use when a user wants to list available streams, understand a stream's schema, check data quality or retention, or sample documents from a stream. This is a read-only skill: it cannot create, update, or delete streams or modify stream configuration.

## Observability skills
```{applies_to}
serverless:
  observability: ga
```

$$$agent-builder-observability-investigation-skill$$$ `observability.investigation` {applies_to}`stack: ga 9.4`
:   Answers observability questions and diagnoses issues across APM services and infrastructure. Use when a user asks about service health, error rates, latency, failed transactions, service topology, trace analysis, log patterns, SLO breaches, alert investigations, or general questions about services and their performance.

% $$$agent-builder-observability-rca-skill$$$ `observability.rca` {applies_to}`stack: preview 9.4`
% :   Performs structured root cause analysis for incidents, outages, errors, and service degradations. Use when a user asks why something is broken, slow, or failing; when an alert has fired; or when they need to trace a cascading failure across services.

% TODO: Confirm GA status for observability.rca — marked experimental in Kibana source.

## Security skills
```{applies_to}
serverless:
  security: ga
```

$$$agent-builder-entity-analytics-skill$$$ `entity-analytics` {applies_to}`stack: ga 9.4+`
:   Finds and investigates security entities including hosts, users, services, and generic entities. Analyzes entity risk scores, asset criticality, and historical behavior. Use to discover risky entities or profile a specific entity by ID.

$$$agent-builder-find-security-ml-jobs-skill$$$ `find-security-ml-jobs` {applies_to}`stack: ga 9.4+`
:   Investigates anomalous behavior detected by {{ml-app}} jobs, including abnormal access patterns, lateral movement, unexpected logins, suspicious domain activity, and large data transfers.

$$$agent-builder-threat-hunting-skill$$$ `threat-hunting` {applies_to}`stack: ga 9.4+`
:   Runs hypothesis-driven threat hunts using iterative ES|QL exploration. Covers IOC search, anomaly identification, baseline behavioral comparison, and lateral movement tracking.

$$$agent-builder-detection-rule-edit-skill$$$ `detection-rule-edit` {applies_to}`stack: ga 9.4+`
:   Creates and edits {{elastic-sec}} detection rules. Use when a user asks to build a rule from natural language or edit rule fields such as severity, tags, MITRE ATT&CK mappings, schedule, query, or index patterns.

## Elasticsearch skills
```{applies_to}
serverless:
  elasticsearch: ga
```

$$$agent-builder-search-catalog-ecommerce-skill$$$ `search.catalog-ecommerce` {applies_to}`stack: ga 9.4+`
:   Guides agents through building catalog and e-commerce search solutions on {{es}}.

$$$agent-builder-search-elasticsearch-onboarding-skill$$$ `search.elasticsearch-onboarding` {applies_to}`stack: ga 9.4+`
:   Guides developers through building a complete search experience on {{es}}, from understanding requirements and designing an index mapping to generating and testing API snippets in Dev Tools.

$$$agent-builder-search-hybrid-search-skill$$$ `search.hybrid-search` {applies_to}`stack: ga 9.4+`
:   Guides agents through building hybrid search solutions that combine keyword and semantic search.

$$$agent-builder-search-keyword-search-skill$$$ `search.keyword-search` {applies_to}`stack: ga 9.4+`
:   Guides agents through building keyword and full-text search solutions on {{es}}.

$$$agent-builder-search-rag-chatbot-skill$$$ `search.rag-chatbot` {applies_to}`stack: ga 9.4+`
:   Guides agents through building retrieval-augmented generation chatbot solutions on {{es}}.

$$$agent-builder-search-semantic-search-skill$$$ `search.semantic-search` {applies_to}`stack: ga 9.4+`
:   Guides agents through building semantic and vector search solutions on {{es}}.

$$$agent-builder-search-use-case-library-skill$$$ `search.use-case-library` {applies_to}`stack: ga 9.4+`
:   Presents a library of {{es}} use cases when users want to explore what they can build, need help identifying which category their project falls into, or are looking for inspiration. Covers product search, knowledge base search, AI assistants, recommendations, customer support, location-based search, log and event search, and vector database use cases.

$$$agent-builder-search-vector-database-skill$$$ `search.vector-database` {applies_to}`stack: ga 9.4+`
:   Guides agents through using {{es}} as a vector database.

## Related pages

- [Skills in {{agent-builder}}](skills.md)
- [Custom skills](custom-skills.md)
- [Skill creation guidelines](skill-creation-guidelines.md)
- [Tools in {{agent-builder}}](tools.md)
- [Built-in tools reference](tools/builtin-tools-reference.md)
- [Custom agents](custom-agents.md)
