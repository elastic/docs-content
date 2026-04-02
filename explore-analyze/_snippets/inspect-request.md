The request **Inspector** is available in **Discover** and for all **Dashboards** visualization panels that are built from a query. The available information can differ based on the request.

1. Open the **Inspector**:
   - If you're in **Discover**, select **Inspect** from the application's toolbar.
   - If you're in **Dashboards**, open the panel menu and select **Inspect**.
1. Open the **View** dropdown, then select **Requests**.
1. Several tabs with different information can appear, depending on nature of the request:
   :::{tip}
   Some visualizations rely on several requests. From the dropdown, select the request you want to inspect. 
   :::
    * **Statistics**: Provides general information and statistics about the request. For example, you can check if the number of hits and query time match your expectations. If not, this can indicate an issue with the request used to build the visualization.
    * **Clusters and shards**: Lists the {{es}} clusters and shards per cluster queried to fetch the data and shows the status of the request on each of them. With the information in this tab, you can check if the request is properly executed, especially in case of cross-cluster search.

      :::{note}
      This tab is not available for {{esql}} queries and Vega visualizations.
      :::
      
    * **Request**: Provides a full view of the visualization's request, which you can copy or **Open in Console** to refine, if needed.
    * **Response**: Provides a full view of the response returned by the request.