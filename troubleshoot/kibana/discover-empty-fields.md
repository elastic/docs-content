---
navigation_title: Empty fields in Discover
description: Find out why some fields show as empty in Discover even though your data has values for them, and how to see those values in the table.
type: troubleshooting
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
---

# Some fields show as empty in Discover [discover-empty-fields]

A field that you add to the **Discover** table can show empty cells even though your data has values for it. For other common issues, refer to the blog post [Learn how to resolve common issues with Discover](https://www.elastic.co/blog/troubleshooting-guide-common-issues-kibana-discover-load).

## Symptoms

* The cells of a field that you added as a column in the results table are empty for some or all results.
* You expect values for that field.

## Causes

This can happen in several cases:

* With runtime fields and regular keyword fields, when the string exceeds the value set for the [ignore_above](elasticsearch://reference/elasticsearch/mapping-reference/ignore-above.md) setting used when indexing the data into {{es}}.
* Due to the structure of nested fields, a leaf field added to the table as a column doesn't contain values in any of its cells.

## Resolution

If the field is a nested field:

1. Open the fields list in the sidebar and find the root field of the nested field.
2. Add the root field as a column. The table shows a JSON representation of the values of the nested field.

To learn more about how **Discover** reads nested fields, refer to the blog post about how [Discover uses the Fields API](https://www.elastic.co/blog/discover-uses-fields-api-in-7-12).

If the field is a keyword field with long strings, check the `ignore_above` setting in the [mapping reference](elasticsearch://reference/elasticsearch/mapping-reference/ignore-above.md).
