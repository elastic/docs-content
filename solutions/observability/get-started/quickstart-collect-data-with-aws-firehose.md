---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/collect-data-with-aws-firehose.html
  - https://www.elastic.co/guide/en/serverless/current/collect-data-with-aws-firehose.html
---

# Quickstart: Collect data with AWS Firehose [collect-data-with-aws-firehose]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


In this quickstart guide, you’ll learn how to use AWS Firehose to send logs and metrics to Elastic.

The AWS Firehose streams are created using a CloudFormation template, which can collect all available CloudWatch logs and metrics for your AWS account.

This approach requires minimal configuration as the CloudFormation template creates a Firehose stream, enables CloudWatch metrics collection across all namespaces, and sets up an account-level subscription filter for CloudWatch log groups to send logs to Elastic via Firehose. You can use an AWS CLI command or upload the template to the AWS CloudFormation portal to customize the following parameter values:

::::{dropdown} Required Input Parameters
* `ElasticEndpointURL`: Elastic endpoint URL.
* `ElasticAPIKey`: Elastic API Key.

::::


::::{dropdown} Optional Input Parameters
* `HttpBufferInterval`: The Kinesis Firehose HTTP buffer interval, in seconds. Default is `60`.
* `HttpBufferSize`: The Kinesis Firehose HTTP buffer size, in MiB. Default is `1`.
* `S3BackupMode`: Source record backup in Amazon S3, failed data only or all data. Default is `FailedDataOnly`.
* `S3BufferInterval`: The Kinesis Firehose S3 buffer interval, in seconds. Default is `300`.
* `S3BufferSize`: The Kinesis Firehose S3 buffer size, in MiB. Default is `5`.
* `S3BackupBucketARN`: By default, an S3 bucket for backup will be created. You can override this behaviour by providing an ARN of an existing S3 bucket that ensures the data can be recovered if record processing transformation does not produce the desired results.
* `Attributes`: List of attribute name-value pairs for HTTP endpoint separated by commas. For example "name1=value1,name2=value2".

::::


::::{dropdown} Optional Input Parameters Specific for Metrics
* `EnableCloudWatchMetrics`: Enable CloudWatch Metrics collection. Default is `true`. When CloudWatch metrics collection is enabled, by default a metric stream will be created with metrics from all namespaces.
* `FirehoseStreamNameForMetrics`: Name for Amazon Data Firehose Stream for collecting CloudWatch metrics. Default is `elastic-firehose-metrics`.
* `IncludeOrExclude`: Select the metrics you want to stream. You can include or exclude specific namespaces and metrics. If no filter namespace is given, then default to all namespaces. Default is `Include`.
* `MetricNameFilters`: Comma-delimited list of namespace-metric names pairs to use for filtering metrics from the stream. If no metric name filter is given, then default to all namespaces and all metrics. For example "AWS/EC2:CPUUtilization|NetworkIn|NetworkOut,AWS/RDS,AWS/S3:AllRequests".
* `IncludeLinkedAccountsMetrics`: If you are creating a metric stream in a monitoring account, specify `true` to include metrics from source accounts that are linked to this monitoring account, in the metric stream. Default is `false`.
* `Tags`: Comma-delimited list of tags to apply to the metric stream. For example "org:eng,project:firehose".

::::


::::{dropdown} Optional Input Parameters Specific for Logs
* `EnableCloudWatchLogs`: Enable CloudWatch Logs collection. Default is `true`. When CloudWatch logs collection is enabled, an account-level subscription filter policy is created for all CloudWatch log groups (except the log groups created for Firehose logs).
* `FirehoseStreamNameForLogs`: Name for Amazon Data Firehose Stream for collecting CloudWatch logs. Default is `elastic-firehose-logs`.

::::


::::{important}
Some AWS services need additional manual configuration to properly ingest logs and metrics. For more information, check the [AWS integration](https://www.elastic.co/docs/current/integrations/aws) documentation.
::::


Data collection with AWS Firehose is supported on {{ech}} deployments in AWS, Azure and GCP.


## Prerequisites [_prerequisites_5]

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

* An [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) deployment. The deployment includes an {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data.
* A user with the `superuser` [built-in role](../../../deploy-manage/users-roles/cluster-or-deployment-auth/built-in-roles.md) or the privileges required to onboard data.

    ::::{dropdown} Expand to view required privileges
    * [**Cluster**](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-cluster): `['monitor', 'manage_own_api_key']`
    * [**Index**](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md#privileges-list-indices): `{ names: ['logs-*-*', 'metrics-*-*'], privileges: ['auto_configure', 'create_doc'] }`
    * [**Kibana**](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md): `{ spaces: ['*'], feature: { fleet: ['all'], fleetv2: ['all'] } }`

    ::::

* An active AWS account and the necessary permissions to create delivery streams.

::::{note}
The default CloudFormation stack is created in the AWS region selected for the user’s account. This region can be modified either through the AWS Console interface or by specifying a `--region` parameter in the AWS CLI command when creating the stack.
::::

:::

:::{tab-item} Serverless
:sync: serverless

* An {{obs-serverless}} project. To learn more, refer to [Create an Observability project](../../../solutions/observability/get-started/create-an-observability-project.md).
* A user with the **Admin** role or higher—required to onboard system logs and metrics. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).
* An active AWS account and the necessary permissions to create delivery streams.

:::

::::



## Limitations [_limitations_3]

The AWS Firehose receiver has the following limitations:

* It does not support AWS PrivateLink.
* It is not available for on-premise Elastic Stack deployments.
* The CloudFormation template detects and ingests logs and metrics within a single AWS region only.

The following table shows the type of data ingested by the supported AWS services:

| AWS Service | Data type |
| --- | --- |
| VPC Flow Logs | Logs |
| API Gateway | Logs, Metrics |
| CloudTrail | Logs |
| Network Firewall | Logs, Metrics |
| Route53 | Logs |
| WAF | Logs |
| DynamoDB | Metrics |
| EBS | Metrics |
| EC2 | Metrics |
| ECS | Metrics |
| ELB | Metrics |
| EMR | Metrics |
| MSK | Metrics |
| Kinesis Data Stream | Metrics |
| Lambda | Metrics |
| NAT Gateway | Metrics |
| RDS | Metrics |
| S3 | Metrics |
| SNS | Metrics |
| SQS | Metrics |
| Transit Gateway | Metrics |
| AWS Usage | Metrics |
| VPN | Metrics |
| Uncategorized Firehose Logs | Logs |


## Collect your data [_collect_your_data_5]

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

1. In {{kib}}, go to the **Observability** UI and click **Add Data**.
2. Under **What do you want to monitor?** select **Cloud**, **AWS**, and then select **AWS Firehose**.

    :::{image} ../../../images/observability-quickstart-aws-firehose-entry-point.png
    :alt: AWS Firehose entry point
    :class: screenshot
    :::

3. Click **Create Firehose Stream in AWS** to create a CloudFormation stack from the CloudFormation template.
4. Go back to the **Add Observability Data** page.


:::

:::{tab-item} Serverless
:sync: serverless

1. [Create a new {{obs-serverless}} project](../../../solutions/observability/get-started/create-an-observability-project.md), or open an existing one.
2. In your {{obs-serverless}} project, go to **Add Data**.
3. Under **What do you want to monitor?** select **Cloud**, **AWS**, and then select **AWS Firehose**.

    :::{image} ../../../images/serverless-quickstart-aws-firehose-entry-point.png
    :alt: AWS Firehose entry point
    :class: screenshot
    :::

4. Click **Create Firehose Stream in AWS** to create a CloudFormation stack from the CloudFormation template.
5. Go back to the **Add Observability Data** page.

:::

::::

## Visualize your data [_visualize_your_data_4]

After installation is complete and all relevant data is flowing into Elastic, the **Visualize your data** section allows you to access the different dashboards for the various services.

:::{image} ../../../images/observability-quickstart-aws-firehose-dashboards.png
:alt: AWS Firehose dashboards
:class: screenshot
:::

Here is an example of the VPC Flow logs dashboard:

:::{image} ../../../images/observability-quickstart-aws-firehose-vpc-flow.png
:alt: AWS Firehose VPC flow
:class: screenshot
:::

Refer to [What is Elastic {{observability}}?](../../../solutions/observability/get-started/what-is-elastic-observability.md) for a description of other useful features.
