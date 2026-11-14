---
navigation_title: Process data
description: Add a pipeline to a stream and configure processors that add, change, or remove fields, drop records, or run OTTL statements before data reaches a destination.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Process data before it reaches Elasticsearch

A pipeline is an ordered list of processors that runs on every record passing through it. You add a pipeline on a connection of the Streams Map, between a source and whatever comes next, and the processing runs in Elastic-managed OpenTelemetry Collectors. By the time a record reaches a destination, it has already been changed, and a record a processor dropped never arrives anywhere. Nothing changes in your shippers or in {{es}}.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

Use a pipeline to:

* Add context that every record from a source should carry, such as an environment or team name.
* Drop records you don't want to pay to store, such as debug logs or health-check requests.
* Remove or change fields before they're indexed, including sensitive fields that shouldn't reach any destination.
* Set the `data_stream.dataset` or `data_stream.namespace` attributes that decide which data stream a record lands in.

## How a Streams pipeline differs from an ingest pipeline [streams-process-vs-ingest]

Both change records, but they run in different places and on different terms:

| Aspect | Streams pipeline | {{es}} ingest pipeline |
| --- | --- | --- |
| Runs in | Elastic-managed OpenTelemetry Collectors, outside the cluster | The {{es}} cluster |
| Runs when | Before data reaches any destination | At index time, on data already headed for an index |
| Applies to | Every destination downstream of it, including Amazon S3 and remote deployments | Only the data stream it's attached to |
| Language | OpenTelemetry Transformation Language (OTTL) | Ingest processors and Painless |
| Data model | OTLP: resource, scope, and record | The {{es}} document |

The two aren't exclusive. An ingest pipeline attached to a data stream still runs when Streams hands the record to {{es}}, after any processing on the Streams Map. Processing that must run inside {{es}}, such as the parsing in integration pipelines, stays there. Processing you add to a classic stream is an ingest pipeline and isn't shown on the Map.

## Available processors [streams-process-available]

The list in the **Processing** panel comes from the Streams backend, so it can change without a {{kib}} release. It currently includes:

* [Add fields](processors/add-fields.md): add named fields to a record's body, resource, scope, attributes, or metadata, with a fixed value or an OTTL expression, optionally when a condition holds.
* [Filter](processors/filter.md): drop records that match an OTTL condition.
* [Rename fields](processors/rename-fields.md): give a field a new name in the same location.
* [Set](processors/set.md): write to any field by its OTTL path, including fields of the record itself such as a log's severity or a span's name.
* [Transform](processors/transform.md): run OTTL statements of your choice, for anything the other processors don't cover.

There are no parsing processors, such as Grok, Dissect, or JSON, and no enrichment processors, such as GeoIP. Refer to [Streams limitations](limitations.md#streams-limitations-processing).

Every processor except Filter and Transform takes an optional **Condition**, an OTTL condition that must hold for the processor to act on a record. Without one, the processor acts on every record of the selected signals. To learn what each **Location** means, how to refer to fields, and how to write conditions, refer to [Fields and conditions](fields-and-conditions.md).

If the list is empty, or the panel says it can't edit the processing, refer to [Troubleshooting](troubleshooting.md#streams-troubleshoot-processor-list).

## Add a pipeline and a processor [streams-process-add]

To add a pipeline, you need the **Admin** role.

1. On the Streams Map, hover over the connection where the processing should run, select the {icon}`plus_circle` plus icon that appears on it, then select **Add processing**. A pipeline node appears on the connection and the **Processing** panel opens.
1. Select **Add processor**, then pick a processor from the **Processor** list.
1. Under **Signals**, choose which of **Logs**, **Metrics**, **Traces**, and **Documents** the processor applies to. Only the signals the pipeline carries are offered. A processor that doesn't support a signal can't be applied to it.
1. Configure the processor and select **Create**. The settings differ per processor and are described on the pages listed under [Available processors](#streams-process-available). The processor appears as a card that summarizes its configuration.
1. Select **Save and apply**.

When you create a processor, Streams checks its configuration against the backend first. A processor with errors can't be created, and one with warnings asks you to **Continue anyway**.

:::{warning}
Saved processing applies to live data immediately. There's no way to test a processor against sample data first, so add processors one at a time, start with one whose effect is easy to spot, and check the result in **Discover** before adding the next. A processor that drops records or deletes fields takes effect on data your shippers are sending right now.
:::

## Manage the processors in a pipeline [streams-process-manage]

To open a pipeline, select its node on the Streams Map. In the **Processing** panel, each processor is a card, and processors run top to bottom.

From the panel, you can:

- **Add a processor**: Select {icon}`processor` **Create processor** below the last card.
- **Edit a processor**: Open the {icon}`boxes_vertical` **Step context menu** on its card and select **Edit**. Change the configuration, then select **Update**.
- **Duplicate a processor**: Open the **Step context menu** and select **Duplicate**. The copy appears below the original.
- **Reorder processors**: Open the **Step context menu** and select **Move up** or **Move down**, or drag a card by the {icon}`grab` handle before its name.
- **Delete a processor**: Open the **Step context menu** and select **Delete**.
- **Delete the whole pipeline**: Select the {icon}`trash` **Delete all processors** icon in the panel header and confirm. When you save, the pipeline node disappears from the Map.

None of these changes run until you select **Save and apply**. Until then, new and changed processors are marked **Unsaved**. Select **Cancel** to drop the unsaved changes and keep the last saved pipeline.

If you close the panel with the {icon}`cross` icon or select outside it while you have unsaved changes, Streams asks whether to discard them. Select **Keep editing** to return to the panel, or **Discard changes** to drop them.

## Related pages [streams-process-related]

* [Route data](route-data.md): Add a router to send records to different destinations by condition, or to copy them to more than one.
* [Fields and conditions](fields-and-conditions.md): Learn what each location means, how to refer to fields in OTTL, and how to write conditions.
* [Work with the Streams Map](streams-map.md): Learn how to read the Map, add nodes on connections, connect them, and save your changes.
* [How Streams works](get-started/how-streams-work.md): Understand how sources, pipelines, routers, and destinations fit together.
* [Streams limitations](limitations.md#streams-limitations-processing): Check what processing can't do yet before you plan a pipeline.
* [Troubleshooting](troubleshooting.md#streams-troubleshoot-processor-list): Find out what to do when the processor list is empty or can't be edited.
* [Streams glossary](glossary.md): Look up record, location, context, and the other terms used on this page.
