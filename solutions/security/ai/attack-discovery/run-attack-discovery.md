---
navigation_title: Run Attack Discovery
description: "The different ways to trigger Attack Discovery analysis, from a manual run to a fully automated, always-on pipeline."
applies_to:
  stack: ga
  serverless:
    security: ga
products:
  - id: security
  - id: cloud-serverless
---

# Run Attack Discovery [run-attack-discovery]

You can run Attack Discovery on demand or on a recurring schedule. Use the following table to find the right entry point for your needs.

| Best for | Available in | Go to |
|---|---|---|
| Creating or managing schedules without leaving the unified attack-triage view. Only supports scheduled runs, and requires turning on the [**Enable alerts and attacks alignment**](/solutions/security/get-started/configure-advanced-settings.md#enable-alerts-and-attacks-alignment) setting. | {applies_to}`stack: preview 9.4` {applies_to}`serverless: preview` | [Attacks page](/solutions/security/ai/attack-discovery/run-from-attacks-page.md) |
| Triggering an on-demand run, or setting up a schedule. The only entry point that supports on-demand runs. | {applies_to}`stack: ga` {applies_to}`serverless: ga` | [Attack Discovery page](/solutions/security/ai/attack-discovery/run-from-attack-discovery-page.md) |

:::{note}
Schedules created on either page appear on both, so you can switch between them without losing track of what's running.
:::

