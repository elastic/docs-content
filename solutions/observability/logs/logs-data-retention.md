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

* [Manage data retention using Streams](#logs-data-retention-streams)
* [Store logs in data streams](#logs-data-retention-data-streams)
* [Customize the built-in `logs@lifecycle` policy](#logs-data-retention-data-streams)
* [Automate rollover based on log volume](#logs-data-retention-automate-rollover)
* [Inspect and manage {{ilm-init}} policies using the {{ilm-init}} API](#logs-data-retention-ilm-api)

## Manage data retention using Streams [logs-data-retention-streams]

[Streams](../streams/streams.md) provides a single, centralized UI within {{kib}} that simplifies common tasks, including setting data retention. The **Retention** tab lets you manage how your stream retains data and provides insight into data ingestion and storage size.

For more on managing data retention through the Streams UI, refer to [Manage data retention for Streams](../streams/management/retention.md).

## Store logs in data streams [logs-data-retention-data-streams]

A data stream lets you store append-only time series data across multiple indices while giving you a single named resource for requests. Data streams also provide the following benefits:

- {{ilm-init}} out of the box to automate the management of the backing indices.
- Automatic rollover to ensure backing indices stay within optimal size and performance limits.
- Tiered storage (hot, warm, and cold phases) to optimize storage and performance.

Refer to the [data stream](/manage-data/data-store/data-streams.md) docs for more information.

## Customize the built-in `logs@lifecycle` policy [logs-data-retention-built-in-ilm]

The `logs@lifecycle` {{ilm-init}} policy is preconfigured for common logging use cases. View or duplicate the policy at **{{stack-manage-app}}** → **Index Lifecycle Policies** or find `Index Lifecycle Policies` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

The logs {{ilm-init}} policy provides a foundation for your logs data streams, but you might need to tailor it to fit your situation. Common modifications include:

- Adjust hot, warm, and cold phase transitions.
- Set retention durations for different phases.
- Update rollover conditions.

Refer to the **[Customize built-in policies tutorial](../../../manage-data/lifecycle/index-lifecycle-management/ilm-tutorials.md)** for more on modifying the logs {{ilm-init}} policy.

% I think we should go more into what modifications are of interest for logs users. What are some scenarios where users might want to adjust their phases or rollover conditions?

## Automate rollover based on log volume [logs-data-retention-automate-rollover]

When continuously indexing timestamped documents, you need to periodically roll over to a new index to ensure that backing indices stay within optimal size and performance limits.

Refer to the [Automate rollover tutorial](../../../manage-data/lifecycle/index-lifecycle-management/ilm-tutorials.md) for more information.

## Use the {{ilm-init}} API [logs-data-retention-ilm-api]

You can also review {{ilm-init}} policies using the `Get lifecycle policies` API.

For example, running `GET /_ilm/policy/logs@lifecycle` pulls up the default logs {{ilm-init}} policy, and shows a result similar to the following:

```json
{
  "logs@lifecycle": {
    "version": 1,
    "modified_date": "2025-05-19T16:45:58.754Z",
    "policy": {
      "phases": {
        "hot": {
          "min_age": "0ms",
          "actions": {
            "rollover": {
              "max_age": "30d",
              "max_primary_shard_size": "50gb"
            }
          }
        }
      },
      "_meta": {
        "description": "default policy for the logs index template installed by x-pack",
        "managed": true
      },
      "deprecated": false
    },
    "in_use_by": {
      "indices": [],
      "data_streams": [],
      "composable_templates": []
    }
  }
}
```

Refer to the [{{ilm-init}} API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ilm) for more information.