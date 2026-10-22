---
navigation_title: AI
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Call LLMs, run Agent Builder agents, and add context to agent conversations from workflows with AI steps. This reference lists each step's parameters, output, and examples.
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

{applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview` AI steps can also create {{agent-builder}} conversations and add content to them without triggering an agent response.

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

Generative AI connectors are deprecated. The `ai.agent` step accepts an {{infer}} endpoint through `inference-id`; the other AI steps currently take `connector-id` only.
:::

## Step types

- [`ai.prompt`](#ai-prompt): Send a prompt to a model and receive a response. Supports structured output with a JSON Schema. {applies_to}`stack: preview 9.3, ga 9.4+`
- [`ai.classify`](#ai-classify): Classify input into a fixed set of categories. {applies_to}`stack: ga 9.4+`
- [`ai.summarize`](#ai-summarize): Generate a summary of the provided content. {applies_to}`stack: ga 9.4+`
- [`ai.agent`](#ai-agent): Invoke an {{agent-builder}} agent as a workflow step. {applies_to}`stack: preview 9.3, ga 9.4+`
- [`ai.conversation.create`](#ai-conversation-create): Create an empty {{agent-builder}} conversation. {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview`
- [`ai.conversation.add_event`](#ai-conversation-add-event): Add an event, such as a note, to a conversation without triggering an agent response. {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview`
- [`ai.conversation.add_user_message`](#ai-conversation-add-user-message): Add a user message to a conversation without triggering an agent response. {applies_to}`stack: preview 9.6+` {applies_to}`serverless: preview`

For `ai.prompt`, `ai.classify`, `ai.summarize`, and `ai.agent`, `connector-id`, `agent-id`, and `inference-id` are **top-level step fields** (alongside `name`, `type`, `if`, `foreach`) and are written in **kebab-case**. They are not nested under `with`, and not `connectorId`. Inside `with`, most of their parameters use `camelCase` (`systemPrompt`, `maxLength`, `includeRationale`). The conversation steps have no top-level fields and use `snake_case` inside `with`.

::::{applies-switch}
:::{applies-item} { stack: ga 9.5, serverless: ga }
Liquid expressions are evaluated in these top-level fields, so you can use templated values (for example, `"{{ consts.agent_id }}"`).
:::
:::{applies-item} stack: ga 9.3-9.4
Liquid expressions in these top-level fields aren't evaluated, so use a literal value (for example, `agent-id: elastic-ai-agent`) instead of `"{{ consts.agent_id }}"`.
:::
::::

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
| `message` | `with` | string | Yes | User message to send to the agent. |
| `schema` | `with` | object | No | JSON Schema for structured output. |
| `conversation_id` | `with` | string | No | Continue an existing conversation by ID. |
| `attachments` | `with` | array | No | Attachments to provide to the agent. Each attachment has `{ id?, type, data?, origin?, hidden? }`. |

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` The step ignores `public-conversation` if `create-conversation` isn't `true`, or if it continues an existing conversation instead of creating one. Neither case returns an error.

**Output shape:**

| Field | Type | Presence |
|---|---|---|
| `message` | string | Always. Text response, or a string representation when `schema` is provided. |
| `structured_output` | any | Present when `schema` is provided. |
| `conversation_id` | string | Present when `create-conversation: true` or `conversation_id` was provided. |

:::{important}
Use `connector-id` **or** `inference-id`, not both. The schema rejects a step that sets both.
:::

### Example: Call an agent

```yaml
- name: investigate
  type: ai.agent
  agent-id: "security-analyst-agent"
  connector-id: "my-openai"
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
| `template_id` | `with` | string | No | ID of a conversation template to apply. Templates are defined by {{kib}} features, and you can't create your own. The template sets default metadata for the conversation. The step fails if the template doesn't exist. |
| `metadata` | `with` | object | No | Initial metadata values. Requires `template_id`, and each key must be defined by the template. Up to 100 keys. Each value can be a string (up to 10,000 characters), a number, a boolean, or an array of up to 100 strings (up to 2,000 characters each). |

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

## `ai.conversation.add_event` [ai-conversation-add-event]

```{applies_to}
stack: preview 9.6+
serverless: preview
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
stack: preview 9.6+
serverless: preview
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

## Related

- [Configured AI connectors](/deploy-manage/manage-connectors.md): Set up the Generative AI connector referenced by `connector-id`.
- [Switch step](/explore-analyze/workflows/steps/switch.md): A common pairing: classify with `ai.classify`, then dispatch with `switch`.
- [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md): Pair AI classifications with a reviewer gate for uncertain cases.
- [{{agent-builder}} overview](/explore-analyze/ai-features/elastic-agent-builder.md): Concepts behind the agents referenced by `ai.agent`.
- [Add events to a conversation with the API](/explore-analyze/ai-features/agent-builder/kibana-api.md#add-conversation-events): Add the same events from outside a workflow.
