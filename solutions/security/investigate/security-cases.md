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
* {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` [Attach attacks from Attack Discovery](#cases-add-attacks)

:::{agent-skill}
:url: https://github.com/elastic/agent-skills/tree/main/skills/security/case-management
:::

## Set an alert closing reason when closing a case [cases-set-closing-reason]
```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

If **Sync detections** or **Sync alerts** (depending on your {{stack}} version) is on, closing the case prompts you to select how to close its attached detection alerts. You can close them without a reason, or select a closing reason.

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

Attached entities appear in their own **Entities** section on the case's **Attachments** tab. To access this section, you need the `read` privilege for the `.entities.v2.latest.*` index pattern.

## Add attacks [cases-add-attacks]

```{applies_to}
serverless:
  security: ga
stack: ga 9.6+
```

Attach an attack to a case so your team can review the finding and the alerts it correlates in one place.

To add attacks to a case:

1. On the [Attacks page](/solutions/security/ai/attack-discovery/manage-discoveries-from-attacks-page.md), select **Take actions** on the attack's row. In the attack details flyout, select **Take action**.
2. Select **Add to case**.
3. Select an existing case, or create a new one.

{{kib}} attaches the attack and its alerts together. If **Sync detections** is on, attack statuses update when the case status changes.

When you [remove an attack](/explore-analyze/cases/attach-objects-to-cases.md#cases-remove-attachments), you can also remove its alerts. Alerts that you added separately stay on the case.

## Automate case workflows [cases-automate]

Use [Elastic Workflows](/explore-analyze/workflows.md) to create, update, and close cases programmatically as part of a larger SOC automation. The [Triage a security alert into a case](/explore-analyze/workflows/use-cases/security/automate-security-operations/alert-triage-with-case.md) workflow shows the end-to-end pattern: open a case when a detection alert fires, attach the alert and observables, isolate the host, and notify the on-call analyst. For the full `cases.*` step reference, refer to [Cases action steps](/explore-analyze/workflows/steps/cases.md).

Detection rules can also create cases directly, without a workflow, using the [Cases connector](kibana://reference/connectors-kibana/cases-action-type.md) rule action.