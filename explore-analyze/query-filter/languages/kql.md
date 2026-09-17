---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/kuery-query.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
description: Filter documents in Kibana with KQL. Match fields, ranges, wildcards, and boolean conditions in Discover, dashboards, and other Kibana apps.
---

# KQL [kuery-query]

The {{kib}} Query Language (KQL) is a text-based query language for filtering data.

* KQL only filters data. It does not aggregate, transform, or sort data.
* KQL is different from the [Lucene query language](lucene-query-syntax.md). Lucene has a different feature set.

Use KQL to filter documents by field existence, value, or range.

To compare KQL with Query DSL, {{esql}}, and other languages, refer to [Query languages](../languages.md).


## Semi-structured search [semi-structured-search]

Combine free text search with field-based search using KQL. Enter a term to match across all fields. Start typing a field name to get suggestions for fields and operators.

| Query type | Example |
| --- | --- |
| Exact phrase query | `http.response.body.content.text:"quick brown fox"` |
| Multiple values | `http.response.status_code: (400 OR 401 OR 404)` |
| Boolean query | `response:200 or extension:php` |
| Range query | `account_number >= 100 and items_sold <= 200` |
| Wildcard query | `machine.os:win*` |

To match any of several values on one field, use parentheses and `OR`. For the full syntax, refer to [Combining multiple queries](#_combining_multiple_queries).



## Filter for documents where a field exists [_filter_for_documents_where_a_field_exists]

To find documents where a field has an indexed value, use `*`. For example, documents where `http.request.method` exists:

```yaml
http.request.method: *
```

This matches any indexed value, including an empty string.


## Filter for documents that match a value [_filter_for_documents_that_match_a_value]

Use KQL to match a number, text, date, or boolean value. For example, documents where `http.request.method` is GET:

```yaml
http.request.method: GET
```

The field name is optional. If you omit it, KQL searches all fields for the given value. For example, to search all fields for “Hello”:

```yaml
Hello
```

On keyword, numeric, date, or boolean fields, the value must match exactly, including punctuation and case.

On `text` fields, {{es}} analyzes the value using the [field’s mapping settings](../../../solutions/search/full-text/text-analysis-during-search.md). For example, documents where `http.request.body.content` contains “null pointer”:

```yaml
http.request.body.content: null pointer
```

Because this is a `text` field, the order of these search terms does not matter. Documents that contain “pointer null” also match. To search `text` fields for terms in that order, surround the value in quotation marks:

```yaml
http.request.body.content: "null pointer"
```

Escape certain characters with a backslash, unless you surround the value with quotes. For example, either of these queries matches `http.request.referrer` [https://example.com](https://example.com):

```yaml
http.request.referrer: "https://example.com"
http.request.referrer: https\://example.com
```

Escape these characters:

```yaml
\():<>"*
```


## Filter for documents within a range [_filter_for_documents_within_a_range]

To find values in a range, use KQL range syntax. For example, `http.response.bytes` less than 10000:

```yaml
http.response.bytes < 10000
```

For an inclusive range, combine conditions. For example, bytes greater than 10000 and less than or equal to 20000:

```yaml
http.response.bytes > 10000 and http.response.bytes <= 20000
```

On multi-value fields, KQL tests each condition against every value in the array. `number > 300 AND number < 400` matches `"number": [500, 10]`. 500 matches the first condition and 10 matches the second. If one value must satisfy every condition, use [Query DSL](elasticsearch://reference/query-languages/query-dsl/query-dsl-range-query.md).

You can also use range syntax for strings, IP addresses, and timestamps. For example, documents earlier than two weeks ago:

```yaml
@timestamp < now-2w
```

For more examples on acceptable date formats, refer to [Date Math](elasticsearch://reference/elasticsearch/rest-apis/common-options.md#date-math).


## Filter for documents using wildcards [_filter_for_documents_using_wildcards]

To match a pattern, use a wildcard. You can use wildcards on keyword, text, and wildcard fields. They do not work on numeric, date, or boolean fields.

For example, `machine.os` values that begin with "win":

```yaml
machine.os: win*
```

Only `*` is supported. It matches zero or more characters.

By default, you can put `*` at the start of a pattern. For example, `url` values that contain `elastic`:

```yaml
url: *elastic*
```

Queries that start with `*` can slow searches.

{applies_to}`serverless: unavailable` To avoid that, turn leading wildcards off with the [`query:allowLeadingWildcards`](kibana://reference/advanced-settings.md#query-allowleadingwildcards) advanced setting.

## Negating a query [_negating_a_query]

To exclude documents, use the `not` keyword (not case-sensitive). For example, documents where `http.request.method` is not GET:

```yaml
NOT http.request.method: GET
```


## Combining multiple queries [_combining_multiple_queries]

To combine queries, use `AND` or `OR` (not case-sensitive). For example, GET requests or responses with status 400:

```yaml
http.request.method: GET OR http.response.status_code: 400
```

To require both conditions, use `AND`:

```yaml
http.request.method: GET AND http.response.status_code: 400
```

Use parentheses to set precedence. This example matches GET requests with status 200, or POST requests with status 400:

```yaml
(http.request.method: GET AND http.response.status_code: 200) OR
(http.request.method: POST AND http.response.status_code: 400)
```

You can also use parentheses to match several values on one field. For example, GET, POST, or DELETE:

```yaml
http.request.method: (GET OR POST OR DELETE)
```


## Matching multiple fields [_matching_multiple_fields]

You can also use wildcards to query multiple fields. For example, documents where any sub-field of `datastream` contains “logs”:

```yaml
datastream.*: logs
```

If the matching fields have different types, the query can fail. For example, if `datastream.*` matches both numeric and string fields, `datastream.*: logs` returns an error. You cannot query numeric fields for string values.

## Querying nested fields [_querying_nested_fields]

[Nested fields](elasticsearch://reference/elasticsearch/mapping-reference/nested.md) use a special syntax. Consider this document, where `user` is nested:

```json
{
  "user" : [
    {
      "first" : "John",
      "last" :  "Smith"
    },
    {
      "first" : "Alice",
      "last" :  "White"
    }
  ]
}
```

To find a `user` array value with first name “Alice” and last name “White”:

```yaml
user:{ first: "Alice" and last: "White" }
```

If nested fields contain other nested fields, use the full path. Consider this document, where `user` and `names` are both nested:

```json
{
  "user": [
    {
      "names": [
        {
          "first": "John",
          "last": "Smith"
        },
        {
          "first": "Alice",
          "last": "White"
        }
      ]
    }
  ]
}
```

To find a `user.names` array value with first name “Alice” **and** last name “White”:

```yaml
user.names:{ first: "Alice" and last: "White" }
```

