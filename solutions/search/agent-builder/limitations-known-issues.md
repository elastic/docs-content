---
navigation_title: "Limitations & known issues"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
    observability: unavailable
    security: unavailable
---

# Limitations and known issues in {{agent-builder}}

## Limitations

### Feature availability

#### Non-serverless deployments

{{agent-builder}} is enabled by default in {{serverless-full}} for {{es}} projects.

However, it must be enabled for non-serverless deployments {applies_to}`stack: preview 9.2`. Refer to [Get started](get-started.md#enable-agent-builder) for instructions.

#### Serverless deployments

In the first release of {{agent-builder}} on serverless, the feature is **only available on {{es}} projects**.

## Known issues

### Incompatible LLMs

While Elastic offers LLM [connectors](kibana://reference/connectors-kibana.md) for many different vendors and models, not all LLMs are robust enough to be used with {{agent-builder}}. We recommend using the [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) (the default). Learn more in [](models.md).

The following errors suggest your selected model may not be compatible with {{agent-builder}}:

```console-response
Error: Invalid function call syntax
```

```console-response
Error executing agent: No tool calls found in the response.
```

$$$conversation-length-exceeded$$$

### {{esql}} limitations

{{esql}} tools are subject to the current limitations of the {{esql}} language itself. For example, [named parameters](elasticsearch://reference/query-languages/esql/esql-syntax.md#esql-function-named-params) (`?parameter_name`) do not currently work with the `LIKE` and `RLIKE` operators ([issue #131356](https://github.com/elastic/elasticsearch/issues/131356)).

For non-serverless deployments, ensure your cluster supports the {{esql}} features you intend to use.

For a complete list of {{esql}} limitations, refer to the the [{{esql}} limitations documentation](elasticsearch://reference/query-languages/esql/limitations.md).

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


