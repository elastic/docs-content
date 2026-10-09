---
navigation_title: "Claude Code"
description: Use the Context Engine skill and Elastic CLI to retrieve context from an AI index in Claude Code.
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

# Use {{context-engine}} with Claude Code

:::{include} _snippets/hidden-docs-notice.md
:::

Use {{context-engine}} with Claude Code to bring context distilled from your organization's data into coding sessions. By retrieving relevant [Knowledge Indicators (KIs)](concepts.md#knowledge-indicators) from an [AI index](concepts.md#ai-indices) instead of repeatedly discovering and interpreting source data, Claude Code can complete tasks faster and use fewer model tokens.

The {{context-engine}} skill teaches Claude Code when and how to retrieve context. Claude Code runs the locally installed Elastic CLI, which calls the {{context-engine}} APIs. This integration does not require an MCP server.

For guidance that applies to every agent integration, refer to [Configure agents to use an AI index](use-context-engine-with-agents.md). For the list, describe, and query flow, refer to [Retrieve context from an AI index](retrieve-context-from-ai-index.md).

## Before you begin

You need:

- Claude Code installed.
- Node.js 22.12.0 or later to install the Elastic CLI.
- `contextEngine:enabled` turned on in the {{kib}} space you want to query.
- An AI index that contains at least one Knowledge Indicator (KI).
- The {{context-engine}} **Read** privilege in that space.
- The {{es}} `read` and `view_index_metadata` privileges for the AI index's backing indices.
- An API key with those {{kib}} and {{es}} privileges.

## Install the Elastic CLI

Install the latest [Elastic CLI](cli://cli/installation.md) globally so Claude Code can run it from its shell environment:

```bash
npm install -g @elastic/cli@latest
elastic --version
```

The Elastic CLI is in technical preview. Install a version that includes the {{context-engine}} command group.

## Confirm the {{context-engine}} commands

Run the following command in the same environment as Claude Code:

```bash
elastic kb context-engine --help
```

The command output should include operations for listing, describing, and querying AI indices. If the command group is unavailable, update the Elastic CLI before continuing.

## Configure an Elastic CLI context

Add a named context with the {{kib}} URL and API key for the deployment:

```bash
elastic config context add context-engine \
  --kb-url https://my-deployment.kb.us-east-1.aws.elastic.cloud \
  --kb-api-key <api-key>
```

The Elastic CLI stores the API key in the operating system's credential store when one is available. Set the new context as the default, then verify that the CLI can connect:

```bash
elastic config current-context set context-engine
elastic status
```

To target a non-default {{kib}} space, include `/s/<space-id>` in the {{kib}} URL.

## Install the {{context-engine}} skill

The `kibana-context-engine` skill supplies the retrieval procedure and the Elastic CLI commands that Claude Code needs.

:::{note}
The skill is not yet publicly available. This draft will be updated with its supported installation path before publication.
:::

<!--
Install the [Elastic plugin for Claude](/explore-analyze/ai-features/claude-plugin.md), which includes the `kibana-context-engine` skill.

Tracked by https://github.com/elastic/search-team/issues/16314. Replace this comment with the supported installation steps after the skill is publicly available and its distribution through the Elastic plugin for Claude is confirmed.
-->

In Claude Code, run `/skills` and confirm that `kibana-context-engine` is available.

## Retrieve context

Start a new Claude Code session so the newly installed skill is available, then ask a question covered by one of your AI indices. Tell Claude Code to use {{context-engine}} if you want to exercise the integration explicitly. For example:

```text
Use Context Engine to explain <subject covered by your AI index>. Tell me which AI index and Knowledge Indicators you used.
```

Claude Code should load the skill and run these operations in order:

1. **List** the available AI indices and select one whose description matches the question.
2. **Describe** that AI index to obtain its {{esql}} target, fields, KI types, tags, and example queries.
3. **Query** the AI index for relevant KIs and use the results to answer the question.

For the underlying retrieval sequence, refer to [Retrieve context from an AI index](retrieve-context-from-ai-index.md).

## Verify the retrieval

Review the commands Claude Code ran and confirm that it:

- Used `elastic kb context-engine` commands rather than querying the backing index directly.
- Listed the available AI indices before selecting one, unless the prompt already identified the AI index.
- Described the selected AI index before constructing the {{esql}} query.
- Queried the target and fields returned by the describe operation.
- Used KIs from the expected AI index to answer the question.

The commands should correspond to the following operations:

| Operation | Elastic CLI command |
| --- | --- |
| List AI indices | `elastic kb context-engine get-context-engine-ai-index` |
| Describe an AI index | `elastic kb context-engine get-context-engine-ai-index-aiindexid-describe --ai-index-id '<id>'` |
| Query AI indices | `elastic kb context-engine post-context-engine-ai-index-query --query '<esql>'` |

## Troubleshoot the integration

Use the following table to resolve common setup and retrieval problems:

| Symptom | Resolution |
| --- | --- |
| Claude Code does not load `kibana-context-engine`. | Confirm that the skill is installed in a location Claude Code discovers, then start a new session and run `/skills`. |
| `elastic` is not found. | Install the CLI globally and confirm that its executable is on the `PATH` available to Claude Code. |
| `elastic kb context-engine` is not a recognized command. | Update the Elastic CLI to a version that contains the {{context-engine}} commands. |

For additional API-level failures, refer to [Troubleshoot retrieval](retrieve-context-from-ai-index.md#troubleshoot-retrieval).

<!--
## Next step

To send Claude Code traces to Elastic, refer to [Send Claude Code telemetry to Elastic](send-claude-code-telemetry.md).

Tracked by https://github.com/elastic/search-team/issues/16315.
-->
