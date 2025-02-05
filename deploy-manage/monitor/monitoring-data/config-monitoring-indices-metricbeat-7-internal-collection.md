---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/config-monitoring-indices-metricbeat-7-internal-collection.html
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
---

# Configuring indices created by Metricbeat 7 or internal collection [config-monitoring-indices-metricbeat-7-internal-collection]

When monitoring [using {{metricbeat}} 7](../stack-monitoring/collecting-monitoring-data-with-metricbeat.md) or [internal collection](https://www.elastic.co/guide/en/beats/filebeat/current/monitoring-internal-collection.html), data is stored in a set of indices called either:

* `.monitoring-{{product}}-7-mb-{{date}}`, when using {{metricbeat}} 7.
* `.monitoring-{{product}}-7-{{date}}`, when using internal collection.

The settings and mappings for these indices are determined by [legacy index templates](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-templates-v1.html) named `.monitoring-{{product}}`. You can retrieve these templates in {{kib}} by navigating to **Stack Management** > **Index Management** > **Index Templates**, or by using the {{es}} `_template` API:

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

