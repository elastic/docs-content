---
navigation_title: "Availability and limits"
description: Check where Context Engine is available, how to turn it on in a Kibana space, which privileges each task requires, and the limits that apply to AI indices, Knowledge Indicators, queries, and automations.
type: overview
applies_to:
  stack: experimental 9.6
  serverless: experimental
products:
  - id: elasticsearch
  - id: kibana
  - id: observability
  - id: security
---

# {{context-engine}} availability and limits

:::{include} _snippets/hidden-docs-notice.md
:::

Use this page to check whether you can use {{context-engine}} in your environment, what you must turn on or grant before you start, and the limits that apply to AI indices, Knowledge Indicators (KIs), queries, and automations.

## Deployment types and licensing

For {{stack}} deployments, {{context-engine}} requires an Enterprise license or trial.

In {{serverless-short}}, the `contextEngine:enabled` setting is available in the following project types:

| Project type | Availability |
| --- | --- |
| {{es-serverless}} | Available |
| {{obs-serverless}} | Available |
| {{sec-serverless}} | Available in the Security Analytics Complete feature tier and with [Elastic AI SOC Engine (EASE)](/solutions/security/ai/ease/ease-intro.md). Not available in the Security Analytics Essentials tier. |

For information about project feature tiers, refer to [Project features and add-ons](/deploy-manage/deploy/elastic-cloud/project-settings.md#project-features-add-ons).

## Turn on {{context-engine}} in a space [turn-on-context-engine]

{{context-engine}} is turned off by default. To use it, turn on the **{{context-engine}}** advanced setting (`contextEngine:enabled`) in each {{kib}} space where you need it:

1. Open **Stack Management** → **Advanced Settings**.
2. Search for **{{context-engine}}**.
3. Turn on **{{context-engine}}**, then save the change.

The setting applies only to the current space. AI indices are also scoped to the space where you create them, so an AI index is not visible from other spaces. For setting details, refer to the [{{kib}} advanced settings reference](kibana://reference/advanced-settings.md).

While the setting is turned off in a space:

- The **Context** app does not appear in the {{kib}} navigation.
- Requests to the [{{context-engine}} APIs](context-engine-api.md) in that space return `404`.
- Workflow steps that read or write KIs, such as `context-engine.createKi`, fail with an error that asks you to turn on the setting.
- {{agent-builder}} agents in that space do not use their assigned AI indices.

Turning the setting off does not delete AI indices, KIs, or automation workflows. After you turn the setting on or off, {{agent-builder}} agents can take up to 5 minutes to reflect the change.

## Required privileges [context-engine-privileges]

{{context-engine}} uses the **{{context-engine}}** {{kib}} feature privilege together with {{es}} index privileges on the AI index's backing indices, which use the `ai-index-*` pattern. The {{kib}} privilege controls access to the **Context** app and the {{context-engine}} APIs. The index privileges control which AI indices and KIs a user or API key can read or change.

| Task | {{kib}} privileges | {{es}} privileges |
| --- | --- | --- |
| Turn on {{context-engine}} in a space | **All** for **Advanced Settings** | None |
| View AI indices and KIs, or retrieve them through the APIs or agent tools | **Read** for **{{context-engine}}** | `read` and `view_index_metadata` on the backing indices |
| Create and edit AI indices and sources | **All** for **{{context-engine}}** | Access to the source data you select |
| Create and run automations | **All** for **{{context-engine}}**, plus [workflow privileges](/explore-analyze/workflows/get-started/setup.md) | Access to the source data that the automation reads |
| {applies_to}`stack: experimental 9.7+` Edit, delete, or restore KIs in {{kib}} | **All** for **{{context-engine}}** | `write` on the backing index |
| Delete an AI index and its KIs | **All** for **{{context-engine}}**, plus permission to delete workflows to remove its automations | `delete_index` on the backing index |
| Assign an AI index to an {{agent-builder}} agent | [Permission to create or edit agents](/explore-analyze/ai-features/agent-builder/permissions.md), plus **Read** for **{{context-engine}}** | `read` and `view_index_metadata` on the backing indices |

Users with only the **Read** privilege can inspect AI indices and KIs but do not see actions that change them.

External clients, such as scripts, LangChain applications, and Claude Code, call the APIs with the privileges of their credentials. To create an API key with the privileges required for retrieval, refer to [Create an API key](retrieve-context-from-ai-index.md#create-query-api-key).

## Limits [context-engine-limits]

The following limits apply to {{context-engine}} objects and requests.

### AI indices

| Item | Limit |
| --- | --- |
| AI indices returned when listing a space | 100 |
| AI index ID | 256 characters |
| AI index description | 2,048 characters |
| Sources for each AI index | 100 |
| Automations for each AI index | 100 |

### Knowledge Indicators

| Item | Limit |
| --- | --- |
| KI title | 512 characters |
| KI description | 2,048 characters |
| KI content | 65,536 characters |
| Tags for each KI | 100 |

### Queries

| Item | Limit |
| --- | --- |
| {{esql}} query length | 10,000 characters |
| Rows returned | 100 by default, up to 1,000 |
| Response size | 20 MB |
| Fields returned by the describe operation | 500 |
| KI types and tags summarized by the describe operation | 20 each |

To reduce a large response, use `KEEP` to return only the fields you need, lower the result limit, or aggregate the data with `STATS`.

### Automation generation [generation-limit]

When {{agent-builder}} sets up a Bottom-Up or Cumulative / Wiki-style automation from a template, each run processes a limited number of source documents or profiled units:

| Item | {applies_to}`stack: experimental =9.6` | {applies_to}`stack: experimental 9.7+` {applies_to}`serverless: experimental` |
| --- | --- | --- |
| Documents for each Bottom-Up run | 50 by default, up to 10,000 | 50 by default, up to 2,000 |
| Units for each Cumulative / Wiki-style run | 100 by default, up to 10,000 | 100 by default, up to 2,000 |

A Bottom-Up run reads the source documents in document ID order after it applies its filter, so running it again does not reach documents beyond the limit. When a source contains more documents, narrow the automation's filter, such as with a time range or status condition, or use an aggregate strategy such as Index/Table Metadata or Cumulative / Wiki-style. For guidance, refer to [Select a generation strategy](build-and-maintain-ai-index.md#select-a-generation-strategy).
