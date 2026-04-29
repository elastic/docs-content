---
navigation_title: Switch
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Reference for the switch step, which routes to different step blocks based on an evaluated expression.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Switch [workflows-switch-step]

The `switch` step evaluates an expression once and compares its value against each case's `match` field in order, then dispatches to the first matching case and executes its `steps`. Use it for multi-way branching where an `if` chain would be awkward (for example, routing by alert category, severity tier, or environment name).

## Parameters

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `name` | top level | string | Yes | Unique step identifier. |
| `type` | top level | string | Yes | Must be `switch`. |
| `expression` | top level | string | Yes | Expression to evaluate. The result is converted to a string for comparison with each case's `match` value. |
| `cases` | top level | array | Yes | Array of `{ match, steps }` objects. Each case's `match` is a string, number, or boolean compared to the evaluated expression. |
| `default` | top level | array | No | Steps to run if no case matches. |

:::{important}
`cases` is an **array of objects**, not a map of names to step lists. Each entry has a `match` value and a `steps` array. Order matters: the first matching `match` wins.
:::

## Example: Dispatch by alert category

```yaml
- name: classify
  type: ai.classify
  connector-id: "my-openai"
  with:
    input: "${{ event.alerts[0] }}"
    categories: ["malware", "phishing", "lateral_movement", "reconnaissance"]

- name: dispatch
  type: switch
  expression: "{{ steps.classify.output.category }}"
  cases:
    - match: "malware"
      steps:
        - name: open_malware_case
          type: cases.createCase
          with:
            title: "Malware: {{ event.alerts[0].host.name }}"
            severity: "critical"
            tags: ["malware"]

    - match: "phishing"
      steps:
        - name: open_phishing_case
          type: cases.createCase
          with:
            title: "Phishing: {{ event.alerts[0].user.name }}"
            severity: "high"
            tags: ["phishing"]

    - match: "lateral_movement"
      steps:
        - name: escalate
          type: pagerduty.triggerIncident
          connector-id: "platform-pagerduty"
          with:
            severity: "critical"
            summary: "Lateral movement detected: {{ event.alerts[0].host.name }}"
  default:
    - name: route_to_analyst
      type: slack.postMessage
      connector-id: "platform-slack"
      with:
        channel: "#soc-triage"
        text: "Alert needs manual review: {{ event.alerts[0]._id }}"
```

## When to use `switch` versus `if`

Reach for `switch` when:

- You're comparing a single expression against several candidate values.
- Adding a new case should not require nesting or reorganizing existing cases.

Reach for [`if`](/explore-analyze/workflows/steps/if.md) when:

- You're evaluating compound conditions on different fields.
- You have only two branches.

## Related

- [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md): Overview of all flow-control types.
- [If step](/explore-analyze/workflows/steps/if.md): For two-way branching and compound conditions.
- [AI classify step](/explore-analyze/workflows/steps/ai-steps.md#ai-classify): A common pairing: classify into an enum, then `switch` on the result.
