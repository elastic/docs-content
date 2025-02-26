---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/metrics-app-fields.html
---

# Infrastructure app fields [metrics-app-fields]

This section lists the required fields the {{infrastructure-app}} uses to display data. Please note that some of the fields listed are not [ECS fields](ecs://docs/reference/index.md#_what_is_ecs).


## Additional field details [_additional_field_details]

The `event.dataset` field is required to display data properly in some views. This field is a combination of `metricset.module`, which is the {{metricbeat}} module name, and `metricset.name`, which is the metricset name.

To determine each metric’s optimal time interval, all charts use `metricset.period`. If `metricset.period` is not available, then it falls back to 1 minute intervals.


## Base fields [base-fields]

The `base` field set contains all fields which are on the top level. These fields are common across all types of events.

`@timestamp`
:   Date/time when the event originated.

    This is the date/time extracted from the event, typically representing when the source generated the event. If the event source has no original timestamp, this value is typically populated by the first time the pipeline received the event. Required field for all events.

    type: date

    required: True

    ECS field: True

    example: `May 27, 2020 @ 15:22:27.982`


`message`
:   For log events the message field contains the log message, optimized for viewing in a log viewer.

    For structured logs without an original message field, other fields can be concatenated to form a human-readable summary of the event.

    If multiple messages exist, they can be combined into one message.

    type: text

    required: True

    ECS field: True

    example: `Hello World`



## Hosts fields [host-fields]

These fields must be mapped to display host data in the {{infrastructure-app}}.

`host.name`
:   Name of the host.

    It can contain what `hostname` returns on Unix systems, the fully qualified domain name, or a name specified by the user. The sender decides which value to use.

    type: keyword

    required: True

    ECS field: True

    example: `MacBook-Elastic.local`


`host.ip`
:   IP of the host that records the event.

    type: `ip`

    required: True

    ECS field: True



## Docker container fields [docker-fields]

These fields must be mapped to display Docker container data in the {{infrastructure-app}}.

`container.id`
:   Unique container id.

    type: keyword

    required: True

    ECS field: True

    example: `data`


`container.name`
:   Container name.

    type: keyword

    required: True

    ECS field: True


`container.ip_address`
:   IP of the container.

    type: `ip`

    required: True

    ECS field: False



## Kubernetes pod fields [kubernetes-fields]

These fields must be mapped to display Kubernetes pod data in the {{infrastructure-app}}.

`kubernetes.pod.uid`
:   Kubernetes Pod UID.

    type: keyword

    required: True

    ECS field: False

    example: `8454328b-673d-11ea-7d80-21010a840123`


`kubernetes.pod.name`
:   Kubernetes pod name.

    type: keyword

    required: True

    ECS field: False

    example: `nginx-demo`


`kubernetes.pod.ip`
:   IP of the Kubernetes pod.

    type: keyword

    required: True

    ECS field: False



## AWS EC2 instance fields [aws-ec2-fields]

These fields must be mapped to display EC2 instance data in the {{infrastructure-app}}.

`cloud.instance.id`
:   Instance ID of the host machine.

    type: keyword

    required: True

    ECS field: True

    example: `i-1234567890abcdef0`


`cloud.instance.name`
:   Instance name of the host machine.

    type: keyword

    required: True

    ECS field: True


`aws.ec2.instance.public.ip`
:   Instance public IP of the host machine.

    type: keyword

    required: True

    ECS field: False



## AWS S3 bucket fields [aws-s3-fields]

These fields must be mapped to display S3 bucket data in the {{infrastructure-app}}.

`aws.s3.bucket.name`
:   The name or ID of the AWS S3 bucket.

    type: keyword

    required: True

    ECS field: False



## AWS SQS queue fields [aws-sqs-fields]

These fields must be mapped to display SQS queue data in the {{infrastructure-app}}.

`aws.sqs.queue.name`
:   The name or ID of the AWS SQS queue.

    type: keyword

    required: True

    ECS field: False



## AWS RDS database fields [aws-rds-fields]

These fields must be mapped to display RDS database data in the {{infrastructure-app}}.

`aws.rds.db_instance.arn`
:   Amazon Resource Name (ARN) for each RDS.

    type: keyword

    required: True

    ECS field: False


`aws.rds.db_instance.identifier`
:   Contains a user-supplied database identifier. This identifier is the unique key that identifies a DB instance.

    type: keyword

    required: True

    ECS field: False



## Additional grouping fields [group-inventory-fields]

Depending on which entity you select in the **Infrastructure inventory** view, these additional fields can be mapped to group entities by.

`cloud.availability_zone`
:   Availability zone in which this host is running.

    type: keyword

    required: True

    ECS field: True

    example: `us-east-1c`


`cloud.machine.type`
:   Machine type of the host machine.

    type: keyword

    required: True

    ECS field: True

    example: `t2.medium`


`cloud.region`
:   Region in which this host is running.

    type: keyword

    required: True

    ECS field: True

    example: `us-east-1`


`cloud.instance.id`
:   Instance ID of the host machine.

    type: keyword

    required: True

    ECS field: True

    example: `i-1234567890abcdef0`


`cloud.provider`
:   Name of the cloud provider. Example values are `aws`, `azure`, `gcp`, or `digitalocean`.

    type: keyword

    required: True

    ECS field: True

    example: `aws`


`cloud.instance.name`
:   Instance name of the host machine.

    type: keyword

    required: True

    ECS field: True


`cloud.project.id`
:   Name of the project in Google Cloud.

    type: keyword

    required: True

    ECS field: False


`service.type`
:   The type of the service data is collected from.

    The type can be used to group and correlate logs and metrics from one service type.

    Example: If metrics are collected from {{es}}, service.type would be `elasticsearch`.

    type: keyword

    required: True

    ECS field: False

    example: `elasticsearch`


`host.hostname`
:   Name of the host.

    It normally contains what the `hostname` command returns on the host machine.

    type: keyword

    required: True, if you want to use the {{ml-features}}.

    ECS field: True

    example: `Elastic.local`


`host.os.name`
:   Operating system name, without the version.

    Multi-fields:

    * os.name.text (type: text)

        type: keyword

        required: True

        ECS field: True

        example: `Mac OS X`


`host.os.kernel`
:   Operating system kernel version as a raw string.

    type: keyword

    required: True

    ECS field: True

    example: `4.4.0-112-generic`


