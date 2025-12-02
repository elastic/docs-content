---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/logs-data-stream.html
applies_to:
  stack: ga
  serverless: ga
  deployment:
    ess: ga
products:
  - id: elasticsearch
---

# Logs data streams [logs-data-stream]

% TODO confirm serverless behavior
% TODO expand overview and move how-to to a subpage ?


Logs data streams help you store data from logs more efficiently. In benchmarks, log data stored in a logs data stream used ~2.5 times less disk space than a [regular data stream](/manage-data/data-store/data-streams.md), at a small penalty (10-20%) in indexing performance. The exact impact varies by data set and {{es}} version.

## Set up a logs data stream [how-to-use-logsds]

::::{note}
The {{es}} `logsdb` index mode is enabled by default for logs in [{{serverless-full}}](https://www.elastic.co/elasticsearch/serverless).
::::

### Create a logs data stream [create-logsds]

To create a new logs data stream, set your [template](../templates.md) `index.mode` to `logsdb`:

```console
PUT _index_template/my-index-template
{
  "index_patterns": ["my-datastream-*"],
  "data_stream": { },
  "template": {
     "settings": {
        "index.mode": "logsdb" <1>
     }
  },
  "priority": 101 <2>
}
```

1. The `logsdb` index mode setting.
2. The index template priority. By default, {{es}} ships with a `logs-*-*` index template with a priority of 100. To make sure your index template takes priority over the default `logs-*-*` template, set its `priority` to a number higher than 100. For more information, refer to [Avoid index pattern collisions](../templates.md#avoid-index-pattern-collisions).

After the index template is created, new indices that use the template are configured as a logs data stream. You can start indexing data and [using the data stream](use-data-stream.md).

For details on index templates and more settings, refer to [](/manage-data/data-store/index-basics.md#index-management-manage-index-templates).


### Enable logsdb for existing data streams [logsdb-existing-data-streams]

Starting with version `9.0`, `logsdb` index mode is automatically applied to data streams with names matching the pattern `logs-*-*`. For other data streams (in older instances or with names that don't match the `logs-*-*` pattern), you can set `index.mode` to `logsdb` manually in the relevant [template](../templates.md).

::::{tip}
To enable `logsdb` for specific {{product.integrations}}, refer to [](logs-data-stream-integrations.md).
::::

When enabling `logsdb` index mode on a data stream that already exists, make sure to check mappings and sorting. The `logsdb` mode automatically maps `host.name` as a keyword if it's included in the sort settings. If a `host.name` field already exists but has a different type, mapping errors might occur, preventing `logsdb` mode from being fully applied.

To avoid mapping conflicts, consider these options:

* **Adjust mappings:** Check your existing mappings to ensure that `host.name` is mapped as a keyword.
* **Change sorting:** If needed, you can remove `host.name` from the sort settings and use a different set of fields. Sorting by `@timestamp` can be a good fallback.
* **Switch to a different [index mode](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-mode-setting)**: If resolving `host.name` mapping conflicts is not feasible, you can choose not to use `logsdb` mode.


#### Enable `logsdb` mode for all logs data streams in a cluster [enable-logsdb-cluster-wide]

To enable `logsdb` mode for all logs data streams in a cluster, create or modify a component template named `logs@custom` and add the  `index.mode: logsdb` setting. 

::::{important}
To apply your changes, you must [roll over the data stream](../data-streams.md#data-streams-rollover) (automatically or manually).
::::