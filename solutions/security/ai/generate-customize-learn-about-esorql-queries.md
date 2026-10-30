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

[{{agent-builder}}](/solutions/security/ai/agent-builder/agent-builder.md) and the AI Assistant can help you learn about and use the Elasticsearch Query Language ({{esql}}) to accomplish goals across {{elastic-sec}}.

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
