---
navigation_title: Add fields processor
description: Add fields to records in a Streams pipeline, with a literal value or an OTTL expression, optionally only when a condition holds.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Add fields processor

The **Add fields** processor writes one or more named fields to a record. Use it when every record from a source should carry a piece of context it doesn't have yet, such as the environment it came from, the team that owns it, or the `data_stream.dataset` that decides where it's indexed. Each field gets a literal value or the result of an OTTL expression, and an optional condition limits the processor to records that match.

Add fields works on fields you name within a location, such as an attribute or a key in the log body. To write to a field of the record itself, such as a log's severity or a span's name, or to address a field by its full OTTL path, use the [Set](set.md) processor.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Configuration [streams-add-fields-config]

**Condition**
:   An OTTL condition that must hold for the fields to be added. Without it, the fields are added to every record of the selected signals. Example: `attributes["http.route"] == "/api/orders"`.

**Fields**
:   One row per field to write. Each row has:

    * **Location**: where the field lives. **Body** (logs only, the default), **Resource**, **Scope**, **Attributes**, or **Metadata**, or **Document** when the pipeline carries documents from a Managed _bulk source.
    * **Name**: the field's name within the location, such as `deployment.environment.name`. To reach a key inside a nested map, add the inner keys in brackets, such as `department["name"]` in the body.
    * **Value**: a literal value, with its type selected from **String**, **Integer**, **Number**, **Boolean**, or **Null**. To use an OTTL expression evaluated for each record instead, such as `Concat([attributes["host.name"], attributes["service.name"]], "/")`, select **Use OTTL value** and enter it in **OTTL value**. A field takes one or the other.
    * **Action**: **Upsert** writes unconditionally. **Update** writes only when the field already exists. **Insert** writes only when the field is absent.

    Select **Add item** to add another field. Drag a field by its handle to reorder, or select the minus icon to remove it.

**Signals**
:   Which of **Logs**, **Metrics**, **Traces**, and **Documents** flowing through the pipeline the processor applies to. Only the signals the pipeline carries are offered, and all of them are selected by default.

## Examples [streams-add-fields-examples]

Tag everything from a source with its environment, in the resource so it's shared by all records:

* **Fields**: Location **Resource**, Name `deployment.environment.name`, Value `production`, Action **Insert**

**Insert** leaves the field alone on records that already name their environment.

Send logs from one service to their own data stream by setting the dataset attribute, with a condition:

* **Condition**: `resource.attributes["service.name"] == "checkout"`
* **Fields**: Location **Attributes**, Name `data_stream.dataset`, Value `checkout`, Action **Upsert**

With an {{es}} destination in Auto index mode, the records then land in `logs-checkout.otel-default`. Refer to [how Auto mode picks a data stream](../destinations/elasticsearch.md#streams-es-destination-auto-data-stream).

## Related pages [streams-add-fields-related]

* [Process data](../process-data.md): Learn how pipelines run, what the locations mean, and how to add and manage processors.
* [Set](set.md): Write to any field by its path, including fields of the record itself such as a log's severity.
* [Rename fields](rename-fields.md): Change a field's name instead of adding a new field.
* [Filter](filter.md): Drop whole records instead of changing them.
* [Transform](transform.md): Change several fields in one step with OTTL statements when a single add isn't enough.
