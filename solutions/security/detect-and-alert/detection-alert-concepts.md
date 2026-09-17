---
applies_to:
  stack: ga all
  serverless:
    security: ga all
products:
  - id: security
  - id: cloud-serverless
description: Understand what detection alerts are, where they are stored, how they are generated, and how they differ from external alerts.
---

# Detection alert concepts [detection-alert-concepts]

Detection alerts are the primary output of {{elastic-sec}}'s detection engine. When a detection rule's query matches events in your data, the engine creates alert documents that represent potential threats for analysts to investigate.

## What is a detection alert

A detection alert is an {{es}} document created by the detection engine when a rule finds events matching its criteria. Each alert is a self-contained record that includes:

* **Context from the source event**: ECS fields like `host.name`, `user.name`, `process.name`, and `source.ip` are copied from the original event so analysts can investigate without returning to the raw data.
* **Rule metadata**: The alert captures which rule created it, including the rule name, ID, type, severity, risk score, and MITRE ATT&CK mappings.
* **Workflow fields**: Fields like status, tags, and assignees track the alert through triage and investigation.

Every detection alert has `event.kind` set to `signal`. This distinguishes detection alerts from source events (`event.kind: "event"`) and [external alerts](detection-vs-external-alerts.md) (`event.kind: "alert"`).


## Alert lifecycle [alert-lifecycle]

Every detection alert moves through a lifecycle from creation to resolution:

:::::{stepper}
::::{step} Created
A detection rule runs on its configured schedule and finds events matching its query. The detection engine creates an alert for each match with `kibana.alert.workflow_status` set to `open`. Open alerts appear on the [Alerts page](/solutions/security/detect-and-alert/manage-detection-alerts.md) and are visible to all analysts in the {{kib}} space.
::::
::::{step} Triaged
An analyst reviews the alert and [changes its status](/solutions/security/detect-and-alert/manage-detection-alerts.md#detection-alert-status) to `acknowledged` to signal that investigation is underway. During triage, the analyst can:

- [Assign the alert](/solutions/security/detect-and-alert/manage-detection-alerts.md#assign-users-to-alerts) to a team member
- [Apply tags](/solutions/security/detect-and-alert/manage-detection-alerts.md#apply-alert-tags) for categorization
- [Open the alert in Timeline](/solutions/security/detect-and-alert/manage-detection-alerts.md#signals-to-timelines) for deeper investigation
- [Attach it to a case](/explore-analyze/cases/attach-objects-to-cases.md) for tracking and collaboration
- [Take response actions](/solutions/security/endpoint-response-actions.md) on affected endpoints
::::
::::{step} Resolved
After investigation, the analyst sets the status to `closed` and optionally specifies a [closing reason](/solutions/security/detect-and-alert/manage-detection-alerts.md#detection-alert-status):

- False positive — the alert does not represent a real threat
- True positive — the alert is confirmed malicious activity
- Duplicate — another alert already covers this activity

Closed alerts remain in the alert index and can be reopened if needed.
::::
:::::


## Filtering and searching alerts [alert-filtering]

You can filter and search detection alerts from the [Alerts page](/solutions/security/detect-and-alert/manage-detection-alerts.md) using KQL, drop-down controls, and time range filters. For programmatic access, you can [query the alert index alias directly](/solutions/security/detect-and-alert/query-alert-indices.md). The following sections describe what is and isn't supported when filtering and searching alerts.

### What's supported

| Capability | Details |
|------------|---------|
| KQL on any mapped field | The KQL search bar can query any field that exists in the alert index mappings, including ECS fields (`host.name`, `user.name`) and detection engine fields (`kibana.alert.rule.name`, `kibana.alert.severity`). |
| Drop-down filter controls | Filter by status, severity, user, and host. You can customize these controls (up to 4) and the **Status** control cannot be removed. |
| Assignee and tag filtering | Filter by assigned analysts or alert tags using the controls above the Alerts table or with KQL (`kibana.alert.workflow_tags: "tag-name"`). |
| Time range filtering | Use the date/time picker to scope alerts to a specific window (default: last 24 hours). |
| Sorting | Sort by any sortable field. The default sort is `@timestamp` descending. |
| Grouping | Group alerts by up to three fields (for example, rule name, host, source IP). |
| Building block filter | Toggle building block alerts on or off. By default, they are excluded. |
| Programmatic queries | Query `.alerts-security.alerts-<space-id>` using the {{es}} search API with KQL, ES\|QL, or Query DSL. |

### Known limitations

| Limitation | Details |
|------------|---------|
| Max search page size | Alert search requests return a maximum of 1,000 results per page. To retrieve more, use pagination (for example, `search_after`). |
| Unmapped fields are excluded | Detection alert searches use `include_unmapped: false`. Fields that are not in the alert index mappings are not returned in search results, and filtering on them can produce unexpected results. To add custom fields, use [runtime fields](/solutions/security/get-started/create-runtime-fields-in-elastic-security.md). |
| No sorting in event-rendered view | When the Alerts table is set to **Event rendered view**, sorting is not available. Switch to **Grid view** to sort. |
| Drop-down control limit | A maximum of 4 drop-down filter controls can be displayed above the Alerts table. |
| Filter state is browser-local | Customizations to drop-down filter controls are saved in the browser's local storage, not the user profile. They do not persist across browsers or devices. |
| Alert retention | Alert indices have no delete phase by default. Alerts accumulate indefinitely unless you add a delete phase to the {{ilm-init}} policy. Large alert volumes can affect search performance. Refer to [Retention and rollover](alert-storage-and-schema.md#alert-retention) for details. |


## Learn more

* [Alert storage and schema](alert-storage-and-schema.md): Where alerts are stored and how alert documents are structured
* [How alerts are generated](how-alerts-are-generated.md): The alert generation pipeline, deduplication, limits, and alert types
* [Detection alerts and external alerts](detection-vs-external-alerts.md): How detection alerts differ from third-party external alerts
