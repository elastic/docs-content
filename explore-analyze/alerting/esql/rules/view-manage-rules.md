---
navigation_title: View and manage rules
applies_to:
  stack: ga 9.6+
  serverless: ga
products:
  - id: kibana
description: "Search, filter, and bulk-manage rules. Use inline editing, the rule summary flyout, and the rule details page to manage rules and rotate their API keys."
---

# View and manage rules in {{alerting-v2-system}} [manage-rules]

After you create {{alerting-v2-system}} rules, use the **Rules** page to keep track of them. Search and filter to find the ones you need, check status and recent activity at a glance, and make changes without losing your place in the list.

To open the **Rules** page, go to **Alerting** → **Rules** in the {{observability}} navigation menu, or find **Rules** using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

## Find and filter rules [find-filter-rules]

Use the search bar to find rules by name or description. Each space-separated term is matched independently using prefix matching. Tags and grouping fields appear in results but aren't searchable.

Combine text search with filter controls to narrow by rule type, status, or tags. Select any column header to sort. Use bulk actions to enable, disable, or delete several rules at once, or to [rotate their API keys](#rotate-rule-api-key).

## Edit a rule inline [quick-edit-rule]

To update common rule settings without opening the full rule details page, use the inline edit option on any row on the **Rules** page. The inline editor also opens from the rule summary flyout header.

Use inline edit when you need to adjust metadata or scheduling settings quickly without navigating away from the list.

## Inspect a rule with the summary flyout [rule-summary-flyout]

To inspect a rule without navigating away from the **Rules** page, select the expand icon on any row. The rule summary flyout opens alongside the list and shows a snapshot of the rule: its status, last run time, recent alert activity, and quick actions such as enable, disable, and snooze.

Use the flyout when you want to confirm a rule is healthy or take a quick action without committing to a full page load. To open the complete rule configuration with all settings and edit controls, select the rule name in the table row or in the flyout header.

## Review rule configuration and activity [rule-details-page]

The rule details page is organized into tabs that let you review a rule's configuration and activity history.

- **Overview**: For rules that group matches into an alert, this tab shows a color-coded activity timeline per series, summary statistics, and a link to matching alerts on the **Alerts** page. Every rule also has an **Artifacts** section for linked dashboards and (if your role can read them) linked action policies.
- **Conditions**: The rule's base query, alert condition, schedule, lookback, grouping, and recovery settings.
- **Runbook**: The rule's investigation guide, if one has been added. Use it to document steps for diagnosing or responding to alerts produced by this rule.

Use **Edit** to modify the rule. From the actions menu, you can enable, disable, clone, or delete the rule, or [rotate its API key](#rotate-rule-api-key).

## Disable or snooze a rule [disable-snooze-rule]

Use **Disable** when you want the rule to stop running entirely until you re-enable it. Snoozing is different: the rule keeps evaluating, but you suppress notifications or quiet a specific series or action policy.

## Rotate a rule's API key [rotate-rule-api-key]

A rule queries your data with an API key based on the credentials of the user who creates or enables it. Rotating the key gives the rule a new key based on your credentials, without editing the rule. Editing the rule doesn't replace the key, and the key doesn't expire on its own, so the rule can keep running with access that the user no longer has.

In {{serverless-short}}, the new key is an {{ecloud}} API key. In {{stack}}, it's an {{es}} API key. To learn how each key type handles later role changes, refer to [Which type of API key a rule uses](../manage/authorization.md#rule-api-key-type).

Before you rotate a key, make sure your own access covers the data the rule queries. The new key carries your access, so the rule can reach only the data that you can reach. If you have less access than the rule's current key, the rule might fail or miss data on its next run.

**Update API key** is available only for enabled rules. If a rule is disabled, you don't need to rotate its key. Enabling the rule gives it a new key based on your credentials.

To rotate a key, select **Update API key**, then confirm. {{kib}} generates the new key, invalidates the previous one, and keeps the rule's schedule and enabled state. After the rotation, **Last updated by** on the rule details page shows your name. Because editing a rule also updates **Last updated by**, that field doesn't always show whose key the rule uses.

You can select **Update API key** from any of these places:

- The rule details page
- A row's actions menu on the **Rules** page
- The rule summary flyout
- The bulk actions menu on the **Rules** page

When you rotate keys in bulk, {{kib}} rotates every key it can. If some keys can't be rotated, the notification lists those rules and the reason for each.

## Related pages

- [Create a rule](create-a-rule.md): Compare rule creation paths and choose the one that fits your workflow.
- [Review rule execution history](review-rule-execution-history.md): Monitor rule execution outcomes across all rules in a space.
- [Review rule change history](review-rule-change-history.md): See who changed a rule and when, and compare its versions.
- [View and manage alerts](../alerts/view-and-manage-alerts.md): Triage and investigate the alerts a rule produces.
- [Rule, action policy, and workflow authorization](../manage/authorization.md): Understand which credential authorizes each operation and how to fix authorization errors.
- [Manage action policies](../action-policies/manage-action-policies.md): Rotate an action policy's API key, which is separate from a rule's.
