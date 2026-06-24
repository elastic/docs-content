---
navigation_title: Troubleshooting
description: Resolve common issues with Elastic Workflows. Trigger attachment, flow control, case and alert steps, Liquid filters, AI connector IDs, composition, human-in-the-loop, and concurrency.
applies_to:
  stack: ga 9.4+
  serverless: ga
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Troubleshoot workflows [workflows-troubleshooting]

Quick answers to the issues first-time workflow authors hit most often. Each section states the symptom, the cause, and the resolution.

## Triggers [workflows-ts-triggers]

### An alert workflow never fires [workflows-ts-alert-never-fires]

**Symptom.** You've authored a workflow with `type: alert` and enabled it, but the workflow never runs when the expected alerts fire.

**Cause.** Declaring the trigger is necessary but not sufficient. The workflow must also be attached to the alerting or detection rule's **Actions** with a **Run Workflow** action. Without the attachment, alerts fire from the rule but the workflow is never invoked.

**Resolution.** Open the rule, add a **Run Workflow** action, and select the workflow. Refer to [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md) for the full setup sequence.

### A scheduled workflow stopped firing [workflows-ts-scheduled-stopped]

**Symptom.** A previously working scheduled workflow stops executing.

**Cause.** One of three common causes:

1. The workflow was disabled (`enabled: false`).
2. The interval is shorter than 1 minute. The minimum interval is `1m` / `60s`; schedules with sub-minute intervals from earlier versions were auto-migrated on first edit.
3. A `drop` concurrency strategy is skipping new runs while a prior run is still executing.

**Resolution.** Verify the workflow is enabled, check the interval in the YAML editor, and review execution history for `skipped` entries. For concurrency details, refer to [Settings concurrency control](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md).

### A `workflows.failed` trigger rejects `condition` at the top level [workflows-ts-workflows-failed-condition]

**Symptom.** The workflow editor rejects a `workflows.failed` trigger when `condition` is placed directly under the trigger.

**Cause.** The condition belongs under an `on:` block, not at the trigger top level.

**Resolution.** Nest the condition under `on:`:

```yaml
triggers:
  - type: workflows.failed
    on:
      condition: "event.workflow.name : 'ops--rollback-deployment'"
```

Refer to [Event-driven triggers](/explore-analyze/workflows/triggers/event-driven-triggers.md).

## Flow control [workflows-ts-flow-control]

### A `while` loop stopped silently after 2000 iterations [workflows-ts-while-cap]

**Symptom.** A `while` loop exits without an error after exactly 2000 iterations, even though the work isn't done.

**Cause.** `max-iterations` defaults to 2000, and the default `on-limit` is `continue` — so the step **succeeds quietly** when the cap is reached, instead of failing the workflow.

**Resolution.** Set `max-iterations` explicitly with `on-limit: fail` to make the workflow fail when the cap is hit:

```yaml
- name: poll
  type: while
  condition: "steps.check.output.status : 'pending'"
  max-iterations:
    limit: 10000
    on-limit: fail
  steps:
    - ...
```

Refer to [`while`](/explore-analyze/workflows/steps/while.md).

### A `switch` step errors on save [workflows-ts-switch-shape]

**Symptom.** A `switch` step fails validation at save time.

**Cause.** The `cases` block is an array of objects, not a map.

**Resolution.** Structure `cases` as an array where each entry has `case:` and `steps:`:

```yaml
# Wrong
cases:
  foo:
    - { ... }
  bar:
    - { ... }

# Right
cases:
  - case: foo
    steps: [ { ... } ]
  - case: bar
    steps: [ { ... } ]
```

Refer to [`switch`](/explore-analyze/workflows/steps/switch.md).

### `foreach` can't find the array [workflows-ts-foreach-array]

**Symptom.** A `foreach` loop errors or processes nothing.

**Cause.** The `foreach` value must be a Liquid expression that evaluates to an array. When passing a non-string value (an array or object), use the raw-value form `${{ ... }}` so the value isn't stringified.

**Resolution.** For step-level iteration or the `foreach` step:

```yaml
- name: process
  foreach: "${{ event.alerts }}"    # raw-value form for an array
  steps: [ ... ]
```

Inside the loop, reference items as `foreach.item`, `foreach.index`, and `foreach.total`. Refer to [`foreach`](/explore-analyze/workflows/steps/foreach.md).

## Cases and alerts [workflows-ts-cases-alerts]

### `cases.addAlerts` rejects the `alerts` parameter [workflows-ts-addalerts-shape]

**Symptom.** `cases.addAlerts` fails validation with an `alerts` parameter error.

**Cause.** The `alerts` parameter takes an array of objects (each with `alertId` and `index`), not an array of ID strings.

**Resolution.**

```yaml
- name: attach
  type: cases.addAlerts
  with:
    case_id: "{{ steps.case.output.id }}"
    alerts:
      - alertId: "{{ event.alerts[0]._id }}"
        index:   "{{ event.alerts[0]._index }}"
        rule:
          id:   "{{ event.rule.id }}"
          name: "{{ event.rule.name }}"
```

Refer to [`cases.addAlerts`](/explore-analyze/workflows/steps/cases.md#cases-addalerts).

### `kibana.SetAlertsStatus` step type is rejected [workflows-ts-pascal-case]

**Symptom.** The workflow editor reports an unknown step type for `kibana.set_alerts_status` or similar.

**Cause.** The alert-management step types use PascalCase. Step type IDs are case-sensitive.

**Resolution.** Use the correct case:

- `kibana.SetAlertsStatus`
- `kibana.SetAlertTags`

Refer to [{{kib}} action steps](/explore-analyze/workflows/steps/kibana.md).

### `cases.closeCase` rejects a `reason` field [workflows-ts-closecase-reason]

**Symptom.** `cases.closeCase` fails validation when a `reason` parameter is included.

**Cause.** `cases.closeCase` doesn't accept a `reason` parameter.

**Resolution.** Document the reason with a `cases.addComment` call before closing:

```yaml
- name: note_why
  type: cases.addComment
  with:
    case_id: "{{ steps.case.output.id }}"
    comment: "Closing: confirmed duplicate of case XXX."

- name: close
  type: cases.closeCase
  with:
    case_id: "{{ steps.case.output.id }}"
```

Refer to [`cases.closeCase`](/explore-analyze/workflows/steps/cases.md#cases-closecase).

## Liquid and data flow [workflows-ts-liquid]

### `to_json` filter not found [workflows-ts-to-json]

**Symptom.** A Liquid expression using `to_json` fails with an unknown-filter error.

**Cause.** `to_json` doesn't exist. The workflow engine provides `json` to serialize and `json_parse` to parse.

**Resolution.**

```yaml
# Serialize a value to a JSON string
payload: "{{ event.alerts[0] | json }}"

# Parse a JSON string into an object
parsed: "{{ steps.http.output.body | json_parse }}"
```

Refer to [Liquid filters](/explore-analyze/workflows/reference/liquid-filters.md).

### An array is passed as a string [workflows-ts-array-string]

**Symptom.** A step expects an array but receives a stringified version of it, and the step fails validation.

**Cause.** The expression used `{{ ... }}` (string form) instead of `${{ ... }}` (raw-value form). The string form stringifies the value.

**Resolution.**

```yaml
# Wrong — renders the array as a string
items: "{{ event.alerts }}"

# Right — passes the array as an array
items: "${{ event.alerts }}"
```

Refer to [Templating engine](/explore-analyze/workflows/templating.md).

### `data.filter` condition is rejected [workflows-ts-filter-kql]

**Symptom.** A `data.filter` step fails with an invalid-condition error.

**Cause.** The `condition` field uses {{kib}} Query Language (KQL), not Liquid comparison syntax. KQL uses `:` for equality.

**Resolution.**

```yaml
# Wrong — Liquid comparison
condition: "item.severity == 'critical'"

# Right — KQL equality
condition: "item.severity : 'critical'"
```

The same applies to the `if` step's `condition`. Refer to [`data.filter`](/explore-analyze/workflows/steps/data.md#data-filter).

### A Liquid template fails with a rendering limit error [workflows-ts-liquid-limits]

**Symptom.** A step that renders a large template — often a `console` report — fails with an error such as `memory alloc limit exceeded`, `parse length limit exceeded`, or `render limit exceeded`.

**Cause.** The templating engine caps the size, render time, and memory of each template render. A template that builds a large string, such as a final report that concatenates thousands of rows, can exceed one of these limits.

**Resolution.** Reduce the size of the rendered output by returning structured data or write results to an index instead of formatting one large string, and move heavy filtering or grouping into [`data.*` steps](/explore-analyze/workflows/steps/data.md). Refer to [Template rendering limits](/explore-analyze/workflows/templating.md#workflows-template-limits).

## AI steps [workflows-ts-ai]

### An AI step rejects `connectorId` [workflows-ts-ai-connector-id]

**Symptom.** An `ai.prompt`, `ai.classify`, `ai.summarize`, or `ai.agent` step fails validation on `connectorId` or `connector_id`.

**Cause.** The parameter is `connector-id` (kebab-case) and lives at the step top level, not inside `with`.

**Resolution.**

```yaml
# Wrong
- type: ai.prompt
  with:
    connectorId: "my-openai"
    prompt: "..."

# Right
- type: ai.prompt
  connector-id: "my-openai"
  with:
    prompt: "..."
```

The same pattern applies to `agent-id` and `inference-id` on AI steps. Refer to [AI steps](/explore-analyze/workflows/steps/ai-steps.md).

### `ai.summarize` rejects `content` [workflows-ts-summarize-input]

**Symptom.** An `ai.summarize` step fails validation on the `content` parameter.

**Cause.** The input parameter is named `input`, not `content`.

**Resolution.**

```yaml
- type: ai.summarize
  connector-id: "..."
  with:
    input: "${{ steps.gather.output }}"
```

Refer to [`ai.summarize`](/explore-analyze/workflows/steps/ai-steps.md#ai-summarize).

### Templated `agent-id` or `connector-id` isn't substituted [workflows-ts-ai-top-level-templating]
```{applies_to}
stack: ga 9.3-9.4
```

**Symptom.** An AI step fails because a referenced resource (for example, an agent or connector) isn't found, even though the value is correctly defined in `consts:`.

**Cause.** Liquid expressions are evaluated only inside the step's `with:` block. On fields outside `with:`, including `agent-id`, `connector-id`, `inference-id`, and `conversation-id`, the engine sends the text to the runtime as-is. So `agent-id: "{{ consts.agent_id }}"` arrives at the API as the literal text `{{ consts.agent_id }}`, instead of being substituted with the value of `consts.agent_id`. Workflows 9.5 adds top-level field templating, so this limitation applies to 9.3 and 9.4 only.

**Resolution.** Use literal values in top-level fields. For `ai.agent`, drop `connector-id` entirely (the agent encodes its connector). For fields that need templating, place them inside `with:` in snake-case (for example, `conversation_id`). On 9.5 and later, top-level templating resolves, but a literal value keeps an example portable across all versions.

```yaml
# Not evaluated on 9.3-9.4; resolves on 9.5+
- type: ai.agent
  agent-id: "{{ consts.agent_id }}"
  connector-id: "{{ consts.connector_id }}"
  with:
    message: "..."

# Portable: a literal value works on all versions
- type: ai.agent
  agent-id: elastic-ai-agent
  with:
    message: "..."
```

Fixed in 9.5 ([elastic/security-team#17236](https://github.com/elastic/security-team/issues/17236)).

## Composition [workflows-ts-composition]

### `workflow.execute` rejects `workflow_id` [workflows-ts-workflow-id]

**Symptom.** A `workflow.execute` or `workflow.executeAsync` step fails validation on the `workflow_id` or `workflowId` parameter.

**Cause.** The parameter is `workflow-id` (kebab-case), and it lives inside `with`. Composition steps are the one exception to the top-level-kebab-case convention used by AI steps.

**Resolution.**

```yaml
- name: run_child
  type: workflow.execute
  with:
    workflow-id: "shared--enrich-documents"
    inputs:
      documents: "${{ event.alerts }}"
```

Refer to [Composition steps](/explore-analyze/workflows/steps/composition.md).

## Human-in-the-loop [workflows-ts-hitl]

### A paused execution is stuck [workflows-ts-hitl-stuck]

**Symptom.** A workflow paused by `waitForInput` never resumes.

**Cause.** `waitForInput` doesn't time out by default. The workflow waits indefinitely until someone submits the resume form or calls the resume API.

**Resolution.** To limit the wait, set a workflow-level `settings.timeout`. The workflow cancels when the timeout elapses.

```yaml
settings:
  timeout: "24h"
```

Refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md).

## Execution and concurrency [workflows-ts-execution]

### An execution was `skipped` [workflows-ts-execution-skipped]

**Symptom.** An execution appears in history with state `skipped`.

**Cause.** The workflow's `concurrency.strategy` is `drop` and another execution was already running for the same `key` when this one was due to start.

**Resolution.** This is the intended behavior of `drop`. If you want the new run to cancel the old one instead, use `strategy: cancel-in-progress`.

```yaml
settings:
  concurrency:
    key: "{{ event.alerts[0].host.name }}"
    strategy: cancel-in-progress
    max: 1
```

### A workflow cancelled mid-execution [workflows-ts-execution-cancelled]

**Symptom.** A workflow terminated with a `cancelled` state.

**Cause.** One of:

- `settings.timeout` — The workflow's overall time budget was exceeded.
- Concurrency with `cancel-in-progress` — A new execution kicked this one out.
- Operator cancel — Someone clicked **Cancel all** in the UI.

**Resolution.** The execution view shows the cancellation reason on the terminal state. Review it and adjust `settings.timeout` or the concurrency strategy if needed.

## Setup and permissions [workflows-ts-setup]

### You can't create workflows [workflows-ts-create-permission]

**Symptom.** The **Create a new workflow** button is disabled, or the editor rejects save attempts.

**Cause.** Your user role is missing one of the Workflows feature privileges.

**Resolution.** Ensure your role has at least `All` on the **Analytics > Workflows** feature. For finer-grained access, use the sub-feature privileges: `create`, `read`, `update`, `delete`, `execute`, `readExecution`, and `cancelExecution`. Refer to [Setup](/explore-analyze/workflows/get-started/setup.md).

### Workflows isn't visible in {{kib}} [workflows-ts-ui-missing]

**Symptom.** The **Workflows** navigation entry doesn't appear in {{kib}}.

**Cause.** The `workflows:ui:enabled` advanced setting has been disabled, or the deployment doesn't have the required license or subscription tier.

**Resolution.** `workflows:ui:enabled` defaults to `true`. If it has been explicitly disabled, re-enable it in **Advanced settings**. Confirm the deployment is on a supported tier (Enterprise license on Elastic Cloud Hosted or self-managed, or a Serverless project of the required type). Refer to [Setup](/explore-analyze/workflows/get-started/setup.md).

## Still stuck [workflows-ts-still-stuck]

- Search this documentation for error messages or parameter names.
- Review the [Cheat sheet](/explore-analyze/workflows/reference/cheat-sheet.md) for quick syntax references.
- Review the [Step type index](/explore-analyze/workflows/reference/step-types.md) for the full catalog.
- File an issue on the [{{kib}} GitHub repo](https://github.com/elastic/kibana/issues/new/choose) with a minimal reproduction.

% Ben Ironside Goldstein, 2026-05-04: The following PM claims were reconciled with the
% Kibana schema source:
%   - PM: "workflows.failed condition lives under on:" — confirmed by Tinsae in PR review.
%   - PM: "while default max-iterations: 2000 with on-limit: continue" — confirmed against
%     DEFAULT_LOOP_MAX_ITERATIONS in kbn-workflows/spec/schema.ts. PR A's earlier "no default"
%     claim was incorrect and has been reverted in this PR.
%   - PM: Resume API wraps body in { "input": {...} } and path /api/workflows/executions —
%     PR A: flat body, path /api/workflowExecutions/{id}/resume. Still pending SME
%     reconfirmation.
%   - PM: cases.setCustomField / cases.createCaseFromTemplate "not registered" — PR A: both
%     are registered in 9.4 GA.
