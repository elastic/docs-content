---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-events.html
applies:
  hosted: all
---

# AutoOps events [ec-autoops-events]

An AutoOps event provides a detailed analysis of a specific issue, including why it was triggered and the steps needed to resolve it. The following sections provide you with comprehensive insights and context around issues, the reasons why the event was created, as well as the affected nodes and indices with high indexing activity.

:::{image} ../../../images/cloud-autoops-events.png
:alt: AutoOps events
:::


## What was detected [ec-autoops-what-was-detected]

This section describes the reasons for which the event was created, as well as links to drill down into the issue.


## Recommendations [ec-autoops-recommendations]

AutoOps provides a set of recommendations. The sequence of their appearance indicates the suggested order of steps to address the issue.


## Event duration [ec-autoops-event-duration]

The time the event was detected (opened at) and the time AutoOps identified that the issue no longer exists (closed at). The closing of an event does not necessarily indicate that the customer resolved the issue, but rather that AutoOps no longer detects it.


## Background and impact [ec-autoops-background-impact]

Provides background and context as to why an event is important, and the impact it can have on performance and stability.


## Event timeline chart [ec-autoops-event-timeline]

This chart visually represents metrics related to an issue. It appears only for events with dynamic metrics. For example, load issues will have this section, while settings-related issues will not. The event timeline chart displays just the last 15 minutes.


## Event severity [ec-autoops-event-severity]

Events are categorized into three levels of severity - high, medium, and low - based on their potential impact on cluster performance and stability:

* **High**: Events can immediately cause significant usability, performance and stability problems.
* **Medium**: Events may lead to severe problems if not addressed.
* **Low**: Events have minimal/not urgent impact.


## Event settings [ec-autoops-event-customize]

AutoOps events are set to `open` and `close` based on triggering mechanisms that have default settings for each event type. You can modify the default settings through the Customize option in the event settings. Be cautious while changing these settings, to avoid situations where alerts fail to trigger.


## Notifications [ec-autoops-notifications]

AutoOps can send notifications to a variety of operation management tools like PagerDuty, Opsgenie, Slack, Teams and custom webhooks. Refer to [Notifications settings](ec-autoops-notifications-settings.md) for more details.


## Sharing events with others [ec-autoops-event-sharing]

You can easily share event information with other users by sending them a direct link to the AutoOps event using the share event link located at the top right of the event window.

Only users with access to the AutoOps deployment from which the link was copied can view the event details.

