---
navigation_title: Get started
applies_to:
  serverless: preview
products:
  - id: kibana
  - id: cloud-serverless
description: "Enable {{alerting-v2}}, data streams for alert events and actions, optional API key cleanup settings, and verification steps."
---

# Get started with {{alerting-v2}} [alerting-set-up-v2]

$$$alerting-set-up-v2$$$
$$$alerting-before-you-begin-v2$$$

{{alerting-v2}} is available in {{stack}} 9.4 and later. This page explains how to enable it and configure initial settings.

## Prerequisites

To use {{alerting-v2}}, you need:

- {{stack}} 9.4 or later.
- ES|QL knowledge. {{alerting-v2}} rules are defined using ES|QL queries. Familiarity with ES|QL syntax, aggregations, and the `STATS`, `WHERE`, `EVAL`, and `KEEP` commands is essential. Refer to the [ES|QL reference](elasticsearch://reference/query-languages/esql.md) for details.
- Data indexed in {{es}}. Your source data must be indexed and accessible from the cluster where you create rules, such as logs, metrics, traces, or alert events from other rules.
- Appropriate privileges. You need Kibana privileges to create and manage rules, action policies, and workflows. Refer to [Alerting privileges](alerting-privileges.md) for details.

## Enable {{alerting-v2}}

{{alerting-v2}} is available in 9.4 and later. When it is enabled for your deployment, use Management > Alerts and Insights > Rules V2 to open the v2 rules list and author rules. If Rules V2 does not appear in the navigation, ask your administrator whether alerting v2 is enabled in your environment.

## Index configuration

{{alerting-v2}} automatically creates and manages the following data streams:

- `.rule-events` stores signal and alert event documents produced each time a rule runs. This is an append-only data stream.
- `.alert-actions` stores alert action records such as acknowledge, snooze, deactivate, fire, and suppress for suppression tracking and audit.

No manual index configuration is required. The system creates these data streams with the appropriate mappings when the first rule executes.

## {{kib}} advanced settings [kibana-advanced-settings-v2]

$$$kibana-advanced-settings-v2$$$

Optional `kibana.yml` settings control how often {{kib}} cleans up API keys for action policies after a policy is updated or deleted:

| Setting | Default | Purpose |
|---|---|---|
| `xpack.alerting_v2.invalidateApiKeysTask.interval` | `5m` | How often {{kib}} processes keys that are marked for invalidation |
| `xpack.alerting_v2.invalidateApiKeysTask.removalDelay` | `1h` | How long to wait after invalidation before old key material can be removed |

Change these only when your operations team or Elastic Support recommends it. Aggressive values can affect how reliably workflows run after policy changes.

## Verify the installation

To verify that {{alerting-v2}} is working:

1. Navigate to Management > Alerts and Insights > Rules V2.
2. Confirm that the rules list page loads.
3. Click Create rule to confirm the rule form opens.
4. Optionally, create a test rule with a simple ES|QL query and verify that alert events appear in Discover by querying the `.rule-events` data stream.

## Related

- [Core {{alerting-v2}} concepts](core-v2-alerting-concepts.md)
- [{{alerting-v2}} privileges](alerting-privileges.md)
