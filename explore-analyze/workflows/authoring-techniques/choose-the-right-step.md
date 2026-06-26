---
navigation_title: Choose the right step
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Decision aid for picking the right workflow step. Start from what you want to do; end at the step you need.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Choose the right step [workflows-choose-the-right-step]

Workflows ship with many step types. This page is keyed by intent: find the row that matches what you're trying to do; the right column gives you the step you need and links to its reference.

For an alphabetical catalog of every step type, refer to the [Step type index](/explore-analyze/workflows/reference/step-types.md).

## I want to… [workflows-choose-intent]

### Query or modify {{es}} data [workflows-choose-elasticsearch]

| Intent | Step |
|---|---|
| Run a Query DSL search | [`elasticsearch.search`](/explore-analyze/workflows/steps/elasticsearch.md) |
| Run an ES\|QL query | [`elasticsearch.esql.query`](/explore-analyze/workflows/steps/elasticsearch.md) |
| Index one document | [`elasticsearch.index`](/explore-analyze/workflows/steps/elasticsearch.md) |
| Index many documents efficiently | [`elasticsearch.bulk`](/explore-analyze/workflows/steps/elasticsearch.md) |
| Update a document | [`elasticsearch.update`](/explore-analyze/workflows/steps/elasticsearch.md) |
| Create, delete, or check an index | [`elasticsearch.indices.create`](/explore-analyze/workflows/steps/elasticsearch.md), [`elasticsearch.indices.delete`](/explore-analyze/workflows/steps/elasticsearch.md), [`elasticsearch.indices.exists`](/explore-analyze/workflows/steps/elasticsearch.md) |
| Call an {{es}} API not listed above | [`elasticsearch.request`](/explore-analyze/workflows/steps/elasticsearch.md) |

### Work with cases [workflows-choose-cases]

| Intent | Step |
|---|---|
| Create a case | [`cases.createCase`](/explore-analyze/workflows/steps/cases.md#cases-createcase) |
| Look up a case | [`cases.getCase`](/explore-analyze/workflows/steps/cases.md#cases-getcase), [`cases.findCases`](/explore-analyze/workflows/steps/cases.md#cases-findcases), [`cases.getCasesByAlertId`](/explore-analyze/workflows/steps/cases.md#cases-getcasesbyalertid) |
| Change status, severity, or tags | [`cases.updateCase`](/explore-analyze/workflows/steps/cases.md#cases-updatecase) or the field-specific `set*` steps |
| Attach alerts or observables | [`cases.addAlerts`](/explore-analyze/workflows/steps/cases.md#cases-addalerts), [`cases.addObservables`](/explore-analyze/workflows/steps/cases.md#cases-addobservables) |
| Add a comment | [`cases.addComment`](/explore-analyze/workflows/steps/cases.md#cases-addcomment) |
| Close the case | [`cases.closeCase`](/explore-analyze/workflows/steps/cases.md#cases-closecase) |
| Assign or unassign | [`cases.assignCase`](/explore-analyze/workflows/steps/cases.md#cases-assigncase), [`cases.unassignCase`](/explore-analyze/workflows/steps/cases.md#cases-unassigncase) |

The `kibana.*` case steps (`kibana.createCase`, `kibana.getCase`, `kibana.updateCase`, `kibana.addCaseComment`) are deprecated. Use the `cases.*` replacements. Refer to [Migrate workflows from 9.3 to 9.4](/explore-analyze/workflows/authoring-techniques/migrate-from-9-3.md).

### Manage detection alerts [workflows-choose-alerts]

| Intent | Step |
|---|---|
| Change alert status (`open`, `closed`, `acknowledged`, `in-progress`) | [`kibana.SetAlertsStatus`](/explore-analyze/workflows/steps/kibana.md) (PascalCase) |
| Add or remove tags on alerts | [`kibana.SetAlertTags`](/explore-analyze/workflows/steps/kibana.md) (PascalCase) |

### Call an external system [workflows-choose-external]

| Intent | Step |
|---|---|
| There's a dedicated {{kib}} connector (Slack, Jira, PagerDuty, and so on) | The connector's named step, for example [`slack.postMessage`](/explore-analyze/workflows/steps/external-systems-apps.md). |
| No dedicated connector, credentials matter | [`http`](/explore-analyze/workflows/steps/external-systems-apps.md) with a configured HTTP connector for secrets storage. |
| No dedicated connector, quick one-off | [`http`](/explore-analyze/workflows/steps/external-systems-apps.md) without a `connector-id`. |

### Branch or loop [workflows-choose-flow-control]

| Intent | Step |
|---|---|
| Conditional branch | [`if`](/explore-analyze/workflows/steps/if.md) |
| Multi-way dispatch on a value | [`switch`](/explore-analyze/workflows/steps/switch.md) |
| Iterate over an array | [`foreach`](/explore-analyze/workflows/steps/foreach.md) |
| Loop until a condition is false | [`while`](/explore-analyze/workflows/steps/while.md) |
| Fan out to independent executions | [`workflow.executeAsync`](/explore-analyze/workflows/steps/composition.md) |
| Exit or skip a loop iteration | [`loop.break`](/explore-analyze/workflows/steps/loop-break.md), [`loop.continue`](/explore-analyze/workflows/steps/loop-continue.md) |
| Small conditional on a single step | Step-level `if:` field. Refer to the [Steps overview](/explore-analyze/workflows/steps.md). |

### Pause [workflows-choose-pause]

| Intent | Step |
|---|---|
| Fixed-duration pause | [`wait`](/explore-analyze/workflows/steps/wait.md) |
| Pause for human input | [`waitForInput`](/explore-analyze/workflows/steps/wait-for-input.md). Refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md). |

### Transform data between steps [workflows-choose-transform]

| Intent | Step |
|---|---|
| Set a named variable | [`data.set`](/explore-analyze/workflows/steps/data.md#data-set) |
| Map each element of an array to a new shape | [`data.map`](/explore-analyze/workflows/steps/data.md#data-map) |
| Keep only matching elements | [`data.filter`](/explore-analyze/workflows/steps/data.md#data-filter) |
| Find the first matching element | [`data.find`](/explore-analyze/workflows/steps/data.md#data-find) |
| Group and aggregate | [`data.aggregate`](/explore-analyze/workflows/steps/data.md#data-aggregate) |
| Concatenate arrays | [`data.concat`](/explore-analyze/workflows/steps/data.md#data-concat) |
| Remove duplicates | [`data.dedupe`](/explore-analyze/workflows/steps/data.md#data-dedupe) |
| Parse or serialize JSON | [`data.parseJson`](/explore-analyze/workflows/steps/data.md#data-parsejson), [`data.stringifyJson`](/explore-analyze/workflows/steps/data.md#data-stringifyjson) |
| Extract or replace through regex | [`data.regexExtract`](/explore-analyze/workflows/steps/data.md#data-regexextract), [`data.regexReplace`](/explore-analyze/workflows/steps/data.md#data-regexreplace) |
| A small inline transform | [Liquid templating](/explore-analyze/workflows/templating.md), no step needed |

### Call an AI model [workflows-choose-ai]

| Intent | Step |
|---|---|
| General prompt, optionally with structured output | [`ai.prompt`](/explore-analyze/workflows/steps/ai-steps.md#ai-prompt) |
| Classify into a fixed category set | [`ai.classify`](/explore-analyze/workflows/steps/ai-steps.md#ai-classify) |
| Summarize content | [`ai.summarize`](/explore-analyze/workflows/steps/ai-steps.md#ai-summarize) |
| Invoke an {{agent-builder}} agent | [`ai.agent`](/explore-analyze/workflows/steps/ai-steps.md#ai-agent) |

### Call another workflow [workflows-choose-composition]

| Intent | Step |
|---|---|
| Synchronous: parent waits for the child's result | [`workflow.execute`](/explore-analyze/workflows/steps/composition.md) {applies_to}`stack: preview 9.4+` |
| Fire-and-forget | [`workflow.executeAsync`](/explore-analyze/workflows/steps/composition.md) {applies_to}`stack: preview 9.4+` |
| Emit outputs from a child workflow | [`workflow.output`](/explore-analyze/workflows/steps/composition.md) {applies_to}`stack: preview 9.4+` |
| Explicitly terminate a workflow as failed | [`workflow.fail`](/explore-analyze/workflows/steps/composition.md) {applies_to}`stack: preview 9.4+` |

### Log or debug [workflows-choose-debug]

| Intent | Step |
|---|---|
| Log a message to the execution view | [`console`](/explore-analyze/workflows/steps/external-systems-apps.md) |
| Understand what a step produced mid-run | Inspect the step's output in the execution view. Refer to [Monitor workflow execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md). |
| Log only when running a test | `console` with a step-level `if: "execution.isTestRun"` |

## Still not sure? [workflows-choose-still-not-sure]

Browse the [Step type index](/explore-analyze/workflows/reference/step-types.md) for an A-to-Z list, or use the YAML editor's autocomplete in {{kib}}. The autocomplete surfaces every step type with its description as you type.

## Related [workflows-choose-related]

- [Anatomy of a workflow](/explore-analyze/workflows/authoring-techniques/anatomy.md): Every top-level field and the execution lifecycle.
- [Steps overview](/explore-analyze/workflows/steps.md): The step catalog organized by category.
- [Step type index](/explore-analyze/workflows/reference/step-types.md): Alphabetical lookup for every step type.
- [Cheat sheet](/explore-analyze/workflows/reference/cheat-sheet.md): One-page bookmark reference.
