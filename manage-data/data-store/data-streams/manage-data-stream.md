---
applies_to:
  stack: ga
  serverless: ga
---

# Manage a data stream [index-management-manage-data-streams]

Investigate your data streams and address lifecycle management needs in the **Data Streams** view.

The value in the **Indices** column indicates the number of backing indices. Click this number to drill down into details.

A value in the data retention column indicates that the data stream is managed by a data stream lifecycle policy. This value is the time period for which your data is guaranteed to be stored. Data older than this period can be deleted by {{es}} at a later time.

In {{es-serverless}}, indices matching the `logs-*-*` pattern use the logsDB index mode by default. The logsDB index mode creates a [logs data stream](./logs-data-stream.md).

:::{image} /manage-data/images/serverless-management-data-stream.png
:alt: Data stream details
:screenshot:
:::

* To view more information about a data stream, such as its generation or its current index lifecycle policy, click the stream’s name. From this view, you can navigate to **Discover** to further explore data within the data stream.
* To view information about the stream’s backing indices, click the number in the **Indices** column.
* To modify the data retention value, select a data stream, open the **Manage**  menu, and click **Edit data retention**.

## Manage data streams on the Streams page [manage-data-streams-with-streams]
```{applies_to}
serverless: ga
stack: preview =9.1, ga 9.2+
```
The [**Streams**](/solutions/observability/streams/streams.md) page provides a centralized interface for managing your data in {{kib}}. It consolidates common data management tasks and eliminates the need for manual configuration of multiple applications and components. A stream maps directly to an {{es}} data stream, for example `logs-myapp-default`. Any changes that you make on the **Streams** page are automatically propagated to the associated data stream.

:::{image} /manage-data/images/data-stream-management-streams.png
:alt: The Streams page
:screenshot:
:::


You can perform the following data management tasks on the **Streams** page:
* [define parsing and field extraction logic](/solutions/observability/streams/management/extract.md)
* [configure data retention policies](/solutions/observability/streams/management/retention.md)
* [manually adjust index settings](/solutions/observability/streams/management/advanced.md)
* [manage and update field mappings](/solutions/observability/streams/management/schema.md)
* [identify failed and degraded documents](/solutions/observability/streams/management/data-quality.md)
* [partition data into child streams](/solutions/observability/streams/management/partitioning.md) {applies_to}`stack: preview 9.2+` {applies_to}`serverless: preview`
