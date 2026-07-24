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

This page explains how to open a rule's changes history, review its version history, compare revisions, and restore the rule to a previous state. Rule changes history is available for custom rules and for installed or modified Elastic prebuilt rules.

## Open the changes history page [open-rule-changes-history]

1. Find **{{siem-rules-ui}}** in the navigation menu or by using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click the rule's name to open its details page.
3. Select **All actions** > **History**.

The changes history page opens in a split-panel layout, with the **Version history** panel on the right and a diff view on the left.

## Review the version history [review-rule-version-history]

The **Version history** panel lists every recorded change for the rule, most recent first. Each entry shows:

* Rule's revision number at that point in time (for example, `R2`)
* Elastic version number if it's a prebuilt rule (for example, `V3`)
* Action taken (for example, created, edited, enabled, disabled, deleted, imported, or restored)
* Date and time of the change
* User who made the change
* Number of changes included in that revision

Scroll to the bottom to load older entries.

## View a diff between revisions [view-rule-changes-diff]

Select any entry in the **Version history** panel to view a diff of that revision against the revision immediately before it. Added content is highlighted in green, and removed content is highlighted in red. If a revision didn't change any visible rule fields, the diff view indicates that there are no changes to display.

## Restore a rule to a previous revision [restore-rule-from-history]

If a rule was changed unexpectedly or you want to undo a set of changes, you can restore the rule to any revision in its history.

1. In the **Version history** panel, find the revision you want to restore.
2. Select the actions menu on that entry, then select **Restore this revision**.
3. Confirm the restore.

The rule is updated to match the selected revision, and a new entry is added to the version history to record the restore.

::::{note}
You can also restore a deleted rule. This re-creates the rule, but it remains disabled. You must [enable it](/solutions/security/detect-and-alert/manage-detection-rules.md#enable-disable-rules) manually.
::::

::::{warning}
If someone else changes or deletes the rule after the revision you're restoring was captured, a conflict dialog warns you before you continue. You can review the conflicting changes, or restore anyway and permanently overwrite them.
::::

## Rule changes history limitations [rule-changes-history-limitations]

* You can't view or restore changes made before this feature was introduced, or while it was turned off.
* Rule changes history is read-only. You can't edit or delete version history entries.
* Capturing rule changes history adds a small amount of overhead when rules are created or updated.

## Turn off rule changes history [turn-off-rule-changes-history]

Rule changes history is turned on by default. If you want to turn it off — for example, to avoid that overhead — disable the `securitySolution:enableRuleChangesHistory` [advanced setting](/solutions/security/get-started/configure-advanced-settings.md#enable-rule-changes-history).

::::{note}
Turning off rule changes history creates a gap in rule revisions. That gap isn't filled when you turn the feature back on later, and changes made while it was off can't be recovered.
::::
