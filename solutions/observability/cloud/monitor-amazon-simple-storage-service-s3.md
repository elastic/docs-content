---
navigation_title: S3
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-amazon-s3.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---



# Monitor Amazon Simple Storage Service (S3) [monitor-amazon-s3]


[Amazon Simple Storage Service (S3)](https://aws.amazon.com/s3/) is a highly available object storage service that provides durability, security, and scalability. To store data, you create one or more buckets that contain objects. An object consists of a file and optional metadata that describes the file. For each bucket, you can control access to it.

Like most AWS services, Amazon S3 and Amazon CloudWatch are integrated so you can collect, view, and analyze CloudWatch metrics for your S3 buckets to help understand and improve the performance of applications that use Amazon S3. The Elastic [Amazon S3 integration](https://docs.elastic.co/en/integrations/aws/s3) collects metrics from Amazon CloudWatch using {{agent}}.

With the Amazon S3 integration, you can collect these S3 metrics from CloudWatch:

* Daily storage metrics for buckets. Use these metrics to monitor bucket storage. These metrics are reported once per day by default and are provided to AWS customers at no additional cost.
* Request metrics. Use these metrics to quickly identify and act on operational issues. These request metrics are available at one-minute intervals after some latency for processing, and they are not enabled by default.


## Get started [get-started-s3]

If you plan to collect request metrics, enable them for the S3 buckets you want to monitor. To learn how, refer to the [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/configure-request-metrics-bucket.html).

To collect S3 metrics, you typically need to install the Elastic [Amazon S3 integration](https://docs.elastic.co/en/integrations/aws/s3) and deploy an {{agent}} locally or on an EC2 instance.

Expand the **quick guide** to learn how, or skip to the next section if your data is already in {{es}}.

:::::{dropdown} Quick guide: Add data
1. In the Observability UI, find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the query bar, search for and select the **Amazon S3** integration.
3. Read the overview to make sure you understand integration requirements and other considerations.
4. Click **Add Amazon S3**.

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


{{agent}} is currently the preferred way to add S3 metrics. For other ways, refer to [Adding data to {{es}}](/manage-data/ingest.md).


## Dashboards [dashboard-s3]

{{kib}} provides a full data analytics platform with out-of-the-box dashboards that you can clone and enhance to satisfy your custom visualization use cases. For example, to see an overview of your S3 metrics in {{kib}}, go to the **Dashboard** app and navigate to the **[Metrics AWS] S3 Overview** dashboard.

:::{image} /solutions/images/observability-s3-dashboard.png
:alt: Screenshot showing the S3 dashboard
:screenshot:
:::


## Metrics to watch [_metrics_to_watch_2]

Here are the key metrics that you should watch, organized by category. For a full list of fields exported by the integration, refer to the [Amazon S3 integration](https://docs.elastic.co/en/integrations/aws/s3) docs.

* Daily storage metrics for buckets

    * `aws.s3_daily_storage.number_of_objects`
    * `aws.s3_daily_storage.bucket.size.bytes`

* Request metrics

    * `aws.s3_request.requests.total`
    * `aws.s3_request.requests.get`
    * `aws.s3_request.requests.put`
    * `aws.s3_request.requests.delete`
    * `aws.s3_request.requests.head`
    * `aws.s3_request.requests.post`
    * `aws.s3_request.requests.select`
    * `aws.s3_request.requests.list`
    * `aws.s3_request.requests.select_scanned.bytes`
    * `aws.s3_request.requests.select_returned.bytes`
    * `aws.s3_request.downloaded.bytes`
    * `aws.s3_request.uploaded.bytes`
    * `aws.s3_request.downloaded.bytes_per_period`
    * `aws.s3_request.uploaded.bytes_per_period`
    * `aws.s3_request.errors.4xx`
    * `aws.s3_request.errors.5xx`
    * `aws.s3_request.latency.first_byte.ms`
    * `aws.s3_request.latency.total_request.ms`
