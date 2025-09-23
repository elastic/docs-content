---
navigation_title: Monitor {{aws}} with Elastic Serverless Forwarder
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-aws-esf.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---



# Monitor Amazon Web Services (AWS) with Elastic Serverless Forwarder [monitor-aws-esf]


The Elastic Serverless Forwarder (ESF) is an Amazon Web Services (AWS) Lambda function that ships logs from your AWS environment to Elastic. Elastic Serverless Forwarder is published in the AWS Serverless Application Repository (SAR). For more information on ESF, check the [Elastic Serverless Forwarder Guide](elastic-serverless-forwarder://reference/index.md).


## What you’ll learn [aws-esf-what-you-learn]

In this tutorial, you’ll learn how to:

* Enable AWS VPC flow logs to be sent to your S3 bucket
* Create an SQS queue and notifications for VPC flow logs
* Install and configure the Elastic AWS integration from {{kib}}
* Visualize and analyze AWS logs in the Elastic Stack


## Before you begin [aws-esf-prerequisites]

Create an [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) deployment. The deployment includes an {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data. Elastic Serverless Forwarder works with Elastic Stack 7.17 and later. You also need an AWS account with permissions to pull the necessary data from AWS.


## Step 1: Create an S3 Bucket to store VPC flow logs [esf-step-one]

1. In the [AWS S3 console](https://s3.console.aws.amazon.com/s3), choose **Create bucket** from the left navigation pane.
2. Specify the AWS region in which you want it deployed.
3. Enter the bucket name.

For more details, refer to the Amazon documentation on how to [Create your first S3 bucket](https://docs.aws.amazon.com/AmazonS3/latest/userguide/creating-bucket.html).


## Step 2: Enable AWS VPC flow logs to be sent to your S3 bucket [esf-step-two]

1. In the [Amazon EC2 console](https://console.aws.amazon.com/ec2/), choose **Network Interfaces** from the left navigation pane.
2. Select the network interface you want to use.
3. From the **Actions** drop-down menu, choose **Create flow log**.
4. For **Destination**, select **Send to an S3 bucket**.
5. For **S3 bucket ARN**, enter the name of the S3 bucket you created in the previous step.

For more details, refer to the Amazon documentation on how to [Create a flow log that publishes to Amazon S3](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3.html).


## Step 3: Create an SQS queue and notifications for VPC flow logs [esf-step-three]

The Amazon Simple Queue Service (SQS) event notification on Amazon S3 serves as a trigger for the Lambda function. When a new log file gets written to an Amazon S3 bucket and meets the criteria, a notification is generated that triggers the Lambda function.

1. In the [SQS console](https://console.aws.amazon.com/sqs/) create a standard SQS queue that uses the default settings.

    ::::{important}
    Make sure you set a visibility timeout of 910 seconds for any SQS queues you want to use as a trigger. This is 10 seconds greater than the Elastic Serverless Forwarder Lambda timeout. If this requirement is not met, CloudFormation will throw an error.
    ::::

2. In the **Advanced** settings, modify the JSON access policy to define which S3 ObjectCreated events should be sent to the queue. Here is an example of JSON file:

    ```json
    {
      "Version": "2008-10-17",
      "Id": "__default_policy_ID",
      "Statement": [
        {
          "Sid": "__owner_statement",
          "Effect": "Allow",
          "Principal": {
            "AWS": "arn:aws:iam::627286350134:root"
          },
          "Action": "SQS:*",
          "Resource": "arn:aws:sqs:eu-central-1:627286350134:vpc-flow-logs-docs-queue"
        },
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "s3.amazonaws.com"
          },
          "Action": "SQS:SendMessage",
          "Resource": "arn:aws:sqs:eu-central-1:627286350134:vpc-flow-logs-docs-queue"
        }
      ]
    }
    ```

3. Go to the properties of the S3 bucket containing the VPC flow logs and enable event notification.

For more details, refer to the AWS documentation on how to [Configure a bucket for notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ways-to-add-notification-config-to-bucket.html).


## Step 4: Install the Elastic AWS integration [esf-step-four]

{{kib}} offers prebuilt dashboards, ingest node configurations, and other assets that help you get the most value out of the logs you ingest.

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for AWS.
3. Click the AWS integration, select **Settings** and click **Install AWS assets** to install all the AWS integration assets.


## Step 5: Create a new S3 bucket to store the configuration file [esf-step-five]

Note that you can store more than one configuration file.

1. In the [AWS S3 console](https://s3.console.aws.amazon.com/s3), click **Create** bucket. Give the bucket a name and specify the region where you want it deployed.

    ::::{important}
    Make sure you create the S3 bucket in the same region as the bucket containing VPC flow logs.
    ::::



## Step 6: Create a configuration file to specify the source and destination [esf-step-six]

Elastic Serverless Forwarder uses the configuration file to know the input source and the Elastic connection for the destination information.

1. In Elastic Cloud, from the AWS Integrations page click **Connection details** on the upper right corner and copy your Cloud ID.
2. Create an encoded API key for authentication.

    You are going to reference both the Cloud ID and the newly created API key from the configuration file. Here is an example:

    ```yaml
    inputs:
      - type: "s3-sqs"
        id: "<your-sqs-queue-arn>"
        outputs:
          - type: "elasticsearch"
            args:
              cloud_id: "<your-cloud-id>"
              api_key: "<your-api-key>>"
    ```

3. Upload the configuration file you have just created to the S3 bucket you created at step 5.


## Step 7: Ingest VPC flow logs into Elastic [esf-step-seven]

Deploy the Elastic Serverless Forwarder from AWS SAR and provide appropriate configurations for the Lambda function to start ingesting VPC flow logs into Elastic.

1. From the Lambda console select **Applications** and click **Create Application**.
2. From the **Serverless application** tab, select **elastic-serverless-forwarder**.
3. On the **Review, configure and deploy** page, fill in the following fields:

    * **ElasticServerlessForwarderS3Buckets**: Specify the ARN of the S3 Bucket you created at step 1 where the VPC Flow Logs are sent.
    * **ElasticServerlessForwarderS3ConfigFile**: Specify the URL of the configuration file in the format "s3://bucket-name/config-file-name".
    * **ElasticServerlessForwarderS3SQSEvents**: Specify the S3 SQS Notifications queue used as the trigger of the Lambda function. The value is the ARN of the SQS Queue you created at step 3.


The above values are used by the Lambda deployment to create minimal IAM policies and set up the environment variables for the Lambda function to execute properly. The deployed Lambda will read the VPC flow log files as they get written to the S3 bucket and send it to Elastic.


## Step 8: Visualize AWS logs [esf-step-eight]

Navigate to Kibana to see your logs parsed and visualized in the [Logs AWS] VPC Flow Log Overview dashboard.
