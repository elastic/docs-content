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
    condition: <KQL expression>
    steps:
      # Steps to run if condition is true
    else:
      # Steps to run if condition is false (optional)
```

To skip a single step instead of branching between two sets of steps, set the `if` property on that step. Refer to [Step-level `if`](#workflows-step-level-if).

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

## Step-level `if` [workflows-step-level-if]
```{applies_to}
stack: ga 9.4+
```

To skip a single step, set the `if` property on the step itself rather than wrapping the step in an `if` step. The step runs only when the condition is true.

```yaml
steps:
  - name: escalate
    type: console
    if: "steps.triage.output.risk_score >= 70"
    with:
      message: "Escalating: risk score {{ steps.triage.output.risk_score }}."
```

A step-level `if` takes the same boolean and KQL expressions as the `if` step's `condition`, and you can set it on any step type, with two exceptions:

* The `if` step itself. It already branches on its own `condition`, so setting a step-level `if` on it is a validation error.
* A step inside a [`parallel`](/explore-analyze/workflows/steps/parallel.md) branch body. Set `if` on the `parallel` step to gate every branch at once, or evaluate the condition in a step that runs before the `parallel` step.

A step-level `if` expression and an `if` step's `condition` can each be up to 2,000 characters long. For a longer condition, compute the value in an earlier step, for example with [`data.set`](/explore-analyze/workflows/steps/data.md#data-set), and compare that shorter value instead.
