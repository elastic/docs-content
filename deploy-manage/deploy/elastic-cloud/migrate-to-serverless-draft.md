---
navigation_title: Migrate to Serverless (draft)
description: Assess your existing solution, prepare and test a Serverless project, and plan the move to production.
applies_to:
  serverless: ga
products:
  - id: cloud-serverless
type: how-to
---

# Migrate to {{serverless-full}}

Moving to {{serverless-full}} involves creating a project and adapting your existing solution to it. You can transfer supported user data and export some configuration, while other components require manual setup or redesign. The work involved depends on the features and integrations your solution uses.

Start with understanding your existing solution. The features you use, the way data is ingested, and the applications connected to {{es}} determine what can move directly and what needs to change. Distinguish the assets supplied by Elastic from the configuration and customizations that make them part of your solution.

This guide helps you assess that work, create the destination, prepare and test your solution, and complete the move to production.

% Working outline for local comparison. Develop and verify each section before publication.
% Keep the existing guide intact. Remove the temporary TOC entry before including changes in the PR.
% Reassess the content type after the inventory and migration methods are developed.

## Migration overview [migrate-to-serverless-order]

Assess your existing solution, create the destination project, and prepare and test your solution. Repeat preparation as needed, then complete the migration and switch to production. The preparation section explains how to migrate or recreate each type of asset.

:::{image} /deploy-manage/images/serverless-migration-proposed-order.svg
:alt: Assess the solution and create the destination project. Prepare assets, transfer data, test reads and indexing, and evaluate the destination. Return to preparation to refine or recreate the project, or continue to complete the migration and switch to production.
:::

## Assess your existing solution [migrate-to-serverless-assess]

Understand what your solution needs and how you can reproduce it in {{serverless-short}} before preparing the destination.

### Identify your use cases and destination [migrate-to-serverless-use-cases]

Identify whether your deployment supports search applications, {{observability}}, {{elastic-sec}}, or several use cases. Use the [project type comparison](serverless.md#get-started) to identify the destination project to evaluate.

% TODO: Reuse concise use-case examples from the existing guide where they help identify assets or select a destination.

### Inventory your assets [migrate-to-serverless-inventory]

Build an inventory of what your solution uses and what you need to preserve in the destination. Include the applications and external systems connected to your deployment, as well as the resources stored in {{es}} and {{kib}}. Work with the people who configure and use each part of the solution.

Cover the following areas:

- **User data:** Indices, data streams, and the data they contain.
- **Data structures and processing:** Templates, mappings, aliases, ingest pipelines, and lifecycle configuration.
- **{{kib}} content and feature configuration:** Dashboards, visualizations, rules, integrations, agent policies, and other functionality you use.
- **Access and connections:** Users, roles, credentials, applications, collectors, and external integrations.

Focus the transfer work on your own resources and customizations. Assets managed by Elastic normally do not need to be copied manually: the destination components or integrations create the resources they provide when configured. Record which component supplies each managed asset so you can set it up in the destination. If you modified a managed resource directly, capture those changes separately and review how to apply them through supported customization mechanisms.

Use this inventory when you [prepare and test the destination](#migrate-to-serverless-prepare). That section explains the methods, APIs, Serverless adaptations, and creation prerequisites for each type of asset.

### Check compatibility [migrate-to-serverless-compatibility]

Use [Compare {{ech}} and {{serverless-short}}](differences-from-other-elasticsearch-offerings.md) to check whether your required features and capabilities are available in the destination project. Identify dependencies that need an alternative and any blockers to the migration. The [destination preparation guidance](#migrate-to-serverless-set-up) explains how to adapt individual resources.

## Create the destination project [migrate-to-serverless-create]

Use the [project type comparison](serverless.md#get-started) to select the project type that matches your solution: {{es}}, Elasticsearch Vector Database, {{observability}}, or {{elastic-sec}}.

% TODO: Review and refine the Security feature-tier guidance in this section.

If your solution uses detection rules, select a {{elastic-sec}} project with the Security Analytics Essentials or Complete feature tier. Elastic AI SOC Engine (EASE) does not support detection rules. Review the [Security feature tiers](/solutions/security/security-serverless-feature-tiers.md#sec-subscription-features) and [prebuilt rule customization support](/solutions/security/detect-and-alert/customize-prebuilt-rules.md#customize-subscription-capabilities) to confirm that the selected tier supports the customizations you need to retain.

[Create the destination project](create-serverless-project.md) and [find its connection details](find-connection-details-serverless.md). Configure the [network access](/deploy-manage/security/network-security.md) and credentials needed by your migration tools and test clients. Check access to both {{es}} and {{kib}} from the environments where those tools run.

If your source deployment combines use cases that cannot be supported in a single project, evaluate separate destination projects for those workloads.

## Prepare and test the destination [migrate-to-serverless-prepare]

Use your inventory to migrate or recreate the assets your solution needs in the destination project. The following sections describe the methods, APIs, and tools for each resource type, including compatibility considerations and changes needed to adapt your configuration or data to {{serverless-short}}.

The suggested sequence helps you avoid resource creation errors caused by missing dependencies. You can follow a different sequence, provided you satisfy the creation prerequisites identified for each resource.

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

During preparation, transfer and verify data that no longer changes. You can retain these verified copies when completing the migration, reducing the amount of data to transfer during the final migration window. Leave data that is still changing for that window, unless you have designed and tested an [incremental transfer procedure](#migrate-to-serverless-incremental).

You can start with a subset to validate the process. If you copy data that continues to change, treat that copy as provisional. Before switching to production, replace it with a complete copy taken after source modifications stop, or reconcile all subsequent changes.

#### Select the data to transfer

Identify complete indices that no longer receive new documents, updates, or deletes. For data streams, start with historical backing indices that meet this condition, leaving the current write index for the final window. A backing index is not necessarily immutable after rollover: updates, deletes, and retention can still change its contents.

Record the source indices selected for transfer, their destination names, and which copies you have verified. Use this record to identify the data still pending during the [final transfer](#migrate-to-serverless-final-transfer). If no data is stable, use preparation to test the procedure and perform the definitive copy during the final window.

:::{important}
Do not transfer system indices as user data. The backing indices of your application's data streams are part of its user data, even though their names start with `.ds-`. Identify them through the data stream definition rather than selecting all hidden indices.
:::

#### Select a transfer method [migrate-to-serverless-transfer-documents]

- **{{ech}} to {{serverless-short}}:** Use [reindex from remote](/manage-data/migrate/migrate-data-using-reindex-api.md) when the destination can reach the source. {{es}} transfers the documents directly between the environments, without an intermediate {{ls}} instance.
- **Other sources or transfer requirements:** Use [{{ls}}](/manage-data/migrate/migrate-with-logstash.md), running it on a host that can reach both environments.

Check the [supported source and destination combinations](/manage-data/migrate.md#data-migration-guides-serverless) and the selected method's authentication requirements. You can also reingest data from its original source. User-managed snapshot and restore is unavailable in {{serverless-short}}.

If historical documents have already passed through source ingest pipelines, avoid processing them again during transfer. Check request-selected pipelines and the destination's default and final pipelines. A request's `pipeline=_none` bypasses the default pipeline but does not bypass an `index.final_pipeline`. Refer to [ingest pipeline settings](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-default-pipeline).

#### Migrate regular indices [migrate-to-serverless-regular-indices]

For each source index:

1. Retrieve its definition with [the get index API]({{es-apis}}operation/operation-indices-get), `GET /<source-index>`.
2. [Create the destination index]({{es-serverless-apis}}operation/operation-indices-create) with the source mappings and compatible settings. Omit generated metadata such as the index UUID and creation date, and remove settings managed by {{serverless-short}}, such as shard and replica counts. Replace [{{ilm-init}} configuration](#migrate-to-serverless-lifecycle) where needed. Check the effective destination templates before creating the index.
3. Transfer the documents using the selected method, with this source index and its prepared destination as explicit targets. Preserve document IDs when configuring {{ls}}, as shown in the [example](#migrate-to-serverless-logstash-example).
4. [Verify the copy](#migrate-to-serverless-verify-data), then recreate the [aliases](/manage-data/data-store/aliases.md) your applications use. Check alias filters, routing, and write targets against the destination names.

#### Migrate data streams [migrate-to-serverless-data-streams]

We recommend transferring each source backing index to a separate destination index, verifying the copy, and then adding it to the destination data stream. This keeps a one-to-one correspondence that helps you track and verify transfers across migration phases. Performing these operations manually requires more work, but you can automate the procedure using the APIs and transfer tools.

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

    Omit the internal `_data_stream_timestamp` mapping when creating standalone copies. Association with the destination stream configures it. Keep ingest pipelines off these copy indices so that historical documents are not processed again. Review destination retention separately: document transfer does not preserve source lifecycle state or index age.

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

- **Identify:** List the source spaces with [the get spaces API]({{kib-apis}}operation/operation-get-spaces-space), `GET /api/spaces/space`. Select the spaces your solution needs and record their IDs, names, descriptions, and access requirements.
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

- **Identify:** Select the user-managed cases that you need to retain, and record their attached files, alerts, Timelines, connectors, and Cases configuration.
- **Migrate:** [Export and import cases](/explore-analyze/cases/manage-cases.md#export-import-cases) with saved objects, including related objects. The export includes connectors, user actions, text comments, and supported saved object attachments. It does not include connector secrets, attached files, alerts, or Timelines. If you migrated a connector earlier, retain the existing destination connector when resolving the import conflict instead of overwriting it. Recreate Cases configuration, such as the default connector, custom fields, and templates, separately in the destination.
- **Verify:** Open the imported cases and check their comments, attachments, saved object references, and connectors. Re-authenticate imported connectors when prompted.

#### Maintenance windows [migrate-to-serverless-maintenance-windows]
```{applies_to}
serverless:
  observability: ga
  security: ga
```

Maintenance windows are available in {{observability}} and {{elastic-sec}} projects. They are not included in saved object export and import.

- **Identify:** List the source maintenance windows with the [find maintenance windows API]({{kib-apis}}operation/operation-get-maintenance-window-find), `GET /api/maintenance_window/_find`, and review their schedules, recurrence, filters, and rule scope.
- **Migrate:** Recreate each required window from the **Maintenance Windows** page or with the [create maintenance window API]({{kib-serverless-apis}}operation/operation-post-maintenance-window), `POST /api/maintenance_window`.
- **Verify:** Confirm that each window has the intended status, schedule, recurrence, filters, and effect on rules in the destination.

#### Workflows [migrate-to-serverless-workflows]

Workflows are available across {{serverless-short}} project types with the appropriate feature tier. Migrate user-managed workflows, not managed workflows supplied by Elastic features.

- **Identify:** Inventory the user-managed workflows and record their connectors, referenced resources, triggers, schedules, and dependencies on other workflows.
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

- **Identify:** View source jobs and {{dfeeds}} on **Anomaly Detection Jobs** in {{kib}}, or use the [get anomaly detection jobs API]({{es-apis}}operation/operation-ml-get-jobs) and [get {{dfeeds}} API]({{es-apis}}operation/operation-ml-get-datafeeds). Record job IDs, source indices, and space assignments.
- **Prepare:** Recreate required filter lists before importing jobs. Missing referenced filter lists cause the import to fail.
- **Migrate:** Recreate unchanged prebuilt jobs from the corresponding [Security](/solutions/security/detect-and-alert/machine-learning.md#ml-job-settings-interface) or [Observability](/solutions/observability/logs/inspect-log-anomalies.md) feature. For custom or modified jobs, follow [Export and import anomaly detection jobs](/explore-analyze/machine-learning/setting-up-machine-learning.md#move-anomaly-detection-jobs). Adapt {{dfeed}} indices and restore calendars and space assignments. Preserve job IDs referenced by rules, or update those references.
- **Verify:** Run jobs and {{dfeeds}} over the intended historical interval and confirm that they process destination data and produce results. Job exports contain configuration only, so imported jobs must rebuild their learned models from that data.

#### Data frame analytics jobs [migrate-to-serverless-analytics-jobs]
```{applies_to}
serverless:
  vectordb: unavailable
```

[Data frame analytics jobs](/explore-analyze/machine-learning/data-frame-analytics.md) perform outlier detection, regression, or classification and write the analysis results to a destination index. Regression and classification also produce trained models.

- **Identify:** View source jobs on **Data Frame Analytics Jobs** in {{kib}}, or use the [get data frame analytics jobs API]({{es-apis}}operation/operation-ml-get-data-frame-analytics). Record source indices, destination indices, and any trained models used by your solution.
- **Prepare:** Transfer the required source data before importing the jobs.
- **Migrate:** Follow [Export and import data frame analytics jobs](/explore-analyze/machine-learning/setting-up-machine-learning.md#move-dataframe-analytics-jobs), adapting source and destination index references. To retain an existing trained model, transfer it separately as described in [Trained models](#migrate-to-serverless-trained-models).
- **Verify:** Run the required analyses against destination data and check the output indices and results.

#### Trained models hosted in the project [migrate-to-serverless-trained-models]
```{applies_to}
serverless:
  vectordb: unavailable
```

[Trained models](/explore-analyze/machine-learning/data-frame-analytics/ml-trained-models.md) perform {{infer}} inside your project for tasks such as classification, regression, and text embedding generation. They include models produced by data frame analytics jobs and pretrained NLP models used by ingest pipelines and applications.

- **Identify:** View source models on **{{models-app}}** in {{kib}}, or use the [get trained models API]({{es-apis}}operation/operation-ml-get-trained-models). Record model IDs, deployment IDs, and aliases referenced by your solution.
- **Migrate:** Use the procedure for the model type:

    - For built-in models, [install the corresponding model](/explore-analyze/machine-learning/nlp/ml-nlp-built-in-models.md) in the destination.
    - For custom data frame analytics models, follow [Exporting and importing models](/explore-analyze/machine-learning/data-frame-analytics/ml-trained-models.md#export-import).
    - For custom NLP models, [import the model and vocabulary using {{product.eland}}](/explore-analyze/machine-learning/nlp/ml-nlp-import-model.md), then [start its deployment](/explore-analyze/machine-learning/nlp/ml-nlp-deploy-model.md).

    Preserve referenced IDs and recreate aliases, or update the resources that use them. Serverless model deployments always use [adaptive allocations](/deploy-manage/autoscaling/trained-model-autoscaling.md).

- **Verify:** [Test {{infer}}](/explore-analyze/machine-learning/nlp/ml-nlp-test-inference.md) with the same sample inputs in the source and destination and compare the results. Use the IDs or aliases your pipelines and applications reference.

#### {{infer-cap}} endpoints [migrate-to-serverless-inference-endpoints]

[{{infer-cap}} endpoints](/explore-analyze/elastic-inference.md) provide named access to models hosted in the project, EIS, or external providers.

- **Identify:** View source endpoints on **Elastic Inference** or **External Inference** in {{kib}} (**Inference endpoints** in earlier versions), or use the [get {{infer}} endpoint API]({{es-apis}}operation/operation-inference-get). Record each endpoint's `inference_id`, `task_type`, `service`, and settings.
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

::::{step} Verify the solution with test clients
:anchor: migrate-to-serverless-test

The checks for each asset confirm that individual resources are ready. Use test clients to verify that they work together as a solution before changing production connections. Apply the following checklist to the features you use, using representative data from the copies already transferred and from test ingestion:

- [ ] **Client connections and permissions:** Test at least one instance of each client type used in the source. Run a test application for each client library you use, enroll a test {{agent}} in a destination policy, and test your Beats and Logstash configurations where applicable. Confirm that each client connects, authenticates, and performs its required operations with the intended permissions.
- [ ] **Indexing and processing:** Send representative documents and confirm that they reach the intended indices or data streams with the expected fields and values. Include examples that exercise enrich, inference, and failure handling where applicable. To investigate pipeline processing, use [the simulate pipeline API]({{es-serverless-apis}}operation/operation-ingest-simulate) with documents as they arrive before processing. Test `@custom` extensions through the integration pipeline that calls them.
- [ ] **Application queries:** Run the searches, filters, and aggregations your applications use. Compare source and destination results for the same transferred dataset and time range, accounting for any intentional changes.
- [ ] **Kibana experience:** Open the dashboards and views your users rely on in each required space. Check that they show the expected data and that filters, links, and navigation work with the migrated resources.
- [ ] **Solution features:** Run controlled tests of the rules, workflows, machine learning jobs, and inference features you use. Confirm the expected results and use test destinations for notifications or other external actions.
- [ ] **Performance testing (optional):** If performance is critical to your migration decision, consider additional load testing based on your workload requirements and available testing resources.

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

Monitor production behavior and keep the source available for the agreed rollback period. Retire it after that period and any requirements to retain source data or state have been met.

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
