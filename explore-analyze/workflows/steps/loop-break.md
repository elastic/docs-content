---
navigation_title: Loop break
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Reference for the loop.break step, which exits the innermost enclosing foreach or while loop.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Loop break [workflows-loop-break-step]

The `loop.break` step exits the innermost enclosing [`foreach`](/explore-analyze/workflows/steps/foreach.md) or [`while`](/explore-analyze/workflows/steps/while.md) loop immediately. Use it to stop iterating once a condition is met, for example when you want to process items until you find the first critical match and then move on.

## Parameters

The `loop.break` step takes no step-specific parameters; only the standard `name` and `type` fields required on every step.

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `name` | top level | string | Yes | Unique step identifier. |
| `type` | top level | string | Yes | Must be `loop.break`. |

## Example: Stop on first critical match

```yaml
- name: find_critical
  type: foreach
  foreach: "${{ event.alerts }}"
  steps:
    - name: check_critical
      type: if
      condition: "foreach.item.kibana.alert.severity : critical"
      steps:
        - name: record_and_exit
          type: cases.addComment
          with:
            case_id: "{{ consts.triage_case_id }}"
            comment: "First critical alert found at position {{ foreach.index }}"
        - name: exit
          type: loop.break
```

The loop terminates as soon as the first critical alert is processed.

## Related

- [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md): Overview of all flow-control types.
- [Loop continue step](/explore-analyze/workflows/steps/loop-continue.md): Skip to the next iteration instead of exiting.
- [Foreach step](/explore-analyze/workflows/steps/foreach.md) and [While step](/explore-analyze/workflows/steps/while.md): The loop types `loop.break` can exit from.
