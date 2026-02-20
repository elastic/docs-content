---
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: observability
---

# Configure logs data retention

Your data retention policies define how long {{es}} keeps your log data before automatically removing it. Setting an appropriate data retention period helps manage storage costs and keeps your log data manageable.

Manage log data retention in the following ways:

* [Manage log data retention in Streams](#logs-data-retention-streams)
* [Manage log data retention in data streams](#logs-data-retention-data-streams)

## Manage data retention using Streams [logs-data-retention-streams]
```{applies_to}
stack: ga 9.2+
```

[Streams](../streams/streams.md) provides a single, centralized UI within {{kib}} that simplifies common tasks, including setting data retention. The **Retention** tab lets you manage how your stream retains data and provides insight into data ingestion and storage size.

For more on managing data retention through the Streams UI, refer to [Manage data retention for Streams](../streams/management/retention.md).

## Manage data retention in data streams [logs-data-retention-data-streams]

A data stream lets you store append-only time series data across multiple indices while giving you a single named resource for requests. Data streams also provide the following benefits:

- {{ilm-init}} out of the box to automate the management of the backing indices.
- Automatic rollover to ensure backing indices stay within optimal size and performance limits.
- Tiered storage (hot, warm, and cold phases) to optimize storage and performance.

Refer to the [data stream lifecycle](/manage-data/lifecycle/data-stream.md) docs for more information.

### Customize the built-in `logs@lifecycle` policy [logs-data-retention-built-in-ilm]

The `logs@lifecycle` {{ilm-init}} policy is preconfigured for common logging use cases. View or duplicate the policy at **{{stack-manage-app}}** → **Index Lifecycle Policies** or find `Index Lifecycle Policies` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

The logs {{ilm-init}} policy provides a foundation for your logs data streams, but you might need to tailor it to fit your situation. Common modifications include:

- Adjust hot, warm, and cold phase transitions.
- Set retention durations for different phases.
- Update rollover conditions.

Refer to the **[Customize built-in policies tutorial](../../../manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md))** for more on modifying the logs {{ilm-init}} policy.

### Automate rollover based on log volume [logs-data-retention-automate-rollover]

When continuously indexing timestamped documents, you need to periodically roll over to a new index to ensure that backing indices stay within optimal size and performance limits.

Refer to the [Automate rollover tutorial](../../../manage-data/lifecycle/index-lifecycle-management/ilm-tutorials.md) for more information.

### Update data stream retention using the data stream lifecycles APIs

You can get information about a data stream lifecycle and modify it using the {{kib}} **Index Management** tools or the {{es}} [lifecycle API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-data-lifecycle). Refer to [Update the lifecycle of a data stream](../../../manage-data/lifecycle/data-stream/tutorial-update-existing-data-stream.md) for more information.