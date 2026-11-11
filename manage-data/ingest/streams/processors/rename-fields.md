---
navigation_title: Rename fields processor
description: Rename fields of records in a Streams pipeline, within their location, optionally only when a condition holds.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Rename fields processor

The **Rename fields** processor gives a field a new name in the same location. Use it to bring attributes from a shipper or an application into the names your dashboards and detection rules expect, for example renaming a custom `env` attribute to `deployment.environment.name`, without a second copy of the data.

To move a field between locations, such as from the record's attributes to the resource, use [Transform](transform.md).

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Configuration [streams-rename-fields-config]

**Condition**
:   An OTTL condition that must hold for the fields to be renamed. Without it, they're renamed in every record of the selected signals.

**Fields**
:   One row per rename. Each row has:

    * **Location**: where the field lives. **Record** (the default), **Body** (logs only), **Resource**, **Scope**, **Attributes**, or **Metadata**, or **Document** when the pipeline carries documents from a Managed _bulk source.
    * **Name**: the field's current name within the location, such as `env`. With **Record**, the name is a path from the record instead. Select one of the suggested paths, such as `attributes["key"]`, `body["key"]`, or `trace_state["key"]`, and replace `key` with the field's name, or type a path.
    * **New name**: the name to give it, in the same form as **Name**.

    Select **Add item** to add another rename.

**Signals**
:   Which of **Logs**, **Metrics**, **Traces**, and **Documents** flowing through the pipeline the processor applies to. Only the signals the pipeline carries are offered, and all of them are selected by default.

## Example [streams-rename-fields-example]

Align a shipper's attribute names with OpenTelemetry semantic conventions:

| Location | Name | New name |
| --- | --- | --- |
| Resource | `env` | `deployment.environment.name` |
| Attributes | `status_code` | `http.response.status_code` |

## Related pages [streams-rename-fields-related]

* [Process data](../process-data.md): Learn how pipelines run, what the locations mean, and how to add and manage processors.
* [Add fields](add-fields.md) and [Set](set.md): Write new fields or new values instead of renaming existing fields.
* [Transform](transform.md): Move a field from one location to another, which Rename fields can't do.
* [Filter](filter.md): Drop whole records instead of changing them.
