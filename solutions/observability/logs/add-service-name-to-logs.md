---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/add-logs-service-name.html
  - https://www.elastic.co/guide/en/serverless/current/observability-add-logs-service-name.html
applies_to:
  stack: all
  serverless: all
products:
  - id: observability
  - id: cloud-serverless
---

# Add a service name to logs [observability-add-logs-service-name]

Adding the `service.name` field to your logs associates them with the services that generate them. You can use this field to view and manage logs for distributed services located on multiple hosts.

To add a service name to your logs, either:

* Use the `add_fields` processor through an integration, {{agent}} configuration, or {{filebeat}} configuration.
* Map an existing field from your data stream to the `service.name` field.


## Use the add fields processor to add a service name [observability-add-logs-service-name-use-the-add-fields-processor-to-add-a-service-name]

For log data without a service name, use the [`add_fields` processor](/reference/fleet/add_fields-processor.md) to add the `service.name` field. You can add the processor in an integration’s settings or in the {{agent}} or {{filebeat}} configuration.

For example, adding the `add_fields` processor to the inputs section of a standalone {{agent}} or {{filebeat}} configuration would add `your_service_name` as the `service.name` field:

```console
processors:
    - add_fields:
        target: service
        fields:
            name: your_service_name
```

Adding the `add_fields` processor to an integration’s settings would add `your_service_name` as the `service.name` field:

:::{image} /solutions/images/serverless-add-field-processor.png
:alt: Add the add_fields processor to an integration
:screenshot:
:::

For more on defining processors, refer to [define processors](/reference/fleet/agent-processors.md).


## Map an existing field to the service name field [observability-add-logs-service-name-map-an-existing-field-to-the-service-name-field]

For logs that with an existing field being used to represent the service name, map that field to the `service.name` field using the [alias field type](elasticsearch://reference/elasticsearch/mapping-reference/field-alias.md). Follow these steps to update your mapping:

1. Find the **Index Management** page in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Index Templates**.
3. Search for the index template you want to update.
4. From the **Actions** menu for that template, select **edit**.
5. Go to **Mappings**, and select **Add field**.
6. Under **Field type**, select **Alias** and add `service.name` to the **Field name**.
7. Under **Field path**, select the existing field you want to map to the service name.
8. Select **Add field**.

For more ways to add a field to your mapping, refer to [add a field to an existing mapping](/manage-data/data-store/mapping/explicit-mapping.md#add-field-mapping).


## Additional ways to process data [observability-add-logs-service-name-additional-ways-to-process-data]

The {{stack}} provides additional ways to process your data:

* **[Ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md):** convert data to ECS, normalize field data, or enrich incoming data.
* **[Logstash](logstash://reference/index.md):** enrich your data using input, output, and filter plugins.