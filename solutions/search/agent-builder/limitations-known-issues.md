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

Initially, {{agent-builder}} only supports working with the [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) running on the Elastic Inference Service, on {{ech}} and {{serverless-full}}. 

Locally this picks the first AI connector available.

## Known issues


- **Default agent can misinterpret SQL syntax as ES|QL**
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

- **Not all LLMs are compatible**
  - While Elastic offers LLM connectors for many different vendors and models, not all LLMs are robust enough to be used with {{agent-builder}}.
  - Errors such as:
    ```console-response
    Error: Invalid function call syntax
    ```
    or
    ```
    Error executing agent: No tool calls found in the response.
    ```
    may indicate that your selected model is ill-equipped for the precise response structure necessary for {{agent-builder}}.
  - We recommend using the [Elastic Managed LLM](kibana://reference/connectors-kibana/elastic-managed-llm.md) 

- **{{agent-builder}} is not accessible**
  - {{agent-builder}} was added in a private preview in September, 2025 for Serverless, and in 9.2.0 for Elastic Cloud.
  - While in this preview stage, {{agent-builder}} is not enabled by default.
  - To enable it, you must go to Stack Management -> Kibana -> Advanced Settings -> Elastic Agent Builder, and enable it.

    