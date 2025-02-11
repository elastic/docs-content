---
navigation_title: "Conditions"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/condition.html
---

# Conditions [condition]

When a watch is triggered, its condition determines whether or not to execute the watch actions. {{watcher}} supports the following condition types:

* [`always`](condition-always.md): The condition always evaluates to `true`, so the watch actions are always performed.
* [`never`](condition-never.md): The condition always evaluates to `false`, so the watch actions are never executed.
* [`compare`](condition-compare.md): perform simple comparisons against values in the watch payload to determine whether or not to execute the watch actions.
* [`array_compare`](condition-array-compare.md): compare an array of values in the watch payload to a given value to determine whether or not to execute the watch actions.
* [`script`](condition-script.md): use a script to determine whether or not to execute the watch actions.

::::{note}
If you omit the condition definition from a watch, the condition defaults to `always`.
::::

When a condition is evaluated, it has full access to the watch execution context, including the watch payload (`ctx.payload.*`). The [script](condition-script.md), [compare](condition-compare.md)  and [array_compare](condition-array-compare.md) conditions can use the payload data to determine whether or not the necessary conditions are met.

In addition to the watch wide condition, you can also configure conditions per [action](action-conditions.md).
