---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/aws-metrics.html
---

# AWS metrics [aws-metrics]

::::{important} 
Additional AWS charges for GetMetricData API requests are generated using this module.

::::



## Monitor EC2 instances [monitor-ec2-instances] 

To help you analyze the EC2 instance metrics listed on the **Infrastructure inventory** page, you can select view filters based on the following predefined metrics or you can add [custom metrics](../infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

|     |     |
| --- | --- |
| **CPU Usage** | Average of `aws.ec2.cpu.total.pct`. |
| **Inbound Traffic** | Average of `aws.ec2.network.in.bytes_per_sec`. |
| **Outbound Traffic** | Average of `aws.ec2.network.out.bytes_per_sec`. |
| **Disk Reads (Bytes)** | Average of `aws.ec2.diskio.read.bytes_per_sec`. |
| **Disk Writes (Bytes)** | Average of `aws.ec2.diskio.write.bytes_per_sec`. |


## Monitor S3 buckets [monitor-s3-buckets] 

To help you analyze the S3 bucket metrics listed on the **Infrastructure inventory** page, you can select view filters based on the following predefined metrics or you can add [custom metrics](../infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

|     |     |
| --- | --- |
| **Bucket Size** | Average of `aws.s3_daily_storage.bucket.size.bytes`. |
| **Total Requests** | Average of `aws.s3_request.requests.total`. |
| **Number of Objects** | Average of `aws.s3_daily_storage.number_of_objects`. |
| **Downloads (Bytes)** | Average of `aws.s3_request.downloaded.bytes`. |
| **Uploads (Bytes)** | Average of `aws.s3_request.uploaded.bytes`. |


## Monitor SQS queues [monitor-sqs-queues] 

To help you analyze the SQS queue metrics listed on the **Infrastructure inventory** page, you can select view filters based on the following predefined metrics or you can add [custom metrics](../infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

|     |     |
| --- | --- |
| **Messages Available** | Max of `aws.sqs.messages.visible`. |
| **Messages Delayed** | Max of `aws.sqs.messages.delayed`. |
| **Messages Added** | Max of `aws.sqs.messages.sent`. |
| **Messages Returned Empty** | Max of `aws.sqs.messages.not_visible`. |
| **Oldest Message** | Max of `aws.sqs.oldest_message_age.sec`. |


## Monitor RDS databases [monitor-rds-databases] 

To help you analyze the RDS database metrics listed on the **Infrastructure inventory** page, you can select view filters based on the following predefined metrics or you can add [custom metrics](../infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

|     |     |
| --- | --- |
| **CPU Usage** | Average of `aws.rds.cpu.total.pct`. |
| **Connections** | Average of `aws.rds.database_connections`. |
| **Queries Executed** | Average of `aws.rds.queries`. |
| **Active Transactions** | Average of `aws.rds.transactions.active`. |
| **Latency** | Average of `aws.rds.latency.dml`. |

For information about which required fields the {{infrastructure-app}} uses to display AWS services metrics, see the [{{infrastructure-app}} field reference](asciidocalypse://docs/docs-content/docs/reference/observability/fields-and-object-schemas/metrics-app-fields.md).

