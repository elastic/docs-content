---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/gcp-dataflow.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
---

# GCP Dataflow templates [gcp-dataflow]

In this tutorial, you’ll learn how to ship logs directly from the Google Cloud Console with the Dataflow template for analyzing GCP Audit Logs in the {{stack}}.


## What you’ll learn [_what_youll_learn_3]

You’ll learn how to:

* Export GCP audit logs through Pub/Sub topics and subscriptions.
* Ingest logs using [Google Dataflow](https://cloud.google.com/dataflow) and view those logs in {{kib}}.


## Before you begin [_before_you_begin_3]

Create an [{{ech}}](https://cloud.elastic.co/registration?page=docs&placement=docs-body) deployment. The deployment includes an {{es}} cluster for storing and searching your data, and {{kib}} for visualizing and managing your data.


## Step 1: Install the GCP integration [_step_1_install_the_gcp_integration]

You’ll start with installing the Elastic GCP integration to add pre-built dashboards, ingest node configurations, and other assets that help you get the most of the GCP logs you ingest.

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for `gcp`.

    :::{image} /solutions/images/observability-monitor-gcp-kibana-integrations.png
    :alt: {{kib}} integrations
    :::

3. Click the Elastic Google Cloud Platform (GCP) integration to see more details about it, then click **Add Google Cloud Platform (GCP)**.

    :::{image} /solutions/images/observability-monitor-gcp-integration.png
    :alt: GCP integration
    :::

4. Click **Save integration**.

:::::{note}
This tutorial assumes the Elastic cluster is already running. To continue, you’ll need your **Cloud ID** and an **API Key**.

To find the Cloud ID of your [deployment](https://cloud.elastic.co/deployments), go to the deployment’s **Overview** page.

![Cloud ID](/solutions/images/observability-monitor-gcp-cloud-id.png "")

Use [{{kib}}](/deploy-manage/api-keys/elasticsearch-api-keys.md#create-api-key) to create a Base64-encoded API key to authenticate on your deployment.

::::{important}
You can optionally restrict the privileges of your API Key; otherwise they’ll be a point in time snapshot of permissions of the authenticated user. For this tutorial the data is written to the `logs-gcp.audit-default` data streams.

::::


:::::



## Step 2: Create a Pub/Sub topic and subscription [_step_2_create_a_pubsub_topic_and_subscription]

Before configuring the Dataflow template, create a Pub/Sub topic and subscription from your Google Cloud Console where you can send your logs from Google Operations Suite. There are three available filesets: `audit`, `vpcflow`, `firewall`. This tutorial covers the `audit` fileset.

1. Go to the **Logs Router** page to configure GCP to export logs to a Pub/Sub topic. Use the search bar to find the page:

    :::{image} /solutions/images/observability-monitor-gcp-navigate-logs-router.png
    :alt: Navigate to Logs Router page
    :::

    To set up the logs routing sink, click  **Create sink**. Set **sink name** as `monitor-gcp-audit-sink`. Select the **Cloud Pub/Sub topic** as the **sink service** and **Create new Cloud Pub/Sub topic** named `monitor-gcp-audit`:

    :::{image} /solutions/images/observability-monitor-gcp-create-pubsub-topic.png
    :alt: Create Pub/Sub topic
    :::

    Finally, under **Choose logs to include in sink**, add `logName:"cloudaudit.googleapis.com"` (it includes all audit logs). Click **create sink**.  It will look something like the following:

    :::{image} /solutions/images/observability-monitor-gcp-create-sink.png
    :alt: Create logs routing sink
    :::

2. Now go to the **Pub/Sub** page to add a subscription to the topic you just created. Use the search bar to find the page:

    :::{image} /solutions/images/observability-monitor-gcp-pub-sub.png
    :alt: GCP Pub/Sub
    :::

    To add a subscription to the `monitor-gcp-audit` topic click **Create subscription**:

    :::{image} /solutions/images/observability-monitor-gcp-pub-sub-create-subscription.png
    :alt: Create GCP Pub/Sub Subscription
    :::

    Set `monitor-gcp-audit-sub` as the **Subscription ID** and leave the **Delivery type** as pull:

    :::{image} /solutions/images/observability-monitor-gcp-pub-sub-subscription-id.png
    :alt: GCP Pub/Sub Subscription ID
    :::

    Finally, scroll down and click **Create**.



## Step 3: Configure the Google Dataflow template [_step_3_configure_the_google_dataflow_template]

After creating a Pub/Sub topic and subscription, go to the **Dataflow Jobs** page and configure your template to use them. Use the search bar to find the page:

:::{image} /solutions/images/observability-monitor-gcp-dataflow-jobs.png
:alt: GCP Dataflow Jobs
:::

To create a job, click **Create Job From Template**. Set **Job name** as `auditlogs-stream` and select `Pub/Sub to Elasticsearch` from the **Dataflow template** dropdown menu:

:::{image} /solutions/images/observability-monitor-gcp-dataflow-pub-sub-elasticsearch.png
:alt: GCP Dataflow Pub/Sub to {{es}}
:::

Before running the job, fill in required parameters:

:::{image} /solutions/images/observability-monitor-gcp-dataflow-required-parameters.png
:alt: GCP Dataflow Required Parameters
:::

::::{note}
For **Cloud Pub/Sub subscription**, use the subscription you created in the previous step. For **Cloud ID** and **Base64-encoded API Key**, use the values you got earlier. If you don’t have an **Error output topic**, create one like you did in the previous step.

::::


After filling the required parameters, click **Show Optional Parameters** and add `audit` as the log type parameter.

:::{image} /solutions/images/observability-monitor-gcp-dataflow-optional-parameters.png
:alt: GCP Dataflow Optional Parameters
:::

When you are all set, click **Run Job** and wait for Dataflow to execute the template, which takes a few minutes.

Finally, navigate to {{kib}} to see your logs parsed and visualized in the **[Logs GCP] Audit** dashboard.

:::{image} /solutions/images/observability-monitor-gcp-dataflow-audit-dashboard.png
:alt: GCP audit overview dashboard
:::

Besides collecting audit logs from your Google Cloud Platform, you can also use Dataflow integrations to ingest data directly into Elastic from [Google BigQuery](https://www.elastic.co/blog/ingest-data-directly-from-google-bigquery-into-elastic-using-google-dataflow) and [Google Cloud Storage](https://www.elastic.co/blog/ingest-data-directly-from-google-cloud-storage-into-elastic-using-google-dataflow).
