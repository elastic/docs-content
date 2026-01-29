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

Prompt engineering in {{agent-builder}} involves three key areas:

* **Custom instructions**: When you [create a custom agent](custom-agents.md), you define instructions that shape the agent's persona, reasoning patterns, and guardrails.
* **Tool descriptions**: When you [define custom tools](tools/custom-tools.md), you write descriptions that help the agent understand when and how to use each tool.
* **Chat prompts**: How you phrase your questions when [chatting with agents](chat.md) affects the quality and accuracy of responses.

This guide outlines best practices for all three to help you build reliable, cost-effective agents.

:::{tip}
To learn about best practices specifically for your custom tool definitions, refer to [](tools/custom-tools.md#best-practices).
:::

## How agents process prompts

When you chat with an agent, your message is combined with the agent's system-level instructions before being sent to the LLM. [Built-in agents](builtin-agents-reference.md) have preconfigured instructions optimized for their use case. [Custom agents](custom-agents.md) combine your custom instructions with {{agent-builder}}'s base system prompt, which enables core features like visualization and citations.

This means your chat prompts work together with the agent's instructions. A well-designed custom agent with clear instructions requires less detailed chat prompts, while a general-purpose built-in agent may need more specific prompts to achieve the same results.

:::{tip}
To understand the baseline reasoning patterns of your agent, refer to the official prompt engineering guides provided by LLM vendors. Understanding the "system prompt" philosophy of the underlying model helps you write instructions and chat prompts that complement, rather than contradict, the model's native behavior.
:::

## Prompting guidelines

The prompt serves as the agent's operating manual. Follow these guidelines to minimize hallucinations and maximize tool accuracy.

### Start light and iterate

Avoid "over-prompting" with excessive text. High-reasoning models are capable of inferring intent from concise, well-structured instructions.

* **Begin with clarity**: Use unambiguous instructions specific to your primary tasks. Only add granular, step-by-step logic if the model fails a specific use case during testing.
* **Consult provider guides**: If your agent relies on a specific [model](models.md) family (for example Anthropic Claude or OpenAI GPT), use their specific architecture optimizations. For example, certain models are sensitive to specific keywords when extended thinking features are enabled.
* **Benchmark changes**: Treat prompts like code. Version your prompts and measure performance against a "golden dataset"—a collection of verified query-and-response pairs. Avoid modifying prompts based on a single failure; ensure changes improve aggregate performance.

### Structure and scope

Avoid prompts that attempt to handle multiple unrelated tasks. If a prompt becomes difficult to manage or the agent fails to follow sequences, consider adjusting your architecture.

#### Choose the right tool: Agents or Workflows

Not every task benefits from prompt engineering. Some tasks are better suited to deterministic [workflows](/explore-analyze/workflows.md) than to agent-based reasoning. Consider the following when deciding:

| Task requirement | Recommended approach |
| :--- | :--- |
| **High accuracy & sequential steps** | **Workflow**: Use a Workflow for logic that must be executed in a specific order (for example Step 1 must complete before Step 2). Hard-coded logic is more reliable than probabilistic reasoning. |
| **Independent, complex tasks** | **Specialized agents**: Break tasks into sub-agents to keep the context window focused and reduce tool-selection errors. |
| **Open-ended discovery** | **Agent**: Use a standard agent when the path to a solution requires dynamic reasoning or varied data exploration. |

:::{tip}
You can trigger workflows directly from agent conversations using [workflow tools](tools/workflow-tools.md).
:::

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

In the context window, custom instructions appear before tool definitions. To maximize prompt caching and reduce latency and [costs](monitor-usage.md):

* **Maintain static instructions**: Keep the instruction block consistent across sessions.
* **Avoid dynamic variables**: Do not insert volatile data (such as millisecond timestamps or session IDs) directly into the main instruction block. This forces the LLM to re-process the entire prompt, including the tool definitions, on every turn.

## Define behavior and tone

Use custom instructions to define how the agent communicates and handles uncertainty. A clear persona helps the agent make consistent decisions when faced with ambiguous situations.

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

Agents encounter incomplete data, failed tool calls, and ambiguous requests. Explicit instructions for these scenarios prevent the agent from guessing or hallucinating responses.

### Anticipate edge cases

Instruct the agent on how to handle missing information to prevent "hallucinated" values.

* **Example instruction**: "If the user does not provide a date range, default to the 'last 30 days' and explicitly inform the user of this assumption."

### Tool failure recovery

Teach the agent to be resilient. If a tool returns an error or an empty response, provide a specific recovery path:

* **Example instruction**: "If the `customer_search` tool returns no results, do not state that the customer does not exist. Instead, ask the user to provide an alternative identifier like an email address or phone number."


## Related pages

* [Custom agents](custom-agents.md)
* [Custom tools](tools/custom-tools.md)
* [Best practices for tool definitions](tools/custom-tools.md#best-practices)
* [Agent Chat](chat.md)

