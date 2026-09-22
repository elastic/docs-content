# Docs triage instructions

These instructions tell TriageBot which of this repository's existing labels applies when. They
never add labels to the menu. Apply only labels that already exist in this repository.

## Team ownership

This repository routes issues to exactly three team labels:

- `Team:SKI`
- `Team:Admin`
- `Team:Developer`

Every other `Team:` label in this repository is retired. `Team:Experience`, `Team:Ingest`,
`Team:DocsEng`, `Team:Projects`, `Team:Platform`, `Team:Search`, and
`Team:Docs Visualizations & Analysis` still appear in the label menu because older issues carry
them. Never select a retired team label. Select at most one team label.

| Team label | Owns | Keywords and paths |
|---|---|---|
| `Team:SKI` | Kibana, Observability, Security, and data ingestion docs | Kibana, dashboards, visualizations, Discover, Lens, maps, Canvas, alerting, rules, cases; Observability, APM, OpenTelemetry, synthetics, SLOs; Security, SIEM, endpoint security, detection rules, security analytics; Fleet, Elastic Agent, Beats, Logstash, integrations, data streams. Paths: `explore-analyze/` (default), `manage-data/ingest/` (except for `manage-data/ingest/ingesting-data-from-applications`, `manage-data/ingest/sample-data`, and `manage-data/ingest/transform-enrich`), `solutions/observability/`, `solutions/security/`, `reference/apm-agents/`, `reference/fleet/`, `reference/ingestion-tools/`, `reference/kibana/`, `reference/observability/`, `reference/security/`, `troubleshoot/ingest/`, `troubleshoot/observability/`, `troubleshoot/security/`, `release-notes/elastic-observability/`, `release-notes/elastic-security/` |
| `Team:Admin` | Cluster administration, data management, deployment docs | Cluster management, index management, authentication, roles, API keys, network security, cluster security, snapshots, ILM, data lifecycle, CCR, licensing, subscriptions, upgrades, stack monitoring, Elastic Cloud, ECH, ECE, ECK, serverless deployment, ingest pipelines, ingest node, ingest processors, enrich processor. Elasticsearch cluster, node, snapshot, security, and index management APIs, including cat APIs and stats APIs. Paths: `deploy-manage/`, `cloud-account/`, `manage-data/` (except `manage-data/ingest/`), `serverless/`, `explore-analyze/scripting/`, `troubleshoot/deployments/`, `troubleshoot/elasticsearch/`, `troubleshoot/kibana/` |
| `Team:Developer` | Elasticsearch developer and Search solution docs | Elasticsearch search, query, inference, and ML APIs; ES\|QL, query DSL, search features, relevance, vector search, semantic search, inference APIs, machine learning, transforms, connectors, clients, search applications, cross-cluster search. Paths: `solutions/search/`, `reference/elasticsearch-clients/`, `reference/machine-learning/`, `explore-analyze/ai-features/agent-builder/`, `explore-analyze/cross-cluster-search/`, `explore-analyze/cross-project-search/`, `explore-analyze/transforms/`, `manage-data/data-store`, `manage-data/ingest/ingesting-data-from-applications`, `manage-data/ingest/sample-data` |

### Resolving CODEOWNERS entries

`.github/CODEOWNERS` names GitHub teams, not labels. Resolve them with this table:

| CODEOWNERS team | Team label |
|---|---|
| `@elastic/ski-docs` | `Team:SKI` |
| `@elastic/admin-docs` | `Team:Admin` |
| `@elastic/developer-docs` | `Team:Developer` |
| `@elastic/docs` | none — omit the team label |
| `@elastic/doc-leads` | none — omit the team label |
| `@elastic/docs-engineering` | none — omit the team label |
| `@elastic/core-docs` | none — omit the team label |
| `@elastic/docs-serverless-release-team` | none — omit the team label |

An issue that resolves to a team with no label gets no team label at all. Never substitute a
retired label such as `Team:DocsEng` or `Team:Projects`. The issue still gets `triaged`, and a
missing team label is not a reason to call the issue not routable.

Docs tooling, build, CI, and website-rendering issues belong to `@elastic/docs-engineering`, so
they get no team label. Get-started and content-strategy issues belong to `@elastic/core-docs`,
so they get no team label either.

### Shared ownership

Some paths have two owners. For example, `explore-analyze/machine-learning/` is owned by
`@elastic/developer-docs` and `@elastic/ski-docs`, and `troubleshoot/monitoring/` is owned by
`@elastic/admin-docs` and `@elastic/ski-docs`. Pick the single team whose keywords best match the
issue content. Add `cross-team` only when two teams clearly own the affected area and you cannot
pick one.

`manage-data/ingest/transform-enrich` has mixed ownership. Ingest pipelines, ingest processors,
and enrich processor content is ES Foundations and belongs to `Team:Admin`. Logstash pipeline
content belongs to `Team:SKI`. Use keyword matching to pick the right team for issues under this
path.

### Elasticsearch API routing

Issues about Elasticsearch API documentation, including the API reference at
`elastic.co/docs/api/doc/elasticsearch/`, should be routed based on the feature area the API
serves, not defaulted to a single team. Match the API to the team that owns the underlying
feature:

- Cluster, node, snapshot, security, index lifecycle, and index management APIs → `Team:Admin`
- Search, query, inference, ML, and transform APIs → `Team:Developer`
- Fleet and Elastic Agent APIs → `Team:SKI`

When the feature area is unclear, add `human-needed` instead of guessing.
