---
navigation_title: "Retrieve context"
description: Retrieve Knowledge Indicators from an AI index through the Context Engine APIs or tools.
type: how-to
applies_to:
  stack: experimental 9.6
  serverless: experimental
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# Retrieve context from an AI index

:::{include} _snippets/hidden-docs-notice.md
:::

Query an AI index to retrieve its Knowledge Indicators (KIs) as context for an agent or application. You can call the {{context-engine}} APIs directly. Agent integrations can expose tools that perform the list, describe, and query sequence.

## Before you begin

To query an AI index, you need:

- The `contextEngine:enabled` advanced setting turned on in the {{kib}} space you want to query.
- At least one AI index that contains KIs.
- The {{context-engine}} **Read** privilege in that space.
- The {{es}} `read` and `view_index_metadata` privileges for the AI index's backing indices.

For direct API access, you also need credentials for the caller. The examples on this page use an API key.

## How to query AI indices

Choose a query mode based on whether your code or an agent controls the retrieval sequence:

| Query mode | Use it when |
| --- | --- |
| [{{context-engine}} APIs](#query-with-apis) | Your application or script manages the retrieval sequence and constructs the {{esql}} query. |
| [{{context-engine}} tools](#query-with-tools) | An agent decides when to retrieve context and calls tools that wrap the list, describe, and query operations. |

## Query with APIs [query-with-apis]

Run the requests from [{{kib}} Console](/explore-analyze/query-filter/tools/console.md) or use cURL from an application environment. Console uses your current session and {{kib}} space.

<!--
Claude Code can use the {{context-engine}} skill to perform the same sequence through the `elastic` CLI, which calls the {{context-engine}} APIs. For setup instructions, refer to [Use {{context-engine}} with Claude Code](use-context-engine-with-claude-code.md).
-->

For cURL, set the {{kib}} URL and encoded API key used by the examples:

```bash
export KIBANA_URL="https://my-deployment.kb.us-east-1.aws.elastic.cloud"
export KIBANA_API_KEY="VnVhQ2ZHY0JDZGJrU..."
```

For a non-default space, include `/s/<space-id>` at the end of `KIBANA_URL` in the cURL examples.

### 1. List AI indices

Use the [list AI indices API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-context-engine-ai-index) to retrieve the AI indices that the caller can read:

::::{tab-set}
:group: context-engine-api-client
:::{tab-item} Console
:sync: console
```console
GET kbn:/api/context_engine/ai_index
```
:::
:::{tab-item} cURL
:sync: curl
```bash
curl -X GET "${KIBANA_URL}/api/context_engine/ai_index" \
  -H "Authorization: ApiKey ${KIBANA_API_KEY}" \
  -H "elastic-api-version: 2023-10-31"
```
:::
::::

Use each entry's `description` to determine whether the AI index is relevant. Keep its `id` for the describe request. The response also contains `dest.value`, which is the exact {{esql}} target for the AI index.

An AI index is omitted when the caller cannot read its backing index. It can still appear before an automation has written any KIs to its backing index.

### 2. Describe an AI index

Use the [describe AI index API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-context-engine-ai-index-aiindexid-describe) before constructing a query:

::::{tab-set}
:group: context-engine-api-client
:::{tab-item} Console
:sync: console
```console
GET kbn:/api/context_engine/ai_index/customer_support/_describe
```
:::
:::{tab-item} cURL
:sync: curl
```bash
export AI_INDEX_ID="customer_support"

curl -X GET "${KIBANA_URL}/api/context_engine/ai_index/${AI_INDEX_ID}/_describe" \
  -H "Authorization: ApiKey ${KIBANA_API_KEY}" \
  -H "elastic-api-version: 2023-10-31"
```
:::
::::

The `response` field contains a context block with the AI index's purpose, {{esql}} target, fields, semantic fields, KI types, tags, and example queries. Use its target and field names verbatim. Fields can differ between AI indices.

### 3. Query the AI index

Construct an {{esql}} query from the describe response and submit it with the [query AI indices API](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-context-engine-ai-index-query). The following example filters an AI index for KIs of type `faq`:

::::{tab-set}
:group: context-engine-api-client
:::{tab-item} Console
:sync: console
```console
POST kbn:/api/context_engine/ai_index/_query
{
  "query": "FROM ai-index-ds-customer_support | WHERE type == ?type | KEEP title, description, content, type, tags | LIMIT 10",
  "params": { "type": "faq" },
  "limit": 10
}
```
:::
:::{tab-item} cURL
:sync: curl
```bash
curl -X POST "${KIBANA_URL}/api/context_engine/ai_index/_query" \
  -H "Authorization: ApiKey ${KIBANA_API_KEY}" \
  -H "elastic-api-version: 2023-10-31" \
  -H "kbn-xsrf: true" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "FROM ai-index-ds-customer_support | WHERE type == ?type | KEEP title, description, content, type, tags | LIMIT 10",
    "params": { "type": "faq" },
    "limit": 10
  }'
```
:::
::::

Replace `ai-index-ds-customer_support` and the selected fields with values returned by the describe operation. Pass user-provided values as named parameters instead of adding them directly to the query string.

The query operation applies the current {{kib}} space to the request and returns only documents visible in that space. Do not add a space condition to the {{esql}} query.

By default, the query operation returns only active, unexpired KIs. For an AI index backed by a data stream, it also returns only the latest revision of each KI. To query deleted or expired KIs, add conditions that reference `governance.lifecycle.status` or `expires_at`. When a query references either field, the operation does not apply the corresponding default filter.

## Query with tools [query-with-tools]

An agent can perform the retrieval sequence when its integration provides access to the list, describe, and query operations. How those operations become available depends on the integration:

- With [{{agent-builder}}](use-context-engine-with-agent-builder.md), assign an AI index to an agent. {{agent-builder}} automatically adds the three tools and retrieval instructions.
- With [LangChain](langchain-integration.md), wrap the three {{context-engine}} API operations as LangChain tools, then provide them to the agent with instructions that establish their order.

<!--
- [Use {{context-engine}} through MCP and skills](use-context-engine-through-mcp-and-skills.md)
-->

In each case, the agent uses the AI index description to select relevant context, constructs {{esql}} from the describe response, and uses the returned KIs to complete the task.

## Verify the results

Confirm the following details across the three operations:

- The list response includes the expected AI index and the description matches the question or task.
- The describe response supplies the expected {{esql}} target, fields, KI types, tags, and example queries.
- The query response contains `columns` and `values` that represent relevant KIs from the selected AI index.

When an agent runs the sequence, inspect its tool calls to confirm that it selected the expected AI index, used the target and fields from the describe response, and retrieved relevant context.

## Troubleshoot retrieval

Use the following table to resolve common retrieval problems:

| Symptom | Cause | Resolution |
| --- | --- | --- |
| Every {{context-engine}} operation returns `403`. | The credential lacks the {{kib}} **{{context-engine}}** feature privilege. | Add the privilege in the space that contains the AI index. {{es}} index privileges alone are not enough. |
| Query or describe operations return `403`. | The credential lacks {{es}} privileges on the backing indices. | Grant `read` and `view_index_metadata` on the relevant `ai-index-*` indices. |
| Every {{context-engine}} operation returns `404`. | `contextEngine:enabled` is turned off in the space targeted by the request. | Turn on {{context-engine}} in that space's advanced settings. |
| An expected AI index is not listed. | The credential cannot read its backing index, or the AI index is registered in another space. | Check the credential's index privileges and the space targeted by the request. |
| A query returns `Unknown index` for an AI index that was listed. | The AI index is registered, but its backing index does not exist yet. | Select an AI index that contains data. |
| A query returns no rows even though the AI index contains data. | The request targets the wrong space, or the query contains its own space condition. | Target the correct space and remove any space condition from the query. |
| The describe operation omits KI types or tags. | `type` or `tags` is not mapped as an aggregatable keyword field, or the AI index has no active, unexpired KIs. | Check the mappings, or run an automation to generate KIs. Other describe output remains available. |
| The response is too large. | The result exceeds the 20 MB response limit. | Use `KEEP` to return only the required fields, lower the result limit, or aggregate the data with `STATS`. |
