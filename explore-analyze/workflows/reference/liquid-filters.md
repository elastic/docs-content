---
navigation_title: Liquid filters
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Every Liquid filter available in workflow expressions, categorized, with worked examples for the two custom filters and the commonly-confused ones.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Liquid filters [workflows-liquid-filters]

Filters transform values inside Liquid expressions. Pipe a value through a filter with `|`. The workflow engine provides the standard [LiquidJS](https://liquidjs.com/filters/overview.html) filter set plus two custom additions: `json_parse` and `entries`.

This page is the full categorized catalog. For the mental model and syntax, refer to [Templating engine](/explore-analyze/workflows/templating.md).

## Custom filters (workflow-specific) [workflows-filters-custom]

### `json_parse` [workflows-filters-json-parse]

Parses a JSON string into a structured value. The counterpart of the standard `json` filter, which serializes a value to a JSON string.

```yaml
# HTTP response body is a JSON string; parse it to access fields
config: "{{ steps.http.output.body | json_parse }}"
host:   "{{ steps.http.output.body | json_parse | map: 'host' | first }}"
```

Use when you have a string that happens to be JSON and you need to index into it.

### `entries` [workflows-filters-entries]

Converts an object into an array of `[key, value]` pairs so you can iterate an object's properties.

```yaml
message: |
  {% for kv in steps.config.output | entries %}
    {{ kv[0] }}: {{ kv[1] }}
  {% endfor %}
```

Use when you don't know the keys in advance but you want to iterate them all.

:::{note}
`to_json` doesn't exist. For serialization, use [`json`](#workflows-filters-encoding); for parsing, use [`json_parse`](#workflows-filters-json-parse).
:::

## Strings [workflows-filters-strings]

`upcase`, `downcase`, `capitalize`, `strip`, `lstrip`, `rstrip`, `truncate`, `truncatewords`, `replace`, `replace_first`, `replace_last`, `remove`, `remove_first`, `remove_last`, `prepend`, `append`, `slice`, `strip_html`, `strip_newlines`, `slugify`, `number_of_words`, `escape`, `escape_once`.

Worked examples:

```yaml
# Uppercase
title: "{{ event.rule.name | upcase }}"

# Truncate with ellipsis
preview: "{{ steps.summary.output.text | truncate: 140 }}"

# Remove a substring
cleaned: "{{ msg | remove: 'REDACTED: ' }}"

# Slug for a URL
slug: "{{ event.rule.name | slugify }}"

# Replace and capitalize
friendly: "{{ raw | replace: '_', ' ' | capitalize }}"
```

## Arrays [workflows-filters-arrays]

`join`, `split`, `first`, `last`, `size`, `map`, `compact`, `sort`, `sort_natural`, `uniq`, `reverse`, `concat`, `push`, `pop`, `shift`, `unshift`, `where`, `where_exp`, `find`, `find_exp`, `has`, `has_exp`, `reject`, `reject_exp`, `group_by`, `group_by_exp`, `array_to_sentence_string`.

Worked examples:

```yaml
# Extract one field from each element
ids: "${{ event.alerts | map: '_id' }}"

# Filter by a simple equality
critical: "${{ event.alerts | where: 'kibana.alert.risk_score', 90 }}"

# Filter with an expression (where_exp) for OR / comparison / multi-field
high_severity: "${{ event.alerts | where_exp: 'a', 'a.severity == \"high\" or a.severity == \"critical\"' }}"

# Count
count: "{{ event.alerts | size }}"

# Join into a human-readable list
hosts: "{{ event.alerts | map: 'host.name' | uniq | join: ', ' }}"

# Group by a key
by_host: "${{ event.alerts | group_by: 'host.name' }}"
```

:::{tip}
Use `where: <field>, <value>` for simple equality. Use `where_exp: <name>, '<expr>'` for anything more complex (OR conditions, comparisons, multi-field predicates).
:::

## Numbers [workflows-filters-numbers]

`abs`, `ceil`, `floor`, `round`, `plus`, `minus`, `times`, `divided_by`, `modulo`, `at_least`, `at_most`.

Worked examples:

```yaml
# Percent with rounding
pct: "{{ error_rate | times: 100 | round: 2 }}%"

# Clamp to a ceiling
capped: "{{ count | at_most: 1000 }}"

# Arithmetic
next: "{{ variables.counter | plus: 1 }}"
```

## Dates [workflows-filters-dates]

`date`, `date_to_string`, `date_to_long_string`, `date_to_rfc822`, `date_to_xmlschema`.

Worked examples:

```yaml
# Custom format (strftime)
today: "{{ now | date: '%Y-%m-%d' }}"

# Timezone-aware output
at: "{{ execution.startedAt | date: '%Y-%m-%d %H:%M:%S %Z' }}"

# ISO 8601 (XML schema)
iso: "{{ now | date_to_xmlschema }}"
```

## Encoding and JSON [workflows-filters-encoding]

`json`, `json_parse` (custom), `base64_encode`, `base64_decode`, `url_encode`, `url_decode`, `cgi_escape`, `uri_escape`, `xml_escape`.

Worked examples:

```yaml
# Serialize to a JSON string (for logging or string bodies)
payload: "{{ event.alerts[0] | json }}"

# Parse a JSON string (the counterpart)
parsed: "{{ steps.http.output.body | json_parse }}"

# URL-encode a query parameter
search_url: "https://example.com/search?q={{ inputs.term | url_encode }}"

# Base64 for basic auth
basic: "{{ inputs.user | append: ':' | append: inputs.pass | base64_encode }}"
```

## Objects [workflows-filters-objects]

`entries` (custom), `default`.

Worked examples:

```yaml
# Fallback for missing values
name: "{{ event.alerts[0].host.name | default: 'unknown' }}"

# Iterate object keys
message: |
  {% for kv in steps.config.output | entries %}
    - {{ kv[0] }} = {{ kv[1] }}
  {% endfor %}
```

## Chain filters [workflows-filters-chain]

Filters compose. The output of one feeds the next:

```yaml
top_3_hosts: "{{ event.alerts | map: 'host.name' | uniq | slice: 0, 3 | join: ', ' }}"
```

Reads left to right: map each alert to its host name, remove duplicates, take the first three, join with commas.

## Related [workflows-filters-related]

- [Templating engine](/explore-analyze/workflows/templating.md): The mental model and the `{{ }}` vs. `${{ }}` distinction.
- [Context variables](/explore-analyze/workflows/reference/context-variables.md): The data you can filter.
- [Data steps](/explore-analyze/workflows/steps/data.md): For transformations too big for filters (filter, group, parse, extract).
- [LiquidJS documentation](https://liquidjs.com/filters/overview.html): Upstream filter semantics and corner cases.
