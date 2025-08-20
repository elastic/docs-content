---
navigation_title: Kinesis data streams
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-amazon-kinesis.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---



# Monitor Amazon Kinesis data streams [monitor-amazon-kinesis]


[Amazon Kinesis Data Streams](https://aws.amazon.com/kinesis/data-streams/) is a real-time data streaming service that you can use to capture, process, and store large amounts of data from a variety of sources, including websites, mobile applications, IoT devices, and more.

Amazon Kinesis Data Streams and Amazon CloudWatch are integrated so that you can collect and monitor CloudWatch metrics for your Kinesis data streams, such as tracking shard usage and recording related operations for each Kinesis data stream. The Elastic [Amazon Kinesis Data Stream integration](https://docs.elastic.co/en/integrations/aws/kinesis) collects metrics from Amazon CloudWatch using {{agent}}.

By default, Kinesis Data Streams sends stream-level (basic level) metrics to CloudWatch every minute automatically. There is also shard-level data (enhanced level) that is sent to CloudWatch every minute and incurs an additional cost per stream. To get shard-level data, you must specifically enable it for each stream by using the AWS Kinesis `enable-enhanced-monitoring` API. For example

```shell
aws kinesis enable-enhanced-monitoring --stream-name samplestream --shard-level-metrics ALL
```

For more details, refer to the [EnableEnhancedMonitoring](https://docs.aws.amazon.com/kinesis/latest/APIReference/API_EnableEnhancedMonitoring.html) documentation.


## Get started [get-started-kinesis]

To collect Kinesis data stream metrics from Amazon CloudWatch, you typically need to install the Elastic [Amazon Kinesis Data Stream integration](https://docs.elastic.co/en/integrations/aws/kinesis) and deploy an {{agent}}.

Expand the **quick guide** to learn how, or skip to the next section if your data is already in {{es}}.

:::::{dropdown} Quick guide: Add data
1. In the Observability UI, find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the query bar, search for and select the **Amazon Kinesis Data Stream** integration.
3. Read the overview to make sure you understand integration requirements and other considerations.
4. Click **Add Amazon Kinesis Data Stream**.

    ::::{tip}
    If you’re installing an integration for the first time, you may be prompted to install {{agent}}. If you see this page, click **Add integration only (skip agent installation)**.
    ::::

5. Configure the integration name and optionally add a description. Make sure you configure all required settings.
6. Choose where to add the integration policy.

    * If {{agent}} is not already deployed locally or on an EC2 instance, click **New hosts** and enter a name for the new agent policy.
    * Otherwise, click **Existing hosts** and select an existing agent policy.

7. Click **Save and continue**. This step takes a minute or two to complete. When it’s done, you’ll have an agent policy that contains an integration policy for the configuration you just specified. If an {{agent}} is already assigned to the policy, you’re done. Otherwise, you need to deploy an {{agent}}.
8. To deploy an {{agent}}:

    1. In the popup, click **Add {{agent}} to your hosts** to open the **Add agent** flyout. If you accidentally close the popup or the flyout doesn’t open, go to **{{fleet}} → Agents**, then click **Add agent** to access the flyout.
    2. Follow the steps in the **Add agent** flyout to download, install, and enroll the {{agent}}.

9. When incoming data is confirmed—after a minute or two—click **View assets** to access the dashboards.

For more information {{agent}} and integrations, refer to the [{{fleet}} and {{agent}} documentation](/reference/fleet/index.md).

::::


:::::


{{agent}} is currently the preferred way to add Kinesis data stream metrics. For other ways, refer to [Adding data to {{es}}](/manage-data/ingest.md).


## Dashboards [dashboard-kinesis]

{{kib}} provides a full data analytics platform with out-of-the-box dashboards that you can clone and enhance to satisfy your custom visualization use cases. For example, to see an overview of your Kinesis data streams in {{kib}}, go to the **Dashboard** app and navigate to the **[Metrics AWS] Kinesis Overview** dashboard.

:::{image} /solutions/images/observability-kinesis-dashboard.png
:alt: Screenshot showing the Kinesis overview dashboard
:screenshot:
:::


## Metrics to watch [metrics-to-watch-kinesis]

This section lists the key metrics that you should watch, organized by category. For a full description of fields exported by the integration, refer to the [Amazon Kinesis Data Stream integration](https://docs.elastic.co/en/integrations/aws/kinesis) docs.

* GetRecords

    * `aws.kinesis.metrics.GetRecords.Bytes.avg`
    * `aws.kinesis.metrics.GetRecords.IteratorAgeMilliseconds.avg`
    * `aws.kinesis.metrics.GetRecords.Latency.avg`
    * `aws.kinesis.metrics.GetRecords.Records.avg`
    * `aws.kinesis.metrics.GetRecords.Records.sum`
    * `aws.kinesis.metrics.GetRecords.Success.avg`
    * `aws.kinesis.metrics.GetRecords.Success.sum`
    * `aws.kinesis.metrics.ReadProvisionedThroughputExceeded.avg`
    * `aws.kinesis.metrics.IteratorAgeMilliseconds.avg`

* PutRecord

    * `aws.kinesis.metrics.PutRecord.Bytes.avg`
    * `aws.kinesis.metrics.PutRecord.Latency.avg`
    * `aws.kinesis.metrics.PutRecord.Success.avg`

* PutRecords

    * `aws.kinesis.metrics.PutRecords.Bytes.avg`
    * `aws.kinesis.metrics.PutRecords.Latency.avg`
    * `aws.kinesis.metrics.PutRecords.Success.avg`
    * `aws.kinesis.metrics.PutRecords.TotalRecords.sum`
    * `aws.kinesis.metrics.PutRecords.SuccessfulRecords.sum`
    * `aws.kinesis.metrics.PutRecords.FailedRecords.sum`
    * `aws.kinesis.metrics.PutRecords.ThrottleRecords.sum`
    * `aws.kinesis.metrics.WriteProvisionedThroughputExceeded.avg`

* Incoming and outgoing

    * `aws.kinesis.metrics.IncomingBytes.avg`
    * `aws.kinesis.metrics.IncomingRecords.avg`
    * `aws.kinesis.metrics.OutgoingBytes.avg`
    * `aws.kinesis.metrics.OutgoingRecords.avg`
    * `aws.kinesis.metrics.OutgoingRecords.sum`

* SubscribeToShard

    * `aws.kinesis.metrics.SubscribeToShard.RateExceeded.avg`
    * `aws.kinesis.metrics.SubscribeToShard.Success.avg`
    * `aws.kinesis.metrics.SubscribeToShardEvent.Bytes.avg`
    * `aws.kinesis.metrics.SubscribeToShardEvent.MillisBehindLatest.avg`
    * `aws.kinesis.metrics.SubscribeToShardEvent.Success.avg`
    * `aws.kinesis.metrics.SubscribeToShardEvent.Records.sum`
