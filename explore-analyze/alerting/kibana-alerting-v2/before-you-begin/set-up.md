---
navigation_title: Alerting setup
applies_to:
  stack:
    since: "9.4"
products:
  - id: kibana
description: "Enable Kibana alerting v2, data streams created for alert events and actions, optional API key cleanup settings, and verification steps."
---

# Set up Kibana alerting v2 [alerting-set-up-v2]

Kibana alerting v2 is available in {{stack}} 9.4 and later. This page explains how to enable it and configure initial settings.

## Enable Kibana alerting v2

Kibana alerting v2 is available in 9.4 and later. When it is enabled for your deployment, use Management > Alerts and Insights > Rules V2 to open the v2 rules list and author rules. If Rules V2 does not appear in the navigation, ask your administrator whether alerting v2 is enabled in your environment.

## Index configuration

Kibana alerting v2 automatically creates and manages the following data streams:

- `.rule-events` stores signal and alert event documents produced each time a rule runs. This is an append-only data stream.
- `.alert-actions` stores alert action records such as acknowledge, snooze, deactivate, fire, and suppress for suppression tracking and audit.

No manual index configuration is required. The system creates these data streams with the appropriate mappings when the first rule executes.

## {{kib}} advanced settings

Optional `kibana.yml` settings control how often {{kib}} cleans up API keys for notification policies after a policy is updated or deleted:

| Setting | Default | Purpose |
|---|---|---|
| `xpack.alerting.invalidateApiKeysTask.interval` | `5m` | How often {{kib}} processes keys that are marked for invalidation |
| `xpack.alerting.invalidateApiKeysTask.removalDelay` | `1h` | How long to wait after invalidation before old key material can be removed |

Change these only when your operations team or Elastic Support recommends it. Aggressive values can affect how reliably workflows run after policy changes.

## Verify the installation

To verify that Kibana alerting v2 is working:

1. Navigate to Management > Alerts and Insights > Rules V2.
2. Confirm that the rules list page loads.
3. Click Create rule to confirm the rule form opens.
4. Optionally, create a test rule with a simple ES|QL query and verify that alert events appear in Discover by querying the `.rule-events` data stream.
