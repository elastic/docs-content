---
navigation_title: "Context length exceeded"
description: "Learn how to diagnose and resolve context length exceeded errors in Agent Builder conversations."
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless:
    elasticsearch: ga
    observability: preview
    security: preview
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Context length exceeded in {{agent-builder}} conversations

A "context length exceeded" error occurs when a conversation exceeds the maximum context length supported by the LLM. It typically happens when tool responses return large amounts of data that consume the available token budget.

Broad questions or data spread across many indices can also cause slow responses or incomplete answers, even before hitting the context limit. These symptoms share a root cause: the agent is retrieving more data than it can efficiently process.

## Symptoms

In the UI, you may see messages such as:

* _This conversation exceeded the maximum context length. This typically occurs when tools return a very large response. Try again with a different request or start a new conversation._
* _Something in the query caused the model to freeze mid-thought. Performance debugging can be broad - try narrowing your question._

The API returns an error with `errCode: context_length_exceeded`:

```json
{
  "error": {
    "code": "agentExecutionError",
    "message": "The request exceeded the model's maximum context length...",
    "meta": {
      "errCode": "context_length_exceeded"
    }
  }
}
```

You may also experience:

* Slow agent responses
* Incomplete or failed answers to broad questions
* Agent timing out during data retrieval

## Diagnosis

Identify what's consuming context:

* **Built-in agents**: [Built-in agents](../builtin-agents-reference.md) use broad index search patterns that can match many indices and fields. This is useful for exploration but can retrieve large amounts of data for broad queries.
* **Index search tools**: [Index search tools](../tools/index-search-tools.md) dynamically determine what to retrieve based on natural language queries. They search all text and semantic_text fields by default, which can return substantial data when queries are broad or indices contain large documents.
* **Large documents or high document count**: Indices with large documents, many fields, or a high number of records are more likely to exceed context limits when broad prompts match multiple results.
* **Aggregation-style questions**: Questions that require synthesizing information across many documents (such as comparisons, summaries, or ranges across a dataset) force the agent to retrieve and process large amounts of data.
* **Long conversations**: Each message in a conversation adds to the context. Long conversations can exhaust the [token budget](../monitor-usage.md) even with modest tool responses.

## Resolution

### Use ES|QL tools instead of index search tools

[ES|QL tools](../tools/esql-tools.md) give you precise control over what data is returned. Instead of letting the agent dynamically decide what to retrieve, you define exactly which fields to return and how many results to include.

Consider creating purpose-built tools that:

- Return only identifier fields (like IDs and names) for initial searches
- Retrieve full details only for specific records
- Filter or aggregate data before returning results

This pattern keeps initial responses small and lets the agent fetch more data only when needed. Always include a `LIMIT` clause in your ES|QL queries to cap the number of results.

For more on creating custom tools, refer to [Tools in {{agent-builder}}](../tools.md).

### Write more targeted prompts

Narrow your chat questions to reduce the scope of data retrieval. Specific questions could return less data than exploratory questions.

### Use a model with a larger context window

Some LLMs support larger context windows that can accommodate bigger tool responses. Consider switching to a model like Gemini or GPT-4.1 if you frequently work with large datasets.

### Refine agent instructions

Update your agent's system prompt to guide the agent toward more efficient behavior. For example, instruct the agent to:

- Search for identifiers first, then retrieve full details only for relevant matches
- Ask clarifying questions when a query is ambiguous or could match a large dataset

### Start a new conversation

If you've been working in a long conversation, begin a fresh one. You can optionally provide a brief summary of relevant context from the previous conversation.
