---
navigation_title: Manage data from integrations
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Manage data from integrations [ilm-manage-data-from-integrations]

An [Elastic integration](https://docs.elastic.co/en/integrations) is a pre-packaged collection of assets that provides an effective way to monitor a product, system, or service, with minimal required setup.

When you install an integration, the [data streams](/manage-data/data-store/data-streams.md) associated with it are managed automatically by a default ILM policy. 

To view or adjust how your integration data is managed, a first step is to find the data streams associated with it. One approach is to start with an integration daashboard in {{kib}} to find the sets of data for which you'd like to customize the data lifecycle. A second approach is to start from the installed integration to view the assets associated with it.

::::{dropdown} Find the data stream for a {{kib}} visualation
To find the data stream associated with a visualization in {{kib}}:

1. Open **Dashboards** in {{kib}} and select a dashboard. For example, with the [System integration](integration-docs://reference/system.md) installed, you can open the `[Metrics System] Host overview` dashboard to find visualizations about the system being monitored.

1. On the dashboard, hover over a visualization and click the **Explore in Discover** icon.

    ![Explore in discover](/manage-data/images/ilm-explore-in-discover.png "")

1. In **Discover**, select a document and click the **Toggle dialog with details** icon.

    ![Toggle dialog with details](/manage-data/images/ilm-toggle-document-details.png "")

1. Note that there are three `data_stream` fields: `data_stream.dataset`, `data_stream.namespace`, and `data_stream.type`.

    ![Toggle dialog with details](/manage-data/images/ilm-document-data-stream.png "")

    The full data stream name is composed of the following fields, separated by a hyphen:

    `data_stream.type`
    :   The general type of data, such as `logs`, `metrics`, `traces`, or `synthetics`

    `data_stream.dataset`
    :   The specific type of data. For example, metrics fields in the System integration include `system.cpu`, `system.diskio`, `system.network`, and others.
   
    `data_stream.namespace`
    :   A user-configurable arbitrary grouping, such as an environment (`dev`, `prod`, or `qa`). 
   
    For example, in the System integration, the **CPU usage over time** visualization is associated with the `metrics-system.cpu-default` data stream. 
::::

::::{dropdown} Find the data streams for integration assets
To find the data streams associated with an installed integration:

1. Go to **Integrations > Installed integrations** and select an integration.

1. Open the **Assets** tab and expand **Index templates**

   In the list of [index templates](/manage-data/data-store/templates.md), each template name matches the `data_stream.type` and `data_stream.dataset` of an associated data stream. For example, the `metrics-system.cpu` template 
::::

After you've identified the data stream associated with the data that you'd like to manage, you can [view its current lifecycle status](/manage-data/lifecycle/index-lifecycle-management/policy-view-status.md), including details about its associated ILM policy. You can then follow our tutorial to [customize the built-in ILM policy](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md) to configure how the data is managed over time.
