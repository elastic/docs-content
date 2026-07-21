---
navigation_title: Run from Attacks view
description: "For SOC analysts: open the Attacks view under Detections to configure, run, and schedule Attack Discovery."
applies_to:
  stack: preview =9.4, ga 9.5+
  serverless: ga
products:
  - id: security
  - id: cloud-serverless
---

# Run from the Attacks view [run-from-attacks-page]

Use the **Attacks** view under **Detections** to configure which alerts Attack Discovery analyzes, then start a manual or scheduled run. For triage after a run finishes, refer to [Manage discoveries from the Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md).

## Before you begin [run-from-attacks-page-before-you-begin]

To use the **Attacks** view, you need:

* `All` for **Attack discovery**, plus at least `Read` for {{rules-ui}} and **Alerts**. For the full privilege list, refer to [Grant access to Attack Discovery](/solutions/security/ai/attack-discovery/grant-access.md).
* The [**Enable alerts and attacks alignment**](/solutions/security/get-started/configure-advanced-settings.md#enable-alerts-and-attacks-alignment) setting turned on. 
* {applies_to}`stack: ga 9.5+` {applies_to}`serverless: ga` [**Attack Discovery Workflows**](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) turned on if you want the settings flyout with skill, query, and workflow retrieval. Existing schedules do not adopt these enhancements until you [update each schedule](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md) manually.

## Open the Attacks view [open-attacks-view]

:::::{applies-switch}

::::{applies-item} { "stack": "ga 9.5+", "serverless": "ga" }

Open the **Attacks** view at **Detections > Views > Attacks**. The view includes the same run and schedule capabilities as the **Attack Discovery** page.

::::

::::{applies-item} stack: preview =9.4

Open **Attacks** at **Detections > Views > Attacks**. Use it with the [**Attack Discovery**](/solutions/security/ai/attack-discovery/index.md) page as follows:

- Go to **Attack Discovery** for manual runs.
- Go to **Attacks** for recurring schedules and day-to-day triage.

::::

:::::

## Start a run [attacks-view-start-a-run]

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.5+", "serverless": "ga" }

1. [Configure Attack Discovery settings](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md).
2. Start Attack Discovery with a [manual run](/solutions/security/ai/attack-discovery/manual-runs-from-attacks-page.md) or a [scheduled run](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md).
3. If a run fails, [troubleshoot it with AI](/solutions/security/ai/attack-discovery/troubleshoot-runs-from-attacks-page.md).
4. [Manage discoveries from the Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md).

:::

:::{applies-item} stack: preview =9.4

1. [Configure which alerts to analyze](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md#attacks-page-schedule-alert-selection) when you create or edit a schedule (classic schedule flyout controls).
2. [Schedule runs](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md) from **Attacks**, or [manually run Attack Discovery](/solutions/security/ai/attack-discovery/manual-runs-from-attacks-page.md) from the Attack Discovery page.
3. [Manage discoveries from the Attacks view](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md).

:::

::::
