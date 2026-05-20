---
navigation_title: AI
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Reference for the four AI step types (prompt, classify, summarize, and agent) that bring LLM calls into workflows.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# AI steps [workflows-ai-steps]

AI steps let workflows call a large language model (LLM) for reasoning, classification, summarization, or agent-driven execution. All four AI step types share a connector-based auth model: configure a generative AI connector in {{kib}}, then reference it by ID from a workflow step. When `connector-id` is omitted, the default connector configured for the workflow is used.

## Step types

- [`ai.prompt`](#ai-prompt): Send a prompt to a model and receive a response. Supports structured output with a JSON Schema. {applies_to}`stack: preview 9.3, ga 9.4+`
- [`ai.classify`](#ai-classify): Classify input into a fixed set of categories. {applies_to}`stack: ga 9.4+`
- [`ai.summarize`](#ai-summarize): Generate a summary of the provided content. {applies_to}`stack: ga 9.4+`
- [`ai.agent`](#ai-agent): Invoke an {{agent-builder}} agent as a workflow step. {applies_to}`stack: preview 9.3, ga 9.4+`

:::{important}
`connector-id`, `agent-id`, and `inference-id` are **top-level step fields** (alongside `name`, `type`, `if`, `foreach`), written in **kebab-case**. They are not nested under `with`, and not `connectorId`. Inside `with`, most AI parameters use `camelCase` (`systemPrompt`, `maxLength`, `includeRationale`). Authentication-style references stay at the top level in kebab-case; content parameters stay inside `with` in camelCase.
:::

## `ai.prompt` [ai-prompt]

```{applies_to}
stack: preview 9.3, ga 9.4+
```

Call an LLM with a prompt. Supports optional structured output through a JSON Schema.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `connector-id` | top level | string | No | The GenAI connector to use. Defaults to the workflow's default connector if omitted. |
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
| `connector-id` | top level | string | No | GenAI connector to use. |
| `input` | `with` | string, array, or object | Yes | Input to classify. |
| `categories` | `with` | `string[]` | Yes | Allowed categories. At least one required. |
| `instructions` | `with` | string | No | Guidance for the classifier. |
| `allowMultipleCategories` | `with` | boolean | No | Allow the output to include more than one category. |
| `fallbackCategory` | `with` | string | No | Category returned when the model can't confidently choose. |
| `includeRationale` | `with` | boolean | No | Include the model's reasoning in the output. |
| `temperature` | `with` | number (0–1) | No | Model temperature. |

**Output shape:**

| Field | Type | Presence |
|---|---|---|
| `category` | string | Present when `allowMultipleCategories` is false (default). |
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

## `ai.summarize` [ai-summarize]

```{applies_to}
stack: ga 9.4+
```

Summarize content with an LLM. Input can be a string, an array, or an object.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `connector-id` | top level | string | No | GenAI connector to use. |
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
| `connector-id` | top level | string | No | GenAI connector. Mutually exclusive with `inference-id`. |
| `inference-id` | top level | string | No | Inference endpoint ID. Mutually exclusive with `connector-id`. |
| `create-conversation` | top level | boolean | No | When `true`, persist the conversation for follow-up steps or later reference. |
| `message` | `with` | string | Yes | User message to send to the agent. |
| `schema` | `with` | object | No | JSON Schema for structured output. |
| `conversation_id` | `with` | string | No | Continue an existing conversation by ID. |
| `attachments` | `with` | array | No | Attachments to provide to the agent. Each attachment has `{ id?, type, data?, origin?, hidden? }`. |

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

## Related

- [Configured AI connectors](/deploy-manage/manage-connectors.md): Set up the GenAI connector referenced by `connector-id`.
- [Switch step](/explore-analyze/workflows/steps/switch.md): A common pairing: classify with `ai.classify`, then dispatch with `switch`.
- [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md): Pair AI classifications with a reviewer gate for uncertain cases.
- [{{agent-builder}} overview](/explore-analyze/ai-features/elastic-agent-builder.md): Concepts behind the agents referenced by `ai.agent`.
