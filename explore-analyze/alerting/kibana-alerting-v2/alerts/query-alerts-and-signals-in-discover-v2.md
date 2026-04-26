---
navigation_title: Query alerts in Discover
applies_to:
  stack: unavailable
  serverless: preview
products:
  - id: kibana
description: "Use {{esql}} in Discover against `.rule-events` and `.alert-actions`: sample queries, trends, and MTTA-style analysis for {{alerting-v2}}."
---

# Query alerts and signals in Discover [explore-alerts-discover-v2]

$$$explore-alerts-discover-v2$$$

Discover gives you direct {{esql}} access to everything {{alerting-v2}} records, including rule evaluation history, episode progressions, triage actions, and operational metrics like mean time to acknowledge.

The Alerts UI shows current episode state. Discover lets you go further: ask arbitrary questions, spot trends over time, replay how a specific incident unfolded, or correlate alert history with other data in your environment.

To use this page, open Discover, select {{esql}}, paste a query from the examples below, then adjust the time range and placeholders (`YOUR_RULE_ID`, `YOUR_GROUP_HASH`) to match your environment.

[CONTENT NEEDED: The queries on this page use `.rule-events` and `.alert-actions` directly. Confirm whether these will remain the intended query surface, or whether users should query an ES|QL view or a stable user-facing data stream instead. Update all examples accordingly before publishing.]

<!--[CONTENT NEEDED for M2: Review and expand the query examples below once M2 field renames (`group_hash` → `series.key`, new `series.tracked_by`, `episode.severity`, `episode.severity_max`) are finalized. Add examples that take advantage of the new first-class severity and series fields.]
-->

For field names, types, and episode fields, refer to [Alert states and fields reference](alert-states-and-fields-reference-v2.md#alert-states-reference-v2) and [Rule event and field reference](../rules/rule-event-field-reference-v2.md#rule-reference-v2). For triage in the product UI, refer to [View, manage, and reference alerts](view-and-manage-alerts-v2.md).

