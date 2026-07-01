---
applies_to:
  stack: preview 9.3, ga 9.4+
  serverless: ga
description: Understand alert triggers and how to create and configure them.
products:
  - id: kibana
  - id: cloud-serverless
  - id: cloud-hosted
  - id: cloud-enterprise
  - id: cloud-kubernetes
  - id: elastic-stack
---

# Alert triggers

Alert triggers run workflows automatically when detection or alerting rules generate an alert. Use alert triggers for alert enrichment, automated incident response, case creation, or notification routing.

Alert-triggered workflows run with the permissions of the user who last saved the rule. For details, refer to [Execution permissions](/explore-analyze/workflows/execution-permissions.md).

When a rule generates an alert that triggers your workflow, the trigger provides rich context data to the workflow through the `event` field.

:::{warning}
Declaring `type: alert` on a workflow isn't enough to run the workflow when alerts fire. You also have to attach the workflow to the rule's **Actions** using a **Run Workflow** action. Without the attachment, the rule fires alerts but the workflow is never invoked. This is the single most common setup mistake.
:::

## Schema [workflows-alert-trigger-schema]

| Parameter | Type | Required | Description |
|---|---|---|---|
| `type` | string | Yes | Must be `alert`. |

That's the entire trigger schema. There's no `with` block on an alert trigger: rule targeting happens in the alerting rule's **Actions** configuration, not in the workflow.

```yaml
triggers:
  - type: alert
```

## Setup [workflows-alert-trigger-setup]

To set up an alert trigger, follow these steps:

:::::{stepper}

::::{step} Define an alert trigger
Create a workflow with an alert trigger:

```yaml
name: Security Alert Response
description: Enriches and triages security alerts
enabled: true
triggers:
  - type: alert
steps:
  ....
```
::::

::::{step} Configure the alert rule
After creating your workflow, configure your alert rule to trigger it.

::::{tab-set}

:::{tab-item} Alerting rules (Stack and Observability)
1. Go to **{{rules-ui}}** in **{{stack-manage-app}}** or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Find or create the alerting rule you want to trigger the workflow.
3. In the rule settings, under **Actions**, select **Add action**.
4. Select **Workflows**.
5. Select your workflow from the dropdown or create a new one. You can only select enabled workflows.
6. Under **Action frequency**, choose whether to run separate workflows for each generated alert.
7. (Optional) Add multiple workflows by selecting **Add action** again.
8. Create or save the rule.

:::{image} /explore-analyze/images/workflows-alerting-rule-action.png
:alt: Alerting rule settings showing a workflow selected as an action 
:screenshot:
:::

:::

:::{tab-item} Security detection rules
1. Go to **{{siem-rules-ui}}** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Find or create the detection rule you want to trigger the workflow.
3. In the rule settings, under **Actions**, select **Workflows**.
4. Select your workflow from the dropdown or create a new one. You can only select enabled workflows.
5. Under **Action frequency**, choose whether to run separate workflows for each generated alert.
6. (Optional) Add multiple workflows by selecting **Add action**.
7. Create or save the rule.

:::{image} /explore-analyze/images/workflows-detection-rule-action.png
:alt: Detection rule settings showing a workflow selected as an action
:screenshot:
:::

:::

::::

::::

:::::

When the configured rule generates an alert, your workflow automatically executes with the alert context.

## Alert event payload [workflows-alert-trigger-event]

When an attached rule fires, the workflow runs and receives the alert payload through the `event` context variable:

| `event.*` field | Contains |
|---|---|
| `event.alerts` | Array of alert documents produced by the rule. |
| `event.rule` | Metadata about the rule that fired, including `id`, `name`, `tags`, and `type`. |
| `event.spaceId` | The {{kib}} space the rule belongs to. |
| `event.params.*` | Any params configured on the rule's **Run Workflow** action. |

Reference these fields with Liquid templating in workflow steps:

```yaml
- name: log
  type: console
  with:
    message: |
      Got {{ event.alerts | size }} alerts from rule "{{ event.rule.name }}".
      First host: {{ event.alerts[0].host.name }}
```

The shape of an individual alert document inside `event.alerts` depends on the rule type (detection rule, alerting rule, or ES|QL rule) and the source data the rule runs against. Common fields include `_id`, `_index`, `host.name`, `user.name`, `kibana.alert.severity`, `kibana.alert.risk_score`, and `kibana.alert.start`.

% Ben Ironside Goldstein, 2026-04-16: Alert event payload fields depend on rule type (detection vs
% alerting vs ES|QL) and source data. The generic examples here are conservative, but an SME pass
% on which fields are guaranteed present in 9.4 GA across rule types would strengthen this page.
% Flagged in PR summary.

## Alert states [workflows-alert-trigger-states]

When you attach a workflow to an alerting rule, you can choose which alert states trigger it:

| State | Meaning | Default |
|---|---|---|
| `new` | First time this alert has fired. | On |
| `ongoing` | Alert is continuing from a previous check. | Off |
| `recovered` | Alert has cleared and returned to normal. | Off |

Security detection rules produce only `new` alerts, so the state checkboxes are hidden for them. Observability rules that track ongoing conditions benefit from separate workflows per state. For example, a first-response workflow on `new` and a recovery-notification workflow on `recovered`.

