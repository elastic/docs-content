---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/esql-visualizations.html
---

# ES|QL [esql-visualizations]

You can add ES|QL visualizations to a dashboard directly from queries in Discover, or you can start from a dashboard.


## Edit and add from Discover [_edit_and_add_from_discover]

In Discover, [typing ES|QL queries](../query-filter/languages/esql-kibana.md) automatically shows a visualization. The visualization type depends on the content of the query: histogram, bar charts, etc. You can manually make changes to that visualization and edit its type and display options using the pencil button ![pencil button](../../images/kibana-esql-icon-edit-visualization.svg "").

You can then **Save** and add it to an existing or a new dashboard using the save button of the visualization ![save button](../../images/kibana-esql-icon-save-visualization.svg "").


## Create from dashboard [_create_from_dashboard]

1. From your dashboard, select **Add panel**.
2. Choose **ES|QL** under **Visualizations**. An ES|QL editor appears and lets you configure your query and its associated visualization. The **Suggestions** panel can help you find alternative ways to configure the visualization.

   ::::{tip}
   Check the [ES|QL reference](https://www.elastic.co/guide/en/elasticsearch/reference/current/esql-language.html) to get familiar with the syntax and optimize your query.
   ::::

3. When editing your query or its configuration, run the query to update the preview of the visualization.

    ![Previewing an ESQL visualization](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt69dcceb4f1e12bc1/66c752d6aff77d384dc44209/edit-esql-visualization.gif "")

4. Select **Apply and close** to save the visualization to the dashboard.
