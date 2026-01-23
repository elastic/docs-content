---
applies_to:
  stack: preview 9.3
  serverless: preview
description: Understand alert triggers and how to create and configure them.
---

# Alert triggers

Alert triggers run workflows automatically when detection or alerting rules generate an alert. Use alert triggers for alert enrichment, automated incident response, case creation, or notification routing.

When a rule generates an alert that triggers your workflow, the trigger provides rich context data to the workflow through the `event` field.

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

:::{tab-item} Alerting rules
1. Go to **{{rules-ui}}** in **{{stack-manage-app}}** or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Find or create the alerting rule you want to trigger the workflow.
3. In the rule settings, under **Actions**, select **Add action**.
4. Select **Workflows**.
5. Select your workflow from the dropdown or create a new one. You can only select enabled workflows.
6. Choose whether to run separate workflows for each generated alert.
7. (Optional) Add multiple workflows by selecting **Add action** again.
8. Create or save the rule.
:::

:::{tab-item} Security detection rules
1. Go to **Detection rules (SIEM)** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Find or create the detection rule you want to trigger the workflow.
3. In the rule settings, under **Actions**, select **Workflows**.
4. Select your workflow from the dropdown or create a new one. You can only select enabled workflows.
5. Choose whether to run separate workflows for each generated alert.
6. (Optional) Add multiple workflows by selecting **Add action**.
7. Create or save the rule.
:::

::::

::::

:::::

When the configured rule generates an alert, your workflow automatically executes with the alert context.

