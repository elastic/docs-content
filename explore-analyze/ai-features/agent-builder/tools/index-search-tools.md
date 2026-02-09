---
navigation_title: "Index search tools"
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



# Index search tools

Index search tools provide intelligent, natural language-driven search over specified {{es}} resources. Instead of defining explicit queries, you specify a pattern of [indices](/manage-data/data-store/index-basics.md), [aliases](/manage-data/data-store/aliases.md), or [data streams](/manage-data/data-store/data-streams.md), and the tool uses a combination of built-in capabilities to intelligently interpret and execute search requests. The tool automatically generates queries in Query DSL or {{esql}} format based on the search intent.

## When to use index search tools

Use custom **Index search tools** when:

* You want agents to handle diverse, exploratory queries
* The search intent varies significantly across requests
* Users need flexible, dynamic search functionality
* You want to scope general search capabilities to specific indices

## Key characteristics

* Accept natural language queries from the agent
* Automatically determine optimal search strategy (full-text, semantic)
* Leverage built-in tools like index exploration, query generation, and semantic search
* Ideal for flexible, user-driven exploratory searches
* No need to pre-define query logic

## Configuration

Index search tools support the following configuration parameters:

`pattern`
:   An index pattern string (e.g., `logs-myapp-*`, `my-index`, `.alerts-security-*`) specifying which indices, aliases, or data streams to search.

    :::{tip}
    [Avoid overly broad wildcard patterns](#wildcard-warning) like `*` or `logs-*` across large datasets.
    :::

`row_limit` (optional)
:   Maximum number of rows to return from {{esql}} queries. This helps control the amount of data retrieved and prevents exceeding context length limits.

`custom_instructions` (optional)
:   Domain-specific guidance for {{esql}} query generation. For example: `"Always include @timestamp and filter out records where environment='test'"`.

## How it works

When an agent calls an index search tool:

1. The agent provides a natural language query (e.g., "find recent errors related to authentication")
2. The tool analyzes the query intent and available indices
3. It automatically orchestrates built-in tools to:
   - Explore the index structure and mappings
   - Generate appropriate queries ({{esql}} or query DSL)
   - Execute semantic search if relevant
   - Rank and format results
4. Returns results in a format the agent can interpret and present


## Best practices

- **Use specific patterns**: Scope tools to relevant index patterns rather than broad wildcards (e.g., `logs-myapp-*` instead of `logs-*`)
- **Write descriptive tool names**: Help agents select the right tool for the query (e.g., "Search Security Alerts" vs. "Search Tool")
- **Provide context in descriptions**: Explain what data the indices contain and what types of questions the tool can answer
- **Create domain-specific tools**: Build separate tools for different data domains (logs, metrics, alerts) rather than one general-purpose tool
- **Use custom instructions wisely**: Leverage the custom instructions parameter to guide {{esql}} query generation with domain-specific requirements, such as always including certain fields, applying specific filters, or handling time ranges in a particular way
- **Set appropriate row limits**: Configure row limits to prevent retrieving excessive data that could exceed context length limits

For general guidance on naming tools and writing effective descriptions, refer to [Custom tools best practices](custom-tools.md#best-practices).


## Common patterns

* **Wildcard patterns**: `logs-*`, `metrics-*`, `events-*`
* **Specific indices**: `products`, `users`, `orders`

$$$wildcard-warning$$$
:::{warning}
Avoid overly broad patterns like `*` or `logs-*` across large datasets. Broad wildcards can cause the agent to retrieve more data than the LLM can process, resulting in slow responses or errors. Refer to [Context length exceeded](../troubleshooting/context-length-exceeded.md) for tips on diagnosing and resolving these issues.
:::
