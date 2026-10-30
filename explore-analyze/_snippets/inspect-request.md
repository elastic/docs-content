The request **Inspector** is available in **Discover** and for all **Dashboards** visualization panels that are built from a query. The available information can differ based on the request.

1. Open the **Inspector**:
   - If you're in **Discover**:
      - {applies_to}`serverless:` {applies_to}`stack: ga 9.4` Hover over the active tab and select the {icon}`boxes_vertical` **Actions** icon, then select **Inspect**. You can also select **Inspect tab** from the application menu to inspect the active tab.
      - {applies_to}`stack: ga 9.0-9.3` Select **Inspect** from the application menu.
   - If you're in **Dashboards**, open the panel menu and select **Inspect**.
1. Open the **View** dropdown, then select **Requests**.
1. Several tabs with different information can appear, depending on nature of the request and your deployment type:
   :::{tip}
   Some visualizations rely on several requests. From the dropdown, select the request you want to inspect. 
   :::
    * **Statistics**: Provides general information and statistics about the request. For example, you can check if the number of hits and query time match your expectations. If not, this can indicate an issue with the request used to build the visualization.
    * **Clusters and shards**: Lists the {{es}} clusters and shards queried to fetch the data, including for [{{ccs}}](/explore-analyze/cross-cluster-search.md) queries. Use this tab to verify that the request ran correctly. This tab is not available for Vega visualizations. In {{serverless-short}}, this tab appears only when your project has no linked projects.
    * {applies_to}`serverless:` **Projects**: Replaces **Clusters and shards** when your project has linked projects for [{{cps}}](/explore-analyze/cross-project-search.md). Lists the projects the request searched, so you can check which projects your query reached. Each row shows the project's status, response time, provider, region, and tag count. Expand a row to see its shard breakdown. This tab is not available for Vega visualizations.
    * **Request**: Provides a full view of the visualization's request, which you can copy or **Open in Console** to refine, if needed.
    * **Response**: Provides a full view of the response returned by the request.
