---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-aws-metrics.html
---

# AWS metrics [observability-aws-metrics]

::::{important}
Additional AWS charges for GetMetricData API requests are generated using this module.

::::



## Monitor EC2 instances [monitor-ec2-instances]

To analyze EC2 instance metrics, you can select view filters based on the following predefined metrics, or you can add [custom metrics](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

|  |  |
| --- | --- |
| **CPU Usage** | Average of `aws.ec2.cpu.total.pct`. |
| **Inbound Traffic** | Average of `aws.ec2.network.in.bytes_per_sec`. |
| **Outbound Traffic** | Average of `aws.ec2.network.out.bytes_per_sec`. |
| **Disk Reads (Bytes)** | Average of `aws.ec2.diskio.read.bytes_per_sec`. |
| **Disk Writes (Bytes)** | Average of `aws.ec2.diskio.write.bytes_per_sec`. |


## Monitor S3 buckets [monitor-s3-buckets]

To analyze S3 bucket metrics, you can select view filters based on the following predefined metrics, or you can add [custom metrics](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

|  |  |
| --- | --- |
| **Bucket Size** | Average of `aws.s3_daily_storage.bucket.size.bytes`. |
| **Total Requests** | Average of `aws.s3_request.requests.total`. |
| **Number of Objects** | Average of `aws.s3_daily_storage.number_of_objects`. |
| **Downloads (Bytes)** | Average of `aws.s3_request.downloaded.bytes`. |
| **Uploads (Bytes)** | Average of `aws.s3_request.uploaded.bytes`. |


## Monitor SQS queues [monitor-sqs-queues]

To analyze SQS queue metrics, you can select view filters based on the following predefined metrics, or you can add [custom metrics](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

|  |  |
| --- | --- |
| **Messages Available** | Max of `aws.sqs.messages.visible`. |
| **Messages Delayed** | Max of `aws.sqs.messages.delayed`. |
| **Messages Added** | Max of `aws.sqs.messages.sent`. |
| **Messages Returned Empty** | Max of `aws.sqs.messages.not_visible`. |
| **Oldest Message** | Max of `aws.sqs.oldest_message_age.sec`. |


## Monitor RDS databases [monitor-rds-databases]

To analyze RDS database metrics, you can select view filters based on the following predefined metrics, or you can add [custom metrics](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

|  |  |
| --- | --- |
| **CPU Usage** | Average of `aws.rds.cpu.total.pct`. |
| **Connections** | Average of `aws.rds.database_connections`. |
| **Queries Executed** | Average of `aws.rds.queries`. |
| **Active Transactions** | Average of `aws.rds.transactions.active`. |
| **Latency** | Average of `aws.rds.latency.dml`. |

For information about the fields used by the Infrastructure UI to display AWS services metrics, see the [Infrastructure app fields](/reference/observability/serverless/infrastructure-app-fields.md).
