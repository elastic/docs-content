---
applies_to:
  serverless: ga
  stack: ga 9.2+
products:
  - id: observability
  - id: elasticsearch
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---
# Streamlang [streams-streamlang-overview]

Streamlang is a YAML domain-specific language (DSL) for defining stream processing and routing logic. Streamlang provides a consistent processing interface that can be transpiled to multiple execution targets, including {{es}} ingest pipelines and ES|QL. This allows processing to run at ingest time or query time without rewriting rules.

You can write Streamlang directly using the [YAML editing mode](./extract.md#streams-editing-yaml-mode) in the **Processing** tab or the [interactive mode](./extract.md#streams-editing-interactive-mode) which generates Streamlang behind the scenes.

## Structure [streams-streamlang-structure]

A Streamlang configuration is a YAML document with a single top-level `steps` array. Each step is either an [`action` block (processor)](#streams-streamlang-processors) or a [`condition` block](#streams-streamlang-condition-blocks):

```yaml
steps:
  - action: <processor_type>
    # processor-specific parameters
  - action: <processor_type>
    # processor-specific parameters
    where:
      # optional condition
  - condition:
      field: <field_path>
      eq: <value>
      steps:
        - action: <processor_type>
          # nested processor
```

Steps run in order. Each processor transforms input documents, and passes results to the next step.

## Processors [streams-streamlang-processors]

Processors are the building blocks of a Streamlang configuration. Each processor has an `action` field that specifies an operation to perform.

All processors support the following common options:

| Option | Type | Description |
| --- | --- | --- |
| `description` | string | A human-readable description of the processor. |
| `ignore_failure` | boolean | When `true`, document processing continues even if this processor fails. |
| `where` | [condition](#streams-streamlang-conditions) | A condition that the processor must meet to run. |

The following table lists all available processors. Refer to the individual processor pages for YAML parameters and examples.

| Action | Description |
| --- | --- |
| [`append`](./extract/append.md) | Adds values to an array field, or creates the field as an array if it doesn't exist. |
| [`concat`](./extract/concat.md) | Concatenates a mix of field values and literal strings into a single field. |
| [`convert`](./extract/convert.md) | Converts a field value to a different data type. |
| [`date`](./extract/date.md) | Parses date strings into timestamps. |
| [`dissect`](./extract/dissect.md) | Parses structured text using delimiter-based patterns. |
| [`drop_document`](./extract/drop.md) | Prevents indexing of a document from based on a condition. |
| [`grok`](./extract/grok.md) | Parses unstructured text using predefined or custom patterns. |
| [`join`](./extract/join.md) | Concatenates the values of multiple fields with a delimiter. |
| [`lowercase`](./extract/lowercase.md) | Converts a string field to lowercase. |
| [`math`](./extract/math.md) | Evaluates an arithmetic expression and stores the result. |
| [`network_direction`](./extract/network-direction.md) | Determines network traffic direction based on source and destination IP addresses. |
| [`redact`](./extract/redact.md) | Redacts sensitive data in a string field by matching patterns. |
| [`remove`](./extract/remove.md) | Removes a field from the document. |
| [`remove_by_prefix`](./extract/remove.md#streams-remove-by-prefix-processor) | Removes a field and all nested fields matching a prefix. |
| [`rename`](./extract/rename.md) | Moves a field's value to a new field name and removes the original. |
| [`replace`](./extract/replace.md) | Replaces portions of a string field that match a regular expression. |
| [`set`](./extract/set.md) | Assigns a value to a field, creating the field if it doesn't exist. |
| [`trim`](./extract/trim.md) | Removes leading and trailing whitespace from a string field. |
| [`uppercase`](./extract/uppercase.md) | Converts a string field to uppercase. |

## Conditions [streams-streamlang-conditions]

Conditions are Boolean expressions that control when processors run and how wired streams route data into partitions. They appear in `where` clauses on processors, in [condition blocks](#streams-streamlang-condition-blocks), and in stream [partitioning](#streams-streamlang-partition-conditions).

### Comparison conditions [streams-streamlang-comparison-operators]

Each comparison condition specifies a `field` and an operator with a value:

| Operator | Description | Example value |
| --- | --- | --- |
| `eq` | Equals | `"active"`, `200` |
| `neq` | Not equals | `"error"` |
| `lt` | Less than | `100` |
| `lte` | Less than or equal to | `100` |
| `gt` | Greater than | `0` |
| `gte` | Greater than or equal to | `1` |
| `contains` | Field value contains the substring | `"error"` |
| `startsWith` | Field value starts with the string | `"/api"` |
| `endsWith` | Field value ends with the string | `".log"` |
| `includes` | Multivalue field includes the value | `"admin"` |

### Range conditions [streams-streamlang-range-conditions]

Use `range` to match values within a numeric range. You can combine any of `gt`, `gte`, `lt`, and `lte`:

```yaml
where:
  field: attributes.status_code
  range:
    gte: 200
    lt: 300
```

### Existence conditions [streams-streamlang-existence-conditions]

Use `exists` to check whether a field is present:

```yaml
# Field must exist
where:
  field: attributes.user_id
  exists: true

# Field must not exist
where:
  field: attributes.temp
  exists: false
```

### Logical operator conditions [streams-streamlang-logical-operators]

Combine conditions using `and`, `or`, and `not`:

```yaml
# All conditions must be true
where:
  and:
    - field: attributes.env
      eq: production
    - field: attributes.level
      eq: error

# At least one condition must be true
where:
  or:
    - field: attributes.level
      eq: error
    - field: attributes.level
      eq: warn

# Negate a condition
where:
  not:
    field: attributes.path
    startsWith: "/internal"
```

### Special conditions [streams-streamlang-special-conditions]

| Condition | Description |
| --- | --- |
| `always: {}` | Always evaluates to `true`. |
| `never: {}` | Always evaluates to `false`. |

## Partition conditions [streams-streamlang-partition-conditions]

When [partitioning data into child streams](./partitioning.md), conditions use the previous operators to define how to route documents to a child stream.

For example, the following routes documents where `attributes.filepath` equals `Linux.log`:

```yaml
field: attributes.filepath
eq: Linux.log
```

To enter conditions in YAML format when configuring a partition, turn on the **Syntax editor** under **Condition** in the **Partitioning** tab.

## Condition blocks [streams-streamlang-condition-blocks]

Condition blocks group processors so that they run only when they meet a condition. Use a `condition` step with nested `steps`:

```yaml
steps:
  - condition:
      field: attributes.env
      eq: production
      steps:
        - action: set
          to: attributes.is_prod
          value: true
        - action: remove
          from: attributes.debug_info
```

You can nest condition blocks for complex logic:

```yaml
steps:
  - condition:
      field: attributes.source
      eq: webserver
      steps:
        - action: grok
          from: body.message
          patterns:
            - "%{IP:attributes.client_ip} %{WORD:attributes.method} %{URIPATHPARAM:attributes.path} %{NUMBER:attributes.status}"
        - condition:
            field: attributes.status
            gte: 500
            steps:
              - action: set
                to: attributes.alert_level
                value: critical
```