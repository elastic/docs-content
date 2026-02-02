---
description: Learn how to write effective custom instructions and tool descriptions in Elastic Agent Builder to build reliable, cost-effective agents.
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

[Prompt engineering](https://en.wikipedia.org/wiki/Prompt_engineering) is the process of structuring or crafting an instruction in order to produce better outputs from a generative artificial intelligence (GenAI) model. 

Prompt engineering in {{agent-builder}} involves three key areas:

* **Custom instructions**: When you [create a custom agent](custom-agents.md), you define instructions that shape the agent's persona, reasoning patterns, and guardrails.
* **Tool descriptions**: When you [define custom tools](tools/custom-tools.md#writing-effective-tool-descriptions), you write descriptions that help the agent understand when and how to use each tool.
* **Chat prompts**: How you phrase your questions when [chatting with agents](chat.md) affects the quality and accuracy of responses.

This guide outlines best practices to help you build reliable, cost-effective agents.

:::{tip}
To learn about best practices for creating custom tools, refer to [](tools/custom-tools.md#best-practices).
:::

## How agents process prompts

When you chat with an agent, your message is combined with the agent's system-level instructions before being sent to the LLM. [Built-in agents](builtin-agents-reference.md) have preconfigured instructions optimized for their use case. [Custom agents](custom-agents.md) combine your custom instructions with {{agent-builder}}'s base system prompt, which enables core features like visualization and citations.

This means your chat prompts work together with the agent's instructions. A well-designed custom agent with clear instructions requires less detailed chat prompts, while a general-purpose built-in agent may need more specific prompts to achieve the same results.

:::{tip}
To understand the baseline reasoning patterns of your agent, refer to the official prompt engineering guides provided by LLM vendors. Understanding the "system prompt" philosophy of the underlying model helps you write instructions and chat prompts that complement, rather than contradict, the model's native behavior.
:::

## Agents or workflows

Not every task benefits from prompt engineering. Some tasks are better suited to deterministic [workflows](/explore-analyze/workflows.md) than to agent-based reasoning. Consider the following when deciding:

| Task requirement | Recommended approach |
| :--- | :--- |
| **High accuracy & sequential steps** | **Workflow**: Use a Workflow for logic that must be executed in a specific order (for example Step 1 must complete before Step 2). Hard-coded logic is more reliable than probabilistic reasoning. |
| **Independent, complex tasks** | **Specialized agents**: Break tasks into sub-agents to keep the context window focused and reduce tool-selection errors. |
| **Open-ended discovery** | **Agent**: Use a standard agent when the path to a solution requires dynamic reasoning or varied data exploration. |

:::{tip}
You can trigger workflows directly from agent conversations using [workflow tools](tools/workflow-tools.md).
:::

## Custom instructions, tool descriptions, or user input

When building agents, you must decide where specific logic belongs: in the agent's custom instructions, in a tool description, or derived dynamically from the user query. Use the following table to guide your decisions:

| Logic type | Source | Rationale |
| :--- | :--- | :--- |
| **Global behavior** | Custom instructions | Instructions like "Always answer in French" or "Be concise" apply to the entire session, regardless of which tools are used. |
| **Multi-step sequences** | Custom instructions | "First search for the user, then look up their recent orders." The agent needs to know the order of operations before selecting tools. |
| **Trigger criteria** | Tool description | "Use this tool ONLY for European market data." The LLM evaluates this when deciding which tool to call. |
| **API constraints** | Tool description | "The search parameter must be at least 3 characters." This prevents invalid API calls. |
| **Dynamic intent** | User input | "Find me the sales for Q3." The LLM extracts values from the user's message and passes them as tool parameters at runtime. |

:::{tip}
For detailed guidance on writing effective tool descriptions, refer to [](tools/custom-tools.md#best-practices).
:::

## Core principles

Apply these principles when writing custom instructions and tool descriptions to build agents that are efficient, effective, and easier to maintain.

### Start light and iterate

Avoid "over-prompting" with excessive text. High-reasoning models are capable of inferring intent from concise, well-structured instructions.

* **Begin with clarity**: Use unambiguous instructions specific to your primary tasks. Only add granular, step-by-step logic if the model fails a specific use case during testing.
* **Consult provider guides**: If you aren't switching [models](models.md) frequently, consult that provider's official prompt engineering guide (for example, [Anthropic's Claude best practices](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices)). These guides contain specific guidance to unlock maximum performance for that architecture. For example, certain models are sensitive to specific keywords: Claude Opus 4.5 is sensitive to the word "think" when extended thinking is disabled.
* **Benchmark changes**: Treat prompts like code. Version your prompts and measure performance against a "golden dataset": a collection of verified query-and-response pairs. Avoid modifying prompts based on a single failure; ensure changes improve aggregate performance.

### Use structured formatting

Large blocks of text can lead to instruction drift. Use Markdown headers and whitespace to separate instructions into logical blocks:

```markdown
# Goal
Define the high-level objective.

# Steps
Outline the preferred sequence of reasoning.

# Guardrails
List constraints, safety rules, and prohibited actions.
```

### Optimize for prompt caching

In the context window, custom instructions appear before tool definitions. To maximize prompt caching and reduce latency and [costs](monitor-usage.md):

* **Maintain static instructions**: Keep the instruction block consistent across sessions.
* **Avoid dynamic variables**: Do not insert volatile data (such as millisecond timestamps or session IDs) directly into the main instruction block. This forces the LLM to re-process the entire prompt, including the tool definitions, on every turn.

## Define behavior and tone

Use custom instructions to define how the agent communicates and handles uncertainty. A clear persona helps the agent make consistent decisions when faced with ambiguous situations.

### Set an operational persona

Explicitly define the agent's risk tolerance and interaction style based on your use case. For example:

* **Precautionary (Finance/Security)**: "You are a precautionary agent. You must verify tool output before summarizing. If data is ambiguous, ask clarifying questions. Do not assume default values."
* **Explorative (Research/Search)**: "You are an autonomous researcher. If a search yields few results, broaden your query terms and attempt a new search without prompting the user for permission."

### Normalize inputs and outputs

Define formatting rules to ensure consistency between the LLM, the tools, and the user interface. For example:

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

