---
description: Customize the fields in a Kibana data view by adding runtime or scripted fields and changing how fields are displayed.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Customize data view fields [managing-data-views]

To customize the fields in your data view, you can add runtime fields to the existing documents, add scripted fields to compute data on the fly, and change how {{kib}} displays the data view fields.

* [Explore your data with runtime fields](runtime-fields.md) — add fields after ingestion, evaluated at query time
* [Manage scripted fields](scripted-fields.md) — deprecated in favor of runtime fields and {{esql}}
* [Format data view fields](field-formatters.md) — reference for the available field formatters
* [Data view field cache](data-view-field-cache.md) — how {{kib}} caches field lists in the browser

## Related pages

* [Data views](../data-views.md)
