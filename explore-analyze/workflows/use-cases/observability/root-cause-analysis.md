---
navigation_title: Root cause analysis
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Build an observability workflow that runs an Agent Builder agent on an alert, then opens a case populated with the agent's root-cause analysis and supporting investigation steps.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Automate root cause analysis for an observability alert [workflows-observability-rca]

This guide walks through building an observability workflow that responds to an alert by running an {{agent-builder}} agent for root-cause analysis, generating a case title and description from the agent's output, opening the case, and attaching both the alert and the agent's reasoning trace as comments.

The workflow is adapted from [`root-cause-analysis-rca-workflow.yaml`](https://github.com/elastic/workflows/blob/main/workflows/examples/root-cause-analysis-rca-workflow.yaml) in the `elastic/workflows` library.

If you're new to workflows, complete [Build your first workflow](/explore-analyze/workflows/get-started/build-your-first-workflow.md) first.

## Before you begin [workflows-rca-prereqs]

- **Permissions.** `All` on **Analytics > Workflows**, **Observability > Cases**, and whatever Agent Builder privilege is required to invoke agents in your space. Refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
- **Alerting rule.** A configured [observability alerting rule](/solutions/observability/incident-management/alerting.md) that fires on the conditions you want to auto-investigate (metric thresholds, SLO burn rate, anomaly detection, or custom query).
- **SRE agent.** An {{agent-builder}} agent configured to investigate observability signals. The examples use `elastic-ai-agent` as a default. Substitute your agent ID.
- **Attach the workflow to the rule.** After saving the workflow, attach it as an action on the alerting rule. Refer to [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md).

## How it works [workflows-rca-how-it-works]

The workflow runs in a single pass when an alert fires:

1. An **alert trigger** starts the workflow with the alert payload at `event`.
2. An **`ai.agent` step** runs an initial analysis of the alert and returns the agent's conversation ID so follow-up steps can continue the same conversation.
3. Two more **`ai.agent` calls** reuse the conversation to generate a case title and a case description.
4. A **`cases.createCase` step** opens the case with the agent-generated title and description.
5. **`cases.addAlerts`** attaches the triggering alert.
6. A **`kibana.request` step** fetches the agent's conversation transcript.
7. **`cases.addComment` steps** append the agent's reasoning trace and the raw analysis as comments for auditability.

## Build the workflow [workflows-rca-build]

:::::{stepper}

::::{step} Trigger on observability alerts

```yaml
triggers:
  - type: alert
```

Attach the workflow to the alerting rule you want to investigate.
::::

::::{step} Run initial RCA

Call the agent with the alert payload. Keep `create-conversation: true` so follow-up steps can continue the conversation and the agent has context when generating the title and description:

```yaml
steps:
  - name: rca_analysis
    type: ai.agent
    agent-id: elastic-ai-agent
    create-conversation: true
    with:
      message: |
        Investigate the following alert and propose root causes.
        Keep your analysis and data exploration brief to preserve context.

        <alert>
        {{ event | json }}
        </alert>
```

The agent's response is at `steps.rca_analysis.output.message`, and the conversation ID is at `steps.rca_analysis.output.conversation_id`.
::::

::::{step} Generate a case title and description

Reuse the conversation (so the agent remembers its analysis) and ask it for a title and description:

```yaml
  - name: case_title
    type: ai.agent
    agent-id: elastic-ai-agent
    with:
      conversation_id: "{{ steps.rca_analysis.output.conversation_id }}"
      message: "Based on your analysis, produce a clear case title. Output only the title."

  - name: case_description
    type: ai.agent
    agent-id: elastic-ai-agent
    with:
      conversation_id: "{{ steps.rca_analysis.output.conversation_id }}"
      message: "Based on your analysis, produce a clear case description. Output only the description."
```

Using a conversation ID keeps tokens cheap and ensures the title and description match the earlier analysis.
::::

::::{step} Open the case

Create the case with the agent-generated title and description:

```yaml
  - name: create_case
    type: cases.createCase
    with:
      title: "{{ steps.case_title.output.message }}"
      description: "{{ steps.case_description.output.message }}"
      owner: "observability"
      severity: "medium"
      tags: ["auto-rca", "ai-generated"]
```

`owner` is `observability` for observability cases.
::::

::::{step} Attach the alert

```yaml
  - name: attach_alert
    type: cases.addAlerts
    with:
      case_id: "{{ steps.create_case.output.case.id }}"
      alerts:
        - alertId: "{{ event.alerts[0]._id }}"
          index: "{{ event.alerts[0]._index }}"
          rule:
            id: "{{ event.rule.id }}"
            name: "{{ event.rule.name }}"
```
::::

::::{step} Attach the agent's analysis and reasoning

Append the raw analysis as one comment and the reasoning trace as another. Fetch the reasoning trace with a `kibana.request` against the Agent Builder conversations API:

```yaml
  - name: add_analysis
    type: cases.addComment
    with:
      case_id: "{{ steps.create_case.output.case.id }}"
      comment: "{{ steps.rca_analysis.output.message }}"

  - name: get_conversation
    type: kibana.request
    with:
      method: GET
      path: /api/agent_builder/conversations/{{ steps.rca_analysis.output.conversation_id }}

  - name: add_reasoning
    type: cases.addComment
    with:
      case_id: "{{ steps.create_case.output.case.id }}"
      comment: |
        ## AI investigation summary

        [View full conversation]({{ kibanaUrl }}/app/agent_builder/conversations/{{ steps.rca_analysis.output.conversation_id }})

        {%- for round in steps.get_conversation.output.rounds %}
        {%- for step in round.steps %}
        {%- if step.type == "reasoning" %}
        - **Reasoning:** {{ step.reasoning }}
        {%- elsif step.type == "tool_call" %}
        - **Action:** `{{ step.tool_id }}`
        {%- endif %}
        {%- endfor %}
        {%- endfor %}
```

The Liquid loop walks the conversation's rounds and formats each reasoning step and tool call as a bullet. The comment becomes an auditable record of how the agent reached its conclusion.
::::

:::::

## Complete workflow [workflows-rca-complete]

:::{dropdown} Full workflow YAML

```yaml
name: observability--root-cause-analysis
description: Investigate an observability alert with an AI agent, then open a case populated with the analysis and reasoning trace.
enabled: true
tags: ["rca", "ai", "observability"]

triggers:
  - type: alert

steps:
  - name: rca_analysis
    type: ai.agent
    agent-id: elastic-ai-agent
    create-conversation: true
    with:
      message: |
        Investigate the following alert and propose root causes.
        Keep your analysis and data exploration brief to preserve context.

        <alert>
        {{ event | json }}
        </alert>

  - name: case_title
    type: ai.agent
    agent-id: elastic-ai-agent
    with:
      conversation_id: "{{ steps.rca_analysis.output.conversation_id }}"
      message: "Based on your analysis, produce a clear case title. Output only the title."

  - name: case_description
    type: ai.agent
    agent-id: elastic-ai-agent
    with:
      conversation_id: "{{ steps.rca_analysis.output.conversation_id }}"
      message: "Based on your analysis, produce a clear case description. Output only the description."

  - name: create_case
    type: cases.createCase
    with:
      title: "{{ steps.case_title.output.message }}"
      description: "{{ steps.case_description.output.message }}"
      owner: "observability"
      severity: "medium"
      tags: ["auto-rca", "ai-generated"]

  - name: attach_alert
    type: cases.addAlerts
    with:
      case_id: "{{ steps.create_case.output.case.id }}"
      alerts:
        - alertId: "{{ event.alerts[0]._id }}"
          index: "{{ event.alerts[0]._index }}"
          rule:
            id: "{{ event.rule.id }}"
            name: "{{ event.rule.name }}"

  - name: add_analysis
    type: cases.addComment
    with:
      case_id: "{{ steps.create_case.output.case.id }}"
      comment: "{{ steps.rca_analysis.output.message }}"

  - name: get_conversation
    type: kibana.request
    with:
      method: GET
      path: /api/agent_builder/conversations/{{ steps.rca_analysis.output.conversation_id }}

  - name: add_reasoning
    type: cases.addComment
    with:
      case_id: "{{ steps.create_case.output.case.id }}"
      comment: |
        ## AI investigation summary

        [View full conversation]({{ kibanaUrl }}/app/agent_builder/conversations/{{ steps.rca_analysis.output.conversation_id }})

        {%- for round in steps.get_conversation.output.rounds %}
        {%- for step in round.steps %}
        {%- if step.type == "reasoning" %}
        - **Reasoning:** {{ step.reasoning }}
        {%- elsif step.type == "tool_call" %}
        - **Action:** `{{ step.tool_id }}`
        {%- endif %}
        {%- endfor %}
        {%- endfor %}
```

:::

## Extend this workflow [workflows-rca-extend]

- **Route by service.** Use a [`switch` step](/explore-analyze/workflows/steps/switch.md) on `event.alerts[0].service.name` to pick different agents for different services (a database-focused agent for DB alerts, a frontend-focused agent for RUM alerts, and so on).
- **Summarize before paging.** Add an [`ai.summarize` step](/explore-analyze/workflows/steps/ai-steps.md#ai-summarize) that turns the analysis into a one-liner and post it to the on-call Slack channel.
- **Gate destructive remediation.** If you want the workflow to trigger remediation, add an [`if` step](/explore-analyze/workflows/steps/if.md) that only runs when the agent's confidence is high, and invoke a [child workflow](/explore-analyze/workflows/steps/composition.md) that handles the remediation in isolation.
- **Correlate across signals.** Add [`elasticsearch.esql.query`](/explore-analyze/workflows/steps/elasticsearch.md) steps before the agent call to pull metric and log context in the alert's time window, and feed them into the agent's prompt.

## Related pages [workflows-rca-related]

- [Observability workflows](/explore-analyze/workflows/use-cases/observability.md): The outcome this workflow supports.
- [AI steps reference](/explore-analyze/workflows/steps/ai-steps.md): Parameters for `ai.agent` and related AI steps.
- [{{agent-builder}} for Observability](/solutions/observability/ai/agent-builder-observability.md): How Agent Builder integrates with observability workflows.
- [{{observability}} incident management](/solutions/observability/incident-management.md): The product surface this workflow automates.
- [{{observability}} alerting](/solutions/observability/incident-management/alerting.md): How alert triggers fire on {{observability}} rules.
- [Cases action steps](/explore-analyze/workflows/steps/cases.md): Full reference for `cases.*` steps.
- [`elastic/workflows` examples folder](https://github.com/elastic/workflows/tree/main/workflows/examples): More end-to-end examples.
