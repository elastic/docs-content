---
navigation_title: Detection rules
applies_to:
  stack: ga 9.5+
  serverless: ga
description: Reference for the security.enableRule and security.disableRule action steps that let workflows enable or disable detection rules in Elastic Security.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Detection rules action steps [workflows-detection-rules-steps]

Detection rules action steps let workflows enable or disable one or more detection rules in {{elastic-sec}} by rule ID list or KQL query. Prefer these named steps over a generic [`kibana.request`](/explore-analyze/workflows/steps/kibana.md#kibana-request) call to the detection engine `_bulk_action` API when you only need to change rule enabled state.

:::{note}
These steps live under the `security.*` step type namespace (`security.enableRule`, `security.disableRule`). They expose an explicit input schema so parameters are discoverable in the Workflows editor, and they report per-rule outcomes in the step output.
:::

Use Detection rules steps for patterns like:

- Enable a newly imported rule as soon as a prerequisite data source is available.
- Disable a noisy rule (or every rule matching a tag query) until an investigation completes.
- Flip rule state from a scheduled health check without hand-writing a bulk-action request.

## Shared conventions [workflows-detection-rules-conventions]

Both Detection rules steps share the same conventions.

**All parameters live under `with`.** Both `ids` and `query` are `with`-level fields — there are no top-level fields specific to these steps.

**Selector: exactly one of `ids` or `query`.** `ids` is an explicit list of rule UUIDs. `query` is a KQL string that selects rules by their attributes. Providing both, or neither, is incorrect.

:::{important}
The "exactly one of `ids` or `query`" constraint is **not** enforced in the YAML editor and is **not** caught when you save the workflow. A definition that provides both, or neither, saves without error and fails only **at runtime** when the step executes.
:::

**Use the rule `id` (UUID), not `rule_id`.** The `ids` field takes the rule object's `id`. It must contain at least one ID. An empty `query` is also rejected (it would otherwise match every rule).

**Idempotent, partial-success semantics.** Rules already in the target state count as **skipped**, not failures. The step **succeeds** when `succeeded + skipped > 0` and reports any per-rule failures in the output `errors` array. It **fails** only when every targeted rule fails (including "rule not found") or a non-recoverable error occurs.

**Per-rule handling.** To act on the outcome of individual rules, run a search first and [`foreach`](/explore-analyze/workflows/steps/foreach.md) over the results, invoking the step once per rule.

:::{include} ../_snippets/schema-location-legend.md
:::

## Step catalog [workflows-detection-rules-catalog]

Jump to either step:

[`security.enableRule`](#security-enablerule) ·
[`security.disableRule`](#security-disablerule)

---

### `security.enableRule` [security-enablerule]

Enable one or more detection rules.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `ids` | `with` | `string[]` (rule UUIDs) | Provide exactly one of `ids`/`query` | Rule `id` UUIDs to enable (at least one). Use the rule `id`, not `rule_id`. |
| `query` | `with` | `string` (KQL) | Provide exactly one of `ids`/`query` | KQL query selecting the rules to enable. Must be non-empty (an empty query would match every rule). |

```yaml
# Enable a single rule by id
- name: enable_rule
  type: security.enableRule
  with:
    ids:
      - '{{ variables.rule_id }}'
```

```yaml
# Enable every rule matching a query
- name: enable_high_severity_rules
  type: security.enableRule
  with:
    query: 'alert.attributes.params.severity: high'
```

### `security.disableRule` [security-disablerule]

Disable one or more detection rules.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `ids` | `with` | `string[]` (rule UUIDs) | Provide exactly one of `ids`/`query` | Rule `id` UUIDs to disable (at least one). Use the rule `id`, not `rule_id`. |
| `query` | `with` | `string` (KQL) | Provide exactly one of `ids`/`query` | KQL query selecting the rules to disable. Must be non-empty (an empty query would match every rule). |

```yaml
# Disable a single rule by id
- name: disable_rule
  type: security.disableRule
  with:
    ids:
      - '{{ variables.rule_id }}'
```

```yaml
# Disable every rule matching a query
- name: disable_noisy_rules
  type: security.disableRule
  with:
    query: 'alert.attributes.tags: noisy'
```

## Output [workflows-detection-rules-output]

Both steps return the same summary object. Use it for branching or logging after the step.

| Field | Type | Description |
|---|---|---|
| `succeeded` | `number` | Rules whose state changed. |
| `failed` | `number` | Rules the step couldn't update. |
| `skipped` | `number` | Rules already in the target state (already enabled or already disabled). |
| `total` | `number` | Total rules targeted. |
| `errors` | `array` | Present only when at least one rule failed. Each entry includes `message`, `status_code`, and `rules` (`id`, and `name` when known). |

## Related

- [Security action steps](/explore-analyze/workflows/steps/security.md): Overview of the `security.*` step namespace.
- [Manage detection rules at scale](/explore-analyze/workflows/use-cases/security/manage-detection-rules.md): Patterns for automating rule-operations work with workflows.
- [Kibana action steps](/explore-analyze/workflows/steps/kibana.md): Generic `kibana.request` for other detection engine bulk actions (for example, `run`).
- [Detection rule concepts](/solutions/security/detect-and-alert/detection-rule-concepts.md): Background on how detection rules work.
