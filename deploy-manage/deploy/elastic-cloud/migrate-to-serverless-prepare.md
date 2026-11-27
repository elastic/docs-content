---
navigation_title: Prepare and test the destination
description: Migrate and adapt your assets, transfer historical data, and test the Serverless destination before production.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
type: how-to
---

# Prepare and test the destination [migrate-to-serverless-prepare]

**Serverless migration process**

:::{image} /deploy-manage/images/serverless-migration-navigation-grouped-prepare.svg
:alt: Assess, create project, prepare and test, and switch to production. The preparation cycle runs from Prepare to Transfer data to Test and validate and back to Prepare. Prepare is highlighted for the destination preparation page.
:::

Previous: [Create project](migrate-to-serverless-create-project.md) · [Transfer data](migrate-to-serverless-transfer-data.md) · Next: [Test and validate](migrate-to-serverless-test-and-validate.md)

Use your inventory to migrate or recreate the assets your solution needs in the destination project. The following sections describe the methods, APIs, and tools for each resource type, including compatibility considerations and changes needed to adapt your configuration or data to {{serverless-short}}.

The suggested sequence helps you avoid resource creation errors caused by missing dependencies. You can follow a different sequence, provided you satisfy the creation prerequisites for each resource.

% Diagram scope includes planned entries whose supported procedures still need to be developed from the research notes.
% Use entry labels only when they provide concrete actions. Omit Prepare when no additional preparation is needed.

:::{image} /deploy-manage/images/serverless-migration-assets.svg
:alt: Prepare integration packages and Fleet configuration, data structures, a subset of data for testing, Kibana and solution resources, AI and machine learning, and access. Test and validate the destination. Refine or recreate the project and repeat preparation, or continue to complete the migration and switch to production.
:::

[Test the migrated configuration and data](migrate-to-serverless-test-and-validate.md) with representative read and indexing workflows to confirm that the solution works before changing production connections.

:::::{stepper}

::::{step} Configure {{fleet}} and integrations
:anchor: migrate-to-serverless-configure-fleet

Install the integration packages and recreate the {{fleet}} configuration your solution uses. If you organize integration assets or policies by [{{kib}} space](/deploy-manage/manage-spaces-fleet.md), create the required spaces in the destination before proceeding.

### Install integration packages [migrate-to-serverless-integrations]

[Integration packages](/reference/fleet/install-uninstall-integration-assets.md) supply {{es}} and {{kib}} assets, such as templates, ingest pipelines, and dashboards. Install the required packages in the destination instead of copying their managed assets from the source.

- **Identify:** Review the installed integrations and their versions in the source {{kib}}, or use the [installed packages API]({{kib-apis}}operation/operation-get-fleet-epm-packages-installed) where available. Retrieve all pages when using the API. Select the packages your solution still needs.
- **Prepare:** Find each required package in the destination's [Integrations catalog](/reference/fleet/install-uninstall-integration-assets.md#install-integration-assets) and select an available version. If the package is already installed, compare its version with the one you intend to use before changing it. Record customizations for the separate [template](#migrate-to-serverless-component-templates) and [pipeline](#migrate-to-serverless-pipelines) migration procedures, including any direct edits to managed resources.
- **Migrate:** Follow [Install integration assets](/reference/fleet/install-uninstall-integration-assets.md#install-integration-assets) in the destination {{kib}}, or use the [package installation API]({{kib-serverless-apis}}operation/operation-post-fleet-epm-packages-pkgname-pkgversion), `POST /api/fleet/epm/packages/{pkgName}/{pkgVersion}`. API requests go to the {{kib}} endpoint. Install packages separately from configuring agent policies.
- **Verify:** Confirm that each selected package and version is installed successfully and inspect its supplied assets. Check that dashboards and other {{kib}} assets are available in the [required space](/deploy-manage/manage-spaces-fleet.md#spaces-manage-assets).

:::{note}
The Fleet Server integration package (`fleet_server`) is preinstalled in {{es}}, {{observability}}, and {{elastic-sec}} projects and does not need to be migrated.

Install only the integrations you still need. For example, omit the {{es}} or {{kib}} monitoring integrations if their only purpose was to monitor the source deployment and you plan to retire it.
:::

### Migrate {{fleet}} outputs and policies [migrate-to-serverless-fleet]

[Agent policies](/reference/fleet/agent-policy.md) configure groups of {{agent}}s. Their [integration policies](/reference/fleet/add-integration-to-policy.md) define what each integration collects, and [outputs](/reference/fleet/fleet-settings.md#output-settings) determine where agents send data. Recreate the user-managed configuration for the [packages installed earlier](#migrate-to-serverless-integrations).

Outputs, proxies, and Fleet Server hosts are shared across the deployment or project. With [space-aware {{fleet}}](/deploy-manage/manage-spaces-fleet.md), agent and integration policies are associated with spaces and can be shared across them. Older source deployments might still use the global policy model.

- **Identify:** In the source {{fleet}}, review the outputs, agent policies, and integration policies your solution uses. You can also use the {{kib}} APIs to retrieve [outputs]({{kib-apis}}operation/operation-get-fleet-outputs), [agent policies]({{kib-apis}}operation/operation-get-fleet-agent-policies), and [integration policies]({{kib-apis}}operation/operation-get-fleet-package-policies). For space-aware policies, use the corresponding space and record their space assignments, counting shared policies once. Retrieve all pages of policy results. Record the associations between policies, package versions, enabled inputs and streams, and output assignments for both collected data and agent monitoring. Distinguish explicit output assignments from inherited defaults.
- **Prepare:** Decide which outputs should send data to the new project and which external destinations you still need. Review the [{{fleet}} and {{agent}} restrictions for {{serverless-short}}](/reference/fleet/fleet-agent-serverless-restrictions.md). Obtain the credentials, certificates, and secret values needed to recreate outputs and integration settings. Source secret references are not transferable. Prepare any required [proxies](/reference/fleet/fleet-agent-proxy-support.md) before creating outputs that reference them. Compare source integration settings with the package versions installed in the destination, and adapt the configuration where those versions differ. Use the project's provided Fleet Server hosts instead of copying the source hosts.
- **Migrate:** Recreate the resources in this order, using the creation APIs linked below or the corresponding {{fleet}} configuration pages. For API requests, build the documented creation payloads rather than submitting complete GET responses. If you use the APIs, record the destination output and agent policy IDs. You will need them to recreate the policy associations in the following steps.

    1. **Prepare destination outputs.** Use the project's provided output for data that should go to the new project. Recreate required custom outputs from **Fleet** → **Settings**, or with the [create output API]({{kib-serverless-apis}}operation/operation-post-fleet-outputs), `POST /api/fleet/outputs`. Restore their connection settings and secrets, and replace proxy references with destination IDs. New outputs of type `elasticsearch` must use the project's default {{es}} URL. For external destinations, use a supported type such as [Logstash](/reference/fleet/ls-output-settings.md), [Kafka](/reference/fleet/kafka-output-settings.md), or [Remote Elasticsearch](/reference/fleet/remote-elasticsearch-output.md), following its configuration requirements and restrictions. Configure the default outputs for data and agent monitoring according to your solution.
    2. **Recreate agent policies.** [Create each policy](/reference/fleet/agent-policy.md#create-a-policy) in its intended destination space, or use the [create agent policy API]({{kib-serverless-apis}}operation/operation-post-fleet-agent-policies), `POST /api/fleet/agent_policies?sys_monitoring=false`. The query parameter avoids adding a System integration automatically. [Assign shared policies to the required spaces](/deploy-manage/manage-spaces-fleet.md#spaces-manage-policies) instead of creating a copy per space. Reproduce the required policy settings and replace explicit `data_output_id` and `monitoring_output_id` references with destination output IDs. Keep inherited assignments unset so they use the destination defaults.
    3. **Recreate integration policies.** [Add each integration to its agent policies](/reference/fleet/add-integration-to-policy.md), or use the [create package policy API]({{kib-serverless-apis}}operation/operation-post-fleet-package-policies), `POST /api/fleet/package_policies`. Use the destination package version and agent policy IDs in `policy_ids`. Restore the integration settings, secret values, and enabled or disabled state of inputs and streams. Replace any explicit `output_id` with the corresponding destination ID. If a policy is shared, recreate it once and associate it with the required destination agent policies.

- **Verify:** Confirm that the destination outputs and policies exist and have the expected settings, package versions, policy associations, space assignments, and enabled inputs and streams. Check output assignments for both collected data and agent monitoring, including [output precedence](/reference/fleet/integration-level-outputs.md#_order_of_precedence). Verify actual collection and delivery later, when you [test the solution with test clients](migrate-to-serverless-test-and-validate.md#migrate-to-serverless-test). Keep production agents connected to the source until the [production transition](migrate-to-serverless-production.md).

::::

::::{step} Prepare data structures and processing
:anchor: migrate-to-serverless-set-up

Recreate the {{es}} configuration your solution uses to structure, process, and search data, including index templates, ingest pipelines, stored scripts, synonym sets, and enrich policies.

% TODO: Develop the procedures for transforms and other data structures and processing resources as their procedures are verified.
% Editorial grouping informed by Elevate Knowledge; retain only verified creation prerequisites, not the executor's entire ordering.

### Stored scripts [migrate-to-serverless-scripts]

[Stored scripts](/explore-analyze/scripting/modules-scripting-store-and-retrieve.md) let applications and other resources reference reusable scripts by ID. Stored search templates also use the script APIs.

- **Identify:** Collect the script IDs used by your applications, queries, and pipelines. Retrieve each definition with [the get script API]({{es-apis}}operation/operation-get-script), `GET /_scripts/{id}`. This API requires a known ID; it does not list all stored scripts.
- **Migrate:** Recreate each definition with [the create or update script API]({{es-serverless-apis}}operation/operation-put-script), `PUT /_scripts/{id}`, using the same script ID to preserve existing references. Use the returned `script` object as the request's `script` value, excluding response fields such as `_id` and `found`.
- **Verify:** Retrieve the destination script and compare its definition with the source. Test its use in queries, search templates, or pipelines when you [verify the solution](migrate-to-serverless-test-and-validate.md#migrate-to-serverless-test).

### Synonym sets [migrate-to-serverless-synonyms]

[Synonym sets](/solutions/search/full-text/search-with-synonyms.md) group rules that search analyzers use to match equivalent terms.

- **Identify:** List API-managed sets with [the get synonym sets API]({{es-apis}}operation/operation-synonyms-get-synonyms-sets), `GET /_synonyms`, and retrieve their rules with [the get synonym set API]({{es-apis}}operation/operation-synonyms-get-synonym), `GET /_synonyms/{id}`. Retrieve all pages of both sets and rules.
- **Prepare:** File-based synonyms are unavailable in {{serverless-short}}. Convert their rules to API-managed sets and update [analyzer references](/solutions/search/full-text/search-with-synonyms.md#synonyms-synonym-token-filters). These sets are search-time only, so review any index-time synonym usage separately. Sets must exist before you create indices that reference them.
- **Migrate:** Recreate each set with [the create or update synonym set API]({{es-serverless-apis}}operation/operation-synonyms-put-synonym), `PUT /_synonyms/{id}`, sending all its rules in `synonyms_set`. Preserve the set ID or update analyzer references. You can also recreate sets through the [Synonyms UI](/solutions/search/full-text/search-with-synonyms.md#synonyms-store-synonyms-kibana) where available.
- **Verify:** Retrieve the destination rules and compare them with the source. After preparing the dependent index, [test its analyzer](/solutions/search/full-text/search-with-synonyms.md#synonyms-test-analyzer) and run representative synonym queries.

### Enrich policies and reference data [migrate-to-serverless-enrich]

The [enrich processor](/manage-data/ingest/transform-enrich/data-enrichment.md) adds information from reference indices to incoming documents, such as product details matched by product ID. An enrich policy specifies which indices to use, how to match documents, and which fields to add. If any of your pipelines use this processor, transfer their reference data and recreate and run the policies in the destination before migrating those pipelines.

The following steps use the {{es}} APIs. You can also view, create, and run enrich policies in {{kib}} under **Index Management** → **Enrich Policies**.

- **Identify:** Retrieve source enrich policies with [the get enrich policy API]({{es-apis}}operation/operation-enrich-get-policy), `GET /_enrich/policy`.
- **Migrate:** For each policy, follow this sequence:

    1. **Prepare the reference data.** The policy's `indices` field, inside its `match`, `range`, or `geo_match` definition, identifies the reference indices or data streams to transfer. Migrate them from the source environment following [Transfer data](migrate-to-serverless-transfer-data.md), preserving the source mappings.
    2. **Create the policy.** Recreate the source policy with the same name and configuration using [the create enrich policy API]({{es-serverless-apis}}operation/operation-enrich-put-policy), `PUT /_enrich/policy/{name}`. Update `indices` if you renamed the reference indices or data streams in the destination.
    3. **Run the policy.** Use [the execute enrich policy API]({{es-serverless-apis}}operation/operation-enrich-execute-policy), `PUT /_enrich/policy/{name}/_execute?wait_for_completion=true`. Running the policy generates the destination's `.enrich-*` system index. You do not need to migrate that index from the source. Confirm that the response reports `status.phase: COMPLETE`.

- **Verify:** Before proceeding to [ingest pipelines](#migrate-to-serverless-pipelines), confirm that all required enrich policies have their reference data in the destination and have run successfully against that data.

% TODO: Add an example using the user's tested LDAP reference data and user UUID enrichment once the exact lab definitions and sample documents are available.

### Ingest pipelines [migrate-to-serverless-pipelines]

[Ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md) transform incoming documents before indexing by running a sequence of processors. The following guidance uses the {{es}} APIs. You can also create, manage, and test pipelines on {{kib}}'s **Ingest pipelines** management page.

- **Identify:** Retrieve source definitions with [the get pipeline API]({{es-apis}}operation/operation-ingest-get-pipeline), `GET /_ingest/pipeline` or `GET /_ingest/pipeline/{id}`. Migrate your custom pipelines, including `@custom` integration extensions. Do not migrate integration-managed pipelines manually. They are installed automatically when you [install the corresponding integration packages](#migrate-to-serverless-integrations).
- **Prepare:** Resolve the references in each pipeline's processors:

    - For `enrich` processors, complete the [enrich policy and reference data migration](#migrate-to-serverless-enrich) first.
    - For `script` processors using `id`, migrate the referenced [stored scripts](#migrate-to-serverless-scripts).

- **Migrate:** Recreate each pipeline with the same ID and configuration using [the create or update pipeline API]({{es-serverless-apis}}operation/operation-ingest-put-pipeline), `PUT /_ingest/pipeline/{id}`. Use the definition under that ID in the GET response as the request body. Omit the system-generated root fields `created_date`, `created_date_millis`, `modified_date`, and `modified_date_millis` if present. Update resource references if their IDs changed in the destination.
- **Verify:** Retrieve the destination pipeline definitions and compare them with the source, accounting for any updated resource references. Test their processing when you [verify the solution](migrate-to-serverless-test-and-validate.md#migrate-to-serverless-test).

### Component templates [migrate-to-serverless-component-templates]

[Component templates](/manage-data/data-store/templates.md#component-templates) define reusable mappings, settings, and aliases that index templates apply to new indices and data streams. Many integration package index templates reference `@custom` component templates as supported extension points for mapping and setting customizations. Account for these customizations and any other component templates your solution relies on when preparing the destination.

The following guidance uses the {{es}} APIs. You can also view, create, and manage component templates in {{kib}} under **Index Management** → **Component Templates**.

- **Identify:** List source components with [the get component templates API]({{es-apis}}operation/operation-cluster-get-component-template). Select your custom components and integration extensions, such as `@custom` components.
- **Prepare:** Compare `template.settings` with the [settings available in Serverless](elasticsearch://reference/elasticsearch/index-settings/serverless.md). Remove unsupported settings, such as `index.number_of_shards` and `index.number_of_replicas`. If configured, `index.refresh_interval` must be `5s` or higher, or `-1` to disable automatic refreshes. [Adapt ILM references](#migrate-to-serverless-lifecycle) where present. Preserve other mappings, aliases, and user metadata.
- **Migrate:** Create each component with [the create or update component template API]({{es-serverless-apis}}operation/operation-cluster-put-component-template), or recreate it in {{kib}}. For the API, use the selected entry's `component_template` object from the GET response as a starting point, retaining only fields accepted by the destination API. Review any existing destination definition before replacing it.
- **Verify:** Retrieve the destination component and compare its definition with the source, accounting for the settings and lifecycle adaptations you made.

:::{tip}
Use `_meta.managed` to identify templates explicitly marked as managed. The `@custom` suffix identifies customization candidates and does not determine their managed status. A missing flag means the resource is unmarked, not necessarily user-created. Review your customizations, including any direct modifications to managed assets.
:::

:::{dropdown} Example: Filter out managed templates from API responses
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
      "index.number_of_replicas": "1",
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
- Replaces the {{ilm-init}} policy reference with the selected data stream retention. Other {{ilm-init}} actions are not transferred by this change. Data stream retention specifies a minimum storage period, rather than an exact deletion time. Refer to [How data stream lifecycle works](/manage-data/lifecycle/data-stream.md#data-streams-lifecycle-how-it-works).

The template configures the lifecycle of new data streams. For a data stream that already exists in the destination, [update its lifecycle separately](/manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md#set-lifecycle).
:::

### Index templates [migrate-to-serverless-templates]

[Composable index templates](/manage-data/data-store/templates.md#index-templates) determine the configuration applied when a matching index or data stream is created. They can contain configuration directly and optionally reference component templates.

Referenced component templates must exist when you create an index template, except those listed in `ignore_missing_component_templates`.

The following guidance uses the {{es}} APIs. You can also view, create, and manage index templates in {{kib}} under **Index Management** → **Index Templates**.

- **Identify:** List source templates with [the get index templates API]({{es-apis}}operation/operation-indices-get-index-template). Select your custom templates and record their `index_patterns`, `priority`, `composed_of`, and any `data_stream` configuration. Leave integration-managed templates to the [installed packages](#migrate-to-serverless-integrations).
- **Prepare:** Adapt settings and lifecycle configuration defined directly in the index template. Remove [settings unavailable in {{serverless-short}}](elasticsearch://reference/elasticsearch/index-settings/serverless.md), such as shard and replica counts. If configured, `index.refresh_interval` must be `5s` or higher, or `-1` to disable automatic refreshes. [Adapt {{ilm}} configuration](#migrate-to-serverless-lifecycle) where present. Preserve the order of entries in `composed_of`, because later components override earlier ones. Use `GET /_index_template` in the destination to compare existing patterns and priorities with your template, then [resolve any overlaps](/manage-data/data-store/templates.md#avoid-index-pattern-collisions).
- **Migrate:** Create each template with [the create or update index template API]({{es-serverless-apis}}operation/operation-indices-put-index-template), or recreate it in {{kib}}. For the API, use the selected entry's `index_template` object from the GET response as a starting point, retaining only fields accepted by the destination API. Review any existing destination definition before replacing it.
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

### Legacy index templates [migrate-to-serverless-legacy-templates]
```{applies_to}
serverless: unavailable
```

Legacy index templates are not supported in {{serverless-short}}. Convert those you still need to composable index templates.

- **Identify:** Retrieve the source definitions with [the get legacy index templates API]({{es-apis}}operation/operation-indices-get-template), `GET /_template`.
- **Prepare:** Compare their `index_patterns` with the index names your applications still create. Check whether a composable template already matches those names, because [composable templates take precedence over legacy templates](/manage-data/data-store/templates.md#precedence-and-resolution-rules). Select only the configuration your destination still needs.
- **Migrate:** Recreate that configuration following the [index template guidance](#migrate-to-serverless-templates), optionally using [component templates](#migrate-to-serverless-component-templates). Account for differences in precedence: matching legacy templates can merge, while composable index templates select the highest-priority match.

:::{note}
Templates apply when indices are created. Copying documents from an existing index does not by itself require recreating the legacy template that originally configured it.
:::

### Lifecycle policies [migrate-to-serverless-lifecycle]
```{applies_to}
serverless: unavailable
```

{{ilm-cap}} policies are not supported in {{serverless-short}} and cannot be migrated. If {{ilm-init}} manages data streams or regular indices in the source environment, migrate their data to data streams and use [data stream lifecycle](/manage-data/lifecycle/data-stream.md) in the destination. Refer to [Migrate {{ilm-init}}-managed data streams to data stream lifecycle](/manage-data/lifecycle/data-stream/tutorial-migrate-ilm-managed-data-stream-to-data-stream-lifecycle.md) for guidance on replacing {{ilm}} with data stream lifecycle.

{{serverless-short}} does not expose data tiers. Elastic fully manages sharding and the underlying storage infrastructure, so you do not need to reproduce {{ilm}} actions such as shrink, force merge, or tier migration. Use data stream lifecycle to configure retention and, when needed, downsampling.

::::

::::{step} Transfer data for testing
:anchor: migrate-to-serverless-data

Select the data you want to transfer to the destination. We recommend starting with a representative subset to validate the destination and rehearse the transfer.

If you plan to keep this project for production, you can also transfer all the historical data you need that no longer changes. Follow [Transfer data to {{serverless-full}}](migrate-to-serverless-transfer-data.md) for instructions on selecting, copying, and verifying the data.

::::

::::{step} Migrate content and configuration in {{kib}}
:anchor: migrate-to-serverless-kibana

Use this section to migrate or recreate user-managed content and configuration in {{kib}}, including spaces, dashboards and visualizations, and resources specific to {{observability}} and {{elastic-sec}}. For each resource, use its supported mechanism: saved object export and import, a dedicated workflow or public API, or manual recreation.

The following procedures group related {{kib}} assets by functionality. Assets that use the same mechanism can be migrated together, while the separate procedures highlight considerations specific to each group.

Unless stated otherwise, API requests in this section use the {{kib}} endpoint. To make [API calls to a non-default space](/deploy-manage/manage-spaces.md#spaces-api-requests), include `/s/{space_id}` in the request path and repeat the procedure for each required space.

### Spaces [migrate-to-serverless-spaces]

[{{kib}} spaces](/deploy-manage/manage-spaces.md) organize saved objects and access into separate environments. Saved object export and import operates within a space and does not create the destination space. Prepare the required destination spaces before migrating their content.

- **Identify:** Retrieve the source space definitions with [the get spaces API]({{kib-apis}}operation/operation-get-spaces-space), `GET /api/spaces/space`.
- **Migrate:** Recreate each required space in the destination from the **Spaces** management page or with [the create space API]({{kib-serverless-apis}}operation/operation-post-spaces-space). The default destination space already exists. Preserve each source space ID when practical because you cannot change it after creating the space.
- **Verify:** Confirm that each destination space has the intended ID and settings. Use that ID in the space-specific requests in the following procedures, and recreate its access when you [prepare project access](#migrate-to-serverless-access).

### Dashboards, visualizations, and {{data-sources}} [migrate-to-serverless-saved-objects]

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

### {{connectors-ui}} [migrate-to-serverless-connectors]

[{{kib}} connectors](/deploy-manage/manage-connectors.md) are available across {{serverless-short}} project types, but the available connector types depend on the destination project type and feature tier. Connectors are isolated to the space in which they are created, so migrate each connector to every destination space that requires it.

{{rules-ui}}, cases, and workflows can reference connectors. At this stage, you can migrate all required connectors or defer those that will be included as related objects when you export rules or cases. Do not defer connectors used by workflows or other resources whose export does not include them.

- **Identify:** In each source space, use the **{{saved-objects-app}}** page to select the user-created connectors required by your rules, cases, and other resources. For a programmatic inventory, use the [get connectors API]({{kib-apis}}operation/operation-get-actions-connectors).
- **Migrate:** Use saved object export and import in {{kib}} or the {{saved-objects-app}} [export]({{kib-apis}}operation/operation-post-saved-objects-export) and [import]({{kib-serverless-apis}}operation/operation-post-saved-objects-import) APIs to migrate the selected connectors. Connector IDs are immutable and identify the connectors referenced by dependent resources. Avoid `createNewCopies`, which generates new IDs. If you recreate a connector manually, assign its source ID when you create it or update every resource that references it.
- **Verify:** Re-enter any secrets or complete any authorization required after import. [Test each connector](/explore-analyze/alerting/alerts/testing-connectors.md) from the **{{connectors-ui}}** page or with the [run connector API]({{kib-serverless-apis}}operation/operation-post-actions-connector-id-execute) before enabling resources that use it.

### {{observability}} rules [migrate-to-serverless-observability-rules]
```{applies_to}
serverless:
  observability: ga
```

[{{observability}} rules](/solutions/observability/incident-management/alerting.md) use the same saved object export and import mechanism and APIs as dashboards. Exported rules are inactive, and their execution history and operational state are not included.

- **Identify:** List the source rules with the [get rules API]({{kib-apis}}operation/operation-get-alerting-rules-find), `GET /api/alerting/rules/_find`. Retrieve all pages, select the rules that the destination supports, and record their connectors and other dependencies.
- **Migrate:** Follow [rule export and import](/solutions/observability/incident-management/create-manage-rules.md#observability-create-manage-rules-import-and-export-rules), using `POST /api/saved_objects/_export` and `POST /api/saved_objects/_import`. Include related objects (`includeReferencesDeep: true` with the API) so that the export contains referenced connectors and other dependencies. Connector secrets are not included. If you migrated a connector earlier, retain the existing destination connector when resolving the import conflict instead of overwriting it.
- **Verify:** Check the imported rules' data sources, queries, connectors, permissions, and feature dependencies. For rules that use {{ml}}, prepare the referenced [anomaly detection jobs](#migrate-to-serverless-anomaly-jobs). Test their actions, then enable the rules when the destination is ready to run them.

### Security detection rules [migrate-to-serverless-security-rules]
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

### Cases [migrate-to-serverless-cases]
```{applies_to}
serverless:
  observability: ga
  security: ga
```

Cases are available in {{observability}} and {{elastic-sec}} projects. Migrate them in their original space and solution context.

- **Identify:** Review the selected cases and their attachments. Identify any files, alerts, or Timelines that you need to retain separately from the case export.
- **Migrate:** [Export and import cases](/explore-analyze/cases/manage-cases.md#export-import-cases) with saved objects, including related objects. The export includes connectors, user actions, text comments, and supported saved object attachments. It does not include connector secrets, attached files, alerts, or Timelines. If you migrated a connector earlier, retain the existing destination connector when resolving the import conflict instead of overwriting it. Recreate Cases configuration, such as the default connector, custom fields, and templates, separately in the destination.
- **Verify:** Open the imported cases and check their comments, attachments, saved object references, and connectors. Re-authenticate imported connectors when prompted.

### Maintenance windows [migrate-to-serverless-maintenance-windows]
```{applies_to}
serverless:
  observability: ga
  security: ga
```

Maintenance windows are available in {{observability}} and {{elastic-sec}} projects. They are not included in saved object export and import.

- **Identify:** Retrieve the source definitions with the [find maintenance windows API]({{kib-apis}}operation/operation-get-maintenance-window-find), `GET /api/maintenance_window/_find`.
- **Migrate:** Recreate each required window from the **Maintenance Windows** page or with the [create maintenance window API]({{kib-serverless-apis}}operation/operation-post-maintenance-window), `POST /api/maintenance_window`.
- **Verify:** Confirm that each window has the intended status, schedule, recurrence, filters, and effect on rules in the destination.

### Workflows [migrate-to-serverless-workflows]

Workflows are available across {{serverless-short}} project types with the appropriate feature tier. Migrate user-managed workflows, not managed workflows supplied by Elastic features.

- **Identify:** Review the selected workflow definitions for references to connectors, other workflows, and source-specific endpoints or resource IDs. Identify which references need to change for the destination.
- **Migrate:** Use the [export workflows API]({{kib-apis}}operation/operation-post-workflows-export), `POST /api/workflows/export`, and the destination [bulk create workflows API]({{kib-serverless-apis}}operation/operation-post-workflows), `POST /api/workflows`. Map the exported `entries` to the `workflows` creation payload. The export response is not itself a create request. You can also recreate individual YAML definitions from the **Workflows** page.
- **Verify:** Before enabling the migrated workflows, verify their dependencies, permissions, credentials, triggers, schedules, and external effects. Run controlled tests in the destination. Execution history is not migrated.

% TODO: Develop SLOs, Timelines, Synthetics, Reporting schedules, Streams, Endpoint artifacts, Attack Discovery, and other feature-specific configuration from the research notes without implying saved object coverage.

::::


::::{step} Prepare AI and {{ml}} resources
:anchor: migrate-to-serverless-inference

Prepare the {{ml}} jobs and datafeeds, trained models, and {{infer}} endpoints your solution uses. Include resources configured directly in **Machine Learning** and those created from {{observability}} or {{elastic-sec}} features.

Of the resources covered here, {{es}} {{vectordb}} projects support only [{{infer}} endpoints](#migrate-to-serverless-inference-endpoints), backed by Elastic Inference Service (EIS) or external providers.

In {{observability}} projects, {{ml}} jobs require [Observability Complete](/solutions/observability/observability-serverless-feature-tiers.md). In {{elastic-sec}} projects, they require [Security Analytics Essentials or Complete](/solutions/security/security-serverless-feature-tiers.md). The {{infer}} management UI is unavailable in Observability Logs Essentials.

### Anomaly detection jobs and datafeeds [migrate-to-serverless-anomaly-jobs]
```{applies_to}
serverless:
  vectordb: unavailable
```

[Anomaly detection jobs](/explore-analyze/machine-learning/anomaly-detection.md) learn patterns in time series data and identify unusual behavior. Their datafeeds define which data they analyze. Jobs can be custom or supplied by a solution or integration.

- **Identify:** View source jobs and {{dfeeds}} on **Anomaly Detection Jobs** in {{kib}}, or use the [get anomaly detection jobs API]({{es-apis}}operation/operation-ml-get-jobs) and [get {{dfeeds}} API]({{es-apis}}operation/operation-ml-get-datafeeds).
- **Prepare:** Recreate required filter lists before importing jobs. Missing referenced filter lists cause the import to fail.
- **Migrate:** Recreate unchanged prebuilt jobs from the corresponding [Security](/solutions/security/detect-and-alert/machine-learning.md#ml-job-settings-interface) or [Observability](/solutions/observability/logs/inspect-log-anomalies.md) feature. For custom or modified jobs, follow [Export and import anomaly detection jobs](/explore-analyze/machine-learning/setting-up-machine-learning.md#move-anomaly-detection-jobs). Adapt {{dfeed}} indices and restore calendars and space assignments. Preserve job IDs referenced by rules, or update those references.
- **Verify:** Run jobs and {{dfeeds}} over the intended historical interval and confirm that they process destination data and produce results. Job exports contain configuration only, so imported jobs must rebuild their learned models from that data.

### Data frame analytics jobs [migrate-to-serverless-analytics-jobs]
```{applies_to}
serverless:
  vectordb: unavailable
```

[Data frame analytics jobs](/explore-analyze/machine-learning/data-frame-analytics.md) perform outlier detection, regression, or classification and write the analysis results to a destination index. Regression and classification also produce trained models.

- **Identify:** View source jobs on **Data Frame Analytics Jobs** in {{kib}}, or use the [get data frame analytics jobs API]({{es-apis}}operation/operation-ml-get-data-frame-analytics).
- **Prepare:** Transfer the required source data before importing the jobs.
- **Migrate:** Follow [Export and import data frame analytics jobs](/explore-analyze/machine-learning/setting-up-machine-learning.md#move-dataframe-analytics-jobs), adapting source and destination index references. To retain an existing trained model, transfer it separately as described in [Trained models](#migrate-to-serverless-trained-models).
- **Verify:** Run the required analyses against destination data and check the output indices and results.

### Trained models hosted in the project [migrate-to-serverless-trained-models]
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

### {{infer-cap}} endpoints [migrate-to-serverless-inference-endpoints]

[{{infer-cap}} endpoints](/explore-analyze/elastic-inference.md) provide named access to models hosted in the project, EIS, or external providers.

For embedding generation during migration, review the [data transfer considerations](migrate-to-serverless-transfer-data.md#migrate-to-serverless-transfer-considerations).

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

:::::

## Next step

Continue to [Test and validate the destination](migrate-to-serverless-test-and-validate.md) to verify the complete solution and decide how to proceed.
