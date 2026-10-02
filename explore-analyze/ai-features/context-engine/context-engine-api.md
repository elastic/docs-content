---
navigation_title: "APIs"
description: Use the Context Engine APIs to manage, inspect, and query AI indices programmatically.
type: reference
applies_to:
  stack: experimental 9.6
  serverless: experimental
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# {{context-engine}} APIs

:::{include} _snippets/hidden-docs-notice.md
:::

Use the {{context-engine}} APIs to manage AI indices, inspect their configuration, and query their Knowledge Indicators (KIs) with {{esql}}. The {{kib}} API reference provides their complete parameters, request and response schemas, and errors.

## Before you begin

Turn on the `contextEngine:enabled` advanced setting in each {{kib}} space where you want to use the APIs. Requests to a space where the setting is turned off return `404`.

API requests use the permissions and space of the authenticated caller. Include the space in the request URL when you are not using the default space.

The caller also needs the `read` index privilege on each AI index's backing index (`ai-index-*`). AI indices without it are left out of list results, and query requests against them return `403`.

## Operations quick access

The following operations are available:

| Operation | Endpoint |
| --- | --- |
| [List AI indices](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-context-engine-ai-index) | `GET /api/context_engine/ai_index` |
| [Create an AI index](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-context-engine-ai-index) | `POST /api/context_engine/ai_index` |
| [Query AI indices](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-context-engine-ai-index-query) | `POST /api/context_engine/ai_index/_query` |
| [Get an AI index](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-context-engine-ai-index-aiindexid) | `GET /api/context_engine/ai_index/{aiIndexId}` |
| [Create or update an AI index](https://www.elastic.co/docs/api/doc/kibana/operation/operation-put-context-engine-ai-index-aiindexid) | `PUT /api/context_engine/ai_index/{aiIndexId}` |
| [Delete an AI index](https://www.elastic.co/docs/api/doc/kibana/operation/operation-delete-context-engine-ai-index-aiindexid) | `DELETE /api/context_engine/ai_index/{aiIndexId}` |
| [Describe an AI index](https://www.elastic.co/docs/api/doc/kibana/operation/operation-get-context-engine-ai-index-aiindexid-describe) | `GET /api/context_engine/ai_index/{aiIndexId}/_describe` |

For task-oriented examples, refer to [Create and manage AI indices](create-and-manage-ai-indices.md), [Add and manage sources](add-and-manage-sources.md), and [Query AI indices from LangChain](langchain-integration.md).
