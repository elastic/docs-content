---
navigation_title: AI
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Call LLMs, run Agent Builder agents, and manage agent conversations, including their attachments and metadata, from workflows with AI steps. This reference lists each step's parameters, output, and examples.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# AI steps [workflows-ai-steps]

AI steps let workflows call a large language model (LLM) for reasoning, classification, summarization, or agent-driven execution.

AI steps can also manage {{agent-builder}} conversations:

- {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` Create a conversation.
- {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` Add notes and user messages to a conversation without triggering an agent response.
- {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` Read and update a conversation's attachments and metadata.

The `ai.prompt`, `ai.classify`, `ai.summarize`, and `ai.agent` steps reference a model by ID in the step. Configure a Generative AI connector in {{kib}} and pass its ID in `connector-id`. For [`ai.agent`](#ai-agent), you can instead pass an {{infer}} endpoint ID in `inference-id`.

If you omit both, `ai.agent` uses the same model that {{agent-builder}} would use for the agent. Refer to [Model configuration in {{agent-builder}}](/explore-analyze/ai-features/agent-builder/models.md).

If you omit `connector-id` from `ai.prompt`, `ai.classify`, or `ai.summarize`:

::::{applies-switch}
:::{applies-item} { stack: ga 9.5+, serverless: ga }
The step uses the first available model assigned to it in [**Feature Settings**](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#feature-settings), under **AI Prompt step**, **AI Classify step**, or **AI Summarize step**. Each step comes with recommended models assigned by default, so this works without any setup. If none of the assigned models is available, the step uses the [default AI connector](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#genai-settings).
:::
:::{applies-item} stack: ga 9.3-9.4
The step uses the [default AI connector](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#genai-settings).
:::
::::

:::{note}
:applies_to: { serverless: deprecated, stack: deprecated 9.5+ }

Generative AI connectors are deprecated. The `ai.agent` step accepts an {{infer}} endpoint through `inference-id`. The `ai.prompt`, `ai.classify`, and `ai.summarize` steps take `connector-id` only.
:::

## Reasoning level [ai-reasoning-level]

```{applies_to}
stack: preview 9.6+
serverless: preview
```

Use the optional `reasoning-level` field on `ai.prompt` and `ai.agent` steps to control how much reasoning the model does before it responds. The field accepts `none`, `minimal`, `low`, `medium`, `high`, or `xhigh`, in lowercase. Only `ai.prompt` and `ai.agent` accept this field. How each level affects the response depends on the model and provider.

Whether the model receives the level depends on how the step connects to it:

- [Elastic Managed LLMs](/explore-analyze/ai-features/agent-builder/models.md) and {{infer}} endpoints receive the level you set. If the model doesn't support that level, the step fails. Check the model provider's documentation for the levels each model supports.
- Other connectors, such as OpenAI, Amazon Bedrock, and Google Gemini, ignore the field, and the step runs normally.

On [`ai.agent`](#ai-agent) steps:

- If you omit `reasoning-level`, the step uses the agent's default level. Only built-in agents have a default. For custom agents, or when the agent has no default, the model uses its own default.
- The level applies only to the agent's own model calls. It doesn't apply to the [subagents](/explore-analyze/ai-features/agent-builder/agent-builder-agents.md#subagents) that the agent starts, or to tasks that {{agent-builder}} sends to the [fast model](/explore-analyze/ai-features/agent-builder/models.md#fast-model).

For example, this step sets a high reasoning level for a custom agent:

```yaml
- name: investigate
  type: ai.agent
  agent-id: "security-analyst-agent"
  reasoning-level: "high"
  with:
    message: "Investigate alert {{ event.alerts[0]._id }} and propose next steps."
```

## Step types

- [`ai.prompt`](#ai-prompt): Send a prompt to a model and receive a response. Supports structured output with a JSON Schema. {applies_to}`stack: preview 9.3, ga 9.4+`
- [`ai.classify`](#ai-classify): Classify input into a fixed set of categories. {applies_to}`stack: ga 9.4+`
- [`ai.summarize`](#ai-summarize): Generate a summary of the provided content. {applies_to}`stack: ga 9.4+`
- [`ai.agent`](#ai-agent): Invoke an {{agent-builder}} agent as a workflow step. {applies_to}`stack: preview 9.3, ga 9.4+`
- [`ai.conversation.create`](#ai-conversation-create): Create an empty {{agent-builder}} conversation. {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview`
- [`ai.conversation.add_event`](#ai-conversation-add-event): Add an event, such as a note, to a conversation without triggering an agent response. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
- [`ai.conversation.add_user_message`](#ai-conversation-add-user-message): Add a user message to a conversation without triggering an agent response. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
- [`ai.conversation.metadata.read`](#ai-conversation-metadata-read): Read the metadata of a conversation. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
- [`ai.conversation.metadata.patch`](#ai-conversation-metadata-patch): Update the metadata of a conversation. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
- [`ai.attachment.add`](#ai-attachment-add): Add an attachment to a conversation. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
- [`ai.attachment.update`](#ai-attachment-update): Update an attachment in a conversation. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
- [`ai.attachment.delete`](#ai-attachment-delete): Delete an attachment from a conversation. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
- [`ai.attachment.read`](#ai-attachment-read): Read the content of an attachment. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`
- [`ai.attachment.list`](#ai-attachment-list): List the attachments in a conversation. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga`

Where a step's fields go, and how they're named, depends on the step:

| Steps | Top-level fields | Parameters inside `with` |
|---|---|---|
| `ai.prompt`, `ai.classify`, `ai.summarize`, `ai.agent` | Fields marked **top level** in each step's table, such as `connector-id`, `agent-id`, and `inference-id`. They use kebab-case (`connector-id`, not `connectorId`) and sit alongside `name`, `type`, `if`, and `foreach`, not under `with`. | Mostly camelCase, such as `systemPrompt`, `maxLength`, and `includeRationale`. |
| `ai.conversation.*`, `ai.attachment.*` | None. | snake_case, such as `conversation_id`. |

Whether you can use Liquid expressions in these top-level fields depends on your version:

::::{applies-switch}
:::{applies-item} { stack: ga 9.5+, serverless: ga }
Liquid expressions are evaluated in these top-level fields, so you can use templated values (for example, `"{{ consts.agent_id }}"`).
:::
:::{applies-item} stack: ga 9.3-9.4
Liquid expressions in these top-level fields aren't evaluated, so use a literal value (for example, `agent-id: elastic-ai-agent`) instead of `"{{ consts.agent_id }}"`.
:::
::::

{applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` `ai.prompt` and `ai.agent` also accept a top-level `reasoning-level` field. Refer to [Reasoning level](#ai-reasoning-level).

:::{include} ../_snippets/schema-location-legend.md
:::

## `ai.prompt` [ai-prompt]

```{applies_to}
stack: preview 9.3, ga 9.4+
```

Call an LLM with a prompt. Supports optional structured output through a JSON Schema.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `connector-id` | top level | string | No | The Generative AI connector to use. If omitted, the step uses the default model described at the start of this page. |
| `reasoning-level` {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` | top level | string | No | How much reasoning the model does before it responds: `none`, `minimal`, `low`, `medium`, `high`, or `xhigh`. If omitted, the model uses its own default. Refer to [Reasoning level](#ai-reasoning-level). |
| `prompt` | `with` | string | Yes | Prompt text. Supports Liquid templating. |
| `systemPrompt` | `with` | string | No | System prompt sent before the user prompt. |
| `schema` | `with` | object | No | JSON Schema for structured output. |
| `temperature` | `with` | number (0–1) | No | Model temperature. Lower values are more deterministic. |

**Output shape:**

- Free text: `{ content: string, metadata: object }`
- With `schema`: `{ content: <structured object matching schema>, metadata: object }`

```yaml
- name: summarize
  type: ai.prompt
  connector-id: "my-openai"
  with:
    prompt: |
      Summarize this alert in one sentence:
      {{ event.alerts[0] | json }}
```

### Example: Structured output

```yaml
- name: extract_details
  type: ai.prompt
  connector-id: "my-openai"
  with:
    prompt: "Extract key details from this alert: {{ event.alerts[0] | json }}"
    schema:
      type: "object"
      properties:
        severity:
          type: "string"
          enum: ["low", "medium", "high", "critical"]
        summary:
          type: "string"
        key_indicators:
          type: "array"
          items:
            type: "string"
```

The structured result is available at `steps.extract_details.output.content.severity`, and so on.

## `ai.classify` [ai-classify]

```{applies_to}
stack: ga 9.4+
```

Classify input into one of a fixed set of categories. Optionally includes a rationale and supports multi-label classification.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `connector-id` | top level | string | No | Generative AI connector to use. |
| `input` | `with` | string, array, or object | Yes | Input to classify. |
| `categories` | `with` | array of string or object | Yes | Allowed categories. At least one required. Each entry is a plain category-name string. {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Each entry can also be an object with `name` and `description`. |
| `instructions` | `with` | string | No | Guidance for the classifier. |
| `allowMultipleCategories` | `with` | boolean | No | Allow the output to include more than one category. |
| `fallbackCategory` | `with` | string or object | No | Category returned when the model can't confidently choose. Accepts a plain string. {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` Can also accept an object with `name` and `description`. |
| `includeRationale` | `with` | boolean | No | Include the model's reasoning in the output. |
| `temperature` | `with` | number (0–1) | No | Model temperature. |

**Output shape:**

| Field | Type | Presence |
|---|---|---|
| `category` | string | Present when `allowMultipleCategories` is false (default). Always the category `name`, even when you define the category as an object. |
| `categories` | `string[]` | Present when `allowMultipleCategories` is true. |
| `rationale` | string | Present when `includeRationale` is true. |
| `metadata` | object | Always. |

```yaml
- name: classify
  type: ai.classify
  connector-id: "my-bedrock"
  with:
    input: "${{ event.alerts[0] }}"
    categories: ["true_positive", "false_positive", "needs_investigation"]
    includeRationale: true
    fallbackCategory: "needs_investigation"
```

:::{tip}
Always set `fallbackCategory` in production. Without a fallback, a confused model can fail the step. With one, every invocation produces a usable category you can branch on with a [`switch`](/explore-analyze/workflows/steps/switch.md) or [`if`](/explore-analyze/workflows/steps/if.md).
:::

### Example: Category descriptions [ai-classify-category-descriptions]

```{applies_to}
stack: ga 9.5+
serverless: ga
```

`categories` and `fallbackCategory` also accept an object with `name` and `description` instead of a plain string. When you supply a description, the step includes it in the classification prompt sent to the model, which improves category selection when categories are closely related or ambiguous. This doesn't affect category names in the output: `category` and `categories` in the step output always contain the category `name`, never the description.

```yaml
- name: classify_alert
  type: ai.classify
  connector-id: "my-bedrock"
  with:
    input: "{{ inputs.alert_narrative }}"
    categories:
      - name: "Phishing"
        description: "User-targeted deception to steal credentials or deliver malicious links; no sustained host compromise pattern required."
      - name: "Malware"
        description: "Execution of malicious code, ransomware, or clear C2/beaconing on an endpoint."
      - name: "Credential Access"
        description: "Brute force, password spraying, or secret dumping without confirmed large outbound data transfer."
    fallbackCategory:
      name: "Unknown"
      description: "Insufficient signal to map confidently to any defined category."
    includeRationale: true
```

You can mix plain strings and objects in the same `categories` list: the classifier treats a plain string as a category with no description.

## `ai.summarize` [ai-summarize]

```{applies_to}
stack: ga 9.4+
```

Summarize content with an LLM. Input can be a string, an array, or an object.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `connector-id` | top level | string | No | Generative AI connector to use. |
| `input` | `with` | string, array, or object | Yes | Content to summarize. |
| `instructions` | `with` | string | No | Summary guidance. |
| `maxLength` | `with` | number | No | Approximate maximum length (positive integer). |
| `temperature` | `with` | number (0–1) | No | Model temperature. |

**Output shape:** `{ content: string, metadata?: object }`.

```yaml
- name: summary
  type: ai.summarize
  connector-id: "my-gemini"
  with:
    input: "${{ steps.gather.output }}"
    instructions: "Describe the root cause in two or three sentences."
    maxLength: 500
```

## `ai.agent` [ai-agent]

```{applies_to}
stack: preview 9.3, ga 9.4+
```

Invoke an {{agent-builder}} agent as a workflow step. Useful when you want a multi-turn agent loop embedded inside a workflow. The agent handles tool selection, reasoning, and response synthesis. The workflow handles pre- and post-processing.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `agent-id` | top level | string | No | Agent to invoke. Defaults to the built-in Elastic AI Agent. |
| `connector-id` {applies_to}`serverless: deprecated` {applies_to}`stack: deprecated 9.5+` | top level | string | No | Generative AI connector. Mutually exclusive with `inference-id`. Generative AI connectors are deprecated, so use `inference-id` for new workflows. |
| `inference-id` | top level | string | No | Inference endpoint ID. Mutually exclusive with `connector-id`. |
| `create-conversation` | top level | boolean | No | When `true`, persist the conversation for follow-up steps or later reference. |
| `public-conversation` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | top level | boolean | No | When `true`, make the conversation this step creates public. Any user who can access the agent can read and continue the conversation and see it in their conversation list. Only applies when `create-conversation` is `true`. Defaults to `false` (private). Refer to [Conversation access control](/explore-analyze/ai-features/agent-builder/permissions.md#conversation-access-control). |
| `ephemeral` {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | top level | boolean | No | When `true`, the agent uses the history, attachments, and metadata of the conversation set in `conversation_id` as context but doesn't change it. The run doesn't answer a conversation that's [awaiting your input](/explore-analyze/ai-features/agent-builder/chat.md#track-conversation-status), and it runs the agent's [pre-execution workflows](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md#pre-execution-workflows) but not its post-execution workflows. The [user who authorizes the run](/explore-analyze/workflows/authorization.md#workflows-authorization-user) must own the conversation, be a member of it, or the conversation must be public, and must be able to use its agent. Otherwise, the step fails. Has no effect without `conversation_id`. Can't be combined with `create-conversation: true`. The editor doesn't flag this combination, but the step fails at run time. Defaults to `false`. Refer to [Example: Summarize a conversation without changing it](#ai-agent-ephemeral). |
| `reasoning-level` {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` | top level | string | No | How much reasoning the agent's model does before it responds: `none`, `minimal`, `low`, `medium`, `high`, or `xhigh`. If omitted, the step uses the agent's default level, if it has one. Refer to [Reasoning level](#ai-reasoning-level). |
| `message` | `with` | string | Yes | User message to send to the agent. |
| `schema` | `with` | object | No | JSON Schema for structured output. |
| `conversation_id` | `with` | string | No | Continue an existing conversation by ID. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` With `ephemeral: true`, the conversation is read and not updated. |
| `attachments` | `with` | array | No | Attachments to provide to the agent. Each attachment has `{ id?, type, data?, origin?, hidden? }`. |

**Output shape:**

| Field | Type | Presence |
|---|---|---|
| `message` | string | Always. Text response, or a string representation when `schema` is provided. |
| `structured_output` | any | Present when `schema` is provided. |
| `conversation_id` | string | Present when the step creates or updates a conversation. {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` Omitted when `ephemeral` is `true`, even if `conversation_id` was provided. |

:::{important}
Use `connector-id` **or** `inference-id`, not both. The schema rejects a step that sets both.
:::

### Example: Call an agent

```yaml
- name: investigate
  type: ai.agent
  agent-id: "security-analyst-agent"
  inference-id: "my-inference-endpoint"
  create-conversation: true
  with:
    message: |
      Investigate alert {{ event.alerts[0]._id }} and propose next steps.
    schema:
      type: "object"
      properties:
        findings:
          type: "array"
          items:
            type: "string"
        recommended_action:
          type: "string"
```

### Example: Continue a conversation

```yaml
- name: followup
  type: ai.agent
  agent-id: "security-analyst-agent"
  with:
    conversation_id: "{{ steps.investigate.output.conversation_id }}"
    message: "Apply the recommended action and report back."
```

### Example: Summarize a conversation without changing it [ai-agent-ephemeral]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

The following step summarizes the `investigate` conversation without changing it. The summary is in `steps.summarize.output.message`.

```yaml
- name: summarize
  type: ai.agent
  agent-id: "security-analyst-agent"
  ephemeral: true
  with:
    conversation_id: "{{ steps.investigate.output.conversation_id }}"
    message: "Summarize this conversation in five bullet points."
```

## `ai.conversation.create` [ai-conversation-create]

```{applies_to}
stack: preview 9.6+
serverless: preview
```

Create an empty {{agent-builder}} conversation without sending a message. Use the returned `conversation_id` in later steps, such as [`ai.conversation.add_event`](#ai-conversation-add-event), [`ai.conversation.add_user_message`](#ai-conversation-add-user-message), or [`ai.agent`](#ai-agent).

All parameters go in the `with` block and use `snake_case`.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `agent_id` | `with` | string | No | Agent to associate with the conversation. Defaults to the built-in Elastic AI Agent. The step fails if the agent doesn't exist or the user whose privileges authorize the run can't use it. |
| `conversation_id` | `with` | string (UUID) | No | ID for the new conversation. Must be a UUID. Generated if omitted. The step fails if a conversation with this ID already exists. |
| `title` | `with` | string | No | Conversation title, up to 500 characters. Defaults to `New conversation`. |
| `access_control` | `with` | object | No | Who can access the conversation. Defaults to private. Takes `access_mode` (`private` or `public`) and optional `entries` (up to 100). Each entry adds a member and has the shape `{ type: user, id: <user profile UID>, role: member }`. Entries are allowed only for private conversations. The step fails if you set `access_mode: public` with any entries. Refer to [Conversation access control](/explore-analyze/ai-features/agent-builder/permissions.md#conversation-access-control). |
| `template_id` | `with` | string | No | ID of a built-in conversation template. Use `investigation` or `escalation`. The template sets default metadata and controls the [**Chat info** flyout](/explore-analyze/ai-features/agent-builder/chat.md#conversation-templates). The step fails if the template doesn't exist. For the keys you can set, refer to [Conversation template metadata](#conversation-template-metadata). |
| `metadata` | `with` | object | No | Initial metadata values. Requires `template_id`, and each key must be defined by the template. Up to 100 keys. Key names can be up to 256 characters. Each value can be a string (up to 10,000 characters), a number, a boolean, or an array of up to 100 strings (up to 2,000 characters each). |

**Output shape:**

| Field | Type | Presence |
|---|---|---|
| `conversation_id` | string | Always. |
| `agent_id` | string | Always. |
| `template_id` | string | When `template_id` is set. |
| `metadata` | object | Always. The conversation metadata after template defaults and your `metadata` values are applied. Empty if no template is used. |

If you set `agent_id`, set the same agent in `agent-id` on any [`ai.agent`](#ai-agent) step that continues the conversation. Otherwise, `ai.agent` runs the default Elastic AI Agent, not the agent you set when you created the conversation.

```yaml
- name: create_conversation
  type: ai.conversation.create
  with:
    title: "Checkout incident"
```

To create an investigation and set its severity and description:

```yaml
- name: create_investigation
  type: ai.conversation.create
  with:
    title: "Checkout incident"
    template_id: investigation
    metadata:
      severity: high
      description: "Checkout error rate increased after the last deploy."
```

### Conversation template metadata [conversation-template-metadata]

Each built-in template defines the metadata keys that a conversation accepts. The step fails if `metadata` includes a key that the template doesn't define. The agent can update these keys during later runs on the conversation. Other content in the **Chat info** flyout, such as impact and proposed actions, doesn't come from these keys.

`investigation` and `escalation` share these keys:

| Key | Description | Accepted values | Default |
|---|---|---|---|
| `status` | Whether the investigation or escalation is open or closed. Can't be empty. | `open` or `closed` | `open` |
| `severity` | The severity level | `low`, `medium`, `high`, or `critical` | None |
| `assignees` | The assigned users | List of user profile UIDs | None |
| `verdict` | The outcome of the investigation or escalation | Text, up to 10,000 characters | None |
| `summary` | The summary of the investigation or escalation so far | Text, up to 10,000 characters | None |
| `description` | A one-line summary | Text, up to 10,000 characters | None |
| `close_reason` | The reason for closing | `false_positive`, `benign`, `resolved`, `duplicate`, or `other` | None |

Each template also accepts its own keys:

- `investigation`: `workflow_execution_ids`, a list of workflow execution IDs for runs that have worked on the investigation.
- `escalation`: `linked_investigations`, a list of conversation IDs of the investigations linked to the escalation.

To update these keys from a workflow, use [`ai.conversation.metadata.patch`](#ai-conversation-metadata-patch).

## `ai.conversation.add_event` [ai-conversation-add-event]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

Add an event to an {{agent-builder}} conversation without triggering an agent response. {{kib}} features can define their own event types, and each type defines the shape of its `data` payload. {{agent-builder}} provides the `text_note` type for notes. The agent reads a note the next time it runs on the conversation. Other event types might only be shown in the conversation and not sent to the agent. The step works the same way as the [add events to a conversation API](/explore-analyze/ai-features/agent-builder/kibana-api.md#add-conversation-events).

All parameters go in the `with` block and use `snake_case`.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation to add the event to. |
| `type` | `with` | string | Yes | Event type, up to 256 characters. Must be a custom event type defined by {{kib}}, such as `text_note` to add a note. Built-in conversation event types, such as user messages, are rejected. To add a user message, use [`ai.conversation.add_user_message`](#ai-conversation-add-user-message). |
| `data` | `with` | object | Depends on `type` | Event payload, validated against the shape that `type` defines. Required for `text_note`: set `text` (up to 1,000 characters) and, optionally, `title` (up to 256 characters). Neither field can be an empty string. Other fields in `data` are discarded. |

**Output shape:**

| Field | Type | Presence |
|---|---|---|
| `conversation_id` | string | Always. |
| `event_id` | string | Always. |
| `type` | string | Always. |
| `created_at` | string | Always. ISO 8601 timestamp. |

If the event type is unknown or `data` doesn't match the type, the step fails and adds nothing. You can't update or remove an event after you add it.

:::{note}
Events are attributed to the user whose privileges authorize the run, not to the workflow. That user must own the conversation or be a member of it, or the conversation must be public. The user must also be able to use the conversation's agent. Otherwise, the step fails. To find out which user authorizes a run, refer to [Workflow authorization](/explore-analyze/workflows/authorization.md#workflows-authorization-user).
:::

### Example: Add a note, then summarize

```yaml
- name: create_conversation
  type: ai.conversation.create
  with:
    title: "Checkout incident"

- name: add_update
  type: ai.conversation.add_event
  with:
    conversation_id: "{{ steps.create_conversation.output.conversation_id }}"
    type: text_note
    data:
      title: "Status update"
      text: "Checkout service latency is back to normal."

- name: summarize
  type: ai.agent
  with:
    conversation_id: "{{ steps.create_conversation.output.conversation_id }}"
    message: "Summarize the status updates in this conversation."
```

## `ai.conversation.add_user_message` [ai-conversation-add-user-message]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

Add a user message to an existing {{agent-builder}} conversation without triggering an agent response. The agent reads the message the next time it runs on the conversation.

All parameters go in the `with` block and use `snake_case`.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation to add the message to. The conversation must already exist. To create one, use [`ai.conversation.create`](#ai-conversation-create). |
| `message` | `with` | string | Yes | Message text. Can't be empty or contain only whitespace. |

**Output shape:** `{ conversation_id: string }`.

Unlike `ai.agent`, this step doesn't accept attachments.

:::{note}
Messages are attributed to the user whose privileges authorize the run, not to the workflow. That user must own the conversation or be a member of it, or the conversation must be public. The user must also be able to use the conversation's agent. Otherwise, the step fails. To find out which user authorizes a run, refer to [Workflow authorization](/explore-analyze/workflows/authorization.md#workflows-authorization-user).
:::

The following example runs in a workflow with an alert trigger, after an [`ai.conversation.create`](#ai-conversation-create) step named `create_conversation`. It adds the ID of the alert that triggered the workflow to the conversation:

```yaml
- name: add_alert
  type: ai.conversation.add_user_message
  with:
    conversation_id: "{{ steps.create_conversation.output.conversation_id }}"
    message: "A new alert fired: {{ event.alerts[0]._id }}"
```

## Conversation metadata steps [ai-conversation-metadata-steps]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

Conversation metadata is a set of structured fields, such as `status` or `severity`, that track the state of a conversation. The template applied to the conversation defines which fields exist and which values each one accepts.

Use these steps to read the metadata, for example to branch a workflow on a field's value, or to update it, for example to record the outcome of an investigation. The agent also sees the fields and their current values each time it runs on the conversation. In the chat, users see the template name as the conversation's type, but not the field values.

Only conversations with a template have metadata:

- Conversations that `ai.agent` creates, or that users start in chat, have no template.
- To create a conversation with a template from a workflow, use [`ai.conversation.create`](#ai-conversation-create) with `template_id` set to a built-in template: `investigation` or `escalation`. `ai.conversation.create` is in technical preview, so a workflow that creates a conversation with metadata depends on a preview step.

Both built-in templates, `investigation` and `escalation`, define the following fields:

| Field | Type | Accepted values | Default |
|---|---|---|---|
| `status` | One value from a fixed list | `open`, `closed` | `open` |
| `severity` | One value from a fixed list | `low`, `medium`, `high`, `critical` | None |
| `close_reason` | One value from a fixed list | `false_positive`, `benign`, `resolved`, `duplicate`, `other` | None |
| `assignees` | List of text values | User IDs | None |
| `verdict` | Text | The outcome, up to 10,000 characters | None |
| `summary` | Text | A summary so far, up to 10,000 characters | None |
| `description` | Text | A one-line summary | None |

The `escalation` template also has a `linked_investigations` field, a list of investigation IDs.

:::{note}
These steps run with the privileges of the user who authorizes the run. That user needs:

- Access to the conversation: they own it, are a member of it, or the conversation is public.
- Access to the agent the conversation uses.

Otherwise, the step fails with a `Conversation <id> not found` error, even if the conversation ID is correct. To find out which user authorizes a run, refer to [Workflow authorization](/explore-analyze/workflows/authorization.md#workflows-authorization-user).
:::

### `ai.conversation.metadata.read` [ai-conversation-metadata-read]

Read all metadata fields of a conversation.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation to read the metadata from. |

**Output shape:** `{ metadata: object }`. The current metadata fields and their values. Empty if the conversation has no metadata.

The following example runs in a separate workflow that receives the ID of an investigation conversation as an input, for example when another workflow [calls it](/explore-analyze/workflows/authoring-techniques/compose-workflows.md). It logs a message if the investigation is closed:

```yaml
inputs:
  - name: conversation_id
    type: string
    required: true

steps:
  - name: read_metadata
    type: ai.conversation.metadata.read
    with:
      conversation_id: "{{ inputs.conversation_id }}"

  - name: check_status
    type: if
    condition: 'steps.read_metadata.output.metadata.status : "closed"'
    steps:
      - name: log_closed
        type: console
        with:
          message: "The investigation is closed."
```

### `ai.conversation.metadata.patch` [ai-conversation-metadata-patch]

Update one or more metadata fields of a conversation. The step merges your values into the existing metadata. Fields you don't include keep their current values.

The step has the following requirements:

- The conversation must have a template applied.
- You can only set fields that the template defines.
- Each value must match the field's type and constraints. For example, a field with a fixed list of values rejects any value that isn't in the list.
- You can't set a field to `null` or remove it. To clear a text or list field that isn't required, set it to an empty string or an empty list. You can't clear a required field, such as `status`, or a field with a fixed list of values.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation to update. |
| `updates` | `with` | object | Yes | Fields to set, as key-value pairs. For size limits, refer to the list after this table. |

The `updates` object has the following limits:

- 1 to 100 key-value pairs.
- Keys up to 256 characters.
- Values can be a string (up to 10,000 characters), a number, a boolean, or an array of up to 100 strings (up to 2,000 characters each).

**Output shape:**

| Field | Type | Presence |
|---|---|---|
| `conversation_id` | string | Always. |
| `changed_fields` | array of strings | Always. Names of the fields whose values changed. Empty if no value changed. |
| `metadata` | object | Always. All metadata fields after the update. |

The following example runs after an [`ai.conversation.create`](#ai-conversation-create) step named `create_conversation` that sets `template_id: investigation`. It closes the investigation and records why:

```yaml
- name: resolve_investigation
  type: ai.conversation.metadata.patch
  with:
    conversation_id: "{{ steps.create_conversation.output.conversation_id }}"
    updates:
      status: "closed"
      close_reason: "resolved"
      severity: "low"
```

## Conversation attachment steps [ai-attachment-steps]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

An attachment is content, such as a runbook or a dashboard, that you add to an {{agent-builder}} conversation so the agent can use it as context. Each attachment has a type, such as text, that determines the shape of its content. When you update an attachment, the earlier content is kept as a previous version.

Use these steps to add, update, delete, read, and list the attachments in a conversation.

All parameters go in the `with` block and use `snake_case`. Every attachment step takes the `conversation_id` of the conversation the attachment belongs to.

The examples in this section use the conversation created by the `investigate` step in [Example: Call an agent](#example-call-an-agent).

These steps follow the same access rules as the [conversation metadata steps](#ai-conversation-metadata-steps): the user who authorizes the run must be able to access both the conversation and the agent it uses.

### `ai.attachment.add` [ai-attachment-add]

Add an attachment to a conversation. Provide the content directly in `data`, or set `origin` to copy it from a {{kib}} object, such as a dashboard.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation to add the attachment to. |
| `type` | `with` | string | Yes | Attachment type, such as `text`. {{kib}} features can register their own attachment types, so the available types depend on your deployment. The step fails if the type doesn't exist. |
| `data` | `with` | any | Depends | Attachment content. Its shape depends on `type`. For `text`, use `{ content: "<text>" }`. Required unless you set `origin`. |
| `origin` | `with` | string | Depends | ID of the {{kib}} object to copy the content from, such as a dashboard ID, up to 2,048 characters. Required unless you set `data`. |
| `id` | `with` | string | No | Attachment ID, up to 256 characters. Generated if omitted. The step fails if the conversation already has an attachment with this ID. |
| `description` | `with` | string | No | Description of the attachment, up to 1,024 characters. |
| `hidden` | `with` | boolean | No | When `true`, users don't see the attachment when it's added, even if `render_inline` is `true`. The agent can still use it, and users see it if the agent refers to it in a response. Takes precedence over `render_inline`. Defaults to `false`. |
| `render_inline` | `with` | boolean | No | When `true`, users see the attachment as soon as they open the conversation. When `false`, users see it only when the agent refers to it in a response. Defaults to `false`. |

If you set `origin` without `data`, the step copies the object's content once, when it creates the attachment. Later changes to the object don't update the attachment. If you set both `data` and `origin`, the step uses `data` as the content and doesn't copy anything from the object. Not all attachment types support `origin`. For example, `text` doesn't, but the dashboard type, `platform.dashboard.dashboard_state`, does. To attach a dashboard, set `type` to `platform.dashboard.dashboard_state` and `origin` to the dashboard ID.

**Output shape:**

| Field | Type | Presence |
|---|---|---|
| `attachment_id` | string | Always. |
| `type` | string | Always. |
| `current_version` | number | Always. `1` for a new attachment. |

The following example adds a runbook to the conversation and shows it to users as soon as they open the conversation:

```yaml
- name: add_runbook
  type: ai.attachment.add
  with:
    conversation_id: "{{ steps.investigate.output.conversation_id }}"
    type: text
    data:
      content: "Runbook: reset the checkout cache before retrying."
    description: "Checkout runbook"
    render_inline: true
```

### `ai.attachment.update` [ai-attachment-update]

Update the content or description of an attachment. You can't update a deleted attachment.

The step creates a new version only when `data` differs from the current content. Updating only `description` doesn't create a new version.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation the attachment belongs to. |
| `attachment_id` | `with` | string | Yes | Attachment to update. |
| `data` | `with` | any | No | New attachment content. |
| `description` | `with` | string | No | New description, up to 1,024 characters. |
| `render_inline` | `with` | boolean | No | When `true`, the new version is displayed as soon as a user opens the conversation. Has an effect only when `data` changes and a new version is created. |

**Output shape:** `{ attachment_id: string, current_version: number }`. `current_version` is the new version number when the content changed, and the existing version number otherwise.

The following example replaces the runbook's content, which creates version 2 of the attachment:

```yaml
- name: update_runbook
  type: ai.attachment.update
  with:
    conversation_id: "{{ steps.investigate.output.conversation_id }}"
    attachment_id: "{{ steps.add_runbook.output.attachment_id }}"
    data:
      content: "Runbook: reset the checkout cache, then restart the payment service."
```

### `ai.attachment.delete` [ai-attachment-delete]

Delete an attachment from a conversation. By default, the step does a regular deletion: the attachment is marked as deleted, but its content and version history are kept. A deleted attachment no longer appears in the agent's list of attachments, and users no longer see it in the conversation. You can still read it with [`ai.attachment.read`](#ai-attachment-read), and list it with `include_deleted: true` in [`ai.attachment.list`](#ai-attachment-list). To remove the attachment and its history completely, set `permanent: true`.

You can't permanently delete an attachment in the following cases. Use a regular deletion instead.

- The agent has already used the attachment in the conversation, by reading it, updating it, or comparing its versions.
- The attachment, or its `data`, has a `client_id` field. This isn't the `id` you can set with [`ai.attachment.add`](#ai-attachment-add).

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation the attachment belongs to. |
| `attachment_id` | `with` | string | Yes | Attachment to delete. |
| `permanent` | `with` | boolean | No | When `true`, removes the attachment completely. Defaults to `false`. |

**Output shape:** `{ success: boolean, permanent: boolean }`.

The following example deletes the runbook. Because `permanent` isn't set, you can still read and list the attachment afterward:

```yaml
- name: delete_runbook
  type: ai.attachment.delete
  with:
    conversation_id: "{{ steps.investigate.output.conversation_id }}"
    attachment_id: "{{ steps.add_runbook.output.attachment_id }}"
```

### `ai.attachment.read` [ai-attachment-read]

Read the content of an attachment. By default, the step returns the current version. You can also read an attachment that was deleted without `permanent: true`.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation the attachment belongs to. |
| `attachment_id` | `with` | string | Yes | Attachment to read. |
| `version` | `with` | number | No | Version to read. Defaults to the current version. The step fails if the version doesn't exist. |

**Output shape:** `{ data: any, version: number }`.

The following example reads version 1 of the runbook, which is its content from before the update:

```yaml
- name: read_runbook
  type: ai.attachment.read
  with:
    conversation_id: "{{ steps.investigate.output.conversation_id }}"
    attachment_id: "{{ steps.add_runbook.output.attachment_id }}"
    version: 1
```

### `ai.attachment.list` [ai-attachment-list]

List the attachments of a conversation. The step returns a summary of each attachment, not its content. To get the content, use [`ai.attachment.read`](#ai-attachment-read).

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation whose attachments to list. |
| `include_deleted` | `with` | boolean | No | When `true`, also returns attachments deleted without `permanent: true`. Defaults to `false`. |

**Output shape:**

| Field | Type | Presence |
|---|---|---|
| `attachments` | array | Always. Each item has `id`, `type`, `current_version`, `active`, and, if set, `description`. `active` is `false` for deleted attachments. |
| `total_token_estimate` | number | Always. Estimated size, in tokens, of the active attachments. Deleted attachments aren't counted, even with `include_deleted: true`. Use it to check how much of the model's context window the attachments use. Refer to [](/explore-analyze/ai-features/agent-builder/troubleshooting/context-length-exceeded.md). |

The following example lists the attachments in the conversation that haven't been deleted:

```yaml
- name: list_attachments
  type: ai.attachment.list
  with:
    conversation_id: "{{ steps.investigate.output.conversation_id }}"
```

## Related

- [Configured AI connectors](/deploy-manage/manage-connectors.md): Set up the Generative AI connector referenced by `connector-id`.
- [Switch step](/explore-analyze/workflows/steps/switch.md): A common pairing: classify with `ai.classify`, then dispatch with `switch`.
- [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md): Pair AI classifications with a reviewer gate for uncertain cases.
- [{{agent-builder}} overview](/explore-analyze/ai-features/elastic-agent-builder.md): Concepts behind the agents referenced by `ai.agent`.
- [Add events to a conversation with the API](/explore-analyze/ai-features/agent-builder/kibana-api.md#add-conversation-events): Add the same events from outside a workflow.
