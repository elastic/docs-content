---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/pause-export.html
applies_to:
  deployment:
    self: deprecated 7.16.0
products:
  - id: elasticsearch
---


# Pausing data collection [pause-export]

:::{include} _snippets/legacy-warning.md
:::

To stop generating monitoring data in {{es}}, disable data collection:

```yaml
xpack.monitoring.collection.enabled: false
```

When this setting is `false`, {{es}} monitoring data is not collected and all monitoring data from other sources such as {{kib}}, Beats, and Logstash is ignored.

You can update this setting by using the [Cluster Update Settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings).

If you want to collect data from sources such as {{kib}}, Beats, and Logstash but not collect data about your {{es}} cluster, you can disable data collection just for {{es}}:

```yaml
xpack.monitoring.collection.enabled: true
xpack.monitoring.elasticsearch.collection.enabled: false
```

If you want to separately disable a specific exporter, you can specify the `enabled` setting (which defaults to `true`) per exporter. For example:

```yaml
xpack.monitoring.exporters.my_http_exporter:
  type: http
  host: ["10.1.2.3:9200", "10.1.2.4:9200"]
  enabled: false <1>
```

1. Disable the named exporter. If the same name as an existing exporter is not used, then this will create a completely new exporter that is completely ignored. This value can be set dynamically by using cluster settings.


::::{note}
Defining a disabled exporter prevents the default exporter from being created.
::::


To re-start data collection, re-enable these settings.

