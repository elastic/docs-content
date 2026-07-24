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
| [`ai.classify`](/explore-analyze/workflows/steps/ai-steps.md#ai-classify) | AI | Classify input into a fixed category set. |
| [`ai.prompt`](/explore-analyze/workflows/steps/ai-steps.md#ai-prompt) | AI | Prompt a model, optionally with structured output. |
| [`ai.summarize`](/explore-analyze/workflows/steps/ai-steps.md#ai-summarize) | AI | Summarize content with an LLM. |
| [`cases.addAlerts`](/explore-analyze/workflows/steps/cases.md#cases-addalerts) | Cases | Attach detection alerts to a case. |
| [`cases.addAttachments`](/explore-analyze/workflows/steps/cases.md#cases-addattachments) {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | Cases | Attach several attachment types to a case in one request. |
| [`cases.addComment`](/explore-analyze/workflows/steps/cases.md#cases-addcomment) | Cases | Add a comment to a case. |
| [`cases.addEvents`](/explore-analyze/workflows/steps/cases.md#cases-addevents) | Cases | Attach events to a case. |
| [`cases.addObservables`](/explore-analyze/workflows/steps/cases.md#cases-addobservables) | Cases | Add observables (IPs, hashes, domains) to a case. |
| [`cases.addTags`](/explore-analyze/workflows/steps/cases.md#cases-addtags) | Cases | Add tags to a case. |
| [`cases.assignCase`](/explore-analyze/workflows/steps/cases.md#cases-assigncase) | Cases | Assign a case to one or more users. |
| [`cases.closeCase`](/explore-analyze/workflows/steps/cases.md#cases-closecase) | Cases | Close a case. |
| [`cases.createCase`](/explore-analyze/workflows/steps/cases.md#cases-createcase) | Cases | Create a case. |
| [`cases.createCaseFromTemplate`](/explore-analyze/workflows/steps/cases.md#cases-createcasefromtemplate) | Cases | Create a case from a template. |
| [`cases.deleteCases`](/explore-analyze/workflows/steps/cases.md#cases-deletecases) | Cases | Delete one or more cases. |
| [`cases.deleteObservable`](/explore-analyze/workflows/steps/cases.md#cases-deleteobservable) | Cases | Delete an observable from a case. |
| [`cases.findCases`](/explore-analyze/workflows/steps/cases.md#cases-findcases) | Cases | Search for cases. |
| [`cases.findSimilarCases`](/explore-analyze/workflows/steps/cases.md#cases-findsimilarcases) | Cases | Find cases similar to a given case. |
| [`cases.getAllAttachments`](/explore-analyze/workflows/steps/cases.md#cases-getallattachments) | Cases | List every attachment on a case. |
| [`cases.getCase`](/explore-analyze/workflows/steps/cases.md#cases-getcase) | Cases | Fetch a case by ID. |
| [`cases.getCases`](/explore-analyze/workflows/steps/cases.md#cases-getcases) | Cases | Fetch multiple cases by ID. |
| [`cases.getCasesByAlertId`](/explore-analyze/workflows/steps/cases.md#cases-getcasesbyalertid) | Cases | Find cases containing a specific alert. |
| [`cases.pushCases`](/explore-analyze/workflows/steps/cases.md#cases-pushcases) | Cases | Push one or more cases to their configured external connector. |
| [`cases.removeTags`](/explore-analyze/workflows/steps/cases.md#cases-removetags) | Cases | Remove tags from a case. |
| [`cases.setCategory`](/explore-analyze/workflows/steps/cases.md#cases-setcategory) | Cases | Set a case's category. |
| [`cases.setCustomField`](/explore-analyze/workflows/steps/cases.md#cases-setcustomfield) | Cases | Set a custom field on a case. |
| [`cases.setDescription`](/explore-analyze/workflows/steps/cases.md#cases-setdescription) | Cases | Update a case's description. |
| [`cases.setSeverity`](/explore-analyze/workflows/steps/cases.md#cases-setseverity) | Cases | Set a case's severity. |
| [`cases.setStatus`](/explore-analyze/workflows/steps/cases.md#cases-setstatus) | Cases | Set a case's status. |
| [`cases.setTitle`](/explore-analyze/workflows/steps/cases.md#cases-settitle) | Cases | Update a case's title. |
| [`cases.unassignCase`](/explore-analyze/workflows/steps/cases.md#cases-unassigncase) | Cases | Remove assignees from a case. |
| [`cases.updateCase`](/explore-analyze/workflows/steps/cases.md#cases-updatecase) | Cases | Update one case's fields. |
| [`cases.updateCases`](/explore-analyze/workflows/steps/cases.md#cases-updatecases) | Cases | Bulk update multiple cases. |
| [`cases.updateObservable`](/explore-analyze/workflows/steps/cases.md#cases-updateobservable) | Cases | Update an observable. |
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
| [`security.assignAlert`](/explore-analyze/workflows/steps/attack-triage.md#security-assignalert) | Security | Assign or unassign users on one or more alerts. |
| [`security.assignAttack`](/explore-analyze/workflows/steps/attack-triage.md#security-assignattack) | Security | Assign or unassign users on one or more attacks. |
| [`security.disableRule`](/explore-analyze/workflows/steps/detection-rules.md#security-disablerule) {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | Security | Disable one or more detection rules by rule-ID list or KQL query, with partial-failure reporting. |
| [`security.enableRule`](/explore-analyze/workflows/steps/detection-rules.md#security-enablerule) {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | Security | Enable one or more detection rules by rule-ID list or KQL query, with partial-failure reporting. |
| [`security.setAlertStatus`](/explore-analyze/workflows/steps/attack-triage.md#security-setalertstatus) | Security | Set alert status: `open`, `acknowledged`, or `closed`. |
| [`security.setAlertTags`](/explore-analyze/workflows/steps/attack-triage.md#security-setalerttags) | Security | Add or remove tags on one or more alerts. |
| [`security.setAttackStatus`](/explore-analyze/workflows/steps/attack-triage.md#security-setattackstatus) | Security | Set attack status: `open`, `acknowledged`, or `closed`. |
| [`security.setAttackTags`](/explore-analyze/workflows/steps/attack-triage.md#security-setattacktags) | Security | Add or remove tags on one or more attacks. |
| [`switch`](/explore-analyze/workflows/steps/switch.md) | Flow control | Multi-way dispatch. |
| [`wait`](/explore-analyze/workflows/steps/wait.md) | Flow control | Pause for a fixed duration. |
| [`waitForInput`](/explore-analyze/workflows/steps/wait-for-input.md) | Flow control | Pause for human input (human-in-the-loop). |
| [`while`](/explore-analyze/workflows/steps/while.md) | Flow control | Loop while a condition holds. |
| [`workflow.execute`](/explore-analyze/workflows/steps/composition.md#workflow-execute) | Composition (tech preview) | Run a child workflow synchronously. |
| [`workflow.executeAsync`](/explore-analyze/workflows/steps/composition.md#workflow-executeasync) | Composition (tech preview) | Fire-and-forget child workflow. |
| [`workflow.fail`](/explore-analyze/workflows/steps/composition.md#workflow-fail) | Composition (tech preview) | Terminate the workflow as failed. |
| [`workflow.output`](/explore-analyze/workflows/steps/composition.md#workflow-output) | Composition (tech preview) | Emit the final outputs of a workflow. |

## External connector steps [workflows-external-connectors]

In addition to the steps listed previously, every configured {{kib}} connector exposes one or more `<connector>.<action>` step types. Common examples include:

- `slack.postMessage` — Post a message to a Slack channel.
- `jira.createIssue` — Create a Jira issue.
- `pagerduty.triggerIncident` — Page an on-call rotation.
- `virustotal.scanFileHash` — Scan a file hash.

Because the available connector steps depend on which connectors your deployment has configured, they aren't enumerated here. Refer to the [{{kib}} connectors reference](kibana://reference/connectors-kibana.md) for the full catalog.

## Deprecated step types [workflows-deprecated-steps]

These still work in existing workflows but can't be used in new ones. Refer to the [migration guide](/explore-analyze/workflows/authoring-techniques/migrate-from-9-3.md) for full replacement details.

| Deprecated | Replacement |
|---|---|
| `kibana.createCaseDefaultSpace` | [`cases.createCase`](/explore-analyze/workflows/steps/cases.md#cases-createcase) |
| `kibana.getCaseDefaultSpace` | [`cases.getCase`](/explore-analyze/workflows/steps/cases.md#cases-getcase) |
| `kibana.updateCaseDefaultSpace` | [`cases.updateCase`](/explore-analyze/workflows/steps/cases.md#cases-updatecase) |
| `kibana.addCaseCommentDefaultSpace` | [`cases.addComment`](/explore-analyze/workflows/steps/cases.md#cases-addcomment) |

## Related [workflows-step-types-related]

- [Steps overview](/explore-analyze/workflows/steps.md): Common fields every step accepts.
- [Cheat sheet](/explore-analyze/workflows/reference/cheat-sheet.md): Step menu organized by intent rather than alphabetically.
- [`elastic/workflows` library](https://github.com/elastic/workflows): 57 example workflows that exercise these step types.
