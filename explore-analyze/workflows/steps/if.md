---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about the if step for conditional logic in workflows.
---

# If

The `if` step evaluates a boolean or {{kib}} Query Language (KQL) expresson and executes different steps based on whether the condition is true or false.

```yaml
steps:
  - name: conditionalStep
    type: if
    condition: <KQL expression>
    steps:
      # Steps to execute if condition is true
    else:
      # Steps to execute if condition is false (optional)
```

Use the following parameters to configure an `if` step:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Unique step identifier |
| `type` | Yes | Step type - must be `if` |
| `condition` | Yes | A boolean or KQL expression to evaluate |
| `steps` | Yes | An array of steps to execute if the condition is true |
| `else` | No | An array of steps to execute if the condition is false |

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
condition: "status: active and isEnabled: true"             # AND
condition: "status: active or status: pending"              # OR
condition: "not status: inactive"                           # NOT
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

This example executes different steps based on the event severity:

```yaml
steps:
  - name: checkSeverity
    type: if
    condition: event.severity: 'critical'
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
              message: "Processing park: {{ item._source.title }}"
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
