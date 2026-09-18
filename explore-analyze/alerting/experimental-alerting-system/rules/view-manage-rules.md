---
navigation_title: View and manage rules
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Search, filter, and bulk-manage rules in the experimental alerting system. Use inline editing, the rule summary flyout, and the rule details page to manage rules and rotate their API keys."
---

# View and manage rules in the {{alerting-v2-system}} [manage-rules]

After you create rules in the {{alerting-v2-system}}, go to **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Rules** to keep track of them. Search and filter to find the ones you need, check status and recent activity at a glance, and make changes without losing your place in the list.

## Find and filter rules [find-filter-rules]

Use the search bar to find rules by name or description. Each space-separated term is matched independently using prefix matching. Tags and grouping fields appear in results but aren't searchable.

Combine text search with filter controls to narrow by rule type, status, or tags. Select any column header to sort. To act on several rules at once, use bulk actions to enable, disable, or delete them, or to [update their API keys](#rotate-rule-api-key).

## Edit a rule inline [quick-edit-rule]

To update common rule settings without opening the full rule details page, use the inline edit option on any row on the **Rules** page. The inline editor also opens from the rule summary flyout header.

Use inline edit when you need to adjust metadata or scheduling settings quickly without navigating away from the list.

## Inspect a rule with the summary flyout [rule-summary-flyout]

To inspect a rule without navigating away from the **Rules** page, select the expand icon on any row. The rule summary flyout opens alongside the list and shows a snapshot of the rule: its status, last run time, recent alert episode activity, and quick actions such as enable, disable, and snooze.

Use the flyout when you want to confirm a rule is healthy or take a quick action without committing to a full page load. To open the complete rule configuration with all settings and edit controls, select the rule name in the table row or in the flyout header.

## Review rule configuration and activity [rule-details-page]

The rule details page is organized into tabs that let you review a rule's configuration and activity history.

- **Overview** (only when matches are grouped into an alert episode): Shows a color-coded alert activity timeline per series, with summary statistics (alert episodes started, recovered, still open, and median duration) and a link to view matching alert episodes on the **Alerts** page.
- **Conditions**: The rule's base query, alert condition, schedule, lookback, grouping, and recovery settings.
- **Runbook**: The rule's investigation guide, if one has been added. Use it to document steps for diagnosing or responding to alerts produced by this rule.

Use **Edit** to modify the rule. From the actions menu, you can enable, disable, clone, or delete the rule, or [update its API key](#rotate-rule-api-key).

## Disable or snooze a rule [disable-snooze-rule]

Use **Disable** when you want the rule to stop running entirely until you re-enable it. Snoozing is different: the rule keeps evaluating, but you suppress notifications or quiet a specific series or action policy.

## Rotate a rule's API key [rotate-rule-api-key]
```{applies_to}
stack: experimental 9.6+
serverless: experimental
```

A rule queries your data with an API key from the user who last saved it. That key doesn't expire on its own, so it can outlast the privileges of the user it came from. To replace the key without editing the rule, select **Update API key**. {{kib}} generates a new key from your credentials and privileges, invalidates the previous key, and keeps the rule's schedule and enabled state. After the rotation, **Last updated by** on the rule details page shows your name.

The new key carries your privileges, so rotate a key only if you have every privilege the rule needs. If your privileges are narrower than those of the user who last saved the rule, the rule fails on its next run.

You can select **Update API key** from any of these places:

- The rule details page
- A row's actions menu on the **Rules** page
- The rule summary flyout
- Bulk actions, after you select the rules you want to update

When you rotate keys in bulk, {{kib}} names any rule it can't update in the notification and rotates the rest.

You can rotate a key only for a rule that's enabled. For a disabled rule, **Update API key** stays unavailable until you enable the rule. If a rule is running when you select the action, the rotation skips it. Try again after the run finishes.

## Related pages

- [Create a rule](create-a-rule.md): Compare rule creation paths and choose the one that fits your workflow.
- [Review rule execution history](review-rule-execution-history.md): Monitor rule execution outcomes across all rules in a space.
- [View and manage alerts](../alerts/view-and-manage-alerts.md): Triage and investigate the alert episodes a rule produces.
- [Rule, action policy, and workflow authorization](../authorization.md): Understand which credential authorizes each operation and how to fix authorization errors.