---
navigation_title: "Limitations"
description: "Find limitations and known issues for Agent Builder."
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

# Limitations and known issues in {{agent-builder}}

This section lists the limitations and known issues in {{agent-builder}}.

::::{admonition}
This feature requires the appropriate {{stack}} [subscription](https://www.elastic.co/pricing) or {{serverless-short}} [project feature tier](/deploy-manage/deploy/elastic-cloud/project-settings.md).
::::

## Limitations

:::{tip}
{{agent-builder}} is automatically enabled on all deployment types as of 9.4. For instructions about enabling {{agent-builder}} in earlier versions, refer to [Get started](get-started.md#access-agent-builder).
:::

### Cross-cluster search support

In version 9.4+, [index search tools](tools/index-search-tools.md) support [cross-cluster search (CCS)](/explore-analyze/cross-cluster-search.md). Index search tools only search remote clusters when you explicitly configure a cross-cluster pattern like `remote_cluster:logs-*`. Without a remote pattern, the tool resolves indices locally. To learn how to configure a tool for remote clusters, refer to [Index search tools](tools/index-search-tools.md#common-patterns).

In previous versions, only [{{esql}} tools](tools/esql-tools.md) support CCS. To search remote clusters, use a custom {{esql}} tool and instruct your agent to query `remote_cluster:index_name`.

### A2A streaming not supported

The [A2A server](a2a-server.md) does not currently support streaming operations. All agent interactions use the synchronous `message/send` method, which returns a complete response only after task execution completes.

### Human-in-the-loop prompts require an interactive conversation

[Human-in-the-loop prompts](chat.md#human-in-the-loop-prompts) are supported only in interactive {{agent-builder}} conversations. Standalone sub-agent executions, whether foreground or background, cannot collect a response to these prompts, so actions that require confirmation or authorization are declined. A2A clients also cannot respond to {{agent-builder}} HITL prompts.

This limitation is separate from the [`waitForInput`](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md) step in Workflows, which pauses a workflow execution for reviewer input.

### {{esql}} limitations

{{esql}} tools are subject to the current limitations of the [{{esql}} language](elasticsearch://reference/query-languages/esql.md).

Ensure your cluster version supports the {{esql}} features you intend to use.

For a complete list of {{esql}} limitations, refer to the [{{esql}} limitations documentation](elasticsearch://reference/query-languages/esql/limitations.md).

## Known issues

### Troubleshoot incompatible LLMs

The following errors suggest your selected model may not be compatible with {{agent-builder}}:

```console-response
Error: Invalid function call syntax
```

```console-response
Error executing agent: No tool calls found in the response.
```

To learn more, refer to [](models.md).

### Claude 4.6 Sonnet may generate invalid ES|QL for dashboards

Current testing shows that Claude 4.6 Sonnet may generate invalid {{esql}} for dashboard and visualization workflows, particularly with reserved keywords, dotted field names such as `system.load.1`, and incorrectly formatted aliases.

**Workaround:** Use a higher-tier model, such as Claude 4.6 Opus, for {{esql}}-heavy dashboard generation. To learn more, refer to [Recommended models](models.md#recommended-models).

### Context length exceeded error [conversation-length-exceeded]

This error occurs when a conversation exceeds the maximum context length supported by the LLM. This typically happens when tools return large responses that consume the available token budget.

To learn more, refer to [Context length exceeded in {{agent-builder}} conversations](troubleshooting/context-length-exceeded.md).

### Misinterpreted SQL syntax as ES|QL

The `.execute_esql` tool is designed only for [{{esql}}](elasticsearch://reference/query-languages/esql.md) syntax, not other query languages.

When using SQL syntax with the default agent, it attempts to use the `.execute_esql` tool instead of recognizing the input as SQL.

This results in parsing errors like this:
```console-response
[
  {
    "type": "error",
    "data": {
      "message": "parsing_exception\n\tCaused by:\n\t\tinput_mismatch_exception: null\n\tRoot causes:\n\t\tparsing_exception: line 1:15: mismatched input 'WHERE' expecting {<EOF>, '|', ',', 'metadata'}",
      "stack": "ResponseError: parsing_exception\n\tCaused by:\n\t\tinput_mismatch_exception: null\n\tRoot causes:\n\t\tparsing_exception: line 1:15: mismatched input 'WHERE' expecting {<EOF>, '|', ',', 'metadata'}\n    at KibanaTransport._request (Desktop/Dev/kibana/node_modules/@elastic/elasticsearch/node_modules/@elastic/transport/src/Transport.ts:591:17)\n    at processTicksAndRejections (node:internal/process/task_queues:105:5)\n    at Desktop/Dev/kibana/node_modules/@elastic/elasticsearch/node_modules/@elastic/transport/src/Transport.ts:697:22\n    at KibanaTransport.request (Desktop/Dev/kibana/node_modules/@elastic/elasticsearch/node_modules/@elastic/transport/src/Transport.ts:694:14)"
    }
  }
]
```

### MCP server URL copy button omits space name

:::{note}
Fixed on serverless and 9.3.
:::

On 9.2 deployments, the **Copy your MCP server URL** button does not include the space name when used from a custom {{kib}} Space.

**Workaround:** Manually add `/s/<space-name>` to the URL. For example: `https://<deployment>/s/<space-name>/api/agent_builder/mcp`

For more information about {{agent-builder}} and Spaces, refer to [Permissions and access control](permissions.md#working-with-spaces).


## Related pages

- [Get started](get-started.md)
- [Troubleshooting](troubleshooting.md)
