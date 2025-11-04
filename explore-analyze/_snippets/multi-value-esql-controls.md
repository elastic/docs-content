You can create controls that let users select multiple values. To do that:

1. Add the [`MV_CONTAINS`](elasticsearch://reference/query-languages/esql/functions-operators/mv-functions.md#esql-mv_contains) function to your query, and [create a variable](#add-variable-control) as one of its parameters. For example:

    ```esql
    FROM logs-* | WHERE MV_CONTAINS(?values, field)
    ```

    :::{note}
    Multi-selection is only available for `?values` variables. It is not available for `??fields` and `??functions` variables.
    :::

2. When defining the control, select the **Allow multiple selections** option.

3. Save the control.

The newly configured control becomes available and allows users to select multiple values.
