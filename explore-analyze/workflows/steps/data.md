---
navigation_title: Data
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Reference for the 11 data step types that filter, map, aggregate, parse, and transform data inside a workflow.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Data action steps [workflows-data-steps]

Data action steps are explicit, testable data transformations. They do the things you *could* do inline with Liquid templating, but with their own named output, an execution log, and an attachment point for error handling.

Use a data step when the transformation has any complexity: multi-field mapping, grouping, JSON parsing, regex extraction, or deduplication. For small inline transforms (take a field, uppercase it, fall back to a default), use [Liquid templating](/explore-analyze/workflows/templating.md) instead.

## Source data location

Most data steps place the source of the data to transform at the **step top level**, not inside `with`. `with` holds the transformation configuration. The exceptions are `data.set`, which has no separate source field, and where noted below.

| Top-level field | Used by |
|---|---|
| `items` | `data.map`, `data.filter`, `data.find`, `data.aggregate`, `data.dedupe` |
| `arrays` | `data.concat` |
| `source` | `data.parseJson`, `data.stringifyJson`, `data.regexExtract`, `data.regexReplace` |

Source arrays usually need the raw-value form `${{ ... }}` so they pass as an array rather than as a string:

```yaml
items: "${{ steps.search.output.hits.hits }}"
```

See [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md) for the `{{ }}` vs. `${{ }}` distinction.

## Step catalog

**Variables and mapping**
[`data.set`](#data-set) ·
[`data.map`](#data-map)

**Filter, find, and aggregate**
[`data.filter`](#data-filter) ·
[`data.find`](#data-find) ·
[`data.aggregate`](#data-aggregate)

**Combine and de-duplicate**
[`data.concat`](#data-concat) ·
[`data.dedupe`](#data-dedupe)

**JSON**
[`data.parseJson`](#data-parsejson) ·
[`data.stringifyJson`](#data-stringifyjson)

**Regex**
[`data.regexExtract`](#data-regexextract) ·
[`data.regexReplace`](#data-regexreplace)

---

## Variables and mapping

### `data.set` [data-set]

Set named variables in the workflow context. Subsequent steps reference them as `{{ variables.<name> }}`. Unlike the other data steps, `data.set` has no top-level source field; values go directly inside `with`.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| (variable values) | `with` | object | Yes | Key/value pairs to assign to `variables`. |

```yaml
- name: init
  type: data.set
  with:
    service_name: "checkout"
    threshold: 70
```

Later steps can read `{{ variables.service_name }}` and `{{ variables.threshold }}`.

### `data.map` [data-map]

Transform each element of an array into a new shape. `items` is a top-level step field; the per-element mapping goes under `with.fields`. Inside the mapping, `item` refers to the current array element.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `items` | top level | array (passed through Liquid) | Yes | Source array. |
| `fields` | `with` | object | Yes | Per-element field mapping. Values can reference `item`. |

```yaml
- name: normalize_alerts
  type: data.map
  items: "${{ steps.search.output.hits.hits }}"
  with:
    fields:
      id: "{{ item._id }}"
      severity: "{{ item._source.kibana.alert.severity }}"
      host: "{{ item._source.host.name }}"
```

---

## Filter, find, and aggregate

### `data.filter` [data-filter]

Keep only the elements of an array that match a {{kib}} Query Language (KQL) predicate. Inside the condition, `item.<field>` refers to element fields and `index` refers to the zero-based position.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `items` | top level | array | Yes | Source array. |
| `condition` | `with` | KQL string | Yes | KQL predicate evaluated per element. |
| `limit` | `with` | number | No | Max matching results. Use for early-exit optimization. |

Output is always an array of matched items.

```yaml
- name: only_critical
  type: data.filter
  items: "${{ steps.search.output.hits.hits }}"
  with:
    condition: "item._source.kibana.alert.severity : critical"
    limit: 10
```

### `data.find` [data-find]

Return the first element of an array that matches a KQL predicate. Output is `{ item, index }`, or `null` when nothing matches (unless `errorIfEmpty` is set).

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `items` | top level | array | Yes | Source array. |
| `condition` | `with` | KQL string | Yes | KQL predicate. |
| `errorIfEmpty` | `with` | boolean | No | Fail the step when no element matches. |

```yaml
- name: first_critical
  type: data.find
  items: "${{ event.alerts }}"
  with:
    condition: "item.kibana.alert.severity : critical"
    errorIfEmpty: false
```

### `data.aggregate` [data-aggregate]

Group a collection by one or more keys and compute metrics per group. Supported operations: `count`, `sum`, `avg`, `min`, `max`.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `items` | top level | array | Yes | Source array. |
| `group_by` | `with` | `string[]` | Yes | Fields to group by. |
| `metrics` | `with` | array | Yes | Array of `{ name, operation, field? }` metrics. `count` doesn't need a `field`; the others do. |
| `order` | `with` | string | Yes | `asc` or `desc`. |
| `buckets` | `with` | object | No | Bucket configuration with `field` and `ranges`. Each range has `from`, `to`, and `label`; `from` or `to` can be omitted to create open-ended ranges. |
| `order_by` | `with` | string | No | Metric name to order by. |
| `limit` | `with` | number | No | Max number of buckets to return. |

Basic grouping:

```yaml
- name: count_by_host
  type: data.aggregate
  items: "${{ event.alerts }}"
  with:
    group_by: ["host.name"]
    metrics:
      - name: "count"
        operation: "count"
    order: "desc"
    order_by: "count"
    limit: 10
```

With bucketed aggregation:

```yaml
- name: age_distribution
  type: data.aggregate
  items: "${{ steps.fetch_users.output }}"
  with:
    group_by: ["department"]
    metrics:
      - name: "count"
        operation: "count"
    order: "desc"
    buckets:
      field: "age"
      ranges:
        - to: 30
          label: "junior"
        - from: 30
          to: 50
          label: "mid"
        - from: 50
          label: "senior"
```

---

## Combine and de-duplicate

### `data.concat` [data-concat]

Concatenate arrays. `arrays` is the top-level source field.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `arrays` | top level | `array[]` | Yes | Array of arrays to concatenate (maximum 50). |
| `dedupe` | `with` | boolean | No | Remove duplicates after concatenation. |
| `flatten` | `with` | `boolean` or number 1–10 | No | Flatten nested arrays. `true` flattens one level; a number flattens to that depth. |

```yaml
- name: combine_lists
  type: data.concat
  arrays:
    - "${{ steps.list_a.output }}"
    - "${{ steps.list_b.output }}"
  with:
    dedupe: true
```

### `data.dedupe` [data-dedupe]

Remove duplicates from an array. The uniqueness fields go in `with.keys`.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `items` | top level | array | Yes | Source array. |
| `strategy` | top level | string | No | `keep_first` (default) or `keep_last`. |
| `keys` | `with` | `string[]` | Yes | Fields that determine uniqueness. |

```yaml
- name: unique_hosts
  type: data.dedupe
  items: "${{ event.alerts }}"
  strategy: "keep_first"
  with:
    keys: ["host.name"]
```

---

## JSON

### `data.parseJson` [data-parsejson]

Parse a JSON string into an object.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `source` | top level | string | Yes | JSON string to parse. |

```yaml
- name: parse_payload
  type: data.parseJson
  source: "${{ steps.http_call.output.body }}"
```

:::{tip}
For inline parsing inside a Liquid expression (for example, inside another step's `body`), use the [`json_parse` Liquid filter](/explore-analyze/workflows/templating.md). Reach for `data.parseJson` when you want the parsed result as a separate named step output that downstream steps can reference.
:::

### `data.stringifyJson` [data-stringifyjson]

Serialize an object to a JSON string.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `source` | top level | any | Yes | Value to serialize. |
| `pretty` | `with` | boolean | No | Pretty-print the output with indentation. |

```yaml
- name: to_string
  type: data.stringifyJson
  source: "${{ steps.search.output }}"
  with:
    pretty: true
```

---

## Regex

:::{important}
The regex steps use the standard JavaScript engine, which is vulnerable to regular expression denial-of-service (ReDoS) with catastrophic backtracking patterns. To protect against this:

- Input strings are limited to **100 KB**.
- Patterns with unbounded quantifiers (for example, `.*` or `.+`) applied to overlapping character classes can hang the workflow. Prefer anchored patterns and specific character classes.
- Test your patterns with representative input before running at scale.
:::

### `data.regexExtract` [data-regexextract]

Extract matches from a string with a regular expression. `fields` maps output field names to capture group references (`$1`, `$2`, or named groups).

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `source` | top level | string | Yes | Source string. |
| `errorIfNoMatch` | top level | boolean | No | Fail the step if the regex doesn't match. |
| `pattern` | `with` | regex string | Yes | Regular expression. |
| `fields` | `with` | object | Yes | Map of output field names to group references. |
| `flags` | `with` | string | No | Regex flags (for example, `i`, `g`). |

```yaml
- name: pull_user_id
  type: data.regexExtract
  source: "${{ steps.log.output.message }}"
  errorIfNoMatch: false
  with:
    pattern: "user_id=(?<id>[a-f0-9]+)"
    fields:
      user_id: "id"
    flags: "i"
```

### `data.regexReplace` [data-regexreplace]

Replace regex matches in a string.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `source` | top level | string | Yes | Source string. |
| `detailed` | top level | boolean | No | Include match details in the output. |
| `pattern` | `with` | regex string | Yes | Regular expression. |
| `replacement` | `with` | string | Yes | Replacement string. |
| `flags` | `with` | string | No | Regex flags. |

```yaml
- name: redact_ssn
  type: data.regexReplace
  source: "${{ steps.log.output.message }}"
  with:
    pattern: "\\b\\d{3}-\\d{2}-\\d{4}\\b"
    replacement: "[REDACTED]"
    flags: "g"
```

## Related

- [Templating engine](/explore-analyze/workflows/templating.md): Liquid filters for small inline transformations.
- [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md): The `{{ }}` vs. `${{ }}` distinction and error-handling strategies.
- [Foreach step](/explore-analyze/workflows/steps/foreach.md): Pair with data steps for per-item work after filtering or mapping.
