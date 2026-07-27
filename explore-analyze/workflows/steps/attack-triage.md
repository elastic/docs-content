---
navigation_title: Attack triage
applies_to:
  stack: ga 9.5+
  serverless: ga
description: Reference for the security.* action steps that let workflows set status, manage assignees, and manage tags on attacks in Elastic Security.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Attack triage action steps [workflows-attack-triage-steps]

Attack triage action steps let workflows manage the lifecycle of attacks you triage on the [Attacks page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md). This includes status changes, assignments, and tags on the correlated attacks that group related alerts in {{elastic-sec}}.

:::{note}
These steps live under the `security.*` step type namespace (for example, `security.setAttackStatus`). They expose explicit input schemas for operations that were previously reachable only through the generic `kibana.request` step, so parameters are validated at save time and discoverable in the Workflows editor.
:::

Use attack triage steps for patterns like:

- Assign a newly detected attack to an on-call analyst as soon as it's created.
- Tag attacks as escalated before handing off to a case with [`cases.*`](/explore-analyze/workflows/steps/cases.md) steps.
- Close an attack and cascade the same status to every alert correlated with it, in one step.

To manage individual alerts, use the [Alert triage action steps](/explore-analyze/workflows/steps/alert-triage.md).

## Shared conventions [workflows-attack-triage-conventions]

Every attack triage step shares the same conventions, so once you learn one step the others are predictable.

**All parameters live under `with`.** IDs, status, assignees, and tags are all `with`-level fields. There are no top-level fields specific to this namespace.

**Single or bulk.** The `ids` field accepts either a single string or an array of strings, so one step can target one or many attacks.

**Add/remove is not a full override.** For assignees and tags, existing values are preserved unless explicitly listed in the corresponding `*_to_remove` field. This is the opposite of a "set/replace" operation, so you can't overwrite the full list by sending only `*_to_add`.

**At least one of add/remove is required.** The assign and tags steps (`assignees_to_add`/`assignees_to_remove`, `tags_to_add`/`tags_to_remove`) require at least one of the pair. You can send both in a single step invocation.

**Cascade to related alerts.** Every attack step accepts an `update_related_alerts` boolean (default `false`) that also applies the change to the alerts correlated with the attack.

:::{note}
The equivalent [alert steps](/explore-analyze/workflows/steps/alert-triage.md) use different parameter names. Attack steps use `ids` instead of `alert_ids` and `reason` instead of `close_reason`, and alert steps don't have the `update_related_alerts` parameter.
:::

:::{include} ../_snippets/schema-location-legend.md
:::

## Step catalog [workflows-attack-triage-catalog]

The 3 attack triage steps manage the attack lifecycle. Jump to any step:

[`security.setAttackStatus`](#security-setattackstatus) ·
[`security.assignAttack`](#security-assignattack) ·
[`security.setAttackTags`](#security-setattacktags)

---

### `security.setAttackStatus` [security-setattackstatus]

Change the status of one or multiple attacks.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `ids` | `with` | `string` or `string[]` | Yes | A single attack ID or a list of IDs (bulk). |
| `status` | `with` | `string` | Yes | New status for the attacks: `open`, `acknowledged`, or `closed`. |
| `reason` | `with` | `string` | No, only valid when `status: closed` | Reason for closing. Predefined values: `false_positive`, `duplicate`, `true_positive`, `benign_positive`, `automated_closure`, `other`. A custom string (max 1024 chars) is also accepted. |
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

- [Security action steps](/explore-analyze/workflows/steps/security.md): Overview of the `security.*` step namespace.
- [Alert triage action steps](/explore-analyze/workflows/steps/alert-triage.md): Status, assignee, and tag management for individual alerts.
- [Triage and manage attacks](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md): The {{kib}} UI for the attacks these steps automate.
- [Cases action steps](/explore-analyze/workflows/steps/cases.md): Hand off a triaged attack to a case after status, assignee, or tag changes.
- [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md): Run a workflow automatically when a detection rule generates an alert.
