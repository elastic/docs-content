---
navigation_title: Exceptions
applies_to:
  stack: ga 9.6+
  serverless: ga
description: Reference for the security.createRuleException and security.createExceptionListItem action steps that let workflows add exceptions in Elastic Security.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Exceptions action steps [workflows-exceptions-steps]

Exception action steps let workflows add [exception items](/solutions/security/detect-and-alert/rule-exceptions.md) in {{elastic-sec}}, so matching events stop generating alerts. Use these named steps instead of a generic [`kibana.request`](/explore-analyze/workflows/steps/kibana.md#kibana-request) call to the exceptions API.

:::{note}
These steps live under the `security.*` step type namespace. They expose an explicit input schema, so parameters are validated at save time and discoverable in the Workflows editor.
:::

Both steps create the same kind of exception item. They differ in which list the item lands on, and therefore in how many rules it affects.

| Step | Where the item lands | What it affects |
|---|---|---|
| [`security.createRuleException`](#security-createruleexception) | The rule's own default exception list: the list that belongs to one rule and isn't shared with any other. The step creates that list if the rule doesn't have one yet. | Only that rule. |
| [`security.createExceptionListItem`](#security-createexceptionlistitem) | An existing exception list that you identify by `list_id`, usually a [shared exception list](/solutions/security/detect-and-alert/create-manage-shared-exception-lists.md). The step fails if the list doesn't exist. | Every rule linked to that list. |

Use these steps for patterns like:

- Exclude a known-good host from a noisy rule during a maintenance window.
- Add a reviewed IP address to a shared allowlist that several rules use.
- Create a temporary exception from an alert, with an expiration time.
- Re-run the same suppression workflow without duplicating the exception item.

## Shared conventions [workflows-exceptions-conventions]

Both exception steps share the same conventions.

**All parameters live under `with`.** There are no top-level fields specific to these steps.

**Detection rules have two identifiers.** The `rule_id` parameter on `security.createRuleException` takes the rule object's `id` (a UUID, at most 36 characters), not the rule's `rule_id` field. On an alert, that UUID is `kibana.alert.rule.uuid`.

% Reviewer check (remove before merge): is there a supported UI path for finding a rule's `id` that we should link here?

**Each entry pairs a `field` with an `operator`.** The operators match the operator labels you select when you build an exception in {{elastic-sec}}.

| Operator | Operand | Notes |
|---|---|---|
| `is`, `is_not` | `value` (string) | Exact match. |
| `matches`, `does_not_match` | `value` (string) | Supports `*` and `?` wildcards. |
| `is_one_of`, `is_not_one_of` | `values` (string array) | Match any listed value. |
| `exists`, `does_not_exist` | none | Don't set `value`, `values`, or `list`. |
| `is_in_list`, `is_not_in_list` | `list.id` and `list.type` | Match against a [value list](/solutions/security/detect-and-alert/create-manage-value-lists.md), a saved set of values such as IP addresses or keywords. `list.id` is the value list's ID, and `list.type` is its {{es}} data type, such as `keyword` or `ip`. |

**A value-list entry can't mix with other entry types in the same item.** If any entry uses `is_in_list` or `is_not_in_list`, every entry in that item must.

**`entries` is a logical AND.** Every entry of an item must match for the exception to apply. Create a separate item for each alternative (OR) condition.

**Nested conditions aren't supported.** Fields mapped as `nested` in the source indices, mostly Endpoint objects, can't be targeted from these steps. Add those exceptions in the {{elastic-sec}} UI or through the API. Refer to [Exception types and value syntax](/solutions/security/manage-elastic-defend/exception-types-and-syntax.md).

**`expire_time` makes the exception temporary.** When set, it's an ISO 8601 datetime after which the exception no longer applies. Omit it for an exception that doesn't expire.

**Provide `item_id` when the workflow might run more than once.** If you omit `item_id`, the API assigns a new random identifier on every run, so a retry, a scheduled trigger, or a loop creates a duplicate exception item. When `item_id` is set and an item with that identifier already exists on the target list, the step skips creation and returns the existing item, or updates it when `overwrite` is `true`. `overwrite: true` requires `item_id`. Providing `overwrite` without `item_id` fails validation.

**Creating, skipping, and overwriting all count as success.** The `outcome` output field reports which one happened, so later steps can branch on it. The step fails only on an error, such as a missing rule or list.

**On overwrite, existing comments are preserved.** The steps don't send `comments` when they update an item, because the API appends them as new comments. Other item fields are replaced.

:::{important}
`item_id` isn't scoped to a particular list. If an item with that `item_id` already exists on a list other than the one the step targets, the step fails rather than skipping, overwriting, or creating a duplicate. The error names the list that holds the conflicting item. Use a different `item_id` in that case.
:::

The identity that runs the workflow must be able to manage exceptions. Refer to [Exception privileges](/solutions/security/detect-and-alert/add-manage-exceptions.md#exceptions-requirements) and [Workflow authorization](/explore-analyze/workflows/authorization.md).

The examples on this page use [Liquid templating](/explore-analyze/workflows/templating.md) to pull values from the workflow's context. `consts.*` values are constants declared at the top of the workflow, `variables.*` values come from an earlier [`data.set`](/explore-analyze/workflows/steps/data.md#data-set) step, and `event.*` is available only in an alert-triggered or event-driven workflow. Refer to [Context variables](/explore-analyze/workflows/reference/context-variables.md).

:::{include} ../_snippets/schema-location-legend.md
:::

## Step catalog [workflows-exceptions-catalog]

Jump to either step:

[`security.createRuleException`](#security-createruleexception) ·
[`security.createExceptionListItem`](#security-createexceptionlistitem)

---

### `security.createRuleException` [security-createruleexception]

Add an exception item to a detection rule's own default exception list. The exception affects only that rule.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `rule_id` | `with` | `string` (rule UUID) | Yes | The rule object's `id` (UUID), not `rule_id`. On an alert, use `kibana.alert.rule.uuid`. The rule's default exception list is created automatically if it doesn't exist yet. |
| `item_id` | `with` | `string` | No | Stable identifier for idempotency. Omit only when a duplicate item on every run is acceptable. |
| `overwrite` | `with` | `boolean` | No (default `false`) | When `true` and `item_id` already exists on this rule's default list, update that item instead of skipping. Requires `item_id`. |
| `name` | `with` | `string` | Yes | Exception item name. |
| `description` | `with` | `string` | Yes | Exception item description. |
| `entries` | `with` | `array` | Yes (at least 1) | Match conditions for the item. Refer to [Shared conventions](#workflows-exceptions-conventions). |
| `os_types` | `with` | `string[]` | No | OS types the exception applies to: `linux`, `macos`, or `windows`. |
| `tags` | `with` | `string[]` | No | Tags for the item. |
| `expire_time` | `with` | `string` (ISO 8601) | No | Datetime after which the exception no longer applies. |
| `comments` | `with` | `string[]` | No | Comments attached on create. Not sent on overwrite, so existing comments stay. |

```yaml
# Exclude a host from a rule
- name: add_exception_to_rule
  type: security.createRuleException
  with:
    rule_id: "{{ variables.rule_id }}"
    name: "Exclude maintenance host"
    description: "Host is under maintenance"
    entries:
      - field: host.name
        operator: is
        value: "{{ variables.host_name }}"
```

```yaml
# Temporary exception created from an alert
- name: add_exception_from_alert
  type: security.createRuleException
  with:
    rule_id: "{{ event.kibana.alert.rule.uuid }}"
    name: "Auto exception for {{ event.host.name }}"
    description: "Created by workflow"
    expire_time: "{{ variables.expiration }}"
    comments:
      - "Excluded during the patching window"
    entries:
      - field: host.name
        operator: is
        value: "{{ event.host.name }}"
      - field: user.name
        operator: is_one_of
        values:
          - svc-patching
          - svc-backup
```

```yaml
# Idempotent: re-running this workflow updates the same item instead of duplicating it
- name: add_or_update_exception
  type: security.createRuleException
  with:
    rule_id: "{{ variables.rule_id }}"
    item_id: "maintenance-window-{{ variables.host_name }}"
    overwrite: true
    name: "Exclude maintenance host"
    description: "Host is under maintenance"
    entries:
      - field: host.name
        operator: is
        value: "{{ variables.host_name }}"
```

### `security.createExceptionListItem` [security-createexceptionlistitem]

Add an exception item to an existing exception list. Adding to a shared exception list affects every rule linked to that list.

To find a list's `list_id`, search for it on the **Shared exception lists** page. Refer to [Create and manage shared exception lists](/solutions/security/detect-and-alert/create-manage-shared-exception-lists.md).

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `list_id` | `with` | `string` | Yes | The target exception list's `list_id`. The list must already exist. This step doesn't create it. |
| `namespace_type` | `with` | `string` | No (default `single`) | Whether the target list exists in one {{kib}} space (`single`) or in every space (`agnostic`). This is about spaces, not about how many rules use the list. It must match how the list was created. |
| `item_id` | `with` | `string` | No | Stable identifier for idempotency. Omit only when a duplicate item on every run is acceptable. |
| `overwrite` | `with` | `boolean` | No (default `false`) | When `true` and `item_id` already exists on `list_id`, update that item instead of skipping. Requires `item_id`. |
| `name` | `with` | `string` | Yes | Exception item name. |
| `description` | `with` | `string` | Yes | Exception item description. |
| `entries` | `with` | `array` | Yes (at least 1) | Match conditions for the item. Refer to [Shared conventions](#workflows-exceptions-conventions). |
| `os_types` | `with` | `string[]` | No | OS types the exception applies to: `linux`, `macos`, or `windows`. |
| `tags` | `with` | `string[]` | No | Tags for the item. |
| `expire_time` | `with` | `string` (ISO 8601) | No | Datetime after which the exception no longer applies. |
| `comments` | `with` | `string[]` | No | Comments attached on create. Not sent on overwrite, so existing comments stay. |

```yaml
# Add an item to a shared exception list
- name: add_exception_to_shared_list
  type: security.createExceptionListItem
  with:
    list_id: corporate-allowlist
    name: "Allow scanner IP"
    description: "Vulnerability scanner traffic"
    entries:
      - field: source.ip
        operator: is
        value: "{{ event.source.ip }}"
```

```yaml
# Item referencing a value list, in a list that exists in every space
- name: add_value_list_exception
  type: security.createExceptionListItem
  with:
    list_id: global-scanner-allowlist
    namespace_type: agnostic
    name: "Allow approved scanner IPs"
    description: "Source IPs of the approved scanners"
    entries:
      - field: source.ip
        operator: is_in_list
        list:
          id: approved_scanner_ips
          type: ip
```

The following complete workflow runs daily and keeps one allowlist entry current. Because the item carries a stable `item_id`, each run updates the same item instead of adding a duplicate.

```yaml
name: security--refresh-scanner-allowlist
description: Keep the scanner allowlist entry current.
enabled: true

version: "1"

triggers:
  - type: scheduled
    with:
      every: "1d"

consts:
  allowlist_id: corporate-allowlist
  scanner_host: build-agent-01

steps:
  - name: add_allowlist_item
    type: security.createExceptionListItem
    with:
      list_id: "{{ consts.allowlist_id }}"
      item_id: "allowlisted-host-{{ consts.scanner_host }}"
      overwrite: true
      name: "Allow {{ consts.scanner_host }}"
      description: "Reviewed build agent"
      entries:
        - field: host.name
          operator: is
          value: "{{ consts.scanner_host }}"
```

Without `item_id`, running this workflow again creates a second, separate exception item for the same host rather than updating the first. `item_id` and `overwrite: true` together make re-runs safe.

## Output [workflows-exceptions-output]

Both steps return the same summary of the created, skipped, or overwritten item.

| Field | Type | Description |
|---|---|---|
| `id` | `string` | Internal `id` of the created or existing item. |
| `item_id` | `string` | The item's `item_id`. |
| `list_id` | `string` | The list the item is on. |
| `namespace_type` | `string` | `single` or `agnostic`. Always `single` for a rule's own default list. |
| `name` | `string` | The item's name. |
| `created_at` | `string` | Creation timestamp. |
| `created_by` | `string` | Creator. |
| `expire_time` | `string` | Present only if set on the item. |
| `outcome` | `string` | `created`, `skipped`, or `overwritten`. |

## Related

- [Security action steps](/explore-analyze/workflows/steps/security.md): Overview of the `security.*` step namespace.
- [Detection rules action steps](/explore-analyze/workflows/steps/detection-rules.md): Enable or disable detection rules.
- [Workflow authorization](/explore-analyze/workflows/authorization.md): Whose privileges authorize each run.
- [Rule exceptions](/solutions/security/detect-and-alert/rule-exceptions.md): How single-rule and shared exceptions work in {{elastic-sec}}.
- [Create and manage shared exception lists](/solutions/security/detect-and-alert/create-manage-shared-exception-lists.md): Create the lists `security.createExceptionListItem` adds to.
- [Create and manage value lists](/solutions/security/detect-and-alert/create-manage-value-lists.md): Value lists used by the `is_in_list` operators.
- [Add and manage exceptions](/solutions/security/detect-and-alert/add-manage-exceptions.md): Create exceptions in the {{elastic-sec}} UI, and the privileges required.
- [Manage detection rules at scale](/explore-analyze/workflows/use-cases/security/manage-detection-rules.md): Patterns for automating rule-operations work with workflows.
- [Step type index](/explore-analyze/workflows/reference/step-types.md): Alphabetical lookup of every step type.
