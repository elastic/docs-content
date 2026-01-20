---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn how to use the Liquid templating engine to create dynamic workflows.
---

# Templating engine [workflows-templating]

The workflow templating engine enables dynamic, type-safe template rendering using the [Liquid templating language](https://liquidjs.com/). It allows you to inject variables, apply transformations, and control data flow throughout your workflows.

## Syntax overview [workflows-template-syntax]

The templating engine supports several syntax patterns for different use cases:

| Syntax | Purpose | Example |
|--------|---------|---------|
| Double curly braces | Insert values as strings | `"Hello, {{name}}"` |
| Dollar-sign prefix | Preserve data types (arrays, objects, numbers) | `${{myArray}}` |
| Percent tags | Control flow (conditionals, loops) | `{%if active%}...{%end if%}` |
| Raw tags | Output literal curly braces | `{%raw%}{{ }}{%end raw%}` |

### String interpolation [workflows-string-interpolation]

Use double curly braces for basic string interpolation. Variables and expressions inside the braces are evaluated and rendered as strings.

```yaml
message: "Hello {{user.name}}!"                       # Result: "Hello Alice"
url: "https://api.example.com/users/{{user.id}}"      # Result: "https://api.example.com/users/12"
```

### Type-preserving expressions [workflows-type-preserving]

Use the dollar-sign prefix (`${{ }}`) when you need to preserve the original data type (array, object, number, boolean) instead of converting the result to a string.

```yaml
# Using {{ }} - converts to string
tags: "{{inputs.tags}}"     # Result: "[\"admin\", \"user\"]" (string)

# Using ${{ }} - preserves type
tags: "${{inputs.tags}}"    # Result: ["admin", "user"] (actual array)
```

:::{important}
The type-preserving syntax (`${{ }}`) must occupy the entire string value. You cannot mix it with other text.

✅ **Valid:**

```yaml
tags: "${{inputs.tags}}"
items: "${{inputs.items | slice: 0, 2}}"
```

❌ **Invalid:**

```yaml
message: "Tags are: ${{inputs.tags}}"
```
:::

### Escaping template syntax [workflows-escaping]

Use raw tags (`{% raw %}`) to output literal curly brace characters (`{{ }}`) without rendering them.

```yaml
value: "{% raw %}{{_ingest.timestamp }{%endraw%}"  # Result: "{{_ingest.timestamp }"
```

### Control flow with Liquid tags [workflows-control-flow]

Use Liquid tags (`{% %}`) for control flow and logic, such as conditionals and loops.

```yaml
message: |
  {% if user.role == 'admin' %}
    Welcome, administrator!
  {% endif %}
```

Common tags include: `if` (`{%if%}`), `for` (`{%for%}`), `assign` (`{%assign%}`), and `case` (`{%case%}`).

### Liquid code blocks [workflows-liquid-blocks]

Combine multiple Liquid statements inside one tag block using (`{%-liquid...-%}`):

```yaml
message: |
  {%- liquid
    assign greeting = "Hello"
    echo greeting
    echo " "
    echo user.name
  -%}
```

## How to use the templating engine [workflows-templating-howto]

The templating engine is used directly within your workflow YAML to make your workflows dynamic.

### Reference data from previous steps [workflows-ref-previous-steps]

Use double curly braces (`{{ }}`) to inject outputs from earlier steps into later ones:

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

### Use constants and inputs [workflows-use-constants]

Reference workflow-level constants or inputs:

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

### Preserve data types [workflows-preserve-types]

When you need arrays or objects (not strings), use the dollar-sign prefix (`${{ }}`):

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
    type: elasticsearch.index
    with:
      index: "reports"
      document:
        # Preserves the array type, doesn't stringify it
        tags: "${{steps.get_tags.output.hits.hits[0]._source.tags}}"
```

### Apply filters to transform data [workflows-apply-filters]

Chain filters to manipulate values:

```yaml
steps:
  - name: create_alert
    type: console
    with:
      message: |
        User: {{user.name | upcase}}
        Email: {{user.email | downcase}}
        Created: {{user.created_at | date: "%Y-%m-%d"}}
```

### Use conditionals for dynamic content [workflows-conditionals]

Add logic with `if` (`{%for%}`) tags:

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

### Loop through results [workflows-loops]

Iterate over arrays with `for` (`{%for%}`) loops:

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

## Template rendering behavior [workflows-template-rendering]

The engine renders templates recursively through all data structures, ensuring full support for nested workflows and dynamic data substitution.

**Input:**

```yaml
message: "Hello {{user.name}}"
config:
  url: "{{api.url }}"
tags: ["{{tag1}}", "{{tag2}}"]
```

**After rendering:**

```yaml
message: "Hello Alice"
config:
  url: "https://api.example.com"
tags: ["admin", "user"]
```

### Type handling [workflows-type-handling]

| Type | Behavior |
|------|----------|
| Strings | Processed as templates; variables interpolated, filters applied |
| Numbers, Booleans, Null | Returned as-is |
| Arrays | Each element processed recursively |
| Objects | Each property value processed recursively (keys are not processed) |

### Syntax comparison [workflows-syntax-comparison]

| Feature | String syntax | Type-preserving syntax |
|---------|---------|----------|
| Output type | Always string | Preserves original type |
| Arrays | Stringified | Actual array |
| Objects | Stringified | Actual object |
| Booleans | `"true"` / `"false"` | `true` / `false` |
| Numbers | `"123"` | `123` |
| Filters | Applied (stringified result) | Applied (type preserved) |

### Null and undefined handling [workflows-null-handling]

| Case | Behavior |
|------|----------|
| Null values | Returned as-is |
| Undefined variables | Empty string in string syntax; `undefined` in type-preserving syntax |
| Missing context properties | Treated as undefined |

## Quick reference [workflows-templating-reference]

| What you want to do | Syntax |
|---------------------|--------|
| Insert a string value | Double curly braces around the variable (`{{variable}}`)|
| Preserve arrays/objects/numbers | Dollar sign prefix before double curly braces (`${{variable}}`)|
| Access step output | `steps.step_name.output` inside braces (`{{steps.step_name.output}}`)|
| Access constants | `consts.my_constant` inside braces (`{{consts.my_constant}}`) |
| Apply a filter | Pipe character after the variable (`{{value \| filter_name}}`) |
| Conditional logic | `if`/`endif` tags `{%if condition%}...{%endif%}` |
| Loop through items | `for`/`endfor` tags `{%for item in array%}...{%endfor%}` |
| Output literal braces | Use `raw`/`endraw` tags `{%raw%}{{ }}{%endraw%}` |

## Learn more

- [Liquid Templating Language](https://shopify.github.io/liquid/)
- [LiquidJS Documentation](https://liquidjs.com/)

