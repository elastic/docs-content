---
navigation_title: Advanced features
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Advanced features for data exploration in Discover including document comparison, runtime fields, tabs, background queries, alerts, and pattern analysis.
---

# Advanced data exploration features in Discover

After mastering the basics of **Discover**, these advanced features help you work more efficiently with complex data exploration tasks. Compare documents to identify differences, create runtime fields without reindexing, run multiple explorations simultaneously, and set up automated monitoring with alerts.

## Advanced data manipulation

* **[Compare documents](compare-documents.md)** - Compare field values across multiple documents side by side to identify differences and patterns.
* **[Add fields to your {{data-source}}](add-fields-to-data-views.md)** - Create runtime fields on the fly to extend your data model without reindexing.

## Specialized exploration

* **[Work with tabs](work-with-tabs.md)** - Run multiple explorations simultaneously in separate tabs to compare queries, time periods, or data sources.
* **[Context-aware experiences](context-aware-discover.md)** - Understand how Discover adapts its interface for logs, metrics, traces, and security data.
* **[Run queries in the background](background-search.md)** - Send long-running queries to the background while you continue working.

## Integration and analysis

* **[Generate alerts from Discover](generate-alerts-from-discover.md)** - Create rules that periodically check your data against conditions and send notifications.
* **[View field statistics](show-field-statistics.md)** - Explore field distributions, top values, and statistical summaries.
* **[Run pattern analysis](run-pattern-analysis-discover.md)** - Find patterns in unstructured log messages with log pattern analysis.
* **[Search for relevance](discover-search-for-relevance.md)** - Sort documents by relevance score to find the most relevant results.

