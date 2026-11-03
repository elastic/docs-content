---
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Learn about the if step for conditional logic in workflows.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# If

The `if` step evaluates a boolean or {{kib}} Query Language (KQL) expression and runs different steps based on whether the condition is true or false.

Use the following parameters to configure an `if` step:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Unique step identifier |
| `type` | Yes | Step type - must be `if` |
| `condition` | Yes | A boolean or KQL expression to evaluate |
| `steps` | Yes | An array of steps to run if the condition is true |
| `else` | No | An array of steps to run if the condition is false |

```yaml
steps:
  - name: conditionalStep
    type: if
    condition: <boolean or KQL expression>
    steps:
      # Steps to run if condition is true
    else:
      # Steps to run if condition is false (optional)
```

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.4+` To run or skip one step on its own instead of branching between two sets of steps, set `if` on that step. Refer to [Skip a single step](#workflows-step-level-if).

The `condition` field supports the following expression types:

* [Boolean expressions](#boolean-expressions)
* [KQL expressions](#kql-expressions)

## Boolean expressions

Use `${{ }}` syntax when you want the expression to evaluate directly to a boolean value:

```yaml
steps:
  - name: check-enabled
    type: if
    condition: "${{ inputs.isEnabled }}"
    steps:
      - name: process-enabled
        type: http
    else:
      - name: log-disabled
        type: console
```

If the expression evaluates to `undefined`, it defaults to `false`.

## KQL expressions

Use a string-based condition to evaluate the value as a KQL expression. You can use `{{ }}` templating to inject dynamic values:

```yaml
steps:
  - name: check-status
    type: if
    condition: "{{ steps.fetchData.output.status }}: completed"
    steps:
      - name: process-data
        type: http
```

### Supported KQL features

The `if` step supports the following KQL features: 

#### Equality checks

```yaml
condition: "status: active"
condition: "user.role: admin"
condition: "isActive: true"
condition: "count: 42"
condition: "users[0].name: Alice"  # Array index access
```

#### Range operators

```yaml
condition: "count >= 100"
condition: "count <= 1000"
condition: "count > 50"
condition: "count < 200"
condition: "count >= 100 and count <= 1000"
```

#### Wildcard matching

```yaml
condition: "fieldName:*"        # Field exists
condition: "user.name: John*"   # Starts with
condition: "user.name: *Doe"    # Ends with
condition: "txt: *ipsum*"       # Contains
condition: "user.name: J*n Doe" # Pattern
```

#### Logical operators

```yaml
condition: "status: active and isEnabled: true"             # And
condition: "status: active or status: pending"              # Or
condition: "not status: inactive"                           # Not
condition: "status: active and (role: admin or role: moderator)"  # Nested
```

#### Property path access

```yaml
condition: "user.info.name: John Doe"            # Nested property
condition: "steps.fetchData.output.status: completed"  # Deep nesting
condition: "users[0].name: Alice"                # Array access
condition: "users.0.name: Alice"                 # Alternative syntax
```

### Example: Check severity

This example runs different steps based on the event severity:

```yaml
steps:
  - name: checkSeverity
    type: if
    condition: "event.severity: 'critical'"
    steps:
      - name: handleCritical
        type: console
        with:
          message: "Critical alert!"
    else:
      - name: handleNormal
        type: console
        with:
          message: "Normal severity"
```

You can write the same check as a [boolean expression](#boolean-expressions) with `${{ }}` syntax, for example `condition: "${{ event.severity == 'critical' }}"`.

### Example: Check search results count

This example checks the number of search results and processes them differently based on the count:

```yaml
name: National Parks Conditional Processing
steps:
  - name: searchParks
    type: elasticsearch.search
    with:
      index: national-parks-index
      size: 100
  
  - name: checkResultCount
    type: if
    condition: "steps.searchParks.output.hits.total.value > 5"
    steps:
      - name: processLargeDataset
        type: foreach
        foreach: "{{ steps.searchParks.output.hits.hits }}"
        steps:
          - name: processPark
            type: console
            with:
              message: "Processing park: {{ foreach.item._source.title }}"
    else:
      - name: handleSmallDataset
        type: console
        with:
          message: "Only {{ steps.searchParks.output.hits.total.value }} parks found - manual review needed"
```

### Example: Complex KQL condition

This example uses multiple logical operators to check a combination of conditions:

```yaml
steps:
  - name: check-complex
    type: if
    condition: "status: active and (count >= 100 or role: admin)"
    steps:
      - name: process-authorized
        type: http
```

## Skip a single step [workflows-step-level-if]
```{applies_to}
serverless: ga
stack: ga 9.4+
```

When only one step in a workflow is optional, you don't need a separate `if` step to control it. Instead, set `if` directly on that step. This step-level `if` makes the step run only when its condition is true. When the condition is false, the workflow skips the step and continues with the next one.

For example, the following snippets both run a `notify` step only when an earlier search step, `find_failed_logins`, finds at least one match. The first snippet wraps `notify` in an `if` step:

```yaml
- name: check_results
  type: if
  condition: "steps.find_failed_logins.output.hits.total.value > 0"
  steps:
    - name: notify
      type: console
      with:
        message: "Found {{ steps.find_failed_logins.output.hits.total.value }} failed logins."
```

The second snippet sets a step-level `if` on `notify`. The result is the same, with one fewer step and one fewer level of nesting:

```yaml
- name: notify
  type: console
  if: "steps.find_failed_logins.output.hits.total.value > 0"
  with:
    message: "Found {{ steps.find_failed_logins.output.hits.total.value }} failed logins."
```

Use an `if` step instead when you need an `else` branch for the false case, or when one condition controls several steps.

A step-level `if` accepts the same [boolean](#boolean-expressions) and [KQL](#kql-expressions) expressions as the `if` step's `condition`.

A skipped step doesn't produce output, so a later reference such as `{{ steps.notify.output }}` resolves to an empty value. If a later step depends on the skipped step's output, set the same condition on that step too.

### Step-level `if` limitations and alternatives [workflows-step-level-if-limitations]

A step-level `if` causes a validation error in the following cases. Each case has an alternative that you can use instead.

#### Add another condition to an `if` step [workflows-step-level-if-on-if-step]

An `if` step already uses `condition` to decide what runs, so it can't also have a step-level `if`. For example, an `if` step can't have both `condition: "status: active"` and `if: "inputs.enabled: true"`.

Instead, combine both checks in `condition` with `and`, for example `condition: "status: active and inputs.enabled: true"`.

#### Skip a step inside a `parallel` branch [workflows-step-level-if-parallel-branch]

Steps inside a [`parallel`](/explore-analyze/workflows/steps/parallel.md) branch can't have a step-level `if`, so a branch can't skip individual steps. For example, you can't skip a GeoIP lookup in one branch when an alert has no source IP.

To run or skip all branches at once, add `if` to the `parallel` step instead, for example `if: "inputs.enrich: true"`. To skip steps in only one branch, move those steps into a child workflow, add `if` to them there, and call the child workflow from the branch with [`workflow.execute`](/explore-analyze/workflows/steps/composition.md#workflow-execute).

For more about what a branch can contain, refer to [Branch body limitations](/explore-analyze/workflows/steps/parallel.md#workflows-parallel-branch-limits).

#### Use a condition longer than 2,000 characters [workflows-step-level-if-condition-length]

A step-level `if` and an `if` step's `condition` can each be up to 2,000 characters long. You might reach this limit with a check that lists hundreds of host names joined with `or`.

Instead, move the long part out of the condition. For example, store the host names as a list in [`consts`](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-consts), then check the list with `if: "${{ consts.watched_hosts contains inputs.host_name }}"`. You can also calculate a value in an earlier [`data.set`](/explore-analyze/workflows/steps/data.md#data-set) step and check that value instead.
