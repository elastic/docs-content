---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/config-monitoring-data-streams-metricbeat-8.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: elasticsearch
---

# Configuring data streams created by Metricbeat 8 [config-monitoring-data-streams-metricbeat-8]

When monitoring using {{metricbeat}}, data is stored in a set of data streams with the following pattern:

```
.monitoring-{{product}}-8-mb
```
For example: 

```
.monitoring-es-8-mb
```

The settings and mappings for these data streams are determined by an index template with the following pattern:

```
.monitoring-{{product}}-mb
```

For example:

```
.monitoring-es-mb
```

You can alter the settings of each data stream by cloning this index template and editing it.

::::{warning} 
You need to repeat this procedure when upgrading the {{stack}} to get the latest updates to the default monitoring index templates.
::::

You can clone index templates in {{kib}}:

* go to the **Index Management** management page in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
* Select **Index Templates**, 
* From the **View** dropdown, select **System templates**.
* Search for the index template.
* Select the **Clone** action.
* Change the name, for example into `custom_monitoring`.
* Set the priority to `500`, to ensure it overrides the default index template.
* Specify the settings you want to change in the `settings` section.
* Save the cloned template.

You can also use the {{es}} API:

* Retrieve the index template using the [get index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-index-template).
* Edit the index template: set the template `priority` to `500`, and specify the settings you want to change in the `settings` section.
* Store the updated index template under a different name, for example `custom_monitoring`, using the [create index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template).

::::{note} 
{{metricbeat}} 8 uses [composable templates](../../../manage-data/data-store/templates.md), rather than legacy templates.
::::

After changing the index template, the updated settings are only applied to the data stream’s new backing indices. [Roll over the data stream](../../../manage-data/data-store/data-streams/use-data-stream.md#manually-roll-over-a-data-stream) to immediately apply the updated settings to the data stream’s write index.