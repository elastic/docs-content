---
navigation_title: Glossary
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Reference of terms used across Elastic Workflows documentation, with links to the canonical reference pages.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Glossary [workflows-glossary]

Every term and acronym used in the Workflows documentation. Each entry links to the canonical reference page where one exists.

## A-B [workflows-glossary-a-b]

### Action [workflows-glossary-action]

In alerting, an operation a rule takes when it fires. Workflows runs as an action through the **Run workflow** rule action. Refer to [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md).

### Agent Builder [workflows-glossary-agent-builder]

A {{kib}} feature for building conversational AI agents. Workflows integrates as a tool provider (workflows can be called by agents) and as a step type (`ai.agent` calls agents from a workflow). Refer to [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md).

### Alert [workflows-glossary-alert]

A document produced by an alerting rule when it fires. Refer to [Detection alert](#workflows-glossary-detection-alert).

### Alert state [workflows-glossary-alert-state]

One of `new`, `ongoing`, or `recovered`. Workflows can trigger on any combination of these states. Refer to [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md).

### Alerting rule [workflows-glossary-alerting-rule]

A {{kib}} construct that watches data and fires when a condition is met. Triggers alert-type workflows. Refer to [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md).

### Anatomy [workflows-glossary-anatomy]

The top-level structure of a workflow YAML file. Refer to [Anatomy of a workflow](/explore-analyze/workflows/authoring-techniques/anatomy.md).

## C [workflows-glossary-c]

### Case [workflows-glossary-case]

A {{kib}} Cases document for tracking an investigation. Workflows provides 25+ `cases.*` step types. Refer to [Cases action steps](/explore-analyze/workflows/steps/cases.md).

### Composition [workflows-glossary-composition]

```{applies_to}
stack: preview 9.4+
serverless: preview
```

Invoking one workflow from another. The parent calls a child through `workflow.execute` (synchronous) or `workflow.executeAsync` (fire-and-forget). Refer to [Composition steps](/explore-analyze/workflows/steps/composition.md) and [Compose workflows](/explore-analyze/workflows/authoring-techniques/compose-workflows.md).

### Composition depth [workflows-glossary-composition-depth]

How deep a nested `workflow.execute` chain goes. Capped by the engine to prevent infinite recursion. Refer to [Composition steps](/explore-analyze/workflows/steps/composition.md).

### Concurrency [workflows-glossary-concurrency]

Controls for what happens when overlapping executions would otherwise run at the same time. Configured under `settings.concurrency`. Refer to [Workflow settings](/explore-analyze/workflows/authoring-techniques/settings.md).

### Connector [workflows-glossary-connector]

A configured integration with an external system (Slack, Jira, PagerDuty, OpenAI, and so on). Referenced from workflow steps by `connector-id`. Refer to [{{kib}} connectors](/deploy-manage/manage-connectors.md).

### Context [workflows-glossary-context]

The shared data environment a workflow execution builds up as steps run. Accessed in YAML through Liquid templating. Refer to [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md).

### Context variable [workflows-glossary-context-variable]

A named item in the workflow context: `inputs.*`, `consts.*`, `steps.*`, `event.*`, `foreach.*`, `execution.*`, and so on. Refer to [Context variables](/explore-analyze/workflows/reference/context-variables.md).

## D-E [workflows-glossary-d-e]

### Data step [workflows-glossary-data-step]

A step type in the `data.*` namespace for transformations: `data.filter`, `data.map`, `data.aggregate`, and others. Refer to [Data action steps](/explore-analyze/workflows/steps/data.md).

### Detection alert [workflows-glossary-detection-alert]

An alert produced by a {{elastic-sec}} detection rule. Always in state `new` when delivered to a workflow. Refer to [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md).

### ES|QL [workflows-glossary-esql]

Elasticsearch Query Language. {{es}}'s SQL-like query language. Used in `elasticsearch.esql.query` steps. Refer to [Elasticsearch action steps](/explore-analyze/workflows/steps/elasticsearch.md) and [ES|QL reference](elasticsearch://reference/query-languages/esql.md).

### Event [workflows-glossary-event]

The trigger payload. For alert triggers, the alert data; for scheduled triggers, empty. Accessed as `event.*` in Liquid templates. Refer to [Context variables](/explore-analyze/workflows/reference/context-variables.md).

### Event-driven trigger [workflows-glossary-event-driven-trigger]

```{applies_to}
stack: preview 9.4+
serverless: preview
```

A trigger that fires on a platform event rather than on a schedule or manual invocation. Includes `workflows.failed` and the `cases.*` event triggers. Refer to [Event-driven triggers](/explore-analyze/workflows/triggers/event-driven-triggers.md).

### Execution [workflows-glossary-execution]

One run of a workflow. Has an ID, a start time, a trigger, a terminal state, and an execution view. Refer to [Monitor workflow execution](/explore-analyze/workflows/authoring-techniques/monitor-workflows.md).

## F-H [workflows-glossary-f-h]

### Fallback [workflows-glossary-fallback]

An `on-failure` strategy that runs alternative steps when the primary step fails and all retries are exhausted. Refer to [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md).

### Fan-out [workflows-glossary-fan-out]

Starting multiple concurrent pieces of work from one workflow. Implement with [`workflow.executeAsync`](/explore-analyze/workflows/steps/composition.md) for independent child executions, or [`foreach`](/explore-analyze/workflows/steps/foreach.md) for per-item iteration within one execution.

### Foreach [workflows-glossary-foreach]

Both a step type and a step-level field. The step type is a loop; the field is a per-step iteration modifier. Refer to [`foreach`](/explore-analyze/workflows/steps/foreach.md) and the [Steps overview](/explore-analyze/workflows/steps.md).

### GenAI [workflows-glossary-genai]

Generative AI. A model class that produces text, code, or structured data from a prompt. Workflows integrates through connectors (OpenAI, Bedrock, Gemini, Generic GenAI) and the `ai.*` step types. Refer to [AI steps](/explore-analyze/workflows/steps/ai-steps.md).

### HITL [workflows-glossary-hitl]

Human-in-the-loop. A workflow that pauses for human input, typically through `waitForInput`. Refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md).

## I-K [workflows-glossary-i-k]

### Input [workflows-glossary-input]

A runtime parameter of a workflow. Declared under the `manual` trigger on 9.5+ and serverless, or at the workflow root on 9.4. Refer to [Anatomy: `inputs`](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-inputs).

### KQL [workflows-glossary-kql]

{{kib}} Query Language. Used for `if` conditions and `data.filter` predicates in workflows. Refer to the [KQL reference](/explore-analyze/query-filter/languages/kql.md).

## L [workflows-glossary-l]

### Liquid [workflows-glossary-liquid]

The template language used to reference context variables inside workflow YAML. The engine evaluates expressions like `{{ inputs.name }}` and `${{ steps.fetch.output }}` at runtime. Refer to [Templating engine](/explore-analyze/workflows/templating.md).

## N-O [workflows-glossary-n-o]

### Observable [workflows-glossary-observable]

In Cases, an indicator of compromise (IP, hash, domain, URL). Added with `cases.addObservables`. Refer to [`cases.addObservables`](/explore-analyze/workflows/steps/cases.md#cases-addobservables).

### On-failure [workflows-glossary-on-failure]

Per-step error-handling configuration. Strategies: `retry`, `continue`, `fallback`, `abort`. Refer to [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md).

### Output [workflows-glossary-output]

Either the data a step produces (accessed through `steps.<name>.output`), or a top-level declaration of what a workflow returns (required for workflows invoked through composition). Refer to [Anatomy: `outputs`](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-outputs).

## P-R [workflows-glossary-p-r]

### RBAC [workflows-glossary-rbac]

Role-based access control. {{kib}}'s privilege system. Workflows defines seven sub-feature privileges (`create`, `read`, `update`, `delete`, `execute`, `readExecution`, `cancelExecution`). Refer to [Set up Workflows](/explore-analyze/workflows/get-started/setup.md).

### Resume [workflows-glossary-resume]

Continuing a paused workflow after a `waitForInput` step. Done through the UI or the REST API. Refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md).

### Retry [workflows-glossary-retry]

An `on-failure` strategy that re-runs a step. Supports exponential backoff, jitter, and per-error conditions. Refer to [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md).

### RRule [workflows-glossary-rrule]

Recurrence Rule. The iCalendar recurrence specification. Scheduled triggers accept rules for calendar-style recurrence. Refer to [Scheduled triggers](/explore-analyze/workflows/triggers/scheduled-triggers.md).

## S [workflows-glossary-s]

### Scheduled trigger [workflows-glossary-scheduled-trigger]

A trigger that runs a workflow on a time-based schedule. Refer to [Scheduled triggers](/explore-analyze/workflows/triggers/scheduled-triggers.md).

### Schema (output) [workflows-glossary-schema-output]

The declared shape of a workflow's outputs. Required for workflows invoked through `workflow.execute`. The engine validates child outputs against this schema before returning them to the parent. Refer to [Anatomy: `outputs`](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-outputs).

### Space [workflows-glossary-space]

A {{kib}} tenancy construct. Workflows belong to spaces; triggers and connectors scope to the space.

### Step [workflows-glossary-step]

One unit of work in a workflow. Has a `name`, a `type`, and step-specific parameters. Refer to the [Steps overview](/explore-analyze/workflows/steps.md).

### Step type [workflows-glossary-step-type]

The identifier of a particular kind of step (`elasticsearch.search`, `cases.createCase`, and so on). Refer to the [Step type index](/explore-analyze/workflows/reference/step-types.md).

### Streams [workflows-glossary-streams]

```{applies_to}
stack: preview 9.4+
serverless: preview
```

A {{kib}} Observability feature. Workflow steps in the `kibana.streams.*` namespace operate on Observability streams. Refer to [Streams action steps](/explore-analyze/workflows/steps/streams.md).

## T [workflows-glossary-t]

### Tech Preview [workflows-glossary-tech-preview]

A stability level. Features are usable and documented, but the schema or behavior can change in future releases. Marked with `applies_to: <product>: preview` in this docset; the badge appears at the top of each affected page and beside the navigation entry.

### Terminal state [workflows-glossary-terminal-state]

An execution's final state. One of `completed`, `failed`, `cancelled`, `timed_out`, or `skipped`. Refer to [Anatomy: execution lifecycle](/explore-analyze/workflows/authoring-techniques/anatomy.md#workflows-anatomy-lifecycle).

### Trigger [workflows-glossary-trigger]

What starts a workflow. Supported types: `manual`, `scheduled`, `alert`, `workflows.failed`, and the `cases.*` event-driven triggers. Refer to [Triggers](/explore-analyze/workflows/triggers.md).

## V-W [workflows-glossary-v-w]

### Variables [workflows-glossary-variables]

Named values set by `data.set` steps. Global within an execution. Accessed as `variables.<name>`. Refer to [`data.set`](/explore-analyze/workflows/steps/data.md#data-set).

### waitForApproval [workflows-glossary-wait-for-approval]

```{applies_to}
stack: preview 9.5+
serverless: preview
```

A human-in-the-loop step that pauses a workflow for an approve or reject decision. Refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md) and [`waitForApproval`](/explore-analyze/workflows/steps/wait-for-approval.md).

### waitForInput [workflows-glossary-wait-for-input]

The human-in-the-loop primitive. Pauses a workflow for human input. Refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md) and [`waitForInput`](/explore-analyze/workflows/steps/wait-for-input.md).

### Workflow [workflows-glossary-workflow]

A declarative YAML automation. The primary unit of work in Elastic Workflows. Refer to [Anatomy of a workflow](/explore-analyze/workflows/authoring-techniques/anatomy.md).

### `workflows.failed` [workflows-glossary-workflows-failed]

```{applies_to}
stack: preview 9.4+
serverless: preview
```

An [event-driven trigger](/explore-analyze/workflows/triggers/event-driven-triggers.md) that fires when another workflow's execution reaches the `failed` terminal state. Used to build handler workflows that react to failures.

## Y [workflows-glossary-y]

### YAML [workflows-glossary-yaml]

YAML Ain't Markup Language. The format in which workflows are authored. Whitespace-sensitive.

## Related [workflows-glossary-related]

- [Cheat sheet](/explore-analyze/workflows/reference/cheat-sheet.md): One-page bookmark reference for the YAML shape, common patterns, and top gotchas.
- [Step type index](/explore-analyze/workflows/reference/step-types.md): Alphabetical catalog of every step type.
- [Context variables](/explore-analyze/workflows/reference/context-variables.md): Every variable you can reference in a Liquid expression.
- [Liquid filters](/explore-analyze/workflows/reference/liquid-filters.md): Filters available in workflow expressions.
