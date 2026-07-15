---
navigation_title: View rule changes history
applies_to:
  stack: ga 9.5
  serverless: ga
products:
  - id: security
  - id: cloud-serverless
description: View a chronological history of changes made to a detection rule, compare revisions, and restore a rule to a previous state.
---

# View rule changes history [view-rule-changes-history]

Rule changes history keeps a chronological record of changes made to a detection rule, so you can see what changed, when, and who made the change. This is useful for troubleshooting unexpected rule behavior, auditing rule changes for compliance purposes, and recovering from unwanted or accidental edits.

This page explains how to open a rule's changes history, review its timeline of changes, compare revisions, and restore the rule to a previous state. Rule changes history is available for custom rules and for installed or modified Elastic prebuilt rules.

## Open the changes history page [open-changes-history]

1. Find **{{siem-rules-ui}}** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Open the rule's details page.
3. Select **All actions** > **History**.

The changes history page opens in a split-panel layout: a timeline of recorded changes on the right, and a diff view on the left.

## Review the changes timeline [review-changes-timeline]

The timeline lists every recorded change for the rule, most recent first. Each entry shows:

* Action taken (for example, created, updated, enabled, disabled, or deleted)
* Date and time of the change
* User who made the change
* Rule's revision number at that point in time

Scroll to the bottom to load older entries.

## View a diff between revisions [view-changes-diff]

Select any entry in the timeline to view a diff of that revision against the revision immediately before it. Added content is highlighted in green, and removed content is highlighted in red. If a revision didn't change any visible rule fields, the diff view indicates that there are no changes to display.

## Restore a rule to a previous revision [restore-rule-from-history]

If a rule was changed unexpectedly or you want to undo a set of changes, you can restore the rule to any revision in its history.

1. In the timeline, find the revision you want to restore.
2. Select the actions menu on that entry, then select **Restore**.
3. Confirm the restore.

The rule is updated to match the selected revision, and a new entry is added to the timeline to record the restore.

::::{note}
You can also restore a deleted rule. This re-creates the rule, but it remains disabled. You must [enable it](/solutions/security/detect-and-alert/manage-detection-rules.md#enable-disable-rules) manually.
::::

::::{warning}
If someone else changes or deletes the rule after the revision you're restoring was captured, a conflict dialog warns you before you continue. You can review the conflicting changes, or restore anyway and permanently overwrite them.
::::

## Rule changes history limitations [rule-changes-history-limitations]

* You can't view or restore changes made before this feature was introduced, or while it was turned off.
* Rule changes history is read-only. You can't edit or delete timeline entries.

## Turn off rule changes history [turn-off-rule-changes-history]

Rule changes history is turned on by default. If you want to turn it off, disable the `securitySolution:enableRuleChangesHistory` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#enable-rule-changes-history).
