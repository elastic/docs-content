---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-service-status.html
  - https://www.elastic.co/guide/en/cloud/current/ec_subscribe_to_individual_regionscomponents.html
  - https://www.elastic.co/guide/en/cloud/current/ec_service_status_api.html
  - https://www.elastic.co/guide/en/serverless/current/general-serverless-status.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/ech-service-status.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/echservice_status_api.html
  - https://www.elastic.co/guide/en/cloud-heroku/current/echsubscribe_to_individual_regionscomponents.html
applies_to:
  deployment:
    ess: all
  serverless: all
---

# Service status

{{ech}} deployments and Serverless projects run on different cloud platforms, such as Amazon Web Services (AWS),  Google Cloud Platform (GCP), and Microsoft Azure. Like any service, it might undergo availability changes from time to time. When availability changes, Elastic makes sure to provide you with a current service status.

To check current and past service availability, go to to the [Cloud Status](https://cloud-status.elastic.co/) page. Services are separated into {{ech}} services and [Serverless services](https://status.elastic.co/?section=serverless).

## Subscribe to updates [ec_subscribe_to_updates]

Don’t want to check the service status page manually? You can get notified about changes to the service status automatically.

To receive service status updates:

1. Go to the [Cloud Status](https://cloud-status.elastic.co/) page and select **SUBSCRIBE TO UPDATES**.
2. Select one of the following methods to be notified of status updates:

    * Email
    * Twitter
    * Atom and RSS feeds

After you subscribe to updates, you are notified whenever a service status update is posted.

## Subscribe to individual regions or components

If you want to know about specific status updates, rather than all of them, you can adjust your preferences by using the following steps. These steps apply to both new signups and adjustments to an existing subscription.

Go to the [Cloud Status](https://cloud-status.elastic.co/) page and select **SUBSCRIBE TO UPDATES**. Enter your email address and click **SUBSCRIBE VIA EMAIL**. You will be brought to a page with a list of regions and components.

Here, you can customize your selections as needed, and then click **Save**.

## Service Status API [ec_service_status_api]

If you want a programmatic method of ingesting our service status updates, then you can consume updates using the Service Status API.

For more information and to get started, go to our [Service Status API](https://status.elastic.co/api/) page.

