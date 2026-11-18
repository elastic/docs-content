---
navigation_title: Step type index
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Every step type available for Elastic Workflows, ordered alphabetically, with a one-line description and a link to its full reference.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Step type index [workflows-step-types]

Every step type available for Elastic Workflows, ordered alphabetically. Use this lookup when you know the step ID and want the reference fast. If you know what you want to *do* but not which step to use, refer to [Choose the right step](/explore-analyze/workflows/authoring-techniques/choose-the-right-step.md).

| Step type | Category | What it does |
|---|---|---|
| [`ai.agent`](/explore-analyze/workflows/steps/ai-steps.md#ai-agent) | AI | Invoke an {{agent-builder}} agent as a step. |
| [`ai.attachment.add`](/explore-analyze/workflows/steps/ai-steps.md#ai-attachment-add) {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | AI | Add an attachment to an {{agent-builder}} conversation. |
| [`ai.attachment.delete`](/explore-analyze/workflows/steps/ai-steps.md#ai-attachment-delete) {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | AI | Delete an attachment from an {{agent-builder}} conversation. |
| [`ai.attachment.list`](/explore-analyze/workflows/steps/ai-steps.md#ai-attachment-list) {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | AI | List the attachments in an {{agent-builder}} conversation. |
| [`ai.attachment.read`](/explore-analyze/workflows/steps/ai-steps.md#ai-attachment-read) {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | AI | Read the content of an attachment in an {{agent-builder}} conversation. |
| [`ai.attachment.update`](/explore-analyze/workflows/steps/ai-steps.md#ai-attachment-update) {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | AI | Update an attachment in an {{agent-builder}} conversation. |
| [`ai.classify`](/explore-analyze/workflows/steps/ai-steps.md#ai-classify) | AI | Classify input into a fixed category set. |
| [`ai.conversation.metadata.patch`](/explore-analyze/workflows/steps/ai-steps.md#ai-conversation-metadata-patch) {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | AI | Update the metadata of an {{agent-builder}} conversation. |
| [`ai.conversation.metadata.read`](/explore-analyze/workflows/steps/ai-steps.md#ai-conversation-metadata-read) {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` | AI | Read the metadata of an {{agent-builder}} conversation. |
| [`ai.prompt`](/explore-analyze/workflows/steps/ai-steps.md#ai-prompt) | AI | Prompt a model, optionally with structured output. |
| [`ai.summarize`](/explore-analyze/workflows/steps/ai-steps.md#ai-summarize) | AI | Summarize content with an LLM. |
| `cases.addAlerts` | Cases | Attach detection alerts to a case. |
| `cases.addAttachments` {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | Cases | Attach several attachment types to a case in one request. |
| `cases.addComment` | Cases | Add a comment to a case. |
| `cases.addEvents` | Cases | Attach events to a case. |
| `cases.addObservables` | Cases | Add observables (IPs, hashes, domains) to a case. |
| `cases.addTags` | Cases | Add tags to a case. |
| `cases.assignCase` | Cases | Assign a case to one or more users. |
| `cases.closeCase` | Cases | Close a case. |
| `cases.createCase` | Cases | Create a case. |
| `cases.createCaseFromTemplate` | Cases | Create a case from a template. |
| `cases.deleteCases` | Cases | Delete one or more cases. |
| `cases.deleteObservable` | Cases | Delete an observable from a case. |
| `cases.findCases` | Cases | Search for cases. |
| `cases.findSimilarCases` | Cases | Find cases similar to a given case. |
| `cases.getAllAttachments` | Cases | List every attachment on a case. |
| `cases.getCase` | Cases | Fetch a case by ID. |
| `cases.getCases` | Cases | Fetch multiple cases by ID. |
| `cases.getCasesByAlertId` | Cases | Find cases containing a specific alert. |
| `cases.pushCases` | Cases | Push one or more cases to their configured external connector. |
| `cases.removeTags` | Cases | Remove tags from a case. |
| `cases.setCategory` | Cases | Set a case's category. |
| `cases.setCustomField` | Cases | Set a custom field on a case. |
| `cases.setDescription` | Cases | Update a case's description. |
| `cases.setSeverity` | Cases | Set a case's severity. |
| `cases.setStatus` | Cases | Set a case's status. |
| `cases.setTitle` | Cases | Update a case's title. |
| `cases.unassignCase` | Cases | Remove assignees from a case. |
| `cases.updateCase` | Cases | Update one case's fields. |
| `cases.updateCases` | Cases | Bulk update multiple cases. |
| `cases.updateObservable` | Cases | Update an observable. |
| [`console`](/explore-analyze/workflows/steps/external-systems-apps.md) | HTTP and console | Log a message to the workflow execution view. |
| [`data.aggregate`](/explore-analyze/workflows/steps/data.md#data-aggregate) | Data | Group and aggregate a collection. |
| [`data.concat`](/explore-analyze/workflows/steps/data.md#data-concat) | Data | Concatenate arrays. |
| [`data.dedupe`](/explore-analyze/workflows/steps/data.md#data-dedupe) | Data | Remove duplicates from an array. |
| [`data.filter`](/explore-analyze/workflows/steps/data.md#data-filter) | Data | Keep elements matching a KQL predicate. |
| [`data.find`](/explore-analyze/workflows/steps/data.md#data-find) | Data | Return the first element matching a KQL predicate. |
| [`data.map`](/explore-analyze/workflows/steps/data.md#data-map) | Data | Transform each element of an array. |
| [`data.parseJson`](/explore-analyze/workflows/steps/data.md#data-parsejson) | Data | Parse a JSON string into an object. |
| [`data.regexExtract`](/explore-analyze/workflows/steps/data.md#data-regexextract) | Data | Extract fields from a string using regex. |
| [`data.regexReplace`](/explore-analyze/workflows/steps/data.md#data-regexreplace) | Data | Replace regex matches in a string. |
| [`data.set`](/explore-analyze/workflows/steps/data.md#data-set) | Data | Set named variables in the workflow context. |
| [`data.stringifyJson`](/explore-analyze/workflows/steps/data.md#data-stringifyjson) | Data | Serialize an object to a JSON string. |
| [`elasticsearch.bulk`](/explore-analyze/workflows/steps/elasticsearch.md#named-actions) | {{es}} | Bulk index, update, or delete documents. |
| [`elasticsearch.esql.query`](/explore-analyze/workflows/steps/elasticsearch.md#named-actions) | {{es}} | Run an ES\|QL query. |
| [`elasticsearch.index`](/explore-analyze/workflows/steps/elasticsearch.md#named-actions) | {{es}} | Index one document. |
| [`elasticsearch.indices.create`](/explore-analyze/workflows/steps/elasticsearch.md#named-actions) | {{es}} | Create an index. |
| [`elasticsearch.indices.delete`](/explore-analyze/workflows/steps/elasticsearch.md#named-actions) | {{es}} | Delete one or more indices. |
| [`elasticsearch.indices.exists`](/explore-analyze/workflows/steps/elasticsearch.md#named-actions) | {{es}} | Check whether indices exist. |
| [`elasticsearch.request`](/explore-analyze/workflows/steps/elasticsearch.md#generic-request-actions) | {{es}} | Generic {{es}} API escape hatch. |
| [`elasticsearch.search`](/explore-analyze/workflows/steps/elasticsearch.md#named-actions) | {{es}} | Run a search. |
| [`elasticsearch.update`](/explore-analyze/workflows/steps/elasticsearch.md#named-actions) | {{es}} | Update one document. |
| [`entityStore.updateAssetCriticality`](/explore-analyze/workflows/steps/entity-store.md#entitystore-updateassetcriticality) {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` | Entity store | Set or remove an entity's asset criticality, and optionally recalculate its risk score. |
| [`foreach`](/explore-analyze/workflows/steps/foreach.md) | Flow control | Iterate over a collection. |
| [`http`](/explore-analyze/workflows/steps/external-systems-apps.md#http-actions) | HTTP and console | Call any external HTTP API. |
| [`if`](/explore-analyze/workflows/steps/if.md) | Flow control | Conditional branching. |
| [`kibana.request`](/explore-analyze/workflows/steps/kibana.md#kibana-request) | {{kib}} | Generic {{kib}} API escape hatch. |
| [`kibana.SetAlertsStatus`](/explore-analyze/workflows/steps/kibana.md#kibana-setalertsstatus) | {{kib}} | Update detection alert status. PascalCase. |
| [`kibana.SetAlertTags`](/explore-analyze/workflows/steps/kibana.md#kibana-setalerttags) | {{kib}} | Add or remove tags on detection alerts. PascalCase. |
| [`kibana.streams.get`](/explore-analyze/workflows/steps/streams.md#kibana-streams-get) | Streams (tech preview) | Fetch a stream by name. |
| [`kibana.streams.getSignificantEvents`](/explore-analyze/workflows/steps/streams.md#kibana-streams-getsignificantevents) | Streams (tech preview) | Get significant events for a stream. |
| [`kibana.streams.list`](/explore-analyze/workflows/steps/streams.md#kibana-streams-list) | Streams (tech preview) | List available streams. |
| [`loop.break`](/explore-analyze/workflows/steps/loop-break.md) | Flow control | Exit the innermost loop. |
| [`loop.continue`](/explore-analyze/workflows/steps/loop-continue.md) | Flow control | Skip to the next iteration. |
| [`parallel`](/explore-analyze/workflows/steps/parallel.md) {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` | Flow control | Run branches concurrently and collect a per-branch result. |
| [`security.assignAlert`](/explore-analyze/workflows/steps/alert-triage.md#security-assignalert) | Security | Assign or unassign users on one or more alerts. |
| [`security.assignAttack`](/explore-analyze/workflows/steps/attack-triage.md#security-assignattack) | Security | Assign or unassign users on one or more attacks. |
| [`security.disableRule`](/explore-analyze/workflows/steps/detection-rules.md#security-disablerule) {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | Security | Disable one or more detection rules by rule-ID list or KQL query, with partial-failure reporting. |
| [`security.enableRule`](/explore-analyze/workflows/steps/detection-rules.md#security-enablerule) {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | Security | Enable one or more detection rules by rule-ID list or KQL query, with partial-failure reporting. |
| [`security.setAlertStatus`](/explore-analyze/workflows/steps/alert-triage.md#security-setalertstatus) | Security | Set alert status: `open`, `acknowledged`, or `closed`. |
| [`security.setAlertTags`](/explore-analyze/workflows/steps/alert-triage.md#security-setalerttags) | Security | Add or remove tags on one or more alerts. |
| [`security.setAttackStatus`](/explore-analyze/workflows/steps/attack-triage.md#security-setattackstatus) | Security | Set attack status: `open`, `acknowledged`, or `closed`. |
| [`security.setAttackTags`](/explore-analyze/workflows/steps/attack-triage.md#security-setattacktags) | Security | Add or remove tags on one or more attacks. |
| [`switch`](/explore-analyze/workflows/steps/switch.md) | Flow control | Multi-way dispatch. |
| [`wait`](/explore-analyze/workflows/steps/wait.md) | Flow control | Pause for a fixed duration. |
| [`waitForApproval`](/explore-analyze/workflows/steps/wait-for-approval.md) {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` | Flow control | Pause for approve/reject (human-in-the-loop). |
| [`waitForInput`](/explore-analyze/workflows/steps/wait-for-input.md) | Flow control | Pause for human input (human-in-the-loop). |
| [`while`](/explore-analyze/workflows/steps/while.md) | Flow control | Loop while a condition holds. |
| [`workflow.execute`](/explore-analyze/workflows/steps/composition.md#workflow-execute) | Composition (tech preview) | Run a child workflow synchronously. |
| [`workflow.executeAsync`](/explore-analyze/workflows/steps/composition.md#workflow-executeasync) | Composition (tech preview) | Fire-and-forget child workflow. |
| [`workflow.fail`](/explore-analyze/workflows/steps/composition.md#workflow-fail) | Composition (tech preview) | Terminate the workflow as failed. |
| [`workflow.output`](/explore-analyze/workflows/steps/composition.md#workflow-output) | Composition (tech preview) | Emit the final outputs of a workflow. |

## External connector steps [workflows-external-connectors]

Every configured {{kib}} connector also exposes one or more step types. A connector with a single action uses its connector type as the step type, such as `slack` or `pagerduty`. A connector with several actions exposes one `<connector>.<action>` step type for each action, such as `jira.pushToService`. Common examples include:

- `slack` posts a message to the Slack channel that the connector's webhook targets.
- `jira.pushToService` creates or updates a Jira issue.
- `pagerduty` sends a trigger, acknowledge, or resolve event to PagerDuty, for example to page an on-call rotation.
- `virustotal.scanFileHash` scans a file hash.

Because the available connector steps depend on which connectors your deployment has configured, they aren't enumerated here. Refer to the [{{kib}} connectors reference](kibana://reference/connectors-kibana.md) for the full catalog.

## Deprecated step types [workflows-deprecated-steps]

Deprecated step types still work in existing workflows but can't be used in new ones. They're hidden from autocomplete and the **Add Action** menu, and the YAML editor shows a deprecation warning with a replacement suggestion on hover. 

Refer to the [migration guide](/explore-analyze/workflows/authoring-techniques/migrate-from-9-3.md) for Cases replacement details. For AI connector steps, replace them with [`ai.prompt`](/explore-analyze/workflows/steps/ai-steps.md#ai-prompt) (or another [AI step](/explore-analyze/workflows/steps/ai-steps.md) such as `ai.classify`, `ai.summarize`, or `ai.agent` when that better matches the task).

| Deprecated | Replacement |
|---|---|
| `kibana.createCaseDefaultSpace` | `cases.createCase` |
| `kibana.getCaseDefaultSpace` | `cases.getCase` |
| `kibana.updateCaseDefaultSpace` | `cases.updateCase` |
| `kibana.addCaseCommentDefaultSpace` | `cases.addComment` |
| `inference.*` | [`ai.prompt`](/explore-analyze/workflows/steps/ai-steps.md#ai-prompt) |
| `bedrock.*` | [`ai.prompt`](/explore-analyze/workflows/steps/ai-steps.md#ai-prompt) |
| `gen-ai.*` | [`ai.prompt`](/explore-analyze/workflows/steps/ai-steps.md#ai-prompt) |
| `gemini.*` | [`ai.prompt`](/explore-analyze/workflows/steps/ai-steps.md#ai-prompt) |

## Related [workflows-step-types-related]

- [Steps overview](/explore-analyze/workflows/steps.md): Common fields every step accepts.
- [Cheat sheet](/explore-analyze/workflows/reference/cheat-sheet.md): Step menu organized by intent rather than alphabetically.
- [`elastic/workflows` library](https://github.com/elastic/workflows): 57 example workflows that exercise these step types.
