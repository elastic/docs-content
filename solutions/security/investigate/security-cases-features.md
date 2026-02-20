---
navigation_title: Security case features
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/cases-open-manage.html
  - https://www.elastic.co/guide/en/serverless/current/security-cases-open-manage.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
---

# Security case features [security-cases-features]

{{elastic-sec}} includes additional case features beyond the core functionality. For general case management, refer to [](/explore-analyze/cases/manage-cases.md).

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

## Add observables [add-case-observables]

Observables are discrete pieces of data relevant to an investigation—such as IP addresses, file hashes, domain names, or URLs. By attaching observables to cases, you can spot patterns across incidents or events. For example, if the same malicious IP appears in multiple cases, you may be dealing with a coordinated attack or shared threat infrastructure. This correlation helps you assess the true scope of an incident and prioritize your response.

From the **Observables** tab, you can view and manage case observables:

- {applies_to}`stack: ga 9.3`: Go to the case's details page, then select the **Attachments** tab.
- {applies_to}`stack: ga 9.0-9.2`: Go to the case's details page.  

You can manually add observables to cases, or {applies_to}`stack: ga 9.2` with the appropriate subscription, auto-extract them from alerts. Each case supports up to 50 observables.

To manually add an observable:

1. Select **Add observable** from the **Observables** tab.
2. Provide the necessary details:

    * **Type**: Select a type for the observable. You can choose a preset type or a [custom one](/explore-analyze/cases/configure-case-settings.md#cases-observable-types).
    * **Value**: Enter a value for the observable. The value must align with the type you select.
    * **Description** (Optional): Provide additional information about the observable.

3. Select **Add observable**.

After adding an observable to a case, you can remove or edit it using the action menu {icon}`boxes_horizontal`. To find related investigations, check the **Similar cases** tab for other cases that share the same observables.

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

Attach [Timelines](/solutions/security/investigate/timeline.md) to cases to preserve your investigation context and share it with your team. When you link a Timeline, other analysts can see the exact queries, filters, and events you examined, making it easier to collaborate, hand off investigations, or document your evidence trail.

::::{tip}
To insert a Timeline link in the case description, click the Timeline icon (![Timeline icon](/solutions/images/security-add-timeline-button.png "title =20x20")).
::::