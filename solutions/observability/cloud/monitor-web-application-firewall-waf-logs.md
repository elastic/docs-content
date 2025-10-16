---
navigation_title: WAF logs
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-aws-waf-firehose.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---



# Monitor Web Application Firewall (WAF) logs [monitor-aws-waf-firehose]


In this section, you’ll learn how to send AWS WAF events from AWS to your {{stack}} using Amazon Data Firehose.

You will go through the following steps:

* Select a WAF-compatible resource (for example, a CloudFront distribution)
* Create a delivery stream in Amazon Data Firehose
* Create a web Access Control List (ACL) to generate WAF logs
* Set up logging to forward the logs to the {{stack}} using a Firehose stream
* Visualize your WAF logs in {{kib}}


## Before you begin [firehose-waf-prerequisites]

We assume that you already have:

* An AWS account with permissions to pull the necessary data from AWS.
* An [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) deployment. The deployment includes an {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data. AWS Data Firehose works with Elastic Stack version 7.17 or greater, running on Elastic Cloud only.

::::{important}
Make sure the deployment is on AWS, because the Amazon Data Firehose delivery stream connects specifically to an endpoint that needs to be on AWS.
::::



## Step 1: Install the AWS integration in {{kib}} [firehose-waf-step-one]

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Browse the catalog to find the AWS integration.
3. Navigate to the **Settings** tab and click **Install AWS assets**.


## Step 2: Create a delivery stream in Amazon Data Firehose [firehose-waf-step-two]

1. Go to the [AWS console](https://console.aws.amazon.com/) and navigate to Amazon Data Firehose.
2. Click **Create Firehose stream** and choose the source and destination of your Firehose stream. Unless you are streaming data from Kinesis Data Streams, set source to `Direct PUT` and destination to `Elastic`.
3. Provide a meaningful **Firehose stream name** that will allow you to identify this delivery stream later. Your Firehose name must start with the prefix `aws-waf-logs-` or it will not show up later.

::::{note}
For advanced use cases, source records can be transformed by invoking a custom Lambda function. When using Elastic integrations, this should not be required.
::::



## Step 3: Specify the destination settings for your Firehose stream [firehose-waf-step-three]

1. From the **Destination settings** panel, specify the following settings:

    * **To find the Elasticsearch endpoint URL**:

        1. Go to the [Elastic Cloud](https://cloud.elastic.co/) console
        2. Find your deployment in the **Hosted deployments** card and select **Manage**.
        3. Under **Applications** click **Copy endpoint** next to **Elasticsearch**.

    * **To create the API key**:

        1. Go to the [Elastic Cloud](https://cloud.elastic.co/) console
        2. Select **Open Kibana**.
        3. Open the **API keys** management page in the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create API key**. If you are using an API key with **Restrict privileges**, make sure to review the Indices privileges to provide at least `auto_configure` and `write` permissions for the indices you will be using with this delivery stream.

    * **Content encoding**: For a better network efficiency, leave content encoding set to GZIP.
    * **Retry duration**: Determines how long Firehose continues retrying the request in the event of an error. A duration of 60-300s should be suitable for most use cases.
    * **es_datastream_name**: `logs-aws.waf-default`


::::{important}
Verify that your **Elasticsearch endpoint URL** includes `.es.` between the **deployment name** and **region**. Example: `https://my-deployment.es.us-east-1.aws.elastic-cloud.com`
::::



## Step 4: Create a web access control list [firehose-waf-step-four]

To create a new web access control list (ACL), follow these steps:

1. Go to the [AWS console](https://console.aws.amazon.com/) and navigate to the **WAF & Shield** page.
2. Describe web ACL by entering the resource type, region, and name.
3. Associate it to an AWS resource. If you don’t have an existing resource, you can create and attach a web ACL to several AWS resources:

    * CloudFront distribution
    * Application Load Balancers
    * Amazon API Gateway REST APIs
    * Amazon App Runner services
    * AWS AppSync GraphQL APIs
    * Amazon Cognito user pools
    * AWS Verified Access Instances

4. Add a 1 or 2 rules to the **Free rule groups** list from the AWS managed rule groups. Keep all other settings to their default values.
5. Set the rule priority by keeping default values.
6. Configure metrics by keeping default values.
7. Review and create the web ACL.


## Step 5: Set up logging [firehose-waf-step-five]

1. Go to the web ACL you created in the previous step.
2. Open the **Logging and metrics** section and edit the following settings:

    * **Logging destination**: select "Amazon Data Firehose stream"
    * **Amazon Data Firehose stream**: select the Firehose stream you created in step 2.


WAF creates the required Identity and Access Management (IAM) role. If your Firehose stream name doesn’t appear in the list, make sure the name you chose for the stream starts with `aws-waf-logs-`, as prescribed by AWS naming conventions.


## Step 6: Visualize your WAF logs in {{kib}} [firehose-waf-step-six]

You can now log into your {{stack}} to check if the WAF logs are flowing. To generate logs, you can use cURL to send HTTP requests to your testing CloudFront distribution.

```console
curl -i https://<your cloudfront distribution>.cloudfront.net
```

To maintain a steady flow of logs, you can use `watch -n 5` to repeat the command every 5 seconds.

```console
watch -n 5 curl -i https://<your cloudfront distribution>.cloudfront.net
```

Navigate to Kibana and visualize the first WAF logs in your {{stack}}.

:::{image} /solutions/images/observability-firehose-waf-logs.png
:alt: Firehose WAF logs in Kibana
:screenshot:
:::
