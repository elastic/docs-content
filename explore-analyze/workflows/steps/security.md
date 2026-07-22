---
navigation_title: Security
applies_to:
  stack: ga 9.5+
  serverless: ga
description: Reference for Security action steps that enable or disable detection rules from a workflow by rule ID list or KQL query.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Security action steps [workflows-security-steps]

Security action steps let workflows enable or disable {{elastic-sec}} detection rules. Prefer these named `security.*` steps over a generic [`kibana.request`](/explore-analyze/workflows/steps/kibana.md#kibana-request) call when you need to change rule state.

Both steps on this page are authenticated automatically using the permissions or API key of the identity executing the workflow, the same model as the [`kibana.*`](/explore-analyze/workflows/steps/kibana.md) and [`cases.*`](/explore-analyze/workflows/steps/cases.md) steps.

Use Security steps for patterns like:

- Enable a rule (or set of rules) after a maintenance window ends.
- Disable noisy or high-volume rules when a threshold is crossed, then re-enable them later.
- Drive rule lifecycle changes from a scheduled audit or an on-demand manual workflow.

## Shared conventions [workflows-security-conventions]

The rule management steps share the same conventions.

**All parameters live under `with`.** Both `ids` and `query` are `with`-level fields.

**Selector: provide exactly one of `ids` or `query`.** `ids` is an explicit list of rule UUIDs. `query` is a KQL string that selects rules by their attributes.

% SME/eng: confirm whether workflow Save (Zod validation) catches the exactly-one-of refine, or only runtime fails. Source comment in bulk_action_schemas.ts says "workflow validation time"; issue #7352 says runtime-only. First-pass wording below follows the issue.
:::{note}
You must set either `ids` or `query`. The YAML editor does not catch a missing or duplicate selector. If you set both or omit both, the workflow can still save, and the step fails when it runs.
:::

**Use the rule `id` (UUID), not `rule_id`.** The `ids` field takes the rule object's `id`. The list must contain at least one ID. An empty `query` is not allowed because it would match every rule.

**Success and failure.** Rules already in the target state count as **skipped**, not failures. The step succeeds if at least one targeted rule was updated or skipped. Per-rule failures appear in the output `errors` array. The step fails if every targeted rule fails (including when a rule is not found) or another error stops the step.

**Per-rule handling.** To act on the outcome of individual rules, search for the rules first and use a [`foreach`](/explore-analyze/workflows/steps/foreach.md) step to invoke enable or disable once per rule.

:::{include} ../_snippets/schema-location-legend.md
:::

## Step catalog [workflows-security-catalog]

Jump to a step:

**Rules**
[`security.enableRule`](#security-enablerule) ·
[`security.disableRule`](#security-disablerule)

---

## Rules

### `security.enableRule` [security-enablerule]

Enable one or more detection rules by rule ID list or KQL query.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `ids` | `with` | `string[]` (rule UUIDs) | Provide exactly one of `ids`/`query` | Rule `id` UUIDs to enable (at least one). Use the rule `id`, not `rule_id`. |
| `query` | `with` | string (KQL) | Provide exactly one of `ids`/`query` | KQL query selecting the rules to enable. Cannot be empty. |

```yaml
# Enable a single rule by id
- name: enable_rule
  type: security.enableRule
  with:
    ids:
      - "{{ variables.rule_id }}"
```

```yaml
# Enable every rule matching a query
- name: enable_high_severity_rules
  type: security.enableRule
  with:
    query: 'alert.attributes.params.severity: high'
```

### `security.disableRule` [security-disablerule]

Disable one or more detection rules by rule ID list or KQL query.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `ids` | `with` | `string[]` (rule UUIDs) | Provide exactly one of `ids`/`query` | Rule `id` UUIDs to disable (at least one). Use the rule `id`, not `rule_id`. |
| `query` | `with` | string (KQL) | Provide exactly one of `ids`/`query` | KQL query selecting the rules to disable. Cannot be empty. |

```yaml
# Disable a single rule by id
- name: disable_rule
  type: security.disableRule
  with:
    ids:
      - "{{ variables.rule_id }}"
```

```yaml
# Disable every rule matching a query
- name: disable_noisy_rules
  type: security.disableRule
  with:
    query: 'alert.attributes.tags: noisy'
```

## Output reference [workflows-security-rule-output]

Both rule steps return the same summary shape on `steps.<step_name>.output`:

| Field | Type | Description |
|---|---|---|
| `succeeded` | number | Rules whose state changed. |
| `failed` | number | Rules that could not be updated. |
| `skipped` | number | Rules already in the target state (already enabled or already disabled). |
| `total` | number | Total rules targeted. |
| `errors` | array | Included when one or more rules failed. Each entry has `message`, `status_code`, and `rules` (each with `id`; `name` when available). |

Use the summary for branching or logging after the step. For example, check `steps.disable_noisy_rules.output.failed` before notifying an on-call channel.

## Combine with a search and foreach [workflows-security-foreach]

When you need per-rule control, fetch the rule set first (for example with [`kibana.request`](/explore-analyze/workflows/steps/kibana.md#kibana-request)), then loop:

```yaml
- name: find_noisy_rules
  type: kibana.request
  with:
    method: GET
    path: /api/detection_engine/rules/_find
    query:
      filter: 'alert.attributes.tags: "noisy"'
      per_page: 100

- name: disable_each_noisy_rule
  foreach: "${{ steps.find_noisy_rules.output.body.data }}"
  type: security.disableRule
  with:
    ids:
      - "{{ foreach.item.id }}"
```

## Related

- [Manage detection rules at scale](/explore-analyze/workflows/use-cases/security/manage-detection-rules.md): Rule-operations patterns that pair scheduled audits with rule lifecycle steps.
- [Kibana action steps](/explore-analyze/workflows/steps/kibana.md): Generic `kibana.request` for detection engine APIs without a named step.
- [Step type index](/explore-analyze/workflows/reference/step-types.md): Alphabetical lookup of every step type.
- [Choose the right step](/explore-analyze/workflows/authoring-techniques/choose-the-right-step.md): Intent-based guide to picking a step.
- [Manage detection rules](/solutions/security/detect-and-alert/manage-detection-rules.md): The Detection rules UI in {{elastic-sec}}.
