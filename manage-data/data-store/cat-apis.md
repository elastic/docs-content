---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/cat.html
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Compact and aligned text (CAT) APIs [cat-apis]

The compact and aligned text (CAT) APIs return data in a human-readable, tabular format. They are intended only for use in the Kibana console or on the command line.

:::{important}
CAT APIs are intended only for human consumption. They are not intended for use by applications. For application consumption, use the corresponding JSON APIs.
:::

## List all CAT APIs [cat-list-all]

Use `GET /_cat` to see a list of all available CAT APIs:

```console
GET /_cat
```

## Common query parameters [cat-query-params]

All CAT APIs support the following query parameters:

`v`
:   (Optional, Boolean) If `true`, enables verbose output that adds headers to each column. Defaults to `false`.

`help`
:   (Optional, Boolean) If `true`, outputs available columns. This option can't be combined with any other query string option. Defaults to `false`.

`h`
:   (Optional, string) A comma-separated list of column names to display. Supports simple wildcards.

`s`
:   (Optional, string) A comma-separated list of column names or column aliases used to sort the response. Appending `:asc` or `:desc` to a column name sorts the response in ascending or descending order respectively.

`format`
:   (Optional, string) Specifies the format for the response. Options are `text` (default), `json`, `cbor`, `yaml`, and `smile`.

`bytes`
:   (Optional, [byte size units](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#byte-units)) Sets the unit used to display byte values.

`time`
:   (Optional, [time units](elasticsearch://reference/elasticsearch/rest-apis/api-conventions.md#time-units)) Sets the unit used to display time values.

## Display available columns [cat-display-columns]

Use the `help` query parameter to display all available columns for a CAT API and their descriptions:

```console
GET /_cat/indices?help
```

This is useful for discovering which columns you can select with the `h` parameter.

## Verbose output [cat-verbose-output]

By default, CAT API responses don't include column headers. Use the `v` parameter to enable verbose output and add column names to the response:

```console
GET /_cat/indices?v=true
```

## Select columns [cat-select-columns]

Use the `h` parameter to select which columns to display. The following example shows only the `index`, `health`, and `docs.count` columns:

```console
GET /_cat/indices?h=index,health,docs.count
```

To display verbose output with selected columns:

```console
GET /_cat/indices?v=true&h=index,health,docs.count
```

## Sort results [cat-sort-results]

Use the `s` parameter to sort the response by one or more columns. Append `:asc` or `:desc` to specify the sort direction:

```console
GET /_cat/nodes?v=true&s=cpu:desc
```

## Response formats [cat-response-formats]

By default, CAT APIs return data as plain text. To get JSON output instead, use the `format` parameter:

```console
GET /_cat/indices?format=json
```

## Related resources [cat-resources]

For detailed information about individual CAT APIs, including their specific parameters and response columns, refer to the [CAT API reference](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-cat).
