---
meta_title: Kibana Query Language (KQL) - Kibana
navigation_title: KQL
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/kuery-query.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: overview
description: Use Kibana Query Language (KQL) to filter data in Discover, dashboards, and other Kibana apps. See example queries and find where to learn the full syntax.
---

# {{kib}} Query Language (KQL) overview [kuery-query]

{{kib}} Query Language (KQL) is a text-based language for filtering data in {{kib}}. Enter a KQL query in the query bar of **Discover**, dashboards, and other {{kib}} apps to narrow the data down to the documents you care about. You can start with plain text and add field conditions when you need more precision. You can also use KQL syntax in the Query DSL [`kql` clause](elasticsearch://reference/query-languages/query-dsl/query-dsl-kql-query.md) in {{es}} and the {{esql}} [`KQL` function](elasticsearch://reference/query-languages/esql/functions-operators/search-functions/kql.md).

## When to use KQL [kql-when-to-use]

Use KQL when you want to:

* Search for a word or phrase without naming a field.
* Find documents where a field exists, matches a value, or falls in a range.
* Combine, exclude, or group conditions with `AND`, `OR`, and `NOT`.

KQL only filters data. It does not aggregate, transform, or sort data. For those tasks, use a language such as {{esql}}.

## How KQL works [kql-how-it-works]

A KQL condition is a field name, an operator, and a value, such as `http.request.method: GET`. If you leave out the field name, KQL searches the index's [default fields](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-query-default-field). As you type in the query bar, {{kib}} suggests fields, operators, and values.

By default, the query bar of dashboards and of **Discover** in classic mode uses KQL. In **Discover**, you can also switch the query bar to the [Lucene query language](lucene-query-syntax.md), which has a different feature set.

## Combine free text with field-based search [semi-structured-search]

To search without naming a field, enter a term. To narrow the results, start typing a field name and select a suggested field and operator. You can mix both in one query.

These examples show common patterns:

| Query type | Example |
| --- | --- |
| Exact phrase query | `http.response.body.content.text: "quick brown fox"` |
| Multiple values | `http.response.status_code: (400 OR 401 OR 404)` |
| Boolean query | `response: 200 OR extension: php` |
| Range query | `account_number >= 100 AND items_sold <= 200` |
| Wildcard query | `machine.os: win*` |

## Next steps [kql-next-steps]

* [KQL syntax reference](elasticsearch://reference/query-languages/kql.md): Look up how to match values, ranges, and wildcards, negate or combine conditions, and query multiple or nested fields.
* [Search and filter data in Discover](../../discover/discover-get-started.md#search-in-discover): Try KQL on your own data.
* [Search and filter your dashboard data](../../dashboards/using.md#search-or-filter-your-data): Use the query bar to focus a dashboard.

## Related pages [kql-related-pages]

* [Query languages](../languages.md): Compare KQL with Query DSL, {{esql}}, and other languages.
* [Lucene query syntax in {{kib}}](lucene-query-syntax.md)
