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

## Manage data streams in Streams
```{applies_to}
serverless: ga
stack: preview 9.1, ga 9.2
```
Starting with {{stack}} version 9.2, [**Streams**](/solutions/observability/streams/streams.md) provides a centralized interface for managing your data in {{kib}}. It consolidates common data management tasks and eliminates the need for manual configuration of multiple applications and components. A stream directly corresponds to an {{es}} data stream, for example `logs-myapp-default`. Any changes that you make in Streams are automatically propagated to the associated data stream.

:::{image} /manage-data/images/data-stream-management-streams.png
:alt: Streams details
:screenshot:
:::


You can perform the following data management tasks in Streams:
* [define parsing and field extraction logic](ADD LINK to /solutions/observability/streams/management/extract.md) to structure incoming data {applies_to}`"stack": "ga 9.2, preview 9.1"` 
* [configure data retention policies](ADD LINK to /solutions/observability/streams/management/retention.md) {applies_to}`"stack": "ga 9.2, preview 9.1"`
* [manually adjust index settings](ADD LINK to/solutions/observability/streams/management/advanced.md) {applies_to}`"stack": "ga 9.2, preview 9.1"`
* [manage and update field mappings](ADD LINK to/solutions/observability/streams/management/schema.md) {applies_to}`stack: ga 9.2` 
* [identify failed and degraded documents](ADD LINK to/solutions/observability/streams/management/data-quality.md) {applies_to}`stack: ga 9.2`
