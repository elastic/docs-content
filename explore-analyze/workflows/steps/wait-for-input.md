---
navigation_title: Wait for input
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Reference for the waitForInput step, which pauses a workflow until a human submits input through the Kibana UI, resume API, or an external channel.
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

For the end-to-end pattern, including the Inbox app, external Slack delivery, and design guidance, refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md). For a fixed approve/reject decision without a custom schema, use [`waitForApproval`](/explore-analyze/workflows/steps/wait-for-approval.md) {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` instead.

:::{include} ../_snippets/schema-location-legend.md
:::

## Parameters

| Parameter | Location | Type | Required | Description |
|---|---|---|---|---|
| `name` | top level | string | Yes | Unique step identifier. |
| `type` | top level | string | Yes | Must be `waitForInput`. |
| `timeout` {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` | top level | duration | No | How long the step waits for input. Format: number + unit (`ms`/`s`/`m`/`h`/`d`/`w`). Defaults to `72h`. If no one responds before the timeout, the step fails. |
| `message` | `with` | string | No | Markdown message displayed to the reviewer. |
| `schema` | `with` | object | No | JSON Schema that describes the expected input. Renders as a form in the Kibana UI and Inbox **Respond** flyout, and validates the resume payload. |
| `channels` {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` | `with` | object | No | External notification channels that send resume links. Responders can act without signing in to {{kib}}. See [External channels](#external-channels). |

`message`, `schema`, and `channels` are optional. If you omit `schema`, the resume accepts any payload.

## Output

How the resume payload appears on the step output depends on the Stack version:

::::{applies-switch}

:::{applies-item} { stack: preview 9.5+, serverless: preview }
The submitted fields are under `response`, and who responded is `respondedBy`:

```yaml
response:            # The submitted payload (fields from your schema)
  approved: true
  notes: "..."
respondedBy: "..."   # Who responded
```

Downstream steps reference fields under `response`: `{{ steps.<step_name>.output.response.<field> }}`.
:::

:::{applies-item} stack: ga 9.4
The resume body is the step output directly. Downstream steps reference fields like `{{ steps.<step_name>.output.<field> }}`.

```yaml
approved: true
notes: "..."
```
:::

::::

## Execution state

- While waiting, the execution state is `WAITING_FOR_INPUT`.
- {applies_to}`stack: ga 9.4` There is no step-level default timeout. The workflow waits until a reviewer responds, or until a workflow-level [`settings.timeout`](/explore-analyze/workflows/authoring-techniques/pass-data-handle-errors.md) cancels the run.
- {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` By default, the step times out after `72h`. This default applies whether or not you configure an external channel. Override it with a top-level `timeout` on the step. If no one responds before the timeout, the step fails.

## External channels [external-channels]

```{applies_to}
stack: preview 9.5+
serverless: preview
```

Use `with.channels` to notify responders outside Kibana. Slack is the only built-in channel. Responders can open a hosted HTML form or use a one-click query link. Both work without a {{kib}} session.

| Channel key | Connector type | Required fields | Notes |
|---|---|---|---|
| `slack` | Slack webhook (`slack`) | `connector-id` | Posts to the channel configured on the webhook connector. |
| `slack_api` | Slack API (`slack_api`) | `connector-id`, `channels` (array of Slack channel IDs) | Posts interactive notifications to the listed channels. |

Both channel configs accept an optional `message` template. Use `{{ context.hitl.externalFormLink }}` for the hosted form URL and `{{ context.hitl.externalQueryLink }}` for the one-click query link. If you omit `message`, the notification includes the form link by default.

:::{warning}
External channels send public, short-lived resume links. Don't use them for destructive, production-impacting, or hard-to-reverse workflows.
:::

To turn off external resume, set the `hitlExternalResume.enabled` settings in `kibana.yml`. For details, refer to [Human-in-the-loop](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md#workflows-hitl-external-channels).

## Example: Approval gate before a destructive action

```yaml
- name: review
  type: waitForInput
  timeout: 24h
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
  if: "steps.review.output.response.approved : true"
  connector-id: "edr-connector"
  with:
    method: "POST"
    url: "https://edr.example.com/isolate"
    body:
      host: "{{ event.alerts[0].host.name }}"
      reason: "{{ steps.review.output.response.notes }}"
```

## Example: Notify Slack while waiting

```{applies_to}
stack: preview 9.5+
serverless: preview
```

```yaml
- name: review
  type: waitForInput
  timeout: 72h
  with:
    message: "Review this escalation and submit your decision."
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
    channels:
      slack:
        connector-id: my-slack-webhook-connector
      slack_api:
        connector-id: my-slack-api-connector
        channels: ["C0123456789"]
```

## Related

- [Human-in-the-loop pattern](/explore-analyze/workflows/authoring-techniques/human-in-the-loop.md): The full HITL pattern, including Inbox and external resume.
- [`waitForApproval` step](/explore-analyze/workflows/steps/wait-for-approval.md) {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview`: Approve/reject without a custom schema.
- [Flow control steps](/explore-analyze/workflows/steps/flow-control-steps.md): Other flow-control types you'll often combine with `waitForInput`.
- [If step](/explore-analyze/workflows/steps/if.md): Typical gate around the post-review action.
