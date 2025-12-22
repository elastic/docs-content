---
navigation_title: SQS
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/monitor-amazon-sqs.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---



# Monitor Amazon Simple Queue Service (SQS) [monitor-amazon-sqs]


[Amazon Simple Queue Service (SQS)](https://aws.amazon.com/sqs/) is a message queuing service that allows your application components to communicate asynchronously through messages, making it easier to decouple and scale microservices, distributed systems, and serverless applications.

AWS SQS and Amazon CloudWatch are integrated and therefore, you can collect, view, and analyze data. Metrics for Amazon SQS queues are automatically collected and pushed to CloudWatch at one-minute intervals.

You can view and analyze the queue’s metrics from the Amazon SQS console, the CloudWatch console, the AWS CLI, or by using the CloudWatch API.

The Elastic [Amazon SQS integration](https://docs.elastic.co/en/integrations/aws/sqs) collects metrics from Amazon CloudWatch using {{agent}}.


## Get started [get-started-sqs]

To collect SQS metrics, you typically need to install the Elastic [Amazon SQS integration](https://docs.elastic.co/en/integrations/aws/sqs) and deploy an {{agent}} locally or on an EC2 instance.

Expand the **quick guide** to learn how, or skip to the next section if your data is already in {{es}}.

:::::{dropdown} Quick guide: Add data
1. In the Observability UI, find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the query bar, search for and select the **Amazon SQS** integration.
3. Read the overview to make sure you understand integration requirements and other considerations.
4. Click **Add Amazon SQS**.

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


{{agent}} is currently the preferred way to add SQS metrics. For other ways, refer to [Adding data to {{es}}](/manage-data/ingest.md).


## Dashboards [dashboard-sqs]

For example, to see an overview of your SQS metrics in {{kib}}, go to the **Dashboard** app and navigate to the **[Metrics AWS] SQS Overview** dashboard.

:::{image} /solutions/images/observability-sqs-dashboard.png
:alt: Screenshot showing the SQS overview dashboard
:screenshot:
:::


## Metrics to watch [_metrics_to_watch_3]

Here are the key metrics that you should watch, organized by category. For a full list of fields exported by the integration, refer to the [Amazon SQS integration](https://docs.elastic.co/en/integrations/aws/sqs) docs.

* messages

    * `aws.sqs.messages.delayed`
    * `aws.sqs.messages.not_visible`
    * `aws.sqs.messages.visible`
    * `aws.sqs.messages.deleted`
    * `aws.sqs.messages.received`
    * `aws.sqs.messages.sent`
    * `aws.sqs.oldest_message_age.sec`
    * `aws.sqs.sent_message_size.bytes`

* queue

    * `aws.sqs.queue.name`
