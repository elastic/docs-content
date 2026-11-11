---
navigation_title: Add variable controls
applies_to:
  serverless: preview
  stack: preview 9.2
products:
  - id: kibana
type: how-to
description: Add variable controls to an ES|QL query in Discover so you can change values without keeping several copies of the query.
---

# Add variable controls to Discover queries

If you run the same query again and again with a different value each time, a variable control lets you pick that value from a list instead of editing the query. For example, a control can switch the field that a query groups by. The query holds a variable, such as `?field`, and the control fills it in.

## Before you begin

- Make sure **Discover** is in {{esql}} mode. Classic mode doesn't support this functionality. To switch, refer to [Switch to Discover's {{esql}} mode](switch-esql-mode.md#switch-discover-query-mode).
- If you're new to {{esql}} in Discover, start with [Get started with {{esql}} in Discover](try-esql.md).

## Create a variable control from the Discover editor [add-variable-control]

You create a control while you write the query, from the editor's autocomplete menu.

:::{image} /explore-analyze/images/variable-control-discover.png
:alt: The Create variable control panel beside an ES|QL query, with Create control in the editor's autocomplete menu.
:screenshot:
:width: 75%
:::

:::{include} ../_snippets/variable-control-procedure.md
:::

:::{include} ../_snippets/variable-control-examples.md
:::

**Result:** The control appears for the query, and Discover inserts its variable where you created it.

:::{image} /explore-analyze/images/kibana-discover-esql-variable-control.png
:alt: A Count by control set to host.keyword in Discover, with its list of fields open.
:screenshot:
:width: 75%
:::

### Allow multi-value selections in a Discover control [esql-multi-values-controls]
```{applies_to}
serverless: preview
stack: preview 9.3
```

:::{include} ../_snippets/multi-value-esql-controls.md
:::

### Edit a variable control in Discover [edit-a-variable-control]

To change a control, hover over it and select the {icon}`pencil` edit button. You can change every option except the name, so the `?` or `??` prefix stays the same. For the options, refer to [](#add-variable-control). When you save your edits, Discover updates the control for your query.

### Add a Discover query and its controls to a dashboard [import-discover-query-with-controls]

:::{include} ../_snippets/import-discover-query-controls-into-dashboard.md
:::

## Related pages

- [How to query in Discover's {{esql}} mode](use-esql.md)
- [Add variable controls to dashboards](../visualize/add-variable-controls.md)
- [Save and manage Discover sessions](save-open-search.md)
