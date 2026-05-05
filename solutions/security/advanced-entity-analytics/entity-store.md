---
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
To use the entity store, you must have the appropriate privileges. For more information, refer to [Entity risk scoring requirements](/solutions/security/advanced-entity-analytics/entity-risk-scoring-requirements.md).

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

{applies_to}`stack: preview 9.4+` {applies_to}`serverless: planned` Entity relationships sourced from the entity store — such as access patterns, dependencies, and resolution links — are visible in the entity details flyout's [Graph View](/solutions/security/advanced-entity-analytics/view-entity-details.md#visualizations) tab. Entities that appear in both the entity store and in raw events are rendered as a single deduplicated node in the graph.

When the entity store is enabled, the following resources are created for the active space:

:::::{applies-switch}

::::{applies-item} { stack: ga 9.4+, serverless: planned }
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

1. Find the **Entity Analytics** management page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Turn the toggle on.

:::{note}
If you've upgraded from a previous version, and the entity store was installed in any space, it's automatically migrated after the upgrade. Your existing index data is retained.
:::
:::

:::{applies-item} { stack: ga 9.0-9.3 }
To enable the entity store:

1. Find **Entity Store** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Turn the toggle on.
:::

::::

Once you enable the entity store, the **Entities** section appears on the following pages:

* {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga` [Entity analytics](/solutions/security/advanced-entity-analytics/overview.md)
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
1. Find the **Entity Analytics** management page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
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

## Troubleshoot entity store performance [entity-store-troubleshoot]
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

The entity store runs scheduled log extraction to keep entity data up to date.

To determine whether log extraction is slow or unhealthy, check the **Engine Status** tab or query the Entity store status API.

A process might be **slow** if:

* New entities are not appearing as expected.
* The last successful execution does not appear to advance (`lastExecutionTimestamp`). You can verify this only through the API.

A process might be **unhealthy** if:

* The engine enters an `error` state.
* Component health indicators are degraded.
* Extraction appears stalled and no forward progress is visible.

If log extraction appears slow, you can modify the following log extraction configuration settings to balance freshness, coverage, and query cost.

#### `frequency`

Use `frequency` to control how often extraction runs.

* Decrease frequency if extraction is healthy but too resource-intensive and {{es}} CPU utilization is too high. The minimum supported value is `30s`.

#### `docsLimit`

Use `docsLimit` to control how many entities can be processed in one extraction page.

* Lower it if {{kib}} is consuming too much memory.
* Default: `10000` entities.

#### `maxLogsPerPage`

Use `maxLogsPerPage` to cap the raw-log slice size before aggregation.

* Lower it if queries are too heavy or time-consuming.
* Default: `40000` documents.

Start with `maxLogsPerPage` rather than `docsLimit` when extraction is slow or unstable, because it reduces the amount of raw source data processed in each extraction operation. Adjust `docsLimit` if tuning `maxLogsPerPage` is insufficient and you still see performance issues.
