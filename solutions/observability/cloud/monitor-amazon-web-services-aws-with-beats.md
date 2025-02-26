---
navigation_title: "Monitor {{aws}} with {{beats}}"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-aws.html
---



# Monitor Amazon Web Services (AWS) with Beats [monitor-aws]


In this tutorial, you’ll learn how to monitor your {{aws}} infrastructure using Elastic {{observability}}: Logs and Infrastructure metrics.


## What you’ll learn [aws-what-you-learn]

You’ll learn how to:

* Create and configure an S3 bucket
* Create and configure an SQS queue.
* Install and configure {{filebeat}} and {{metricbeat}} to collect Logs and Infrastructure metrics
* Collect logs from S3
* Collect metrics from Amazon CloudWatch


## Before you begin [aws-before-you-begin]

Create an [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) deployment. The deployment includes an {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data.

With this tutorial, we assume that your logs and your infrastructure data are already shipped to CloudWatch. We are going to show you how you can stream your data from CloudWatch to {{es}}. If you don’t know how to put your AWS logs and infrastructure data in CloudWatch, Amazon provides a lot of documentation around this specific topic:

* Collect your logs and infrastructure data from specific [AWS services](https://www.youtube.com/watch?v=vAnIhIwE5hY)
* Export your logs [to an S3 bucket](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/S3ExportTasksConsole.md)


## Step 1:  Create an S3 Bucket [aws-step-one]

To centralize your logs in {{es}}, you need to have an S3 bucket. {{filebeat}}, the agent you’ll use to collect logs, has an input for S3.

In the [AWS S3 console](https://s3.console.aws.amazon.com/s3), click on **Create bucket**. Give the bucket a **name** and specify the **region** in which you want it deployed.

:::{image} ../../../images/observability-creating-a-s3-bucket.png
:alt: S3 bucket creation
:::


## Step 2:  Create an SQS Queue [aws-step-two]

You should now have an S3 bucket in which you can export your logs, but you will also need an SQS queue. To avoid significant lagging with polling all log files from each S3 bucket, we will use Amazon Simple Queue Service (SQS). This will provide us with an Amazon S3 notification when a new S3 object is created. The [{{filebeat}} S3 input](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-input-aws-s3.md) checks SQS for new messages regarding the new object created in S3 and uses the information in these messages to retrieve logs from S3 buckets. With this setup, periodic polling from each S3 bucket is not needed. Instead, the {{filebeat}} S3 input guarantees near real-time data collection from S3 buckets with both speed and reliability.

Create an SQS queue and configure our S3 bucket to send a message to the SQS queue whenever new logs are present in the S3 bucket. Go to the [SQS console](https://eu-central-1.console.aws.amazon.com/sqs/)

::::{note}
Make sure that the queue is created in the same region as the S3 bucket.

::::


:::{image} ../../../images/observability-creating-a-queue.png
:alt: Queue Creation
:::

Create a standard SQS queue and edit the access policy by using a JSON object to define an advanced access policy:

::::{note}
Replace `<sqs-arn>` with the ARN of the SQS queue, `<s3-bucket-arn>` with the ARN of the S3 bucket you just created, the `<source-account>` with your source account.

::::


```console
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
      "Resource": "<sqs-arn>",
      "Condition": {
        "StringEquals": {
          "aws:SourceAccount": "<source-account>"
        },
        "ArnLike": {
          "aws:SourceArn": "<s3-bucket-arn>"
        }
      }
    }
  ]
}
```


## Step 3:  Enable Event Notification [aws-step-three]

Now that your queue is created, go to the properties of the S3 bucket you created and click **Create event notification**.

Specify that you want to send a notification on every object creation event.

:::{image} ../../../images/observability-configure-event-notification.png
:alt: Event Notification Setting
:::

Set the destination as the SQS queue you just created.

:::{image} ../../../images/observability-configure-notification-output.png
:alt: Event Notification Setting
:::


## Step 4: Install and configure {{filebeat}} [aws-step-four]

To monitor AWS using the {{stack}}, you need two main components: an Elastic deployment to store and analyze the data and an agent to collect and ship the data.


### Install {{filebeat}} [_install_filebeat]

Download and install {{filebeat}}.

:::::::{tab-set}

::::::{tab-item} DEB
Version 9.0.0-beta1 of Filebeat has not yet been released.
::::::

::::::{tab-item} RPM
Version 9.0.0-beta1 of Filebeat has not yet been released.
::::::

::::::{tab-item} MacOS
Version 9.0.0-beta1 of Filebeat has not yet been released.
::::::

::::::{tab-item} Linux
Version 9.0.0-beta1 of Filebeat has not yet been released.
::::::

::::::{tab-item} Windows
Version 9.0.0-beta1 of Filebeat has not yet been released.
::::::

:::::::

### Set up assets [_set_up_assets]

{{filebeat}} comes with predefined assets for parsing, indexing, and visualizing your data. Run the following command to load these assets. It may take a few minutes.

```bash
./filebeat setup -e -E 'cloud.id=YOUR_DEPLOYMENT_CLOUD_ID' -E 'cloud.auth=elastic:YOUR_SUPER_SECRET_PASS' <1>
```

1. Substitute your Cloud ID and an administrator’s `username:password` in this command. To find your Cloud ID, click on your [deployment](https://cloud.elastic.co/deployments).


::::{important}
Setting up {{filebeat}} is an admin-level task that requires extra privileges. As a best practice, [use an administrator role to set up](asciidocalypse://docs/beats/docs/reference/filebeat/privileges-to-setup-beats.md) and a more restrictive role for event publishing (which you will do next).

::::



### Configure {{filebeat}} output [_configure_filebeat_output]

Next, you are going to configure {{filebeat}} output to {{ecloud}}.

1. Use the {{filebeat}} keystore to store [secure settings](asciidocalypse://docs/beats/docs/reference/filebeat/keystore.md). Store the Cloud ID in the keystore.

    ```bash
    ./filebeat keystore create
    echo -n "<Your Deployment Cloud ID>" | ./filebeat keystore add CLOUD_ID --stdin
    ```

2. To store logs in {{es}} with minimal permissions, create an API key to send data from {{filebeat}} to {{ecloud}}. Log into {{kib}} (you can do so from the Cloud Console without typing in any permissions) and find `Dev Tools` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Send the following request:

    ```console
    POST /_security/api_key
    {
      "name": "filebeat-monitor-gcp",
      "role_descriptors": {
        "filebeat_writer": {
          "cluster": [
            "monitor",
            "read_ilm",
            "cluster:admin/ingest/pipeline/get", <1>
            "cluster:admin/ingest/pipeline/put" <1>
          ],
          "index": [
            {
              "names": ["filebeat-*"],
              "privileges": ["view_index_metadata", "create_doc"]
            }
          ]
        }
      }
    }
    ```

    1. {{filebeat}} needs extra cluster permissions to publish logs, which differs from the {{metricbeat}} configuration. You can find more details [here](asciidocalypse://docs/beats/docs/reference/filebeat/feature-roles.md).

3. The response contains an `api_key` and an `id` field, which can be stored in the {{filebeat}} keystore in the following format: `id:api_key`.

    ```bash
    echo -n "IhrJJHMB4JmIUAPLuM35:1GbfxhkMT8COBB4JWY3pvQ" | ./filebeat keystore add ES_API_KEY --stdin
    ```

    ::::{note}
    Make sure you specify the `-n` parameter; otherwise, you will have painful debugging sessions due to adding a newline at the end of your API key.

    ::::

4. To see if both settings have been stored, run the following command:

    ```bash
    ./filebeat keystore list
    ```

5. To configure {{filebeat}} to output to {{ecloud}}, edit the `filebeat.yml` configuration file. Add the following lines to the end of the file.

    ```yaml
    cloud.id: ${CLOUD_ID}
    output.elasticsearch:
      api_key: ${ES_API_KEY}
    ```

6. Finally, test if the configuration is working. If it is not working, verify that you used the right credentials and, if necessary, add them again.

    ```bash
    ./filebeat test output
    ```



## Step 5: Configure the AWS Module [aws-step-five]

Now that the output is working, you can set up the [{{filebeat}} AWS](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-aws.md) module which will automatically create the AWS input. This module checks SQS for new messages regarding the new object created in the S3 bucket and uses the information in these messages to retrieve logs from S3 buckets. With this setup, periodic polling from each S3 bucket is not needed.

There are many different filesets available: `cloudtrail`, `vpcflow`, `ec2`, `cloudwatch`, `elb` and `s3access`. In this tutorial, we are going to show you a few examples using the `ec2` and the `s3access` filesets.

The `ec2` fileset is used to ship and process logs stored in CloudWatch, and export them to an S3 bucket. The `s3access` fileset is used when S3 access logs need to be collected. It provides detailed records for the requests that are made to a bucket. Server access logs are useful for many applications. For example, access log information can be useful in security and access audits. It can also help you learn about your customer base and understand your Amazon S3 bill.

Let’s enable the AWS module in {{filebeat}}.

```bash
./filebeat modules enable aws
```

Edit the `modules.d/aws.yml` file with the following configurations.

```yaml
- module: aws
  cloudtrail:
    enabled: false
  cloudwatch:
    enabled: false
  ec2:
    enabled: true <1>
    var.credential_profile_name: fb-aws <2>
    var.queue_url: https://sqs.eu-central-1.amazonaws.com/836370109380/howtoguide-tutorial <3>
  elb:
    enabled: false
  s3access:
    enabled: false
  vpcflow:
    enabled: false
```

1. Enables the `ec2` fileset.
2. This is the AWS profile defined following the [AWS standard](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.md).
3. Add the URL to the queue containing notifications around the bucket containing the EC2 logs


Make sure that the AWS user used to collect the logs from S3 has at least the following permissions attached to it:

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

You can now upload your logs to the S3 bucket. If you are using CloudWatch, make sure to edit the policy of your bucket as shown in [step 3 of the AWS user guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/S3ExportTasksConsole.md). This will help you avoid permissions issues.

Start {{filebeat}} to collect the logs.

```bash
./filebeat -e
```

Here’s what we’ve achieved so far:

:::{image} ../../../images/observability-one-bucket-archi.png
:alt: Current Architecture
:::

Now, let’s configure the `s3access` fileset. The goal here is to be able to monitor how people access the bucket we created. To do this, we’ll create another bucket and another queue. The new architecture will look like this:

:::{image} ../../../images/observability-two-buckets-archi.png
:alt: Architecture with Access Logging Enabled
:::

Create a new S3 bucket and SQS queue. Ensure that the event notifications on the new bucket are enabled, and that it’s sending notifications to the new queue.

Now go back to the first bucket, and go to **Properties** > **Server access logging**. Specify that you want to ship the access logs to the bucket you most recently created.

:::{image} ../../../images/observability-Server-Access-Logging.png
:alt: Enabling Server Access Logging
:::

Copy the URL of the queue you created. Edit the `modules.d/aws.yml`file with the following configurations.

```yaml
- module: aws
  cloudtrail:
    enabled: false
  cloudwatch:
    enabled: false
  ec2:
    enabled: true <1>
    var.credential_profile_name: fb-aws <2>
    var.queue_url: https://sqs.eu-central-1.amazonaws.com/836370109380/howtoguide-tutorial <3>
  elb:
    enabled: false
  s3access:
    enabled: true <1>
    var.credential_profile_name: fb-aws <2>
    var.queue_url: https://sqs.eu-central-1.amazonaws.com/836370109380/access-log <4>
  vpcflow:
    enabled: false
```

1. Enables the `ec2` fileset.
2. This is the AWS profile defined following the [AWS standard](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.md).
3. Add the URL to the queue containing notifications around the bucket containing the EC2 logs
4. Add the URL to the queue containing notifications around the bucket containing the S3 access logs


Once you have edited the config file, you need to restart {{filebeat}}. To stop {{filebeat}}, you can press CTRL + C in the terminal. Now let’s restart {{filebeat}} by running the following command:

```bash
./filebeat -e
```


## Step 6: Visualize Logs [aws-step-six]

Now that the logs are being shipped to {{es}} we can visualize them in {{kib}}. To see the raw logs, find **Discover** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

The filesets we used in the previous steps also come with pre-built dashboards that you can use to visualize the data. In {{kib}}, find **Dashboards** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Search for S3 and select the dashboard called: **[Filebeat AWS] S3 Server Access Log Overview**:

:::{image} ../../../images/observability-S3-Server-Access-Logs.png
:alt: S3 Server Access Log Overview
:::

This gives you an overview of how your S3 buckets are being accessed.


## Step 7: Collect Infrastructure metrics [aws-step-seven]

To monitor your AWS infrastructure you will need to first make sure your infrastructure data are being shipped to CloudWatch. To ship the data to {{es}} we are going to use the AWS module from {{metricbeat}}. This module periodically fetches monitoring metrics from AWS CloudWatch using **GetMetricData** API for AWS services.

::::{important}
Extra AWS charges on CloudWatch API requests will be generated by this module. Please see [AWS API requests](asciidocalypse://docs/beats/docs/reference/metricbeat/metricbeat-module-aws.md#aws-api-requests) for more details.

::::



## Step 8: Install and configure {{metricbeat}} [aws-step-eight]

In a new terminal window, run the following commands.


### Install {{metricbeat}} [_install_metricbeat]

Download and install {{metricbeat}}.

:::::::{tab-set}

::::::{tab-item} DEB
Version 9.0.0-beta1 of Metricbeat has not yet been released.
::::::

::::::{tab-item} RPM
Version 9.0.0-beta1 of Metricbeat has not yet been released.
::::::

::::::{tab-item} MacOS
Version 9.0.0-beta1 of Metricbeat has not yet been released.
::::::

::::::{tab-item} Linux
Version 9.0.0-beta1 of Metricbeat has not yet been released.
::::::

::::::{tab-item} Windows
Version 9.0.0-beta1 of Metricbeat has not yet been released.
::::::

:::::::

### Set up assets [_set_up_assets_2]

{{metricbeat}} comes with predefined assets for parsing, indexing, and visualizing your data. Run the following command to load these assets. It may take a few minutes.

```bash
./metricbeat setup -e -E 'cloud.id=YOUR_DEPLOYMENT_CLOUD_ID' -E 'cloud.auth=elastic:YOUR_SUPER_SECRET_PASS' <1>
```

1. Substitute your Cloud ID and an administrator’s `username:password` in this command. To find your Cloud ID, click on your [deployment](https://cloud.elastic.co/deployments).


::::{important}
Setting up {{metricbeat}} is an admin-level task that requires extra privileges. As a best practice, [use an administrator role to set up](asciidocalypse://docs/beats/docs/reference/metricbeat/privileges-to-setup-beats.md), and a more restrictive role for event publishing (which you will do next).

::::



### Configure {{metricbeat}} output [_configure_metricbeat_output]

Next, you are going to configure {{metricbeat}} output to {{ecloud}}.

1. Use the {{metricbeat}} keystore to store [secure settings](asciidocalypse://docs/beats/docs/reference/metricbeat/keystore.md). Store the Cloud ID in the keystore.

    ```bash
    ./metricbeat keystore create
    echo -n "<Your Deployment Cloud ID>" | ./metricbeat keystore add CLOUD_ID --stdin
    ```

2. To store metrics in {{es}} with minimal permissions, create an API key to send data from {{metricbeat}} to {{ecloud}}. Log into {{kib}} (you can do so from the Cloud Console without typing in any permissions) and find `Dev Tools` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). From the **Console**, send the following request:

    ```console
    POST /_security/api_key
    {
      "name": "metricbeat-monitor",
      "role_descriptors": {
        "metricbeat_writer": {
          "cluster": ["monitor", "read_ilm"],
          "index": [
            {
              "names": ["metricbeat-*"],
              "privileges": ["view_index_metadata", "create_doc"]
            }
          ]
        }
      }
    }
    ```

3. The response contains an `api_key` and an `id` field, which can be stored in the {{metricbeat}} keystore in the following format: `id:api_key`.

    ```bash
    echo -n "IhrJJHMB4JmIUAPLuM35:1GbfxhkMT8COBB4JWY3pvQ" | ./metricbeat keystore add ES_API_KEY --stdin
    ```

    ::::{note}
    Make sure you specify the `-n` parameter; otherwise, you will have painful debugging sessions due to adding a newline at the end of your API key.

    ::::

4. To see if both settings have been stored, run the following command:

    ```bash
    ./metricbeat keystore list
    ```

5. To configure {{metricbeat}} to output to {{ecloud}}, edit the `metricbeat.yml` configuration file. Add the following lines to the end of the file.

    ```yaml
    cloud.id: ${CLOUD_ID}
    output.elasticsearch:
      api_key: ${ES_API_KEY}
    ```

6. Finally, test if the configuration is working. If it is not working, verify if you used the right credentials and add them again.

    ```bash
    ./metricbeat test output
    ```


Now that the output is working, you are going to set up the AWS module.


## Step 9: Configure the AWS module [aws-step-nine]

To collect metrics from your AWS infrastructure, we’ll use the [{{metricbeat}} AWS](asciidocalypse://docs/beats/docs/reference/metricbeat/metricbeat-module-aws.md) module. This module contains many metricsets: `billing`, `cloudwatch`, `dynamodb`, `ebs`, `ec2`, `elb`, `lambda`, and many more. Each metricset is created to help you stream and process your data. In this tutorial, we’re going to show you a few examples using the `ec2` and the `billing` metricsets.

1. Let’s enable the AWS module in {{metricbeat}}.

    ```bash
    ./metricbeat modules enable aws
    ```

2. Edit the `modules.d/aws.yml` file with the following configurations.

    ```yaml
    - module: aws <1>
      period: 24h <2>
      metricsets:
        - billing <3>
      credential_profile_name: mb-aws <4>
      cost_explorer_config:
        group_by_dimension_keys:
          - "AZ"
          - "INSTANCE_TYPE"
          - "SERVICE"
        group_by_tag_keys:
          - "aws:createdBy"
    - module: aws <1>
      period: 300s <2>
      metricsets:
        - ec2 <3>
      credential_profile_name: mb-aws <4>
    ```

    1. Defines the module that is going to be used.
    2. Defines the period at which the metrics are going to be collected
    3. Defines the metricset that is going to be used.
    4. This is the AWS profile defined following the [AWS standard](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.md).


Make sure that the AWS user used to collect the metrics from CloudWatch has at least the following permissions attached to it:

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

You can now start {{metricbeat}}:

```bash
./metricbeat -e
```


## Step 10: Visualize metrics [aws-step-ten]

Now that the metrics are being streamed to {{es}} we can visualize them in {{kib}}. To open **Infrastructure inventory**, find **Infrastructure** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Make sure to show the **AWS** source and the **EC2 Instances**:

:::{image} ../../../images/observability-EC2-instances.png
:alt: Your EC2 Infrastructure
:::

The metricsets we used in the previous steps also comes with pre-built dashboard that you can use to visualize the data. In {{kib}}, find **Dashboards** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). Search for EC2 and select the dashboard called: **[Metricbeat AWS] EC2 Overview**:

:::{image} ../../../images/observability-ec2-dashboard.png
:alt: EC2 Overview
:::

If you want to track your billings on AWS, you can also check the **[Metricbeat AWS] Billing Overview** dashboard:

:::{image} ../../../images/observability-aws-billing.png
:alt: Billing Overview
:::
