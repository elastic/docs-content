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

The [**Agent-to-Agent (A2A) server**](https://github.com/a2aproject/A2A) enables external A2A clients, such as other agent frameworks, to communicate with {{agent-builder}} agents.

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

In 9.2 through 9.5, `message/stream` isn't supported. Refer to [Limitations and known issues](limitations-known-issues.md#a2a-streaming-not-supported).

### Send messages without waiting

```{applies_to}
stack: ga 9.4+
serverless: ga
```

In 9.4, non-blocking requests require version 9.4.5 or later. On earlier versions, `configuration.blocking: false` is ignored and the request waits for the complete response.

To get a response without waiting for the agent to finish, call `message/send` with `configuration.blocking` set to `false`. The response is a task. Poll it with `tasks/get` until it reaches a final state, then read `status.message`, which contains the agent's response or, if the task failed, the error. For the task states, refer to the [A2A protocol specification](https://a2a-protocol.org/v0.3.0/topics/life-of-a-task/).

### Stream responses

```{applies_to}
stack: ga 9.6+
serverless: ga
```

Call the `message/stream` method to receive the response as a stream of server-sent events. The [agent card](#retrieve-agent-metadata-get) reports streaming support by setting `capabilities.streaming` to `true`.

The stream uses the [A2A streaming events](https://a2a-protocol.org/v0.3.0/topics/streaming-and-async/). Artifact updates contain the agent's response text, and status updates in the `working` state report progress, such as tool calls. The final status update is `completed`, `failed`, or `input-required`.

The `input-required` state means the agent is waiting for a response to a prompt, which A2A clients can't send. Refer to [Human-in-the-loop prompts require an interactive conversation](limitations-known-issues.md#human-in-the-loop-prompts-require-an-interactive-conversation).

If the client disconnects before the stream ends, the agent stops.
