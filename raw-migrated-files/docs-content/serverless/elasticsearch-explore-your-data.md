# Explore your data [elasticsearch-explore-your-data]

In addition to search, {{es3}} offers several options for analyzing and visualizing your data.

::::{note}
These features are available on all Elastic deployment types: self-managed clusters, Elastic Cloud Hosted deployments, and {{es-serverless}} projects. They are documented in the {{es}} and {{kib}} core documentation.

::::



## Data analysis [_data_analysis]

[Aggregations](../../../explore-analyze/query-filter/aggregations.md)
:   Use aggregations in your [`_search` API](https://www.elastic.co/docs/api/doc/elasticsearch-serverless/operation/operation-search#operation-search-body-application-json-aggregations) requests to summarize your data as metrics, statistics, or other analytics.

$$$elasticsearch-explore-your-data-discover-your-data$$$

[Discover](../../../explore-analyze/discover.md)
:   Use the **Discover** UI to quickly search and filter your data, get information about the structure of the fields, and display your findings in a visualization.

    🔍 Find **Discover** in your {{es-serverless}} project’s UI under **Analyze / Discover**.



## Visualization [elasticsearch-explore-your-data-visualizations-save-to-the-visualize-library]

[Dashboards](../../../explore-analyze/dashboards.md)
:   Build dynamic dashboards that visualize your data as charts, graphs, maps, and more.

    🔍 Find **Dashboards** in your {{es-serverless}} project’s UI under **Analyze / Dashboard**.


[Maps](../../../explore-analyze/visualize/maps.md)
:   Visualize your geospatial data on a map.

    🔍 Find **Maps** in your {{es-serverless}} project’s UI under **Other tools / Maps**.



## Monitoring [_monitoring]

[Rules](../../../explore-analyze/alerts-cases.md)
:   Create rules that trigger notifications when certain conditions are met in your data.

    🔍 Find **Rules** in your {{es-serverless}} project’s UI under **Project settings > Alerts and insights > Rules**.
