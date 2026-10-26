---
navigation_title: Alert triage
applies_to:
  stack: ga 9.5+
  serverless: ga
description: Reference for the security.* action steps that let workflows set status, manage assignees, and manage tags on alerts in Elastic Security.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Alert triage action steps [workflows-alert-triage-steps]

Alert triage action steps let workflows manage the alert lifecycle in {{elastic-sec}}. These steps handle status changes, assignments, and tags on individual alerts.

:::{note}
These steps live under the `security.*` step type namespace (for example, `security.setAlertStatus`). They expose explicit input schemas for operations that were previously reachable only through the generic `kibana.request` step, so parameters are validated at save time and discoverable in the Workflows editor.
:::

Use alert triage steps for patterns like:

- Close a batch of false-positive alerts and record a close reason.
- Assign a newly detected alert to an on-call analyst as soon as it's created.
- Tag alerts as escalated before handing off to a case with [`cases.*`](/explore-analyze/workflows/steps/cases.md) steps.

To manage the correlated attacks that group these alerts, use the [Attack triage action steps](/explore-analyze/workflows/steps/attack-triage.md).

## Shared conventions [workflows-alert-triage-conventions]

Every alert triage step shares the same conventions, so once you learn one step the others are predictable.

**All parameters live under `with`.** IDs, status, assignees, and tags are all `with`-level fields. There are no top-level fields specific to this namespace.

**Single or bulk.** The `alert_ids` field accepts either a single string or an array of strings, so one step can target one or many alerts.

**Add/remove is not a full override.** For assignees and tags, existing values are preserved unless explicitly listed in the corresponding `*_to_remove` field. This is the opposite of a "set/replace" operation, so you can't overwrite the full list by sending only `*_to_add`.

**At least one of add/remove is required.** The assign and tags steps (`assignees_to_add`/`assignees_to_remove`, `tags_to_add`/`tags_to_remove`) require at least one of the pair. You can send both in a single step invocation.

:::{note}
The equivalent [attack steps](/explore-analyze/workflows/steps/attack-triage.md) use different parameter names. Attack steps use `ids` instead of `alert_ids` and `reason` instead of `close_reason`.
:::

**Reading current assignees.** To remove specific assignees without clearing the whole list, read the current values from the alert's `kibana.alert.workflow_assignee_ids` field (for example, `{{ event.alerts[0].kibana.alert.workflow_assignee_ids }}` in an alert-triggered workflow) before composing the `assignees_to_remove` list for `security.assignAlert`.

:::{include} ../_snippets/schema-location-legend.md
:::

## Step catalog [workflows-alert-triage-catalog]

The 3 alert triage steps manage the alert lifecycle. Jump to any step:

[`security.setAlertStatus`](#security-setalertstatus) ·
[`security.assignAlert`](#security-assignalert) ·
[`security.setAlertTags`](#security-setalerttags)

---

### `security.setAlertStatus` [security-setalertstatus]

Change the status of one or multiple alerts.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `alert_ids` | `with` | `string` or `string[]` | Yes | A single alert ID or a list of IDs (bulk). |
| `status` | `with` | `string` | Yes | New status for the alerts: `open`, `acknowledged`, or `closed`. |
| `close_reason` | `with` | `string` | No, only valid when `status: closed` | Reason for closing. Predefined values: `false_positive`, `duplicate`, `true_positive`, `benign_positive`, `automated_closure`, `other`. A custom string (max 1024 chars) is also accepted. |

```yaml
- name: close_alerts
  type: security.setAlertStatus
  with:
    alert_ids:
      - 'alert-1'
      - 'alert-2'
    status: 'closed'
    close_reason: 'false_positive'
```

### `security.assignAlert` [security-assignalert]

Assign or unassign users on one or multiple alerts.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `alert_ids` | `with` | `string` or `string[]` | Yes | A single alert ID or a list of IDs (bulk). |
| `assignees_to_add` | `with` | `string[]` (user IDs) | At least one of add/remove | User IDs to assign. |
| `assignees_to_remove` | `with` | `string[]` (user IDs) | At least one of add/remove | User IDs to unassign. |

```yaml
- name: update_alert_assignees
  type: security.assignAlert
  with:
    alert_ids: '{{ variables.alert_id }}'
    assignees_to_add:
      - 'user_id_1'
    assignees_to_remove:
      - 'user_id_2'
```

### `security.setAlertTags` [security-setalerttags]

Add or remove tags on one or multiple alerts.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `alert_ids` | `with` | `string` or `string[]` | Yes | A single alert ID or a list of IDs (bulk). |
| `tags_to_add` | `with` | `string[]` | At least one of add/remove | Tags to add. Existing tags are preserved. |
| `tags_to_remove` | `with` | `string[]` | At least one of add/remove | Tags to remove. |

```yaml
- name: retag_alerts
  type: security.setAlertTags
  with:
    alert_ids:
      - 'alert-1'
      - 'alert-2'
    tags_to_add:
      - 'escalated'
    tags_to_remove:
      - 'needs-review'
```

## Related

- [Security action steps](/explore-analyze/workflows/steps/security.md): Overview of the `security.*` step namespace.
- [Attack triage action steps](/explore-analyze/workflows/steps/attack-triage.md): Status, assignee, and tag management for the correlated attacks that group these alerts.
- [Kibana action steps](/explore-analyze/workflows/steps/kibana.md): The `kibana.SetAlertsStatus` and `kibana.SetAlertTags` steps predate this namespace; the `security.*` steps on this page are now the preferred path for alert triage.
- [Cases action steps](/explore-analyze/workflows/steps/cases.md): Hand off a triaged alert to a case after status, assignee, or tag changes.
- [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md): Run a workflow automatically when a detection rule generates an alert.
