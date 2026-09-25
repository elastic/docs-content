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

You also need a destination dashboard.

The following panel types support dashboard drilldowns:

* **Visualizations that use a data view**
* {applies_to}`serverless:` {applies_to}`stack: ga 9.4` **Visualizations based on an {{esql}} query**
* **Vega** visualizations
* **Maps**
* **TSVB**
* **Aggregation-based**
* **Timelion**

For a computed value, including an {{esql}} result, refer to [How a drilldown uses the selected value](drilldowns.md#drilldowns-requirements).

## Set up the origin and destination dashboards [_create_and_set_up_the_dashboards_you_want_to_connect]

This example creates a dashboard and a dashboard drilldown. Follow it with the sample data, or use your own dashboard and data.

1. Add the [**Sample web logs**](/manage-data/ingest/sample-data.md) data. This also adds the **[Logs] Web Traffic** dashboard.
2. Create a new dashboard.

    * {applies_to}`serverless:` {applies_to}`stack: ga 9.2+` In the application menu, select **Add** → **From library**.
    * {applies_to}`stack: ga 9.0-9.1` In the application menu, select **Add from library**.

3. Add the **[Logs] Visits** panel.
4. Set the [time filter](../query-filter/filtering.md) to **Last 30 days**, or to a 30-day period that contains data, depending on when you installed the sample data.
5. Save the dashboard. In the **Title** field, enter `Detailed logs`.
6. Open the **[Logs] Web Traffic** dashboard, then set a search and a filter.

    [Search](using.md#_filter_dashboards_using_the_kql_query_bar): `extension.keyword: ("gz" or "css" or "deb")`<br> [Filter](using.md#_add_pills_using_the_filter_editor): `geo.src: US`

## Create the drilldown [_create_the_dashboard_drilldown]

Create a drilldown that opens the **Detailed logs** dashboard from the **[Logs] Web Traffic** dashboard.

1. On the **[Logs] Web Traffic** dashboard, select **Edit**.
2. Hover over the **[Logs] Errors by host** panel, open the {icon}`boxes_vertical` panel menu, then select {icon}`plus_in_circle` **Create drilldown**.
3. Select **Go to dashboard**.

    1. In **Name**, enter a name. For example, `View details`.
    2. From **Choose destination dashboard**, select **Detailed logs**.
    3. To keep the `geo.src` filter, the KQL query, and the time filter, select **Use filters and query from origin dashboard** and **Use date range from origin dashboard**.
    4. Select **Create drilldown**.

4. Save the dashboard.
5. On the **[Logs] Errors by host** table, select **+** on a value, then select **View details**.

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
