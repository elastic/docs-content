---
navigation_title: Cases
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/cases-overview.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-overview.html
  - https://www.elastic.co/guide/en/security/current/cases-open-manage.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-open-manage.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
description: Create and manage security cases to track incidents, attach alerts, and collaborate with your SOC team using Security-specific features.
---

# Cases for {{elastic-sec}} [security-cases-overview]

Create cases to collect and share information about security incidents and investigations. You can attach alerts, document findings, and collaborate with your SOC team, all in one place. Cases also integrate with external ticketing systems like Jira, ServiceNow, and IBM Resilient, so you can escalate and track incidents across your security workflow. 

Beyond the [core case functionality](/explore-analyze/cases.md), {{elastic-sec}} lets you:

* {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` [Set an alert closing reason when closing a case](#cases-set-closing-reason)
* [View case metrics](#cases-view-metrics)
* [Attach events from Timeline](#cases-add-events)
* [Add threat intelligence indicators](#cases-indicators)
* [Attach Timelines to preserve investigation context](#cases-timeline)
* {applies_to}`stack: preview 9.5` {applies_to}`serverless: preview` [Attach entities under investigation](#cases-add-entities)
* {applies_to}`stack: ga 9.6+` {applies_to}`serverless: ga` [Attach attacks from Attack Discovery](#cases-add-attacks)

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/security/case-management
:::

## Set an alert closing reason when closing a case [cases-set-closing-reason]
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

If **Sync detections** is on (**Sync alerts** in earlier versions), closing the case opens the **Select detection close reason** popup (**Select alert close reason** in earlier versions), where you can choose how attached detection alerts are closed. You can close the attached alerts without a reason, or specify an alert closing reason. 

The available options match the [closing reasons from the **Alerts** page](/solutions/security/detect-and-alert/manage-detection-alerts.md#closing-reasons), including any custom closing reasons defined in the `securitySolution:detectionsCloseReasons` [advanced setting](kibana://reference/advanced-settings.md#kibana-siem-settings).

Alerts that are already closed keep their existing reason; only open and acknowledged attached alerts are updated.

## View case metrics [cases-view-metrics]

Select an existing case to access its summary. The case summary, located under the case title, contains metrics that summarize alert information and response times:

* **Total alerts**: Total number of unique alerts attached to the case
* **Associated users**: Total number of unique users represented in the attached alerts
* **Associated hosts**: Total number of unique hosts represented in the attached alerts
* **Total connectors**: Total number of connectors added to the case
* **Case created**: Date and time the case was created
* **Open duration**: Time elapsed since the case was created
* **In progress duration**: How long the case has been in the `In progress` state
* **Duration from creation to close**: Time elapsed from case creation to closure

Use these metrics to assess incident scope, track response efficiency, and identify trends across cases for process improvements.

## Add events [cases-add-events]

```{applies_to}
stack: ga 9.2
```

Attach events to cases to document suspicious activity and preserve evidence for your investigation. You can add events from Timeline or from the **Events** tab on the **Hosts**, **Network**, or **Users** pages. This helps you build a chronological record of what happened, share findings with your team, and support post-incident analysis. 

View attached events in the case's **Events** tab, where they're organized from newest to oldest. You can find the **Events** tab in the following places:

- {applies_to}`stack: ga 9.3+`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0-9.2`: Go to the case's details page.

## Add indicators [cases-indicators]

Attach [threat intelligence indicators](/solutions/security/investigate/indicators-of-compromise.md) to cases to document evidence of compromise and connect your investigation to known threats. This helps you correlate alerts with threat actor tactics, track IOCs across related incidents, and build a complete picture of an attack.

## Add Timelines [cases-timeline]

Attach [Timelines](/solutions/security/investigate/timeline.md) to cases to preserve your investigation context and share it with your team. When you attach a Timeline, other analysts can see the exact queries, filters, and events you examined, making it easier to collaborate, hand off investigations, or document your evidence trail.

::::{tip}
To insert a Timeline link in the case description, click the Timeline icon {icon}`timeline`.
::::

### Attach a Timeline as a structured table [cases-timeline-attachment]

```{applies_to}
stack: preview 9.5
serverless:
  security: preview
```

Instead of inserting a link, you can attach a Timeline as a structured, filterable table in its own section on the case's **Attachments** tab. From a Timeline, select **Attach to case** → **Attach to new case** or **Attach to existing case**. You can also attach a Timeline from the case itself: select **Attach** → **Timeline** from the case's **Activity** tab.

## Add entities [cases-add-entities]

```{applies_to}
stack: preview 9.5
serverless:
  security: preview
```

Attach a host, user, or service entity to a case to connect it to what's under investigation. From an entity's details flyout, select **Take action** → **Add to new case** or **Add to existing case**.

Attached entities appear in their own **Entities** section on the case's **Attachments** tab. To access this section, you need the `read` privilege for the `.entities.v2.latest.security_*` index.

## Add attacks [cases-add-attacks]

```{applies_to}
stack: ga 9.6+
serverless:
  security: ga
```

Attach an attack to a case to keep the finding, its summary, and the alerts it correlates together. Your team sees why those alerts belong together without rebuilding the investigation. You can attach both scheduled and manually generated attacks.

### Attach an attack [cases-attach-attack]

1. Do one of the following.
   * On the [**Attacks** page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md), select **Take actions** on the attack's row.
   * In the attack details flyout, select **Take action**.
2. Select **Add to case**.
3. Select an existing case, or select **Create case** to open a new case.

Kibana attaches the attack and its alerts in one step. The attack appears as a card in the case's **Activity** tab, and its alerts appear in the **Alerts** section of the **Attachments** tab. A case holds up to 1,000 alerts. If attaching the attack's alerts would exceed that limit, Kibana attaches as many as fit and shows a warning.

To attach attacks, you need the **Create comments & attachments** privilege for **Cases**, and access to the attack. Refer to [Control access to cases](/explore-analyze/cases/control-case-access.md#cases-sub-feature-privileges).

### Review attacks in a case [cases-review-attacks]

The attack card in the **Activity** tab shows the attack's title, when it was detected, its alert count, its summary, and its **Details** and **Attack Chain**. The card keeps the attack as it was when you attached it, so it doesn't change if the attack is updated later. Select **Show attack details** to open the attack's flyout.

To work with all of a case's attacks together, open the **Attachments** tab and expand **Attacks**. The table shows **Detected on**, **Title**, **Alerts**, and **Summary** by default. Use the column picker to add **Risk score**, **Status**, **Attached by**, and **Attached at**. Kibana remembers your column selection.

For each attack, you can open the flyout, select **Investigate in Timeline**, or open **More attack actions** to change its status, assign it, apply tags, run a workflow, or add it to another case. To act on several attacks, select their rows, then open the bulk actions menu.

The table shows each attack's current state. If Kibana can't load an attack, for example because it was deleted or you don't have access to it, the row shows the details captured when you attached it, and **Remove from case** is the only action available.

### Remove an attack from a case [cases-remove-attack]

When you remove an attack, you can also remove the alerts it added to the case. In the **Attacks** section of the **Attachments** tab, select **Remove from case** for one attack, or select several attacks and select **Remove from case** from the bulk actions menu. In the dialog, select **Remove attack and alerts** or **Remove attack only**. You can also remove an attack from its card in the **Activity** tab by opening the card's menu and selecting **Delete attachment**.

**Remove attack and alerts** removes only the alerts that the attack added. Kibana keeps an alert in any of these cases.

* You also attached the alert to the case yourself.
* Another attack on the case still includes the alert.
* The attack no longer includes the alert.
* Kibana can't read an attack it needs to check, for example because the attack was deleted.

Removing an attack with the Cases API, an agent, or a workflow also removes its alerts by default.

### Case status and attacks [cases-attack-status-sync]

When **Sync detections** is on, changing the case status also changes the status of its attached attacks, the same way it changes attached alerts. An open case sets attacks to **Open**, an in-progress case sets them to **Acknowledged**, and a closed case sets them to **Closed**. **Sync detections** is on by default for {{elastic-sec}} cases.

## Automate case workflows [cases-automate]

Use [Elastic Workflows](/explore-analyze/workflows.md) to create, update, and close cases programmatically as part of a larger SOC automation. The [Triage a security alert into a case](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-triage-with-case.md) workflow shows the end-to-end pattern: open a case when a detection alert fires, attach the alert and observables, isolate the host, and notify the on-call analyst. For the full `cases.*` step reference, refer to [Cases action steps](/explore-analyze/workflows/steps/cases.md).

Detection rules can also create cases directly, without a workflow, using the [Cases connector](kibana://reference/connectors-kibana/cases-action-type.md) rule action.