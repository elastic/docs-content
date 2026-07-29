---
navigation_title: Cheat sheet
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: One-page bookmark reference for Elastic Workflows. Workflow anatomy, triggers, step skeleton, the step menu, Liquid, error handling, and the top gotchas.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Workflows cheat sheet [workflows-cheat-sheet]

One-page reference. Bookmark this.

## Workflow anatomy [workflows-cheat-anatomy]

```yaml
name: my-workflow
description: ...
enabled: true
tags: [team, domain]
version: "1"

triggers: [ ... ]        # required
inputs: [ ... ]          # optional
consts: { ... }          # optional
outputs: [ ... ]         # required only for composed workflows
settings: { ... }        # optional
steps: [ ... ]           # required
```

Full reference: [Anatomy of a workflow](/explore-analyze/workflows/authoring-techniques/anatomy.md).

## Triggers [workflows-cheat-triggers]

```yaml
triggers:
  - type: manual

  - type: scheduled
    with:
      every: "5m"                      # or: rrule with freq DAILY/WEEKLY/MONTHLY

  - type: alert                        # requires rule Action attachment

  - type: workflows.failed             # tech preview
    on:
      condition: "event.workflow.name : 'critical-ingest-pipeline'"

  - type: cases.caseCreated            # tech preview (9.5+)
    on:
      condition: 'event.owner: "securitySolution"'
```

The full cases trigger family also includes `cases.caseUpdated`, `cases.caseStatusUpdated`, `cases.attachmentsAdded`, and `cases.commentsAdded`. Refer to [Event-driven triggers](/explore-analyze/workflows/triggers/event-driven-triggers.md).

Minimum schedule interval: **1 minute**. Refer to [Triggers](/explore-analyze/workflows/triggers.md).

## Step skeleton [workflows-cheat-step-skeleton]

```yaml
- name: my_step                        # unique within the workflow
  type: some.step_type
  connector-id: "my-connector"         # top-level, kebab-case (for connector and AI steps)
  if: "inputs.run_me : true"           # step-level KQL guard
  foreach: "{{ some.array }}"          # step-level iteration
  timeout: "30s"
  on-failure:
    retry:
      max-attempts: 3
      delay: "5s"
      strategy: exponential
    continue: true
  with:
    # step-specific parameters.
    # Note: workflow.execute / workflow.executeAsync use `workflow-id` INSIDE `with`.
```

## Step menu by intent [workflows-cheat-step-menu]

| Want to… | Use |
|---|---|
| Query {{es}} | `elasticsearch.search`, `elasticsearch.esql.query` |
| Write to {{es}} | `elasticsearch.index`, `elasticsearch.bulk`, `elasticsearch.update` |
| Manage cases | `cases.createCase`, `cases.updateCase`, `cases.addComment`, `cases.addAlerts`, `cases.pushCases` |
| Manage alerts | `security.setAlertStatus`, `security.setAlertTags`, `security.assignAlert` (preferred); `kibana.SetAlertsStatus`, `kibana.SetAlertTags` (PascalCase) |
| Manage attacks | `security.setAttackStatus`, `security.setAttackTags`, `security.assignAttack` |
| Enable or disable detection rules | `security.enableRule`, `security.disableRule` |
| Call an API | `http` (with optional `connector-id`) |
| Call a service | `<connector>.<action>` (for example, `slack.postMessage`, `jira.createIssue`) |
| Branch | `if`, `switch` |
| Loop | `foreach`, `while`, `loop.break`, `loop.continue` |
| Fan out to independent executions | `workflow.executeAsync` (tech preview) |
| Pause | `wait`, `waitForInput` |
| Transform data | `data.filter`, `data.map`, `data.aggregate`, `data.parseJson`, `data.regexExtract` |
| Call AI | `ai.prompt`, `ai.classify`, `ai.summarize`, `ai.agent` |
| Call another workflow | `workflow.execute` (synchronous), `workflow.executeAsync` (asynchronous, tech preview) |
| Log | `console` |

Full list: [Step type index](/explore-analyze/workflows/reference/step-types.md).

## Liquid quick reference [workflows-cheat-liquid]

```yaml
"{{ expr }}"             # string interpolation
"${{ expr }}"            # raw-value (arrays, objects, booleans, numbers)
```

Top-10 patterns:

```yaml
"{{ inputs.name }}"                                           # read an input
"{{ steps.search.output.hits.total.value }}"                  # read a step output
"{{ event.alerts[0].host.name }}"                             # read trigger payload
"{{ foreach.item._id }}"                                      # inside foreach
"{{ variables.threshold }}"                                   # read a data.set variable
"{{ now | date: '%Y-%m-%d' }}"                                # formatted timestamp
"{{ steps.x.output.body | json_parse }}"                      # parse a JSON string
"{{ event | json }}"                                          # serialize to JSON string
"{{ event.alerts[0].host.name | default: 'unknown' }}"        # fallback
"${{ event.alerts | where: 'severity', 'critical' }}"         # filter inline
```

Full reference: [Liquid filters](/explore-analyze/workflows/reference/liquid-filters.md).

## Context variables at a glance [workflows-cheat-context]

| Variable | Contains |
|---|---|
| `inputs.*` | Workflow inputs at runtime. |
| `consts.*` | Constants from workflow top. |
| `steps.<name>.output` | Output of a previous step. |
| `steps.<name>.error` | Error if that step failed (with `on-failure: continue`). |
| `event.*` | Trigger payload. |
| `execution.*` | Current execution metadata. |
| `workflow.*` | Workflow metadata. |
| `foreach.*` | Loop context: `item`, `index`, `total`, `items`. |
| `while.iteration` | Zero-based iteration counter inside a `while` loop. |
| `variables.*` | Variables set by `data.set`. |
| `now`, `kibanaUrl` | Standard helpers. |

Full reference: [Context variables](/explore-analyze/workflows/reference/context-variables.md).

## Error-handling strategies [workflows-cheat-errors]

```yaml
on-failure:
  retry:
    max-attempts: 3
    delay: "5s"
    strategy: exponential         # or "fixed"
    jitter: true
    condition: "steps.self.error.status : 429"    # KQL
  continue: true                                  # log and move on
  fallback: [ ... ]                               # graceful degradation
  # abort is the default when no on-failure is set
```

Precedence: per-step `on-failure` > workflow-level `settings.on-failure` > `abort`.

For cross-workflow error handling (page on-call when another workflow fails), use the [`workflows.failed` event-driven trigger](/explore-analyze/workflows/triggers/event-driven-triggers.md).

Full reference: [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md).

## Top gotchas [workflows-cheat-gotchas]

1. **Alert trigger needs rule Action attachment.** `type: alert` alone isn't enough. [Attach the workflow](/explore-analyze/workflows/triggers/alert-triggers.md) to the rule's Actions.

2. **`while` defaults to `max-iterations: 2000` with `on-limit: continue`.** When the loop hits the cap, the step succeeds quietly. Set `on-limit: fail` if you want the workflow to fail at the cap.

   ```yaml
   - name: poll_status
     type: while
     condition: "steps.check.output.status != 'ready'"
     max-iterations:
       limit: 100
       on-limit: fail        # Fail the workflow at the cap; default is continue
     steps:
       - name: check
         type: http
         with:
           url: "https://api.example.com/jobs/{{ inputs.job_id }}"
   ```

3. **`switch.cases` is an array**, not a map. Each case is a `{ case: <value>, steps: [...] }` object. Refer to [`switch`](/explore-analyze/workflows/steps/switch.md).

   ```yaml
   - name: route
     type: switch
     expression: "{{ steps.classify.output.severity }}"
     cases:
       - case: critical
         steps:
           - name: page_oncall
             type: pagerduty.triggerIncident
             with: { ... }
       - case: high
         steps:
           - name: notify_team
             type: slack.postMessage
             with: { ... }
     default:
       - name: log_only
         type: console
         with:
           message: "low severity"
   ```

4. **`cases.*` parameters use `snake_case`:** `case_id`, not `caseId`.

   ```yaml
   # Wrong
   - type: cases.addComment
     with:
       caseId: "{{ steps.create.output.case.id }}"

   # Right
   - type: cases.addComment
     with:
       case_id: "{{ steps.create.output.case.id }}"
       comment: "Investigation started."
   ```

5. **`kibana.SetAlertsStatus` / `kibana.SetAlertTags` are PascalCase.** Not `kibana.set_alerts_status`.

   ```yaml
   - name: close_false_positive
     type: kibana.SetAlertsStatus        # PascalCase step type
     with:
       signal_ids: ["{{ event.alerts[0]._id }}"]
       status: closed
       reason: "Verified non-malicious."
   ```

6. **AI step identifiers are top-level kebab-case:** `connector-id`, `agent-id`, `inference-id`. Liquid expressions in these top-level fields aren't evaluated; use literal values. Refer to [AI steps](/explore-analyze/workflows/steps/ai-steps.md).

   ```yaml
   # Wrong — fields nested under with, and templated agent-id is not substituted
   - type: ai.agent
     with:
       agentId: "{{ consts.agent_id }}"
       message: "..."

   # Right — top-level kebab-case with literal values
   - type: ai.agent
     agent-id: elastic-ai-agent
     with:
       message: "..."
   ```

7. **Composition's `workflow-id` is kebab-case but lives *inside* `with`.** It's the one exception to the top-level-kebab-case pattern.

   ```yaml
   - name: enrich
     type: workflow.execute
     with:
       workflow-id: "shared--enrich-alerts"       # kebab-case, inside with
       inputs:
         alerts: "${{ event.alerts }}"
   ```

   :::{tip}
   The `shared--` prefix in the workflow ID is an optional [naming convention](/explore-analyze/workflows/authoring-techniques/compose-workflows.md) for shared workflows, not required syntax.
   :::

8. **`data.*` steps (except `data.set`) put source data at the top level:** `items:`, `arrays:`, or `source:`. The transformation configuration goes in `with`.

   ```yaml
   - name: keep_critical
     type: data.filter
     items: "${{ steps.search.output.hits.hits }}"   # top-level source
     with:
       condition: "item._source.severity : 'critical'"
   ```

9. **Use `${{ ... }}` for arrays and objects**, `{{ ... }}` for strings.

   ```yaml
   # Wrong — array is stringified
   - type: foreach
     foreach: "{{ event.alerts }}"

   # Right — raw-value form preserves the array
   - type: foreach
     foreach: "${{ event.alerts }}"
   ```

10. **`to_json` doesn't exist.** Use `json` to serialize or `json_parse` to parse.

    ```yaml
    # Serialize an object to a JSON string
    payload: "{{ event.alerts[0] | json }}"

    # Parse a JSON string into an object
    parsed: "{{ steps.http.output.body | json_parse }}"
    ```

11. **`data.filter` and `if` conditions are KQL, not Liquid.** Use `item._source.severity : 'critical'`, not `item._source.severity == 'critical'`.

    ```yaml
    # Wrong — Liquid comparison
    - type: data.filter
      items: "${{ steps.search.output.hits.hits }}"
      with:
        condition: "item._source.severity == 'critical'"

    # Right — KQL equality
    - type: data.filter
      items: "${{ steps.search.output.hits.hits }}"
      with:
        condition: "item._source.severity : 'critical'"
    ```

## Related [workflows-cheat-related]

- [Build your first workflow](/explore-analyze/workflows/get-started/build-your-first-workflow.md): Hands-on tutorial if you're new.
- [Glossary](/explore-analyze/workflows/reference/glossary.md): Definitions for every term used in this docset.
- [Step type index](/explore-analyze/workflows/reference/step-types.md): The A-Z lookup.
- [Troubleshooting](/explore-analyze/workflows/authoring-techniques/troubleshooting.md): When something isn't working.
- [`elastic/workflows` library](https://github.com/elastic/workflows): 57 example workflows you can adapt.

% Ben Ironside Goldstein, 2026-05-04: Restored the PM cheat sheet's `while` 2000-default gotcha
% after confirming it against Kibana's DEFAULT_LOOP_MAX_ITERATIONS = 2000 in
% kbn-workflows/spec/schema.ts. The PM source was right; PR A's earlier "no default" claim
% was incorrect. The resume-API input-wrapping gotcha is still pending SME review.
