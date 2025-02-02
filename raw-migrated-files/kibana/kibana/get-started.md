# Quick start [get-started]

To quickly get up and running with {{kib}}, set up on Cloud, then add a sample data set that you can explore and visualize.

When you’re done, you’ll know how to:

* [Explore the data with **Discover**.](../../../explore-analyze/overview/kibana-quickstart.md#explore-the-data)
* [Visualize the data with **Dashboard**.](../../../explore-analyze/overview/kibana-quickstart.md#view-and-analyze-the-data)


### Required privileges [_required_privileges]

You must have `read`, `write`, and `manage` privileges on the `kibana_sample_data_*` indices. Learn how to [secure access to {{kib}}](../../../deploy-manage/users-roles/cluster-or-deployment-auth/quickstart.md), or refer to [Security privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/elasticsearch-privileges.md) for more information.


## Set up on cloud [set-up-on-cloud]

There’s no faster way to get started than with our hosted {{ess}} on Elastic Cloud:

1. [Get a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
2. Log into [Elastic Cloud](https://cloud.elastic.co?page=docs&placement=docs-body).
3. Click **Create deployment**.
4. Give your deployment a name.
5. Click **Create deployment** and download the password for the `elastic` user.

That’s it! Now that you are up and running, it’s time to get some data into {{kib}}. {{kib}} will open as soon as your deployment is ready.


## Add sample data [gs-get-data-into-kibana]

Sample data sets come with sample visualizations, dashboards, and more to help you explore {{kib}} before you ingest or add your own data.

1. Open the **Integrations** page from the navigation menu or using the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).
2. In the list of integrations, select **Sample Data**.
3. On the page that opens, select **Other sample data sets**.
4. Install the sample data sets that you want.

Once installed, you can access the sample data in the various {{kib}} apps available to you.


## Explore the data [explore-the-data]

**Discover** displays the data in an interactive histogram that shows the distribution of data, or documents, over time, and a table that lists the fields for each document that matches the {{data-source}}. To view a subset of the documents, you can apply filters to the data, and customize the table to display only the fields you want to explore.

1. Go to **Discover**.
2. Change the [time filter](../../../explore-analyze/query-filter/filtering.md) to **Last 7 days**.

    :::{image} ../../../images/kibana-timeFilter_discover_8.4.0.png
    :alt: Time filter menu with Last 7 days filter configured
    :class: screenshot
    :::

3. To view the sales orders for women’s clothing that are $60 or more, use the [**KQL**](../../../explore-analyze/query-filter/languages/kql.md) search field:

    ```text
    products.taxless_price >= 60 and category : Women's Clothing
    ```

    :::{image} ../../../images/kibana-kql_discover_8.4.0.png
    :alt: Discover tables that displays only the orders for women's clothing that are $60 or more
    :class: screenshot
    :::

4. To view only the product categories that contain sales orders, hover over the **category** field, then click **+**.

    :::{image} ../../../images/kibana-availableFields_discover_8.4.0.png
    :alt: Discover table that displays only the product categories that contain orders
    :class: screenshot
    :::



## Visualize the data [view-and-analyze-the-data]

A dashboard is a collection of panels that you can use to visualize the data. Panels contain visualizations, interactive controls, text, and more.

1. Go to **Dashboards**.
2. Click **[eCommerce] Revenue Dashboard**.

    :::{image} ../../../images/kibana-dashboard_ecommerceRevenueDashboard_8.6.0.png
    :alt: The [eCommerce] Revenue Dashboard that comes with the Sample eCommerce order data set
    :class: screenshot
    :::



### Create a visualization panel [create-a-visualization]

Create a treemap visualization panel that shows the top sales regions and manufacturers, then add the panel to the dashboard.

1. In the toolbar, click **Edit**.
2. On the dashboard, click **Create visualization**.
3. In the drag-and-drop visualization editor, open the **Visualization type** dropdown, then select **Treemap**.

    :::{image} ../../../images/kibana-visualizationTypeDropdown_lens_8.4.0.png
    :alt: Chart type menu with Treemap selected
    :class: screenshot
    :::

4. From the **Available fields** list, drag the following fields to the workspace:

    * **geoip.city_name**
    * **manufacturer.keyword**

        :::{image} ../../../images/kibana-ecommerceTreemap_lens_8.4.0.png
        :alt: Treemap that displays Top values of geoip.city_name and Top values or manufacturer.keyword fields
        :class: screenshot
        :::

5. Click **Save and return**.

    The treemap appears as the last visualization panel on the dashboard.



### Interact with the data [interact-with-the-data]

You can interact with the dashboard data using controls that allow you to apply dashboard-level filters. Interact with the **[eCommerce] Controls** panel to view the women’s clothing data from the Gnomehouse manufacturer.

1. From the **Manufacturer** dropdown, select **Gnomehouse**.
2. From the **Category** dropdown, select **Women’s Clothing**.

    :::{image} ../../../images/kibana-sampleDataFilter_dashboard_8.6.0.png
    :alt: The [eCommerce] Revenue Dashboard that shows only the women's clothing data from the Gnomehouse manufacturer
    :class: screenshot
    :::



### Filter the data [filter-and-query-the-data]

To view a subset of the data, you can apply filters to the dashboard data. Apply a filter to view the women’s clothing data generated on Wednesday from the Gnomehouse manufacturer.

1. Click **Add filter**.

    :::{image} ../../../images/kibana-addFilter_dashboard_8.6.0.png
    :alt: The Add filter action that applies dashboard-level filters
    :class: screenshot
    :::

2. From the **Field** dropdown, select **day_of_week**.
3. From the **Operator** dropdown, select **is**.
4. From the **Value** dropdown, select **Wednesday**.

    :::{image} ../../../images/kibana-addFilterOptions_dashboard_8.6.0.png
    :alt: The Add filter options configured to display only the women's clothing data generated on Wednesday from the Gnomehouse manufacturer
    :class: screenshot
    :::

5. Click **Add filter**.

    :::{image} ../../../images/kibana-dashboard_sampleDataAddFilter_8.6.0.png
    :alt: The [eCommerce] Revenue Dashboard that shows only the women's clothing data generated on Wednesday from the Gnomehouse manufacturer
    :class: screenshot
    :::



## What’s next? [quick-start-whats-next]

**Add your own data.** Ready to add your own data? Go to [Get started with Elastic Observability](../../../solutions/observability/get-started.md), or go to [Add data to {{kib}}](../../../manage-data/ingest.md) and learn about all the ways you can add data.

**Explore your own data in Discover.** Ready to learn more about exploring your data in **Discover**? Go to [Discover](../../../explore-analyze/discover.md).

**Create a dashboard with your own data.** Ready to learn more about visualizing your data on a **Dashboard**? Go to [Dashboard](../../../explore-analyze/dashboards.md).

**Try out the {{ml-features}}.** Ready to analyze the sample data sets and generate models for its patterns of behavior? Go to [Getting started with {{ml}}](../../../explore-analyze/machine-learning/anomaly-detection/ml-getting-started.md).
