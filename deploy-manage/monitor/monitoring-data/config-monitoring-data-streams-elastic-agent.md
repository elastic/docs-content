---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/config-monitoring-data-streams-elastic-agent.html
applies_to:
  deployment:
    self: all
products:
  - id: elasticsearch
---

# Configuring data streams created by Elastic Agent [config-monitoring-data-streams-elastic-agent]

When [monitoring using {{agent}}](../stack-monitoring/collecting-monitoring-data-with-elastic-agent.md), data is stored in a set of data streams with the following pattern:

```
metrics-{{product}}.stack_monitoring.{{dataset}}-{namespace}
```

For example: 

```
metrics-elasticsearch.stack_monitoring.shard-default
```

The settings and mappings for these data streams are determined by an index template with the following pattern:

```
metrics-{{product}}.stack_monitoring.{{dataset}}
``` 
For example: 

```
metrics-elasticsearch.stack_monitoring.shard
```

To change the settings of each data stream, edit the `metrics-{{product}}.stack_monitoring.{{dataset}}@custom` component template that already exists. You can do this in {{kib}}:


* Go to the **Index Management** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
* Select **Component Templates**.
* Search for the component template.
* Select the **Edit** action.

You can also use the {{es}} API:

* Retrieve the component template using the [get component template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-get-component-template).
* Edit the component template.
* Store the updated component template using the [update component template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template).

After changing the component template, the updated settings are only applied to the data stream’s new backing indices. [Roll over the data stream](../../../manage-data/data-store/data-streams/use-data-stream.md#manually-roll-over-a-data-stream) to immediately apply the updated settings to the data stream’s write index.
