---
description: Reconcile and persist entity metadata from logs, identity providers, and alerts. The entity store powers risk scoring, resolution, and graph visualization.
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/entity-store.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
---

# Entity store [entity-store]

::::{admonition} Requirements
To use the entity store, you must have the appropriate privileges. For more information, refer to [Entity analytics requirements](/solutions/security/advanced-entity-analytics/entity-analytics-requirements.md).

::::


The entity store allows you to query, reconcile, maintain, and persist entity metadata such as:

* Ingested log data
* Data from integrated identity providers (such as Active Directory, EntraID, and Okta)
* Data from internal and external alerts
* External asset repository data
* Asset criticality data
* Entity risk score data

The entity store can hold any entity type observed by {{elastic-sec}}. It allows you to view and query select entities represented in your indices without needing to perform real-time searches of observable data. The entity store extracts entities from all indices in the {{elastic-sec}} [default data view](../get-started/data-views-elastic-security.md#default-data-view-security).

{applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` [Entity resolution](/solutions/security/advanced-entity-analytics/entity-resolution.md) is built on top of the entity store. It links multiple entity records representing the same real-world identity into a resolution group, consolidating their risk scores into a single view.

{applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview` [Entity relationships](/solutions/security/advanced-entity-analytics/entity-relationships.md) sourced from the entity store — such as access patterns, dependencies, and resolution links — are visible in the entity details flyout's [Graph View](/solutions/security/advanced-entity-analytics/view-entity-details.md#visualizations) tab. Entities that appear in both the entity store and in raw events are rendered as a single deduplicated node in the graph.

When the entity store is enabled, the following resources are created for the active space:

:::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: ga }
* A latest entity alias, `entities-latest-<space-id>`, backed by the concrete index `.entities.v2.latest.security_<space-id>-<mapping_version>`. Query this alias to retrieve the current state of all entities in the entity store.
* History snapshot indices, `.entities.v2.history.security_<space-id>.<timestamp>`, which store daily snapshots of entity data and enable [historical analysis](/solutions/security/advanced-entity-analytics/view-analyze-risk-score-data.md#historical-entity-analysis) of entity attributes over time.

:::{note}
Starting in 9.4, the entity store uses {{esql}}-based LOOKUP JOIN queries instead of {{es}} transforms and moves from transform-based indices (`.entities.v1.*`) to ES|QL-based indices (`.entities.v2.*`). When you upgrade from a previous version, existing transforms, enrich policies, and ingest pipelines are removed. Your existing index data is retained. After the entity store is enabled, historical Entity data from logs within the last 3 hours will be extracted.
:::

:::{warning}
:applies_to: {stack: removed 9.4, serverless: removed}
Starting in 9.4, the entity store replaces previous per-type indices with a single shared `latest` alias. Update any direct queries or automations that reference `.entities.v1.latest.security_user_*`, `.entities.v1.latest.security_host_*`, or `.entities.v1.latest.security_service_*` to use `entities-latest-<space-id>` instead. The previous API routes are removed.
:::
::::

::::{applies-item} { stack: ga 9.0-9.3 }
For each entity type (hosts, users, and services):

* {{es}} resources, such as transforms, ingest pipelines, and enrich policies.
* Data and fields for each entity.
* The `.entities.v1.latest.security_user_<space-id>`, `.entities.v1.latest.security_host_<space-id>`, and `.entities.v1.latest.security_services_<space-id>` indices, which contain field mappings for hosts, users, and services respectively. You can query these indices to see a list of fields that are mapped in the entity store.
* {applies_to}`stack: ga 9.2-9.3` Snapshot indices (`.entities.v1.history.<ISO_date>.*`) that store daily snapshots of entity data, enabling [historical analysis](/solutions/security/advanced-entity-analytics/view-analyze-risk-score-data.md#historical-entity-analysis) of attributes over time.
* {applies_to}`stack: ga 9.2-9.3` Reset indices (`.entities.v1.reset.*`) that ensure entity timestamps are updated correctly in the latest index, supporting accurate time-based queries and future data resets.
::::

:::::

## Enable entity store [enable-entity-store]

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }
The entity store is automatically enabled when you turn on risk scoring. In the default {{kib}} space, both are enabled automatically. In non-default spaces, you must enable them manually:

1. Go to the **Entity Analytics** management page. Accessing this page differs based on the [solution view](/deploy-manage/manage-spaces.md#spaces-managing) that you're using:
    * **Security solution view**: Find **{{stack-manage-app}} → Entity Analytics** in the navigation menu.
    * **Classic view**: Find **Manage → Entity Analytics** in the navigation menu.
2. Turn the toggle on.

:::{note}
* If you've upgraded from a previous version, and the entity store was installed in any space, it's automatically migrated after the upgrade. Your existing index data is retained.
* If you use [cross-cluster search](/explore-analyze/cross-cluster-search.md), the entity store ingests logs from every remote cluster. To avoid unnecessary load, turn off risk scoring on any remote cluster where it isn't actively used.
:::
:::

:::{applies-item} { stack: ga 9.0-9.3 }
To enable the entity store:

1. Find **Entity Store** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Turn the toggle on.
:::

::::

Once you enable the entity store, the **Entities** section appears on the following pages:

* {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga` [Entity analytics](/solutions/security/advanced-entity-analytics/monitor-entity-risk.md)
* [Entity analytics dashboard](/solutions/security/dashboards/entity-analytics-dashboard.md)

## Clear entity store data [clear-entity-store]

Once the entity store is enabled, you may want to clear the stored data and start fresh. For example, if you normalized the `user.name`, `host.name`, or `service.name` fields, clearing the entity store data would allow you to repopulate the entity store with the updated, normalized values. This action removes all previously extracted entity information, enabling new data extraction and analysis.

The impact of clearing entity store data on risk scores and asset criticality depends on your version:

:::::{applies-switch}
:::{applies-item} { stack: ga 9.4+, serverless: ga }
Clearing entity store data does not delete your source data. However, asset criticality assignments will need to be reapplied, and risk scoring will run again for the new entities repopulated into the store.
:::
:::{applies-item} { stack: ga 9.0-9.3 }
Clearing entity store data does not delete your source data, assigned entity risk scores, or asset criticality assignments.
:::
:::::

::::{warning}
Clearing entity store data permanently deletes persisted user, host, and service records, and data is no longer available for analysis. Proceed with caution, as this cannot be undone.
::::


To clear entity data:

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }
1. Go to the **Entity Analytics** management page. Accessing this page differs based on the [solution view](/deploy-manage/manage-spaces.md#spaces-managing) that you're using:
    * **Security solution view**: Find **{{stack-manage-app}} → Entity Analytics** in the navigation menu.
    * **Classic view**: Find **Manage → Entity Analytics** in the navigation menu.
2. Click **Clear Entity Data**.
:::

:::{applies-item} { stack: ga 9.0-9.3 }
1. Find **Entity Store** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Clear Entity Data**.
:::

::::


## Verify engine status

Once the entity store is enabled, you can verify which engines are installed and their statuses from the **Engine Status** tab. This tab shows a list of installed resources for each installed entity. Click the resource link to navigate to the resource page and view more information.

::::{applies-switch}

:::{applies-item} { stack: ga 9.4+, serverless: ga }
To access the **Engine Status** tab, find **Entity Analytics** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
:::

:::{applies-item} { stack: ga 9.0-9.3 }
To access the **Engine Status** tab, find **Entity Store** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
:::

::::

## Supported integrations [entity-store-integrations]
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

The entity store creates user, host, and service entities from data in supported source indices (mainly the [Security default data view](/solutions/security/get-started/data-views-elastic-security.md#default-data-view-security)) when the incoming events include the ECS fields needed to identify those entities. Any integration that populates standard ECS identity fields — such as `host.*`, `user.*`, `service.*`, and related `event.*` fields — can contribute to entity creation, as long as the data contains enough information for the entity store to identify and build the entity.

Examples of supported integrations include:

**Identity and account sources:**

* [Active Directory Entity Analytics](integration-docs://reference/entityanalytics_ad.md)
* [Microsoft Entra ID Entity Analytics](integration-docs://reference/entityanalytics_entra_id.md)
* [Okta Entity Analytics](integration-docs://reference/entityanalytics_okta.md)
* [Google Workspace](integration-docs://reference/google_workspace.md)
* [Microsoft 365](integration-docs://reference/o365.md)
* [AWS CloudTrail](integration-docs://reference/aws/cloudtrail.md)

**Endpoint and host sources:**

* [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)
* [CrowdStrike](integration-docs://reference/crowdstrike.md)
* [SentinelOne](integration-docs://reference/sentinel_one.md)
* [Microsoft Defender for Endpoint](integration-docs://reference/microsoft_defender_endpoint.md)

## How entities are created [entity-store-creation-criteria]
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

The entity store creates an entity only when an ingested document contains enough identity information to derive a stable Entity Unique Identifier (EUID). Because [risk scoring](/solutions/security/advanced-entity-analytics/entity-risk-scoring.md), [entity resolution](/solutions/security/advanced-entity-analytics/entity-resolution.md), and [watchlist](/solutions/security/advanced-entity-analytics/watchlists.md) matching apply only to entities that exist in the store, an alert can reference a user or host that does not receive any of this processing if the source document doesn't meet the creation criteria.

Host correlation is more permissive than user correlation, which is why host entities are often created without matching user entities.

### Host entities [entity-store-host-creation]

A host entity is created when a document contains at least one of the following fields. The entity store uses them in the following priority order to derive the host EUID:

1. `host.id`
2. `host.name`
3. `host.hostname`

### User entities [entity-store-user-creation]

A user entity is created through one of two paths:


| Source type | Example integrations | Required identity fields |
| --- | --- | --- |
| Identity and account (IDP) | Okta, Microsoft Entra ID, Active Directory, Microsoft 365 | At least one of `user.email`, `user.id`, `user.name` + `user.domain`, or `user.name` |
| Endpoint telemetry | {{elastic-defend}}, CrowdStrike, SentinelOne | Both `user.name` and `host.id` (the user is treated as a medium-confidence local user tied to that host) |

For identity provider sources, the entity store also factors in the source namespace (for example, `okta`) when deriving the user EUID, so the same identity from different providers stays distinct.

If a document doesn't meet either user creation path, the user might still appear in observed fields or highlighted fields, but it isn't added to the entity store. As a result, that user doesn't receive entity analytics processing such as risk scoring, entity resolution, or watchlist matching. In this situation, it's expected that a host will show a risk score while the associated user shows none.

::::{dropdown} Click for entity creation examples
**A document that creates a user entity (IDP source)**

An alert from an identity source carries account identity fields:

```
event.module: okta
user.email:   jane@acme.com
user.name:    jane
```

Because `event.module` identifies the data as coming from a supported identity provider, and the document carries a qualifying identity field (`user.email`), the entity store derives a user EUID and creates a user entity. That entity is eligible for risk scoring, entity resolution, and watchlist matching.

**A document that does not create a user entity (endpoint telemetry without `host.id`)**

An endpoint alert includes `user.name: jdoe` and `host.name: prod-web-01` but no `host.id`. Because endpoint telemetry requires both `user.name` and `host.id` to create a user entity, no user entity is created. The user may still appear in the alert's observed or highlighted fields, but it doesn't receive risk scoring, entity resolution, or watchlist matching. If the same alert resolves a host entity, the host can show a risk score while the user does not.
::::

## Troubleshoot entity store performance [entity-store-troubleshoot]
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

The entity store runs scheduled log extraction to keep entity data up to date.

To determine whether log extraction is slow or unhealthy, check the **Engine Status** tab or query the [Entity store status API]({{kib-apis}}operation/operation-get-security-entity-store-status).

A process might be **slow** if:

* New entities are not appearing as expected.
* The last successful execution does not appear to advance (`lastExecutionTimestamp`). You can verify this only through the API.

A process might be **unhealthy** if:

* The engine enters an `error` state.
* Component health indicators are degraded.
* Extraction appears stalled and no forward progress is visible.

If log extraction appears slow, you can modify the following log extraction configuration settings to balance freshness, coverage, and query cost. Use the [update entity store API]({{kib-apis}}operation/operation-put-security-entity-store) to apply these settings.

#### `docsLimit`

Use `docsLimit` to control how many entities can be processed in one extraction page.

* Lower it if {{kib}} is consuming too much memory.
* Default: `10000` entities.

#### `excludedIndexPatterns`

Use `excludedIndexPatterns` to exclude specific index patterns from log extraction.

* By default, the entity store extracts entities from all data sources defined in the [default {{elastic-sec}} data view](/solutions/security/get-started/data-views-elastic-security.md#default-data-view-security). Use this parameter to skip patterns that are noisy, irrelevant, or too resource-intensive to process.
* Accepts an array of index pattern strings.

#### `frequency`

Use `frequency` to control how often extraction runs.

* Decrease frequency if extraction is healthy but too resource-intensive and {{es}} CPU utilization is too high. The minimum supported value is `30s`.

#### `maxLogsPerPage`

Use `maxLogsPerPage` to cap the raw-log slice size before aggregation.

* Lower it if queries are too heavy or time-consuming.
* Default: `50000` documents.

Start with `maxLogsPerPage` rather than `docsLimit` when extraction is slow or unstable, because it reduces the amount of raw source data processed in each extraction operation. Adjust `docsLimit` if tuning `maxLogsPerPage` is insufficient and you still see performance issues.

#### `maxLogsPerWindow`

Use `maxLogsPerWindow` to cap the total number of raw log documents processed in a single extraction run, across all slices in the window.

* Lower it if a single task run can still saturate {{es}} CPU even after lowering `maxLogsPerPage`. This is the most effective lever for protecting a cluster from CPU overload, because it bounds the work a single extraction task can do.
* Increase it if cluster CPU is not overloaded and can handle more processed logs.
* Default: `100000` documents.

#### `maxLogsPerWindowCapBehavior`

Use `maxLogsPerWindowCapBehavior` to control what happens when `maxLogsPerWindow` is reached during a run.

* `drop` — the next run advances past the uncapped logs (cursor jumps to the end of the window). Logs above the cap are skipped permanently. Use this to keep the cluster healthy in exchange for coverage gaps when ingest exceeds the cap.
* `defer` — the next run resumes from where the cap fired and processes the remaining logs. Use this to preserve full coverage at the cost of falling behind real time when logs exceed the cap.
* Default: `drop`.

#### `maxTimeWindowSize`

Use `maxTimeWindowSize` to cap the width of each extraction probe window.

* In lagging environments, the extraction window can grow unboundedly, causing probe cost to spiral. Setting this parameter ensures extraction advances through any lag in sequential sub-windows of at most `maxTimeWindowSize` width, rather than querying the full lag in a single pass.
* Increase this value if extraction is falling behind in high-volume deployments.
* Default: `15m`.