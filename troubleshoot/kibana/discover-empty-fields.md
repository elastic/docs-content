---
navigation_title: Empty fields in Discover
description: Find out why some fields show as empty in Discover even though your data has values for them, and how to see those values in the table.
type: troubleshooting
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Some fields show as empty in Discover [discover-empty-fields]

A field that you add to the **Discover** table shows empty cells even though your data has values for it. For other common issues, refer to the blog post [Learn how to resolve common issues with Discover](https://www.elastic.co/blog/troubleshooting-guide-common-issues-kibana-discover-load).

## Symptoms

Cells of a field you added as a column are empty for some or all results, while you expect values.

## Causes

This can happen in several cases:

* With runtime fields and regular keyword fields, when the string exceeds the value set for the [ignore_above](elasticsearch://reference/elasticsearch/mapping-reference/ignore-above.md) setting used when indexing the data into {{es}}.
* Due to the structure of nested fields, a leaf field added to the table as a column doesn't contain values in any of its cells.

## Resolution

For a nested field, add the root field as a column to view a JSON representation of its values. Learn more in [this blog post](https://www.elastic.co/de/blog/discover-uses-fields-api-in-7-12).
