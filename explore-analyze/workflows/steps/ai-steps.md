---
navigation_title: AI
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Call LLMs, run Agent Builder agents, and manage the attachments and metadata of agent conversations from workflows with AI steps. This reference lists each step's parameters, output, and examples.
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

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` AI steps can also read and update the metadata and attachments of {{agent-builder}} conversations.

The `ai.prompt`, `ai.classify`, `ai.summarize`, and `ai.agent` steps reference a model by ID from the workflow step: configure a Generative AI connector in {{kib}} and pass `connector-id`, or, for [`ai.agent`](#ai-agent), pass `inference-id` with an {{infer}} endpoint ID instead. When you omit both, the step uses the workflow's default model.

:::{note}
:applies_to: { serverless: deprecated, stack: deprecated 9.5+ }

Generative AI connectors are deprecated. The `ai.agent` step accepts an {{infer}} endpoint through `inference-id`. The `ai.prompt`, `ai.classify`, and `ai.summarize` steps take `connector-id` only.
:::

## Step types

- [`ai.prompt`](#ai-prompt): Send a prompt to a model and receive a response. Supports structured output with a JSON Schema. {applies_to}`stack: preview 9.3, ga 9.4+`
- [`ai.classify`](#ai-classify): Classify input into a fixed set of categories. {applies_to}`stack: ga 9.4+`
- [`ai.summarize`](#ai-summarize): Generate a summary of the provided content. {applies_to}`stack: ga 9.4+`
- [`ai.agent`](#ai-agent): Invoke an {{agent-builder}} agent as a workflow step. {applies_to}`stack: preview 9.3, ga 9.4+`
- [`ai.conversation.metadata.read`](#ai-conversation-metadata-read): Read the metadata of a conversation. {applies_to}`stack: ga 9.6+`
- [`ai.conversation.metadata.patch`](#ai-conversation-metadata-patch): Update the metadata of a conversation. {applies_to}`stack: ga 9.6+`
- [`ai.attachment.add`](#ai-attachment-add): Add an attachment to a conversation. {applies_to}`stack: ga 9.6+`
- [`ai.attachment.update`](#ai-attachment-update): Update an attachment in a conversation. {applies_to}`stack: ga 9.6+`
- [`ai.attachment.delete`](#ai-attachment-delete): Delete an attachment from a conversation. {applies_to}`stack: ga 9.6+`
- [`ai.attachment.read`](#ai-attachment-read): Read the content of an attachment. {applies_to}`stack: ga 9.6+`
- [`ai.attachment.list`](#ai-attachment-list): List the attachments in a conversation. {applies_to}`stack: ga 9.6+`

In `ai.prompt`, `ai.classify`, `ai.summarize`, and `ai.agent`, the `connector-id`, `agent-id`, and `inference-id` fields are **top-level step fields** (alongside `name`, `type`, `if`, `foreach`) in **kebab-case**. They aren't nested under `with`, and they aren't `connectorId`. Inside `with`, most of their parameters use `camelCase` (`systemPrompt`, `maxLength`, `includeRationale`).

::::{applies-switch}
:::{applies-item} { stack: ga 9.5, serverless: ga }
Liquid expressions are evaluated in these top-level fields, so you can use templated values (for example, `"{{ consts.agent_id }}"`).
:::
:::{applies-item} stack: ga 9.3-9.4
Liquid expressions in these top-level fields aren't evaluated, so use a literal value (for example, `agent-id: elastic-ai-agent`) instead of `"{{ consts.agent_id }}"`.
:::
::::

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` The [conversation metadata](#ai-conversation-metadata-steps) and [conversation attachment](#ai-attachment-steps) steps take all their parameters inside `with`, in `snake_case`.

:::{include} ../_snippets/schema-location-legend.md
:::

## `ai.prompt` [ai-prompt]

```{applies_to}
stack: preview 9.3, ga 9.4+
```

Call an LLM with a prompt. Supports optional structured output through a JSON Schema.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `connector-id` | top level | string | No | The Generative AI connector to use. Defaults to the workflow's default connector if omitted. |
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

## Conversation metadata steps [ai-conversation-metadata-steps]

```{applies_to}
stack: ga 9.6+
serverless: ga
```

Read and update the metadata of an {{agent-builder}} conversation. Metadata is a set of structured fields, such as `status` or `severity`, defined by the template applied to the conversation. Use these steps to branch a workflow on a field value, or to record the outcome of a workflow on the conversation.

Only conversations with a template have metadata:

- Conversations that `ai.agent` creates, or that users start in chat, have no template.
- To create a conversation with a template from a workflow, use `ai.conversation.create` with `template_id` set to a built-in template: `investigation` or `escalation`.

The examples in this section use the `investigation` template, where `status` accepts `open` or `closed`.

:::{note}
These steps run with the privileges of the user who authorizes the run. That user needs:

- Access to the conversation: they own it, are a member of it, or the conversation is public.
- Access to the agent the conversation uses.

Otherwise, the step fails with a `Conversation <id> not found` error. To find out which user authorizes a run, refer to [Workflow authorization](/explore-analyze/workflows/authorization.md#workflows-authorization-user).
:::

### `ai.conversation.metadata.read` [ai-conversation-metadata-read]

Read all metadata fields of a conversation.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation to read the metadata from. |

**Output shape:** `{ metadata: object }`. The current metadata fields and their values. Empty if the conversation has no metadata.

```yaml
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

The conversation must have a template applied. In addition:

- You can only set fields that the template defines.
- Each value must match the type and constraints of its field, such as the allowed options of a select field.
- You can't set a field to `null`.

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

```yaml
- name: resolve_investigation
  type: ai.conversation.metadata.patch
  with:
    conversation_id: "{{ inputs.conversation_id }}"
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

Add, update, delete, read, and list the attachments of an {{agent-builder}} conversation. Each attachment has a type, such as `text`, and keeps a version history of its content.

All parameters go in the `with` block and use `snake_case`. Every attachment step takes the `conversation_id` of the conversation the attachment belongs to.

The examples in this section use the conversation created by the `investigate` step in [Example: Call an agent](#example-call-an-agent).

These steps follow the same access rules as the [conversation metadata steps](#ai-conversation-metadata-steps): the user who authorizes the run must be able to access the conversation.

### `ai.attachment.add` [ai-attachment-add]

Add an attachment to a conversation.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation to add the attachment to. |
| `type` | `with` | string | Yes | Attachment type, such as `text`. The step fails if the type doesn't exist. |
| `data` | `with` | any | Depends | Attachment content. Its shape depends on `type`. For `text`, use `{ content: "<text>" }`. Required unless you set `origin`. |
| `origin` | `with` | string | Depends | Reference to the object the content comes from, such as a dashboard ID, up to 2,048 characters. Required unless you set `data`. |
| `id` | `with` | string | No | Attachment ID, up to 256 characters. Generated if omitted. The step fails if the conversation already has an attachment with this ID. |
| `description` | `with` | string | No | Description of the attachment, up to 1,024 characters. |
| `hidden` | `with` | boolean | No | When `true`, the attachment isn't shown to the user, but the agent can still use it. A hidden attachment is never displayed inline. |
| `render_inline` | `with` | boolean | No | When `true`, the attachment is displayed as soon as a user opens the conversation, even if the agent doesn't refer to it. Defaults to `false`. |

If you set `origin` without `data`, the content is loaded once, when the attachment is created. Not all attachment types support `origin`. For example, `text` doesn't.

**Output shape:**

| Field | Type | Presence |
|---|---|---|
| `attachment_id` | string | Always. |
| `type` | string | Always. |
| `current_version` | number | Always. `1` for a new attachment. |

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

Delete an attachment from a conversation. By default, the step marks the attachment inactive but keeps it, so you can still list it with `include_deleted: true`. To remove the attachment completely, set `permanent: true`.

A permanent deletion fails if the agent has already read, updated, or compared versions of the attachment in the conversation. A regular deletion still works in that case.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `conversation_id` | `with` | string | Yes | Conversation the attachment belongs to. |
| `attachment_id` | `with` | string | Yes | Attachment to delete. |
| `permanent` | `with` | boolean | No | When `true`, removes the attachment completely. Defaults to `false`. |

**Output shape:** `{ success: boolean, permanent: boolean }`.

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
| `total_token_estimate` | number | Always. Estimated number of tokens across the active attachments. Deleted attachments aren't counted, even with `include_deleted: true`. |

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
