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

Variable controls make your queries dynamic, so you don't need to keep several versions of almost identical queries. You change the value from the control, and the query stays the same.

## Before you begin

- You need an {{esql}} query in **Discover**. If you're new to {{esql}} in Discover, start with [Get started with {{esql}} in Discover](try-esql.md).

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

After a control is active for your query, you can still edit it. Hover over the control, then select the {icon}`pencil` **Edit** option.

You can edit all the options described in [](#add-variable-control).

When you save your edits, Discover updates the control for your query.

### Import a Discover query along with its controls into a dashboard [import-discover-query-with-controls]

:::{include} ../_snippets/import-discover-query-controls-into-dashboard.md
:::

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Add variable controls to dashboards](../visualize/add-variable-controls.md)
- [Save a Discover session for reuse](save-open-search.md)
