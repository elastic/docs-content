---
navigation_title: "Prompting best practices"
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

# Best practices for prompt engineering in {{agent-builder}}

Effective AI agents succeed when they use the right tools at the right time. An agent’s ability to reason over user intent, discover relevant data sources, and execute precise tool sequences is determined by how its prompts and tool definitions are structured.

This guide outlines core principles for crafting prompts that enable reliable, cost-effective, and efficient agents within {{agent-builder}}.

:::{tip}
To learn about best practices for your custom tool definitions, refer to [](tools/custom-tools.md#best-practices).
:::

## How prompts interact with preconfigured agents

When building agents with {{agent-builder}}, your custom instructions do not exist in a vacuum. General-purpose agents (like the Elastic AI Agent) and domain-specific agents (such as Observability or Threat Hunting agents) include preconfigured system-level instructions.

Your custom prompt layers on top of these foundational instructions to:
* **Refine behavior**: Narrow the agent's focus to a specific business unit or dataset.
* **Add task-specific logic**: Introduce rules or multi-step reasoning patterns not present in the global prompt.
* **Clarify operations**: Define how the agent should interpret unique organizational data.

:::{tip}
To understand the baseline reasoning patterns of your agent, refer to the official prompt engineering guides provided by LLM vendors. Understanding the "system prompt" philosophy of the underlying model helps you write custom instructions that complement, rather than contradict, the model's native behavior.
:::

## Prompting guidelines

The prompt serves as the agent's operating manual. Follow these guidelines to minimize hallucinations and maximize tool accuracy.

### Start light and iterate

Avoid "over-prompting" with excessive text. High-reasoning models are capable of inferring intent from concise, well-structured instructions.

* **Begin with clarity**: Use unambiguous instructions specific to your primary tasks. Only add granular, step-by-step logic if the model fails a specific use case during testing.
* **Consult provider guides**: If your agent relies on a specific model family (for example Anthropic Claude or OpenAI GPT), use their specific architecture optimizations. For example, certain models are sensitive to specific keywords when extended thinking features are enabled.
* **Benchmark changes**: Treat prompts like code. Version your prompts and measure performance against a "golden dataset"—a collection of verified query-and-response pairs. Avoid modifying prompts based on a single failure; ensure changes improve aggregate performance.

### Structure and scope

Avoid prompts that attempt to handle multiple unrelated tasks. If a prompt becomes difficult to manage or the agent fails to follow sequences, consider adjusting your architecture.

#### Choose the right tool: Agent vs. Workflow

| Task requirement | Recommended approach |
| :--- | :--- |
| **High accuracy & sequential steps** | **Workflow**: Use a Workflow for logic that must be executed in a specific order (for example Step 1 must complete before Step 2). Hard-coded logic is more reliable than probabilistic reasoning. |
| **Independent, complex tasks** | **Specialized Agents**: Break tasks into sub-agents to keep the context window focused and reduce tool-selection errors. |
| **Open-ended discovery** | **Agent**: Use a standard agent when the path to a solution requires dynamic reasoning or varied data exploration. |

#### Use structured formatting

Large blocks of text can lead to instruction drift. Use Markdown headers and whitespace to separate instructions into logical blocks:

```markdown
# Goal
Define the high-level objective.

# Steps
Outline the preferred sequence of reasoning.

# Guardrails
List constraints, safety rules, and prohibited actions.
```

#### Optimize for prompt caching

In the context window, custom instructions appear before tool definitions. To maximize prompt caching and reduce latency and costs:

* **Maintain static instructions**: Keep the instruction block consistent across sessions.
* **Avoid dynamic variables**: Do not insert volatile data (such as millisecond timestamps or session IDs) directly into the main instruction block. This forces the LLM to re-process the entire prompt, including the tool definitions, on every turn.

## Define behavior and tone

### Set an operational persona

Explicitly define the agent's risk tolerance and interaction style based on your use case:

* **Precautionary (Finance/Security)**: "You are a precautionary agent. You must verify tool output before summarizing. If data is ambiguous, ask clarifying questions. Do not assume default values."
* **Explorative (Research/Search)**: "You are an autonomous researcher. If a search yields few results, broaden your query terms and attempt a new search without prompting the user for permission."

### Normalize inputs and outputs

Define formatting rules to ensure consistency between the LLM, the tools, and the user interface:

* **Date formats**: "Always format dates as `YYYY-MM-DD`."
* **Financial values**: "Input monetary values as integers in cents for tool calls, but display them as `$XX.XX` in user responses."
* **Domain context**: Define organizational acronyms or naming conventions. (Example: "In this context, 'AOV' refers to Average Order Value.")

## Error handling and guardrails

### Anticipate edge cases

Instruct the agent on how to handle missing information to prevent "hallucinated" values.

* **Example instruction**: "If the user does not provide a date range, default to the 'last 30 days' and explicitly inform the user of this assumption."

### Tool failure recovery

Teach the agent to be resilient. If a tool returns an error or an empty response, provide a specific recovery path:

* **Example instruction**: "If the `customer_search` tool returns no results, do not state that the customer does not exist. Instead, ask the user to provide an alternative identifier like an email address or phone number."


## Related pages

* [Best practices for tool definitions](tools/custom-tools.md#best-practices)
* [Custom tools](tools/custom-tools.md)
* [Workflow tools](tools/workflow-tools.md)
* [Built-in tools reference](tools/builtin-tools-reference.md)

