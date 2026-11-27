---
navigation_title: Delete fields processor
description: Remove fields from records in a Streams pipeline before they reach any destination, optionally only when a condition holds.
applies_to:
  serverless:
    elasticsearch: preview
    observability: preview
    security: preview
products:
  - id: kibana
  - id: cloud-serverless
---

# Delete fields processor

The **Delete fields** processor removes named fields from a record. Use it to drop fields you don't want to store, such as a verbose payload or a debugging attribute, or to keep sensitive fields such as tokens and personal data from reaching any destination. Because the pipeline runs before the record reaches a destination, a deleted field isn't indexed, isn't written to Amazon S3, and isn't sent to a remote deployment.

To drop whole records instead of fields, use [Filter](filter.md).

:::{include} /manage-data/ingest/streams/_snippets/private-preview-note.md
:::

## Configuration [streams-delete-fields-config]

**Condition**
:   An OTTL condition that must hold for the fields to be deleted. Without it, they're deleted from every record of the selected signals.

**Fields**
:   One row per location. Each row has:

    * **Location**: where the fields live. **Attributes** (the default), **Record**, **Body** (logs only), **Resource**, **Scope**, or **Metadata**, or **Document** when the pipeline carries documents from a Managed _bulk source.
    * **Names**: one or more field names within the location, such as `env`. To reach a key inside a nested map, start the name with a bracket, such as `["labels"]["tier"]`. With **Record**, each name is an OTTL path from the record instead, such as `attributes["env"]`.

    Select **Add item** to add another location.

**Signals**
:   Which of **Logs**, **Metrics**, **Traces**, and **Documents** flowing through the pipeline the processor applies to. Only the signals the pipeline carries are offered, and all of them are selected by default.

## Example [streams-delete-fields-example]

Keep request bodies and session tokens out of every destination, but only for production records:

* **Condition**: `attributes["deployment.environment.name"] == "prod"`
* **Fields**:

  | Location | Names |
  | --- | --- |
  | Attributes | `http.request.body`, `session.token` |

## Related pages [streams-delete-fields-related]

* [Process data](../process-data.md): Learn how pipelines run and how to add and manage processors.
* [Fields and conditions](../fields-and-conditions.md): Learn what each location means, how to refer to fields in OTTL, and how to write conditions.
* [Filter](filter.md): Drop whole records instead of fields.
* [Move fields](move-fields.md) and [Rename fields](rename-fields.md): Keep a field but change where it lives or what it's called.
* [Transform](transform.md): Delete keys that match a pattern with `delete_matching_keys`, which Delete fields can't do.
