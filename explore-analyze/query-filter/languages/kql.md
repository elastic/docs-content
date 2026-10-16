---
meta_title: KQL - Kibana
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

# {{kib}} Query Language (KQL) [kuery-query]

The {{kib}} Query Language (KQL) is a text-based query language for filtering data. Enter a KQL query in the query bar of Discover, dashboards, and other {{kib}} apps to see only the documents that match.

* KQL only filters data. It does not aggregate, transform, or sort data.
* KQL is different from the [Lucene query language](lucene-query-syntax.md). Lucene has a different feature set.

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

To match any of several values on one field, use parentheses and `OR`. For the full syntax, refer to [Combining multiple queries](elasticsearch://reference/query-languages/kql.md#_combining_multiple_queries).


## Look up the full KQL syntax [kql-full-syntax]

To see how to match values, ranges, and wildcards, negate or combine conditions, and query multiple or nested fields, refer to the [KQL syntax reference](elasticsearch://reference/query-languages/kql.md).
