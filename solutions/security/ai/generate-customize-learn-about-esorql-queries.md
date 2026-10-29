---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/esql-queries-assistant.html
  - https://www.elastic.co/guide/en/serverless/current/security-ai-assistant-esql-queries.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Generate, customize, and learn about ES|QL queries

[{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) can help you learn about and use the Elasticsearch Query Language ({{esql}}) to accomplish goals across {{elastic-sec}}.

If you use AI Assistant, refer to [Use AI Assistant (deprecated)](#esql-queries-ai-assistant).

## Use {{agent-builder}} for {{esql}} [esql-queries-agent-builder]

```{applies_to}
stack: ga 9.4+
serverless:
  security: ga
```

Chat with the [Elastic AI Agent](/explore-analyze/ai-features/agent-builder/builtin-agents-reference.md#elastic-ai-agent) to:

* **Learn {{esql}}**: Ask for examples, explanations of complex queries, and best practices.
* **Write new queries**: Describe what you want to find, and the agent generates a matching query. For example: "Write a query to identify documents with `curl.exe` usage and calculate the sum of `destination.bytes`" or "What query would return all user logins to [a host] in the last six hours?"
* **Run queries against your data**: The agent can run the queries it writes and summarize the results, so you can iterate without leaving the conversation.
* **Optimize existing queries**: Paste a query and ask for improvements, refactoring, a general assessment, or better performance with large data sets.
* **Customize queries for your environment**: Ask the agent to adapt a query to your indices and field names.
* **Troubleshoot**: Ask the agent to explain errors or unexpected results.

For hypothesis-driven hunts that run iterative {{esql}} queries, use the `threat-hunting` skill. Refer to [Threat hunting](/solutions/security/ai/agent-builder/skills-use-cases.md#threat-hunting).

## Use AI Assistant (deprecated) [esql-queries-ai-assistant]

```{applies_to}
stack: ga 9.0-9.5, deprecated 9.6+
serverless:
  security: deprecated
```

::::{include} /solutions/_snippets/security-ai-assistant-deprecated.md
::::

Elastic AI Assistant can help you learn about and leverage the Elasticsearch Query Language ({{esql}}) in many ways, including:

* **Education and training**: AI Assistant can serve as a powerful {{esql}} learning tool. Ask it for examples, explanations of complex queries, and best practices.
* **Writing new queries**: Prompt AI Assistant to provide a query that accomplishes a particular task, and it will generate a query matching your description. For example: "Write a query to identify documents with `curl.exe` usage and calculate the sum of `destination.bytes`" or "What query would return all user logins to [a host] in the last six hours?"
* **Providing feedback to optimize existing queries**: Send AI Assistant a query you want to work on and ask it for improvements, refactoring, a general assessment, or to optimize the query’s performance with large data sets.
* **Customizing queries for your environment**: Since each environment is unique, you may need to customize queries that you used in other contexts. AI Assistant can suggest necessary modifications based on contextual information you provide.
* **Troubleshooting**: Having trouble with a query or getting unexpected results? Ask AI Assistant to help you troubleshoot.

In these ways and others, AI Assistant can enable you to make use of {{esql}}'s advanced search capabilities to accomplish goals across {{elastic-sec}}.
