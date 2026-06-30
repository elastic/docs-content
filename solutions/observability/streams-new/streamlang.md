---
applies_to:
  serverless: ga
  stack: ga 9.2+
description: Streamlang reference for the YAML configuration format used to define Streams processing pipelines, conditions, and processor parameters.
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

Streamlang is a YAML domain-specific language (DSL) for defining stream processing and routing logic. Streamlang provides a consistent processing interface that can be converted to multiple execution targets, including {{es}} ingest pipelines and {{esql}}. This allows processing to run at ingest time or query time without rewriting rules.

You can write Streamlang directly using the [YAML editing mode](./parse-and-process.md#streams-editing-yaml-mode) in the **Processing** tab or the [interactive mode](./parse-and-process.md#streams-editing-interactive-mode) which generates Streamlang behind the scenes.

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
| [`append`](./processors/append.md) | Adds values to an array field, or creates the field as an array if it doesn't exist. |
| [`concat`](./processors/concat.md) | {applies_to}`stack: ga 9.4+` Concatenates a mix of field values and literal strings into a single field. |
| [`convert`](./processors/convert.md) | {applies_to}`stack: ga 9.3+` Converts a field value to a different data type. |
| [`date`](./processors/date.md) | Parses date strings into timestamps. |
| [`dissect`](./processors/dissect.md) | Parses structured text using delimiter-based patterns. |
| [`drop_document`](./processors/drop.md) | {applies_to}`stack: ga 9.3+` Prevents indexing of a document from based on a condition. |
| [`enrich`](./processors/enrich.md) | {applies_to}`stack: ga 9.4+` Adds data from an enrich policy to incoming documents. |
| [`grok`](./processors/grok.md) | Parses unstructured text using predefined or custom patterns. |
| [`join`](./processors/join.md) | {applies_to}`stack: ga 9.4+` Concatenates the values of multiple fields with a delimiter. |
| [`lowercase`](./processors/lowercase.md) | {applies_to}`stack: ga 9.4+` Converts a string field to lowercase. |
| [`math`](./processors/math.md) | {applies_to}`stack: ga 9.3+` Evaluates an arithmetic expression and stores the result. |
| [`network_direction`](./processors/network-direction.md) | {applies_to}`stack: ga 9.4+` Determines network traffic direction based on source and destination IP addresses. |
| [`redact`](./processors/redact.md) | {applies_to}`stack: ga 9.4+` Redacts sensitive data in a string field by matching patterns. |
| [`remove`](./processors/remove.md) | {applies_to}`stack: ga 9.3+` Removes a field from the document. |
| [`remove_by_prefix`](./processors/remove.md#streams-remove-by-prefix-processor) | Removes a field and all nested fields matching a prefix. |
| [`rename`](./processors/rename.md) | Moves a field's value to a new field name and removes the original. |
| [`replace`](./processors/replace.md) | {applies_to}`stack: ga 9.3+` Replaces portions of a string field that match a regular expression. |
| [`set`](./processors/set.md) | Assigns a value to a field, creating the field if it doesn't exist. |
| [`trim`](./processors/trim.md) | {applies_to}`stack: ga 9.4+` Removes leading and trailing whitespace from a string field. |
| [`uppercase`](./processors/uppercase.md) | {applies_to}`stack: ga 9.4+` Converts a string field to uppercase. |

### Processor limitations and inconsistencies [streams-processor-inconsistencies]

Streams exposes a Streamlang configuration, but internally it relies on {{es}} ingest pipeline processors and {{esql}}. Streamlang doesn't always have 1:1 parity with the ingest processors because it needs to support options that work in both ingest pipelines and {{esql}}. In most cases, you won't need to worry about these details, but the underlying design decisions still affect the UI and available configuration options. The following are some limitations and inconsistencies when using Streamlang processors:

- **Consistently typed fields**: {{esql}} requires one consistent type per column, so workflows that produce mixed types across documents won't transpile.
- **Conversion of types**: {{esql}} and ingest pipelines accept different conversion combinations and strictness (especially for strings), so `convert` can behave differently across targets.
- **Multi-value commands/functions**: Fields can contain one or multiple values. {{esql}} and ingest processors don't always handle these cases the same way. For example, grok in {{esql}} handles multiple values automatically, while the grok processor does not.
- **Conditional execution**: {{esql}}'s enforced table shape limits conditional casting, parsing, and wildcard field operations that ingest pipelines can do per-document.
- **Arrays of objects / flattening**: Ingest pipelines preserve nested JSON arrays, while {{esql}} flattens to columns, so operations like rename and delete on parent objects can differ or fail.

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

### Logical conditions [streams-streamlang-logical-operators]

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

When [partitioning data into child streams](./organize-your-data.md), conditions use the previous operators to define how to route documents to a child stream.

For example, the following routes documents to a child stream when `attributes.filepath` equals `Linux.log`:

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
