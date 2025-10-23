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
To use the entity store, you must have the appropriate privileges. For more information, refer to [Entity risk scoring requirements](entity-risk-scoring-requirements.md).

::::


The entity store allows you to query, reconcile, maintain, and persist entity metadata such as:

* Ingested log data
* Data from integrated identity providers (such as Active Directory, EntraID, and Okta)
* Data from internal and external alerts
* External asset repository data
* Asset criticality data
* Entity risk score data

The entity store can hold any entity type observed by {{elastic-sec}}. It allows you to view and query select entities represented in your indices  without needing to perform real-time searches of observable data. The entity store extracts entities from all indices in the {{elastic-sec}} [default data view](../get-started/data-views-elastic-security.md#default-data-view-security).

When the entity store is enabled, the following resources are generated for each entity type (hosts, users, and services):

* {{es}} resources, such as transforms, ingest pipelines, and enrich policies.
* Data and fields for each entity.
* The `.entities.v1.latest.security_user_<space-id>`, `.entities.v1.latest.security_host_<space-id>`, and `.entities.v1.latest.security_services_<space-id>` indices, which contain field mappings for hosts, users, and services respectively. You can query these indices to see a list of fields that are mapped in the entity store.
* {applies_to}`stack: ga 9.2` {applies_to}`serverless: ga` Snapshot indices (`.entities.v1.history.<ISO_date>.*`) that store daily snapshots of entity data, enabling [historical analysis](/solutions/security/advanced-entity-analytics/view-analyze-risk-score-data.md#historical-entity-analysis) of attributes over time.
* {applies_to}`stack: ga 9.2` {applies_to}`serverless: ga` Reset indices (`.entities.v1.reset.*`) that ensure entity timestamps are updated correctly in the latest index, supporting accurate time-based queries and future data resets.

## Enable entity store [enable-entity-store]

To enable the entity store:

1. Find **Entity Store** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Entity Store** page, turn the toggle on.

Once you enable the entity store, the **Entities** section appears on the following pages:

* {applies_to}`stack: ga 9.1` {applies_to}`serverless: ga` [Entity analytics](/solutions/security/advanced-entity-analytics/overview.md)
* [Entity analytics dashboard](/solutions/security/dashboards/entity-analytics-dashboard.md)

## Clear entity store data [clear-entity-store]

Once the entity store is enabled, you may want to clear the stored data and start fresh. For example, if you normalized the `user.name`, `host.name`, or `service.name` fields, clearing the entity store data would allow you to repopulate the entity store with the updated, normalized values. This action removes all previously extracted entity information, enabling new data extraction and analysis.

Clearing entity store data does not delete your source data, assigned entity risk scores, or asset criticality assignments.

::::{warning}
Clearing entity store data permanently deletes persisted user, host, and service records, and data is no longer available for analysis. Proceed with caution, as this cannot be undone.
::::


To clear entity data:

1. Find **Entity Store** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Entity Store** page, select **Clear**.


## Verify engine status

Once the entity store is enabled, the **Entity Store** page displays the **Engine Status** tab, where you can verify which engines are installed and their statuses. This tab shows a list of installed resources for each installed entity. Click the resource link to navigate to the resource page and view more information.
