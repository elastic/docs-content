---
navigation_title: Troubleshoot with AI
description: "Use AI troubleshooting from the Attacks view to diagnose failed Attack Discovery runs."
applies_to:
  stack: ga 9.5+
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Troubleshoot a run with AI [troubleshoot-runs-from-attacks-page]

Use AI troubleshooting when an Attack Discovery run fails, is canceled or dismissed, or an analysis step fails. Troubleshooting only diagnoses problems. It never changes your configuration, schedules, or discoveries.

## Before you begin [troubleshoot-runs-before-you-begin]

To troubleshoot a run with AI, you need:

* The [Attack Discovery Workflows](/solutions/security/get-started/configure-advanced-settings.md#enable-attack-discovery-workflows) advanced setting turned on.
* A run in [**Generations**](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md#attacks-view-generations) to diagnose. Use this page when a run fails, is canceled or dismissed, or an analysis step fails.

## Open AI troubleshooting [troubleshoot-runs-open]

1. Go to **Detections > Views > Attacks**.
2. Open the [**Generations**](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md#attacks-view-generations) control center in the **Attacks** view header.
3. Select a failed, canceled, or dismissed run, or a run with a failed analysis step.
4. Start AI troubleshooting.

AI troubleshooting reviews the failed run (alert retrieval, generation, and validation), identifies what went wrong, and suggests a fix. After you identify the fix, update your [Attack Discovery settings](/solutions/security/ai/attack-discovery/configure-alert-retrieval-from-attacks-page.md) if needed, then [start another manual run](/solutions/security/ai/attack-discovery/manual-runs-from-attacks-page.md) or wait for the next scheduled run.

## Download a diagnostic report [troubleshoot-runs-diagnostic-report]

From the same workflow execution details view, you can download a Markdown diagnostic report for the run. Use **Download diagnostic report** to save the file, or copy or inspect it first.

The report includes failure details, step timing, configuration context, and how the run was started. Share the downloaded file with Elastic Support when you open a case about a failed run.

The same diagnostic report is attached automatically when you start AI troubleshooting, so the agent has that context in the conversation.

:::{note}
On the **Attack Discovery** page, after a run finishes, a details button on the success or failure banner opens the workflow execution details flyout if you have workflow-read privileges. From there, the same AI troubleshooting option and diagnostic report actions are available.
:::
