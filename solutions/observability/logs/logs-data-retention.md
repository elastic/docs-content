---
applies_to:
  stack: all
products:
  - id: observability
---

# Configure logs data retention

This page explains how to manage log data retention using index lifecycle management (ILM). You’ll learn about customizing the built-in `logs@lifecycle` policy, automating rollover, and inspecting and managing ILM policies.

## Store logs in data streams

A data stream lets you store append-only time series data across multiple indices while giving you a single named resource for requests. Data streams also provide the following benefits:

- ILM out of the box to automate the management of the backing indices.
- Automatic rollover to ensure backing indices stay within optimal size and performance limits.
- Tiered storage (hot, warm, and cold phases) to optimize storage and performance.

Refer to the [data stream](/manage-data/data-store/data-streams.md) docs for more information.

## Customize the built-in `logs@lifecycle` policy

The `logs@lifecycle` ILM policy is preconfigured for common logging use cases. View or duplicate the policy at **Stack Management** → **Index Lifecycle Policies** or find `Index Lifecycle Policies` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

The logs ILM policy provides a foundation for your logs data streams, but you may need to tailor it to fit your situation. Common modifications include:

- Adjust hot, warm, and cold phase transitions.
- Set retention durations for different phases.
- Update rollover conditions.

Refer to the **[Customize built-in policies tutorial](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md)** for more on modifying the logs ILM policy.

% I think we should go more into what modifications are of interest for logs users. What are some scenarios where users might want to adjust their phases or rollover conditions?

## Automate rollover based on log volume

When continuously indexing timestamped documents, you need to periodically roll over to a new index to ensure that backing indices stay within optimal size and performance limits.

% any logs specific limits or recommendations?

Refer to the [Automate rollover tutorial](/manage-data/lifecycle/index-lifecycle-management/tutorial-automate-rollover.md) for more information.

## Use the ILM API

You can also review ILM policies using the `Get lifecycle policies` API.

For example, running `GET /_ilm/policy/logs@lifecycle` pulls up the default logs ILM policy, and you'll see something like the following:

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

Refer to the [ILM API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ilm) for more information.