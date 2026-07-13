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

# Notification settings [ec-autoops-notifications-settings]

AutoOps can notify you of new events opened or closed through various connectors. You can specify which events you want to be notified about, as well as how and when you want to receive these notifications.

::::{note}
Only **Organization owners** can configure these settings.
::::

## Set up notifications for AutoOps events

To set up notifications for specific events in AutoOps, you have to:

1. [Add connectors](#ec-setup-autoops-connectors) to specify where the notifications will be sent.
2. [Add notification filters](#ec-add-notification-filters) to determine which notifications will be sent to each connector and when.

### Add connectors [ec-setup-autoops-connectors]

To receive notifications for new events, the first step is to specify where the notifications should be sent. AutoOps provides a selection of [built-in connectors](#ec-built-in-connectors) to choose from. You can set up multiple connectors of the same type or of different types based on your needs.

To add a connector, follow these steps:

1. On the **Notifications settings** page, navigate to the **Connector settings** tab and click **Add connector**.
2. Select a connector type and fill in the required fields. Refer to [Configure connectors](#ec-built-in-connectors) for specific instructions for each connector.
3. Click **Run to test** to send a test notification.
4. Save your settings.

#### Configure connectors [ec-built-in-connectors]

The following connectors are available with AutoOps. Expand each section for specific configuration instructions.

:::{dropdown} Email
:name: email

To set up notifications through email, follow these steps:

1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and select **Email** as your connector type.
2. Add a list of recipients.
   You can add up to 40 emails for a single email connector, and opt in to also notify the recipients when events close.
3. Add a [notification filter](#ec-add-notification-filters) for this connector.
:::

:::{dropdown} PagerDuty
:name: ec-autoops-pagerduty

To set up this integration, you need to perform configurations in PagerDuty and AutoOps.

**PagerDuty configuration**
1. Follow PagerDuty's instructions to [create a generic events API integration](https://support.pagerduty.com/main/docs/services-and-integrations#create-a-generic-events-api-integration).
2. Store the integration key securely. You will need it when configuring the connector in AutoOps.

**AutoOps configuration**
1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and select **PagerDuty** as your connector type.
2. In the **Key** field, paste the integration key you copied during the PagerDuty configuration.
3. Add a [notification filter](#ec-add-notification-filters) for this connector.
:::


:::{dropdown} Slack
:name: ec-autoops-slack

To set up this integration, you need to perform configurations in Slack and AutoOps.

**Slack configuration**

1. Follow Slack's instructions to [get started with incoming webhooks](https://docs.slack.dev/messaging/sending-messages-using-incoming-webhooks/#getting_started).
2. Store the webhook URL displayed during the creation securely. You will need it when configuring the connector in AutoOps.

**AutoOps configuration**
1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and select **Slack** as your connector type.
2. In the **URL** field, paste the URL you copied during the Slack configuration.
3. Add a [notification filter](#ec-add-notification-filters) for this connector.

:::


:::{dropdown} VictorOps
:name: ec-autoops-victorops

AutoOps integrates with VictorOps/Splunk On-Call using the [REST Endpoint integration](https://help.splunk.com/en/splunk-enterprise/alert-and-respond/splunk-on-call/integrations-with-splunk-on-call/rest-endpoint-integration-for-splunk-on-call).

To set up this integration, you need to perform configurations in VictorOps/Splunk On-Call and AutoOps.

**VictorOps/Splunk On-Call configuration**

1. In Splunk On-Call, open **Integrations** > **3rd Party Integrations** > **REST - Generic** and enable it.
2. Copy the REST Endpoint URL.
3. Replace `$routing_key` at the end of the URL with your routing key (for example `elastic`).
4. Store the modified URL securely. You will need it when configuring the connector in AutoOps.
5. Configure routing keys under **Settings** > **Keys** so notifications reach the right team.

**AutoOps configuration**

1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and select **VictorOps** as your connector type.
2. In the **URL** field, paste the URL you copied during the Splunk On-Call configuration.
3. Add a [notification filter](#ec-add-notification-filters) for this connector.

:::


:::{dropdown} Opsgenie
:name: ec-autoops-opsgenie

To set up this integration, you need to perform configurations in Opsgenie and AutoOps.

**Opsgenie configuration**

1. Open the main page of your Opsgenie account and click the **Teams** tab. Make sure a team is defined.
2. Go to **Settings** > **Integrations**.
3. Click **Add Integration**. In the **Integration List**, search for **API**.
4. Complete the fields and save your changes.
5. Copy the API key and store it securely. You will need it when configuring the connector in AutoOps.

**AutoOps configuration**

1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and select **Opsgenie** as your connector type.
2. In the **API key** field, paste the API key you copied during the Opsgenie configuration.
3. Add a [notification filter](#ec-add-notification-filters) for this connector.
:::

:::{dropdown} Microsoft Teams
:name: ec-autoops-ms-configuration

To set up this integration, you need to perform configurations in Microsoft Teams and AutoOps.

**Microsoft Teams configuration**

1. Follow Microsoft Teams' instructions to [create incoming webhooks](https://docs.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook).
2. Store the URL displayed during the creation securely. You will need it when configuring the connector in AutoOps.

**AutoOps configuration**

1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and select **Microsoft Teams** as your connector type.
2. In the **URL** field, paste the URL you copied during the Microsoft Teams configuration.
3. Add a [notification filter](#ec-add-notification-filters) for this connector.
:::


:::{dropdown} Webhook
:name: ec-autoops-webhook

To set up notifications through a custom webhook, follow these steps:

1. Follow the instructions to [set up a connector](#ec-setup-autoops-connectors) and select **Webhook** as your connector type.
2. Complete the fields as follows:
    * **Name**: Enter a unique name for this webhook.
    * **URL**: Enter the endpoint to which HTTP requests will be sent when events occur.
    * **Method**: Select a method. `POST` is selected by default.
    * **Header**: Add a key and value. `Content-Type` and `application/json` are added by default.
3. In the **Body** section, edit the message according to how you want it to appear in notifications. Refer to your application documentation for the expected message schema. AutoOps provides a set of optional fields to use. 

    * `RESOURCE_ID`: Customer deployment ID
    * `RESOURCE_NAME`: Customer deployment name
    * `TITLE`: The title of the event.
    * `DESCRIPTION`: The description of the issue that was found.
    * `SEVERITY`: One of the three severity levels (High, Medium, Low).
    * `STATUS`: Indicates if the event is currently open or closed.
    * `MESSAGE`: The background and impact of the issue.
    * `START_TIME`: The time the event was opened.
    * `END_TIME`: The time the event was closed.
    * `ENDPOINT_TYPE`: The type of endpoint (PagerDuty, Slack, VictorOps, Opsgenie, or Microsoft Teams).
    * `AFFECTED_NODES`: List of affected nodes.
    * `AFFECTED_INDICES`: List of affected indices.
    * `EVENT_LINK`: Direct link to the event in AutoOps.
4. Optionally, test the webhook integration by using a tool like [webhook.site](https://webhook.site/#!/view/fe9d630e-2f01-44b7-9e41-ef9520fbe9a7).
5. Add a [notification filter](#ec-add-notification-filters) for this connector.

:::

### Add notification filters [ec-add-notification-filters]

After adding a connector, add a notification filter to specify which events to receive notifications for and how you want to be notified. You can create an unlimited number of filters, and the same connector can be used across multiple filters.

To add a filter, follow these steps:

1. On the **Notifications settings** page, navigate to the **Filter settings** tab and click **Add filter**.
2. Enter a name that best describes the type of notification. This name will appear in other reports and dashboards.
3. Select the connectors to receive the notification. 
4. Select the deployments for which this filter should trigger notifications.
5. Use the **Delay** field to set the period of time you want AutoOps to wait before sending the notification. If all the events listed in this filter are closed by AutoOps in this time, no notification will be sent.
6. Use the **Included Events** and **Excluded Events** fields to select which events should trigger or not trigger this notification.
7. Save your settings.

## Notifications report [ec-notification-report]

From the **Notifications** report, you can review all of the notifications that have been sent by AutoOps. The report lists all the events that were set up in the notification filters and their status.

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
