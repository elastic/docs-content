---
navigation_title: "ES|QL tools"
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# {{esql}} tools

{{esql}} query tools enable you to create parameterized queries that execute directly against your {{es}} data. These custom tools provide precise control over data retrieval through templated [{{esql}}](elasticsearch://reference/query-languages/esql.md) statements.

## When to use {{esql}} tools

Use custom **{{esql}} tools** when:

* You need precise control over the query logic
* Your use case involves repeatable analytical patterns
* You want to expose specific, parameterized queries to agents
* Results should be in a predictable tabular format
* You have well-defined data retrieval requirements

## Key characteristics

* Execute pre-defined {{esql}} queries with dynamic parameters
* Support typed parameters
* Return results in tabular format for structured data analysis
* Ideal for repeatable analytical queries with variable inputs

## Parameter types

{{esql}} tools support the following parameter types:

* **String types**: `text`, `keyword`
* **Numeric types**: `long`, `integer`, `double`, `float`
* **Other types**: `boolean`, `date`, `object`, `nested`

## Parameter options

Parameters can be configured as:

* **Required**: The agent must provide a value when calling the tool
* **Optional**: The agent can omit the parameter when calling the tool. You can set [default values for optional parameters](#default-values-for-optional-parameters).



### Default values for optional parameters

Optional parameters can have default values that are automatically applied when the agent doesn't provide a value. This ensures valid query syntax and consistent behavior.

When an agent calls a tool without specifying optional parameters, it automatically uses the defaults.
When the agent provides a value, it overrides the default.

#### Set default values in UI
```{applies_to}
stack: ga 9.4
serverless: ga
```

When creating {{esql}} tools in the Kibana UI, you must specify default values for all optional parameters. This requirement ensures that tools have sensible fallback behavior and prevents configuration errors that could cause queries to fail at runtime.


#### Set default values with API
```{applies_to}
stack: ga 9.3
serverless: ga
```

When creating {{esql}} tools via the API, default values for optional parameters are not required. However, they are strongly recommended to prevent query syntax errors when agents don't provide values. Without defaults, optional parameters that agents don't specify will be `null`, which can cause queries to fail.

For details about the {{esql}} tools API, refer to the [API documentation](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-agent-builder-tools).

## Query syntax

In your {{esql}} query, reference parameters using the `?parameter_name` syntax. The agent will automatically interpolate parameter values when executing the query.

### Example

Here's an example {{esql}} tool that searches for books using full-text search. `?search_terms` is a named parameter that the agent will provide when executing the query. 

```esql
FROM books
| WHERE MATCH(title, ?search_terms)
| KEEP title, author, year
| LIMIT 10
```

You can ask the LLM to infer the parameters for the query or add them manually.

:::{image} ../images/create-esql-tool-query.png
:screenshot:
:alt: Creating an ES|QL tool with a parameterized query
:::

:::{note}
For API examples, refer to [](/explore-analyze/ai-features/agent-builder/kibana-api.md#tools)
:::

## Best practices

- **Include [`LIMIT`](elasticsearch://reference/query-languages/esql/commands/limit.md) clauses**: Prevent returning excessive results by setting reasonable limits
- **Use meaningful parameter names**: Choose names that clearly indicate what the parameter represents (for example, `start_date` instead of `date1`)
- **Define parameter types**: Ensure parameters have the correct type to avoid runtime errors
- **Provide clear descriptions**: Help agents understand when and how to use each parameter
- **Use [default values](#default-values-for-optional-parameters)** for optional parameters: Set sensible defaults for optional parameters to reduce complexity for agents and ensure consistent behavior when parameters are omitted {applies_to}`stack: ga 9.3`

For general guidance on naming tools and writing effective descriptions, refer to [Custom tools best practices](custom-tools.md#best-practices).

:::{tip}
If queries are slow or failing, you might be retrieving more data than the LLM can process. Refer to [Context length exceeded](../troubleshooting/context-length-exceeded.md) for tips on diagnosing and resolving these issues.
:::

## Limitations

{{esql}} tools are subject to the current limitations of the {{esql}} language itself. For more information, refer to [{{esql}} tool limitations](../limitations-known-issues.md#esql-limitations).

## {{esql}} documentation

To learn more about the language, refer to the [{{esql}} docs](elasticsearch://reference/query-languages/esql.md).