---
navigation_title: Create a dashboard drilldown
description: Create a drilldown that opens another dashboard from a panel and carries the time range, filters, and query.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
type: how-to
---

# Create a dashboard drilldown [dashboard-drilldowns]

A dashboard drilldown opens another dashboard and can carry the time range, filters, and query with it. Use one to continue from a summary into a more specific view.

For example, a dashboard can show logs and metrics for several data centers. A drilldown can open a dashboard for the one data center or server you select.

Refer to [Drilldowns](drilldowns.md) to choose a drilldown type and to check values created at query time.

## Before you begin [create-dashboard-drilldown-requirements]

To create a dashboard drilldown, you need:

:::{include} _snippets/drilldown-access.md
:::

* A destination dashboard.

The following panel types support dashboard drilldowns:

* **Visualizations that use a data view**
* {applies_to}`serverless:` {applies_to}`stack: ga 9.4` **Visualizations based on an {{esql}} query**
* **Vega** visualizations
* **Maps**
* Legacy Kibana visualization types, such as **TSVB**, **Aggregation-based**, and **Timelion**

Some values cannot open a drilldown. For a value created at query time, refer to [How a drilldown uses the selected value](drilldowns.md#drilldowns-requirements).

## Create the drilldown [_create_the_dashboard_drilldown]

This example opens another dashboard from a panel. Follow it with the sample data, or use your own dashboards.

1. Add the [**Sample web logs**](/manage-data/ingest/sample-data.md) data. This also adds the **[Logs] Web Traffic** dashboard.
2. If you don't already have a dashboard to open from the panel, create one. This example uses a dashboard named **Detailed logs**.

    ::::{dropdown} Create the Detailed logs dashboard
    1. Create a new dashboard.

        * {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` In the application menu, select **Add** → **From library**.
        * {applies_to}`stack: ga 9.0-9.1` In the application menu, select **Add from library**.

    2. Add the **[Logs] Visits** panel.
    3. Save the dashboard. In the **Title** field, enter `Detailed logs`.
    ::::

3. Open the **[Logs] Web Traffic** dashboard and select **Edit**.
4. Set a search, a filter, and a time range for the drilldown to carry.

    [Search](using.md#_filter_dashboards_using_the_kql_query_bar): `extension.keyword: ("gz" or "css" or "deb")`<br> [Filter](using.md#_add_pills_using_the_filter_editor): `geo.src: US`<br> [Time filter](../query-filter/filtering.md): **Last 30 days**, or a 30-day period that contains data, depending on when you installed the sample data.

5. Hover over the **[Logs] Errors by host** panel, open the {icon}`boxes_vertical` panel menu, then select {icon}`plus_in_circle` **Create drilldown**.
6. Select **Go to dashboard**.

    1. In **Name**, enter a name. For example, `View details`.
    2. From **Choose destination dashboard**, select **Detailed logs**.
    3. To keep the `geo.src` filter, the KQL query, and the time filter, select **Use filters and query from origin dashboard** and **Use date range from origin dashboard**.
    4. Select **Create drilldown**.

7. Save the dashboard.
8. On the **[Logs] Errors by host** table, select **+** on a value, then select **View details**.

   :::{image} /explore-analyze/images/kibana-dashboard_drilldownOnPanel.png
   :alt: Drilldown on data table that navigates to another dashboard
   :screenshot:
   :::

The **Detailed logs** dashboard opens with the `geo.src` filter, the KQL query, and the time range you set.

## Next steps [create-dashboard-drilldown-next-steps]

* [Manage drilldowns](manage-drilldowns.md)

## Related pages [create-dashboard-drilldown-related-pages]

* [Drilldowns](drilldowns.md)
* [Create a URL drilldown](create-url-drilldown.md)
* [Create a Discover drilldown](create-discover-drilldown.md)
