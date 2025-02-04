---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/lucene-query.html
---

# Lucene query syntax [lucene-query]

Lucene query syntax is available to {{kib}} users who opt out of the [{{kib}} Query Language](kql.md). Full documentation for this syntax is available as part of {{es}} [query string syntax](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax).

The main reason to use the Lucene query syntax in {{kib}} is for advanced Lucene features, such as regular expressions or fuzzy term matching. However, Lucene syntax is not able to search nested objects or scripted fields.

To use the Lucene syntax, open the **Saved query** menu, and then select **Language: KQL** > **Lucene**.

![Click the circle icon for the saved query menu](../../../images/kibana-lucene.png "")

To perform a free text search, simply enter a text string. For example, if you’re searching web server logs, you could enter `safari` to search all fields:

```yaml
safari
```

To search for a value in a specific field, prefix the value with the name of the field:

```yaml
status:200
```

To search for a range of values, use the bracketed range syntax, `[START_VALUE TO END_VALUE]`. For example, to find entries that have 4xx status codes, you could enter `status:[400 TO 499]`.

```yaml
status:[400 TO 499]
```

For an open range, use a wildcard:

```yaml
status:[400 TO *]
```

To specify more complex search criteria, use the boolean operators `AND`, `OR`, and `NOT`. For example, to find entries that have 4xx status codes and have an extension of `php` or `html`:

```yaml
status:[400 TO 499] AND (extension:php OR extension:html)
```

