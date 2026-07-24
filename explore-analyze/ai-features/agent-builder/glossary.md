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
For the full list of pre-configured agents, skills, and tools available out of the box, refer to the [](builtin-agents-reference.md), [](builtin-skills-reference.md), and [](tools/builtin-tools-reference.md) reference pages.
:::

## A

$$$a2a-protocol$$$
A2A protocol
:   The [Agent2Agent (A2A) Protocol](https://a2a-protocol.org/latest/specification/) specification for communication between AI agents. {{agent-builder}} implements A2A so that external clients and other agent frameworks can interact with agents in a standardized way. See [](a2a-server.md#execute-a2a-protocol-post).

$$$a2a-server$$$
A2A server
:   The {{agent-builder}} endpoint that exposes agents to external A2A clients. Use it to integrate {{agent-builder}} agents with third-party agent frameworks. See [](a2a-server.md).

$$$agent$$$
Agent
:   A capability that iteratively uses a large language model (LLM), system context, and a set of tools and skills to complete a task. Each agent translates a user's natural language request into a sequence of tool calls and reasoning steps to answer questions, take actions, or support workflows. {{agent-builder}} ships with built-in agents and lets you create custom agents. See [](agent-builder-agents.md#how-agents-work).

$$$agent-builder$$$
{{agent-builder}}
:   Elastic's platform for creating and optimizing context for AI agents that analyze and act over your enterprise data. {{agent-builder}} combines LLM reasoning with skills, tools, and best practices for context engineering and retrieval, so responses are accurately and efficiently grounded in your data. See [](../elastic-agent-builder.md).

$$$agent-builder-apis$$$
{{agent-builder}} APIs
:   The REST API surface for working with {{agent-builder}} programmatically: endpoints for agents, tools, skills, conversations, and token consumption. {{agent-builder}} APIs are a group within the {{kib}} HTTP API, served under `/api/agent_builder/`. See [](kibana-api.md#available-apis) and the [API reference](https://www.elastic.co/docs/api/doc/kibana/group/endpoint-agent-builder).

$$$agent-builder-execution$$$
Agent Builder execution
:   The metering unit used to bill {{agent-builder}} usage. Each completed agent interaction is metered as one or more executions based on input token consumption; interactions that fail to return a response aren't metered. See [](monitor-usage.md#execution-based-billing).

$$$agent-chat$$$
Agent Chat
:   The synchronous chat interface for interacting with agents using natural language. Agent Chat is available in standalone mode and sidebar mode, and can also be driven programmatically through the {{agent-builder}} APIs. See [](chat.md#agent-chat-gui).

$$$agent-selector$$$
Agent selector
:   The dropdown in Agent Chat used to switch between agents, open the agent management view, or create a new agent. See [](chat.md#start-a-chat-and-select-an-agent).

$$$agentbuilder-feature$$$
`agentBuilder` feature
:   The {{kib}} feature privilege that controls access to {{agent-builder}}. Assign `Read` or `All` to roles. For finer-grained control, pair `Read` with sub-feature privileges such as `Manage agents` and `Manage tools`. See [](permissions.md#kib-privileges).

$$$ai-agent-step$$$
`ai.agent` step {applies_to}`stack: preview 9.3+` {applies_to}`serverless: preview`
:   A workflow step type that invokes an {{agent-builder}} agent as a reasoning engine within a workflow. Use it to summarize data, classify events, or make decisions in the middle of an automation. See [](agents-and-workflows.md#use-ai-agent-workflow-step).

$$$ai-agent-button$$$
AI Agent button
:   The button in the {{kib}} top header that opens sidebar mode so you can chat with an agent from any page. See [](standalone-and-flyout-modes.md#sidebar-mode).

$$$api-key$$$
API key
:   A credential used for programmatic access to {{agent-builder}} APIs, including the MCP server and A2A server endpoints. The API key inherits the privileges of the user who created it. See [](permissions.md#grant-access-with-api-keys).

$$$attachment$$$
Attachment
:   Data or context added to a chat message, such as an alert flyout, a {{kib}} object, or a file. Attachments can trigger an agent to invoke the skill most relevant to the attachment type. See [](chat.md#agent-chat-gui).

## B

$$$built-in-agent$$$
Built-in agent
:   An agent pre-configured by Elastic with default instructions and tools for common use cases. See [](builtin-agents-reference.md#elastic-ai-agent).

$$$built-in-skill$$$
Built-in skill {applies_to}`stack: ga 9.4+`
:   A read-only skill shipped with {{agent-builder}}. Built-in skills span platform, {{product.observability}}, {{product.security}}, and {{es}} domains. See [](builtin-skills-reference.md).

$$$built-in-tool$$$
Built-in tool
:   A read-only tool shipped with {{agent-builder}}, providing core capabilities such as searching {{es}}, executing {{esql}} queries, retrieving documents, and listing indices. Built-in tools cover platform, {{product.observability}}, and {{product.security}} domains. See [](tools/builtin-tools-reference.md#platform-core-tools).

## C

$$$chat-history$$$
Chat history
:   See [](#conversation-history).

$$$connector$$$
Connector {applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview`
:   A {{kib}} integration that enables {{agent-builder}} to communicate with an external service. See [](connectors.md#how-agents-use-connectors).

$$$context-window$$$
Context window
:   The maximum amount of text, measured in tokens, that an LLM can process in a single interaction. When a conversation, tool response, or system prompt grows too large, the agent can encounter a context length exceeded error. See [](monitor-usage.md#token-usage).

$$$context-length-exceeded$$$
Context length exceeded
:   An error returned when a conversation has consumed more tokens than the LLM's context window allows, typically because tool responses or chat history have grown very large. See [](troubleshooting/context-length-exceeded.md).

$$$conversation$$$
Conversation
:   A single exchange or thread between a user and an agent in Agent Chat. Conversations preserve message history, agent identity, and any attachments used. See [](chat.md#agent-chat-gui).

$$$conversation-history$$$
Conversation history
:   The persisted record of previous conversations between a user and the agents they've used. Shown in the chat history panel and shared across standalone mode and sidebar mode. See [](chat.md#find-conversation-history).

$$$custom-agent$$$
Custom agent
:   An agent you create with your own system prompt, tools, skills, and visibility settings. Custom agents are space-aware and exist only in the {{kib}} space where they were created. See [](custom-agents.md#create-a-custom-agent).

$$$custom-instructions$$$
Custom instructions
:   Free-form Markdown that you add to an agent's system prompt to define its persona, scope, tone, or workflow constraints. Custom instructions are always loaded into the context window. See [](custom-agents.md#create-a-custom-agent).

$$$custom-skill$$$
Custom skill {applies_to}`stack: ga 9.4+`
:   A reusable instruction set you author yourself, bundling domain-specific guidance, tools, and reference content. Custom skills are saved in the skill library and can be assigned to any custom agent. See [](custom-skills.md#create-a-custom-skill).

$$$custom-tool$$$
Custom tool
:   A user-defined tool that extends the built-in catalog. Custom tools can be one of four types: {{esql}} tool, index search tool, MCP tool, or workflow tool. See [](tools/custom-tools.md#tool-types).

$$$customize-accordion$$$
Customize accordion {applies_to}`stack: ga 9.4+`
:   The expandable section in the standalone-mode left sidebar that groups the agent-scoped configuration pages: Overview, Skills, Plugins, and Tools. See [](standalone-and-flyout-modes.md#sidebar-mode).

## D

$$$default-agent$$$
Default agent {applies_to}`stack: ga 9.4+`
:   The Elastic AI Agent, which is automatically created in each {{kib}} space and acts as the starting agent for new conversations. See [](builtin-agents-reference.md#elastic-ai-agent).

$$$default-model$$$
Default model
:   The LLM that {{agent-builder}} uses for any agent that doesn't explicitly select a different one. See [](models.md#change-the-default-model).

## E

$$$elastic-ai-agent$$$
Elastic AI Agent
:   The general-purpose default agent shipped with {{agent-builder}}. See [](builtin-agents-reference.md#elastic-ai-agent).

$$$elastic-inference-service-eis$$$
Elastic Inference Service (EIS)
:   Elastic's managed service for running LLMs on Elastic infrastructure, used by Elastic Managed LLMs. See [](models.md#default-model-configuration).

$$$elastic-managed-llm$$$
Elastic Managed LLM
:   A pre-configured LLM provided by Elastic and powered by the Elastic Inference Service. On {{ech}} and {{serverless-full}}, an Elastic Managed LLM is available out of the box, so {{agent-builder}} works with no additional setup. See [](models.md#default-model-configuration).

$$$enable-elastic-capabilities$$$
Elastic capabilities {applies_to}`stack: ga 9.4+`
:   The toggle on an agent's **Settings** tab that opts the agent in to all current and future Elastic-built [tools](tools/builtin-tools-reference.md), [skills](builtin-skills-reference.md), and plugins. Enabled by default for built-in agents, disabled by default for custom agents. See [](agent-builder-agents.md#elastic-capabilities).

$$$entity-store$$$
Entity store
:   The {{product.security}} store of security entities (hosts, users, services). {{agent-builder}} security tools and skills can query the entity store to support investigations. See [](builtin-skills-reference.md#security-skills).

$$$esql-tool$$$
{{esql}} tool
:   A type of custom tool that runs a parameterized {{esql}} query directly against {{es}}. Use {{esql}} tools when you want precise, repeatable retrieval logic that an agent can invoke by name. See [](tools/esql-tools.md#when-to-use-esql-tools).

## F

$$$flyout-mode$$$
Flyout mode
:   Earlier name for sidebar mode. The two terms refer to the same chat panel; **sidebar mode** is the current name used in the documentation. See [](standalone-and-flyout-modes.md#sidebar-mode).

## G

$$$generative-ai-connector$$$
Generative AI connector
:   A {{kib}} connector that connects {{agent-builder}} to an LLM provider such as OpenAI, Anthropic, Amazon Bedrock, Google Gemini, or Azure OpenAI. Distinct from a [](#connector), which connects {{agent-builder}} to non-LLM external services. See [](models.md#configure-a-connector).

$$$genai-settings$$$
GenAI Settings {applies_to}`stack: ga 9.4+`
:   The {{kib}} settings page where you configure the default model and other generative-AI options that affect {{agent-builder}}. See [](models.md#change-the-default-model).

## H

$$$human-in-the-loop$$$
Human-in-the-loop (HITL)
:   A pattern where an agent pauses during a conversation and waits for you to respond before it continues. {{agent-builder}} uses human-in-the-loop prompts to request confirmation for some actions, authorize access to external connectors, and ask clarifying questions. See [](chat.md#human-in-the-loop-prompts).

## I

$$$index-search-tool$$$
Index search tool
:   A type of custom tool that performs natural-language search over a configured set of indices, aliases, or data streams. The tool selects an appropriate query strategy (keyword, semantic, or hybrid) automatically. See [](tools/index-search-tools.md#when-to-use-index-search-tools).

$$$inference-endpoint$$$
Inference endpoint
:   An {{es}} resource that connects the cluster to a third-party or Elastic-managed model on EIS. {{agent-builder}} can use any inference endpoint that supports the `chat_completion` task type as a model source. Inference endpoints are managed from **Elastic inference**, **External inference**, or the [{{infer}} APIs]({{es-apis}}group/endpoint-inference). See [](models.md#add-an-inference-endpoint).

$$$inline-tool$$$
Inline tool
:   A tool that's available only in a specific context. For example, while a particular built-in skill is active or while an attachment is present in the conversation. Inline tools don't appear in the global tools list. See [](tools.md#how-agents-use-tools).

$$$input-tokens$$$
Input tokens
:   The tokens sent to the LLM in a request, including the user's message, the system prompt, accumulated conversation history, and tool responses. See [](monitor-usage.md#token-usage).

## K

$$$kibana-request-step$$$
`kibana.request` step {applies_to}`stack: preview 9.3+` {applies_to}`serverless: preview`
:   A generic Workflows step. When `ai.agent` doesn't cover a scenario, you can use `kibana.request` to call {{agent-builder}} APIs from a workflow. See [](/explore-analyze/workflows/steps/kibana.md#kibana-request).

## M

$$$manage-components$$$
Manage components {applies_to}`stack: ga 9.4+`
:   The link at the bottom of the standalone-mode left sidebar that opens the deployment-wide view of all agents, skills, plugins, connectors, and tools. See [](chat.md#manage-components).

$$$mcp$$$
MCP
:   The [Model Context Protocol](https://modelcontextprotocol.io/), an open standard for connecting AI assistants to external tools and data sources. {{agent-builder}} both _exposes_ tools through an MCP server and _consumes_ tools from remote MCP servers as MCP tools. See [](mcp-server.md#mcp-server-endpoint).

$$$mcp-connector$$$
MCP connector {applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview`
:   A {{kib}} connector that points {{agent-builder}} at a remote MCP server so its tools can be imported as MCP tools. See [](connectors.md#add-a-connector).

$$$mcp-server$$$
MCP server
:   An endpoint that implements the Model Context Protocol. {{agent-builder}} both _exposes_ its own MCP server, making Elastic tools and agents available to external MCP clients such as Claude Desktop, Cursor, VS Code, or LangChain apps, and _consumes_ remote MCP servers through MCP connectors. See [](mcp-server.md#mcp-server-endpoint).

$$$mcp-tool$$$
MCP tool {applies_to}`stack: preview 9.3+` {applies_to}`serverless: preview`
:   A type of custom tool that proxies a tool exposed by a remote MCP server. Use MCP tools to give your agents access to capabilities provided by external services. See [](tools/mcp-tools.md#adding-mcp-tools).

$$$model$$$
Model
:   The LLM that an agent uses to reason and produce responses. {{agent-builder}} can use Elastic Managed LLMs, third-party models accessed through an [](#inference-endpoint), or models accessed through a [](#generative-ai-connector). See [](models.md#use-additional-models).

$$$model-selector$$$
Model selector
:   The dropdown in Agent Chat used to switch the LLM that the current agent calls. See [](models.md#switch-models-in-the-ui).

$$$monitor-inference$$$
`monitor_inference`
:   The {{es}} cluster privilege required when an agent uses an AI connector that calls the {{es}} Inference API. Built-in tools such as `search` and `generate_esql`, and all index search tools, depend on this privilege. See [](permissions.md#es-cluster-privileges).

## O

$$$output-tokens$$$
Output tokens
:   The tokens generated by the LLM in a response, including the final answer shown to the user as well as any internal reasoning steps and tool-call payloads. See [](monitor-usage.md#token-usage).

## P

$$$plugin$$$
Plugin {applies_to}`stack: preview 9.4+` {applies_to}`serverless: preview`
:   A reusable bundle of skills and supporting capabilities that can be assigned to an agent as a single unit. Plugins make it easier to share groups of related skills across agents. See [](plugins.md#install-a-plugin).

$$$prompt-engineering$$$
Prompt engineering
:   The practice of writing instructions, examples, and constraints that steer LLM behavior. {{agent-builder}} provides guidance for shaping agent system prompts, custom instructions, and skill instructions. See [](prompt-engineering.md#core-principles).

## R

$$$reasoning$$$
Reasoning
:   The iterative process an agent follows to answer a request: analyzing the input, choosing tools, executing them, and incorporating results into a response. Each iteration is a _reasoning step_. See [](agent-builder-agents.md#how-agents-work).

$$$reasoning-events$$$
Reasoning events {applies_to}`stack: ga 9.5+`
:   The inline sequence in Agent Chat that shows an agent's reasoning steps, tool calls, tool responses, and final answer in the order they happen. See [](chat.md#inspect-tool-calls-and-reasoning).

$$$reasoning-panel$$$
Reasoning panel {applies_to}`stack: removed 9.5`
:   The pre-9.5 expandable section of the chat reply that showed the reasoning steps, tool calls, and tool responses behind an agent's answer. In 9.5 and later, Agent Chat uses inline reasoning events instead. See [](chat.md#inspect-tool-calls-and-reasoning).

$$$rest-api$$$
REST API
:   See {{agent-builder}} APIs.

$$$retrieval-augmented-generation-rag$$$
Retrieval-Augmented Generation (RAG)
:   Retrieval-augmented generation is a technique for improving language model responses by grounding the model with additional, verifiable sources of information. It works by first retrieving relevant context from a datastore, which is then added to the model's context window. {{agent-builder}} agents use {{es}} as the retrieval layer, which makes the platform a natural fit for RAG applications. See [](/solutions/search/rag.md).

## S

$$$sidebar-mode$$$
Sidebar mode {applies_to}`stack: preview =9.3, ga 9.4+` {applies_to}`serverless: ga`
:   The chat experience that opens as a persistent panel beside the page you're on, so you can chat with an agent without leaving your current {{kib}} workflow. Open it from the AI Agent button or with `cmd+;` / `ctrl+;`. See [](standalone-and-flyout-modes.md#sidebar-mode).

$$$skill$$$
Skill {applies_to}`stack: ga 9.4+`
:   A reusable capability pack that gives an agent specialized expertise for a particular type of task. A skill bundles instructions, tools, and reference content, and loads selectively based on the user's request. Skills sit one level above tools: a tool performs an operation, a skill teaches the agent _how_ and _when_ to use it. See [](skills.md#how-skills-are-invoked).

$$$skill-library$$$
Skill library {applies_to}`stack: ga 9.4+`
:   The deployment-wide collection of custom skills. Any custom agent can pull skills from the library. Built-in skills appear alongside them as read-only entries. See [](custom-skills.md#create-a-custom-skill).

$$$slash-command$$$
Slash command {applies_to}`stack: ga 9.4+`
:   The chat shortcut for explicitly invoking a skill. Type `/` followed by the skill name to bypass automatic skill selection. See [](skills.md#how-skills-are-invoked).

$$$solution-view$$$
Solution view
:   A {{kib}} space navigation mode oriented around a single solution ({{es}}, {{product.observability}}, or {{product.security}}). In {{product.elastic-stack}} deployments on version 8.16 and later, each space has its own navigation, called solution view. The solution view determines which {{agent-builder}} entry points and built-in capabilities are surfaced. See [](get-started.md#access-agent-builder).

$$$space$$$
Space
:   A {{kib}} space. Custom agents and custom tools are _space-aware_: they exist only in the space where they were created. The Elastic AI Agent is also space-aware. See [](/deploy-manage/manage-spaces.md) and [](permissions.md#working-with-spaces).

$$$standalone-mode$$$
Standalone mode
:   The full-page Agent Chat experience, opened from **Agents** in the main navigation. Standalone mode is recommended when you're working with dashboards, visualizations, or long agent replies. See [](standalone-and-flyout-modes.md#standalone-mode).

$$$system-prompt$$$
System prompt
:   The instructions that are always present in the context window. The system prompt defines an agent's core behavior. Custom instructions are layered on top of it. See [](prompt-engineering.md#how-agents-process-prompts).

## T

$$$token$$$
Token
:   The unit of text that an LLM processes. Token counts roughly correspond to fragments of words and determine how much of the context window a message consumes, as well as the cost of a request. See [](monitor-usage.md#token-usage).

$$$tool$$$
Tool
:   A modular function an agent can call to search, retrieve, or manipulate {{es}} data. Tools are the primary mechanism for grounding agent capabilities in your data. {{agent-builder}} provides built-in tools; you can also create custom tools of four types: {{esql}}, index search, MCP, and workflow. See [](tools.md#how-agents-use-tools).

## V

$$$visibility$$$
Visibility
:   A custom agent's sharing setting that controls who can see and edit it. Options are **Public** (anyone in the space), **Shared** (anyone can view; only owners and admins can edit), and **Private** (only owners and admins). See [](custom-agents.md#visibility-settings).

## W

$$$workflow-tool$$$
Workflow tool {applies_to}`stack: preview 9.3+` {applies_to}`serverless: preview`
:   A type of custom tool that lets an agent trigger a workflow from a conversation and use its output. See [](/explore-analyze/workflows.md) and [](tools/workflow-tools.md#add-a-workflow-tool).

$$$workflows$$$
Workflows
:   Elastic's native automation engine for declarative, event-driven automation defined in YAML. {{agent-builder}} integrates with workflows in two directions: agents can trigger workflows through workflow tools, and workflows can call agents through the `ai.agent` and `kibana.request` steps. See [](agents-and-workflows.md#approaches).
