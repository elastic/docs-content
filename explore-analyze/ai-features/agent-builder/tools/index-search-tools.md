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
:   An index pattern string specifying which indices, aliases, or data streams to search. Examples: `logs-myapp-*`, `my-index`, `.alerts-security-*`.

    :::{tip}
    [Avoid overly broad wildcard patterns](#wildcard-warning) like `*` or `logs-*` across large datasets.
    :::

`row_limit` (optional)
:   Maximum number of rows to return from {{esql}} queries. This helps control the amount of data retrieved and prevents exceeding context length limits.

`custom_instructions` (optional)
:   Domain-specific guidance for {{esql}} query generation. For example: `"Always include @timestamp and filter out records where environment='test'"`.

## How it works

When an agent calls an index search tool:

1. The agent provides a natural language query (for example, "find recent errors related to authentication")
2. The tool analyzes the query intent and available indices
3. It automatically orchestrates built-in tools to:
   - Explore the index structure and mappings
   - Generate appropriate queries ({{esql}} or query DSL)
   - Execute semantic search if relevant
   - Rank and format results
4. Returns results in a format the agent can interpret and present

To help agents make better decisions during the source selection phase, you can optimize your index metadata and tool configurations.

## Optimize with metadata

You can add metadata to your index mappings to help agents make better decisions. Index-level [`_meta.description`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-meta-field.md) helps agents select the appropriate indices, while [field-level `meta`](elasticsearch://reference/elasticsearch/mapping-reference/mapping-field-meta.md) helps agents generate better {{esql}} queries.

#### Example: Add index-level metadata

```console
PUT /ecommerce-orders-2025/_mapping
{
  "_meta": {
    "description": "Primary dataset for North American customer orders in 2025. Use this for questions about order values, shipping status, or customer purchase history. Do not use for real-time inventory levels—use the inventory index instead. RELATIONSHIPS: 'customer_id' links to 'customer-profiles' index. NOTES: 'total_amount' includes tax; use 'subtotal' for pre-tax calculations." <1>
  },
  "properties": {
    "order_id": { "type": "keyword" },
    "total_amount": { "type": "double" }, <2>
    "created_at": { "type": "date" },
    "customer_support_notes": { "type": "text" }
  }
}
```
1. Include usage guidance, limitations, relationships, and field semantics in the description
2. Example of fields that might need semantic clarification in the description

#### Example: Add field-level metadata

```console
PUT /ecommerce-orders-2025/_mapping
{
  "properties": {
    "total_amount": {
      "type": "double",
      "meta": {
        "description": "Total order amount including tax. For pre-tax calculations, use the subtotal field instead." <1>
      }
    },
    "status": {
      "type": "keyword",
      "meta": {
        "description": "Order status. Valid values: pending, processing, shipped, delivered, cancelled." <2>
      }
    }
  }
}
```
1. Clarify field semantics to prevent incorrect calculations
2. Document valid values to help agents generate accurate filter conditions

## Best practices

- **Add index [metadata](#optimize-with-metadata) descriptions**: Include `_meta.description` fields in your index mappings:
  - Explain what entities or events the index covers
  - Note what types of questions it can answer
  - Document how fields link to other indices
  - State what the index should NOT be used for
  - Clarify non-obvious field meanings or calculations
- **Use specific patterns**: Scope tools to relevant index patterns rather than broad wildcards (for example, `logs-myapp-*` instead of `logs-*`)
- **Write descriptive tool names**: Help agents select the right tool for the query (for example, "Search Security Alerts" vs. "Search Tool")
- **Provide context in descriptions**: Explain what data the indices contain and what types of questions the tool can answer
- **Create domain-specific tools**: Build separate tools for different data domains (logs, metrics, alerts) rather than one general-purpose tool. In enterprise environments with hundreds of indices, creating scoped search tools prevents the agent from wasting tokens scanning irrelevant data. For example, a "Finance Agent" should not search through "Customer Support" logs.
- **Add custom instructions**: Use the custom instructions parameter to guide {{esql}} query generation with domain-specific requirements, such as always including certain fields, applying specific filters, or handling time ranges in a particular way
- **Set appropriate row limits**: Configure row limits to prevent retrieving excessive data that could exceed context length limits

For general guidance on naming tools and writing effective descriptions, refer to [Custom tools best practices](custom-tools.md#best-practices).

:::{tip}
Creating scoped, domain-specific tools also helps prevent [context length issues](../troubleshooting/context-length-exceeded.md) by reducing the volume of data the agent needs to process.
:::


## Common patterns

The following examples show typical index patterns and domain-specific tool configurations.

### Index pattern syntax

* **Wildcard patterns**: `logs-*`, `metrics-*`, `events-*`
* **Specific indices**: `products`, `users`, `orders`

Instead of creating a single generic search tool, consider creating multiple focused tools that target specific data domains. This gives the agent a smaller, higher-quality list of potential data sources, reducing the chance of retrieving irrelevant data.

:::{dropdown} Support logs tool example
**Tool name**: `Search Support Logs`

**Pattern**: `logs-support-*`

**Description**: "Search through server and application logs for error traces, stack traces, and diagnostic information. Use this when troubleshooting technical support tickets or investigating system issues."
:::

:::{dropdown} Finance invoices tool example
**Tool name**: `Search Invoices`

**Pattern**: `finance-invoices-*`

**Description**: "Search through settled and pending invoices. Use this to retrieve payment status, billing addresses, or invoice details for accounting queries."
:::

:::{dropdown} Security alerts tool example
**Tool name**: `Search Security Alerts`

**Pattern**: `security-alerts-*`

**Description**: "Search security detection alerts and findings. Use this for questions about threat detection, suspicious activity, or security incidents."
:::

$$$wildcard-warning$$$
:::{warning}
Avoid overly broad patterns like `*` or `logs-*` across large datasets. Broad wildcards can cause the agent to retrieve more data than the LLM can process, resulting in slow responses or errors. Refer to [Context length exceeded](../troubleshooting/context-length-exceeded.md) for tips on diagnosing and resolving these issues.
:::
