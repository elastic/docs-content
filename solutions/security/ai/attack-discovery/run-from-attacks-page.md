---
navigation_title: Run from Attacks view
description: "Configure, run, and schedule Attack Discovery from the Attacks view under Detections."
applies_to:
  stack: preview =9.4, ga 9.5+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Run Attack Discovery from the Attacks view [run-from-attacks-page]

From the **Attacks** view, configure which alerts to analyze, then start a manual or scheduled run. Discoveries appear in the same view next to their related alerts.

## Before you begin [run-from-attacks-page-before-you-begin]

To use the **Attacks** view, you need:

* The [Enable alerts and attacks alignment](/solutions/security/get-started/configure-advanced-settings.md#enable-alerts-and-attacks-alignment) advanced setting turned on (only required for {{stack}} 9.4.x). 
* The [Attack Discovery Workflows](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) advanced setting turned on if you want the settings flyout with skill, query, and workflow retrieval.
* A role with the [index privileges](/solutions/security/ai/attack-discovery/grant-access.md#ad-index-privileges) required to generate and read discoveries, and these [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-role-management.md#adding_kibana_privileges) at minimum:
  * **Security > Attack discovery**: `All`
  * **Security > Rules and Exceptions**: `Read`
  * **Security > Alerts**: `Read`

## Start a manual or scheduled run [attacks-view-start-a-run]

::::{applies-switch}

:::{applies-item} { "stack": "ga 9.5+", "serverless": {"security": "ga"} }
1. Open the **Attacks** view at **Detections > Views > Attacks**.
2. [Configure Attack Discovery settings](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md).
3. Start Attack Discovery with a [manual run](/solutions/security/ai/attack-discovery/manual-runs-from-attacks-page.md) or a [scheduled run](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md).

:::

:::{applies-item} stack: preview =9.4

1. Open the **Attacks** view at **Detections > Views > Attacks**.
2. [Configure which alerts to analyze](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md#attacks-page-schedule-alert-selection) when you create or edit a schedule (classic schedule flyout controls).
3. [Schedule runs](/solutions/security/ai/attack-discovery/schedule-runs-from-attacks-page.md) from **Attacks**, or [manually run Attack Discovery](/solutions/security/ai/attack-discovery/manual-runs-from-attacks-page.md) from the Attack Discovery page.

:::

::::
