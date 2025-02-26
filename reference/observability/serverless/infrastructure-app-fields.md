---
mapped_pages:
  - https://www.elastic.co/guide/en/serverless/current/observability-infrastructure-monitoring-required-fields.html
---

# Infrastructure app fields [observability-infrastructure-monitoring-required-fields]

This section lists the fields the Infrastructure UI uses to display data. Please note that some of the fields listed here are not [ECS fields](ecs://docs/reference/index.md#_what_is_ecs).


## Additional field details [observability-infrastructure-monitoring-required-fields-additional-field-details]

The `event.dataset` field is required to display data properly in some views. This field is a combination of `metricset.module`, which is the {{metricbeat}} module name, and `metricset.name`, which is the metricset name.

To determine each metric’s optimal time interval, all charts use `metricset.period`. If `metricset.period` is not available, then it falls back to 1 minute intervals.


## Base fields [base-fields]

The `base` field set contains all fields which are on the top level. These fields are common across all types of events.

| Field | Description | Type |
| --- | --- | --- |
| `@timestamp` | Date/time when the event originated.<br><br>This is the date/time extracted from the event, typically representing when the source generated the event. If the event source has no original timestamp, this value is typically populated by the first time the pipeline received the event. Required field for all events.<br><br>Example: `May 27, 2020 @ 15:22:27.982`<br> | date |
| `message` | For log events the message field contains the log message, optimized for viewing in a log viewer.<br><br>For structured logs without an original message field, other fields can be concatenated to form a human-readable summary of the event.<br><br>If multiple messages exist, they can be combined into one message.<br><br>Example: `Hello World`<br> | text |


## Hosts fields [host-fields]

These fields must be mapped to display host data in the {{infrastructure-app}}.

| Field | Description | Type |
| --- | --- | --- |
| `host.name` | Name of the host.<br><br>It can contain what `hostname` returns on Unix systems, the fully qualified domain name, or a name specified by the user. The sender decides which value to use.<br><br>Example: `MacBook-Elastic.local`<br> | keyword |
| `host.ip` | IP of the host that records the event. | ip |


## Docker container fields [docker-fields]

These fields must be mapped to display Docker container data in the {{infrastructure-app}}.

| Field | Description | Type |
| --- | --- | --- |
| `container.id` | Unique container id.<br><br>Example: `data`<br> | keyword |
| `container.name` | Container name. | keyword |
| `container.ip_address` | IP of the container.<br><br>*Not an ECS field*<br> | ip |


## Kubernetes pod fields [kubernetes-fields]

These fields must be mapped to display Kubernetes pod data in the {{infrastructure-app}}.

| Field | Description | Type |
| --- | --- | --- |
| `kubernetes.pod.uid` | Kubernetes Pod UID.<br><br>Example: `8454328b-673d-11ea-7d80-21010a840123`<br><br>*Not an ECS field*<br> | keyword |
| `kubernetes.pod.name` | Kubernetes pod name.<br><br>Example: `nginx-demo`<br><br>*Not an ECS field*<br> | keyword |
| `kubernetes.pod.ip` | IP of the Kubernetes pod.<br><br>*Not an ECS field*<br> | keyword |


## AWS EC2 instance fields [aws-ec2-fields]

These fields must be mapped to display EC2 instance data in the {{infrastructure-app}}.

| Field | Description | Type |
| --- | --- | --- |
| `cloud.instance.id` | Instance ID of the host machine.<br><br>Example: `i-1234567890abcdef0`<br> | keyword |
| `cloud.instance.name` | Instance name of the host machine. | keyword |
| `aws.ec2.instance.public.ip` | Instance public IP of the host machine.<br><br>*Not an ECS field*<br> | keyword |


## AWS S3 bucket fields [aws-s3-fields]

These fields must be mapped to display S3 bucket data in the {{infrastructure-app}}.

| Field | Description | Type |
| --- | --- | --- |
| `aws.s3.bucket.name` | The name or ID of the AWS S3 bucket.<br><br>*Not an ECS field*<br> | keyword |


## AWS SQS queue fields [aws-sqs-fields]

These fields must be mapped to display SQS queue data in the {{infrastructure-app}}.

| Field | Description | Type |
| --- | --- | --- |
| `aws.sqs.queue.name` | The name or ID of the AWS SQS queue.<br><br>*Not an ECS field*<br> | keyword |


## AWS RDS database fields [aws-rds-fields]

These fields must be mapped to display RDS database data in the {{infrastructure-app}}.

| Field | Description | Type |
| --- | --- | --- |
| `aws.rds.db_instance.arn` | Amazon Resource Name (ARN) for each RDS.<br><br>*Not an ECS field*<br> | keyword |
| `aws.rds.db_instance.identifier` | Contains a user-supplied database identifier. This identifier is the unique key that identifies a DB instance.<br><br>*Not an ECS field*<br> | keyword |


## Additional grouping fields [group-inventory-fields]

Depending on which entity you select in the **Infrastructure inventory** view, these additional fields can be mapped to group entities by.

| Field | Description | Type |
| --- | --- | --- |
| `cloud.availability_zone` | Availability zone in which this host is running.<br><br>Example: `us-east-1c`<br> | keyword |
| `cloud.machine.type` | Machine type of the host machine.<br><br>Example: `t2.medium`<br> | keyword |
| `cloud.region` | Region in which this host is running.<br><br>Example: `us-east-1`<br> | keyword |
| `cloud.instance.id` | Instance ID of the host machine.<br><br>Example: `i-1234567890abcdef0`<br> | keyword |
| `cloud.provider` | Name of the cloud provider. Example values are `aws`, `azure`, `gcp`, or `digitalocean`.<br><br>Example: `aws`<br> | keyword |
| `cloud.instance.name` | Instance name of the host machine. | keyword |
| `cloud.project.id` | Name of the project in Google Cloud.<br><br>*Not an ECS field*<br> | keyword |
| `service.type` | The type of service data is collected from.<br><br>The type can be used to group and correlate logs and metrics from one service type.<br><br>For example, the service type for metrics collected from {{es}} is `elasticsearch`.<br><br>Example: `elasticsearch`<br><br>*Not an ECS field*<br> | keyword |
| `host.hostname` | Name of the host. This field is required if you want to use {{ml-features}}<br><br>It normally contains what the `hostname` command returns on the host machine.<br><br>Example: `Elastic.local`<br> | keyword |
| `host.os.name` | Operating system name, without the version.<br><br>Multi-fields:<br><br>os.name.text (type: text)<br><br>Example: `Mac OS X`<br> | keyword |
| `host.os.kernel` | Operating system kernel version as a raw string.<br><br>Example: `4.4.0-112-generic`<br> | keyword |
