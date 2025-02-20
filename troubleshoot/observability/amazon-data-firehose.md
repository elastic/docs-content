---
navigation_title: "Amazon Data Firehose"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-aws-firehose-troubleshooting.html
---



# Amazon Data Firehose [monitor-aws-firehose-troubleshooting]


You can use the monitoring tab in the Firehose console to ensure there are incoming records and the delivery success rate is 100%. By default Firehose also logs to a Cloudwatch log group with the name `/aws/kinesisfirehose/<delivery stream name>`, which is automatically created when the delivery stream is created. Two log streams, `DestinationDelivery` and `BackupDelivery`, are created in this log group.

The backup settings in the delivery stream specify how failed delivery requests are handled. For more details on how to configure backups to S3, refer to [Step 3: Specify the destination settings for your Firehose stream](../../solutions/observability/cloud/monitor-amazon-web-services-aws-with-amazon-data-firehose.md#firehose-step-three).


## Scaling [aws-firehose-troubleshooting-scaling]

Firehose can [automatically scale](https://docs.aws.amazon.com/firehose/latest/dev/limits.md) to handle very high throughput. If your Elastic deployment is not properly configured for the data volume coming from Firehose, it could cause a bottleneck, which may lead to increased ingest times or indexing failures.

There are several facets to optimizing the underlying Elasticsearch performance, but Elastic Cloud provides several ready-to-use hardware profiles which can provide a good starting point. Other factors which can impact performance are [shard sizing](../../deploy-manage/production-guidance/optimize-performance/size-shards.md), [indexing configuration](../../deploy-manage/production-guidance/optimize-performance/indexing-speed.md), and [index lifecycle management (ILM)](../../manage-data/lifecycle/index-lifecycle-management.md).


## Support [aws-firehose-troubleshooting-support]

If you encounter further problems, please [contact us]](/troubleshoot/index.md#contact-us).

