---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-notifications-settings.html
applies_to:
  stack:
products:
  - id: cloud-hosted
  - id: cloud-kubernetes
  - id: cloud-enterprise
---

# Notifications Settings [ec-autoops-notifications-settings]

AutoOps can notify you of new events opened or closed through various methods and operation management tools. With a customizable mechanism, you can specify which events you want to be notified about, how you wish to receive these notifications, and their frequency.

::::{note}
Only **Organization owners** can configure these settings.
::::


To set up notifications you have to:

1. Set up connectors to specify where the notifications will be sent.
2. Add notification filters to determine which events will be sent to each connector.


## AutoOps connectors [ec-autoops-connectors]

To receive notifications for new events, the first step is to specify where the notifications should be sent. AutoOps provides a selection of [built-in connectors](#ec-built-in-connectors) to choose from. You can set up multiple connectors, even of the same type, based on your needs.


## Set up a connector [ec-setup-autoops-connectors]

1. On the **Notifications Settings** page, navigate to the **Connector settings** tab and click **Add connector**.
2. Select a connector type and fill in the required fields.
3. Click **Run to test** to send a test notification.
4. Save your settings.


## Add notification filters [ec-add-notification-filters]

A notification filter lets you choose which events to receive notifications for and how you want to be notified. You can create an unlimited number of filters, and the same connector can be used across multiple filters.

To set up a filter, follow these steps:

1. On the **Notification settings** page, navigate to the **Filter setting** tab and click **Add filter**.
2. Choose a name that best describes the type of alert notification. This name will appear in other reports and dashboards.
3. Select the deployments for which this filter should trigger notifications.
4. Select the connectors to receive the notification.
5. Use the **Delay** field to set the period of time you want AutoOps to wait before sending the notification. If all the events listed in this filter are closed by AutoOps in this time, no notification will be sent.
6. Choose the type of events this filter applies to.


## Built-in connectors [ec-built-in-connectors]

The following connectors are available with AutoOps:

:::{dropdown} Email
$$$email$$$

To set up notifications through email:

1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and choose **Email** as your connector type.
2. Add a list of recipients.
   You can add up to 40 emails for a single email connector, and opt in to get alerts also when events close.
3. Add a [notification filter](#ec-add-notification-filters) for this connector.
:::

:::{dropdown} PagerDuty 

$$$ec-autoops-pagerduty$$$

The PagerDuty integration consists of the following parts:

**PagerDuty configuration**

1. Follow the steps described in the [Events Integration Functionality](https://developer.pagerduty.com/docs/8a76ad16d6b52-events-integration-functionality) section.
2. Save the integration URL key as you will need it later.

**AutoOps configuration**

1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and choose **PagerDuty** as your connector type.
2. Add a [notification filter](#ec-add-notification-filters) for this connector.
:::


:::{dropdown} Slack

$$$ec-autoops-slack$$$

To set up a webhook to send AutoOps notifications to a Slack channel, go through the following steps.

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click **Create new App**.
3. Select **From Scratch**.
4. Choose a name for your webhook and the workspace to create the app. Click **Create App**.
5. From the left menu, select **Incoming Webhooks**.
6. Toggle the **Activate Incoming Webhooks** to On.
7. Click **Request to Add New Webhook**.
8. Select a Slack channel from the list to receive the notifications and click **Allow**.
9. Copy the webhook URL to set up the webhook notification connector in AutoOps.
10. Add the webhook URL when creating the connector.

:::


:::{dropdown} VictorOps 

$$$ec-autoops-victorops$$$

The VictorOps integration consists of the following parts:

**VictorOps configuration**

1. Follow the steps described in the [REST Endpoint Integration Guide](https://help.victorops.com/knowledge-base/rest-endpoint-integration-guide/).
2. Save the integration URL key as you will need it later.

**AutoOps configuration**

1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and choose **VictorOps** as your connector type.
2. Add a [notification filter](#ec-add-notification-filters) for this connector.
:::


:::{dropdown} Opsgenie 

$$$ec-autoops-opsgenie$$$

The Opsgenie integration consists of the following parts:

**Opsgenie configuration**

1. Open the main page of your Opsgenie account and click the **Teams** tab (a team must be defined).
2. Go to the **Settings** tab of your Opsgenie page, and select Integrations.
3. Select your **Team** and click **Integrations** from the left menu.
4. Click **Add Integration**. On the **Integration List**, search for API.
5. Name your integration and click **Save**.

**AutoOps configuration**

1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and choose **Opsgenie** as your connector type.
2. Add a [notification filter](#ec-add-notification-filters) for this connector.
:::

:::{dropdown} Microsoft Teams 

$$$ec-autoops-ms-configuration$$$

To create an incoming webhook on your Microsoft Teams, follow [these instructions](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook).

Save the URL displayed during the creation of the incoming webhook, as you will use it during the AutoOps configuration.

**AutoOps configuration**

1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and choose **Microsoft Teams** as your connector type.
2. Add a [notification filter](#ec-add-notification-filters) for this connector.
:::


:::{dropdown} Webhook 

$$$ec-autoops-webhook$$$

A webhook enables an application to provide other applications with real-time information. A webhook is a user-defined HTTP callback (HTTP POST), which is triggered by specific events.

**How to add a webhook notification**

1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and choose **Webhook** as your connector type.
2. Complete the fields as follows:

    * **Name**: It must be a unique name for this webhook.
    * **URL**: This is the endpoint to which HTTP POST requests will be sent when events occur.
    * **Method**: POST
    * **Header**: Content-Type, application/Json

3. Review and update the message as it appears in the body section. AutoOps provides a set of optional fields to use in the message. Read your application documentation for the expected message schema.

    * `RESOURCE_ID`: Customer Deployment ID
    * `RESOURCE_NAME`: Customer Deployment name
    * `TITLE`: The title of the event.
    * `DESCRIPTION`: The description of the issue that was found.
    * `SEVERITY`: One of the 3 severity levels (High, Medium and Low).
    * `STATUS`: Indicate if the event is currently open or close.
    * `MESSAGE`: The background and impact of the issue
    * `START_TIME`: The time the event was open.
    * `END_TIME`: The time the event was closed.
    * `ENDPOINT_TYPE`: The type of the endpoint (Slack, PagerDuty, Webhook, Opsgenie, VictorOps and MS Teams).
    * `AFFECTED_NODES`: List of node names.
    * `AFFECTED_INDICES`: List of indices names.
    * `EVENT_LINK`: Direct link to the event in AutoOps.

4. Click **Run to test** to check your settings, and then click **Save**.
5. Optionally, you can test the webhook integration by using the [webhook.site](https://webhook.site/#!/view/fe9d630e-2f01-44b7-9e41-ef9520fbe9a7).
6. Add a [notification filter](#ec-add-notification-filters) for this connector.
:::

## Notifications report [ec-notification-report]

From the **Notifications** report, you can check all the notifications sent. The report lists all the events that were set up in the notification filters and provide their status.

:::{image} /deploy-manage/images/cloud-autoops-notifications-report.png
:alt: The Notifications report
:::

The notification can have one of the following statuses:

* Notification sent
* Connector not defined
* Notification muted
* Sending notification
* Notification failed to send
* Event closed before notification sent

The notification status for each event is also shown in the flyout when you select an event on the **Deployment** or **Cluster** page.

:::{image} /deploy-manage/images/cloud-autoops-notification-status.png
:alt: Notification status in an event flyout
:::
