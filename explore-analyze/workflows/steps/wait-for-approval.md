---
navigation_title: Wait for approval
applies_to:
  stack: preview 9.5+
  serverless: preview
description: Reference for the waitForApproval step, which pauses a workflow until a human approves or rejects the request in Kibana or through an external resume link.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# waitForApproval [workflows-waitforapproval-step]

The `waitForApproval` step pauses workflow execution until a human approves or rejects the request. Use it when the decision is yes or no. The step returns `approved: true` or `false` and renders approve/reject controls in {{kib}} and in external notifications.

For free-form or multi-field input, use [`waitForInput`](/explore-analyze/workflows/steps/wait-for-input.md) instead. For the end-to-end human-in-the-loop pattern, refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md).

:::{include} ../_snippets/schema-location-legend.md
:::

## Parameters

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `name` | top level | string | Yes | Unique step identifier. |
| `type` | top level | string | Yes | Must be `waitForApproval`. |
| `timeout` | top level | duration | No | How long the step waits for a decision. Format: number + unit (`ms`/`s`/`m`/`h`/`d`/`w`). Defaults to `24h`. If no one responds before the timeout, the step fails. |
| `message` | `with` | string | No | Markdown message displayed to approvers. |
| `approveLabel` | `with` | string | No | Label for the approve action. Defaults to `Approve`. |
| `rejectLabel` | `with` | string | No | Label for the reject action. Defaults to `Decline`. |
| `channels` | `with` | object | No | External notification channels that send approve/reject links. Responders can act without signing in to {{kib}}. See [External channels](#external-channels). |

## Output

After someone responds, the step output has this shape:

```yaml
response:
  approved: true    # or false
respondedBy: "..."  # Who responded
```

Downstream steps typically gate on `{{ steps.<step_name>.output.response.approved }}`.

## Execution state

- While waiting, the execution state is `WAITING_FOR_INPUT`.
- By default, the step times out after `24h`. This default applies whether or not you configure an external channel.
- If no one responds before the timeout, the step fails.

## External channels [external-channels]

Use `with.channels` to notify approvers outside Kibana. Slack is the only built-in channel. Notifications include one-click approve and reject links. Responders can act without signing in to {{kib}}.

| Channel key | Connector type | Required fields | Notes |
|---|---|---|---|
| `slack` | Slack webhook (`slack`) | `connector-id` | Posts to the channel configured on the webhook connector. |
| `slack_api` | Slack API (`slack_api`) | `connector-id`, `channels` (array of Slack channel IDs) | Posts approve/reject buttons to the listed channels. |

Both channel configs accept an optional `message` template.

:::{warning}
External channels send public, short-lived resume links. Don't use them for destructive, production-impacting, or hard-to-reverse workflows.
:::

To turn off external resume, set the `hitlExternalResume.enabled` settings in `kibana.yml`. For details, refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md#workflows-hitl-external-channels).

## Example: Approve host isolation

```yaml
- name: request_approval
  type: waitForApproval
  timeout: 24h
  with:
    message: "Approve isolation for {{ event.alerts[0].host.name }}?"
    approveLabel: Approve
    rejectLabel: Decline
    channels:
      slack:
        connector-id: my-slack-webhook-connector
      slack_api:
        connector-id: my-slack-api-connector
        channels: ["C0123456789"]

- name: isolate
  type: http
  if: "steps.request_approval.output.response.approved : true"
  connector-id: "edr-connector"
  with:
    method: "POST"
    url: "https://edr.example.com/isolate"
    body:
      host: "{{ event.alerts[0].host.name }}"
```

## Related

- [Human-in-the-loop pattern](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md): Inbox, external resume, and design guidance.
- [`waitForInput` step](/explore-analyze/workflows/steps/wait-for-input.md): Collect structured input with a custom JSON Schema.
- [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md): Other flow-control types you'll often combine with approval gates.
- [If step](/explore-analyze/workflows/steps/if.md): Typical gate around the post-approval action.
