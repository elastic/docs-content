---
navigation_title: Attack triage
applies_to:
  stack: ga 9.5+
  serverless: ga
description: Reference for the security.* action steps that let workflows set status, manage assignees, and manage tags on alerts and attacks in Elastic Security.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Attack triage action steps [workflows-attack-triage-steps]

Attack triage action steps let workflows manage the same alert and attack lifecycle you triage on the [Attacks page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md), including status changes, assignments, and tags on individual alerts and on the correlated attacks that group them, in {{elastic-sec}}.

:::{note}
These steps live under the `security.*` step type namespace (for example, `security.setAlertStatus`, `security.setAttackStatus`). They expose explicit input schemas for operations that were previously reachable only through the generic `kibana.request` step, so parameters are validated at save time and discoverable in the Workflows editor.
:::

Use Attack triage steps for patterns like:

- Close a batch of false-positive alerts and record a close reason.
- Assign a newly detected attack to an on-call analyst as soon as it's created.
- Tag alerts as escalated before handing off to a case with [`cases.*`](/explore-analyze/workflows/steps/cases.md) steps.
- Close an attack and cascade the same status to every alert correlated with it, in one step.

## Shared conventions [workflows-attack-triage-conventions]

Every `security.*` step shares the same conventions, so once you learn one step the others are predictable.

**All parameters live under `with`.** IDs, status, assignees, and tags are all `with`-level fields — there are no top-level fields specific to this namespace.

**Single or bulk.** Every ID field accepts either a single string or an array of strings, so one step can target one or many alerts or attacks.

**Add/remove is not a full override.** For assignees and tags, existing values are preserved unless explicitly listed in the corresponding `*_to_remove` field. This is the opposite of a "set/replace" operation — you can't overwrite the full list by sending only `*_to_add`.

**At least one of add/remove is required.** The assign and tags steps (`assignees_to_add`/`assignees_to_remove`, `tags_to_add`/`tags_to_remove`) require at least one of the pair. You can send both in a single step invocation.

:::{important}
Parameter naming differs between the alert steps and the attack steps. Document and use these exactly as implemented — don't normalize the names:

- Alert steps use `alert_ids`; attack steps use `ids`.
- The alert close-reason field is `close_reason`; the attack close-reason field is `reason`.
- Attack steps have an extra `update_related_alerts` boolean (default `false`); alert steps don't have this parameter.
:::

**Reading current assignees.** To remove specific assignees without clearing the whole list, read the current values from the alert's `kibana.alert.workflow_assignee_ids` field (for example, `{{ event.alerts[0].kibana.alert.workflow_assignee_ids }}` in an alert-triggered workflow) before composing the `assignees_to_remove` list for `security.assignAlert`.

:::{include} ../_snippets/schema-location-legend.md
:::

## Step catalog [workflows-attack-triage-catalog]

The 6 Attack triage steps group by target: alerts or attacks. Jump to any step:

**Alerts**
[`security.setAlertStatus`](#security-setalertstatus) ·
[`security.assignAlert`](#security-assignalert) ·
[`security.setAlertTags`](#security-setalerttags)

**Attacks**
[`security.setAttackStatus`](#security-setattackstatus) ·
[`security.assignAttack`](#security-assignattack) ·
[`security.setAttackTags`](#security-setattacktags)

---

## Alerts

### `security.setAlertStatus` [security-setalertstatus]

Change the status of one or multiple alerts.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `alert_ids` | `with` | `string` or `string[]` | Yes | A single alert ID or a list of IDs (bulk). |
| `status` | `with` | `open` \| `acknowledged` \| `closed` | Yes | New status for the alerts. |
| `close_reason` | `with` | string | No — only valid when `status: closed` | Reason for closing. Predefined values: `false_positive`, `duplicate`, `true_positive`, `benign_positive`, `automated_closure`, `other`; a custom string (max 1024 chars) is also accepted. |

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

---

## Attacks

### `security.setAttackStatus` [security-setattackstatus]

Change the status of one or multiple attacks.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `ids` | `with` | `string` or `string[]` | Yes | A single attack ID or a list of IDs (bulk). |
| `status` | `with` | `open` \| `acknowledged` \| `closed` | Yes | New status for the attacks. |
| `reason` | `with` | string | No — only valid when `status: closed` | Reason for closing (same predefined values or custom string as `close_reason` above). |
| `update_related_alerts` | `with` | boolean | No (default `false`) | Also apply the status change to alerts related to the attack. |

```yaml
- name: close_attacks
  type: security.setAttackStatus
  with:
    ids:
      - 'attack-1'
      - 'attack-2'
    status: 'closed'
    reason: 'false_positive'
    update_related_alerts: true
```

### `security.assignAttack` [security-assignattack]

Assign or unassign users on one or multiple attacks.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `ids` | `with` | `string` or `string[]` | Yes | A single attack ID or a list of IDs (bulk). |
| `assignees_to_add` | `with` | `string[]` (user IDs) | At least one of add/remove | User IDs to assign. |
| `assignees_to_remove` | `with` | `string[]` (user IDs) | At least one of add/remove | User IDs to unassign. |
| `update_related_alerts` | `with` | boolean | No (default `false`) | Also apply the assignment change to related alerts. |

```yaml
- name: assign_attack
  type: security.assignAttack
  with:
    ids: '{{ variables.attack_id }}'
    assignees_to_add:
      - 'user_id_1'
```

### `security.setAttackTags` [security-setattacktags]

Add or remove tags on one or multiple attacks.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `ids` | `with` | `string` or `string[]` | Yes | A single attack ID or a list of IDs (bulk). |
| `tags_to_add` | `with` | `string[]` | At least one of add/remove | Tags to add. Existing tags are preserved. |
| `tags_to_remove` | `with` | `string[]` | At least one of add/remove | Tags to remove. |
| `update_related_alerts` | `with` | boolean | No (default `false`) | Also apply the tag change to related alerts. |

```yaml
- name: retag_attacks
  type: security.setAttackTags
  with:
    ids:
      - 'attack-1'
      - 'attack-2'
    tags_to_add:
      - 'escalated'
    tags_to_remove:
      - 'needs-review'
    update_related_alerts: true
```

## Related

- [Triage and manage attacks](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md): The {{kib}} UI for the alerts and attacks these steps automate.
- [Kibana action steps](/explore-analyze/workflows/steps/kibana.md): The `kibana.SetAlertsStatus` and `kibana.SetAlertTags` steps predate this namespace; the `security.*` steps on this page are now the preferred path for alert triage.
- [Cases action steps](/explore-analyze/workflows/steps/cases.md): Hand off a triaged alert or attack to a case after status, assignee, or tag changes.
- [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md): Run a workflow automatically when a detection rule generates an alert.
