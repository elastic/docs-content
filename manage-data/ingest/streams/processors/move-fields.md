---
navigation_title: Move fields processor
description: Move fields of records between locations in a Streams pipeline, such as from attributes to the resource, optionally only when a condition holds.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Move fields processor

The **Move fields** processor takes a field from one location and puts its value in another location, under the same or a different name. Use it when a shipper sets a value in the wrong place, for example an environment name recorded as a log attribute that your dashboards expect as a resource attribute, or to promote a field out of a nested map.

To change a field's name without moving it, use [Rename fields](rename-fields.md).

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Configuration [streams-move-fields-config]

**Condition**
:   An OTTL condition that must hold for the fields to be moved. Without it, they're moved on every record of the selected signals.

**Fields**
:   One row per move. Each row has a *from* line and a *to* line:

    * **Location**: where the field lives now. **Attributes** (the default), **Record**, **Body** (logs only), **Resource**, **Scope**, or **Metadata**, or **Document** when the pipeline carries documents from a Managed _bulk source.
    * **Name**: the field's current name within the location, such as `env`. To reach a key inside a nested map, start the name with a bracket, such as `["labels"]["tier"]`. With **Record**, the name is an OTTL path from the record instead, such as `attributes["env"]`.
    * **New location**: where the value goes, from the same list of locations. It defaults to **Attributes**.
    * **New name**: the name to give the field in its new location, in the same form as **Name**.

    Select **Add item** to add another move.

**Signals**
:   Which of **Logs**, **Metrics**, **Traces**, and **Documents** flowing through the pipeline the processor applies to. Only the signals the pipeline carries are offered, and all of them are selected by default.

## Example [streams-move-fields-example]

Promote an environment name that a shipper records on each log to the resource, under the OpenTelemetry semantic convention name:

| Location | Name | New location | New name |
| --- | --- | --- | --- |
| Attributes | `env` | Resource | `deployment.environment.name` |

## Related pages [streams-move-fields-related]

* [Process data](../process-data.md): Learn how pipelines run and how to add and manage processors.
* [Fields and conditions](../fields-and-conditions.md): Learn what each location means, how to refer to fields in OTTL, and how to write conditions.
* [Rename fields](rename-fields.md): Change a field's name without moving it.
* [Add fields](add-fields.md) and [Set](set.md): Write new fields or new values instead of moving existing fields.
* [Delete fields](delete-fields.md): Remove fields instead of moving them.
