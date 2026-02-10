---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Learn about AI steps for integrating AI capabilities into your workflows.
---

# AI steps

AI steps allow your workflows to interact with AI services and Elastic AI agents. Use them to analyze data, generate insights, make context-aware decisions, and automate intelligent responses.

The following AI step types are available:

* **Prompt** (`ai.prompt`): Send prompts to [AI connectors](kibana://reference/connectors-kibana/gen-ai-connectors.md) (such as OpenAI or Google Gemini)
* **Agent** (`ai.agent`): Invoke Elastic AI agents built in Agent Builder

## Prompt

The `ai.prompt` step sends a prompt to an AI connector and returns the response. Use this step to:

* Summarize or interpret data
* Extract insights from unstructured text
* Make context-aware decisions based on data in your workflow
* Generate structured output based on a defined schema

All AI connectors are configured and managed separately through {{kib}}'s {{connectors-ui}} framework. Before using this step, you must first [configure an AI connector](/deploy-manage/manage-connectors.md).

### Parameters

Use the following parameters in the `with` block to configure the step:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The prompt text to send to the AI connector. Can include template variables to reference data from previous steps, inputs, or constants. |
| `connectorId` | string | No | The ID or name of the AI connector to use. If omitted, uses the [default AI connector](/explore-analyze/ai-features/manage-access-to-ai-assistant.md#the-genai-settings-page). |
| `outputSchema` | object | No | A JSON Schema object that defines the structure of the expected response. When provided, the AI connector returns structured data matching the schema. |
| `temperature` | number | No | Controls randomness in the AI response. Accepts values from `0` to `1` (for example, `0.3`). Lower values produce more deterministic responses; higher values produce more random responses. |

### Output structure

The `ai.prompt` step produces output in the following structure:

```yaml
content: <response>  # String or structured object if outputSchema is provided
response_metadata: <metadata>  # Optional metadata from the connector
```

Reference the output in subsequent steps using `steps.<step_name>.output.content`.

### Example: Analyze an alert

This example sends an alert to an AI connector for severity analysis.

```yaml
steps:
  - name: analyze_alert
    type: ai.prompt
    with:
      prompt: "Analyze this security alert and determine its severity: {{ event | json }}"
      connectorId: "my-openai-connector"
```

### Example: Structured output with schema

This example uses `outputSchema` to return a structured response with specific fields and types.

```yaml
steps:
  - name: categorize_alert
    type: ai.prompt
    with:
      prompt: "Analyze this alert and categorize it: {{ event | json }}"
      connectorId: "security-analysis-connector"
      outputSchema:
        type: object
        properties:
          severity:
            type: string
            enum: [low, medium, high, critical]
          category:
            type: string
          requires_human_review:
            type: boolean
      temperature: 0.3
```

## Agent

The `ai.agent` step invokes an Elastic AI agent built using {{agent-builder}}. The agent processes the input message and returns a response, optionally using tools and maintaining conversation context. Use this step to invoke an agent as a "reasoning engine" that summarizes data, classifies events, or makes decisions before passing the results to the next step in your automation.

For detailed configuration options and examples, refer to [Work with AI agents in Elastic Workflows](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md#use-the-ai.agent-step).
