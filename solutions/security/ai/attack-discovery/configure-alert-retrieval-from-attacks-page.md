---
navigation_title: Configure Attack Discovery settings
description: "Configure alert retrieval, generation, and validation for Attack Discovery from the Attacks view."
applies_to:
  stack: preview =9.4, ga 9.5+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Configure Attack Discovery settings from the Attacks view [configure-alert-retrieval-from-attacks-page]

You can configure which alerts Attack Discovery retrieves, and how discoveries are created and checked. Use the following table to find the section that matches your setup.

| Your setup | Available in | Go to |
|---|---|---|
| [Attack Discovery Workflows](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) is turned on. Configure alert retrieval methods, generation, and validation for manual runs and schedules. | {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | [Configure alert retrieval, generation, and validation](#attacks-page-settings-flyout) |
| Attack Discovery Workflows is turned off. Configure alerts for manual runs with the query bar, time filter, and alerts slider. | {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` | [Configure alerts for manual runs with the query bar and alerts slider](#attacks-page-classic-settings) |
| Attack Discovery Workflows is turned off, or not available in your version. Configure alerts for scheduled runs with the query bar, time filter, and alerts slider. | {applies_to}`stack: preview =9.4, ga 9.5+` {applies_to}`serverless: ga` | [Configure alerts for scheduled runs with the query bar and alerts slider](#attacks-page-schedule-alert-selection) |

## Configure alert retrieval, generation, and validation [attacks-page-settings-flyout]
```{applies_to}
stack: ga 9.5+
serverless:
  security: ga
```

When [Attack Discovery Workflows](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) is turned on, use **Attack discovery settings** to control which alerts Attack Discovery analyzes, which LLM creates the discoveries, and how those discoveries are checked before they're saved as attacks. Your choices apply to the manual runs you start from the **Attacks** view and are saved for you on this browser. Schedules can use different settings. 

To open the **Attack discovery settings** flyout, select **Settings** next to **Run** on the **Attacks** page.

### Choose an alert retrieval method [attacks-page-alert-retrieval-method]

Under **Alert retrieval method**, choose one or more ways to collect the alerts Attack Discovery analyzes. At least one method must stay enabled.

| Toggle | Default | What it does | When to use it |
|---|---|---|---|
| **Attack discovery skill retrieves alerts** | On | The skill retrieves and curates additional relevant alerts on top of any alerts collected by the other retrieval methods. | Keep this on for broad coverage. Use it alone for general monitoring, or with a query or workflow when you want the skill to still add related alerts. |
| **{{esql}} or custom query** | Off | Retrieves alerts that match a query you define. | Turn this on when you already know which alerts matter, for example high-severity alerts or a specific rule set. With the toggle on, **Edit with AI** appears next to the query editor so you can refine the query through chat in {{agent-builder}}. |
| **Alert retrieval workflows** | Off | Runs one or more user-authored workflows to retrieve and enrich alerts. | Turn this on when your team maintains reusable retrieval or enrichment logic in Workflows. Select which workflows to run. Select the info icon next to the toggle for a copy-pasteable example. For building custom retrieval workflows, refer to [Run Attack Discovery from a workflow](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md). |

Common setups:

* **Skill only (default):** Broad alert selection without writing a query.
* **Skill plus {{esql}} or workflows:** Focus the run with a query or workflow, and still let the skill add related alerts.
* **{{esql}} or workflows only:** Analyze only the alerts your query or workflows return. Turn off **Attack discovery skill retrieves alerts** for this.

After you choose your retrieval methods, continue with [generation](#attacks-page-generation) and [validation](#attacks-page-validation).

### Understand how alert retrieval methods combine [attacks-page-alert-merge]

When you enable more than one **Alert retrieval method** toggle, Attack Discovery combines their results before analysis:

1. **{{esql}} or custom query** and **Alert retrieval workflows** each add matching alerts.
2. If **Attack discovery skill retrieves alerts** is also on, the skill can add related alerts on top of that result.
3. If the same alert appears from more than one method, Attack Discovery keeps one copy.

:::{important}
The **Attack discovery skill retrieves alerts** toggle only controls whether the skill adds extra related alerts. For manual, scheduled, and workflow-triggered runs, the skill still reviews the collected alerts during generation.
:::

:::{note}
Manual, scheduled, and workflow-triggered runs open a new {{agent-builder}} conversation you can view later. Open it from **Workflow execution details** with **Open conversation**. Runs started from {{agent-builder}} chat stay in the current conversation.
:::

### Choose a connector for generation [attacks-page-generation]

Under **Generation**, select the **Connector for generating attack discoveries**. You must select a connector before you can save alert retrieval settings or start a manual run. Schedules can use their own connector when you create or edit them.

* Use a model that performs well for Attack Discovery. Refer to the [Large language model performance matrix](/solutions/security/ai/large-language-model-performance-matrix.md) for recommended models.
* If you don't already have a connector, add one from the connector dropdown. Refer to [{{connectors-ui}}](/deploy-manage/manage-connectors.md).

If you want to call Attack Discovery from automation instead, select **View example** to open the managed **Security - Attack discovery - Run example** workflow. Refer to [Run Attack Discovery from a workflow](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md) for more information.

Next, [choose a validation workflow](#attacks-page-validation).

### Choose a validation workflow [attacks-page-validation]

Under **Validation**, choose what happens to discoveries after generation and before they're saved as attacks.

For most setups, keep **Security - Attack discovery - Default validation**. That workflow:

1. Removes discoveries that reference alert IDs that were not part of the analysis (hallucinated IDs).
2. Deduplicates the remaining discoveries.
3. Saves the results as attacks.

Choose a different workflow only when you need extra steps before save, such as enrichment, stricter filtering, or org-specific checks. You can:

* Select **View example** to open **Security - Attack discovery - Custom validation example**, which shows how to run the default checks and then change discovery fields before saving.
* Select **Create a new workflow** to build your own validation workflow.

:::{important}
If you create a custom validation workflow, it must save the discoveries you want to keep. Otherwise they never appear as attacks. For details, refer to [Create custom retrieval and validation workflows](/solutions/security/ai/attack-discovery/run-attack-discovery-in-a-workflow.md#run-ad-workflow-custom).
:::

Select **Save** to keep the settings, or **Save and run** to save and start a manual run immediately. You can also [start a manual run](/solutions/security/ai/attack-discovery/manual-runs-from-attacks-page.md) later with **Run**, or [create a schedule](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md).

## Configure alerts for manual runs with the query bar and alerts slider [attacks-page-classic-settings]
```{applies_to}
stack: ga 9.5+
serverless:
  security: ga
```

When [Attack Discovery Workflows](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) is turned off, use **Attack discovery settings** to choose which alerts to analyze. You set a query and time range, then choose how many alerts to send. Your choices apply to the manual runs you start from the **Attacks** view and are saved for you on this browser. Schedules can use different settings.

To open the **Attack discovery settings** flyout, select **Settings** next to **Run** on the **Attacks** page, then:

1. Select a **Connector for generating attack discoveries**.
2. Optionally add a KQL query and set the time range.
3. Use **Set number of alerts to analyze** to choose how many alerts to send. Send fewer alerts if the model's context window is small, or more if it is larger.
4. Review the selection under **Alert summary** or **Alerts preview**.
5. Select **Save**, or **Save and run** to start analysis immediately.

Sending more alerts than your chosen LLM can handle may result in an error.

## Configure alerts for scheduled runs with the query bar and alerts slider [attacks-page-schedule-alert-selection]
```{applies_to}
stack: preview =9.4, ga 9.5+
serverless:
  security: ga
```

When [Attack Discovery Workflows](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) is turned off, or not available in your version, set which alerts each schedule analyzes when you create or edit it. You choose a query, a time range, and how many alerts to send. Sending more alerts than your chosen LLM can handle may result in an error.

Refer to [Schedule runs from the Attacks view](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md) to finish creating or editing the schedule.
