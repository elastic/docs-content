---
applies_to:
  serverless: ga
  stack: preview =9.1, ga 9.2+
---

# Streamlang [streams-streamlang]

Streamlang is a JSON domain-specific language (DSL) for defining processing configurations for Streams. It provides a consistent interface for specifying how to to process documents, regardless of where the processing takes.

Streamlang enables seamless movement between query-time and ingest-time processing for the following use cases:

- **{{es}} ingest pipelines**: Traditional ingest-time processing
- **ES|QL**: Query-time processing
- **OTTL**: OpenTelemetry collector processing (planned)

When you configure processors and conditions in the Streams UI, you're working with Streamlang.

## Editing modes [streams-streamlang-modes]

The Streams processing UI provides two modes for editing Streamlang configurations:

### Interactive mode [streams-streamlang-interactive-mode]

Interactive mode provides a form-based interface for creating and editing processors. This mode is ideal for:

- Building simple processing configurations
- Users who prefer a guided, visual approach
- Configurations that don't require deeply nested conditions

Streams defaults to interactive mode unless the configuration can't be represented in interactive mode (for example, when nesting levels are too deep).

### YAML mode [streams-streamlang-yaml-mode]

YAML mode provides a code editor for writing Streamlang directly. This mode is useful for:

- Advanced configurations with complex or deeply nested conditions
- Users who prefer working with code

### Example configuration [streams-streamlang-example]

The following example demonstrates various Streamlang actions:

```yaml
steps:
- action: rename
  from: attributes.old_name
  to: attributes.new_name
- action: set
  to: attributes.status
  value: active
- action: grok
  from: body.message
  patterns:
  - "%{IP:attributes.client_ip} - %{WORD:attributes.method}"
- action: date
  from: attributes.timestamp
  formats:
  - yyyy-MM-dd'T'HH:mm:ss.SSSZ
  - yyyy-MM-dd HH:mm:ss
  to: attributes.parsed_time
  output_format: yyyy-MM-dd
- action: dissect
  from: body.log
  pattern: "%{attributes.client} %{attributes.method} %{attributes.path}"
- action: append
  to: attributes.tags
  value:
  - new_tag
```

## Actions [streams-streamlang-actions]

Streamlang supports actions, which correspond to the [processors](../extract.md#streams-extract-processors) available in the Streams UI.

## Conditions [streams-streamlang-conditions]

Streamlang uses conditions to define Boolean expressions that control when actions run.

### Filter conditions [streams-streamlang-filter-conditions]

Filter conditions compare a field against a value using an operator:

```yaml
condition:
  field: attributes.status
  eq: active
```

#### Supported operators [streams-streamlang-operators]

| Operator | Description | Example |
|----------|-------------|---------|
| `eq` | Equals | `eq: active` |
| `neq` | Not equals | `neq: inactive` |
| `lt` | Less than | `lt: 100` |
| `lte` | Less than or equals | `lte: 100` |
| `gt` | Greater than | `gt: 0` |
| `gte` | Greater than or equals | `gte: 1` |
| `contains` | Contains substring | `contains: error` |
| `startsWith` | Starts with string | `startsWith: WARN` |
| `endsWith` | Ends with string | `endsWith: .log` |
| `exists` | Field exists | `exists: true` |

#### Range conditions [streams-streamlang-range]

For range comparisons, you can combine multiple bounds:

```yaml
condition:
  field: attributes.response_time
  range:
    gte: 100
    lt: 500
```

### Logical conditions [streams-streamlang-logical]

Combine multiple conditions using logical operators:

#### AND condition [streams-streamlang-and]

All conditions must be true:

```yaml
condition:
  and:
  - field: attributes.env
    eq: prod
  - field: attributes.level
    eq: error
```

#### OR condition [streams-streamlang-or]

At least one condition must be true:

```yaml
condition:
  or:
  - field: attributes.level
    eq: error
  - field: attributes.level
    eq: critical
```

#### NOT condition [streams-streamlang-not]

Negates a condition:

```yaml
condition:
  not:
    field: attributes.env
    eq: dev
```

### Special conditions [streams-streamlang-special]

#### Always condition [streams-streamlang-always]

Always evaluates to true:

```yaml
condition:
  always: {}
```

#### Never condition [streams-streamlang-never]

Always evaluates to false:

```yaml
condition:
  never: {}
```

### Conditional actions [streams-streamlang-conditional-actions]

Add a `condition` clause to any action to make it conditional:

```yaml
steps:
- action: set
  to: attributes.flag
  value: 'yes'
  condition:
    field: attributes.status
    eq: active
```

### Nested conditional steps [streams-streamlang-nested-steps]

Group multiple actions under a shared condition:

```yaml
steps:
- condition:
    field: attributes.env
    eq: prod
  steps:
  - action: set
    to: attributes.prod_flag
    value: prod-env
  - action: append
    to: attributes.tags
    value:
    - production
```

