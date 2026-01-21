---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-autoops-notifications-settings.html
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

1. On the **Notifications Settings** page, navigate to the **Connector Settings** tab and click **Add**.
2. From the drop-down list, choose the connector you want to set up and follow the instructions.
3. Click **Validate** to send a test message.
4. Save your settings.


## Add notification filters [ec-add-notification-filters]

A notification filter lets you choose which events to receive notifications for and how you want to be notified. You can create an unlimited number of filters, and the same connector can be used across multiple filters.

To set up a filter, follow these steps:

1. On the **Notification settings** page, navigate to the **Filter Setting** tab and click **Add**.
2. Choose a name that best describes the type of alert notification. This name will appear in other reports and dashboards.
3. Select the deployments that the new created events will trigger the alert for.
4. Select the connectors to receive the notification.
5. Use the **Delay** field to set the period of time AutoOps will hold before sending the notification. If during this time all of the events listed in this filter are closed by AutoOps, no notification will be sent.
6. Choose the type of events this filter applies to.


## Built-in connectors [ec-built-in-connectors]

The following connectors are available with AutoOps:

* [Email](#email)
* [PagerDuty](#ec-autoops-pagerduty)
* [Slack](#ec-autoops-slack)
* [VictorOps](#ec-autoops-victorops)
* [Opsgenie](#ec-autoops-opsgenie)
* [Microsoft Teams Configuration](#ec-autoops-ms-configuration)
* [Webhook](#ec-autoops-webhook)

:::{dropdown} Email
$$$email$$$

To set up notifications via email, follow these steps:

1. Add a new **Email** connector.
2. Add a list of emails.
   You can add up to 40 emails for a single email connector, and opt in to get alerts also when events close.
3. To receive notifications, scroll down the **Notification** page and click **Add**.
4. Fill in the filter details.
5. Select the events that you want to send to this connector.
:::

:::{dropdown} PagerDuty 

$$$ec-autoops-pagerduty$$$

The PagerDuty integration consists of the following parts:

**PagerDuty configuration**

1. Follow the steps described in the [Events Integration Functionality](https://developer.pagerduty.com/docs/8a76ad16d6b52-events-integration-functionality) section.
2. Save the integration URL key as you will need it later.

**AutoOps configuration**

1. Add a new PagerDuty connector using the PagerDuty configuration application key.
2. To receive Slack notifications, add a notification filter. Scroll down the Notification page and click **Add**.
3. Fill in the filter details.
4. Select the events that should be sent to this output.
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

1. Add a new PagerDuty connector using the PagerDuty configuration application key.
2. To receive Slack notifications, add a notification filter. Scroll down the Notification page and click Add.
3. Fill in the filter details.
4. Select the events that should be sent to this output.
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

1. Open AutoOps and go to **User Profile**. Then, select **Notifications**.
2. Click **Add** and select **Opsgenie** from the dropdown list.
3. Name your connector and add Api Key from opsgenie API configuration. Click the validate button to make sure that your notification setting is working. Don’t forget to save your notification connector!
4. To receive notifications on Opsgenie, you need to add a notification filter. Scroll down the **Notification** page and click **Add**.
5. Fill in the filter details.
6. Select events that should be sent to this output.
:::

:::{dropdown} Microsoft Teams 

$$$ec-autoops-ms-configuration$$$

To create an incoming webhook on your Microsoft Teams, follow [these instructions](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook).

Save the URL displayed during the creation of the incoming webhook, as you will use it during the AutoOps configuration.

**AutoOps configuration**

1. Add a new MS team connector using the URL from Microsoft Teams.
2. To receive notifications into Microsoft Teams, you need to add a notification filter. Scroll down the Notification page and click Add.
3. Fill in the filter details.
4. Select events that should be sent to this output.
:::


::::{dropdown} Webhook 

$$$ec-autoops-webhook$$$

A webhook enables an application to provide other applications with real-time information. A webhook is a user-defined HTTP callback (HTTP POST), which is triggered by specific events.

**How to add a webhook notification**

1. Go to **Settings** > **Notifications** > **Connector settings** and click **Add**.
2. Select Webhook from the drop-dowon list and enter the following details:

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

4. Click **Validate** to check your settings, and then click **Save**.
5. Optionally, you can test the webhook integration by using the [webhook.site](https://webhook.site/#!/view/fe9d630e-2f01-44b7-9e41-ef9520fbe9a7).

::::{note}
When the connector settings have been completed, continue to set up the notification filter to define which events you’d like to be notified about.
::::

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

The notification status appears also in the event details window.

:::{image} /deploy-manage/images/cloud-autoops-notification-status.png
:alt: Notification status
:::
