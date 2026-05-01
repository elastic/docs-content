---
navigation_title: AI-driven alert triage
applies_to:
  stack: ga 9.4+
  serverless: ga
description: Build a workflow that uses an Agent Builder agent to analyze Attack Discovery alerts, create a case with the analysis attached, isolate the affected host, and notify the SOC.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Triage alerts with an AI agent [workflows-ai-driven-alert-triage]

This guide walks through building a workflow that triages [Attack Discovery](/solutions/security/ai/attack-discovery.md) alerts with an [{{agent-builder}}](/explore-analyze/ai-features/elastic-agent-builder.md) agent. The workflow creates a case for each discovery, has an agent produce a remediation analysis, posts a concise summary to Slack, and isolates the host pending review.

The workflow is adapted from [`ad-automated-triaging.yaml`](https://github.com/elastic/workflows/blob/main/workflows/security/response/ad-automated-triaging.yaml) in the `elastic/workflows` library.

If you're new to workflows, complete [Build your first workflow](/explore-analyze/workflows/get-started/build-your-first-workflow.md) first.

## Before you begin [workflows-ai-driven-alert-triage-prereqs]

- **Permissions.** `All` on **Analytics > Workflows**, **Security > Cases**, and whatever Agent Builder privilege is required to invoke agents in your space. Refer to [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).
- **Attack Discovery enabled.** Attack Discovery must be running in your {{elastic-sec}} deployment and producing findings. Refer to [Attack Discovery](/solutions/security/ai/attack-discovery.md).
- **Agent Builder agent.** A configured agent in {{agent-builder}} that can reason over security context. Use one of the built-in agents (for example, the Elastic AI Agent) or a [custom agent](/explore-analyze/ai-features/agent-builder/custom-agents.md). Note the agent ID.
- **Slack connector.** A Slack [connector](/deploy-manage/manage-connectors.md) or webhook URL for notifications.
- **Attach the workflow to a rule.** After saving the workflow, attach it to the Attack Discovery detection rule or the rule group you want to triage. Refer to [Alert triggers](/explore-analyze/workflows/triggers/alert-triggers.md).

## How it works [workflows-ai-driven-alert-triage-how-it-works]

The workflow runs whenever the attached rule fires. Because Attack Discovery alerts batch multiple related alerts into a single finding, the workflow iterates with `foreach` over `event.alerts` and handles each discovery independently:

1. **Create a case** populated with the discovery's attack summary, affected entities, and MITRE tactics.
2. **Attach the component alerts** to the case so investigators can pivot.
3. **Call an agent** to produce a remediation and response analysis. Attach the analysis to the case.
4. **Call an agent again** to produce a short Slack-ready summary.
5. **Isolate the host** pending review.
6. **Notify Slack** with the summary, risk score, and links back to the case, host, and workflow execution.

## Build the workflow [workflows-ai-driven-alert-triage-build]

:::::{stepper}

::::{step} Trigger on Attack Discovery alerts

```yaml
triggers:
  - type: alert
    enabled: true
```

Attach the workflow to the Attack Discovery rule after saving so the rule invokes this workflow.
::::

::::{step} Iterate over each discovery

An Attack Discovery alert bundles multiple related findings. Loop over them so each discovery gets its own case:

```yaml
steps:
  - name: for_each_discovery
    type: foreach
    foreach: event.alerts
    steps:
      # Per-discovery steps go here. Use foreach.item to access the current discovery.
```

Inside the loop, `foreach.item` is the current discovery object, including `foreach.item.attack_discovery.title_with_replacements`, `foreach.item.attack_discovery.alert_ids`, and `foreach.item.risk_score`.
::::

::::{step} Open a case from the discovery

Populate the case body from the discovery's Markdown-formatted summary fields:

```yaml
- name: create_case
  type: cases.createCase
  with:
    title: "[Attack Discovery] {{ foreach.item.attack_discovery.title_with_replacements }}"
    description: |
      ## Attack summary
      {{ foreach.item.attack_discovery.summary_markdown_with_replacements }}

      ## Detailed analysis
      {{ foreach.item.attack_discovery.details_markdown_with_replacements }}

      ## Affected entities
      {{ foreach.item.attack_discovery.entity_summary_markdown_with_replacements }}

      ## Investigation context
      - Discovery ID: {{ foreach.item.uuid }}
      - Risk score: {{ foreach.item.risk_score }}
      - Alert count: {{ foreach.item.attack_discovery.alerts_context_count }}
    owner: "securitySolution"
    severity: "high"
    tags: ["auto-triage", "attack-discovery"]
```
::::

::::{step} Attach the component alerts

Loop over the alert IDs that make up the discovery and attach them:

```yaml
- name: attach_alerts
  type: foreach
  foreach: foreach.item.attack_discovery.alert_ids
  steps:
    - name: add_alert
      type: cases.addAlerts
      with:
        case_id: "{{ steps.create_case.output.id }}"
        alerts:
          - alertId: "{{ foreach.item }}"
            index: ".alerts-security.alerts-default"
            rule:
              id: "{{ event.alerts[0].kibana.alert.rule.uuid }}"
              name: "{{ event.alerts[0].kibana.alert.rule.name }}"
```
::::

::::{step} Ask an agent for a remediation plan

Call the agent with the discovery context and a specific prompt. The agent returns its analysis on `steps.triage.output.message`:

```yaml
- name: triage
  type: ai.agent
  agent-id: "{{ consts.agent_id }}"
  connector-id: "{{ consts.connector_id }}"
  create-conversation: false
  with:
    prompt: |
      How should we remediate this attack?

      - Use your knowledge of Elastic Defend to generate remediation commands.
      - Include a confidence score for the true-positive ratio.
      - Do not render videos or gifs.
      - Do not include citations.

      <detected_attack>
      {{ foreach.item | json(2) }}
      </detected_attack>
```

Then attach the agent's analysis to the case:

```yaml
- name: add_analysis
  type: cases.addComment
  with:
    case_id: "{{ steps.create_case.output.id }}"
    comment: "{{ steps.triage.output.message }}"
```
::::

::::{step} Ask an agent for a Slack-ready summary

Reuse the agent with a different prompt to get a one-to-two-sentence summary suitable for Slack:

```yaml
- name: ai_summary
  type: ai.agent
  agent-id: "{{ consts.agent_id }}"
  connector-id: "{{ consts.connector_id }}"
  create-conversation: false
  with:
    prompt: |
      Produce a one-to-two-sentence summary of the attack below for a Slack
      notification. Wrap entity names like hostnames in backticks.
      Output only the summary, no preamble.

      <detected_attack>
      {{ foreach.item | json(2) }}
      </detected_attack>
```
::::

::::{step} Isolate the affected host

Use `kibana.request` to call the endpoint isolation API and link the action to the case:

```yaml
- name: isolate_host
  type: kibana.request
  with:
    method: POST
    path: /api/endpoint/action/isolate
    body:
      endpoint_ids:
        - "{{ foreach.item.host.id }}"
      comment: "Automated isolation pending analyst review. Case {{ steps.create_case.output.id }}."
      case_ids:
        - "{{ steps.create_case.output.id }}"
```

If your Attack Discovery payload doesn't carry `host.id`, swap in a search step to look up the endpoint by hostname before isolation.
::::

::::{step} Notify Slack

Post a rich Slack message with the AI summary, the risk score, and deep links back to the workflow artifacts:

```yaml
- name: notify_slack
  type: http
  with:
    url: "{{ consts.slack_webhook }}"
    method: POST
    headers:
      content-type: application/json
    body:
      blocks:
        - type: header
          text:
            type: plain_text
            text: "Attack Discovery: {{ foreach.item.attack_discovery.title_with_replacements }}"
        - type: section
          text:
            type: mrkdwn
            text: "{{ steps.ai_summary.output.message }}"
        - type: actions
          elements:
            - type: button
              text: { type: plain_text, text: "View case" }
              url: "{{ kibanaUrl }}/app/security/cases/{{ steps.create_case.output.id }}"
            - type: button
              text: { type: plain_text, text: "View workflow run" }
              url: "{{ kibanaUrl }}/app/workflows/{{ workflow.id }}?executionId={{ execution.id }}&tab=executions"
    timeout: 30s
```
::::

:::::

## Complete workflow [workflows-ai-driven-alert-triage-complete]

:::{dropdown} Full workflow YAML

```yaml
name: security--ai-driven-triage
description: Triage Attack Discovery alerts with an AI agent. Open a case, attach analysis, isolate the host, and notify Slack.
enabled: true
tags: ["auto-triage", "attack-discovery"]

triggers:
  - type: alert
    enabled: true

consts:
  agent_id: "your-agent-id"
  connector_id: "your-connector-id"
  slack_webhook: "https://hooks.slack.com/services/YOUR/WEBHOOK/URL"

steps:
  - name: for_each_discovery
    type: foreach
    foreach: event.alerts
    steps:
      - name: create_case
        type: cases.createCase
        with:
          title: "[Attack Discovery] {{ foreach.item.attack_discovery.title_with_replacements }}"
          description: |
            ## Attack summary
            {{ foreach.item.attack_discovery.summary_markdown_with_replacements }}

            ## Detailed analysis
            {{ foreach.item.attack_discovery.details_markdown_with_replacements }}

            ## Affected entities
            {{ foreach.item.attack_discovery.entity_summary_markdown_with_replacements }}

            ## Investigation context
            - Discovery ID: {{ foreach.item.uuid }}
            - Risk score: {{ foreach.item.risk_score }}
            - Alert count: {{ foreach.item.attack_discovery.alerts_context_count }}
          owner: "securitySolution"
          severity: "high"
          tags: ["auto-triage", "attack-discovery"]

      - name: attach_alerts
        type: foreach
        foreach: foreach.item.attack_discovery.alert_ids
        steps:
          - name: add_alert
            type: cases.addAlerts
            with:
              case_id: "{{ steps.create_case.output.id }}"
              alerts:
                - alertId: "{{ foreach.item }}"
                  index: ".alerts-security.alerts-default"
                  rule:
                    id: "{{ event.alerts[0].kibana.alert.rule.uuid }}"
                    name: "{{ event.alerts[0].kibana.alert.rule.name }}"

      - name: triage
        type: ai.agent
        agent-id: "{{ consts.agent_id }}"
        connector-id: "{{ consts.connector_id }}"
        create-conversation: false
        with:
          prompt: |
            How should we remediate this attack? Reference Elastic Defend
            remediation commands, include a confidence score, and do not
            include citations or media.

            <detected_attack>
            {{ foreach.item | json(2) }}
            </detected_attack>

      - name: add_analysis
        type: cases.addComment
        with:
          case_id: "{{ steps.create_case.output.id }}"
          comment: "{{ steps.triage.output.message }}"

      - name: ai_summary
        type: ai.agent
        agent-id: "{{ consts.agent_id }}"
        connector-id: "{{ consts.connector_id }}"
        create-conversation: false
        with:
          prompt: |
            Produce a one-to-two-sentence summary of the attack below for a
            Slack notification. Wrap hostnames in backticks. Output only the
            summary.

            <detected_attack>
            {{ foreach.item | json(2) }}
            </detected_attack>

      - name: isolate_host
        type: kibana.request
        with:
          method: POST
          path: /api/endpoint/action/isolate
          body:
            endpoint_ids:
              - "{{ foreach.item.host.id }}"
            comment: "Automated isolation pending analyst review. Case {{ steps.create_case.output.id }}."
            case_ids:
              - "{{ steps.create_case.output.id }}"

      - name: notify_slack
        type: http
        with:
          url: "{{ consts.slack_webhook }}"
          method: POST
          headers:
            content-type: application/json
          body:
            blocks:
              - type: header
                text:
                  type: plain_text
                  text: "Attack Discovery: {{ foreach.item.attack_discovery.title_with_replacements }}"
              - type: section
                text:
                  type: mrkdwn
                  text: "{{ steps.ai_summary.output.message }}"
              - type: actions
                elements:
                  - type: button
                    text: { type: plain_text, text: "View case" }
                    url: "{{ kibanaUrl }}/app/security/cases/{{ steps.create_case.output.id }}"
          timeout: 30s
```

:::

## Extend this workflow [workflows-ai-driven-alert-triage-extend]

- **Gate the isolation on a confidence threshold.** Wrap `isolate_host` in an [`if` step](/explore-analyze/workflows/steps/if.md) that reads the confidence score from the agent's analysis and only isolates above a threshold.
- **Route by MITRE tactic.** Use a [`switch` step](/explore-analyze/workflows/steps/switch.md) on `foreach.item.attack_discovery.mitre_attack_tactics` to run different remediation branches per tactic.
- **Compose a shared enrichment workflow.** Extract the "enrich + analyze" sequence into a [child workflow](/explore-analyze/workflows/steps/composition.md) and call it from multiple parent workflows that need similar analysis.
- **Use `ai.summarize` instead.** If you don't need agent reasoning, replace the second `ai.agent` call with [`ai.summarize`](/explore-analyze/workflows/steps/ai-steps.md#ai-summarize) for a simpler, cheaper summary.

## Related pages [workflows-ai-driven-alert-triage-related]

- [AI steps reference](/explore-analyze/workflows/steps/ai-steps.md): Parameters for `ai.agent`, `ai.classify`, `ai.summarize`, and `ai.prompt`.
- [Call {{agent-builder}} agents from Elastic Workflows](/explore-analyze/ai-features/agent-builder/agents-and-workflows.md): How to wire agents into workflow steps.
- [Cases action steps](/explore-analyze/workflows/steps/cases.md): Full reference for `cases.*` steps.
- [Attack Discovery](/solutions/security/ai/attack-discovery.md): What Attack Discovery produces and how to enable it.
- [`elastic/workflows` library](https://github.com/elastic/workflows): More agentic and SOC automation examples.
