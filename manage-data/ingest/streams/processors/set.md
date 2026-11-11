---
navigation_title: Set processor
description: Write to any field of a record in a Streams pipeline by its location or full OTTL path, with a literal value or an OTTL expression.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
  stack: unavailable
products:
  - id: kibana
  - id: cloud-serverless
---

# Set processor

The **Set** processor writes a value to a field addressed by its path. It covers everything [Add fields](add-fields.md) does and also reaches fields of the record itself, such as a log record's `severity_text`, a span's `name`, or a metric's `unit`, and any field you can name with a full OTTL path. Use it when the field you need isn't an attribute, or when you want the OTTL context to be explicit.

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Configuration [streams-set-config]

**Condition**
:   An OTTL condition that must hold for the operations to run. Without it, they run on every record of the selected signals.

**Operations**
:   One row per field to write. Each row has:

    * **Location**: the base of the path. **Record** (the default), **Body** (logs only), **Resource**, **Scope**, **Attributes**, or **Metadata**, or **Document** when the pipeline carries documents from a Managed _bulk source. Locations are portable across signals. To address a field through an explicit OTTL context instead, such as **Log**, **Span**, or **Data point**, select **Use Context** and pick the context. To write a full OTTL path, select **Leave unset**.
    * **Path**: the field's path within the location, or a full OTTL path when no location is set. The field suggests the paths known for the chosen location or context, such as `attributes["key"]`, `event_name`, or `trace_id.string`; select one or type your own.
    * **Value**: a literal value, with its type selected from **String**, **Integer**, **Number**, **Boolean**, or **Null**. To use an OTTL expression evaluated in the applicable context instead, select **Use OTTL value** and enter it in **OTTL value**. A field takes one or the other.
    * **Action**: **Upsert** writes unconditionally. **Update** writes only when the field already exists. **Insert** writes only when the field is absent.

    Select **Add item** to add another operation.

**Signals**
:   Which of **Logs**, **Metrics**, **Traces**, and **Documents** flowing through the pipeline the processor applies to. Only the signals the pipeline carries are offered, and all of them are selected by default.

## Examples [streams-set-examples]

Normalize the severity of logs that arrive with a numeric level but no text:

* **Condition**: `severity_text == "" and severity_number >= 17`
* **Operations**: Location **Record**, Path `severity_text`, Value `ERROR`, Action **Upsert**

Copy the trace ID into an attribute so you can filter on it in Discover:

* **Operations**: Location **Attributes**, Path `trace.id`, OTTL value `trace_id.string`, Action **Insert**

Set a span's status message from one of its attributes, with an explicit context:

* **Operations**: select **Use Context** and choose **Span**, Path `status.message`, OTTL value `attributes["error.message"]`, Action **Update**

## Related pages [streams-set-related]

* [Process data](../process-data.md): Learn how pipelines run, what the locations mean, and how to add and manage processors.
* [Add fields](add-fields.md): Use the simpler processor when you only need to add named fields within a location.
* [Rename fields](rename-fields.md): Change a field's name instead of its value.
* [Transform](transform.md): Run OTTL statements of your choice when a single assignment isn't enough.
* [Filter](filter.md): Drop whole records instead of changing them.
