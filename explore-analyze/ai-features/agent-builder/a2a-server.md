---
navigation_title: "A2A server"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
---

# Agent-to-Agent (A2A) server

The [**Agent-to-Agent (A2A) server**](https://github.com/a2aproject/A2A) enables external A2A clients to communicate with {{agent-builder}} agents.

:::{note}
Streaming operations are not currently supported. Refer to [Limitations and known issues](limitations-known-issues.md#a2a-streaming-not-supported) for more information.
:::

## Agent cards endpoint

Returns metadata for a specific agent. The `agentId` is a path parameter that corresponds to your agent IDs:

```
GET /api/agent_builder/a2a/{agentId}.json
```

## A2A protocol endpoint

Interact with agents following the A2A protocol specification:

```
POST /api/agent_builder/a2a/{agentId}
```

:::{important}
Both A2A endpoints require API key authentication. For more information about the A2A protocol, refer to the [A2A protocol specification](https://a2aprotocol.ai/docs/guide/a2a-protocol-specification-python#protocol-flow-diagram).
:::
