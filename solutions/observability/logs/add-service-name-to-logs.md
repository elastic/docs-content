---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/add-logs-service-name.html
  - https://www.elastic.co/guide/en/serverless/current/observability-add-logs-service-name.html
---

# Add a service name to logs [observability-add-logs-service-name]

Adding the `service.name` field to your logs associates them with the services that generate them. You can use this field to view and manage logs for distributed services located on multiple hosts.

To add a service name to your logs, either:

* Use the `add_fields` processor through an integration, {{agent}} configuration, or {{filebeat}} configuration.
* Map an existing field from your data stream to the `service.name` field.


## Use the add fields processor to add a service name [observability-add-logs-service-name-use-the-add-fields-processor-to-add-a-service-name]

For log data without a service name, use the [`add_fields` processor](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/add_fields-processor.md) to add the `service.name` field. You can add the processor in an integration’s settings or in the {{agent}} or {{filebeat}} configuration.

For example, adding the `add_fields` processor to the inputs section of a standalone {{agent}} or {{filebeat}} configuration would add `your_service_name` as the `service.name` field:

```console
processors:
    - add_fields:
        target: service
        fields:
            name: your_service_name
```

Adding the `add_fields` processor to an integration’s settings would add `your_service_name` as the `service.name` field:

:::{image} ../../../images/serverless-add-field-processor.png
:alt: Add the add_fields processor to an integration
:class: screenshot
:::

For more on defining processors, refer to [define processors](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/agent-processors.md).


## Map an existing field to the service name field [observability-add-logs-service-name-map-an-existing-field-to-the-service-name-field]

For logs that with an existing field being used to represent the service name, map that field to the `service.name` field using the [alias field type](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/field-alias.md). Follow these steps to update your mapping:

1. find **Stack Management** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Index Templates**.
3. Search for the index template you want to update.
4. From the **Actions** menu for that template, select **edit**.
5. Go to **Mappings**, and select **Add field**.
6. Under **Field type**, select **Alias** and add `service.name` to the **Field name**.
7. Under **Field path**, select the existing field you want to map to the service name.
8. Select **Add field**.

For more ways to add a field to your mapping, refer to [add a field to an existing mapping](../../../manage-data/data-store/mapping/explicit-mapping.md#add-field-mapping).


## Additional ways to process data [observability-add-logs-service-name-additional-ways-to-process-data]

The {{stack}} provides additional ways to process your data:

* **https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest.html[Ingest pipelines]:** convert data to ECS, normalize field data, or enrich incoming data.
* **https://www.elastic.co/guide/en/logstash/current/introduction.html[Logstash]:** enrich your data using input, output, and filter plugins.


% What needs to be done: Align serverless/stateful

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/observability-docs/observability/add-logs-service-name.md
% - [ ] ./raw-migrated-files/docs-content/serverless/observability-add-logs-service-name.md