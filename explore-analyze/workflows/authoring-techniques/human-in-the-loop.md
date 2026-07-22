---
navigation_title: Human-in-the-loop
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Pause a workflow to wait for human input, then resume with the reviewer's decision using waitForInput or waitForApproval.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Human-in-the-loop workflows [workflows-human-in-the-loop]

Not every decision should be fully automated. *Human-in-the-loop* (HITL) is the pattern where a workflow pauses at a critical decision point, presents structured findings to a reviewer, waits for their input, and then resumes based on that input. It lets you combine the reach of automation with human judgment where judgment matters most.

## When to reach for HITL

- **Remediation with potential impact.** Isolating a host, blocking a user, or deleting data. Pause for analyst approval before the destructive action.
- **Ambiguous classifications.** When an AI or rule is uncertain, ask a human before proceeding.
- **Escalation gates.** Page an on-call, wait for acknowledgement and decision, then route accordingly.
- **Approval for automation.** A new workflow in test mode can pause and ask for approval on each action for the first few runs, then switch to full automation once trusted.

## The mechanism: `waitForInput` and `waitForApproval`

HITL is built on wait steps that pause execution until a human responds:

| Step | Use when | Response shape |
|---|---|---|
| [`waitForInput`](/explore-analyze/workflows/steps/wait-for-input.md) | You need a custom form (notes, severity, multi-field decisions) | Your JSON Schema payload (see [output shape](#hitl-output-shape)) |
| [`waitForApproval`](/explore-analyze/workflows/steps/wait-for-approval.md) {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` | The decision is approve or reject | `approved: true` or `false` under `output.response` |

When the workflow reaches either step, execution pauses in the `WAITING_FOR_INPUT` state. The reviewer sees the message and form (or approve/reject controls). When they respond, the workflow resumes with their input available as `steps.<step_name>.output`.

## Write a HITL workflow

The three ingredients: a preceding step that gathers context, a wait step that presents it, and subsequent steps that branch on the reviewer's decision.

```yaml
name: isolate-host-with-approval
enabled: true

triggers:
  - type: alert

steps:
  - name: open_case
    type: cases.createCase
    with:
      title: "Potential compromise: {{ event.alerts[0].host.name }}"
      description: "Potential host compromise detected by alert workflow"
      owner: securitySolution
      severity: high
      tags: ["auto-triage"]

  - name: investigate
    type: elasticsearch.search
    with:
      index: "logs-*"
      query:
        term:
          "host.name": "{{ event.alerts[0].host.name }}"

  - name: classify
    type: ai.classify
    connector-id: "my-openai"
    with:
      input: "${{ steps.investigate.output.hits.hits }}"
      categories: ["confirmed_compromise", "likely_benign", "needs_review"]
      includeRationale: true

  - name: review
    type: waitForInput
    timeout: 72h
    with:
      message: |
        ## Alert on `{{ event.alerts[0].host.name }}`

        **AI classification:** {{ steps.classify.output.category }}

        **Rationale:** {{ steps.classify.output.rationale }}

        Isolate this host?
      schema:
        type: object
        properties:
          approved:
            type: boolean
            title: "Isolate the host"
          notes:
            type: string
            title: "Analyst notes"
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

  - name: record_decision
    type: cases.addComment
    with:
      case_id: "{{ steps.open_case.output.case.id }}"
      comment: |
        **Decision:** {% if steps.review.output.response.approved %}isolated{% else %}no action{% endif %}
        **Notes:** {{ steps.review.output.response.notes }}
        **Responded by:** {{ steps.review.output.respondedBy }}
```

Execution pauses at `review`. Until a reviewer responds, the execution state is `WAITING_FOR_INPUT`. When they respond, execution resumes at `isolate`, which is gated by an `if` guard on the approval decision.

## Resume a paused workflow

Resume a paused workflow using the following methods.

### From the Kibana UI

Open the execution view. The paused step renders a form generated from the `schema` (or approve/reject controls for `waitForApproval`). Fill it in, submit, and the workflow resumes.

### From the Inbox app

```{applies_to}
stack: preview 9.5+
serverless: preview
```

The **Inbox** app lists HITL actions that need a response. Enable it with `xpack.inbox.enabled: true` in `kibana.yml` (disabled by default).

Inbox splits into:

- **Awaiting response** — Pending `waitForInput` / `waitForApproval` steps. Open the **Respond** flyout to fill in the form (or approve/reject). If the preceding step included a reasoning summary, Inbox shows it to help the reviewer decide.
- **History** — A record of actions that were responded to, timed out, or whose workflow was deleted. Each entry includes who responded, their response, the channel, and when it happened.

If more than one person responds, only the first response is accepted.

### From the API

Send a `POST` request to the resume endpoint with the reviewer's input:

```http
POST /api/workflowExecutions/{executionId}/resume
Content-Type: application/json

{
  "approved": true,
  "notes": "Confirmed malicious. Proceeding with isolation."
}
```

The input body becomes part of the step output. See [Output shape](#hitl-output-shape) for how to reference fields by Stack version.

### From an external channel (Slack) [workflows-hitl-external-channels]

```{applies_to}
stack: preview 9.5+
serverless: preview
```

Configure `with.channels` on `waitForInput` or `waitForApproval` to notify responders in Slack. Slack is the only built-in channel in 9.5.

| Channel key | What you need |
|---|---|
| `slack` | A Slack **webhook** connector. Posts to the webhook's configured channel. |
| `slack_api` | A Slack **API** connector plus one or more Slack channel IDs (`channels: ["C…"]`). |

How responders act:

- **`waitForApproval`** — Approve and reject links (and Slack API buttons) that resume the step. Responders can act without signing in to {{kib}}.
- **`waitForInput`** — A link to a hosted form where responders submit the schema fields. The Slack notification can also include a one-click query link.

External links work without a {{kib}} session. Each link includes a short-lived, single-use token that {{kib}} invalidates after use, timeout, or workflow cancellation.

:::{warning}
External channels send public resume links. Don't use them for destructive, production-impacting, or hard-to-reverse workflows.
:::

To resume waiting workflows from {{kib}} only, set external resume to `false` in `kibana.yml`:

```yaml
workflowsManagement.hitlExternalResume.enabled: false
workflowsExecutionEngine.hitlExternalResume.enabled: false
```

Both settings default to `true`. When set to `false`, Slack and other external resume links stop working.

## Output shape [hitl-output-shape]

How you read the resume payload depends on the {{stack}} version:

- {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` Fields are under `output.response`, and the responder is `output.respondedBy`. For example: `{{ steps.review.output.response.approved }}`, `{{ steps.review.output.response.notes }}`, and `{{ steps.review.output.respondedBy }}`.
- {applies_to}`stack: ga 9.4` Fields are on the step output directly. For example: `{{ steps.review.output.approved }}` and `{{ steps.review.output.notes }}`.

## Design a good HITL form

A HITL message is read by a human mid-incident. Design for speed:

- **Lead with the decision.** The first line should say what the reviewer needs to decide.
- **Include the evidence.** Relevant context (alert details, enrichment results, AI rationale) belongs in the message so the reviewer doesn't have to dig.
- **Keep the schema small.** Three fields is a lot. One boolean plus an optional notes field is often enough. Prefer [`waitForApproval`](/explore-analyze/workflows/steps/wait-for-approval.md) {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` when you only need yes/no.
- **Use Markdown.** The message supports Markdown, so use headings, bold text, and bullets to make it scannable.

## What happens while the workflow is paused

While a HITL step is waiting, the execution status is `WAITING_FOR_INPUT`. The run appears in the execution history with a resume action. 

{applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview` When Inbox is enabled, the waiting action also appears there.

Timeout behavior depends on the {{stack}} version:

::::{applies-switch}

:::{applies-item} { stack: preview 9.5+, serverless: preview }
By default, `waitForInput` times out after `72h` and `waitForApproval` after `24h`. These defaults apply whether or not you configure an external channel. Override them with a top-level `timeout` on the step. If no one responds before the timeout, the step fails.
:::

:::{applies-item} stack: ga 9.4
`waitForInput` has no default timeout and waits until someone responds. To limit the wait, set a workflow-level `settings.timeout`.
:::

::::

If a workflow-level `settings.timeout` elapses before the reviewer responds, the execution is cancelled.

## Related

- [`waitForInput` step reference](/explore-analyze/workflows/steps/wait-for-input.md): Step parameter details for custom forms.
- [`waitForApproval` step reference](/explore-analyze/workflows/steps/wait-for-approval.md) {applies_to}`stack: preview 9.5+` {applies_to}`serverless: preview`: Approve/reject without a custom schema.
- [AI steps](/explore-analyze/workflows/steps/ai-steps.md): Pair AI classification or summarization with HITL for uncertain cases.
- [Cases action steps](/explore-analyze/workflows/steps/cases.md): Record decisions and outcomes on the case.


% Sub-workflow waiting propagation and Agent Builder rich-input alignment aredeferred pending engineering confirmation (docs-content-internal#1455).
