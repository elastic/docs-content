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

Broad questions or data spread across many indices can also cause slow responses or incomplete answers, even before hitting the context limit.

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

## Causes

These symptoms share a root cause: the agent is retrieving more data than it can efficiently process.

* **Broad queries with built-in agents**: [Built-in agents](../builtin-agents-reference.md) search across many indices and fields. If you ask a vague question, the agent may pull back more data than the context window can handle.
* **Index search tools with large indices**: [Index search tools](../tools/index-search-tools.md) allow the LLM to decide what to retrieve. If your indices contain large documents, many fields, or high document counts, these tools can return more data than the context window can handle.
* **Aggregation-style questions**: Questions like "summarize all errors from last week" or "compare metrics across all services" force the agent to retrieve data from many documents at once.
* **Long conversations**: Each message adds to the context. A long back-and-forth conversation can exhaust the [token budget](../monitor-usage.md) even if individual tool responses are small.

## Diagnosis

To identify which factor is contributing to the issue:

1. **Check which tools your agent uses.** Built-in agents and index search tools can return large responses for broad queries.
2. **Review the indices your agent queries.** Large documents, many fields, or high document counts increase the risk of exceeding context limits with index search tools.
3. **Consider your prompt patterns.** Broad or aggregation-style questions require more data retrieval.
4. **Check conversation length.** Long conversations accumulate context from previous messages. You can [view token usage](../monitor-usage.md) after each response to monitor consumption.

## Resolution

### Quick fixes

- **Write more targeted prompts**: Narrow your chat questions to reduce the scope of data retrieval. Specific questions return less data than exploratory questions.
- **Start a new conversation**: If you've been working in a long conversation, begin a fresh one. You can optionally provide a brief summary of relevant context from the previous conversation.
- **Switch to a model with a larger context window**: Some LLMs support larger context windows that can accommodate bigger tool responses. Refer to [](../models.md) for options.

### Use custom agents with custom tools

The most effective long-term solution is to create a custom agent with {{esql}} tools that return only the data you need.

::::::{stepper}

:::::{step} Create custom {{esql}} tools with targeted queries
[{{esql}} tools](../tools/esql-tools.md) give you precise control over what data is returned. Instead of letting the agent dynamically decide what to retrieve, you define exactly which fields to return and how many results to include.

For example, try creating purpose-built tools that:

- Return only identifier fields (like IDs and names) for initial searches
- Retrieve full details only for specific records
- Filter or aggregate data before returning results

Always include a `LIMIT` clause in your {{esql}} queries to cap the number of results.

:::{tip}
Learn more in [creating custom tools](../tools.md#create-custom-tools).
:::
:::::

:::::{step} Create a custom agent
Create a new agent to use your custom tools. Refer to [Agents in {{agent-builder}}](../agent-builder-agents.md) for instructions.
:::::

:::::{step} Assign tools and refine instructions
Assign your custom {{esql}} tools to the custom agent. Update the agent's system prompt to guide how it uses the tools.
:::::

::::::