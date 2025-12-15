---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-aws-metrics.html
  - https://www.elastic.co/guide/en/observability/current/aws-metrics.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: cloud-serverless
  - id: observability
---

# AWS metrics [observability-aws-metrics]

::::{important}
Additional AWS charges for GetMetricData API requests are generated using this module.

::::

## Monitor EC2 instances [monitor-ec2-instances]

To analyze EC2 instance metrics, you can select view filters based on the following predefined metrics, or you can add [custom metrics](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

:::{note}
:applies_to: stack: ga 9.3
For EC2 instances, The [Infrastructure UI](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) and [inventory rules](/solutions/observability/incident-management/create-an-inventory-rule.md) only support metrics collected by the [EC2 integration](integration-docs://reference/aws/ec2.md).
:::

### Entity definition [monitor-ec2-entity]
```{applies_to}
stack: ga 9.3
```

|  |  |  |
| --- | --- | --- |
| **Filter** | `event.module : aws` | Used to filter relevant data. |
| **Identifier** | `cloud.instance.id` | Used to identify each entity. |
| **Display value** | `cloud.instance.name` | Used as a display friendly value. |

### Metrics [monitor-ec2-metrics]

|  |  |
| --- | --- |
| **CPU Usage** | Average of `aws.ec2.cpu.total.pct`. |
| **Inbound Traffic** | Average of `aws.ec2.network.in.bytes_per_sec`. |
| **Outbound Traffic** | Average of `aws.ec2.network.out.bytes_per_sec`. |
| **Disk Reads (Bytes)** | Average of `aws.ec2.diskio.read.bytes_per_sec`. |
| **Disk Writes (Bytes)** | Average of `aws.ec2.diskio.write.bytes_per_sec`. |


## Monitor S3 buckets [monitor-s3-buckets]

To analyze S3 bucket metrics, you can select view filters based on the following predefined metrics, or you can add [custom metrics](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

:::{note}
:applies_to: stack: ga 9.3
For S3 buckets, the [Infrastructure UI](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) and [inventory rules](/solutions/observability/incident-management/create-an-inventory-rule.md) only support metric data collected by the [S3 integration](integration-docs://reference/aws/s3.md).
:::

### Entity definition [monitor-s3-entity]
```{applies_to}
stack: ga 9.3
```

|  |  |
| --- | --- |
| **Filter** | `event.module : aws` | Used to filter relevant data. |
| **Identifier** | `aws.s3.bucket.name` | Used to identify each entity. |
| **Display value** | `aws.s3.bucket.name` | Used as a display friendly value. |

### Metrics [monitor-s3-metrics]

|  |  |
| --- | --- |
| **Bucket Size** | Average of `aws.s3_daily_storage.bucket.size.bytes`. |
| **Total Requests** | Average of `aws.s3_request.requests.total`. |
| **Number of Objects** | Average of `aws.s3_daily_storage.number_of_objects`. |
| **Downloads (Bytes)** | Average of `aws.s3_request.downloaded.bytes`. |
| **Uploads (Bytes)** | Average of `aws.s3_request.uploaded.bytes`. |


## Monitor SQS queues [monitor-sqs-queues]

To analyze SQS queue metrics, you can select view filters based on the following predefined metrics, or you can add [custom metrics](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

:::{note}
:applies_to: stack: ga 9.3
For SQS queues, the [Infrastructure UI](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) and [inventory rules](/solutions/observability/incident-management/create-an-inventory-rule.md) only support metric data collected by the [SQS integration](integration-docs://reference/aws/sqs.md).
:::

### Entity definition [monitor-sqs-entity]
```{applies_to}
stack: ga 9.3
```

|  |  |
| --- | --- |
| **Filter** | `event.module : aws` | Used to filter relevant data. |
| **Identifier** | `aws.sqs.queue.name` | Used to identify each entity. |
| **Display value** | `aws.sqs.queue.name` | Used as a display friendly value. |

### Metrics [monitor-sqs-metrics]

|  |  |
| --- | --- |
| **Messages Available** | Max of `aws.sqs.messages.visible`. |
| **Messages Delayed** | Max of `aws.sqs.messages.delayed`. |
| **Messages Added** | Max of `aws.sqs.messages.sent`. |
| **Messages Returned Empty** | Max of `aws.sqs.messages.not_visible`. |
| **Oldest Message** | Max of `aws.sqs.oldest_message_age.sec`. |


## Monitor RDS databases [monitor-rds-databases]

To analyze RDS database metrics, you can select view filters based on the following predefined metrics, or you can add [custom metrics](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md#custom-metrics).

:::{note}
:applies_to: stack: ga 9.3
For RDS databases, the [Infrastructure UI](/solutions/observability/infra-and-hosts/analyze-infrastructure-host-metrics.md) and [inventory rules](/solutions/observability/incident-management/create-an-inventory-rule.md) only support metric data collected by the [RDS](integration-docs://reference/aws/rds.md) integration.
:::

### Entity definition [monitor-rds-entity]
```{applies_to}
stack: ga 9.3
```

|  |  |
| --- | --- |
| **Filter** | `event.module : aws` | Used to filter relevant data. |
| **Identifier** | `aws.rds.db_instance.arn` | Used to identify each entity. |
| **Display value** | `aws.rds.db_instance.identifier` | Used as a display friendly value. |

### Metrics [monitor-rds-metrics]

|  |  |
| --- | --- |
| **CPU Usage** | Average of `aws.rds.cpu.total.pct`. |
| **Connections** | Average of `aws.rds.database_connections`. |
| **Queries Executed** | Average of `aws.rds.queries`. |
| **Active Transactions** | Average of `aws.rds.transactions.active`. |
| **Latency** | Average of `aws.rds.latency.dml`. |

For information about the fields used by the Infrastructure UI to display AWS services metrics, refer to the [Infrastructure app fields](/reference/observability/fields-and-object-schemas.md).