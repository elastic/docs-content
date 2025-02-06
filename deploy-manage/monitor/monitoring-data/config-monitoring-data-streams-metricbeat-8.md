---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/config-monitoring-data-streams-metricbeat-8.html
applies:
  hosted: all
  ece: all
  eck: all
  stack: all
---

# Configuring data streams created by Metricbeat 8 [config-monitoring-data-streams-metricbeat-8]

When [monitoring using {{metricbeat}} 8](../stack-monitoring/collecting-monitoring-data-with-metricbeat.md), data is stored in a set of data streams called `.monitoring-{{product}}-8-mb`. For example: `.monitoring-es-8-mb`.

The settings and mappings for these data streams are determined by an index template named `.monitoring-{{product}}-mb`. For example: `.monitoring-es-mb`. You can alter the settings of each data stream by cloning this index template and editing it.

::::{warning} 
You need to repeat this procedure when upgrading the {{stack}} to get the latest updates to the default monitoring index templates.
::::


You can clone index templates in {{kib}}:

* Navigate to **Stack Management** > **Index Management** > **Index Templates**.
* From the **View** dropdown, select **System templates**.
* Search for the index template.
* Select the **Clone** action.
* Change the name, for example into `custom_monitoring`.
* Set the priority to `500`, to ensure it overrides the default index template.
* Specify the settings you want to change in the `settings` section.
* Save the cloned template.

You can also use the {{es}} API:

* Retrieve the index template using the [get index template API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-get-template.html).
* Edit the index template: set the template `priority` to `500`, and specify the settings you want to change in the `settings` section.
* Store the updated index template under a different name, for example `custom_monitoring`, using the [create index template API](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-template.html).

::::{note} 
{{metricbeat}} 8 uses [composable templates](../../../manage-data/data-store/templates.md), rather than legacy templates.
::::


After changing the index template, the updated settings are only applied to the data stream’s new backing indices. [Roll over the data stream](../../../manage-data/data-store/index-types/use-data-stream.md#manually-roll-over-a-data-stream) to immediately apply the updated settings to the data stream’s write index.

