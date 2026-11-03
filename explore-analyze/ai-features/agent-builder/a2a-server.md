---
navigation_title: "A2A server"
description: "Learn how to interact with Agent Builder agents from external clients using A2A protocol endpoints and API key authentication."
applies_to:
  stack: preview =9.2, ga 9.3+
  serverless:
    elasticsearch: ga
    observability: ga
    security: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
  - id: cloud-serverless
---

# Agent-to-Agent (A2A) server in {{agent-builder}}

The [**Agent-to-Agent (A2A) server**](https://github.com/a2aproject/A2A) enables external A2A clients, such as other agent frameworks, to communicate with {{agent-builder}} agents. This page covers the A2A endpoints and how to send messages, poll for results, and stream responses.

## Retrieve agent metadata (GET)

Returns the agent card for a specific agent. The agent card is the agent's metadata, including its capabilities. The `agentId` is a path parameter that corresponds to your agent IDs:

```
GET /api/agent_builder/a2a/{agentId}.json
```

## Execute A2A protocol (POST)

Interact with agents following the A2A protocol specification:

```
POST /api/agent_builder/a2a/{agentId}
```

:::{important}
Both A2A endpoints require API key authentication. Refer to [Create a read-only client key](api-keys.md#create-a-read-only-client-key) for a limited key example. For more information about the A2A protocol, refer to the [A2A protocol specification](https://a2aprotocol.ai/docs/guide/a2a-protocol-specification-python#protocol-flow-diagram).
:::

### Send messages

By default, `message/send` waits until the agent finishes, then returns the complete agent message in a single response.

### Send messages without waiting

```{applies_to}
stack: ga 9.4+
serverless: ga
```

On 9.4, this requires 9.4.5 or later.

To get a response before the agent finishes, poll for the result:

1. Send `message/send` with `configuration.blocking` set to `false`. The response is a task in the `working` state.
2. Send `tasks/get` with the task ID. Repeat until the task reaches a final state: `completed`, `failed`, or `canceled`. While the task is queued, `tasks/get` can report `submitted`.
3. Read the task's `status.message`. If the task is `completed`, it contains the agent's response. If the task `failed`, it contains the error.

### Stream responses

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.6+", "serverless": "ga" }

Send `message/stream` to receive the response as a server-sent event (SSE) stream. The [agent card](#retrieve-agent-metadata-get) reports streaming support by setting `capabilities.streaming` to `true`.

The stream sends [A2A streaming events](https://a2a-protocol.org/v0.3.0/topics/streaming-and-async/) in this order:

1. A task in the `working` state.
2. While the agent works:
   * Artifact updates that contain the agent's response text.
   * Status updates in the `working` state that report progress, such as tool calls.
3. A final status update in the `completed`, `failed`, or `input-required` state.

The `input-required` state means the agent is waiting for a response to a prompt, which A2A clients can't send. Refer to [Human-in-the-loop prompts require an interactive conversation](limitations-known-issues.md#human-in-the-loop-prompts-require-an-interactive-conversation).

If the client disconnects before the stream ends, the agent stops.

In [a2a-inspector](https://github.com/a2aproject/a2a-inspector) 0.2.0 and later, the **Stream** checkbox is selected by default when the agent card reports streaming. Earlier versions stream automatically.
:::

:::{applies-item} { "stack": "preview =9.2, ga 9.3-9.5" }

Streaming isn't supported. Use [`message/send`](#send-messages) instead. Refer to [Limitations and known issues](limitations-known-issues.md#a2a-streaming-not-supported).
:::

::::
