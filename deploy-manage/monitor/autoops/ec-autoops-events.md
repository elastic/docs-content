---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-events.html
applies_to:
  deployment:
    ess: all
    self:
    ece:
    eck:
products:
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: cloud-enterprise
navigation_title: Events
---

# AutoOps events [ec-autoops-events]

AutoOps continuously monitors your {{es}} deployments by sampling performance and health metrics at 10-second intervals. This high-frequency data collection allows AutoOps to rapidly detect and diagnose issues so you can get timely notifications and resolve issues faster. 

When AutoOps detects an issue, it creates an event. Events provide detailed analyses of detected issues, including why they were triggered and the steps needed to resolve them. 

## Event insights

You can view events on the **Deployment** page (for {{ECH}} deployments) or the **Cluster** page (for ECE, ECK, and self-managed clusters) in the **Open Events** and **Events History** sections.

When you select an event, a flyout appears with insights and context for the detected issue.

:::{image} /deploy-manage/images/cloud-autoops-events.png
:screenshot:
:alt: Screenshot showing an AutoOps event flyout
:::

The following table describes the sections in this flyout:

| Section | Description |
| --- | --- |
| What was detected | Describes why the event was created and provides links to drill down into the detected issue. |
| Recommendations | Lists recommendations to address the issue and improve your cluster's overall performance. The recommendations are organized according to the suggested order of execution. |
| Event duration | Shows when the event was opened (when AutoOps detected the issue), and if applicable, when the event was closed (when AutoOps identified that the issue no longer exists). A closed event doesn't necessarily mean that the issue is resolved, just that AutoOps no longer detects it. |
| Background and impact | Provides background and context about why the event is important and its potential impact on cluster performance and stability. |
| Event timeline chart | Visually presents metrics related to the issue in the last 15 minutes. This chart appears only for events with dynamic metrics. For example, load issues will have this section, but settings-related issues will not. |
| Event severity | Categorizes the event into one of three severity levels based on its potential impact on the cluster: <br><br> **High**: Event can immediately cause significant usability, performance, and stability problems.<br> **Medium**: Event may lead to significant problems if not addressed.<br> **Low**: Event has minimal impact and is not urgent. |

## Event actions

In the event flyout, go to the actions menu and select from the following options:

### Customize [ec-autoops-event-customize]

AutoOps events are opened and closed based on triggering mechanisms that have default settings for each event type. Select **Customize** to change these settings. Avoid making changes that will cause alert triggers to fail.

Refer to [](ec-autoops-event-settings.md) for more details.

### Notifications [ec-autoops-notifications]

AutoOps can send event notifications to many operation management tools like PagerDuty, Opsgenie, Slack, Teams, custom webhooks, and more. Select **Notifications** to configure these settings. 

Refer to [](ec-autoops-notifications-settings.md) for more details.

### Dismiss [ec-autoops-dismiss]

Some events may not require your attention immediately, or at all. If you are an Organization owner, you can dismiss an event to remove all events of its kind from your dashboard and prevent AutoOps from opening other similar events. Select **Dismiss** to dismiss an event.

This action can be reversed using the **Dismiss events** report. 

### Share event link [ec-autoops-event-sharing]

You can share event information with other users by sending them a link to the event in AutoOps. Select **Share event link** to share the event.

:::{note}
Users can only view the event from the shared link if they have access to the AutoOps deployment or cluster from which the link was copied.
:::

