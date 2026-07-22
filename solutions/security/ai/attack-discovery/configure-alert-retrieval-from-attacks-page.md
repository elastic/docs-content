---
navigation_title: Configure Attack Discovery settings
description: "Configure alert retrieval, generation, and validation for Attack Discovery from the Attacks view."
applies_to:
  stack: preview =9.4, ga 9.5+
  serverless: ga
products:
  - id: security
  - id: cloud-serverless
---

# Configure Attack Discovery settings from the Attacks view [configure-alert-retrieval-from-attacks-page]

Choose which alerts to analyze and how generation and validation run. From the **Attacks** view, use the settings flyout when Attack Discovery Workflows is on, or the schedule flyout's alert selection controls when it is off. Use the table to find the right section. After you configure settings, [start a manual run](/solutions/security/ai/attack-discovery/manual-runs-from-attacks-page.md) or [create a schedule](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md).

| Your setup | Available in | Go to |
|---|---|---|
| [Attack Discovery Workflows](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) is turned on. Configure alert retrieval methods, generation, and validation for manual runs and schedules. | {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | [Configure the Attack discovery settings flyout](#attacks-page-settings-flyout) |
| Attack Discovery Workflows is turned off. Use the KQL query bar, time filter, and alerts slider when you create or edit a schedule. | {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | [Select alerts in the schedule flyout](#attacks-page-schedule-alert-selection) |
| You are creating or editing a schedule on the **Attacks** page. | {applies_to}`stack: preview =9.4` | [Select alerts in the schedule flyout](#attacks-page-schedule-alert-selection) |

## Configure the Attack discovery settings flyout [attacks-page-settings-flyout]
```{applies_to}
stack: ga 9.5+
serverless: ga
```

Open the **Attack discovery settings** flyout from the **Attacks** view by selecting **Settings**. Use it to configure alert retrieval, generation, and validation.

### Choose an alert retrieval method [attacks-page-alert-retrieval-method]

Under **Alert retrieval method**, choose how alerts are collected. Each method can add alerts to the set that Attack Discovery analyzes. At least one method must stay enabled. You can turn on more than one method at a time.

| Toggle | Default | What it does | When to use it |
|---|---|---|---|
| **Attack discovery skill retrieves alerts** | On | The skill finds and adds related alerts on top of whatever the other methods collect. | Keep this on for broad coverage. Use it alone for general monitoring, or with a query or workflow when you want the skill to still add related alerts. |
| **{{esql}} or custom query** | Off | Retrieves alerts that match a query you define. | Turn this on when you already know which alerts matter, for example high-severity alerts or a specific rule set. With the toggle on, an AI-assisted editing option appears next to the query editor so you can refine the query through chat in {{agent-builder}}. |
| **Alert retrieval workflows** | Off | Runs one or more user-authored workflows to retrieve and enrich alerts. | Turn this on when your team maintains reusable retrieval or enrichment logic in Workflows. Select which workflows to run. For building custom retrieval workflows, refer to [Run Attack Discovery from a workflow](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md). |

Common setups:

* **Skill only (default):** Broad alert selection without writing a query.
* **Skill plus {{esql}} or workflows:** Focus the run with a query or workflow, and still let the skill add related alerts.
* **{{esql}} or workflows only:** Analyze only the alerts your query or workflows return. Turn off **Attack discovery skill retrieves alerts** for this.

After you choose your retrieval methods, continue with [generation](#attacks-page-generation) and [validation](#attacks-page-validation).

### Understand how alert retrieval methods combine [attacks-page-alert-merge]

When you enable more than one **Alert retrieval method** toggle, Attack Discovery merges their results before analysis:

1. **{{esql}} or custom query** and **Alert retrieval workflows** run at the same time and each add matching alerts.
2. If **Attack discovery skill retrieves alerts** is also on, the skill adds related alerts on top of that result.
3. Attack Discovery then checks the collected alerts before saving discoveries. This check is skipped for runs started from {{agent-builder}}, because the agent already verifies its own data. If the same alert appears from more than one method, Attack Discovery keeps the more complete version.

:::{important}
Turning off **Attack discovery skill retrieves alerts** doesn't turn the skill off. The skill still enriches, validates, and searches related evidence on every run. The toggle only controls whether the skill adds *extra* alerts beyond what your query or workflows already supply.
:::

:::{note}
Each time the Attack Discovery skill runs, {{agent-builder}} opens a new conversation for that run. This happens for manual runs, scheduled runs, and other skill-backed triggers, not only when you start from chat.
:::

### Choose a connector for generation [attacks-page-generation]

Under **Generation**, choose the LLM that turns the collected alerts into attack discoveries. This step runs after alert retrieval and before validation.

1. Select the **Connector for generating attack discoveries**. Attack Discovery cannot run without a connector.
2. Prefer a model that performs well for Attack Discovery. Refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md) for recommended models.
3. If you do not already have a connector, add one from the connector dropdown. Refer to [{{connectors-ui}}](/deploy-manage/manage-connectors.md).

The connector you select here applies to manual runs from the **Attacks** view. Schedules can use their own connector when you create or edit them.

If you want to call Attack Discovery from automation instead of from this view, select **View example** to open a working example in the Workflows editor. Refer to [Run Attack Discovery from a workflow](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md).

Next, [choose a validation workflow](#attacks-page-validation).

### Choose a validation workflow [attacks-page-validation]

Under **Validation**, choose what happens to discoveries after generation and before they are saved as attacks. Use this step to check, enrich, or filter findings so only the results you want are saved.

1. Select a **Validation workflow**. For most teams, keep the default **Security - Attack discovery - Default validation**.
2. Select **View example** if you want to inspect how a validation workflow is built before you change anything.
3. Select **Create a new workflow** only when you need custom logic, such as extra enrichment, stricter filtering, or org-specific checks.

:::{important}
Custom validation workflows must explicitly save discoveries. For details, refer to [Create custom retrieval and validation workflows](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md#run-ad-workflow-custom).
:::

After you save these settings, [start a manual run](/solutions/security/ai/attack-discovery/manual-runs-from-attacks-page.md) or [create a schedule](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md).

## Select alerts in the schedule flyout [attacks-page-schedule-alert-selection]

Use the schedule flyout's KQL query bar, time filter, and alerts slider to choose which alerts the schedule analyzes. Sending more alerts than your chosen LLM can handle may result in an error.

Refer to [Schedule runs from the Attacks view](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md) to finish creating or editing the schedule.
