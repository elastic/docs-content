---
navigation_title: "Glossary"
description: "Defines the key terms used throughout the Elastic Agent Builder documentation."
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

# {{agent-builder}} glossary

This glossary defines the terms used throughout the {{agent-builder}} documentation. Definitions describe how each term is used in {{agent-builder}}. Some terms also exist outside this feature with broader meanings.

Entries are listed alphabetically. Where a term applies to a specific deployment, project type, or product version, an `applies_to` badge is placed next to it. Terms without a badge follow the page-level applicability.

:::{tip}
For the full list of pre-configured agents, skills, and tools available out of the box, refer to the [built-in agents](builtin-agents-reference.md), [built-in skills](builtin-skills-reference.md), and [built-in tools](tools/builtin-tools-reference.md) reference pages.
:::

## A

A2A protocol
:   The [Agent2Agent (A2A) Protocol](https://a2a-protocol.org/latest/specification/) specification for communication between AI agents. {{agent-builder}} implements A2A so that external clients and other agent frameworks can interact with agents in a standardized way. See [A2A server](a2a-server.md).

A2A server
:   The {{agent-builder}} endpoint that exposes agents to external A2A clients. Use it to integrate {{agent-builder}} agents with third-party agent frameworks. See [A2A server](a2a-server.md).

Agent
:   A capability that iteratively uses a large language model (LLM), system context, and a set of tools and skills to complete a task. Each agent translates a user's natural language request into a sequence of tool calls and reasoning steps to answer questions, take actions, or support workflows. {{agent-builder}} ships with built-in agents and lets you create custom agents. See [Agents](agent-builder-agents.md).

{{agent-builder}}
:   Elastic's platform for creating and optimizing context for AI agents that analyze and act over your enterprise data. {{agent-builder}} combines LLM reasoning with skills, tools, and best practices for context engineering and retrieval, so responses are accurately and efficiently grounded in your data. See [{{agent-builder}}](../elastic-agent-builder.md).

{{agent-builder}} APIs
:   The REST API surface for working with {{agent-builder}} programmatically: endpoints for agents, tools, skills, conversations, and token consumption. {{agent-builder}} APIs are a group within the {{kib}} HTTP API, served under `/api/agent_builder/`. See [{{agent-builder}} Kibana APIs overview](kibana-api.md) and the [API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-agent-builder).

Agent Builder execution {applies_to}`stack: ga 9.4+`
:   The metering unit used to bill {{agent-builder}} usage. Each completed agent interaction is metered as one or more executions based on input token consumption; interactions that fail to return a response aren't metered. See [](monitor-usage.md).

Agent Chat
:   The synchronous chat interface for interacting with agents using natural language. Agent Chat is available in standalone mode and sidebar mode, and can also be driven programmatically through the {{agent-builder}} APIs. See [Agent Chat](chat.md).

Agent selector
:   The dropdown in Agent Chat used to switch between agents, open the agent management view, or create a new agent. See [Agent Chat](chat.md).

`agentBuilder` feature
:   The {{kib}} feature privilege that controls access to {{agent-builder}}. Assign `Read` or `All` to roles. For finer-grained control, pair `Read` with sub-feature privileges such as `Manage agents` and `Manage tools`. See [Permissions and access control](permissions.md).

`ai.agent` step {applies_to}`stack: preview 9.3+`
:   A workflow step type that invokes an {{agent-builder}} agent as a reasoning engine within a workflow. Use it to summarize data, classify events, or make decisions in the middle of an automation. See [Agents and workflows](agents-and-workflows.md).

AI Agent button {applies_to}`stack: preview =9.3, ga 9.4+`
:   The button in the {{kib}} top header that opens sidebar mode so you can chat with an agent from any page. See [Chat UI modes](standalone-and-flyout-modes.md).

API key
:   A credential used for programmatic access to {{agent-builder}} APIs, including the MCP server and A2A server endpoints. The API key inherits the privileges of the user who created it. See [Permissions and access control](permissions.md).

Attachment
:   Data or context added to a chat message, such as an alert flyout, a {{kib}} object, or a file. Attachments can trigger an agent to invoke the skill most relevant to the attachment type. See [Agent Chat](chat.md).

## B

Built-in agent
:   An agent pre-configured by Elastic with default instructions and tools for common use cases. See [Built-in agents reference](builtin-agents-reference.md).

Built-in skill {applies_to}`stack: ga 9.4+`
:   A read-only skill shipped with {{agent-builder}}. Built-in skills span platform, {{product.observability}}, {{product.security}}, and {{es}} domains. See [Built-in skills reference](builtin-skills-reference.md).

Built-in tool
:   A read-only tool shipped with {{agent-builder}}, providing core capabilities such as searching {{es}}, executing {{esql}} queries, retrieving documents, and listing indices. Built-in tools cover platform, {{product.observability}}, and {{product.security}} domains. See [Built-in tools reference](tools/builtin-tools-reference.md).

## C

Chat history
:   See **Conversation history**.

Connector
:   A {{kib}} integration that enables {{agent-builder}} to communicate with an external service. See [Connectors](connectors.md).

Context window
:   The maximum amount of text, measured in tokens, that an LLM can process in a single interaction. When a conversation, tool response, or system prompt grows too large, the agent can encounter a context length exceeded error. See [Token usage in {{agent-builder}}](monitor-usage.md).

Context length exceeded
:   An error returned when a conversation has consumed more tokens than the LLM's context window allows, typically because tool responses or chat history have grown very large. See [Context length exceeded](troubleshooting/context-length-exceeded.md).

Conversation
:   A single exchange or thread between a user and an agent in Agent Chat. Conversations preserve message history, agent identity, and any attachments used. See [Agent Chat](chat.md).

Conversation history
:   The persisted record of previous conversations between a user and the agents they've used. Shown in the chat history panel and shared across standalone mode and sidebar mode. See [Agent Chat](chat.md).

Custom agent
:   An agent you create with your own system prompt, tools, skills, and visibility settings. Custom agents are space-aware and exist only in the {{kib}} space where they were created. See [Custom agents](custom-agents.md).

Custom instructions
:   Free-form Markdown that you add to an agent's system prompt to define its persona, scope, tone, or workflow constraints. Custom instructions are always loaded into the context window. See [Custom agents](custom-agents.md).

Custom skill {applies_to}`stack: ga 9.4+`
:   A reusable instruction set you author yourself, bundling domain-specific guidance, tools, and reference content. Custom skills are saved in the skill library and can be assigned to any custom agent. See [Custom skills](custom-skills.md).

Custom tool
:   A user-defined tool that extends the built-in catalog. Custom tools can be one of four types: {{esql}} tool, index search tool, MCP tool, or workflow tool. See [Custom tools](tools/custom-tools.md).

Customize accordion {applies_to}`stack: ga 9.4+`
:   The expandable section in the standalone-mode left sidebar that groups the agent-scoped configuration pages: Overview, Skills, Plugins, and Tools. See [Chat UI modes](standalone-and-flyout-modes.md).

## D

Default agent {applies_to}`stack: ga 9.4+`
:   The Elastic AI Agent, which is automatically created in each {{kib}} space and acts as the starting agent for new conversations. See [Built-in agents reference](builtin-agents-reference.md).

Default model {applies_to}`stack: ga 9.4+`
:   The LLM that {{agent-builder}} uses for any agent that doesn't explicitly select a different one. Configure it from **GenAI Settings**. See [Models](models.md).

## E

Elastic AI Agent
:   The general-purpose default agent shipped with {{agent-builder}}. The Elastic AI Agent is a read-only built-in agent {applies_to}`stack: preview =9.2, ga =9.3` and a space-aware, persisted agent that you can customize directly {applies_to}`stack: ga 9.4+`. See [Built-in agents reference](builtin-agents-reference.md).

Elastic Inference Service (EIS) {applies_to}`stack: ga 9.4+`
:   Elastic's managed service for running LLMs on Elastic infrastructure, used by Elastic Managed LLMs. See [Models](models.md).

Elastic Managed LLM {applies_to}`stack: ga 9.4+`
:   A pre-configured LLM provided by Elastic and powered by the Elastic Inference Service. On {{ech}} and {{serverless-full}}, an Elastic Managed LLM is available out of the box, so {{agent-builder}} works with no additional connector setup. See [Models](models.md).

Enable Elastic Capabilities {applies_to}`stack: ga 9.4+`
:   The toggle on a custom agent's **Settings** tab that opts the agent in to all current and future Elastic-built skills, plugins, and tools. The toggle is off by default. See [Custom agents](custom-agents.md).

Entity store
:   The {{product.security}} store of security entities (hosts, users, services). {{agent-builder}} security tools and skills can query the entity store to support investigations. See [Built-in skills reference](builtin-skills-reference.md).

{{esql}} tool
:   A type of custom tool that runs a parameterized {{esql}} query directly against {{es}}. Use {{esql}} tools when you want precise, repeatable retrieval logic that an agent can invoke by name. See [{{esql}} tools](tools/esql-tools.md).

## F

% TODO: Link to the `filestore.read` tool reference once it's added to tools/builtin-tools-reference.md.
File store {applies_to}`stack: ga 9.4+`
:   An in-memory store for skills and intermediate retrieval results. The file store lets agents offload content from the LLM context window and load information dynamically as needed. Agents access the file store using the `filestore.read` tool.

Flyout mode
:   Earlier name for sidebar mode. The two terms refer to the same chat panel; **sidebar mode** is the current name used in the documentation. See [Chat UI modes](standalone-and-flyout-modes.md).

## G

GenAI connector
:   A {{kib}} connector for an LLM provider (for example, OpenAI, Anthropic, Google Gemini, Azure OpenAI, Bedrock, or a self-hosted model). {{agent-builder}} uses GenAI connectors to call models that aren't part of the Elastic Inference Service. See [Models](models.md).

GenAI Settings {applies_to}`stack: ga 9.4+`
:   The {{kib}} settings page where you configure the default model and other generative-AI options that affect {{agent-builder}}. See [Models](models.md).

## I

Index search tool
:   A type of custom tool that performs natural-language search over a configured set of indices, aliases, or data streams. The tool selects an appropriate query strategy (keyword, semantic, or hybrid) automatically. See [Index search tools](tools/index-search-tools.md).

Inline tool
:   A tool that's available only in a specific context. For example, while a particular built-in skill is active or while an attachment is present in the conversation. Inline tools don't appear in the global tools list. See [Built-in tools reference](tools/builtin-tools-reference.md).

Input tokens
:   The tokens sent to the LLM in a request, including the user's message, the system prompt, accumulated conversation history, and tool responses. See [Monitor token usage](monitor-usage.md).

## K

`kibana.request` step {applies_to}`stack: preview 9.3+`
:   A generic Workflows step. When `ai.agent` doesn't cover a scenario, you can use `kibana.request` to call {{agent-builder}} APIs from a workflow. See [Kibana action steps](/explore-analyze/workflows/steps/kibana.md).

## M

Manage components {applies_to}`stack: ga 9.4+`
:   The link at the bottom of the standalone-mode left sidebar that opens the deployment-wide view of all agents, skills, plugins, connectors, and tools. See [Chat UI modes](standalone-and-flyout-modes.md).

MCP
:   The [Model Context Protocol](https://modelcontextprotocol.io/), an open standard for connecting AI assistants to external tools and data sources. {{agent-builder}} both _exposes_ tools through an MCP server and _consumes_ tools from remote MCP servers as MCP tools. See [MCP server](mcp-server.md).

MCP connector {applies_to}`stack: preview 9.3+`
:   A {{kib}} connector that points {{agent-builder}} at a remote MCP server so its tools can be imported as MCP tools. See [Connectors](connectors.md).

MCP server
:   An endpoint that implements the Model Context Protocol. {{agent-builder}} both _exposes_ its own MCP server, making Elastic tools and agents available to external MCP clients such as Claude Desktop, Cursor, VS Code, or LangChain apps, and _consumes_ remote MCP servers through MCP connectors. See [MCP server](mcp-server.md).

MCP tool {applies_to}`stack: preview 9.3+`
:   A type of custom tool that proxies a tool exposed by a remote MCP server. Use MCP tools to give your agents access to capabilities provided by external services. See [MCP tools](tools/mcp-tools.md).

Model
:   The LLM that an agent uses to reason and produce responses. Models are accessed through Elastic Managed LLMs or through GenAI connectors. See [Models](models.md).

Model selector
:   The dropdown in Agent Chat used to switch the LLM that the current agent calls. See [Models](models.md).

`monitor_inference`
:   The {{es}} cluster privilege required when an agent uses an AI connector that calls the {{es}} Inference API. Built-in tools such as `search` and `generate_esql`, and all index search tools, depend on this privilege. See [Permissions and access control](permissions.md).

## O

Output tokens
:   The tokens generated by the LLM in a response, including the final answer shown to the user as well as any internal reasoning steps and tool-call payloads. See [Monitor token usage](monitor-usage.md).

## P

Plugin {applies_to}`stack: ga 9.4+`
:   A reusable bundle of skills and supporting capabilities that can be assigned to an agent as a single unit. Plugins make it easier to share groups of related skills across agents. See [Plugins](plugins.md).

Prompt engineering
:   The practice of writing instructions, examples, and constraints that steer LLM behavior. {{agent-builder}} provides guidance for shaping agent system prompts, custom instructions, and skill instructions. See [Prompt engineering](prompt-engineering.md).

## R

Reasoning
:   The iterative process an agent follows to answer a request: analyzing the input, choosing tools, executing them, and incorporating results into a response. Each iteration is a _reasoning step_. See [Agents](agent-builder-agents.md).

Reasoning panel
:   The expandable section of the chat reply that shows the underlying reasoning steps, tool calls, and tool responses behind an agent's answer. See [Agent Chat](chat.md).

REST API
:   See {{agent-builder}} APIs.

Retrieval-Augmented Generation (RAG)
:   An AI pattern that grounds LLM responses in retrieved data instead of relying solely on model weights. {{agent-builder}} agents use {{es}} as the retrieval layer, which makes the platform a natural fit for RAG applications. See [{{agent-builder}}](../elastic-agent-builder.md).

## S

Sidebar mode {applies_to}`stack: preview =9.3, ga 9.4+`
:   The chat experience that opens as a persistent panel beside the page you're on, so you can chat with an agent without leaving your current {{kib}} workflow. Open it from the AI Agent button or with `cmd+;` / `ctrl+;`. See [Chat UI modes](standalone-and-flyout-modes.md).

Skill {applies_to}`stack: ga 9.4+`
:   A reusable capability pack that gives an agent specialized expertise for a particular type of task. A skill bundles instructions, tools, and reference content, and loads selectively based on the user's request. Skills sit one level above tools: a tool performs an operation, a skill teaches the agent _how_ and _when_ to use it. See [Skills](skills.md).

Skill library {applies_to}`stack: ga 9.4+`
:   The deployment-wide collection of custom skills. Any custom agent can pull skills from the library. Built-in skills appear alongside them as read-only entries. See [Custom skills](custom-skills.md).

Slash command {applies_to}`stack: ga 9.4+`
:   The chat shortcut for explicitly invoking a skill. Type `/` followed by the skill name to bypass automatic skill selection. See [Skills](skills.md).

Solution view
:   A {{kib}} navigation mode oriented around a single solution ({{es}}, {{product.observability}}, or {{product.security}}). The solution view determines which {{agent-builder}} entry points and built-in capabilities are surfaced. See [Get started with {{agent-builder}}](get-started.md).

Space
:   A {{kib}} space. Custom agents and custom tools are _space-aware_ — they exist only in the space where they were created. The Elastic AI Agent is also space-aware. Built-in tools, and built-in agents other than the Elastic AI Agent, are space-agnostic. See [Permissions and access control](permissions.md).

Standalone mode
:   The full-page Agent Chat experience, opened from **Agents** in the main navigation. Standalone mode is recommended when you're working with dashboards, visualizations, or long agent replies. See [Chat UI modes](standalone-and-flyout-modes.md).

System prompt
:   The instructions that are always present in the context window. The system prompt defines an agent's core behavior. Custom instructions are layered on top of it. See [Prompt engineering](prompt-engineering.md).

## T

Token
:   The unit of text that an LLM processes. Token counts roughly correspond to fragments of words and determine how much of the context window a message consumes, as well as the cost of a request. See [Monitor token usage](monitor-usage.md).

Tool
:   A modular function an agent can call to search, retrieve, or manipulate {{es}} data. Tools are the primary mechanism for grounding agent capabilities in your data. {{agent-builder}} provides built-in tools; you can also create custom tools of four types: {{esql}}, index search, MCP, and workflow. See [Tools](tools.md).

## V

Visibility
:   A custom agent's sharing setting that controls who can see and edit it. Options are **Public** (anyone in the space), **Shared** (anyone can view; only owners and admins can edit), and **Private** (only owners and admins). See [Custom agents](custom-agents.md).

## W

Workflow tool {applies_to}`stack: preview 9.3+`
:   A type of custom tool that lets an agent trigger a [workflow](/explore-analyze/workflows.md) from a conversation and use its output. See [Workflow tools](tools/workflow-tools.md).

Workflows
:   Elastic's native automation engine for declarative, event-driven automation defined in YAML. {{agent-builder}} integrates with workflows in two directions: agents can trigger workflows through workflow tools, and workflows can call agents through the `ai.agent` and `kibana.request` steps. See [Agents and workflows](agents-and-workflows.md).
