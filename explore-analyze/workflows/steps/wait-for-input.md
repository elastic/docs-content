---
navigation_title: Wait for input
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Reference for the waitForInput step, which pauses a workflow until a human submits input through the resume API or Kibana UI.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# waitForInput [workflows-waitforinput-step]

The `waitForInput` step pauses workflow execution until a human submits input. It's the primary human-in-the-loop primitive: the building block for approval gates, escalation checkpoints, and review steps.

For the end-to-end pattern including resume API details and design guidance, refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md).

## Parameters

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `name` | top level | string | Yes | Unique step identifier. |
| `type` | top level | string | Yes | Must be `waitForInput`. |
| `message` | `with` | string | No | Markdown message displayed to the reviewer. |
| `schema` | `with` | object | No | JSON Schema that describes the expected input. Renders as a form in the Kibana UI and validates the resume payload. |

Both `message` and `schema` are optional. If you omit `schema`, the resume accepts any payload.

## Output

After the reviewer submits input, the step's output is the submitted payload. Downstream steps reference fields directly: `{{ steps.<step_name>.output.<field> }}`.

## Execution state

- While waiting, the execution state is `WAITING_FOR_INPUT`.
- There is no default timeout. To limit how long the workflow will wait, set a workflow-level [`settings.timeout`](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md).
- If `settings.timeout` elapses before resume, the execution is cancelled.

## Example: Approval gate before a destructive action

```yaml
- name: review
  type: waitForInput
  with:
    message: |
      ## Confirm host isolation

      Host `{{ event.alerts[0].host.name }}` was flagged by rule {{ event.rule.name }}.

      AI classification: **{{ steps.classify.output.category }}**

      Proceed with isolation?
    schema:
      type: object
      properties:
        approved:
          type: boolean
          title: "Isolate the host"
        notes:
          type: string
          title: "Reviewer notes"
      required: ["approved"]

- name: isolate
  type: http
  if: "steps.review.output.approved : true"
  connector-id: "edr-connector"
  with:
    method: "POST"
    url: "https://edr.example.com/isolate"
    body:
      host: "{{ event.alerts[0].host.name }}"
      reason: "{{ steps.review.output.notes }}"
```

## Related

- [Human-in-the-loop pattern](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md): The full HITL pattern, including the resume API.
- [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md): Other flow-control types you'll often combine with `waitForInput`.
- [If step](/explore-analyze/workflows/steps/if.md): Typical gate around the post-review action.
