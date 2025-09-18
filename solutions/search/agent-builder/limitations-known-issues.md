---
navigation_title: "Limitations & known issues"
applies_to:
  stack: preview 9.2
  serverless:
    elasticsearch: preview
---

:::{warning}
WIP

These pages are hidden from the docs TOC and have `noindexed` meta headers.
:::

# Limitations and known issues in {{agent-builder}}

## Model selection

Initally, {{agent-builder}} only supports working with the [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) running on the Elastic Inference Service which uses Claude Sonnet 3.7, on {{ech}} and {{serverless-full}}. 

Locally this picks the first AI connector available.

Initally, there are no UI controls to select which connector (and therefore which model) to use.

## Known issues


- **Default agent misinterprets SQL syntax as ES|QL**
  - The `.execute_esql` tool is designed only for [{{esql}}](elasticsearch://reference/query-languages/esql.md) syntax, not other query languages
  - When using SQL syntax with the default agent, it attempts to use the `.execute_esql` tool instead of recognizing the input as SQL
  - This results in parsing errors like this:
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

