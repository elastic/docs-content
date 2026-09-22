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

Tags, runbooks, and related dashboards are optional artifacts you attach to a rule. They don't change how the rule evaluates. They give responders context when they investigate.

- **Tags**: Free-form labels for filtering and organization. A rule can have up to 20 tags, each up to 128 characters. Tags apply only to rules that group matches into an alert episode.
- **Runbooks**: An investigation guide stored with the rule so responders have context when the rule generates alerts. Runbooks apply only to rules that group matches into an alert episode.
- **Dashboards**: {{kib}} dashboards linked to the rule so responders can open investigation views from the rule details page. You can link dashboards to rules that group matches into an alert episode, and to rules that record matches without grouping them.

Whether a rule groups matches into an alert episode depends on the mode you set when you create it. Refer to [Rule mode](configure-rule-mode.md).

## When to configure tags and runbooks [tags-when-to-use]

Configure tags when:

* You want to filter alert episodes by team, environment, or severity tier on the **Alerts** page (find **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), then go to **Alerts**) without writing a custom {{kib}} Query Language (KQL) query each time.
* You are using action policies and want to scope them by ownership or category rather than by rule name.
    * {applies_to}`stack: experimental 9.6+` {applies_to}`serverless: experimental` Tags are how an action policy selects rules. Its **Rule tags** control covers every rule carrying at least one of the tags you select.
    * {applies_to}`stack: removed 9.6+, experimental =9.5` Alert episodes inherit tags, so any tag you add to a rule is available as a KQL matcher in action policies.
* You manage many rules and need a consistent labeling scheme to track which team owns which alerts.

Configure a runbook when:

* Responders who aren't familiar with the service might need to triage the alert. A runbook surfaces triage steps directly alongside the alert without requiring a separate search.
* The alert requires a consistent response process that you want encoded and version-controlled alongside the rule.

Skip tags and runbooks when:

* The rule records matches without grouping them into an alert episode.
* The rule is experimental or not yet part of a monitored production system.

## Add tags and runbooks to a rule [add-tags-runbooks]

To add tags or a runbook, your role needs **Rules: All** (under **Alerting**). Refer to [Configure access](../get-started/configure-access.md#alerting-manage-rules-privileges).

Tags and runbooks are part of the rule definition, so you set them in the rule form when you create or edit a rule:

* **Tags**: In the **Tags** field, add one or more tags. A rule can have up to 20 tags, each up to 128 characters.
* **Runbook**: Select **Add Runbook**, then write the guide in markdown. Use **Edit Runbook** to revise it later, or **Delete Runbook** to clear it.

Both are stored with the rule, so they take effect only after you save the rule. A saved runbook appears on the **Runbook** tab of the rule details page.

## When to link dashboards [dashboards-when-to-use]

Link a dashboard when responders should open the same investigation view every time the rule fires. For a checkout latency rule, that might be the dashboard showing error rates and deployment history for the checkout service.

For a dashboard you want responders to open from the rule, link it as a dashboard artifact rather than pasting its URL into the runbook. The rule details page lists linked dashboards with their current titles. Each dashboard opens in a new tab.

Skip linked dashboards when no dashboard covers the condition the rule detects, or when dashboards aren't available in your environment.

## Link dashboards to a rule [attach-dashboards]

To link dashboards, your role needs **Rules: All** (under **Alerting**). Refer to [Configure access](../get-started/configure-access.md#alerting-manage-rules-privileges). Linked dashboards appear in the **Dashboards** subsection of the **Artifacts** section on the rule details page.

::::{applies-switch}

:::{applies-item} stack: experimental =9.5

1. Find **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), go to **Rules**, then select the rule.
2. On the **Overview** tab, expand **Artifacts**.
3. In the **Dashboards** section, select **Manage linked dashboards**. The rule edit flyout opens.
4. In **Related dashboards**, search for a dashboard and select it.
5. Save the rule.

:::

:::{applies-item} { stack: experimental 9.6+, serverless: experimental }

1. Find **Alerting V2 Preview** in the navigation menu or [global search](/explore-analyze/find-and-organize/find-apps-and-objects.md), go to **Rules**, then select the rule.
2. On the **Overview** tab, expand **Artifacts**.
3. In the **Dashboards** section, select **Attach related dashboards**.
4. Search for a dashboard. Results are grouped into **Attached** and **Other dashboards**.
5. Select the dashboards to link, then select **Save**.

Selecting **Save** updates the rule right away. You don't need to save the rule separately.

You can also link dashboards while you create or edit a rule, with the optional **Related dashboards** field.

:::

::::

When a rule has no linked dashboards, the **Dashboards** section shows **No dashboards linked**.

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
