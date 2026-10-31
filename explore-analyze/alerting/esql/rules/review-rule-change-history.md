---
navigation_title: Review rule change history
applies_to:
  serverless: ga
  stack: ga 9.6+
products:
  - id: kibana
description: "Find out who changed a rule and when, and compare any two versions of its configuration to see exactly what changed."
---

# Review rule change history in {{alerting-v2-system}} [review-rule-change-history]

A rule's change history shows who changed the rule, when, and exactly which settings changed. {{kib}} saves a new version of a rule each time someone creates, edits, enables, or disables it.

Use the change history to:

- Find out whether a recent edit explains why a rule started alerting more, alerting less, or stopped running.
- See who enabled or disabled a rule.
- Look up a rule's earlier settings before you change them back.

To check whether a rule's runs succeeded, rather than how its settings changed, use [rule execution history](review-rule-execution-history.md).

## Open a rule's change history [open-change-history]

Select **View change history** from any of these places:

- The rule's actions menu on the **Rules** page
- The **Take action** menu in the rule summary flyout
- The actions menu on the rule's details page

The change history opens on the newest version, so you see the most recent change first. Anyone who can view a rule can open its change history, even without permission to edit the rule.

## Find out who changed a rule and when [who-changed-rule]

The change history lists the rule's versions, newest first. Each entry shows who made the change, when they made it, and the kind of change, which is one of `rule_create`, `rule_update`, `rule_enable`, or `rule_disable`. A **Current version** badge marks the version the rule uses now.

{{kib}} records every change, including bulk actions on the **Rules** page and changes made through the API.

If the change history is empty, the rule hasn't changed since change history became available. {{kib}} doesn't record changes made before then.

## See what a change did [see-what-changed]

Select a version to see what it changed. {{kib}} compares it with the version before it and shows the difference as a JSON diff of the rule's configuration, with added and removed lines highlighted.

The oldest version has no earlier version to compare with, so selecting it shows the rule's full configuration at that point.

## Compare two versions [compare-versions]

To see everything that changed across several edits, compare two versions directly:

1. Select the newer version. To compare with the rule's current settings, select the version marked **Current version**.
2. On the older version, select {icon}`boxes_vertical` **Version actions** → **Compare to this version**.

The diff uses the older version as its starting point, so added lines show what the newer version introduced.

## Undo a change [undo-change]

Change history is read-only, so you can't restore an earlier version from it. To undo a change:

1. [Compare](#compare-versions) the current version with the version you want to go back to.
2. [Edit the rule](view-manage-rules.md#rule-details-page) and set each changed field back to its earlier value.

## Related pages

- [View and manage rules](view-manage-rules.md): Find the rule you want to inspect, then edit or delete it.
- [Review rule execution history](review-rule-execution-history.md): Monitor whether a rule runs on schedule and succeeds, rather than how its configuration changed.
- [Configure a rule](configure-a-rule.md): Understand the settings that appear in a rule's change history.
