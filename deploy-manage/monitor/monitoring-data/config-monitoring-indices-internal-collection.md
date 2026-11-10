---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/config-monitoring-indices-metricbeat-7-internal-collection.html
applies_to:
  deployment:
    self: deprecated 7.16, removed 10.0
products:
  - id: elasticsearch
navigation_title: Legacy collection indices
---

# Configuring stack monitoring indices created by legacy collection

:::{include} ../stack-monitoring/_snippets/legacy-warning.md
:::

To configure the data streams created by {{agent}} or {{metricbeat}}, refer to [](configuring-data-streamsindices-for-monitoring.md).

When monitoring using internal or legacy collection, data is stored in a set of indices called `.monitoring-{{product}}-7-{{date}}`. Internal collection is available for [{{es}}](../stack-monitoring/es-legacy-collection-methods.md), [{{kib}}](../stack-monitoring/kibana-monitoring-legacy.md), and [{{beats}}](beats://reference/filebeat/monitoring-internal-collection.md).

The `7` in the index name is the monitoring template version.

Indices created by {{metricbeat}} 7 are called `.monitoring-{{product}}-7-mb-{{date}}`. If you still have these indices from an earlier version, the same templates and steps apply to them.

The settings and mappings for these indices are determined by [legacy index templates]({{es-apis}}operation/operation-indices-put-template) named `.monitoring-{{product}}`.

You can retrieve these templates in {{kib}}. To manage index templates, go to the **Index Management** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), and then select **Index Templates**, 

You can also use the {{es}} `_template` API:

```console
GET /_template/.monitoring-*
```

To change the settings of the indices, add a custom index template. You can do that in {{kib}}, or using the {{es}} API:

* Set `index_patterns` to match the `.monitoring-{{product}}-7-*` indices.
* Set the template `order` to `1`. This ensures your template is applied after the default template, which has an order of 0.
* Specify the `number_of_shards` and/or `number_of_replicas` in the `settings` section.

```console
PUT /_template/custom_monitoring
{
  "index_patterns": [".monitoring-beats-7-*", ".monitoring-es-7-*", ".monitoring-kibana-7-*", ".monitoring-logstash-7-*"],
  "order": 1,
  "settings": {
    "number_of_shards": 5,
    "number_of_replicas": 2
  }
}
```

After changing the index template, the updated settings are only applied to new indices.
