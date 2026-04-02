---
navigation_title: Network Firewall logs
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-aws-firewall-firehose.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---



# Monitor AWS Network Firewall logs [monitor-aws-firewall-firehose]


In this section, you’ll learn how to send AWS Network Firewall log events from AWS to your Elastic stack using Amazon Data Firehose.

You will go through the following steps:

* Select a AWS Network Firewall-compatible resource
* Create a delivery stream in Amazon Data Firehose
* Set up logging to forward the logs to the Elastic stack using a Firehose stream
* Visualize your logs in {{kib}}


## Before you begin [firehose-firewall-prerequisites]

We assume that you already have:

* An AWS account with permissions to pull the necessary data from AWS.
* An [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) deployment. The deployment includes an {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data. AWS Data Firehose works with Elastic Stack version 7.17 or greater, running on Elastic Cloud only.

::::{important}
AWS PrivateLink is not supported. Make sure the deployment is on AWS, because the Amazon Data Firehose delivery stream connects specifically to an endpoint that needs to be on AWS.
::::



## Step 1: Install AWS integration in {{kib}} [firehose-firewall-step-one]

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Browse the catalog to find the AWS integration.
3. Navigate to the **Settings** tab and click **Install AWS assets**.


## Step 2: Select a resource [firehose-firewall-step-two]

:::{image} /solutions/images/observability-firehose-networkfirewall-firewall.png
:alt: AWS Network Firewall
:::

You can either use an existing AWS Network Firewall, or create a new one for testing purposes.

Creating a Network Firewall is not trivial and is beyond the scope of this guide. For more information, check the AWS documentation on the [Getting started with AWS Network Firewall](https://docs.aws.amazon.com/network-firewall/latest/developerguide/getting-started.html) guide.


## Step 3: Create a stream in Amazon Data Firehose [firehose-firewall-step-three]

:::{image} /solutions/images/observability-firehose-networkfirewall-stream.png
:alt: Firehose stream
:::

1. Go to the [AWS console](https://console.aws.amazon.com/) and navigate to Amazon Data Firehose.
2. Click **Create Firehose stream** and choose the source and destination of your Firehose stream. Set source to `Direct PUT` and destination to `Elastic`.
3. Collect {{es}} endpoint and API key from your deployment on Elastic Cloud.

    * **To find the Elasticsearch endpoint URL**:

        1. Go to the [Elastic Cloud](https://cloud.elastic.co/) console
        2. Find your deployment in the **Hosted deployments** card and select **Manage**.
        3. Under **Applications** click **Copy endpoint** next to **Elasticsearch**.
        4. Make sure the endpoint is in the following format: `https://<deployment_name>.es.<region>.<csp>.elastic-cloud.com`.

    * **To create the API key**:

        1. Go to the [Elastic Cloud](https://cloud.elastic.co/) console
        2. Select **Open Kibana**.
        3. Open the **API keys** management page in the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create API key**. If you are using an API key with **Restrict privileges**, make sure to review the Indices privileges to provide at least `auto_configure` and `write` permissions for the indices you will be using with this delivery stream.

4. Set up the delivery stream by specifying the following data:

    * Elastic endpoint URL: The URL that you copied in the previous step.
    * API key: The API key that you created in the previous step.
    * Content encoding: To reduce the data transfer costs, use GZIP encoding.
    * Retry duration: A duration between 60 and 300 seconds should be suitable for most use cases.
    * Backup settings: It is recommended to configure S3 backup for failed records. These backups can then be used to restore failed data ingestion caused by unforeseen service outages.


The Firehose stream is ready to send logs to our Elastic Cloud deployment.


## Step 4: Enable logging [firehose-firewall-step-four]

:::{image} /solutions/images/observability-firehose-networkfirewall-logging.png
:alt: AWS Network Firewall logging
:::

The AWS Network Firewall logs have built-in logging support. It can send logs to Amazon S3, Amazon CloudWatch, and Amazon Kinesis Data Firehose.

To enable logging to Amazon Data Firehose:

1. In the AWS console, navigate to the AWS Network Firewall service.
2. Select the firewall for which you want to enable logging.
3. In the **Logging** section, click **Edit**.
4. Select the **Send logs to** option and choose **Kinesis Data Firehose**.
5. Select the Firehose stream you created in the previous step.
6. Click **Save**.

At this point, the Network Firewall will start sending logs to the Firehose stream.


## Step 5: Visualize your Network Firewall logs in {{kib}} [firehose-firewall-step-five]

:::{image} /solutions/images/observability-firehose-networkfirewall-data-stream.png
:alt: Firehose monitor Network Firewall logs
:::

With the new logging settings in place, the Network Firewall starts sending log events to the Firehose stream.

Navigate to {{kib}} and choose **Visualize your logs with Discover**.

:::{image} /solutions/images/observability-firehose-networkfirewall-discover.png
:alt: Visualize Network Firewall logs with Discover
:screenshot:
:::
