---
navigation_title: Assess your existing solution
description: Assess your existing solution and inventory the assets and compatibility requirements for a Serverless migration.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
type: how-to
---

# Assess your existing solution [migrate-to-serverless-assess]

**Serverless migration process**

:::{image} /deploy-manage/images/serverless-migration-navigation-grouped-assess.svg
:alt: Assess, create project, prepare and test, and switch to production. The preparation cycle runs from Prepare to Transfer data to Test and validate and back to Prepare. Assess is the current phase.
:::

Previous: [Migration overview](migrate-to-serverless.md) · Next: [Create project](migrate-to-serverless-create-project.md)

Understand what your solution needs and how you can reproduce it in {{serverless-short}} before preparing the destination.

## Identify your use cases and candidate project type [migrate-to-serverless-use-cases]

Start with how users and applications rely on the source deployment and the workflows the migration must preserve. Identify whether its workloads provide general search and analytics, vector search or AI retrieval, {{observability}}, {{elastic-sec}}, or a combination. Use the [project type comparison](serverless.md#get-started) to identify the candidate project type for each workload.

Classify each workload by its primary purpose, not by an individual feature or asset type. Embeddings, {{ml}}, {{fleet}}, {{agent}}, integrations, and alerting can support several use cases and do not determine the destination on their own.

## Inventory your assets [migrate-to-serverless-inventory]

Identify the data, configuration, integrations, applications, and external dependencies your solution uses. Review the inventory with the people who configure and use each part of the solution.

Focus on user-created resources and customizations, including direct changes to Elastic-managed assets. You generally do not need to inventory or transfer individual managed, system, or internal assets. The destination integrations and components recreate the resources they provide. Record the integrations and versions you use, and check each feature's migration guidance for exceptions.

The following checklist provides a broad reference to the asset types involved in a migration. Mark the items your solution uses and add any resources specific to your environment. The migration procedures and considerations for each asset type are described in [Prepare and test the destination](migrate-to-serverless-prepare.md). The labels indicate whether you can transfer an asset directly, need to adapt it, or must replace it because it is unavailable in {{serverless-short}}.

% TODO: Add migration procedures and local links for transforms, Watcher, SLOs, Synthetics monitors, reporting schedules, Streams, Attack Discovery, Endpoint artifacts, and network configuration. Keep these entries unlinked until their procedures are documented.

:::{dropdown} Data
- [ ] [Regular indices](migrate-to-serverless-transfer-data.md#migrate-to-serverless-regular-indices), including mappings and settings — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer documents and adapt settings or lifecycle configuration where needed**
- [ ] [Data streams and backing indices](migrate-to-serverless-transfer-data.md#migrate-to-serverless-data-streams), including the current write index — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer documents and adapt settings or lifecycle configuration where needed**
- [ ] [Index and data stream aliases](migrate-to-serverless-transfer-data.md), including filters and write targets — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Stored vectors and `semantic_text` data](migrate-to-serverless-transfer-data.md#migrate-to-serverless-transfer-considerations) — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Preserve embeddings and adapt mappings or inference references where needed**
- [ ] **Write patterns:** Identify indices and data streams that only append documents and those that also update or delete existing documents. Record which applications or jobs perform these operations and how frequently.
- [ ] **Stable historical data:** Identify indices and backing indices that no longer receive new documents, updates, or deletes and can be copied without reconciling later changes.

Use these patterns to plan your [data transfer](migrate-to-serverless-transfer-data.md): determine what you can copy during preparation and what needs a final copy after source changes stop, or a tested incremental synchronization procedure.
:::

:::{dropdown} Data structures and processing
- [ ] [Stored scripts and search templates](migrate-to-serverless-prepare.md#migrate-to-serverless-scripts) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [API-managed synonym sets](migrate-to-serverless-prepare.md#migrate-to-serverless-synonyms) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [File-based or index-time synonyms](migrate-to-serverless-prepare.md#migrate-to-serverless-synonyms) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with API-managed search-time synonym sets or redesign the analyzers**
- [ ] [Enrich policies and reference data](migrate-to-serverless-prepare.md#migrate-to-serverless-enrich) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Custom ingest pipelines and `@custom` extensions](migrate-to-serverless-prepare.md#migrate-to-serverless-pipelines), including referenced scripts, enrich policies, and inference endpoints — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Custom component templates](migrate-to-serverless-prepare.md#migrate-to-serverless-component-templates), including integration `@custom` components — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer compatible definitions, remove unsupported settings, and adapt lifecycle references**
- [ ] [Composable index templates](migrate-to-serverless-prepare.md#migrate-to-serverless-templates), including patterns, priorities, component order, and data stream configuration — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer compatible definitions, remove unsupported settings, and adapt lifecycle configuration**
- [ ] [Legacy index templates](migrate-to-serverless-prepare.md#migrate-to-serverless-legacy-templates) still in use — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with composable templates**
- [ ] [{{ilm-cap}} policies, data tiers, and lifecycle actions](migrate-to-serverless-prepare.md#migrate-to-serverless-lifecycle) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with data stream lifecycle or another retention design**
- [ ] Transforms and other custom processing resources
:::

:::{dropdown} Kibana objects and solution configuration
- [ ] [Spaces](migrate-to-serverless-prepare.md#migrate-to-serverless-spaces), including IDs, settings, and access requirements — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer compatible settings and recreate access**
- [ ] [Dashboards, visualizations, and maps](migrate-to-serverless-prepare.md#migrate-to-serverless-saved-objects) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Discover sessions, data views, saved queries, tags, and annotation groups](migrate-to-serverless-prepare.md#migrate-to-serverless-saved-objects) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Connectors](migrate-to-serverless-prepare.md#migrate-to-serverless-connectors), including IDs, secrets, and authorization — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer definitions and restore secrets or authorization**
- [ ] [Observability rules](migrate-to-serverless-prepare.md#migrate-to-serverless-observability-rules), including actions and referenced {{ml}} jobs — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Security detection rules](migrate-to-serverless-prepare.md#migrate-to-serverless-security-rules), including actions and referenced data views and {{ml}} jobs — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Rule exception lists](migrate-to-serverless-prepare.md#migrate-to-serverless-security-rules) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Value lists](migrate-to-serverless-prepare.md#migrate-to-serverless-security-rules) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer separately from detection rules**
- [ ] [Endpoint exceptions](migrate-to-serverless-prepare.md#migrate-to-serverless-security-rules) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer separately from detection rules**
- [ ] [Cases](migrate-to-serverless-prepare.md#migrate-to-serverless-cases), including comments, configuration, attachments, related alerts, and Timelines — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer supported content and recreate omitted configuration**
- [ ] [Maintenance windows](migrate-to-serverless-prepare.md#migrate-to-serverless-maintenance-windows), including schedules, recurrence, filters, and rule scope — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer schedules and filters, adapting removed rule-category restrictions where used**
- [ ] [User-managed workflows](migrate-to-serverless-prepare.md#migrate-to-serverless-workflows), including triggers, schedules, connectors, and dependencies — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] Watcher watches — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with {{kib}} alerting rules**
- [ ] SLOs
- [ ] Synthetics monitors
- [ ] Reporting schedules
- [ ] Streams
- [ ] Attack Discovery configuration
- [ ] Endpoint artifacts
:::

:::{dropdown} Security and access
- [ ] [Cloud organization users and project assignments](migrate-to-serverless-prepare.md#migrate-to-serverless-access) — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Recreate project assignments**
- [ ] [Custom roles](migrate-to-serverless-prepare.md#migrate-to-serverless-access) and their assignments — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Adapt privileges and recreate assignments**
- [ ] [Deployment-local users](migrate-to-serverless-prepare.md#migrate-to-serverless-access) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with organization users**
- [ ] [Authentication realms and role mappings](migrate-to-serverless-prepare.md#migrate-to-serverless-access) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with organization-level authentication**
- [ ] [API keys, service credentials, certificates, and secrets](migrate-to-serverless-prepare.md#migrate-to-serverless-access) — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Create destination credentials**
- [ ] Network policies, private connectivity, proxies, and allowlists — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Recreate for the destination**
- [ ] [Remote cluster connections and cross-cluster searches](migrate-to-serverless-prepare.md#migrate-to-serverless-remote-clusters) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with CPS only between compatible Serverless projects in the same organization**
- [ ] [Cross-cluster replication](migrate-to-serverless-prepare.md#migrate-to-serverless-remote-clusters) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Redesign replication-dependent workflows. CPS does not replicate data**
:::

:::{dropdown} Fleet and integrations
- [ ] [Integration packages and versions](migrate-to-serverless-prepare.md#migrate-to-serverless-integrations) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Install required packages**
- [ ] Direct modifications to managed integration assets — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Reapply through supported customization mechanisms**
- [ ] [{{fleet}} outputs and proxies](migrate-to-serverless-prepare.md#migrate-to-serverless-fleet), including defaults and external destinations — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Adapt destination URLs and restore credentials**
- [ ] [Agent policies](migrate-to-serverless-prepare.md#migrate-to-serverless-fleet), including settings and space assignments — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer compatible settings and update output and space references**
- [ ] [Integration policies](migrate-to-serverless-prepare.md#migrate-to-serverless-fleet), including enabled inputs, streams, and output assignments — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer input settings, adapt package or output references, and restore secrets**
- [ ] [Enrolled {{agent}}s](migrate-to-serverless-production.md#migrate-to-serverless-production-clients) — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Migrate or re-enroll agents during the production transition**
:::

:::{dropdown} AI and machine learning
- [ ] [Anomaly detection jobs and datafeeds](migrate-to-serverless-prepare.md#migrate-to-serverless-anomaly-jobs), including source indices and space assignments — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer configuration and rebuild learned model state**
- [ ] [{{ml-cap}} filter lists and calendars](migrate-to-serverless-prepare.md#migrate-to-serverless-anomaly-jobs), including scheduled events and job associations — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Data frame analytics jobs](migrate-to-serverless-prepare.md#migrate-to-serverless-analytics-jobs), including source indices, output indices, and generated models — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer configuration**
- [ ] [Data frame analytics trained models](migrate-to-serverless-prepare.md#migrate-to-serverless-trained-models), including model IDs and aliases — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Built-in NLP models](migrate-to-serverless-prepare.md#migrate-to-serverless-trained-models) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Install the corresponding models**
- [ ] [Custom NLP models](migrate-to-serverless-prepare.md#migrate-to-serverless-trained-models), including vocabularies, model IDs, and deployment IDs — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Import models and vocabularies, adapting deployment configuration where needed**
- [ ] [Inference endpoints](migrate-to-serverless-prepare.md#migrate-to-serverless-inference-endpoints), including services, settings, model references, and provider credentials — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer configuration and restore provider credentials where needed**
:::

Also record the information shared across these categories:

- Connected applications, client libraries, and ingestion tools, including Beats, Logstash, OpenTelemetry, APM, standalone agents, content connectors, and crawlers. Identify where their endpoints and credentials are configured.
- Every process that creates, updates, or deletes source data or configuration. Include external integrations, scheduled jobs, and administrative scripts.
- Operational state you need to retain, such as alerts, investigation content, execution history, and learned model state.
- Asset owners, representative queries, typical and peak ingestion and search rates, and acceptance criteria. Record compliance, retention, interruption, data loss, and rollback requirements.

## Check compatibility [migrate-to-serverless-compatibility]

Use [Compare {{ech}} and {{serverless-short}}](differences-from-other-elasticsearch-offerings.md) to check whether your required features and capabilities are available in the destination project. Identify dependencies that need an alternative and any blockers to the migration. The [destination preparation guidance](migrate-to-serverless-prepare.md) explains how to adapt individual resources.

:::{note}
Some source deployments combine use cases that a single destination project cannot support. In that case, evaluate separate destination projects and decide which workloads and assets to migrate to each one. Apply the rest of this guide separately to each destination project.
:::

## Next step

Continue to [Create the destination project](migrate-to-serverless-create-project.md).
