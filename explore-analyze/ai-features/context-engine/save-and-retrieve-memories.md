---
navigation_title: "Save and retrieve memories"
description: Configure memory so agents can save task context in an AI index, retrieve it later, and forget it when it is no longer valid.
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

# Save and retrieve memories with {{context-engine}}

:::{include} _snippets/hidden-docs-notice.md
:::

[Memory](concepts.md#memory) enables an agent to save useful task context in an [AI index](concepts.md#ai-indices) and retrieve it in later interactions. This helps agents reuse findings, decisions, and effective approaches without deriving them again.

Memories are shared with everyone who can access the AI index. They are not private to a user or conversation. Do not store personal, sensitive, or user-specific information in memory.

This guide demonstrates the memory workflow with an [{{agent-builder}} agent](/explore-analyze/ai-features/agent-builder/agent-builder-agents.md). Compatible external agents can use the same memory operations through tools exposed over Model Context Protocol (MCP).

## Before you begin

You need:

- An {{stack}} 9.6 deployment with an Enterprise license, or an {{serverless-full}} project.
- {{context-engine}} enabled in the current {{kib}} space.
- Permission to change global [Advanced Settings](kibana://reference/advanced-settings.md).
- The **All** privilege for the **Context Engine** feature.
- Permission to create or edit a custom {{agent-builder}} agent.
- The `read`, `write`, and `view_index_metadata` privileges for the AI index's backing {{es}} index.

## Enable memory

Memory must be enabled globally before you can enable it for an AI index:

1. In {{kib}}, open **Stack Management** → **Advanced Settings**.
2. Select the **Global Settings** tab.
3. Search for **Context Engine memory**.
4. Turn on **Context Engine memory** (`contextEngine:memoryEnabled`).

This setting applies to all users and spaces in the current Elastic deployment or {{serverless-short}} project. It makes the memory controls and tools available in spaces where {{context-engine}} is enabled, but it does not enable memory for every AI index.

## Enable memory for an AI index

You can enable memory when you create an AI index or on an existing user-created AI index:

1. Open **Context** from the {{kib}} navigation.
2. Create an AI index, or open an existing AI index that you can edit.
3. In **Memory**, confirm that **Enable memory** is on. When the global memory setting is enabled, memory is on by default for user-created AI indices, including existing ones.
4. Confirm that the AI index description identifies the task context that belongs in the index and the questions it should support.

An AI index can contain both automation-generated [Knowledge Indicators (KIs)](concepts.md#knowledge-indicators) and agent-written memories. You cannot enable memory for a managed AI index in {{kib}}. Memory writes are not supported for an AI index whose destination is an index pattern.

## Add the AI index to an agent

Assign the memory-enabled AI index to a custom agent:

1. In {{agent-builder}}, open **Manage components**, then select **Agents**.
2. Create an agent, or open an agent that you can edit.
3. For an existing agent, select **Edit agent settings**. For a new agent, remain on the **Settings** tab.
4. In **AI Indices**, select the memory-enabled AI index under **Additional indices**.
5. Save the agent, then start a new conversation with it.

With {{context-engine}} enabled, {{agent-builder}} automatically includes the `ki-retrieval` skill for chat agents. When the agent loads the skill, it receives the following retrieval tools:

- `platform.context_engine.list_ai_indices`
- `platform.context_engine.describe_ai_index`
- `platform.context_engine.query_ai_indices`

Because the assigned AI index has memory enabled, {{agent-builder}} also gives the agent the following memory tools:

- `platform.context_engine.remember`
- `platform.context_engine.forget`

You do not need to add the skill or tools manually.

## Save a memory

Ask the agent to save a concrete, reusable fact. For example:

```markdown
Remember this for future billing investigations: After changing the tax configuration, refresh the `orders-enriched` transform before validating invoice totals.
```

Confirm that the agent calls `platform.context_engine.remember` and selects the intended AI index. The tool returns the ID of the stored memory.

To inspect the memory in {{kib}}:

1. Open **Context**, then select the AI index.
2. Open the **Knowledge Indicators** tab.
3. Filter the list to the `memory.session_fact` type.
4. Confirm that the title, description, and content identify the saved fact.

You can also select **View raw docs in Discover** to inspect the stored document in [Discover](/explore-analyze/discover.md).

## Retrieve the memory in a later conversation

Test cross-conversation retrieval so the answer cannot come from the original conversation history:

1. Start a new conversation with the same agent.
2. Ask a question that depends on the saved memory without repeating its content. For example:

   ```markdown
   What should I do before validating invoice totals after a tax configuration change?
   ```

3. Confirm that the agent queries the intended AI index and uses the stored memory in its answer.

The agent recalls active, unexpired memories through the same AI index query operation used to retrieve KIs.

## Forget a memory

Ask the agent to forget a memory when its information is no longer valid or useful:

1. In a conversation with the agent, identify the memory and ask the agent to forget it. For example:

   ```markdown
   Forget the memory about refreshing the `orders-enriched` transform.
   ```

2. Confirm that the agent retrieves the correct memory and calls `platform.context_engine.forget` with its ID.
3. Start another conversation and repeat the recall question.
4. Confirm that the forgotten memory is not returned.

Forgetting a memory marks it as deleted so standard memory retrieval excludes it. It does not remove the stored document from {{es}}.

## Memory access and lifecycle

Memory has the following access and retention behavior:

- A memory belongs to its AI index, not to the user or conversation that created it. Anyone who can access the AI index can retrieve the memory.
- The AI index registry and agent assignment are scoped to a {{kib}} space. The {{context-engine}} tools discover and query AI indices registered in the current space.
- Space access does not grant access to an AI index's backing {{es}} index. Reading and writing memories also requires the corresponding {{es}} index privileges.
- `memory.session_fact` records a granular fact learned during a task. `memory.session` records a broader synthesis of what was tried, what worked, and what to do differently.
- By default, a memory expires 90 days after it is last written. The remember tool can set another expiration time or create a non-expiring memory. Expiration excludes a memory from standard retrieval but does not delete its stored documents.
- The remember tool can revise a memory by writing the same memory ID. It does not automatically detect or merge duplicate memories.
- The forget tool creates a deletion tombstone. Forgotten memories remain stored but are excluded from retrieval.
- Disabling memory for an AI index prevents agents from writing, revising, or forgetting memories in that index, but it does not delete stored memories. If none of an agent's assigned AI indices have memory enabled, {{agent-builder}} does not add the memory tools.
- Agent traces do not create memories automatically.

:::{important}
Expired and forgotten memories remain in the AI index. A user with direct access to the backing {{es}} target can still find them. An AI index query can also return them when it [explicitly includes expired or deleted documents](retrieve-context-from-ai-index.md#query-with-apis). If you must remove a memory permanently, delete all its stored documents from the backing target. This requires the `delete` or `write` index privilege.
:::

## Troubleshoot memory

The following issues are specific to memory setup and retrieval:

| Problem | What to check |
| --- | --- |
| The memory controls, skill, or tools are unavailable. | Confirm that **Context Engine memory** is enabled under **Global Settings** and that {{context-engine}} is enabled in the current space. Changes to the {{context-engine}} setting can take up to five minutes to affect the skill. |
| The agent cannot save or forget a memory. | Confirm that memory is enabled for the assigned AI index and that the user has the **All** privilege for **Context Engine** and `write` access to the backing index. |
| The agent uses the wrong AI index. | Assign only the relevant AI indices and make each index's name and description specific to the context it contains. |
| A new conversation does not retrieve a memory. | Confirm that the memory has not expired or been forgotten, and that the same AI index is assigned to the agent. |
| A forgotten memory is still returned. | Confirm that the agent forgot the correct memory ID, then retry retrieval in a new conversation. |

For shared list, describe, and query failures, refer to [Retrieve context from an AI index](retrieve-context-from-ai-index.md#troubleshoot-retrieval).
