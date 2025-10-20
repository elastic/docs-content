---
navigation_title: "Limitations & known issues"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

:::{warning}
These pages are currently hidden from the docs TOC and have `noindexed` meta headers.

**Go to the docs [landing page](/solutions/search/elastic-agent-builder.md).**
:::

# Limitations and known issues in {{agent-builder}}

## Limitations

### Agent Builder not enabled by default

{{agent-builder}} must be enabled for non-serverless deployments {applies_to}`stack: preview 9.2`. Refer to [Get started](get-started.md#enable-agent-builder) for instructions.

### Model selection

Initially, {{agent-builder}} only supports working with the [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) running on the [Elastic Inference Service](/explore-analyze/elastic-inference/eis.md) {applies_to}`stack: preview 9.2`.

Learn about [pricing](https://www.elastic.co/pricing/serverless-search) for the Elastic Managed LLM.

## Known issues

### Incompatible LLMs

While Elastic offers LLM [connectors](kibana://reference/connectors-kibana.md) for many different vendors and models, not all LLMs are robust enough to be used with {{agent-builder}}. We recommend using the [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) (the default).

The following errors suggest your selected model may not be compatible with {{agent-builder}}:

```console-response
Error: Invalid function call syntax
```

```console-response
Error executing agent: No tool calls found in the response.
```

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

    