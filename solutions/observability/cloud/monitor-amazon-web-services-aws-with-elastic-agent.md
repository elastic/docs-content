---
navigation_title: Monitor {{aws}} with {{agent}}
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-aws-elastic-agent.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---



# Monitor Amazon Web Services (AWS) with Elastic Agent [monitor-aws-elastic-agent]


In this tutorial, you’ll learn how to deploy {{agent}} and monitor your AWS infrastructure with Elastic {{observability}}.


## What you’ll learn [aws-elastic-agent-what-you-learn]

You’ll learn how to:

* Collect VPC flow logs and S3 access logs from AWS.
* Collect billing and EC2 metrics from CloudWatch.
* Install and configure {{agent}} to stream the logs and metrics to {{es}}.
* Visualize your data in {{kib}}.

::::{note}
For more use cases, check the [AWS integrations](https://docs.elastic.co/integrations/aws).
::::


First you’ll focus on monitoring logs, then you’ll add metrics after you’ve confirmed that your logs are streaming to {{es}}.


## Before you begin [aws-elastic-agent-before-you-begin]

Create an [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) deployment. The deployment includes an {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data.

In this tutorial, we assume that:

* Your VPC flow logs are already exported to an S3 bucket. To learn how, refer to the AWS documentation about [publishing flow logs to an S3 bucket](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3.html).
* You have EC2 instances in your AWS account. By default, Amazon EC2 sends metric data to CloudWatch. If you don’t have an EC2 instance in your account, refer to the [AWS documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html) to learn how to launch, connect to, and use a Linux instance.


## Step 1: Create a queue and notifications for VPC flow logs [aws-elastic-agent-set-up-sqs-queue-and-notifications]

In this step, you create an Amazon Simple Queue Service (SQS) queue and configure the S3 bucket containing your VPC flow logs to send a message to the SQS queue whenever new logs are present in the S3 bucket.

You should already have an S3 bucket that contains exported VPC flow logs. If you don’t, create one now. To learn how, refer to [publishing flow logs to an S3 bucket](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs-s3.html).

::::{note}
**Why is an SQS queue needed?**

Creating an SQS queue helps avoid significant lagging caused by polling all log files from each S3 bucket. Instead of polling each bucket, you configure the S3 buckets to send a notification to the SQS queue whenever a new object is created. The {{agent}} monitors the SQS queue for new object creation messages and uses information in the messages to retrieve logs from the S3 buckets. With this setup, periodic polling from each S3 bucket is not needed. Instead, the {{agent}} S3 input guarantees near real-time data collection from S3 buckets with both speed and reliability.

::::



### Create an SQS queue [aws-elastic-agent-create-sqs-queue]

To create the SQS queue:

1. Go to the [SQS console](https://console.aws.amazon.com/sqs/) and create an SQS queue. Create a standard SQS queue that uses the default settings.

    ::::{important}
    Make sure you create the SQS queue in the same region as the S3 bucket.

    ::::

2. Edit the queue you created and use a JSON object to define an advanced access policy. The access policy allows S3 ObjectCreated events to be sent to the queue.

    ```shell
    {
      "Version": "2012-10-17",
      "Id": "example-ID",
      "Statement": [
        {
          "Sid": "example-statement-ID",
          "Effect": "Allow",
          "Principal": {
            "AWS": "*"
          },
          "Action": "SQS:SendMessage",
          "Resource": "<sqs-arn>", <1>
          "Condition": {
            "StringEquals": {
              "aws:SourceAccount": "<source-account>" <2>
            },
            "ArnLike": {
              "aws:SourceArn": "<s3-bucket-arn>" <3>
            }
          }
        }
      ]
    }
    ```

    1. Replace `<sqs-arn>` with the ARN of the SQS queue.
    2. Replace `<source-account>` with your AWS account number.
    3. Replace `<s3-bucket-arn>` with the ARN of the S3 bucket containing your VPC flow logs.


    Save your changes and make a note of the queue URL. You will need it later when you configure the AWS integration in {{kib}}.



### Enable event notification on the S3 bucket [aws-elastic-agent-enable-event-notification]

Now that your queue is created, go to the properties of the S3 bucket containing the VPC flow logs and enable event notification:

1. Click **Create event notification**.
2. For the event type, select **All object create events** to send a notification for every object creation event.
3. For the destination, select the SQS queue you just created.


## Step 2: Install the AWS integration [aws-elastic-agent-add-aws-integration]

In this step, you install the AWS integration in {{kib}}. The AWS integration contains inputs for collecting a variety of logs and metrics from AWS. You’ll start out by configuring the integration to collect VPC flow logs. After you get that working, you’ll learn how to add S3 access logs.

To add the integration:

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the query bar, search for **AWS** and select the AWS integration to see more details about it.
3. Click **Add AWS**.
4. Configure the integration name and optionally add a description.

    ::::{tip}
    If you don’t see options for configuring the integration, you’re probably in a workflow designed for new deployments. Follow the steps, then return to this tutorial when you’re ready to configure the integration.
    ::::

5. Specify the AWS credentials required to connect to AWS and read log files. In this tutorial, we use an AWS access key ID and secret, but there are a few other ways to provide AWS credentials. To learn more, refer to the [AWS integration](https://docs.elastic.co/en/integrations/aws) documentation. The account you specify must have at least the following privileges:

    ```yaml
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                  "s3:GetObject",
                  "sqs:ReceiveMessage",
                  "sqs:ChangeMessageVisibility",
                  "sqs:DeleteMessage"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    }
    ```

6. Turn off all data collection selectors *except* **Collect VPC flow logs from S3**.
7. Change defaults and in the **Queue URL** field, specify the URL of the SQS queue you created earlier.
8. Click **Save and continue**. This step takes a minute or two to complete. When it’s done, you’ll have an agent policy that contains the AWS configuration you just specified.

A popup should appear that prompts you to **Add {{agent}} to your hosts**.


## Step 3: Install and run an {{agent}} on your machine [aws-elastic-agent-install]

You can install {{agent}} on any host that can access the AWS account and forward events to {{es}}.

1. In the popup, click **Add {{agent}} to your hosts** to open the **Add agent** flyout.

    ::::{tip}
    If you accidentally closed the popup, go to **{{fleet}} → Agents**, then click **Add agent** to access the installation instructions.
    ::::


    The **Add agent** flyout has two options: **Enroll in {{fleet}}** and **Run standalone**. The default is to enroll the agents in {{fleet}}, as this reduces the amount of work on the person managing the hosts by providing a centralized management tool in {{kib}}.

2. The enrollment token you need should already be selected.

    ::::{note}
    The enrollment token is specific to the {{agent}} policy that you just created. When you run the command to enroll the agent in {{fleet}}, you will pass in the enrollment token.
    ::::

3. To download, install, and enroll the {{agent}}, select your host operating system and copy the installation command shown in the instructions.
4. Run the command on the host where you want to install {{agent}}.

It takes a few minutes for {{agent}} to enroll in {{fleet}}, download the configuration specified in the policy, and start collecting data. You can wait to confirm incoming data, or close the window.

**What have you achieved so far?**

VPC flow logs are sent to an S3 bucket, which sends a notification to the SQS queue. When {{agent}} detects a new message in the queue, it uses the information in the message to retrieve flow logs from the S3 bucket. {{agent}} processes each message, parses it into fields, and then sends the data to {{es}}.

:::{image} /solutions/images/observability-agent-tut-one-bucket-archi.png
:alt: Diagram of the current logging architecture for VPC flow logs
:::


## Step 4: Collect S3 access logs [aws-elastic-agent-collect-s3-access-logs]

::::{note}
S3 access logs contain detailed records for the requests that are made to a bucket. Server access logs are useful for many applications. For example, access log information can be useful in security and access audits. It can also help you learn about your customer base and understand your Amazon S3 bill.

::::


Next, you’ll collect S3 access logs generated by the bucket that contains VPC flow logs. You could use any S3 bucket to generate S3 access logs, but to avoid creating extra buckets in AWS, you’ll use a bucket that already exists.

You create a new S3 bucket and queue for the access logs, then configure the older S3 bucket to generate access logs.

When you’re done, your monitoring architecture will look like this:

:::{image} /solutions/images/observability-agent-tut-two-buckets-archi.png
:alt: Diagram of the logging architecture with access logging enabled
:::


### Create a bucket and queue for S3 access logs [aws-elastic-agent-create-S3-bucket]

To create the new bucket and queue for S3 access logs:

1. In the [AWS S3 console](https://s3.console.aws.amazon.com/s3), click **Create bucket**. Give the bucket a **name** and specify the **region** where you want it deployed.

    ::::{important}
    Make sure you create the S3 bucket and SQS queue (next step) in the same region as the bucket containing VPC flow logs.

    ::::

2. Follow the steps you learned earlier to create an SQS queue and edit the access policy (use the ARNs of the new S3 bucket and queue). Make a note of the queue URL because you will need it later when you configure S3 access log collection.
3. Configure the new S3 bucket to send notifications to the new queue when objects are created (follow the steps you learned earlier).
4. Go back to the old S3 bucket (the one that contains VPC flow logs), and under **Properties**, edit the **Server access logging** properties. Enable server access logging, and select the new bucket you created as the target bucket.

Now you’re ready to edit the agent policy and configure S3 access log collection.


### Configure the integration to collect S3 access logs [aws-elastic-agent-configure-integration-accesslogs]

The {{agent}} you’ve deployed is already running and collecting VPC flow logs. Now you need to edit the agent policy and configure the integration to collect S3 access logs.

1. In {{kib}}, find **Fleet** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. On the **Agents** tab, click the policy your agent is using.
3. Edit the AWS integration policy and turn on the **Collect S3 access logs from S3** selector.
4. In the **Queue URL** field, enter the URL of the SQS queue you created for S3 access log notifications, then save and deploy your changes.

It takes a few minutes for {{agent}} to update its configuration and start collecting data.


## Step 5: Visualize AWS logs [aws-elastic-agent-visualize-logs]

Now that logs are streaming into {{es}}, you can visualize them in {{kib}}. To see the raw logs, find **Discover** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

Notice that you can filter on a specific data stream. For example, set `data_stream.dataset : "aws.s3access"` to show S3 access logs.

The AWS integration also comes with pre-built dashboards that you can use to visualize the data. In {{kib}}, open the main menu and click **Dashboard**. Search for `VPC Flow` and select the dashboard called **[Logs AWS] VPC Flow Log Overview**:

:::{image} /solutions/images/observability-agent-tut-vpcflowlog-dashboard.png
:alt: Screenshot of the VPC Flow Log Overview dashboard
:screenshot:
:::

Next, open the dashboard called **[Logs AWS] S3 Server Access Log Overview**:

:::{image} /solutions/images/observability-agent-tut-s3accesslog-dashboard.png
:alt: Screenshot of the S3 Server Access Log Overview dashboard
:screenshot:
:::


## Step 6: Collect AWS metrics [aws-elastic-agent-collect-metrics]

In this step, you configure the AWS integration to periodically fetch monitoring metrics from AWS CloudWatch using **GetMetricData** API for AWS services. Specifically you’ll learn how to stream and process billing and EC2 metrics.

::::{important}
Extra AWS charges on CloudWatch API requests may be generated if you configure the AWS integration to collect metrics. To learn more, refer to the [Amazon CloudWatch pricing](https://aws.amazon.com/cloudwatch/pricing/) page.
::::


1. Make sure the AWS account used to collect metrics from CloudWatch has at least the following permissions:

    ```yaml
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": [
                    "ec2:DescribeInstances",
                    "ec2:DescribeRegions",
                    "cloudwatch:GetMetricData",
                    "cloudwatch:ListMetrics",
                    "sts:GetCallerIdentity",
                    "iam:ListAccountAliases",
                    "tag:getResources",
                    "ce:GetCostAndUsage"
                ],
                "Effect": "Allow",
                "Resource": "*"
            }
        ]
    }
    ```

2. In {{kib}}, find **Fleet** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
3. On the **Agents** tab, click the policy your agent is using.
4. Edit the AWS integration policy and turn on the **Collect billing metrics** selector. You can accept the defaults.
5. Also turn on the **Collect EC2 metrics** selector. Optionally change the defaults, then save and deploy your changes.

It takes a few minutes for {{agent}} to update its configuration and start collecting data.


## Step 7: Visualize AWS metrics [aws-elastic-agent-visualize-metrics]

Now that the metrics are streaming into {{es}}, you can visualize them in {{kib}}. Find **Discover** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Select the `metrics-*` data view, then filter on `data_stream.dataset: "aws.ec2_metrics"`:

:::{image} /solutions/images/observability-agent-tut-ec2-metrics-discover.png
:alt: Screenshot of the Discover app showing EC2 metrics
:screenshot:
:::

The AWS integration also comes with pre-built dashboards that you can use to visualize the data. Find **Dashboards** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

Search for EC2 and select the dashboard called **[Metrics AWS] EC2 Overview**:

:::{image} /solutions/images/observability-agent-tut-ec2-overview-dashboard.png
:alt: Screenshot of the EC2 Overview dashboard
:screenshot:
:::

To track your AWS billing, open the **[Metrics AWS] Billing Overview** dashboard:

:::{image} /solutions/images/observability-agent-tut-billing-dashboard.png
:alt: Screenshot of the Billing Overview dashboard
:screenshot:
:::

Congratulations! You have completed the tutorial.
