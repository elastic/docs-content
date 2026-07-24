---
navigation_title: Field reference
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: kibana
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: cloud-serverless
  - id: elastic-stack
description: Look up the fields in the case analytics indices, including case, activity, and attachment fields and the JSON payload fields.
---

# Case analytics field reference [case-analytics-fields]

This page lists the most useful fields in the three [case analytics indices](case-analytics-indices.md). For the complete, authoritative schema, refer to [Case analytics indices schema](kibana://reference/case-analytics-indices-schema.md).

Field names use the singular `case.*` form, such as `case.status`, even though the index names are plural, such as `.cases`. The `owner`, `space_id`, and `@timestamp` fields sit at the top level instead of under `case.*`.

## General case data (`.cases`) [case-analytics-fields-cases]

The `.cases` index holds one document per case, with the current state of each case.

### Identity [case-analytics-fields-identity]

| Field | Type | Description |
| --- | --- | --- |
| `@timestamp` | date | When {{es}} last wrote this document, which tracks the case's last update. |
| `space_id` | keyword | The space the case belongs to. |
| `owner` | keyword | The owning solution: `securitySolution`, `observability`, or `cases` (Stack Management). |
| `case.id` | keyword | The case ID. Join key for the activity and attachment indices. |
| `case.incremental_id` | unsigned_long | The sequential case number shown in the UI. |

### Core attributes [case-analytics-fields-core]

| Field | Type | Description |
| --- | --- | --- |
| `case.title` | text | Case title. Also indexed as `case.title.keyword` for aggregation and sorting. |
| `case.description` | text | Case description. |
| `case.tags` | keyword | Tags applied to the case. |
| `case.category` | keyword | Case category. |
| `case.status` | keyword | Case status: `open`, `in-progress`, or `closed`. |
| `case.severity` | keyword | Case severity: `low`, `medium`, `high`, or `critical`. |
| `case.assignees.uid` | keyword | Profile IDs of the case's assignees. Join to the `.cases-activity` `actor.*` fields when you need display names. |

### Timestamps and timing metrics [case-analytics-fields-timing]

Timing fields store values in seconds and are `null` until the case reaches the corresponding state. Divide by `3600` for hours.

| Field | Type | Description |
| --- | --- | --- |
| `case.created_at` | date | When the case was created. |
| `case.updated_at` | date | When the case was last updated. |
| `case.in_progress_at` | date | When the case first moved to `in-progress`. |
| `case.closed_at` | date | When the case was closed. `null` while the case is open. |
| `case.duration` | unsigned_long | Total time from open to closed, in seconds. |
| `case.time_to_acknowledge` | long | Time from creation to first moving to `in-progress`, in seconds. |
| `case.time_to_investigate` | long | Time from `in-progress` to resolution, in seconds. |
| `case.time_to_resolve` | long | Time from creation to resolution, in seconds. |

### People [case-analytics-fields-people]

| Field | Type | Description |
| --- | --- | --- |
| `case.created_by.username` | keyword | Username of the case creator. Also includes `.email`, `.full_name`, and `.profile_uid`. |
| `case.updated_by.username` | keyword | Username of the last editor. Also includes `.email`, `.full_name`, and `.profile_uid`. |
| `case.closed_by.username` | keyword | Username of the person who closed the case. Also includes `.email`, `.full_name`, and `.profile_uid`. |

### Counters [case-analytics-fields-counters]

| Field | Type | Description |
| --- | --- | --- |
| `case.total_alerts` | integer | Number of alerts attached to the case. |
| `case.total_comments` | integer | Number of user comments on the case. |
| `case.total_events` | integer | Number of attached events. |
| `case.total_observables` | integer | Number of observables on the case. |

### Template and case fields [case-analytics-fields-template]

| Field | Type | Description |
| --- | --- | --- |
| `case.template.id` | keyword | ID of the template applied when the case was created, if any. |
| `case.template.version` | integer | Version of the applied template. |
| `case.extended_fields` | flattened | Template field values, keyed as `<name>_as_<type>`. Query the keys with `FIELD_EXTRACT` or a `terms` aggregation. Refer to [Analyze case fields](analyze-case-fields.md). |
| `case.customFields.key` | keyword | Key of a legacy custom field. Paired with `.type` and `.value`. |
| `case.customFields.type` | keyword | Legacy custom field type. |
| `case.customFields.value` | keyword | Legacy custom field value, with typed sub-fields `.boolean`, `.date`, `.ip`, `.number`, and `.string`. |

### Connector and external service [case-analytics-fields-connector]

| Field | Type | Description |
| --- | --- | --- |
| `case.connector.id` | keyword | ID of the case's connector. Also includes `.name` and `.type`. |
| `case.external_service.connector_name` | keyword | Name of the external system the case was pushed to, such as ServiceNow. |
| `case.external_service.external_id` | keyword | ID of the incident in the external system. |
| `case.external_service.external_title` | text | Title of the external incident. |
| `case.external_service.pushed_at` | date | When the case was last pushed externally. `.pushed_by.*` records who pushed it. |

### Observables [case-analytics-fields-observables]

| Field | Type | Description |
| --- | --- | --- |
| `case.observables.<type>` | keyword | Observables grouped into a keyword array per type, such as `case.observables.url` and `case.observables.ipv4`. |

## Case activity (`.cases-activity`) [case-analytics-fields-activity]

The `.cases-activity` index holds one document per case action, such as a status change, comment, or template change.

| Field | Type | Description |
| --- | --- | --- |
| `@timestamp` | date | When the action occurred. |
| `space_id` | keyword | The space the action's case belongs to. |
| `owner` | keyword | The owning solution. |
| `case.id` | keyword | ID of the case the action was performed on. Join key back to `.cases`. |
| `actor.username` | keyword | Who performed the action. Also includes `.email`, `.full_name`, and `.profile_uid`. |
| `action.type` | keyword | What was acted on, such as `create_case`, `status`, `severity`, `comment`, `template`, `tags`, `assignees`, or `connector`. |
| `action.verb` | keyword | The action verb, such as `create`, `update`, `delete`, or `add`. |
| `action.status_new` | keyword | The new status, on a status-change action. |
| `action.severity_new` | keyword | The new severity, on a severity-change action. |
| `action.tags_changed` | keyword | Tags added or removed, on a tag-change action. |
| `action.assignees_changed` | keyword | Assignee IDs added or removed, on an assignment action. |
| `action.connector_id_new` | keyword | New connector ID, on a connector-change action. |
| `action.attachment_reference_id` | keyword | ID of the attachment referenced by a comment or attachment action. Join key into `.cases-attachments`. |
| `action.payload_json` | wildcard | The full action payload as a JSON string. Query any sub-field with {{esql}}. |

## Case attachments (`.cases-attachments`) [case-analytics-fields-attachments]

The `.cases-attachments` index holds one document per attachment, such as a comment, alert, file, dashboard, or visualization.

| Field | Type | Description |
| --- | --- | --- |
| `@timestamp` | date | When {{es}} last wrote this document. |
| `space_id` | keyword | The space the attachment's case belongs to. |
| `owner` | keyword | The owning solution. |
| `case.id` | keyword | ID of the case the attachment belongs to. Join key back to `.cases`. |
| `attachment.type` | keyword | Attachment kind, such as `user` (comment), `alert`, `externalReference`, `persistableState`, or `dashboard`. |
| `attachment.attachment_id` | keyword | Referenced entity IDs, such as alert IDs or the saved object ID of an attached dashboard. |
| `attachment.comment` | text | Comment text for comment attachments. Also indexed as `.keyword`. |
| `attachment.alert.rule.id` | keyword | Rule ID for alert attachments. Also includes `attachment.alert.rule.name`. |
| `attachment.alert.indices` | keyword | Indices the attached alerts came from. |
| `attachment.event.indices` | keyword | Indices for event attachments. |
| `attachment.data_json` | wildcard | The full attachment payload as a JSON string. For a dashboard attachment, this holds the serialized dashboard configuration. |
| `attachment.metadata_json` | wildcard | The full attachment metadata as a JSON string. |
| `created_at` | date | When the attachment was added. `created_by.*` records who added it. |
| `updated_at` | date | When the attachment was last edited. `updated_by.*` records who edited it. |
| `pushed_at` | date | When the attachment was pushed to an external service. `pushed_by.*` records who pushed it. |

## JSON payload fields [case-analytics-fields-json]

The `.cases-activity` and `.cases-attachments` indices include dedicated fields for the most common values, and also store each full record as JSON:

* `action.payload_json` holds the full case action payload.
* `attachment.data_json` holds the full attachment payload.
* `attachment.metadata_json` holds the full attachment metadata.

These JSON fields have no length limit. Query them with {{esql}} to reach any detail that doesn't have its own field.
