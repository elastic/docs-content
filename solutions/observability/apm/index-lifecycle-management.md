---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-ilm-how-to.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
navigation_title: Index lifecycle management
---

# Index lifecycle management for APM indices [apm-ilm-how-to]

Lifecycle policies allow you to automate the lifecycle of your APM indices as they grow and age. A default policy is applied to each APM data stream, but can be customized depending on your business needs.

In the latest version of Elastic APM, clusters are managed by [index lifecycle management (ILM)](/manage-data/lifecycle/index-lifecycle-management.md) to provide the default data retention settings for APM data as well as allow customization for lifecycle.

::::{note}
Indices created in 8.15.x and 8.16.x might be managed by [data stream lifecycle (DSL)](/manage-data/lifecycle/data-stream.md). More details are available in [APM version 8.15](https://www.elastic.co/guide/en/observability/8.18/apm-release-notes-8.15.html). By default, new indices created in 8.17 are managed by ILM. More details are available in [APM version 8.17](https://www.elastic.co/guide/en/observability/8.18/apm-release-notes-8.17.html). If you have indices managed by DSL, any custom DSL settings that you specified will *not* automatically apply to the new indices managed by ILM. Instead, you can replicate custom DSL settings in ILM using this guide.

::::

## Default policies [index-lifecycle-policies-default]

Each APM data stream has its own default lifecycle policy including a delete definition and a rollover definition.

The table below describes the delete definition for each APM data stream. The delete phase permanently removes the index after a time threshold is met.

| Data stream | Delete after | Notes |
| --- | --- | --- |
| `traces-apm` | 10 days | Raw trace event data |
| `traces-apm.rum` | 90 days | Raw RUM trace event data, used in the UI |
| `logs-apm.error` | 10 days | Error event data |
| `logs-apm.app` | 10 days | Logs event data |
| `metrics-apm.app` | 90 days | Custom application specific metrics |
| `metrics-apm.internal` | 90 days | Common system metrics and language specific metrics (for example, CPU and memory usage) |
| `metrics-apm.service_destination_1m` | 90 days | Aggregated transaction metrics powering the Applications UI |
| `metrics-apm.service_destination_10m` | 180 days | Aggregated transaction metrics powering the Applications UI |
| `metrics-apm.service_destination_60m` | 390 days | Aggregated transaction metrics powering the Applications UI |
| `metrics-apm.service_summary_1m` | 90 days | Aggregated transaction metrics powering the Applications UI |
| `metrics-apm.service_summary_10m` | 180 days | Aggregated transaction metrics powering the Applications UI |
| `metrics-apm.service_summary_60m` | 390 days | Aggregated transaction metrics powering the Applications UI |
| `metrics-apm.service_transaction_1m` | 90 days | Aggregated transaction metrics powering the Applications UI |
| `metrics-apm.service_transaction_10m` | 180 days | Aggregated transaction metrics powering the Applications UI |
| `metrics-apm.service_transaction_60m` | 390 days | Aggregated transaction metrics powering the Applications UI |
| `metrics-apm.transaction_1m` | 90 days | Aggregated transaction metrics powering the Applications UI |
| `metrics-apm.transaction_10m` | 180 days | Aggregated transaction metrics powering the Applications UI |
| `metrics-apm.transaction_60m` | 390 days | Aggregated transaction metrics powering the Applications UI |

Rollover (writing to a new index) prevents a single index from growing too large and optimizes indexing and search performance. Rollover occurs after either an age or size metric is met.

::::{tip}
Default lifecycle policies can change between minor versions. This is not considered a breaking change as index management should continually improve and adapt to new features.
::::

## Configure a custom index lifecycle policy [apm-data-streams-custom-policy]

Mappings and settings for data streams can be customized through the creation of `*@custom` component templates, which are referenced by the index templates created by the {{es}} apm-data plugin. The easiest way to configure a custom index lifecycle policy per data stream is to edit this template.

This tutorial explains how to apply a custom index lifecycle policy to the `traces-apm` data stream.

## Step 1: View data streams [apm-data-streams-custom-one]

The **Data Streams** view in {{kib}} shows you data streams, index templates, and lifecycle policies:

1. Open the **Index Management** from the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Select **Data Streams**.
3. Search for `traces-apm` to see all data streams associated with APM trace data.
4. In this example, I only have one data stream because I’m only using the `default` namespace. You may have more if your setup includes multiple namespaces.

    :::{image} /solutions/images/observability-data-stream-overview.png
    :alt: Data streams info
    :screenshot:
    :::

## Step 2: Create an index lifecycle policy [apm-data-streams-custom-two]

1. Open the **Lifecycle Policies** management page from the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Click **Create policy**.

Name your new policy; For this tutorial, I’ve chosen `custom-traces-apm-policy`. Customize the policy to your liking, and when you’re done, click **Save policy**.

## Step 3: Apply the index lifecycle policy [apm-data-streams-custom-three]

To apply your new index lifecycle policy to the `traces-apm-*` data stream, edit the `<data-stream-name>@custom` component template.

1. Click on the **Component Template** tab and search for `traces-apm`.
2. Select the `traces-apm@custom` template and click **Manage** → **Edit**.
3. Under **Index settings**, set the {{ilm-init}} policy name created in the previous step:

    ```json
    {
      "lifecycle": {
        "name": "custom-traces-apm-policy",
        "prefer_ilm": true
      }
    }
    ```

4. Continue to **Review** and ensure your request looks similar to the image below. If it does, click **Create component template**.

    :::{image} /solutions/images/observability-create-component-template.png
    :alt: Create component template
    :screenshot:
    :::

## Step 4: Roll over the data stream (optional) [apm-data-streams-custom-four]

To confirm that the data stream is now using the new index template and {{ilm-init}} policy, you can either repeat [step one](#apm-data-streams-custom-one), or navigate to **{{dev-tools-app}}** and run the following:

```bash
GET /_data_stream/traces-apm-default <1>
```

1. The name of the data stream we’ve been hacking on appended with your <namespace>

The result should include the following:

```json
{
  "data_streams" : [
    {
      ...
      "template" : "traces-apm-default", <1>
      "ilm_policy" : "custom-traces-apm-policy", <2>
      ...
    }
  ]
}
```

1. The name of the custom index template created in step three
2. The name of the {{ilm-init}} policy applied to the new component template in step two

New {{ilm-init}} policies only take effect when new indices are created, so you either must wait for a rollover to occur (usually after 30 days or when the index size reaches 50 GB), or force a rollover using the [{{es}} rollover API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-rollover):

```bash
POST /traces-apm-default/_rollover/
```

## Namespace-level index lifecycle policies [apm-data-streams-custom-policy-namespace]

It is also possible to create more granular index lifecycle policies that apply to individual namespaces. This process is similar to the tutorial, but includes cloning the original index template(s) and using the index lifecycle you've created in the cloned template(s).

**Use case:** Use cloned index templates only in situations where you need to add namespace-specific customizations to a data stream.

:::{important}
- Cloning index templates is extremely risky because cloned templates are not automatically updated when you upgrade to a new product version. Users may find themselves in situations where their configurations are outdated because cloned templates are being used instead of the latest templates. <br><br>
Any customization done using cloned index templates must be repeated _every time_ you upgrade to a new version.

- Do not edit built-in index templates, add extra component templates, or change template order. Interfering with templates can disrupt how APM data is processed.

:::
