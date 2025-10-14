---
navigation_title: "Index search tools"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

:::{warning}
These pages are currently hidden from the docs TOC and have `noindexed` meta headers.

**Go to the docs [landing page](/solutions/search/elastic-agent-builder.md).**
:::

# Index search tools

Index search tools provide intelligent, natural language-driven search over specified {{es}} resources. Instead of defining explicit queries, you specify a pattern of [indices](/manage-data/data-store/index-basics.md), [aliases](/manage-data/data-store/aliases.md), or [data streams](/manage-data/data-store/data-streams.md), and the tool uses a combination of built-in capabilities to intelligently interpret and execute search requests.

## When to use index search tools

Use custom **Index search tools** when:

* You want agents to handle diverse, exploratory queries
* The search intent varies significantly across requests
* Users need flexible, ad-hoc search functionality
* You want to scope general search capabilities to specific indices

## Key characteristics

* Accept natural language queries from the agent
* Automatically determine optimal search strategy (full-text, semantic)
* Leverage built-in tools like index exploration, query generation, and semantic search
* Ideal for flexible, user-driven exploratory searches
* No need to pre-define query logic

## Configuration

Index search tools require only a single configuration parameter:

* **`pattern`**: An index pattern string (e.g., `logs-*`, `my-index`, `.alerts-*`) specifying which indices, aliases, or data streams to search

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


## Common patterns

* **Wildcard patterns**: `logs-*`, `metrics-*`, `events-*`
* **Specific indices**: `products`, `users`, `orders`
* **System indices**: `.alerts-security-*`, `.ml-anomalies-*`
* **All resources**:  `*`
