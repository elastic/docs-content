---
navigation_title: Human-in-the-loop
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Pause a workflow to wait for human input, then resume with the reviewer's decision using the waitForInput step.
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

## The mechanism: `waitForInput`

HITL is built on one step type: [`waitForInput`](/explore-analyze/workflows/steps/flow-control-steps.md#waitforinput). When the workflow reaches it, execution pauses. The reviewer sees the message (optionally with a form generated from a JSON Schema). When they respond, the workflow resumes with their input available as `steps.<step_name>.output`.

## Design a good HITL form

A HITL message is read by a human mid-incident. Design for speed:

- **Lead with the decision.** The first line should say what the reviewer needs to decide.
- **Include the evidence.** Relevant context (alert details, enrichment results, AI rationale) belongs in the message so the reviewer doesn't have to dig.
- **Keep the schema small.** Three fields is a lot. One boolean plus an optional notes field is often enough.
- **Use Markdown.** The message supports Markdown, so use headings, bold text, and bullets to make it scannable.

## Write a HITL workflow

The three ingredients: a preceding step that gathers context, a `waitForInput` step that presents it, and subsequent steps that branch on the reviewer's decision.

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
    if: "steps.review.output.approved : true"
    connector-id: "edr-connector"
    with:
      method: "POST"
      url: "https://edr.example.com/isolate"
      body:
        host: "{{ event.alerts[0].host.name }}"
        reason: "{{ steps.review.output.notes }}"

  - name: record_decision
    type: cases.addComment
    with:
      case_id: "{{ steps.open_case.output.case.id }}"
      comment: |
        **Decision:** {{ steps.review.output.approved ? "isolated" : "no action" }}
        **Notes:** {{ steps.review.output.notes }}
```

Execution pauses at `review`. Until a reviewer responds, the execution state is `WAITING_FOR_INPUT`. When they respond, execution resumes at `isolate`, which is gated by an `if` guard on the approval decision.

## Resume a paused workflow

Resume a paused workflow using the following methods.

### From the Kibana UI

Open the execution view. The paused step renders a form generated from the `schema`. Fill it in, submit, and the workflow resumes.

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

The input body is available to subsequent steps as `steps.<step_name>.output`. Reference individual fields like `{{ steps.review.output.approved }}` and `{{ steps.review.output.notes }}`.

## What happens while the workflow is paused

- The execution is in the `WAITING_FOR_INPUT` state. It appears in the execution history with a resume action.
- There's no default timeout on `waitForInput`. The workflow waits indefinitely. To limit the wait, set a workflow-level `settings.timeout`.
- If the workflow-level `settings.timeout` elapses before the reviewer responds, the execution is cancelled.

## Related

- [`waitForInput` step reference](/explore-analyze/workflows/steps/flow-control-steps.md#waitforinput): Step parameter details.
- [AI steps](/explore-analyze/workflows/steps/ai-steps.md): Pair AI classification or summarization with HITL for uncertain cases.
- [Cases action steps](/explore-analyze/workflows/steps/cases.md): Record decisions and outcomes on the case.

% Ben Ironside Goldstein, 2026-04-16: The Kibana source README for wait_for_input_step shows the
% output being accessed directly (e.g., steps.review.output.approved). PM internal docs claimed the
% resume API wraps the body in { "input": ... }. Using the Kibana README's direct-access form here;
% if engineering confirms the wrapped form is correct, update the API example above.
