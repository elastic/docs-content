---
navigation_title: Add variable controls
applies_to:
  stack: ga 9.2
  serverless: ga
products:
  - id: kibana
type: how-to
description: Add variable controls to an ES|QL query in Discover so you can change values without keeping several copies of the query.
---

# Add variable controls to Discover queries

Variable controls help you make your queries more dynamic instead of having to maintain several versions of almost identical queries. Viewers change the value from the control. The query stays one query.

## Before you begin

- You need an {{esql}} query in **Discover**. If you are new to that editor, start with [Get started with {{esql}} in Discover](try-esql.md).

## Create a variable control from the Discover editor [add-variable-control]

You can add them from your Discover {{esql}} query.

![Variable control in Discover](/explore-analyze/images/variable-control-discover.png " =75%")

:::{include} ../_snippets/variable-control-procedure.md
:::

:::{include} ../_snippets/variable-control-examples.md
:::

**Result:** The control appears for the query, and its variable is inserted where you created it.

### Allow multi-value selections in a Discover control [esql-multi-values-controls]
```{applies_to}
stack: preview 9.3
serverless: preview
```

:::{include} ../_snippets/multi-value-esql-controls.md
:::

#### Edit a variable control in Discover [edit-a-variable-control]

Once a control is active for your query, you can still edit it by hovering over it and by selecting the {icon}`pencil` **Edit** option that appears.

You can edit all the options described in [](#add-variable-control).

When you save your edits, the control is updated for your query.

### Import a Discover query along with its controls into a dashboard [import-discover-query-with-controls]

:::{include} ../_snippets/import-discover-query-controls-into-dashboard.md
:::

## Related pages

- [Use Discover with {{esql}}](use-esql.md)
- [Add variable controls to dashboards](../visualize/add-variable-controls.md)
- [Save a Discover session for reuse](save-open-search.md)
