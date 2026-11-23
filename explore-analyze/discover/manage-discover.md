---
navigation_title: Manage your view and sessions
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: overview
description: Customize the Discover view, keep explorations in tabs, save and share sessions, run long queries in the background, and create alert rules.
---

# Manage your Discover view and sessions

If you want to keep a **Discover** exploration, share it with others, or tailor how it looks, start here. A session stores your query, filters, and view, so you can save it, add it to a dashboard, copy or export its results, or turn it into an alert rule.

## Set up your workspace

* [Customize the Discover view](document-explorer.md) to show the columns, density, and layout you need.
* Keep [several explorations open side by side](work-with-tabs.md) in tabs.

## Save and share your explorations

* [Save sessions](save-open-search.md) to reuse your queries, filters, and views later, and open, find, or duplicate them.
* [Add sessions to dashboards](use-sessions-in-dashboards.md) as charts, tables, or whole sessions.
* [Copy results](copy-and-share-documents.md) as text, JSON, or Markdown, or share a link to a session or a document.
* [Export your results](export-discover-session.md) as a CSV file, or the session itself as JSON.
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` [Manage sessions programmatically](manage-sessions-programmatically.md) from scripts or a CI/CD pipeline, with the Discover sessions API.
* Run long queries in the [background](background-search.md).
* [Create an alert rule](generate-alerts-from-discover.md) from the query and filters of a session.

## Related pages

- [How Discover works](discover-get-started.md)
- [Explore your data in Discover](explore-data.md)
- [How to query in Discover's {{esql}} mode](use-esql.md)
- [How to query in Discover's classic mode](use-classic-mode.md)
