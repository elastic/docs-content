---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about the foreach step for iterating over data in workflows.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Foreach

The `foreach` step iterates over an array and runs its nested steps once for each item in the array.

Use the following parameters to configure a `foreach` step:

| Parameter | Required | Description |
|-----------|----------|-------------|
| `name` | Yes | Unique step identifier |
| `type` | Yes | Step type - must be `foreach` |
| `foreach` | Yes | A template or JSON expression that evaluates to an array |
| `steps` | Yes | An array of steps to run for each iteration |

```yaml
steps:
  - name: loopStep
    type: foreach
    foreach: <array expression>
    steps:
      # Steps to run for each item
      # Current item is available as 'foreach.item'
```

::::{note}
Inside the loop, the current item is always available as `foreach.item`. You cannot customize this variable name.
::::

The `foreach` field supports the following expression types:

* [Template expressions](#template-expressions)
* [JSON strings](#json-strings)
* [JSON strings with templates](#json-strings-with-templates)

## Template expressions

Use `{{ }}` or `${{ }}` syntax when the array comes from context variables such as step outputs, inputs, or constants. Both syntaxes behave identically for `foreach`:

```yaml
foreach: "{{ steps.getData.output.items }}"
foreach: "${{ steps.getData.output.items }}"
```

## JSON strings

Use a plain JSON array string for static arrays known at definition time:

```yaml
foreach: '["item1", "item2", "item3"]'
```

## JSON strings with templates

Use a JSON string containing `{{ }}` template expressions for dynamically built arrays with a known structure:

```yaml
foreach: '[{{ steps.getCount }}, {{ steps.getCount | plus: 1 }}]'
```

::::{note}
Avoid using plain property paths without template syntax (for example, `foreach: 'consts.items'`). Use `foreach: "{{ consts.items }}"` instead.
::::

## Context variables

The workflow engine automatically provides the following variables during `foreach` iteration. To use these variables, reference them in your step parameters with `{{ }}` syntax:

| Variable | Description |
|----------|-------------|
| `foreach.item` | Current item in the iteration |
| `foreach.index` | Zero-based index of the current iteration |
| `foreach.total` | Total number of items in the array |
| `foreach.items` | Complete array being iterated over |

Example:

```yaml
message: "Processing {{ foreach.item.name }} ({{ foreach.index | plus: 1 }}/{{ foreach.total }})"
```

### Access parent context

Nested `foreach` loops can access parent context using step references:

```yaml
steps:
  - name: outer-foreach
    type: foreach
    foreach: "{{ outerItems }}"
    steps:
      - name: inner-foreach
        type: foreach
        foreach: "{{ innerItems }}"
        steps:
          - name: log-both
            type: console
            with:
              message: "Outer: {{ steps.outer-foreach.index }}, Inner: {{ foreach.index }}"
```

### Access keys with dots

Template expressions support bracket notation for keys that contain dots or other special characters:

```yaml
"{{ foreach.item['service.name'] }}"
```


## Example: Process search results

This example searches for documents and enriches each result with metadata:

```yaml
name: National Parks Enrichment
description: Enrich each park with additional data
steps:
  - name: searchAllParks
    type: elasticsearch.search
    with:
      index: national-parks-index
      size: 100
      query:
        match_all: {}

  - name: enrichEachPark
    type: foreach
    foreach: "{{ steps.searchAllParks.output.hits.hits }}"
    steps:
      - name: logProcessing
        type: console
        with:
          message: "Processing park: {{ foreach.item._source.title }}"

      - name: addMetadata
        type: elasticsearch.update
        with:
          index: national-parks-index
          id: "{{ foreach.item._id }}"
          doc:
            last_processed: "{{ execution.startedAt }}"
            workflow_run: "{{ execution.id }}"
            category_uppercase: "{{ foreach.item._source.category | upcase }}"
```
