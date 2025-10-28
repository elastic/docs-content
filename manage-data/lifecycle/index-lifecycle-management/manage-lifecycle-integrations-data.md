---
navigation_title: Manage the lifecycle policy for integrations data
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Manage the lifecycle policy for integrations data [ilm-manage-lifecycle-policy-integrations-data]

An Elastic integration is a pre-packaged collection of assets that provides an effective, simplified way to monitor a product, system, or service, with minimal required setup. Most integrations rely on {{agent}} as an ingest mechanism, and the policies used to govern installed integrations are managed in {{fleet}}.

You can find installation and configuration details for all integrations in the [Elastic integrations](https://docs.elastic.co/en/integrations) chapter of the **Reference** section. To learn about managing your installed integrations, refer to [Manage Elastic Agent integrations](/reference/fleet/manage-integrations.md) in the {{fleet}} and {{agent}} chapter of the **Reference** section.

When you install an integration, an [{{ilm}}](/manage-data/lifecycle/index-lifecycle-management.md) ({{ilm-init}}) policy is configured automatically to manage the integration's component [data streams](/manage-data/data-store/data-streams.md) and their backing indices. To view or adjust how your integration data is managed, a first step is to find the data streams that you're interested in. There are a few ways to do this:

::::{dropdown} Find the data stream for a {{kib}} visualization
To find the data stream associated with a visualization in a {{kib}}:

1. Open **Dashboards** from the {{kib}} menu and select a dashboard to view. For example, with the [System integration](integration-docs://reference/system.md) installed, you can open the `[Metrics System] Host overview` dashboard to find visualizations about the host system being monitored.

1. Hover over any visualization and click the **Explore in Discover** icon.

    ![Explore in discover](/manage-data/images/ilm-explore-in-discover.png "")

1. In **Discover**, the list of documents shows the columns for fields applicable to the visualzation that you selected. Select any document that has data for those fields and click the **Toggle dialog with details** icon.

    ![Discover documents list](/manage-data/images/ilm-toggle-document-details.png "")

1. In the document details, note that there are three `data_stream` fields. The full [data stream name](/reference/fleet/data-streams.md#data-streams-naming-scheme) is a composite of `data_stream.type`, `data_stream.dataset` and `data_stream.namespace`, separated by a hyphen. For example, in the System integration, the **CPU usage over time** visualization is associated with the `metrics-system.cpu-default` data stream.

    You can also see the data stream's current backing index, as well as other information such as the document timestamp and details about the agent that ingested the data.

    ![Document details](/manage-data/images/ilm-document-data-stream.png "")
::::

::::{dropdown} Find the data streams for an integration
To find the data streams associated with an installed integration:

1. In {{kib}} go to **Management > Integrations > Installed integrations** and select any integration.

1. Open the **Assets** tab and expand the **Index templates** list.

   In the list, the name of each [index template](/manage-data/data-store/templates.md) matches an associated data stream. For example, the `metrics-system.cpu` template matches the `metrics-system.cpu-default` data stream that is set up when the System integration is installed.

    ![Integration assets](/manage-data/images/ilm-integration-assets.png "")
::::

::::{dropdown} Find the data streams managed in {{fleet}}
To find all of the data streams that are managed in {{fleet}}:

1. In {{kib}}, go to the **{{fleet}}** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
1. Select the **Data streams** tab.

1. Use the search field and dropdown menus to filter the list. You can filter by the data stream type, dataset, namespace, or by the integration that the data stream belongs to.

    ![Integration assets](/manage-data/images/ilm-fleet-data-streams.png "")
::::

For any data stream that you're interested in, you can [view its current lifecycle status](/manage-data/lifecycle/index-lifecycle-management/policy-view-status.md), including details about its associated ILM policy.

After you've identified one or more data streams for which you'd like to customize how the data is managed over time, refer to our tutorials:

* For steps to modify {{ilm-init}} policies without changing the built-in defaults, try out the [](/manage-data/lifecycle/index-lifecycle-management/tutorial-customize-built-in-policies.md) tutorial in the data lifecycle documentation.
* For the steps to customize an ILM policy for a set of data streams, such as all logs or metrics data streams across all namespaces, across only a selected namespace, and others, check the set of tutorials in [Customize data retention policies](/reference/fleet/data-streams-ilm-tutorial.md) in the {{fleet}} and {{agent}} reference documentation.
