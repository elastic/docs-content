---
navigation_title: "ES|QL tools"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
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

* **Required**: Must be provided by the agent when calling the tool
* **Optional**: Can be omitted; uses `null` if no default is specified

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
:alt: Creating an ES|QL tool with a parameterized query
:::

## Best practices

- **Include [`LIMIT`](elasticsearch://reference/query-languages/esql/commands/limit.md) clauses**: Prevent returning excessive results by setting reasonable limits
- **Use meaningful parameter names**: Choose names that clearly indicate what the parameter represents (e.g., `start_date` instead of `date1`)
- **Define parameter types**: Ensure parameters have the correct type to avoid runtime errors
- **Provide clear descriptions**: Help agents understand when and how to use each parameter

## Limitations

{{esql}} tools are subject to the current limitations of the {{esql}} language itself. For more information, refer to [{{esql}} tool limitations](../../../search/agent-builder/limitations-known-issues.md#esql-limitations).

## {{esql}} documentation

To learn more about the language, refer to the [{{esql}} docs](elasticsearch://reference/query-languages/esql.md).
