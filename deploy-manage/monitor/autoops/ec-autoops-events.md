---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-events.html
applies_to:
  deployment:
    ess: all
products:
  - id: cloud-hosted
navigation_title: Events
---

# AutoOps events [ec-autoops-events]

AutoOps continuously monitors your {{es}} deployments by sampling performance and health metrics at a 10-second interval. This high-frequency data collection allows for rapid detection and diagnosis of potential issues so you can get timely notifications and resolve issues faster. 

When AutoOps detects an issue, it creates an event. Events provide detailed analyses of detected issues, including why they were triggered and the steps needed to resolve them. 

## Event insights

You can view events on the **Deployment** page in the **Open Events** and **Events History** sections.

When you select an event, a flyout appears with insights and context around the detected issue.

:::{image} /deploy-manage/images/cloud-autoops-events.png
:alt: AutoOps events
:::

The following table describes the different sections in this flyout:

| Section | Description |
| --- | --- |
| What was detected | Describes why the event was created and provides links to drill down into the detected issue. |
| Recommendations | Lists recommendations to address the issue and improve your cluster's overall performance. The recommendations are organized according to the suggested order of execution. |
| Event duration | Shows the time the event was created when AutoOps detected the issue, and if applicable, the time the event was closed when AutoOps identified that the issue no longer exists. The closing of an event doesn't necessarily mean that the issue is resolved, just that AutoOps no longer detects it. |
| Background and impact | Provides background and context about why the event is important and the impact it can have on cluster performance and stability. |
| Event timeline chart | Visually presents metrics related to the issue in the last 15 minutes. This chart appears only for events with dynamic metrics. For example, load issues will have this section, but settings-related issues will not. |
| Event severity | Categorizes the event into one of three severity levels based on its potential impact on the cluster: <br><br> **High**: Event can immediately cause significant usability, performance, and stability problems.<br> **Medium**: Event may lead to significant problems if not addressed.<br> **Low**: Event has minimal impact and is not urgent. |

## Event actions

In the event flyout, select the actions menu to perform the following actions. 

### Change event settings [ec-autoops-event-customize]

AutoOps events are opened and closed based on triggering mechanisms that have default settings for each event type. To change these settings, select **Customize** from the actions menu.

When changing these settings, avoid making changes that will cause alert triggers to fail.

### Configure notifications [ec-autoops-notifications]

AutoOps can send event notifications to many operation management tools like PagerDuty, Opsgenie, Slack, Teams, custom webhooks, and more. To configure notifications, select **Notifications** from the actions menu. 

Refer to [Notifications settings](ec-autoops-notifications-settings.md) for more details.

### Dismiss event

Some events may not require your attention immediately, or at all. If you have the appropriate permissions, you can dismiss an event to remove all events of its kind from your dashboard and prevent AutoOps from opening other similar events. This action can be reversed using the **Dismiss events** report. To dismiss an event, select **Dismiss** from the actions menu.

### Share event [ec-autoops-event-sharing]

You can share event information with other users by sending them a link to the event in AutoOps. To share the event, select **Share event link** from the actions menu.

:::{note}
Users can only view the event from the shared link if they have access to the AutoOps deployment from which the link was copied.
:::

