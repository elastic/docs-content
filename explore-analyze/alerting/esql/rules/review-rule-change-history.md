---
navigation_title: Review rule change history
applies_to:
  serverless: experimental
  stack: experimental 9.6+
products:
  - id: kibana
description: "Review a rule's change history in the experimental alerting system to see who changed a rule and when, and compare versions with a JSON diff."
---

# Review rule change history in the {{alerting-v2-system}} [review-rule-change-history]

Use a rule's change history to see who changed the rule and when, and to compare any two versions of its configuration.

To open the change history, select **View change history** from any of these places:

- A rule's actions menu on the **Rules** page
- The rule summary flyout
- The actions menu on the rule's details page

The change history lists the rule's versions, newest first. A **Current version** badge marks the latest version. Each entry shows who made the change, when they made it, and the kind of change, such as `rule_create` or `rule_update`.

Select an entry to see how that version differs from the one before it. {{kib}} shows the difference as a JSON diff of the rule's configuration, with added and removed lines highlighted. The oldest entry has no earlier version, so selecting it shows its full configuration.

To compare the selected version with a different one, select the **Version actions** icon on that entry, then select **Compare to this version**.

Change history is read-only, so you can't restore an earlier version from it. To undo a change, edit the rule and set the changed fields back to their earlier values.

## Related pages

- [View and manage rules](view-manage-rules.md): Find the rule you want to inspect, then edit or delete it.
- [Review rule execution history](review-rule-execution-history.md): Monitor whether a rule runs on schedule and succeeds, rather than how its configuration changed.
- [Configure a rule](configure-a-rule.md): Understand the settings that appear in a rule's change history.
