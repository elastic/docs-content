---
navigation_title: Review rule change history
applies_to:
  stack: experimental 9.6+
  serverless: experimental
products:
  - id: kibana
description: "Review a rule's change history in the experimental alerting system to see who changed a rule and when, and compare versions with a JSON diff."
---

# Review rule change history in the {{alerting-v2-system}} [review-rule-change-history]

A rule's change history records each change made to the rule's configuration, so you can trace how a rule reached its current state, confirm who changed it and when, and compare two versions to see which fields differ.

To open a rule's change history, do one of the following:

- From **Rules**, open a rule's actions menu, then select **View change history**.
- From a rule's details page, open the actions menu, then select **View change history**.

The change history lists each previous version of the rule with the following details:

| Detail | Description |
|---|---|
| **Author** | The user who made the change. |
| **Timestamp** | When the change was made. |
| **Action** | The kind of change made to the rule. |

Select two versions to compare them. The comparison shows a JSON diff of the rule's configuration that highlights the fields that differ between the versions you selected.

:::{note}
Change history is read-only. You can review and compare previous versions, but you can't restore a rule to an earlier version.
:::

## Related pages

- [View and manage rules](view-manage-rules.md): Find the rule you want to inspect, then edit or delete it.
- [Review rule execution history](review-rule-execution-history.md): Monitor whether a rule runs on schedule and succeeds, rather than how its configuration changed.
- [Configure a rule](configure-a-rule.md): Understand the settings that appear in a rule's change history.
