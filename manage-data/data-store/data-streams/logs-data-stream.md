---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/logs-data-stream.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Logs data streams [logs-data-stream]

Logs data streams help you store data from logs more efficiently. In benchmarks, log data stored in a logs data stream used ~2.5 times less disk space than a [regular data stream](/manage-data/data-store/data-streams.md), at a small penalty (10-20%) in indexing performance. The exact impact varies by data set and {{es}} version.

The `logsdb` index mode is automatically applied to data streams with names matching the pattern `logs-*-*`. In most cases, you won't need to create logs data streams manually.

## Create a logs data stream [create-logsds]

To create a new logs data stream manually, set the corresponding [template](../templates.md) `index.mode` to `logsdb`:

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

After the index template is created, new indices that use the template are configured as a logs data stream. You can start indexing data and [using the data stream](/manage-data/data-store/data-streams/use-data-stream.md).

## Additional resources

* [](/manage-data/data-store/index-basics.md#index-management-manage-index-templates)
* [](/manage-data/data-store/data-streams/logs-data-stream-existing.md)

