---
navigation_title: Flow control
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: The 8 flow-control step types for branching, iterating, looping, pausing, and waiting for human input in workflows.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Flow control steps [workflows-flow-control-steps]

Flow control steps shape a workflow's logic. They decide what runs, what gets skipped, when the workflow loops, and where it pauses. 9.4 ships the full set of 8 step types: `if`, `foreach`, `while`, `switch`, `wait`, `loop.break`, `loop.continue`, and `waitForInput`.

## When to reach for each

| Pattern | Step |
|---|---|
| Branch on a condition | [`if`](#if) |
| Iterate over an array | [`foreach`](#foreach) |
| Loop until a condition is false | [`while`](#while) |
| Multi-way dispatch on a value | [`switch`](#switch) |
| Pause for a fixed duration | [`wait`](#wait) |
| Exit a loop early | [`loop.break`](#loop-break) |
| Skip to the next loop iteration | [`loop.continue`](#loop-continue) |
| Pause for operator input (human-in-the-loop) | [`waitForInput`](#waitforinput) |

For fan-out across independent workflow executions, see [`workflow.executeAsync`](/explore-analyze/workflows/steps/composition.md#workflow-executeasync) in the composition reference.

## `if` [if]

Conditional branching. Evaluates a {{kib}} Query Language (KQL) or boolean expression and runs the `steps` block if true, or the optional `else` block if false.

```yaml
- name: route_severity
  type: if
  condition: "event.alerts[0].kibana.alert.risk_score >= 70"
  steps:
    - name: high_priority
      type: console
      with: { message: "High priority alert" }
  else:
    - name: low_priority
      type: console
      with: { message: "Standard alert" }
```

For expression syntax and additional examples, see [If step](/explore-analyze/workflows/steps/if.md).

## `foreach` [foreach]

Iterate over an array, running nested steps once per item. Inside the loop, the current item is available as `foreach.item`, the zero-based position as `foreach.index`, and the total count as `foreach.total`.

```yaml
- name: process_alerts
  type: foreach
  foreach: "${{ event.alerts }}"
  steps:
    - name: log_alert
      type: console
      with:
        message: "[{{ foreach.index }}/{{ foreach.total }}] {{ foreach.item._id }}"
```

For the full parameter reference, see [Foreach step](/explore-analyze/workflows/steps/foreach.md).

## `while` [while]

Loop while a KQL condition evaluates to true. Optional `max-iterations` caps the number of iterations; without it, the loop continues as long as the condition holds.

```yaml
- name: poll_until_ready
  type: while
  condition: "steps.check.output.status : pending"
  max-iterations:
    limit: 60
    on-limit: fail
  steps:
    - name: check
      type: elasticsearch.search
      with:
        index: "jobs"
        size: 1
    - name: backoff
      type: wait
      with:
        duration: "5s"
```

For the full parameter reference and gotchas, see [While step](/explore-analyze/workflows/steps/while.md).

## `switch` [switch]

Multi-way branching. The engine evaluates an expression once and routes to the matching case. Each case has a `match` value and a `steps` array; an optional `default` runs when no case matches.

```yaml
- name: dispatch_by_category
  type: switch
  expression: "{{ steps.classify.output.category }}"
  cases:
    - match: "malware"
      steps:
        - name: handle_malware
          type: console
          with: { message: "malware path" }
    - match: "phishing"
      steps:
        - name: handle_phishing
          type: console
          with: { message: "phishing path" }
  default:
    - name: handle_other
      type: console
      with: { message: "other" }
```

For the full parameter reference, see [Switch step](/explore-analyze/workflows/steps/switch.md).

## `wait` [wait]

Pause execution for a specified duration, then continue to the next step.

```yaml
- name: backoff
  type: wait
  with:
    duration: "30s"
```

For the full parameter reference, see [Wait step](/explore-analyze/workflows/steps/wait.md).

## `loop.break` [loop-break]

Exit the innermost enclosing loop (`foreach` or `while`) immediately. Takes no parameters.

```yaml
- name: stop_on_match
  type: if
  condition: "foreach.item.severity : critical"
  steps:
    - name: exit
      type: loop.break
```

For the full reference, see [Loop break step](/explore-analyze/workflows/steps/loop-break.md).

## `loop.continue` [loop-continue]

Skip to the next iteration of the innermost enclosing loop. Takes no parameters.

```yaml
- name: skip_empty
  type: if
  condition: "foreach.item.empty : true"
  steps:
    - name: next
      type: loop.continue
```

For the full reference, see [Loop continue step](/explore-analyze/workflows/steps/loop-continue.md).

## `waitForInput` [waitforinput]

Pause the workflow until an operator submits input through the resume API or the Kibana UI. The primary human-in-the-loop primitive.

```yaml
- name: review
  type: waitForInput
  with:
    message: "Review the AI classification and confirm the action."
    schema:
      type: object
      properties:
        approved:
          type: boolean
          title: "Approve"
        notes:
          type: string
          title: "Notes"
      required: ["approved"]
```

For the complete HITL pattern, see [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md). For the step parameter reference, see [waitForInput step](/explore-analyze/workflows/steps/wait-for-input.md).

## Related

- [Composition steps](/explore-analyze/workflows/steps/composition.md): `workflow.executeAsync` for fan-out across independent executions.
- [Pass data and handle errors](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md): `on-failure` strategies for individual steps inside loops.
- [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md): Full HITL pattern using `waitForInput`.
