---
navigation_title: Tags, runbooks, and dashboards
applies_to:
  stack: experimental 9.5+
  serverless: experimental
products:
  - id: kibana
description: "Add tags, runbooks, and related dashboards to rules in the experimental alerting system, for filtering, triage context, and investigation dashboards."
---

# Tags, runbooks, and dashboards in the {{alerting-v2-system}} [rule-artifacts]

Tags, runbooks, and related dashboards are optional artifacts you attach to a rule. Decide when each one is worth adding, then attach tags and runbooks in the rule form or link dashboards from the rule details page.

## When to add artifacts [artifacts-when-to-use]

Tags
:   Free-form labels for filtering and organization. Add them to filter alert episodes on the **Alerts** page, to scope action policies by ownership or category, or to mark which team owns a rule.

    * {applies_to}`serverless: experimental` {applies_to}`stack: experimental 9.6+` An action policy's [**Rule tags**](../action-policies/create-configure-action-policy.md#filter-by-rule-tags) control covers every rule that carries at least one of the tags you select.
    * {applies_to}`stack: removed 9.6+, experimental =9.5` {applies_to}`serverless: unavailable` Alert episodes inherit tags, so any tag on the rule is available as a KQL matcher in action policies.

Runbooks
:   An investigation guide stored with the rule. Add one when responders who don't know the service need triage steps next to the alert, or when the response should stay consistent.

Dashboards
:   {{kib}} dashboards linked from the rule details page. Link one when responders should open the same investigation view each time the rule fires. Prefer a dashboard artifact over a URL in the runbook. You can link dashboards on any rule, including rules that only record matches.

Skip tags and runbooks when the rule doesn't open [alert episodes](configure-rule-mode.md), or when it isn't in production yet. Skip dashboards when no dashboard covers the condition, or when dashboards aren't available.

## Add tags and runbooks to a rule [add-tags-runbooks]

To add tags or a runbook, your role needs **Rules: All** (under **Alerting**). Refer to [Configure access](../get-started/configure-access.md#alerting-manage-rules-privileges).

Tags and runbooks are part of the rule definition, so you set them in the rule form when you create or edit a rule:

* **Tags**: In the **Tags** field, add one or more tags. A rule can have up to 20 tags, each up to 128 characters.
* **Runbook**: Select **Add Runbook**, then write the guide in markdown. Use **Edit Runbook** to revise it later, or **Delete Runbook** to clear it.

Both are stored with the rule, so they take effect only after you save the rule. A saved runbook appears on the **Runbook** tab of the rule details page.

## Link dashboards to a rule [attach-dashboards]

To link dashboards, your role needs **Rules: All** (under **Alerting**). Refer to [Configure access](../get-started/configure-access.md#alerting-manage-rules-privileges). Linked dashboards appear in the **Dashboards** subsection of the **Artifacts** section on the rule details page.

1. Find **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), go to **Rules**, then select the rule.
2. On the **Overview** tab, expand **Artifacts**.
3. In the **Dashboards** section:
   * {applies_to}`stack: experimental 9.6+` {applies_to}`serverless: experimental` Select **Attach related dashboards**. Search for a dashboard. Results are grouped into **Attached** and **Other dashboards**. Select the dashboards to link, then select **Save**. This updates the rule right away.
   * {applies_to}`stack: experimental =9.5` Select **Manage linked dashboards**. In **Related dashboards**, search for a dashboard and select it, then save the rule.

To remove a link, select the remove icon next to the dashboard, then select **Remove** to confirm. Removing a link updates the rule right away. This removes the link only. The dashboard itself is unaffected.

## Handle deleted or unavailable dashboards [deleted-dashboards]

If a linked dashboard is deleted or you don't have access to it, the rule keeps the link rather than removing it without notice. The **Dashboards** section shows a **Dashboard deleted** or **Dashboard unavailable** badge with the dashboard's ID. The link survives when you save the rule.

Keep the link if someone might restore the dashboard or grant you access. Otherwise, remove it so you don't send responders to a dashboard they can't open.

## Examples

### Tag a rule for team ownership and severity

Tags let you filter alerts by team, environment, or severity tier. For a checkout service rule, you might add tags like:

- `team:payments`
- `env:production`
- `sev:p1`

On-call engineers can then narrow the **Alerts** page to rules their team owns without scanning every active alert episode.

### Add a runbook with triage steps

A runbook gives responders immediate context when an alert fires. Write it as Markdown so it renders correctly on the rule details page. Include enough detail that an engineer unfamiliar with the service can triage without asking for help.

```markdown
Fires when checkout error rate exceeds 10% for 3 consecutive evaluations.

Triage steps:
1. Check the checkout service deployment history in the last 30 minutes.
2. Open the checkout errors dashboard linked to this rule.
3. If errors are concentrated in one region, escalate to the infra team.
4. If errors are global, page the payments on-call lead.
```

### Link the dashboard a responder needs first

For the same checkout rule, link the dashboard that breaks down checkout errors by region and endpoint. A responder who opens the rule from an alert episode can go straight to it from **Artifacts**, instead of searching **Dashboards** for the right one mid-incident.

## Related pages

- [Configure a rule](configure-a-rule.md): All configurable rule settings, required and optional.
- [View and manage rules](view-manage-rules.md): Filter the rules list by tag, and review a rule's runbook and linked dashboards on the rule details page.
- [View and manage alerts](../alerts/view-and-manage-alerts.md): Filter the **Alerts** page by tag to narrow alert episodes to your team's rules.
- [YAML rule schema reference](yaml-rule-schema-reference.md): Artifact field names, types, and limits.
