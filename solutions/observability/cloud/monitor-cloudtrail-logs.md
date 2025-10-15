---
navigation_title: CloudTrail logs
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-aws-cloudtrail-firehose.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---



# Monitor CloudTrail logs [monitor-aws-cloudtrail-firehose]


In this section, you’ll learn how to monitor and analyze the CloudTrail logs you send to Elastic with Amazon Data Firehose. You will go through the following steps:

* Install AWS integration in {{kib}}
* Export Cloudtrail events to CloudWatch
* Set up a Firehose delivery stream
* Set up a subscription filter to route Cloudtrail events to a delivery stream
* Visualize your CloudTrail logs in {{kib}}


## Before you begin [firehose-cloudtrail-prerequisites]

We assume that you already have:

* An AWS account with permissions to pull the necessary data from AWS.
* An [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) deployment. The deployment includes an {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data. AWS Data Firehose works with Elastic Stack version 7.17 or greater, running on Elastic Cloud only.

::::{important}
Make sure the deployment is on AWS, because the Amazon Data Firehose delivery stream connects specifically to an endpoint that needs to be on AWS.
::::



## Step 1: Install AWS integration in {{kib}} [firehose-cloudtrail-step-one]

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Browse the catalog to find the Amazon Data Firehose integration.
3. Navigate to the **Settings** tab and click **Install Amazon Data Firehose assets**.


## Step 2: Export Cloudtrail events to CloudWatch [firehose-cloudtrail-step-two]

:::{image} /solutions/images/observability-firehose-cloudtrail-cloudwatch.png
:alt: Cloudtrail to CloudWatch
:::

To export CloudTrail logs to CloudWatch, you must set up a **trail** through the following steps:

1. Go to the [AWS console](https://console.aws.amazon.com/) and navigate to CloudTrail.
2. Click **Create trail** and configure the general details on the **Choose trail attributes** panel, like:

    * Trail name
    * Storage location

        By default, CloudTrail exports data to an S3 bucket. It isn’t possible to opt-out from S3.

3. Specify the encryption options.

    When exporting data from CloudTrail to S3, it is recommended to enable **Log file SSE-KMS encryption**. You can use an existing AWS KMS key, or create a new one.

4. Enable **CloudWatch Logs** and confirm the **Log group name**.

    CloudTrail offers the option to send events to CloudWatch as logs. You must enable this option to forward the events to Amazon Data Firehose.

    You also need to create an IAM Role, or select an existing one, to enable CloudTrail to put log events into a CloudWatch stream.

5. From the **Choose log events** panel, select the event types you want to send to Elastic.
6. Review the attributes and log events you have specified in the previous steps and click **Create trail**.
7. Verify everything is working as expected.

    Open the log group you just created on CloudWatch and make sure there are events from the CloudTrail you have just created.

    :::{image} /solutions/images/observability-firehose-verify-events-cloudwatch.png
    :alt: Verify events in CloudWatch
    :::



## Step 3: Set up a Firehose delivery stream [firehose-cloudtrail-step-three]

:::{image} /solutions/images/observability-firehose-delivery-stream.png
:alt: Firehose delivery stream
:::

You now have a CloudWatch log group with events coming from CloudTrail. For more information on how to set up a Amazon Data Firehose delivery stream to send data to Elastic Cloud, you can also check the [setup guide](monitor-amazon-web-services-aws-with-amazon-data-firehose.md).

1. Collect {{es}} endpoint and API key from your deployment on Elastic Cloud.

    * **To find the Elasticsearch endpoint URL**:

        1. Go to the [Elastic Cloud](https://cloud.elastic.co/) console
        2. Find your deployment in the **Hosted deployments** card and select **Manage**.
        3. Under **Applications** click **Copy endpoint** next to **Elasticsearch**.
        4. Make sure the endpoint is in the following format: `https://<deployment_name>.es.<region>.<csp>.elastic-cloud.com`.

    * **To create the API key**:

        1. Go to the [Elastic Cloud](https://cloud.elastic.co/) console
        2. Select **Open Kibana**.
        3. Open the **API keys** management page in the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create API key**. If you are using an API key with **Restrict privileges**, make sure to review the Indices privileges to provide at least `auto_configure` and `write` permissions for the indices you will be using with this delivery stream.

2. Set up the delivery stream by specifying the following data:

    * Elastic endpoint URL: The URL that you copied in the previous step.
    * API key: The API key that you created in the previous step.
    * Content encoding: To reduce the data transfer costs, use GZIP encoding.
    * Retry duration: A duration between 60 and 300 seconds should be suitable for most use cases.
    * Backup settings: It is recommended to configure S3 backup for failed records. These backups can then be used to restore failed data ingestion caused by unforeseen service outages.


You now have an Amazon Data Firehose delivery specified with:

* source: direct put
* destination: elastic
* parameters: es_datastream_name: logs-aws.cloudtrail-default


## Step 4: Set up a subscription filter to route CloudTrail events to a delivery stream [firehose-cloudtrail-step-four]

:::{image} /solutions/images/observability-firehose-subscription-filter.png
:alt: Firehose subscription filter
:::

The Amazon Data Firehose delivery stream is ready to send logs to your Elastic Cloud deployment.

1. Visit the log group with the CloudTrail events.

    Open the log group where the CloudTrail service is sending the events. You must forward these events to an Elastic stack using the Amazon Data Firehose delivery stream. CloudWatch log group offers a [subscription filter](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Subscriptions.html) that allows you to choose log events from the log group and forward them to other services like Amazon Kinesis stream, an Amazon Data Firehose stream, or AWS Lambda.

2. Create a subscription filter for Amazon Data Firehose by following these steps.

    1. Choose the destination account.

        Select the delivery stream you created in step 3.

    2. Grant permission.

        Follow these steps to enable the CloudWatch service to send log events to the delivery stream in Amazon Data Firehose:

        1. Create a new role with a trust policy that allows CloudWatch to assume the role.

            ```json
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Service": "logs.eu-north-1.amazonaws.com"
                        },
                        "Action": "sts:AssumeRole",
                        "Condition": {
                            "StringLike": {
                                "aws:SourceArn": "arn:aws:logs:eu-north-1:<YOUR ACCOUNT ID>:*"
                            }
                        }
                    }
                ]
            }
            ```

        2. Assign a new IAM policy to the role that permits ”putting records” into a in Amazon Data Firehose delivery stream.

            ```json
            {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Action": "firehose:PutRecord",
                        "Resource": "arn:aws:firehose:eu-north-1:<YOUR ACCOUNT ID>:deliverystream/mbranca-dev-cloudtrail-logs"
                    }
                ]
            }
            ```


When the new role is ready, you can select it in the subscription filter. Select **Amazon CloudTrail** in the log format option to configure log format and filters.


### Verify [_verify]

To check if there are destination error logs, go to the AWS console, visit your Amazon Data Firehose delivery stream, and check for entries in the **Destination error logs**.

If everything is correct, this list should be empty. If there’s an error, you can check the details. The following example shows a delivery stream that fails to send records to the Elastic stack due to bad authentication settings:

:::{image} /solutions/images/observability-firehose-failed-delivery-stream.png
:alt: Firehose failed delivery stream
:::

The Amazon Data Firehose delivery stream reports the number of failed deliveries and failure details.


## Step 5: Visualize your CloudTrail logs in {{kib}} [firehose-cloudtrail-step-five]

With the new subscription filter running, CloudWatch starts routing new CloudTrail log events to the Firehose delivery stream.

:::{image} /solutions/images/observability-firehose-monitor-cloudtrail-logs.png
:alt: Firehose monitor CloudTrail logs
:::

Navigate to {{kib}} and choose among the following monitoring options:

* **Visualize your logs with Discover**

    :::{image} /solutions/images/observability-firehose-cloudtrail-discover.png
    :alt: Visualize CloudTrail logs with Disocver
    :::


* **Visualize your logs with the CloudTrail Dashboard**

    :::{image} /solutions/images/observability-firehose-cloudtrail-dashboard.png
    :alt: Visualize CloudTrail logs with CloudTrail Dashboard
    :::
