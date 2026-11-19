---
navigation_title: Migrate to Serverless
description: Assess your existing solution, prepare and test a Serverless project, and plan the move to production.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
type: how-to
---

# Migrate to {{serverless-full}}

Moving to {{serverless-full}} involves creating a project and adapting your existing solution to it. You can transfer supported user data and export some configuration, while other components require manual setup or redesign. The work involved depends on the features and integrations your solution uses.

This guide covers the full migration process, from assessing the source and preparing and testing the destination to completing the production transition.

## Before you begin [migrate-to-serverless-before-you-begin]

Before starting the migration, make sure that you have:

- **Source access:** Use credentials that can inventory and export every resource in the source environment. A practical broad custom role grants the `all` cluster privilege, `read` and `view_index_metadata` on `*`, and the {{kib}} `all` base privilege for all spaces. You can use the `superuser` role instead, but it is not required. If you use a narrower custom role, confirm that it supports every inventory and export operation in this guide.
- **Destination access:** Make sure that you can create {{serverless-short}} projects in the {{ecloud}} organization. The [predefined **Admin** role](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles-table) or an equivalent role is required. If the destination project already exists, you need the **Admin** role scoped to that project with **Cloud Console, {{es}}, and {{kib}}** access.

## Migration overview [migrate-to-serverless-order]

This guide proposes a three-phase migration process:

- **Assess the source and select a project type:** Inventory the data, configuration, integrations, clients, and dependencies your solution relies on. Select a compatible project type and feature tier, check feature compatibility, and identify the adaptations and migration work required.
- **Prepare and rehearse:** Create the destination and migrate or recreate its assets in dependency order. Transfer and verify stable historical data, rehearse the remaining transfer procedures, and test the complete solution with representative clients. Repeat preparation or recreate the destination until it is ready for production.
- **Complete the production transition:** Plan the migration window and rollback procedure, pause source changes, complete the remaining transfer, switch production clients and ingestion, validate production, and monitor the destination before retiring the source.

The following diagram summarizes these phases and shows the preparation loop you can repeat before moving to production.

:::{image} /deploy-manage/images/serverless-migration-proposed-order.svg
:alt: Assess the solution and create the destination project. Prepare assets, transfer data, test reads and indexing, and evaluate the destination. Return to preparation to refine or recreate the project, or continue to complete the migration and switch to production.
:::

## Assess your existing solution [migrate-to-serverless-assess]

Understand what your solution needs and how you can reproduce it in {{serverless-short}} before preparing the destination.

### Identify your use cases and candidate project type [migrate-to-serverless-use-cases]

Start with how users and applications rely on the source deployment and the workflows the migration must preserve. Identify whether its workloads provide general search and analytics, vector search or AI retrieval, {{observability}}, {{elastic-sec}}, or a combination. Use the [project type comparison](serverless.md#get-started) to identify the candidate project type for each workload.

Classify each workload by its primary purpose, not by an individual feature or asset type. Embeddings, {{ml}}, {{fleet}}, {{agent}}, integrations, and alerting can support several use cases and do not determine the destination on their own.

### Inventory your assets [migrate-to-serverless-inventory]

Identify the data, configuration, integrations, applications, and external dependencies your solution uses. Review the inventory with the people who configure and use each part of the solution.

Focus on user-created resources and customizations, including direct changes to Elastic-managed assets. You generally do not need to inventory or transfer individual managed, system, or internal assets. The destination integrations and components recreate the resources they provide. Record the integrations and versions you use, and check each feature's migration guidance for exceptions.

The following checklist provides a broad reference to the asset types involved in a migration. Mark the items your solution uses and add any resources specific to your environment. [Prepare and test the destination](#migrate-to-serverless-prepare) describes the migration procedures, with links from the corresponding checklist entries. The labels indicate whether you can transfer an asset directly, need to adapt it, or must replace it because it is unavailable in {{serverless-short}}.

% TODO: Add migration procedures and local links for transforms, Watcher, SLOs, Synthetics monitors, reporting schedules, Streams, Attack Discovery, Endpoint artifacts, and network configuration. Keep these entries unlinked until their procedures are documented.

:::{dropdown} Data
- [ ] [Regular indices](#migrate-to-serverless-regular-indices), including mappings and settings — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer documents and adapt settings or lifecycle configuration where needed**
- [ ] [Data streams and backing indices](#migrate-to-serverless-data-streams), including the current write index — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer documents and adapt settings or lifecycle configuration where needed**
- [ ] [Index and data stream aliases](#migrate-to-serverless-data), including filters and write targets — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Stored vectors and `semantic_text` data](#migrate-to-serverless-transfer-considerations) — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Preserve embeddings and adapt mappings or inference references where needed**
- [ ] **Write patterns:** Identify indices and data streams that only append documents and those that also update or delete existing documents. Record which applications or jobs perform these operations and how frequently.
- [ ] **Stable historical data:** Identify indices and backing indices that no longer receive new documents, updates, or deletes and can be copied without reconciling later changes.

Use these patterns to plan your [data transfer](#migrate-to-serverless-data): determine what you can copy during preparation and what needs a final copy after source changes stop, or a tested incremental synchronization procedure.
:::

:::{dropdown} Data structures and processing
- [ ] [Stored scripts and search templates](#migrate-to-serverless-scripts) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [API-managed synonym sets](#migrate-to-serverless-synonyms) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [File-based or index-time synonyms](#migrate-to-serverless-synonyms) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with API-managed search-time synonym sets or redesign the analyzers**
- [ ] [Enrich policies and reference data](#migrate-to-serverless-enrich) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Custom ingest pipelines and `@custom` extensions](#migrate-to-serverless-pipelines), including referenced scripts, enrich policies, and inference endpoints — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Custom component templates](#migrate-to-serverless-component-templates), including integration `@custom` components — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer compatible definitions, remove unsupported settings, and adapt lifecycle references**
- [ ] [Composable index templates](#migrate-to-serverless-templates), including patterns, priorities, component order, and data stream configuration — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer compatible definitions, remove unsupported settings, and adapt lifecycle configuration**
- [ ] [Legacy index templates](#migrate-to-serverless-legacy-templates) still in use — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with composable templates**
- [ ] [{{ilm-cap}} policies, data tiers, and lifecycle actions](#migrate-to-serverless-lifecycle) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with data stream lifecycle or another retention design**
- [ ] Transforms and other custom processing resources
:::

:::{dropdown} Kibana objects and solution configuration
- [ ] [Spaces](#migrate-to-serverless-spaces), including IDs, settings, and access requirements — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer compatible settings and recreate access**
- [ ] [Dashboards, visualizations, and maps](#migrate-to-serverless-saved-objects) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Discover sessions, data views, saved queries, tags, and annotation groups](#migrate-to-serverless-saved-objects) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Connectors](#migrate-to-serverless-connectors), including IDs, secrets, and authorization — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer definitions and restore secrets or authorization**
- [ ] [Observability rules](#migrate-to-serverless-observability-rules), including actions and referenced {{ml}} jobs — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Security detection rules](#migrate-to-serverless-security-rules), including actions and referenced data views and {{ml}} jobs — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Rule exception lists](#migrate-to-serverless-security-rules) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Value lists](#migrate-to-serverless-security-rules) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer separately from detection rules**
- [ ] [Endpoint exceptions](#migrate-to-serverless-security-rules) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer separately from detection rules**
- [ ] [Cases](#migrate-to-serverless-cases), including comments, configuration, attachments, related alerts, and Timelines — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer supported content and recreate omitted configuration**
- [ ] [Maintenance windows](#migrate-to-serverless-maintenance-windows), including schedules, recurrence, filters, and rule scope — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer schedules and filters, adapting removed rule-category restrictions where used**
- [ ] [User-managed workflows](#migrate-to-serverless-workflows), including triggers, schedules, connectors, and dependencies — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] Watcher watches — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with {{kib}} alerting rules**
- [ ] SLOs
- [ ] Synthetics monitors
- [ ] Reporting schedules
- [ ] Streams
- [ ] Attack Discovery configuration
- [ ] Endpoint artifacts
:::

:::{dropdown} Security and access
- [ ] [Cloud organization users and project assignments](#migrate-to-serverless-access) — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Recreate project assignments**
- [ ] [Custom roles](#migrate-to-serverless-access) and their assignments — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Adapt privileges and recreate assignments**
- [ ] [Deployment-local users](#migrate-to-serverless-access) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with organization users**
- [ ] [Authentication realms and role mappings](#migrate-to-serverless-access) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with organization-level authentication**
- [ ] [API keys, service credentials, certificates, and secrets](#migrate-to-serverless-access) — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Create destination credentials**
- [ ] Network policies, private connectivity, proxies, and allowlists — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Recreate for the destination**
- [ ] [Remote cluster connections and cross-cluster searches](#migrate-to-serverless-remote-clusters) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Replace with CPS only between compatible Serverless projects in the same organization**
- [ ] [Cross-cluster replication](#migrate-to-serverless-remote-clusters) — ![Replace or redesign](/deploy-manage/images/serverless-migration-replace.svg "=12x12") **Redesign replication-dependent workflows. CPS does not replicate data**
:::

:::{dropdown} Fleet and integrations
- [ ] [Integration packages and versions](#migrate-to-serverless-integrations) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Install required packages**
- [ ] Direct modifications to managed integration assets — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Reapply through supported customization mechanisms**
- [ ] [{{fleet}} outputs and proxies](#migrate-to-serverless-fleet), including defaults and external destinations — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Adapt destination URLs and restore credentials**
- [ ] [Agent policies](#migrate-to-serverless-fleet), including settings and space assignments — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer compatible settings and update output and space references**
- [ ] [Integration policies](#migrate-to-serverless-fleet), including enabled inputs, streams, and output assignments — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer input settings, adapt package or output references, and restore secrets**
- [ ] [Enrolled {{agent}}s](#migrate-to-serverless-production-clients) — ![Adapt or complete](/deploy-manage/images/serverless-migration-adapt.svg "=12x12") **Migrate or re-enroll agents during the production transition**
:::

:::{dropdown} AI and machine learning
- [ ] [Anomaly detection jobs and datafeeds](#migrate-to-serverless-anomaly-jobs), including source indices and space assignments — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer configuration and rebuild learned model state**
- [ ] [{{ml-cap}} filter lists and calendars](#migrate-to-serverless-anomaly-jobs), including scheduled events and job associations — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Data frame analytics jobs](#migrate-to-serverless-analytics-jobs), including source indices, output indices, and generated models — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer configuration**
- [ ] [Data frame analytics trained models](#migrate-to-serverless-trained-models), including model IDs and aliases — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Transfer**
- [ ] [Built-in NLP models](#migrate-to-serverless-trained-models) — ![Transfer](/deploy-manage/images/serverless-migration-transfer.svg "=12x12") **Install the corresponding models**
- [ ] [Custom NLP models](#migrate-to-serverless-trained-models), including vocabularies, model IDs, and deployment IDs — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Import models and vocabularies, adapting deployment configuration where needed**
- [ ] [Inference endpoints](#migrate-to-serverless-inference-endpoints), including services, settings, model references, and provider credentials — ![Transfer with adaptations](/deploy-manage/images/serverless-migration-mixed.svg "=12x12") **Transfer configuration and restore provider credentials where needed**
:::

Also record the information shared across these categories:

- Connected applications, client libraries, and ingestion tools, including Beats, Logstash, OpenTelemetry, APM, standalone agents, content connectors, and crawlers. Identify where their endpoints and credentials are configured.
- Every process that creates, updates, or deletes source data or configuration. Include external integrations, scheduled jobs, and administrative scripts.
- Operational state you need to retain, such as alerts, investigation content, execution history, and learned model state.
- Asset owners, representative queries, typical and peak ingestion and search rates, and acceptance criteria. Record compliance, retention, interruption, data loss, and rollback requirements.

### Check compatibility [migrate-to-serverless-compatibility]

Use [Compare {{ech}} and {{serverless-short}}](differences-from-other-elasticsearch-offerings.md) to check whether your required features and capabilities are available in the destination project. Identify dependencies that need an alternative and any blockers to the migration. The [destination preparation guidance](#migrate-to-serverless-prepare) explains how to adapt individual resources.

:::{note}
Some source deployments combine use cases that a single destination project cannot support. In that case, evaluate separate destination projects and decide which workloads and assets to migrate to each one. Apply the rest of this guide separately to each destination project.
:::

## Create the destination project [migrate-to-serverless-create]

Confirm the project type selected during assessment. For {{observability}} and {{elastic-sec}} projects, confirm that the selected [{{observability}} feature tier](/solutions/observability/observability-serverless-feature-tiers.md) or [Security feature tier](/solutions/security/security-serverless-feature-tiers.md) supports all capabilities identified during assessment.

1. [Create the destination project](create-serverless-project.md), then [find its connection details](find-connection-details-serverless.md), including the {{es}} and {{kib}} endpoints.
2. If you attach a [network security policy](/deploy-manage/security/network-security.md) to the destination, allow access from the environment where you run the migration. {{serverless-short}} projects accept public traffic by default, but after you attach a policy, traffic that does not match it is denied.
3. Create a temporary [{{serverless-short}} project API key](/deploy-manage/api-keys/serverless-project-api-keys.md) while signed in with the **Admin** role. Do not restrict its security privileges, so that it can access all {{es}} and {{kib}} resources required by the migration procedures in this guide. Store it securely and revoke it when the migration is complete.

## Prepare and test the destination [migrate-to-serverless-prepare]

Use your inventory to migrate or recreate the assets your solution needs in the destination project. The following sections describe the methods, APIs, and tools for each resource type, including compatibility considerations and changes needed to adapt your configuration or data to {{serverless-short}}.

The suggested sequence helps you avoid resource creation errors caused by missing dependencies. You can follow a different sequence, provided you satisfy the creation prerequisites for each resource.

Test the migrated configuration and data with representative read and indexing workflows to confirm that the solution works before changing production connections.

:::{image} /deploy-manage/images/serverless-migration-assets.svg
:alt: Assets to migrate or recreate, grouped by color: integration packages and Fleet, data structures and processing, Kibana content and automation, Observability and Security configuration, access, data, and connections.
:::

% Diagram scope includes planned entries whose supported procedures still need to be developed from the research notes.
% Use entry labels only when they provide concrete actions. Omit Prepare when no additional preparation is needed.

:::::{stepper}

::::{step} Install integration packages
:anchor: migrate-to-serverless-integrations

[Integration packages](/reference/fleet/install-uninstall-integration-assets.md) supply {{es}} and {{kib}} assets, such as templates, ingest pipelines, and dashboards. Install the required packages in the destination instead of copying their managed assets from the source.

- **Identify:** Review the installed integrations and their versions in the source {{kib}}, or use the [installed packages API]({{kib-apis}}operation/operation-get-fleet-epm-packages-installed) where available. Retrieve all pages when using the API. Select the packages your solution still needs.
- **Prepare:** Find each required package in the destination's [Integrations catalog](/reference/fleet/install-uninstall-integration-assets.md#install-integration-assets) and select an available version. If the package is already installed, compare its version with the one you intend to use before changing it. Record customizations for the separate [template](#migrate-to-serverless-component-templates) and [pipeline](#migrate-to-serverless-pipelines) migration procedures, including any direct edits to managed resources.
- **Migrate:** Follow [Install integration assets](/reference/fleet/install-uninstall-integration-assets.md#install-integration-assets) in the destination {{kib}}, or use the [package installation API]({{kib-serverless-apis}}operation/operation-post-fleet-epm-packages-pkgname-pkgversion), `POST /api/fleet/epm/packages/{pkgName}/{pkgVersion}`. API requests go to the {{kib}} endpoint. Install packages separately from configuring agent policies.
- **Verify:** Confirm that each selected package and version is installed successfully and inspect its supplied assets. Check that dashboards and other {{kib}} assets are available in the [required space](/deploy-manage/manage-spaces-fleet.md#spaces-manage-assets).

Package installation does not recreate your agent policies, integration policies, settings, or secrets, or move your agents. Recreate the configuration when you [migrate {{fleet}} outputs and policies](#migrate-to-serverless-fleet). Move production agents during the [production transition](#migrate-to-serverless-production).

:::{note}
The Fleet Server integration package (`fleet_server`) is preinstalled in {{es}}, {{observability}}, and {{elastic-sec}} projects and does not need to be migrated.

Install only the integrations you still need. For example, omit the {{es}} or {{kib}} monitoring integrations if their only purpose was to monitor the source deployment and you plan to retire it.
:::

::::

::::{step} Prepare data structures and processing
:anchor: migrate-to-serverless-set-up

Recreate the {{es}} configuration your solution uses to structure, process, and search data, including index templates, ingest pipelines, stored scripts, synonym sets, and enrich policies.

% TODO: Develop the procedures for transforms and other data structures and processing resources as their procedures are verified.
% Editorial grouping informed by Elevate Knowledge; retain only verified creation prerequisites, not the executor's entire ordering.

#### Stored scripts [migrate-to-serverless-scripts]

[Stored scripts](/explore-analyze/scripting/modules-scripting-store-and-retrieve.md) let applications and other resources reference reusable scripts by ID. Stored search templates also use the script APIs.

- **Identify:** Collect the script IDs used by your applications, queries, and pipelines. Retrieve each definition with [the get script API]({{es-apis}}operation/operation-get-script), `GET /_scripts/{id}`. This API requires a known ID; it does not list all stored scripts.
- **Migrate:** Recreate each definition with [the create or update script API]({{es-serverless-apis}}operation/operation-put-script), `PUT /_scripts/{id}`, using the same script ID to preserve existing references. Use the returned `script` object as the request's `script` value, excluding response fields such as `_id` and `found`.
- **Verify:** Retrieve the destination script and compare its definition with the source. Test its use in queries, search templates, or pipelines when you [verify the solution](#migrate-to-serverless-test).

#### Synonym sets [migrate-to-serverless-synonyms]

[Synonym sets](/solutions/search/full-text/search-with-synonyms.md) group rules that search analyzers use to match equivalent terms.

- **Identify:** List API-managed sets with [the get synonym sets API]({{es-apis}}operation/operation-synonyms-get-synonyms-sets), `GET /_synonyms`, and retrieve their rules with [the get synonym set API]({{es-apis}}operation/operation-synonyms-get-synonym), `GET /_synonyms/{id}`. Retrieve all pages of both sets and rules.
- **Prepare:** File-based synonyms are unavailable in {{serverless-short}}. Convert their rules to API-managed sets and update [analyzer references](/solutions/search/full-text/search-with-synonyms.md#synonyms-synonym-token-filters). These sets are search-time only, so review any index-time synonym usage separately. Sets must exist before you create indices that reference them.
- **Migrate:** Recreate each set with [the create or update synonym set API]({{es-serverless-apis}}operation/operation-synonyms-put-synonym), `PUT /_synonyms/{id}`, sending all its rules in `synonyms_set`. Preserve the set ID or update analyzer references. You can also recreate sets through the [Synonyms UI](/solutions/search/full-text/search-with-synonyms.md#synonyms-store-synonyms-kibana) where available.
- **Verify:** Retrieve the destination rules and compare them with the source. After preparing the dependent index, [test its analyzer](/solutions/search/full-text/search-with-synonyms.md#synonyms-test-analyzer) and run representative synonym queries.

#### Enrich policies and reference data [migrate-to-serverless-enrich]

The [enrich processor](/manage-data/ingest/transform-enrich/data-enrichment.md) adds information from reference indices to incoming documents, such as product details matched by product ID. An enrich policy specifies which indices to use, how to match documents, and which fields to add. If any of your pipelines use this processor, transfer their reference data and recreate and run the policies in the destination before migrating those pipelines.

The following steps use the {{es}} APIs. You can also view, create, and run enrich policies in {{kib}} under **Index Management** → **Enrich Policies**.

- **Identify:** Retrieve source enrich policies with [the get enrich policy API]({{es-apis}}operation/operation-enrich-get-policy), `GET /_enrich/policy`.
- **Migrate:** For each policy, follow this sequence:

    1. **Prepare the reference data.** The policy's `indices` field, inside its `match`, `range`, or `geo_match` definition, identifies the reference indices or data streams to transfer. Migrate them from the source environment following [Transfer data to the destination](#migrate-to-serverless-data), preserving the source mappings.
    2. **Create the policy.** Recreate the source policy with the same name and configuration using [the create enrich policy API]({{es-serverless-apis}}operation/operation-enrich-put-policy), `PUT /_enrich/policy/{name}`. Update `indices` if you renamed the reference indices or data streams in the destination.
    3. **Run the policy.** Use [the execute enrich policy API]({{es-serverless-apis}}operation/operation-enrich-execute-policy), `PUT /_enrich/policy/{name}/_execute?wait_for_completion=true`. Running the policy generates the destination's `.enrich-*` system index. You do not need to migrate that index from the source. Confirm that the response reports `status.phase: COMPLETE`.

- **Verify:** Before proceeding to [ingest pipelines](#migrate-to-serverless-pipelines), confirm that all required enrich policies have their reference data in the destination and have run successfully against that data.

% TODO: Add an example using the user's tested LDAP reference data and user UUID enrichment once the exact lab definitions and sample documents are available.

#### Ingest pipelines [migrate-to-serverless-pipelines]

[Ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md) transform incoming documents before indexing by running a sequence of processors. The following guidance uses the {{es}} APIs. You can also create, manage, and test pipelines on {{kib}}'s **Ingest pipelines** management page.

- **Identify:** Retrieve source definitions with [the get pipeline API]({{es-apis}}operation/operation-ingest-get-pipeline), `GET /_ingest/pipeline` or `GET /_ingest/pipeline/{id}`. Migrate your custom pipelines, including `@custom` integration extensions. Do not migrate integration-managed pipelines manually. They are installed automatically when you [install the corresponding integration packages](#migrate-to-serverless-integrations).
- **Prepare:** Resolve the references in each pipeline's processors:

    - For `enrich` processors, complete the [enrich policy and reference data migration](#migrate-to-serverless-enrich) first.
    - For `script` processors using `id`, migrate the referenced [stored scripts](#migrate-to-serverless-scripts).

- **Migrate:** Recreate each pipeline with the same ID and configuration using [the create or update pipeline API]({{es-serverless-apis}}operation/operation-ingest-put-pipeline), `PUT /_ingest/pipeline/{id}`. Use the definition under that ID in the GET response as the request body. Omit the system-generated root fields `created_date`, `created_date_millis`, `modified_date`, and `modified_date_millis` if present. Update resource references if their IDs changed in the destination.
- **Verify:** Retrieve the destination pipeline definitions and compare them with the source, accounting for any updated resource references. Test their processing when you [verify the solution](#migrate-to-serverless-test).

#### Component templates [migrate-to-serverless-component-templates]

[Component templates](/manage-data/data-store/templates.md#component-templates) define reusable mappings, settings, and aliases that index templates apply to new indices and data streams. Many integration package index templates reference `@custom` component templates as supported extension points for mapping and setting customizations. Account for these customizations and any other component templates your solution relies on when preparing the destination.

The following guidance uses the {{es}} APIs. You can also view, create, and manage component templates in {{kib}} under **Index Management** → **Component Templates**.

- **Identify:** List source components with [the get component templates API]({{es-apis}}operation/operation-cluster-get-component-template), `GET /_component_template`. Select your custom components and integration extensions, such as `@custom` components.
- **Prepare:** Compare `template.settings` with the [settings available in Serverless](elasticsearch://reference/elasticsearch/index-settings/serverless.md). Remove unsupported settings, such as `index.number_of_shards` and `index.number_of_replicas`, and [adapt ILM references](#migrate-to-serverless-lifecycle) where present. Preserve other mappings, aliases, and user metadata.
- **Migrate:** Create each component with [the create or update component template API]({{es-serverless-apis}}operation/operation-cluster-put-component-template), `PUT /_component_template/{name}`, or recreate it in {{kib}}. For the API, use the selected entry's `component_template` object from the GET response as a starting point, retaining only fields accepted by the destination API. Review any existing destination definition before replacing it.
- **Verify:** Retrieve the destination component and compare its definition with the source, accounting for the settings and lifecycle adaptations you made.

:::{tip}
Use `_meta.managed` to identify templates explicitly marked as managed. The `@custom` suffix identifies customization candidates and does not determine their managed status. A missing flag means the resource is unmarked, not necessarily user-created. Review your customizations, including any direct modifications to managed assets.
:::

:::{dropdown} Example: Filter managed templates from API responses
Save the responses from `GET /_component_template` and `GET /_index_template` as `component-templates.json` and `index-templates.json`. Use `jq` to list names for review, retaining unmarked resources and `@custom` extensions:

```bash
jq -r '.component_templates[] | select(.component_template._meta.managed != true or (.name | endswith("@custom"))) | .name' component-templates.json

jq -r '.index_templates[] | select(.index_template._meta.managed != true or (.name | endswith("@custom"))) | .name' index-templates.json
```

These commands filter the saved responses locally. Review the resulting list before selecting resources to migrate.
:::

:::{dropdown} Example: Adapt a custom component template
Suppose a custom component template sets the replica count and references an {{ilm-init}} policy in the source. After reviewing that policy and your destination requirements, you select a retention period of `730d` for new data streams in {{serverless-short}}.

The source definition contains:

```json
{
  "template": {
    "settings": {
      "index.number_of_replicas": "0",
      "index.lifecycle.name": "logs-retention"
    }
  }
}
```

Adapt the definition for the destination:

```json
{
  "template": {
    "lifecycle": {
      "data_retention": "730d",
      "enabled": true
    }
  }
}
```

This adaptation makes two separate changes:

- Removes `index.number_of_replicas`, because Elastic manages replication in {{serverless-short}}.
- Replaces the {{ilm-init}} policy reference with the selected data stream retention. The policy name does not determine the retention value, and other {{ilm-init}} actions are not transferred by this change. Data stream retention specifies a minimum storage period, rather than an exact deletion time. Refer to [How data stream lifecycle works](/manage-data/lifecycle/data-stream.md#data-streams-lifecycle-how-it-works).

These fragments show only the relevant configuration. Preserve other compatible settings, mappings, aliases, and user metadata. Check that the destination data stream's index template includes this component and that other template configuration does not override its retention.

The template configures the lifecycle of new data streams. For a data stream that already exists in the destination, [update its lifecycle separately](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#set-lifecycle).
:::

% TBD: adapt settings and mappings to serverless needs a common place, as it might be needed to be referenced from multiple places: settings like number_of_shards, or refresh_internal of 5s minimum, and perhaps unsupported mappings on serverless (type) might be needed by multiple sections. We have to consider that in the next refinement.

#### Index templates [migrate-to-serverless-templates]

[Composable index templates](/manage-data/data-store/templates.md#index-templates) determine the configuration applied when a matching index or data stream is created. They can contain configuration directly and optionally reference component templates.

Referenced component templates must exist when you create an index template, except those listed in `ignore_missing_component_templates`.

- **Identify:** List source templates with [the get index templates API]({{es-apis}}operation/operation-indices-get-index-template), `GET /_index_template`. Select your custom templates and record their `index_patterns`, `priority`, `composed_of`, and any `data_stream` configuration. Leave integration-managed templates to the [installed packages](#migrate-to-serverless-integrations).
- **Prepare:** Adapt settings and lifecycle configuration defined directly in the index template. Remove settings unavailable in {{serverless-short}} and replace {{ilm}} configuration with data stream lifecycle where applicable. Preserve the order of entries in `composed_of`, because later components override earlier ones. Use `GET /_index_template` in the destination to compare existing patterns and priorities with your template, then [resolve any overlaps](/manage-data/data-store/templates.md#avoid-index-pattern-collisions).
- **Migrate:** Create each template with [the create or update index template API]({{es-serverless-apis}}operation/operation-indices-put-index-template), `PUT /_index_template/{name}`, or recreate it in {{kib}}. For the API, use the selected entry's `index_template` object from the GET response as a starting point, retaining only fields accepted by the destination API. Review any existing destination definition before replacing it.
- **Verify:** Retrieve the destination definition, then [simulate the resolved configuration](/manage-data/data-store/templates/simulate-multi-component-templates.md) for a representative destination name. Check mappings, settings, aliases, and lifecycle configuration, including which template takes precedence. Template changes do not update existing indices or backing indices.

:::{dropdown} Example: Check the configuration for a destination name
After recreating an index template named `application-logs` with the pattern `application-logs-*`, resolve its configuration:

```console
POST /_index_template/_simulate/application-logs
```

Then check the configuration selected for a representative destination name:

```console
POST /_index_template/_simulate_index/application-logs-default
```

Review the resolved configuration and reported overlaps. A template can exist in the destination while a higher-priority template takes precedence for the names you intend to use.
:::

#### Legacy index templates [migrate-to-serverless-legacy-templates]
```{applies_to}
serverless: unavailable
```

Legacy index templates are not supported in {{serverless-short}}. Convert those you still need to composable index templates.

- **Identify:** Retrieve the source definitions with [the get legacy index templates API]({{es-apis}}operation/operation-indices-get-template), `GET /_template`.
- **Prepare:** Compare their `index_patterns` with the index names your applications still create. Check whether a composable template already matches those names, because [composable templates take precedence over legacy templates](/manage-data/data-store/templates.md#precedence-and-resolution-rules). Select only the configuration your destination still needs.
- **Migrate:** Recreate that configuration following the [index template guidance](#migrate-to-serverless-templates), optionally using [component templates](#migrate-to-serverless-component-templates). Account for differences in precedence: matching legacy templates can merge, while composable index templates select the highest-priority match.

Templates apply when indices are created. Copying documents from an existing index does not by itself require recreating the legacy template that originally configured it.

#### Lifecycle policies [migrate-to-serverless-lifecycle]
```{applies_to}
serverless: unavailable
```

{{ilm-cap}} policies are not supported in {{serverless-short}} and cannot be migrated. If {{ilm-init}} manages data streams or regular indices in the source environment, migrate their data to data streams and use [data stream lifecycle](/manage-data/lifecycle/data-stream.md) in the destination. Refer to [Migrate {{ilm-init}}-managed data streams to data stream lifecycle](/manage-data/lifecycle/data-stream/tutorial-migrate-ilm-managed-data-stream-to-data-stream-lifecycle.md) for guidance on replacing {{ilm}} with data stream lifecycle.

{{serverless-short}} does not expose data tiers. Elastic fully manages sharding and the underlying storage infrastructure, so you do not need to reproduce {{ilm}} actions such as shrink, force merge, or tier migration. Use data stream lifecycle to configure retention and, when needed, downsampling.

::::

::::{step} Transfer historical data to the destination
:anchor: migrate-to-serverless-data

Transfer data to validate the destination and rehearse the copy procedure. You can start with a subset and retain verified copies of stable data for production. Treat copies of changing data as provisional: replace them with a complete copy after source changes stop, or reconcile subsequent changes through a tested [incremental transfer procedure](#migrate-to-serverless-incremental).

#### Select the data to transfer

Use your [inventory of write patterns and stable data](#migrate-to-serverless-inventory) to select complete indices or historical backing indices to copy now. Leave the current write index for the final window. Confirm that the selected data remains stable: rollover alone does not prevent later updates, deletes, or retention from changing a backing index's contents.

Record the source indices selected for transfer, their destination names, and which copies you have verified. Use this record to identify the data still pending during the [final transfer](#migrate-to-serverless-final-transfer). If no data is stable, use preparation to test the procedure and perform the definitive copy during the final window.

:::{important}
Do not transfer system indices as user data. The backing indices of your application's data streams are part of its user data, even though their names start with `.ds-`. Identify them through the data stream definition rather than selecting all hidden indices.
:::

#### Select a transfer method [migrate-to-serverless-transfer-documents]

- **{{ech}} to {{serverless-short}}:** Use [reindex from remote](/manage-data/migrate/migrate-data-using-reindex-api.md) when the destination can reach the source. {{es}} transfers the documents directly between the environments, without an intermediate {{ls}} instance.
- **Other sources or transfer requirements:** Use [{{ls}}](/manage-data/migrate/migrate-with-logstash.md), running it on a host that can reach both environments.

Check the [supported source and destination combinations](/manage-data/migrate.md#data-migration-guides-serverless) and the selected method's authentication requirements. You can also re-ingest data from its original source. User-managed snapshot and restore is unavailable in {{serverless-short}}.

#### Transfer considerations [migrate-to-serverless-transfer-considerations]

Apply these considerations when preparing the destination indices and copying documents, for both regular indices and data streams:

- **Vector embeddings:** If your indices or data streams use embeddings for semantic search, retain compatible vector mappings and include the stored vectors in the source reads. Follow the [dense vector retrieval guidance](elasticsearch://reference/elasticsearch/mapping-reference/dense-vector.md#accessing-dense_vector-fields-in-search-responses) or the [`semantic_text` embedding reuse procedure](elasticsearch://reference/elasticsearch/mapping-reference/semantic-text-search-retrieval.md#reindex-while-preserving-embeddings), which requires the same `inference_id`. If you need to regenerate embeddings, [prepare the destination endpoint](#migrate-to-serverless-inference-endpoints) and index the input text through [`semantic_text`](/solutions/search/semantic-search/semantic-search-semantic-text.md) or an [{{infer}} pipeline](/solutions/search/semantic-search/semantic-search-inference.md).
- **Ingest pipelines:** Avoid applying the same transformations twice to documents already processed in the source. Check request-selected pipelines and the destination's default and final pipelines. `pipeline=_none` bypasses the default pipeline but not an `index.final_pipeline`. Refer to [ingest pipeline settings](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline).
- **Transfer load and rejected requests:** Monitor source ingestion and query latency. Reduce copy concurrency or rate if production workloads are affected or the destination repeatedly returns `429`. Use [reindex throttling](elasticsearch://reference/elasticsearch/rest-apis/reindex-indices.md#docs-reindex-throttle) or adjust [{{ls}} input batch sizes and parallel reads](/manage-data/migrate/migrate-with-logstash.md#additional-config). Inspect rejection responses and retry behavior, and record any documents that fail to transfer.

#### Migrate regular indices [migrate-to-serverless-regular-indices]

For each source index, apply the [transfer considerations](#migrate-to-serverless-transfer-considerations) as you complete these steps:

1. Retrieve its definition with [the get index API]({{es-apis}}operation/operation-indices-get), `GET /<source-index>`.
2. [Create the destination index]({{es-serverless-apis}}operation/operation-indices-create) with the source mappings and compatible settings. Omit generated metadata such as the index UUID and creation date, and remove settings managed by {{serverless-short}}, such as shard and replica counts. Replace [{{ilm-init}} configuration](#migrate-to-serverless-lifecycle) where needed. Check the effective destination templates before creating the index.
3. Transfer the documents using the selected method, with this source index and its prepared destination as explicit targets. Preserve document IDs when configuring {{ls}}, as shown in the [example](#migrate-to-serverless-logstash-example).
4. [Verify the copy](#migrate-to-serverless-verify-data), then recreate the [aliases](/manage-data/data-store/aliases.md) your applications use. Check alias filters, routing, and write targets against the destination names.

#### Migrate data streams [migrate-to-serverless-data-streams]

We recommend transferring each source backing index to a separate destination index, verifying the copy, and then adding it to the destination data stream. This keeps a one-to-one correspondence that helps you track and verify transfers across migration phases. Performing these operations manually requires more work, but you can automate the procedure using the APIs and transfer tools.

Apply the [transfer considerations](#migrate-to-serverless-transfer-considerations) to each backing index copy.

1. **Identify the source backing indices.** Retrieve the data stream definition in the source:

    ```console
    GET /_data_stream/logs-myapp-default
    ```

    The `indices` array lists the backing indices, with the current write index last. Select the stable indices to transfer now and record the write index as pending.

2. **Prepare the destination data stream and copy indices.** Use the destination's integration package or custom [data stream template](#migrate-to-serverless-templates) to create the stream if it does not exist:

    ```console
    PUT /_data_stream/logs-myapp-default
    ```

    This creates a write index for future ingestion. For each selected source backing index, create a separate, standalone destination index with the source mappings and compatible settings, as for [regular indices](#migrate-to-serverless-regular-indices). Use a distinct name, such as `migration-logs-myapp-default-000042`, and record its source counterpart. Select names that do not match a data stream template.

    Omit the internal `_data_stream_timestamp` mapping when creating standalone copies. Association with the destination stream configures it. Review destination retention separately: document transfer does not preserve source lifecycle state or index age.

3. **Transfer and verify each copy.** Read one source backing index and write to its corresponding standalone destination index. Complete the transfer and verify the result before adding that index to the stream.

    The following examples show both transfer methods, and they use standard destination indices for historical copies. [Time-series data streams (TSDS)](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) have additional index-mode and timestamp-range requirements and are not covered by these examples.

    :::{dropdown} Example: Transfer one backing index with reindex from remote

    After preparing `migration-logs-myapp-default-000042`, run this request in the destination project. Replace the source endpoint, API key, and backing index name with your values:

    ```console
    POST /_reindex
    {
      "source": {
        "remote": {
          "host": "https://source.example.com:443",
          "api_key": "<SOURCE_ENCODED_API_KEY>"
        },
        "index": ".ds-logs-myapp-default-2026.10.01-000042"
      },
      "dest": {
        "index": "migration-logs-myapp-default-000042",
        "pipeline": "_none"
      }
    }
    ```

    Reindex preserves document IDs unless you change them through a script or processing. Check the response for failures and verify the copy before adding the destination index to the stream. For the next backing index, change both the source and destination index names.

    :::

    :::{dropdown} Example: Transfer one backing index with Logstash
    :name: migrate-to-serverless-logstash-example

    This example reads a single backing index and writes to its prepared standalone counterpart. It assumes log documents with an ISO 8601 `@timestamp` and no source `@version` field. The filter removes the `@version` field that {{ls}} adds. For other document structures, review the input plugin's [reserved-field handling](logstash-docs-md://lsr/plugins-inputs-elasticsearch.md#plugins-inputs-elasticsearch-failure-handling) and compare the resulting documents with the source.

    Save the configuration as `migration.conf`. Replace the endpoints and set `SOURCE_API_KEY` and `DESTINATION_API_KEY` using the {{ls}} `id:api_key` format described in [Migrate data with {{ls}}](/manage-data/migrate/migrate-with-logstash.md).

    ```ruby
    input {
      elasticsearch {
        hosts => ["https://source.example.com:443"]
        api_key => "${SOURCE_API_KEY}"
        index => ".ds-logs-myapp-default-2026.10.01-000042"
        query => '{"query":{"match_all":{}}}'
        ecs_compatibility => "disabled"
        docinfo => true
        docinfo_fields => ["_id"]
        docinfo_target => "[@metadata][migration]"
      }
    }
    filter {
      mutate {
        remove_field => ["@version"]
      }
    }
    output {
      elasticsearch {
        hosts => ["https://destination.example.com:443"]
        api_key => "${DESTINATION_API_KEY}"
        index => "migration-logs-myapp-default-000042"
        document_id => "%{[@metadata][migration][_id]}"
        action => "index"
        data_stream => false
        manage_template => false
        ilm_enabled => false
        pipeline => "_none"
      }
    }
    ```

    Run the transfer:

    ```bash
    bin/logstash -f migration.conf
    ```

    The input's `docinfo` settings retrieve the source ID, and the output's `document_id` preserves it. `data_stream => false` sends documents to the named standalone index instead of using automatic data stream routing. For the next backing index, change both `index` values, retaining a separate destination for each source index.

    Inspect {{ls}} errors and verify the copied data before adding the index to the stream. A successful process exit alone does not confirm that every document was indexed. This configuration is a finite copy, not an incremental synchronization service.

    :::


4. **Add the verified indices to the destination data stream.** In the destination, use [the update data streams API]({{es-serverless-apis}}operation/operation-indices-modify-data-stream):

    ```console
    POST /_data_stream/_modify
    {
      "actions": [
        {
          "add_backing_index": {
            "data_stream": "logs-myapp-default",
            "index": "migration-logs-myapp-default-000042"
          }
        }
      ]
    }
    ```

    This is an expert-level API. Add only indices prepared and verified for this stream. Retrieve the destination stream definition to confirm membership, then query the stream by its name to check that the historical data is available. Recreate any [data stream aliases](/manage-data/data-store/aliases.md) after their target streams exist.

Repeat the procedure for the remaining backing indices during the final window. Keep the destination's write index for new ingestion. Do not replace it with the source's last write index.

Alternatively, you can reindex the entire source data stream directly into the destination data stream in one operation, using `dest.op_type: "create"`. The destination manages its own rollovers, and source backing-index boundaries are not preserved. IDs reused across source backing indices can conflict in the destination. This requires fewer manual operations, but repeated transfers need [additional handling](#migrate-to-serverless-incremental) to avoid missing changes or creating duplicates.

#### Verify and record the transfer [migrate-to-serverless-verify-data]

Review transfer failures and rejected documents. After refreshing the destination indices, compare document counts for each selected source index and its destination copy, using `GET /<index>/_count`. Compare representative documents by ID, field mappings, and query results. Matching counts alone do not establish that the contents match.

Confirm that copied backing indices belong to the intended data stream and that queries through stream names and aliases return the expected data. Record verified source-to-destination pairs and any pending data or errors. Reuse these copies during the final transfer only if the source data has remained unchanged.

::::

::::{step} Migrate content and configuration in {{kib}}
:anchor: migrate-to-serverless-kibana

Use this section to migrate or recreate user-managed content and configuration in {{kib}}, including spaces, dashboards and visualizations, and resources specific to {{observability}} and {{elastic-sec}}. For each resource, use its supported mechanism: saved object export and import, a dedicated workflow or public API, or manual recreation.

The following procedures group related {{kib}} assets by functionality. Assets that use the same mechanism can be migrated together, while the separate procedures highlight considerations specific to each group.

Unless stated otherwise, API requests in this section use the {{kib}} endpoint. To make [API calls to a non-default space](/deploy-manage/manage-spaces.md#spaces-api-requests), include `/s/{space_id}` in the request path and repeat the procedure for each required space.

#### Spaces [migrate-to-serverless-spaces]

[{{kib}} spaces](/deploy-manage/manage-spaces.md) organize saved objects and access into separate environments. Saved object export and import operates within a space and does not create the destination space. Prepare the required destination spaces before migrating their content.

- **Identify:** Retrieve the source space definitions with [the get spaces API]({{kib-apis}}operation/operation-get-spaces-space), `GET /api/spaces/space`.
- **Migrate:** Recreate each required space in the destination from the **Spaces** management page or with [the create space API]({{kib-serverless-apis}}operation/operation-post-spaces-space). The default destination space already exists. Preserve each source space ID when practical because you cannot change it after creating the space.
- **Verify:** Confirm that each destination space has the intended ID and settings. Use that ID in the space-specific requests in the following procedures, and recreate its access when you [prepare project access](#migrate-to-serverless-access).

#### Dashboards, visualizations, and {{data-sources}} [migrate-to-serverless-saved-objects]

Use [{{kib}} saved object export and import](/explore-analyze/find-and-organize/saved-objects.md#saved-objects-import-and-export) to migrate compatible dashboards, Lens and other saved visualizations, maps, Discover sessions, {{data-sources}}, saved queries, tags, and annotation groups.

- **Identify:** In each source space, use the **{{saved-objects-app}}** page to inventory the exportable content. Focus on objects created by your users, including customized copies of packaged content, and do not select managed content that the destination integrations provide. Select standalone objects that your dashboards do not reference separately, because exporting a dashboard does not include unrelated content.

    You can also use the [Saved Objects APIs]({{kib-apis}}group/endpoint-saved-objects) to inventory exportable objects and filter the results. When an export includes the `managed` field, a value of `true` can help identify managed content. Treat `false` or a missing field as unmarked, not as proof that the object was created by a user.

- **Prepare:** Check [version compatibility](/explore-analyze/find-and-organize/saved-objects.md#_compatibility_across_versions), destination feature availability, and existing destination objects.
- **Migrate:** Export the selected objects from the source space and import the resulting NDJSON file into the corresponding destination space:

    - The {{kib}} UI includes related objects by default.
    - With [the export API]({{kib-apis}}operation/operation-post-saved-objects-export), `POST /api/saved_objects/_export`, set `includeReferencesDeep` to `true` to include referenced objects. Use [the import API]({{kib-serverless-apis}}operation/operation-post-saved-objects-import), `POST /api/saved_objects/_import`, in the destination.
    - Treat the exported NDJSON as opaque and do not edit it.
    - Use `overwrite=true` only for destination objects that you have reviewed and intend to replace. The `createNewCopies` option avoids conflicts by generating new IDs, which can break weak links such as URLs embedded in Markdown panels.

- **Verify:** Review the import response's `successResults` and `errors`, including any generated destination IDs and unresolved references. Confirm that the imported resources are present and can be opened without errors. If you have already transferred data to the destination, verify that visualizations, filters, links, and queries load the expected content. Otherwise, defer this check until after the data migration.

#### {{connectors-ui}} [migrate-to-serverless-connectors]

[{{kib}} connectors](/deploy-manage/manage-connectors.md) are available across {{serverless-short}} project types, but the available connector types depend on the destination project type and feature tier. Connectors are isolated to the space in which they are created, so migrate each connector to every destination space that requires it.

{{rules-ui}}, cases, and workflows can reference connectors. At this stage, you can migrate all required connectors or defer those that will be included as related objects when you export rules or cases. Do not defer connectors used by workflows or other resources whose export does not include them.

- **Identify:** In each source space, use the **{{saved-objects-app}}** page to select the user-created connectors required by your rules, cases, and other resources. For a programmatic inventory, use the [get connectors API]({{kib-apis}}operation/operation-get-actions-connectors).
- **Migrate:** Use saved object export and import in {{kib}} or the {{saved-objects-app}} [export]({{kib-apis}}operation/operation-post-saved-objects-export) and [import]({{kib-serverless-apis}}operation/operation-post-saved-objects-import) APIs to migrate the selected connectors. Connector IDs are immutable and identify the connectors referenced by dependent resources. Avoid `createNewCopies`, which generates new IDs. If you recreate a connector manually, assign its source ID when you create it or update every resource that references it.
- **Verify:** Re-enter any secrets or complete any authorization required after import. [Test each connector](/explore-analyze/alerting/alerts/testing-connectors.md) from the **{{connectors-ui}}** page or with the [run connector API]({{kib-serverless-apis}}operation/operation-post-actions-connector-id-execute) before enabling resources that use it.

#### {{observability}} rules [migrate-to-serverless-observability-rules]
```{applies_to}
serverless:
  observability: ga
```

[{{observability}} rules](/solutions/observability/incident-management/alerting.md) use the same saved object export and import mechanism and APIs as dashboards. Exported rules are inactive, and their execution history and operational state are not included.

- **Identify:** List the source rules with the [get rules API]({{kib-apis}}operation/operation-get-alerting-rules-find), `GET /api/alerting/rules/_find`. Retrieve all pages, select the rules that the destination supports, and record their connectors and other dependencies.
- **Migrate:** Follow [rule export and import](/solutions/observability/incident-management/create-manage-rules.md#observability-create-manage-rules-import-and-export-rules), using `POST /api/saved_objects/_export` and `POST /api/saved_objects/_import`. Include related objects (`includeReferencesDeep: true` with the API) so that the export contains referenced connectors and other dependencies. Connector secrets are not included. If you migrated a connector earlier, retain the existing destination connector when resolving the import conflict instead of overwriting it.
- **Verify:** Check the imported rules' data sources, queries, connectors, permissions, and feature dependencies. For rules that use {{ml}}, prepare the referenced [anomaly detection jobs](#migrate-to-serverless-anomaly-jobs). Test their actions, then enable the rules when the destination is ready to run them.

#### Security detection rules [migrate-to-serverless-security-rules]
```{applies_to}
serverless:
  security: ga
```

[Security detection rules](/solutions/security/detect-and-alert/detection-rule-concepts.md) have dedicated export and import workflows and APIs. These workflows cover rule definitions and related resources such as actions, connectors, and exception lists. Do not migrate detection rules with the generic saved object APIs.

- **Identify:** List the source rules with the [find detection rules API]({{kib-apis}}operation/operation-findrules), `GET /api/detection_engine/rules/_find`. Inventory custom rules and prebuilt rules with source-specific state or configuration, such as enabled state, actions, exceptions, or direct edits. Do not select every installed prebuilt rule by default. Record the selected rules' `rule_id` values and dependencies. Also inventory value lists used by rule exceptions, Endpoint exceptions required by your policies, and referenced {{data-sources}}.
- **Prepare:** [Install the required Elastic prebuilt rules](/solutions/security/detect-and-alert/install-prebuilt-rules.md) in the destination. Compare their source and destination versions and resolve version differences before importing source configuration. For rules that use {{ml}}, also prepare the referenced [anomaly detection jobs](#migrate-to-serverless-anomaly-jobs) before enabling the rules.
- **Migrate:** Migrate the selected rules and the resources they require:

    - **Rules, actions, connectors, and exception lists:** Export and import the rules with the [detection rule workflow](/solutions/security/detect-and-alert/manage-detection-rules.md#import-export-rules-ui), or `POST /api/detection_engine/rules/_export` and `POST /api/detection_engine/rules/_import`. For prebuilt rules installed in the destination, use `overwrite=true` to apply source configuration to the matching `rule_id`. If you migrated connectors earlier, keep `overwrite_action_connectors=false`. Restore connector secrets after import.
    - **Value lists:** Rule exports do not include the contents of value lists used by exceptions. From **Manage value lists**, export each required list from the source and import it into the corresponding destination space. You can instead use the [export value list items API]({{kib-apis}}operation/operation-exportlistitems) and [import value list items API]({{kib-serverless-apis}}operation/operation-importlistitems). Importing a file with the same name as an existing list appends its values to that list.
    - **Endpoint exceptions:** Follow [Import and export Endpoint exceptions](/solutions/security/manage-elastic-defend/elastic-endpoint-exceptions.md#import-export-endpoint-exceptions) to export the source exceptions as an NDJSON file and import it into the destination. Import adds entries without replacing existing exceptions. Review policy assignments after import because assignments to policies that do not exist in the destination are removed.
    - **{{data-sources}}:** Ensure that every referenced {{data-source}} exists in the corresponding destination space with the same ID. If it was not already migrated with a dashboard or other saved object, migrate it with [saved object export and import](#migrate-to-serverless-saved-objects). Do not use `createNewCopies`.

- **Verify:** Review the import summary and conflicts for rules, exception lists, and connectors. An existing connector can produce a connector conflict even when the rule imports successfully. Confirm that the required value lists, Endpoint exceptions, and {{data-sources}} are available in the correct space. Confirm each rule's enabled state, dependencies, permissions, actions, and prebuilt rule update status before allowing it to run.

#### Cases [migrate-to-serverless-cases]
```{applies_to}
serverless:
  observability: ga
  security: ga
```

Cases are available in {{observability}} and {{elastic-sec}} projects. Migrate them in their original space and solution context.

- **Identify:** Review the selected cases and their attachments. Identify any files, alerts, or Timelines that you need to retain separately from the case export.
- **Migrate:** [Export and import cases](/explore-analyze/cases/manage-cases.md#export-import-cases) with saved objects, including related objects. The export includes connectors, user actions, text comments, and supported saved object attachments. It does not include connector secrets, attached files, alerts, or Timelines. If you migrated a connector earlier, retain the existing destination connector when resolving the import conflict instead of overwriting it. Recreate Cases configuration, such as the default connector, custom fields, and templates, separately in the destination.
- **Verify:** Open the imported cases and check their comments, attachments, saved object references, and connectors. Re-authenticate imported connectors when prompted.

#### Maintenance windows [migrate-to-serverless-maintenance-windows]
```{applies_to}
serverless:
  observability: ga
  security: ga
```

Maintenance windows are available in {{observability}} and {{elastic-sec}} projects. They are not included in saved object export and import.

- **Identify:** Retrieve the source definitions with the [find maintenance windows API]({{kib-apis}}operation/operation-get-maintenance-window-find), `GET /api/maintenance_window/_find`.
- **Migrate:** Recreate each required window from the **Maintenance Windows** page or with the [create maintenance window API]({{kib-serverless-apis}}operation/operation-post-maintenance-window), `POST /api/maintenance_window`.
- **Verify:** Confirm that each window has the intended status, schedule, recurrence, filters, and effect on rules in the destination.

#### Workflows [migrate-to-serverless-workflows]

Workflows are available across {{serverless-short}} project types with the appropriate feature tier. Migrate user-managed workflows, not managed workflows supplied by Elastic features.

- **Identify:** Review the selected workflow definitions for references to connectors, other workflows, and source-specific endpoints or resource IDs. Identify which references need to change for the destination.
- **Migrate:** Use the [export workflows API]({{kib-apis}}operation/operation-post-workflows-export), `POST /api/workflows/export`, and the destination [bulk create workflows API]({{kib-serverless-apis}}operation/operation-post-workflows), `POST /api/workflows`. Map the exported `entries` to the `workflows` creation payload. The export response is not itself a create request. You can also recreate individual YAML definitions from the **Workflows** page.
- **Verify:** Before enabling the migrated workflows, verify their dependencies, permissions, credentials, triggers, schedules, and external effects. Run controlled tests in the destination. Execution history is not migrated.

% TODO: Develop SLOs, Timelines, Synthetics, Reporting schedules, Streams, Endpoint artifacts, Attack Discovery, and other feature-specific configuration from the research notes without implying saved object coverage.

::::

::::{step} Migrate {{fleet}} outputs and policies
:anchor: migrate-to-serverless-fleet

[Agent policies](/reference/fleet/agent-policy.md) configure groups of {{agent}}s. Their [integration policies](/reference/fleet/add-integration-to-policy.md) define what each integration collects, and [outputs](/reference/fleet/fleet-settings.md#output-settings) determine where agents send data. Recreate the user-managed configuration for the [packages installed earlier](#migrate-to-serverless-integrations).

Outputs, proxies, and Fleet Server hosts are shared across the deployment or project. With [space-aware {{fleet}}](/deploy-manage/manage-spaces-fleet.md), agent and integration policies are associated with spaces and can be shared across them. Older source deployments might still use the global policy model.

- **Identify:** In the source {{fleet}}, review the outputs, agent policies, and integration policies your solution uses. You can also retrieve them with `GET /api/fleet/outputs`, `GET /api/fleet/agent_policies`, and `GET /api/fleet/package_policies`. Send API requests to the {{kib}} endpoint. For space-aware policies, use the corresponding space and record their space assignments, counting shared policies once. Retrieve all pages of policy results. Record the associations between policies, package versions, enabled inputs and streams, and output assignments for both collected data and agent monitoring. Distinguish explicit output assignments from inherited defaults.
- **Prepare:** Decide which outputs should send data to the new project and which external destinations you still need. Review the [{{fleet}} and {{agent}} restrictions for {{serverless-short}}](/reference/fleet/fleet-agent-serverless-restrictions.md). Obtain the credentials, certificates, and secret values needed to recreate outputs and integration settings. Source secret references are not transferable. Prepare any required [proxies](/reference/fleet/fleet-agent-proxy-support.md) before creating outputs that reference them. Compare source integration settings with the package versions installed in the destination, and adapt the configuration where those versions differ. Use the project's provided Fleet Server hosts instead of copying the source hosts.
- **Migrate:** Recreate the resources in this order, using the creation APIs linked below or the corresponding {{fleet}} configuration pages. For API requests, build the documented creation payloads rather than submitting complete GET responses. Let the destination generate resource IDs and record the correspondence with source IDs.

    1. **Prepare destination outputs.** Use the project's provided output for data that should go to the new project. Recreate required custom outputs from **Fleet** → **Settings**, or with the [create output API]({{kib-serverless-apis}}operation/operation-post-fleet-outputs), `POST /api/fleet/outputs`. Restore their connection settings and secrets, and replace proxy references with destination IDs. New outputs of type `elasticsearch` must use the project's default {{es}} URL. For external destinations, use a supported type such as [Logstash](/reference/fleet/ls-output-settings.md), [Kafka](/reference/fleet/kafka-output-settings.md), or [Remote Elasticsearch](/reference/fleet/remote-elasticsearch-output.md), following its configuration requirements and restrictions. Configure the default outputs for data and agent monitoring according to your solution.
    2. **Recreate agent policies.** [Create each policy](/reference/fleet/agent-policy.md#create-a-policy) in its intended destination space, or use the [create agent policy API]({{kib-serverless-apis}}operation/operation-post-fleet-agent-policies), `POST /api/fleet/agent_policies?sys_monitoring=false`. The query parameter avoids adding a System integration automatically. [Assign shared policies to the required spaces](/deploy-manage/manage-spaces-fleet.md#spaces-manage-policies) instead of creating a copy per space. Reproduce the required policy settings and replace explicit `data_output_id` and `monitoring_output_id` references with destination output IDs. Keep inherited assignments unset so they use the destination defaults.
    3. **Recreate integration policies.** [Add each integration to its agent policies](/reference/fleet/add-integration-to-policy.md), or use the [create package policy API]({{kib-serverless-apis}}operation/operation-post-fleet-package-policies), `POST /api/fleet/package_policies`. Use the destination package version and agent policy IDs in `policy_ids`. Restore the integration settings, secret values, and enabled or disabled state of inputs and streams. Replace any explicit `output_id` with the corresponding destination ID. If a policy is shared, recreate it once and associate it with the required destination agent policies.

- **Verify:** Read back the destination resources and compare their settings, package versions, policy associations, space assignments, and enabled inputs and streams. Check the outputs for both collected data and agent monitoring. For collected data, an [integration-level output takes precedence](/reference/fleet/integration-level-outputs.md#_order_of_precedence) over the agent policy output, followed by the global default. Verify actual collection and delivery with [test clients](#migrate-to-serverless-test) before moving production agents.

::::

::::{step} Prepare AI and {{ml}} resources
:anchor: migrate-to-serverless-inference

Prepare the {{ml}} jobs and datafeeds, trained models, and {{infer}} endpoints your solution uses. Include resources configured directly in **Machine Learning** and those created from {{observability}} or {{elastic-sec}} features.

Of the resources covered here, {{es}} {{vectordb}} projects support only [{{infer}} endpoints](#migrate-to-serverless-inference-endpoints), backed by Elastic Inference Service (EIS) or external providers.

In {{observability}} projects, {{ml}} jobs require [Observability Complete](/solutions/observability/observability-serverless-feature-tiers.md). In {{elastic-sec}} projects, they require [Security Analytics Essentials or Complete](/solutions/security/security-serverless-feature-tiers.md). The {{infer}} management UI is unavailable in Observability Logs Essentials.

#### Anomaly detection jobs and datafeeds [migrate-to-serverless-anomaly-jobs]
```{applies_to}
serverless:
  vectordb: unavailable
```

[Anomaly detection jobs](/explore-analyze/machine-learning/anomaly-detection.md) learn patterns in time series data and identify unusual behavior. Their datafeeds define which data they analyze. Jobs can be custom or supplied by a solution or integration.

- **Identify:** View source jobs and {{dfeeds}} on **Anomaly Detection Jobs** in {{kib}}, or use the [get anomaly detection jobs API]({{es-apis}}operation/operation-ml-get-jobs) and [get {{dfeeds}} API]({{es-apis}}operation/operation-ml-get-datafeeds).
- **Prepare:** Recreate required filter lists before importing jobs. Missing referenced filter lists cause the import to fail.
- **Migrate:** Recreate unchanged prebuilt jobs from the corresponding [Security](/solutions/security/detect-and-alert/machine-learning.md#ml-job-settings-interface) or [Observability](/solutions/observability/logs/inspect-log-anomalies.md) feature. For custom or modified jobs, follow [Export and import anomaly detection jobs](/explore-analyze/machine-learning/setting-up-machine-learning.md#move-anomaly-detection-jobs). Adapt {{dfeed}} indices and restore calendars and space assignments. Preserve job IDs referenced by rules, or update those references.
- **Verify:** Run jobs and {{dfeeds}} over the intended historical interval and confirm that they process destination data and produce results. Job exports contain configuration only, so imported jobs must rebuild their learned models from that data.

#### Data frame analytics jobs [migrate-to-serverless-analytics-jobs]
```{applies_to}
serverless:
  vectordb: unavailable
```

[Data frame analytics jobs](/explore-analyze/machine-learning/data-frame-analytics.md) perform outlier detection, regression, or classification and write the analysis results to a destination index. Regression and classification also produce trained models.

- **Identify:** View source jobs on **Data Frame Analytics Jobs** in {{kib}}, or use the [get data frame analytics jobs API]({{es-apis}}operation/operation-ml-get-data-frame-analytics).
- **Prepare:** Transfer the required source data before importing the jobs.
- **Migrate:** Follow [Export and import data frame analytics jobs](/explore-analyze/machine-learning/setting-up-machine-learning.md#move-dataframe-analytics-jobs), adapting source and destination index references. To retain an existing trained model, transfer it separately as described in [Trained models](#migrate-to-serverless-trained-models).
- **Verify:** Run the required analyses against destination data and check the output indices and results.

#### Trained models hosted in the project [migrate-to-serverless-trained-models]
```{applies_to}
serverless:
  vectordb: unavailable
```

[Trained models](/explore-analyze/machine-learning/data-frame-analytics/ml-trained-models.md) perform {{infer}} inside your project for tasks such as classification, regression, and text embedding generation. They include models produced by data frame analytics jobs and pretrained NLP models used by ingest pipelines and applications.

- **Identify:** View source models on **{{models-app}}** in {{kib}}, or use the [get trained models API]({{es-apis}}operation/operation-ml-get-trained-models).
- **Migrate:** Use the procedure for the model type:

    - For built-in models, [install the corresponding model](/explore-analyze/machine-learning/nlp/ml-nlp-built-in-models.md) in the destination.
    - For custom data frame analytics models, follow [Exporting and importing models](/explore-analyze/machine-learning/data-frame-analytics/ml-trained-models.md#export-import).
    - For custom NLP models, [import the model and vocabulary using {{product.eland}}](/explore-analyze/machine-learning/nlp/ml-nlp-import-model.md), then [start its deployment](/explore-analyze/machine-learning/nlp/ml-nlp-deploy-model.md).

    Preserve referenced IDs and recreate aliases, or update the resources that use them. Serverless model deployments always use [adaptive allocations](/deploy-manage/autoscaling/trained-model-autoscaling.md).

- **Verify:** [Test {{infer}}](/explore-analyze/machine-learning/nlp/ml-nlp-test-inference.md) with the same sample inputs in the source and destination and compare the results. Use the IDs or aliases your pipelines and applications reference.

#### {{infer-cap}} endpoints [migrate-to-serverless-inference-endpoints]

[{{infer-cap}} endpoints](/explore-analyze/elastic-inference.md) provide named access to models hosted in the project, EIS, or external providers.

For embedding generation during migration, review the [data transfer considerations](#migrate-to-serverless-transfer-considerations).

- **Identify:** View source endpoints on **Elastic Inference** or **External Inference** in {{kib}} (**Inference endpoints** in earlier versions), or use the [get {{infer}} endpoint API]({{es-apis}}operation/operation-inference-get).
- **Prepare:** Obtain provider credentials for external endpoints. The get endpoint API does not return stored secrets.
- **Migrate:** Recreate custom endpoints with the [create {{infer}} endpoint API]({{es-serverless-apis}}operation/operation-inference-put), using the same service, model, and settings. Preserve `inference_id` or update its references. For default endpoints, use the destination's equivalent when its model and configuration meet your requirements.
- **Verify:** Send representative inputs using the [{{infer}} API]({{es-serverless-apis}}group/endpoint-inference) and confirm that each endpoint produces the expected results.

::::

::::{step} Recreate project access
:anchor: migrate-to-serverless-access

Use the role definitions, assignments, authentication providers, and application access requirements recorded in your inventory.
- **Migration approach:** Recreate the required access with [project custom roles](/deploy-manage/users-roles/serverless-custom-roles.md), adapting privileges to the destination. Manage users and assignments through the [{{ecloud}} organization](/deploy-manage/users-roles/cloud-organization/user-roles.md), and create destination credentials for applications.
- **Compatibility:** Deployment-local users and authentication realms do not transfer to a {{serverless-short}} project. If you use SAML, evaluate [organization-level SAML single sign-on](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md). Review project privileges separately from organization access.

::::

::::{step} Replace remote cluster connections
:anchor: migrate-to-serverless-remote-clusters

Remote cluster connections for cross-cluster search (CCS) and cross-cluster replication (CCR) are unavailable in {{serverless-short}}. For searches across projects, evaluate [cross-project search (CPS)](/deploy-manage/cross-project-search-config.md). CPS connects compatible {{serverless-short}} projects within the same {{ecloud}} organization. It cannot connect to {{ech}}, {{ece}}, {{eck}}, or self-managed clusters.

- **Identify:** Review the source connections on **Remote Clusters** in {{kib}}, or use the [remote cluster info API]({{es-apis}}operation/operation-cluster-remote-info). Record which connections your solution uses for search or replication, including cluster aliases and the queries, dashboards, and rules that reference them.
- **Migrate:** Replace the source behavior according to its purpose:

    - **Search:** Follow [Configure cross-project search](/deploy-manage/cross-project-search-config.md) to configure access, set the intended search scope, and link compatible projects. Adapt cluster prefixes in queries and data views to destination project aliases using [Compare CPS and CCS](/explore-analyze/cross-project-search/cps-compared-to-ccs.md). By default, searches include the origin project and all linked projects, unlike CCS, which searches only the local cluster unless you specify remote targets.
    - **Replication:** [CCR](/deploy-manage/tools/cross-cluster-replication.md) has no direct equivalent in {{serverless-short}}. CPS does not replicate data. Redesign any workflows that depend on replication before completing the migration.

- **Verify:** Run representative searches with the intended users and application credentials. Confirm that queries, dashboards, and rules return data from the expected projects and respect access permissions and search scope. Test any replacement for replication-dependent workflows separately.

::::

::::{step} Verify the solution with test clients
:anchor: migrate-to-serverless-test

The checks for each asset confirm that individual resources are ready. Use test clients to verify that they work together as a solution before changing production connections. Apply the following checklist to the features you use, using representative data from the copies already transferred and from test ingestion:

- [ ] **Client connections and permissions:** Test at least one instance of each client type used in the source. Run a test application for each client library you use, enroll a test {{agent}} in a destination policy, and test your Beats and Logstash configurations where applicable. Confirm that each client connects, authenticates, and performs its required operations with the intended permissions. Check that transient `429` responses trigger retries with exponential backoff and that persistent failures are reported.
- [ ] **Serverless client compatibility:** Remove custom `routing` parameters from requests and replace any application behavior that depends on them. If browser applications send requests directly to {{es}}, route them through a backend service because CORS is unavailable. Refer to [Serverless architectural differences](differences-from-other-elasticsearch-offerings.md#architectural-differences).
- [ ] **Indexing and processing:** Send representative documents and confirm that they reach the intended indices or data streams with the expected fields and values. Include examples that exercise enrich, inference, and failure handling where applicable. To investigate pipeline processing, use [the simulate pipeline API]({{es-serverless-apis}}operation/operation-ingest-simulate) with documents as they arrive before processing. Test `@custom` extensions through the integration pipeline that calls them.
- [ ] **Application queries:** Run the searches, filters, and aggregations your applications use. Compare source and destination results for the same transferred dataset and time range, accounting for any intentional changes.
- [ ] **Kibana experience:** Open the dashboards and views your users rely on in each required space. Check that they show the expected data and that filters, links, and navigation work with the migrated resources.
- [ ] **Solution features:** Run controlled tests of the rules, workflows, machine learning jobs, and inference features you use. Confirm the expected results and use test destinations for notifications or other external actions.
- [ ] **Performance testing (optional):** If performance is critical to your migration decision, consider additional load testing based on your requirements and testing resources. Include queries over recent and historical data. For {{es}} projects, test with the intended [Search Power and Search Boost Window settings](project-settings.md#elasticsearch-manage-project-search-ai-lake-settings), which affect search resources and the volume of data kept search-ready.

Record the results, unresolved issues, and any scenarios you have not tested. Use this record to [decide how to proceed](#migrate-to-serverless-reuse).

::::

::::{step} Evaluate the destination and decide how to proceed
:anchor: migrate-to-serverless-reuse

Use the test results to decide your next action:

- **Continue preparing:** If the solution needs changes, return to the relevant preparation steps and repeat the affected tests.
- **Recreate the project:** If you want to start from a clean destination, [create a new project](#migrate-to-serverless-create) using the setup you tested, repeat preparation, and verify it again.
- **Keep the tested project:** If you intend to use it for production, identify test data and provisional copies to remove, verified historical copies to retain, and any configuration to update.

Once the destination is validated and you have identified the data and configuration still to transfer, continue to [Complete the migration and switch to production](#migrate-to-serverless-production).

::::

:::::

## Complete the migration and switch to production [migrate-to-serverless-production]

Follow this procedure after validating the destination. It coordinates the remaining transfer and the switch of production clients using the asset-specific methods you tested during preparation.

This procedure pauses source writes and configuration changes during the final transfer. If that interruption is unsuitable, evaluate the [alternative migration approaches](#migrate-to-serverless-alternatives).

:::::{stepper}

::::{step} Prepare the production transition
:anchor: migrate-to-serverless-cutover-plan

Schedule the migration window. Identify the data and configuration still to transfer, including changes made in the source since preparation, and prepare the client connection changes.

Transfer and verify any remaining stable historical data while the source is active, following [Transfer historical data to the destination](#migrate-to-serverless-data). Keep the record of completed copies up to date. Identify provisional copies of changing data that need replacement during the final window.

:::{tip}
Consider [manually rolling over](/manage-data/data-store/data-streams/use-data-stream.md#manually-roll-over-a-data-stream) high-volume data streams in the source to include their former write indices in the historical transfer. This can reduce the data left to copy during the final pause. For [TSDS](/manage-data/data-store/data-streams/time-bound-tsds.md), wait until incoming data with current timestamps starts reaching the new backing index before copying the previous one. Rollover alone does not make those indices immutable.
:::

Define the validation criteria and rollback procedure before starting the transition. Include when to return to the source and how to handle any data written to the destination before returning.

::::

::::{step} Pause source writes and configuration changes
:anchor: migrate-to-serverless-offline

Pause ingestion and other processes that create, update, or delete source data, including automated retention that could remove data selected for transfer. Pause edits to the configuration being transferred. Keep the source available for the reads needed by the final transfer.

If you cannot pause writes while keeping the source available for reads, consider [switching ingestion before completing the historical transfer](#migrate-to-serverless-switch-before-history).

::::

::::{step} Complete the final transfer
:anchor: migrate-to-serverless-final-transfer

Use the methods tested during preparation to finish the transfer:

1. Refresh the source inventory and compare it with your record of verified copies. Include new indices, backing indices created by rollovers since preparation, and each data stream's last write index.
2. Transfer the remaining indices and backing indices. Retain verified copies whose source data has remained unchanged. Replace provisional copies of changing data with complete copies from the paused source, unless you have tested a procedure to reconcile subsequent changes. For data streams, verify the new copies and add them to the destination stream as [described during preparation](#migrate-to-serverless-data-streams).
3. Apply pending configuration changes and [verify the complete transferred dataset](#migrate-to-serverless-verify-data) before switching production connections.

If a provisional copy is already attached to a destination data stream, remove it from that stream with `remove_backing_index` before adding its verified replacement. Do not retain both copies. Refer to [the update data streams API]({{es-serverless-apis}}operation/operation-indices-modify-data-stream).

::::

::::{step} Switch production clients and ingestion
:anchor: migrate-to-serverless-production-clients

Update applications and ingestion tools to use the destination endpoints and credentials. For {{fleet}}-managed {{agent}}s, follow the [agent migration instructions](/reference/fleet/migrate-elastic-agent.md#migrate-elastic-agent-migrated-agents) using the destination policies and enrollment settings prepared earlier.

Resume production activity against the destination.

::::

::::{step} Validate production
:anchor: migrate-to-serverless-production-validation

Confirm that production reads and writes use the destination and that the required application, ingestion, and solution workflows meet the validation criteria.

If the criteria are not met and the transition cannot continue, follow the rollback procedure you prepared before the switch.

::::

::::{step} Monitor the destination and retire the source
:anchor: migrate-to-serverless-close

After the bulk transfer ends, check application errors, ingestion rates, query latency, and resource consumption under normal production activity. Repeat the performance checks relevant to your requirements once the workload stabilizes: migration traffic does not represent the project's ongoing workload or cost. Use [AutoOps for Serverless](/deploy-manage/monitor/autoops/autoops-for-serverless.md), where available, to review performance and usage alongside the project's [billing dimensions](/deploy-manage/cloud-organization/billing/serverless-project-billing-dimensions.md).

Keep the source available for the agreed rollback period. Retire it after that period and any requirements to retain source data or state have been met.

::::

:::::

% TODO: Keep this procedure at the coordination level; refer to asset-specific procedures for transfer details.

## Appendix: Alternative migration approaches [migrate-to-serverless-alternatives]

The appropriate migration approach depends on your workload and what interruption, data loss, duplicates, or temporary gaps your application can tolerate. Some logging workloads can accept a brief interruption or incomplete historical data while copying continues. Transactional applications might require coordinated changes to ingestion and application behavior to preserve consistency.

The following alternatives describe approaches to consider, rather than complete synchronization procedures. Design and test your chosen approach against your requirements before switching production traffic.

### Reduce the final transfer with incremental synchronization [migrate-to-serverless-incremental]

- **Approach:** Copy data, including historical and active indices, while the source remains active, then apply subsequent changes incrementally. The main procedure instead leaves changing data for a complete copy during the final pause.
- **When to consider it:** You need a shorter final transfer window and can design and operate a synchronization process that reliably captures the required changes without overloading either environment with reads or writes.
- **Plan for:** You must design and test the incremental process for your workload, including how it identifies new documents, reconciles updates and deletes, handles retries, and controls read and write load. Repeating a document copy does not automatically synchronize the environments. Plan a final pause to apply and verify the remaining changes unless your design also handles writes during the switch.

:::{dropdown} Transfer mechanisms and limitations

- **Adding missing documents:** For a fixed destination index, preserving `_id` and using `create` allows only absent IDs to be added. With reindex, use `dest.op_type: "create"` and `conflicts: "proceed"`. With {{ls}}, retrieve the source ID with `docinfo`, set the output's `document_id`, and set its `action` to `create`. Existing IDs produce conflicts. The selected source documents are still read and sent, so a final full scan can still take substantial time.
- **Updates and deletes:** `create` does not update existing documents. Reindex's default `index` operation can overwrite documents with matching IDs in a regular destination index, but it does not remove documents deleted from the source. Rebuild the destination copy or use a separate procedure that captures and applies all relevant changes.
- **Data streams:** In a conventional data stream, the same ID can exist in different backing indices. Repeating a transfer through the stream name after rollover can therefore create duplicates. For repeated copies, keep a fixed source-to-destination index correspondence and finish the copy before association: direct `create` operations against an attached backing index are rejected. [TSDS](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md) use generated IDs and timestamp-based routing and require separate handling.

Refer to [the reindex API]({{es-apis}}operation/operation-reindex) and the [{{ls}} input's field tracking options](/manage-data/migrate/migrate-with-logstash.md#field-tracking) for available mechanisms. If selecting changes by a timestamp, use a field that reliably captures arrivals or modifications. Event time alone can miss late-arriving documents. Test retries, updates, and deletes relevant to your workload before relying on an incremental procedure for the final transfer.

:::

### Switch ingestion before completing the historical transfer [migrate-to-serverless-switch-before-history]

- **Approach:** Redirect clients to the destination, then finish copying the source data. If stopping writes requires stopping the source cluster, redirect clients before bringing it back online for migration reads. Keep the source data stable during the transfer.
- **When to consider it:** The destination can receive new data while historical data is still incomplete, and your workload can tolerate the interruption needed to redirect clients.
- **Plan for:** Whether clients buffer and retry data during the interruption, or whether you accept some data loss or duplicates. Reconcile mutable indices so that older source documents do not overwrite newer destination changes. Define how applications behave until the historical transfer is complete.

### Parallel ingestion [migrate-to-serverless-parallel]

- **Approach:** Send new data to both environments while preparing the destination and transferring any required historical data.
- **When to consider it:** Your ingestion tools or applications can deliver to both environments, and you want to validate live ingestion before switching production reads.
- **Plan for:** Delivery failures, retries, duplicates, and the boundary between historical copies and new data. Decide how to handle writes that succeed in only one environment, and how to replicate updates or deletes if required. Application changes might be necessary.

### Phased migration [migrate-to-serverless-phased]

- **Approach:** Move separate workloads or applications in stages, validating each before continuing.
- **When to consider it:** Workloads can operate independently, so you can migrate them without switching the whole solution at once.
- **Plan for:** Shared data, queries, and dependencies that span migrated and unmigrated workloads. Decide which environment receives each workload's writes and how clients access its data. Moving clients in stages does not itself synchronize the environments.

## Appendix: {{serverless-short}} index settings and mappings

refresh_interval
shard settings...

refer to xxx for more details.
