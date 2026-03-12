---
navigation_title: Alerting setup
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Enable and configure Kibana alerting v2, including plugin dependencies, index configuration, and verification steps."
---

# Set up Kibana alerting v2 [alerting-set-up-v2]

Kibana alerting v2 is available in {{stack}} 9.4 and later. This page explains how to enable it and configure initial settings.

## Enable Kibana alerting v2

Kibana alerting v2 is enabled by default in 9.4. When enabled, a **Rules V2** tab appears in the rules management area under **Management > Alerts and Insights > Rules V2**.

## Required plugins

Kibana alerting v2 depends on the following {{kib}} plugins, which are enabled by default:

- **Task Manager** — schedules and executes rule evaluations.
- **Encrypted Saved Objects** — stores API keys securely for rule and notification policy execution.
- **ES|QL** — provides query execution for rule evaluation.
- **Spaces** — enforces space-level isolation for rules and policies.

## Index configuration

Kibana alerting v2 automatically creates and manages the following data streams:

- **`.alerts-events-*`** — stores signal and alert event documents produced by rule evaluations. This is an append-only data stream.
- **`.alerts-actions`** — stores alert action records (acknowledge, snooze, deactivate, fire, suppress) used by the dispatcher for suppression tracking and audit.

No manual index configuration is required. The system creates these data streams with the appropriate mappings when the first rule executes.

## Verify the installation

To verify that Kibana alerting v2 is working:

1. Navigate to **Management > Alerts and Insights > Rules V2**.
2. Confirm that the rules list page loads.
3. Click **Create rule** to confirm the rule form opens.
4. Optionally, create a test rule with a simple ES|QL query and verify that alert events appear in Discover by querying the `.alerts-events-*` index.
