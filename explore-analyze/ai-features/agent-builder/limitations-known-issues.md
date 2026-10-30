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

### Frozen tier data excluded by default [frozen-tier-data]

```{applies_to}
stack: ga 9.4.8+
```

{{agent-builder}} tools can exclude documents stored in the [frozen tier](/manage-data/lifecycle/data-tiers.md#frozen-tier). Searching that data recovers [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md) from object storage. These searches are slow and can cause tool calls to time out.

:::{note}
[Data tiers](/manage-data/lifecycle/data-tiers.md) are not relevant to {{serverless-short}} which automatically handles data storage and scaling. 
:::

{applies_to}`stack: ga 9.4.8+` Behavior depends on your version:

* {applies_to}`stack: ga 9.4.8+` **9.4.0 through 9.4.7, and 9.5.0 through 9.5.4:** Tools read frozen tier data.
* {applies_to}`stack: ga 9.4.8+` **9.4.8 and 9.5.5:** Tools always exclude frozen tier data, and the options to include it aren't available.
* {applies_to}`stack: ga 9.4.8+` **9.4.9, 9.5.6, and later:** Tools exclude frozen tier data by default. You can include it with the options in this section.

Query tools exclude documents in frozen tier indices. This includes the built-in `execute_esql`, `generate_esql`, and `search` tools, plus custom [{{esql}} tools](tools/esql-tools.md) and [index search tools](tools/index-search-tools.md).

* If only some matching documents are frozen, the tool returns the rest.
* If every matching document is frozen, the tool returns no documents.

Mapping tools differ:

* `get_index_mapping` can omit fields that exist only in frozen backing indices. This applies when it reads a data stream, an alias, an index pattern, or a remote index. A request for one local index still returns that index mapping.
* `index_explorer` can omit those fields for remote clusters. For a local data stream, it returns the data stream mapping, which doesn't apply this filter.

These Security tools have no `include_frozen` parameter. On versions that exclude frozen tier data, they always exclude it. The options in this section don't apply to them:

* `security.alerts`
* `security.attack_discovery_search`
* `security.search_entities`
* `security.get_entity`, when it reads profile history
* {applies_to}`stack: preview 9.5` `security.pci_compliance`

#### Include frozen tier data

```{applies_to}
stack: ga 9.4.9+
```

To include frozen tier data, use one of these options:

* **For one tool call:** Ask the agent to include frozen tier data. Built-in tools accept an `include_frozen` parameter. The parameter description tells the agent to set it to `true` only when you or the agent instructions ask for frozen tier data. For details, refer to [Frozen tier data in built-in tools](tools/builtin-tools-reference.md#agent-builder-builtin-tools-frozen-tier).
* **For a custom tool:** In **Data tiers**, select **Include frozen tier data**. Or set `include_frozen` to `true` in the tool `configuration` object in the [Tools API](kibana-api.md#tools-apis).
* **For all five built-in tools in a space:** Turn on **Elastic Agent Builder: Include frozen tier data by default** (`agentBuilder:includeFrozenByDefault`). This is an [advanced setting](kibana://reference/advanced-settings.md#kibana-general-settings). Use it for [Model Context Protocol (MCP) clients](mcp-server.md), where you can't adjust a single agent prompt.

  When the setting is on, the parameter description tells the agent to set `include_frozen` to `false` only when you or the agent instructions ask to exclude frozen tier data. An explicit `include_frozen` value on a tool call overrides the setting. The setting doesn't affect custom tools or the Security tools in this section.

Including frozen tier data doesn't extend tool timeouts. Queries over large amounts of frozen data can still time out.

### A2A streaming not supported

The [A2A server](a2a-server.md) does not currently support streaming operations. All agent interactions use the synchronous `message/send` method, which returns a complete response only after task execution completes.

### Human-in-the-loop prompts require an interactive conversation

[Human-in-the-loop prompts](chat.md#human-in-the-loop-prompts) work only in interactive {{agent-builder}} conversations. A sub-agent execution cannot collect a response to these prompts, whether the sub-agent runs in the foreground or the background, so {{agent-builder}} declines any action that requires confirmation or authorization.

The sub-agent run itself does not fail. The tool call returns an error result and the sub-agent continues, so the sub-agent can report the declined action in its output.

A2A executions behave differently: the action is not declined. Instead, the conversation round remains in the `awaiting_prompt` state, but A2A clients cannot respond to the prompt.

{applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` The [`execute_api` tool](tools/builtin-tools-reference.md#http-api-tools) follows the same rule in sub-agent runs and in [workflow `ai.agent` steps](/explore-analyze/workflows/steps/ai-steps.md#ai-agent): it declines any {{es}} or {{kib}} API operation that requires [confirmation](chat.md#confirm-an-api-operation), unless the operation is approved in advance. You can approve operations in advance in these ways:

* **For every run of an agent:** Add the operations to the agent's [auto-approved APIs](custom-agents.md#auto-approve-api-operations-optional). This approval is stored with the agent, so it applies to every run, including runs from workflows, and to the sub-agents the agent starts.
* **For one workflow step:** List the operations under `approvals.auto_approved_apis` in the `ai.agent` step. This approval applies only to that step and to the sub-agents it starts, in addition to the agent's auto-approved APIs.
* **For one sub-agent run:** Before starting a sub-agent, a parent agent can ask you to approve operations for it. The request can name individual operations, a group such as all `indices` operations, or every such operation on {{es}} or {{kib}}. The outcome depends on your response and any existing auto-approvals:

  * If you approve, the sub-agent can call those operations without another prompt.
  * If you deny, the sub-agent runs without access to them.
  * If all requested operations are already auto-approved, you aren't asked.

  A sub-agent can also call any operation that the parent agent or the sub-agent itself auto-approves.

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

### Disabling a workflow breaks agents that use it [disabled-pre-execution-workflow]

```{applies_to}
stack: ga 9.4+
serverless: ga
```

:::{note}
The selector-visibility half of this issue is fixed on serverless and on 9.5.3 and later.
:::

Disabling a workflow doesn't remove it from the agents or spaces that use it as a [pre-execution workflow](agents-and-workflows.md#pre-execution-workflows), so every message to those agents fails with a **Workflow Failed** error. On 9.4.x, and on 9.5.0 through 9.5.2, the disabled workflow also disappears from the **Workflows** selector, so you can't clear it from the UI without re-enabling the workflow first.

**Workaround:** Re-enable the workflow, clear it from the selector, save, then disable the workflow again. You can also clear it through the API. To learn more, refer to [Disabled pre-execution workflow](troubleshooting/pre-execution-workflow-disabled.md).

### MCP server URL copy button omits space name

:::{note}
Fixed on serverless and 9.3.
:::

On 9.2 deployments, the **Copy your MCP server URL** button does not include the space name when used from a custom {{kib}} Space.

**Workaround:** Manually add `/s/<space-name>` to the URL. For example: `https://<deployment>/s/<space-name>/api/agent_builder/mcp`

For more information about {{agent-builder}} and Spaces, refer to [Permissions and access control](permissions.md#space-scope).


## Related pages

- [Get started](get-started.md)
- [Troubleshooting](troubleshooting.md)
