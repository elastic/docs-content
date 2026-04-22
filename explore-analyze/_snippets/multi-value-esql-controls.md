You can create controls that let users select multiple values. To do that:

1. Add the [`MV_CONTAINS`](elasticsearch://reference/query-languages/esql/functions-operators/mv-functions/mv_contains.md) function to your query, with the field as the first parameter (superset) and a [variable](#add-variable-control) as the second parameter (subset). For example:

    ```esql
    FROM logs-* | WHERE MV_CONTAINS(field, ?values)
    ```

    :::{note}
    Multi-selection is only available for `?values` variables. It is not available for `??fields` and `??functions` variables.
    :::

    :::{note}
    [`MV_CONTAINS`](elasticsearch://reference/query-languages/esql/functions-operators/mv-functions/mv_contains.md) checks that _all_ subset values are present. Use [`MV_INTERSECTS`](elasticsearch://reference/query-languages/esql/functions-operators/mv-functions/mv_intersects.md) instead if matching _any_ subset value is enough.
    :::

3. When defining the control, select the **Allow multiple selections** option.

4. Save the control.

The newly configured control becomes available and allows users to select multiple values.
