---
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Learn how to use variables, constants, Liquid templating, and custom filters to move data through Elastic Workflows.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Templating engine [workflows-templating]

The workflow templating engine enables dynamic, type-safe template rendering using the [Liquid templating language](https://liquidjs.com/). It allows you to inject variables, apply transformations, and control data flow throughout your workflows.

## Syntax overview [workflows-template-syntax]

The templating engine supports several syntax patterns for different use cases:

| Syntax | Purpose | Example |
|--------|---------|---------|
| Double curly braces | Insert values as strings | `"Hello, {{name}}"` |
| Dollar-sign prefix | Preserve data types (arrays, objects, numbers) | `${{myArray}}` |
| Percent tags | Control flow (conditionals, loops) | `{%if active%}...{%endif%}` |
| Raw tags | Output literal curly braces | `{%raw%}{{}}{%endraw%}` |

### String interpolation [workflows-string-interpolation]

Use double curly braces for basic string interpolation. Variables and expressions inside the braces are evaluated and rendered as strings.

```yaml
message: "Hello {{user.name}}!"                       # Result: "Hello Alice"
url: "https://api.example.com/users/{{user.id}}"      # Result: "https://api.example.com/users/12"
```

### Type-preserving expressions [workflows-type-preserving]

Use the dollar-sign prefix (`${{ }}`) when you need to preserve the original data type (array, object, number, boolean).

```yaml
# String syntax - converts to string
tags: "{{inputs.tags}}"     # Result: "[\"admin\", \"user\"]" (string)

# Type-preserving syntax - keeps original type
tags: "${{inputs.tags}}"    # Result: ["admin", "user"] (actual array)
```

:::{important}
The type-preserving syntax must occupy the entire string value. You cannot mix it with other text.

✅ **Valid:**

```yaml
tags: "${{inputs.tags}}"
```

❌ **Invalid:**

```yaml
message: "Tags are: ${{inputs.tags}}"
```
:::

| Feature | String syntax | Type-preserving syntax |
|---------|---------------|------------------------|
| Output type | Always string | Preserves original type |
| Arrays | Stringified | Actual array |
| Objects | Stringified | Actual object |
| Booleans | `"true"` / `"false"` | `true` / `false` |
| Numbers | `"123"` | `123` |

### Control flow [workflows-control-flow]

Liquid tags are control flow constructs that use the `{% %}` syntax. Unlike output expressions, tags execute logic without directly rendering a value.

**Conditionals:**

```yaml
message: |
  {% if user.role == 'admin' %}
    Welcome, administrator!
  {% else %}
    Welcome, user!
  {% endif %}
```

**Loops:**

```yaml
message: |
  {% for item in items %}
    - {{item.name}}
  {% endfor %}
```

### Escaping template syntax [workflows-escaping]

Use raw tags to output literal curly brace characters without rendering them:

```yaml
value: "{%raw%}{{_ingest.timestamp}}{%endraw%}"  # Result: "{{_ingest.timestamp}}"
```

## Working with data [workflows-working-with-data]

This section covers common patterns for accessing and transforming data in your workflows.

### Reference inputs [workflows-ref-inputs]

Reference input parameters defined in the workflow using `{{inputs.<input_name>}}`. Inputs are values provided when the workflow is triggered manually.

The location of `inputs` in the YAML depends on your version. On stack 9.4 and earlier, `inputs` sits at the top level of the workflow. On stack 9.5+ and on serverless, `inputs` sits inside the `manual` trigger. Refer to [Workflow anatomy](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-inputs) for the full reference.

::::{applies-switch}

:::{applies-item} stack: preview 9.3, ga 9.4
```yaml
inputs:
  - name: environment
    type: string
    required: true
    default: "staging"
  - name: batchSize
    type: number
    default: 100

triggers:
  - type: manual

steps:
  - name: log_config
    type: console
    with:
      message: |
        Running with:
        - Environment: {{inputs.environment}}
        - Batch Size: {{inputs.batchSize}}
```
:::

:::{applies-item} { stack: ga 9.5+, serverless: ga }
```yaml
triggers:
  - type: manual
    inputs:
      - name: environment
        type: string
        required: true
        default: "staging"
      - name: batchSize
        type: number
        default: 100

steps:
  - name: log_config
    type: console
    with:
      message: |
        Running with:
        - Environment: {{inputs.environment}}
        - Batch Size: {{inputs.batchSize}}
```
:::

::::

### Reference outputs [workflows-ref-step-outputs]

Access output data from previous steps using `{{steps.<step_name>.output}}`:

```yaml
steps:
  - name: search_users
    type: elasticsearch.search
    with:
      index: "users"
      query:
        term:
          status: "active"

  - name: send_notification
    type: slack
    connector-id: "my-slack"
    with:
      message: "Found {{steps.search_users.output.hits.total.value}} active users"
```

### Reference constants [workflows-ref-constants]

Reference workflow-level constants using `{{consts.<constant_name>}}`. Constants are defined at the workflow level and can be referenced when the workflow is triggered.

```yaml
consts:
  indexName: "my-index"
  environment: "production"

steps:
  - name: search_data
    type: elasticsearch.search
    with:
      index: "{{consts.indexName}}"
      query:
        match:
          env: "{{consts.environment}}"
```

### Apply filters [workflows-apply-filters]

Transform values using filters with the pipe `|` character:

```yaml
message: |
  User: {{user.name | upcase}}
  Email: {{user.email | downcase}}
  Created: {{user.created_at | date: "%Y-%m-%d"}}
```

:::{note}
Workflows supports all available LiquidJS [filters](https://liquidjs.com/filters/overview.html), plus two custom filters (`json_parse` and `entries`) documented in the next section.
:::

### Custom filters [workflows-custom-filters]

In addition to the standard LiquidJS filter set, the workflow engine provides two custom filters for shapes that come up often in automation:

| Filter | What it does | Example |
|---|---|---|
| `json_parse` | Parses a JSON string into an object so you can access fields. | `"{{ steps.http.output.body \| json_parse }}"` |
| `entries` | Converts an object into an array of `{key, value}` pairs, which is iterable with `{% for %}`. | `"{% for kv in steps.config.output \| entries %}{{ kv[0] }}: {{ kv[1] }}{% endfor %}"` |

**Parse a JSON string returned as a string body:**

```yaml
- name: parse_response
  type: data.set
  with:
    parsed: "{{ steps.http_call.output.body | json_parse }}"
```

:::{note}
The inverse of `json_parse` is the standard LiquidJS `json` filter, which serializes a value to a JSON string.
:::

**Iterate an object's keys:**

```yaml
- name: summarize_config
  type: console
  with:
    message: |
      {% for kv in steps.config.output | entries %}
        {{ kv[0] }}: {{ kv[1] }}
      {% endfor %}
```

### Choose Liquid or a data step [workflows-liquid-vs-data-steps]

Liquid is excellent for small inline transformations: field access, defaults, formatting, string concatenation. When a transformation grows (filtering a large array, grouping by a key, parsing a JSON payload into named outputs, extracting fields with regex), reach for a [`data.*` step](/explore-analyze/workflows/steps/data.md) instead. Data steps give you explicit, testable transformation with their own named output and their own execution log entry.

| Size of transformation | Use |
|---|---|
| A field access, a default, a format (fits in one expression) | Liquid |
| Filter, group, parse, regex-extract, or multi-field map | A [`data.*` step](/explore-analyze/workflows/steps/data.md) |

### Preserve array and object types [workflows-preserve-types]

When passing arrays or objects between steps, use the type-preserving syntax (`${{ }}`) to avoid stringification:

```yaml
steps:
  - name: get_tags
    type: elasticsearch.search
    with:
      index: "config"
      query:
        term:
          type: "tags"

  - name: create_document
    type: elasticsearch.request
    with:
      method: POST
      path: /reports/_doc
      body:
        # Preserves the array type, doesn't stringify it
        tags: "${{steps.get_tags.output.hits.hits[0]._source.tags}}"
```

:::{important}
The type-preserving syntax must occupy the entire string value. You cannot mix it with other text.

✅ **Valid:**

```yaml
tags: "${{inputs.tags}}"
```

❌ **Invalid:**

```yaml
message: "Tags are: ${{inputs.tags}}"
```
:::

### Use conditionals for dynamic content [workflows-conditionals-example]

Add logic to customize output based on data:

```yaml
steps:
  - name: send_message
    type: slack
    connector-id: "alerts"
    with:
      message: |
        {% if steps.search.output.hits.total.value > 100 %}
        ⚠️ HIGH ALERT: {{steps.search.output.hits.total.value}} events detected!
        {% else %}
        ✅ Normal: {{steps.search.output.hits.total.value}} events detected.
        {% endif %}
```

### Loop through results [workflows-loops-example]

Iterate over arrays to process multiple items:

```yaml
steps:
  - name: summarize_results
    type: console
    with:
      message: |
        Found users:
        {% for hit in steps.search_users.output.hits.hits %}
        - {{hit._source.name}} ({{hit._source.email}})
        {% endfor %}
```

## Context variables [workflows-context-variables]

The workflow engine provides context variables that you can access from any Liquid expression. The most common ones:

- `inputs.<name>` — values provided when the workflow was invoked.
- `consts.<name>` — constants declared at the top of the workflow.
- `steps.<name>.output` — output of a previous step.
- `steps.<name>.error` — error from a failed step (with `on-failure: continue`).
- `event.*` — trigger payload (shape depends on the trigger type).
- `execution.*` — metadata about the current execution.
- `workflow.*` — workflow metadata.
- `foreach.*`, `while.iteration` — loop-local context.
- `variables.<name>` — set by `data.set` steps.
- `now`, `kibanaUrl` — standard helpers.

For the full canonical reference with every variable, the trigger-specific shape of `event.*`, and an example per entry, refer to [Context variables](/explore-analyze/workflows/reference/context-variables.md).

## Template rendering behavior [workflows-template-rendering]

The engine renders templates recursively through all data structures, processing nested objects and arrays.

**Input:**

```yaml
message: "Hello {{user.name}}"
config:
  url: "{{api.url}}"
tags: ["{{tag1}}", "{{tag2}}"]
```

**Rendered output:**

```yaml
message: "Hello Alice"
config:
  url: "https://api.example.com"
tags: ["admin", "user"]
```

### Type handling [workflows-type-handling]

| Type | Behavior |
|------|----------|
| Strings | Processed as templates: variables are interpolated, and filters are applied |
| Numbers, Booleans, Null | Returned as-is |
| Arrays | Each element is processed recursively |
| Objects | Each property value is processed recursively (keys are not processed) |

### Null and undefined handling [workflows-null-handling]

| Case | Behavior |
|------|----------|
| Null values | Returned as-is |
| Undefined variables | Returned as empty string in string syntax and as `undefined` in type-preserving syntax |
| Missing context properties | Treated as undefined |

## Template rendering limits [workflows-template-limits]

To protect execution stability, the templating engine enforces limits on every template render. These limits are most often reached by large `console` reports or loops that concatenate big strings.

| Limit | Default | What it caps |
|---|---|---|
| Parse size | 150,000 characters | Total characters allowed in a single template |
| Render time | 1,000 ms | Time spent rendering a single template |
| Memory | 15,000,000 operations | Object allocations (array and string operations) during a single render |

If a template exceeds one of these limits, the step fails and the render stops. To stay within the limits:

- Reduce the size of the rendered output. For large reports, write results to an index or return structured data instead of formatting a single large string.
- Move heavy transformations (filtering, grouping, or parsing large arrays) into [`data.*` steps](/explore-analyze/workflows/steps/data.md) instead of Liquid.
- Simplify or shorten loops that build large strings.

## Learn more

- [Liquid templating language](https://shopify.github.io/liquid/)
- [LiquidJS documentation](https://liquidjs.com/)