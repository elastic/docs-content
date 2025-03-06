# {{esql}} [esql]

The Elasticsearch Query Language, {{esql}}, makes it faster and easier to explore your data.

{{esql}} is a piped language which allows you to chain together multiple commands to query your data. Based on the query, Lens suggestions in Discover create a visualization of the query results.

{{esql}} comes with its own dedicated {{esql}} Compute Engine for greater efficiency. With one query you can search, aggregate, calculate and perform data transformations without leaving **Discover***. Write your query directly in ***Discover*** or use the ***Dev Tools** with the [{{esql}} API](../../../explore-analyze/query-filter/languages/esql-rest.md).

You can switch to the ES|QL mode of Discover from the application menu bar.

{{esql}} also features in-app help and suggestions, so you can get started faster and don’t have to leave the application to check syntax.

![The ES|QL syntax reference and the autocomplete menu](../../../images/kibana-esql-in-app-help.png "")

You can also use ES|QL queries to create panels on your dashboards, create enrich policies, and create alerting rules.

For more detailed information about {{esql}} in Kibana, refer to [Using {{esql}} in {{kib}}](../../../explore-analyze/query-filter/languages/esql-kibana.md).

::::{note}
{{esql}} is enabled by default in {{kib}}. It can be disabled using the `enableESQL` setting from the [Advanced Settings](kibana://reference/advanced-settings.md).

This will hide the {{esql}} user interface from various applications. However, users will be able to access existing {{esql}} artifacts like saved Discover sessions and visualizations.

::::



## {{observability}} [esql-observability]

{{esql}} makes it much easier to analyze metrics, logs and traces from a single query. Find performance issues fast by defining fields on the fly, enriching data with lookups, and using simultaneous query processing. Combining {{esql}} with {{ml}} and AiOps can improve detection accuracy and use aggregated value thresholds.


## Security [esql-security]

Use {{esql}} to retrieve important information for investigation by using lookups. Enrich data and create new fields on the go to gain valuable insight for faster decision-making and actions. For example, perform a lookup on an IP address to identify its geographical location, its association with known malicious entities, or whether it belongs to a known cloud service provider all from one search bar. {{esql}} ensures more accurate alerts by incorporating aggregated values in detection rules.


## What’s next? [esql-whats-next]

The main documentation for {{esql}} lives in the [{{es}} docs](../../../explore-analyze/query-filter/languages/esql.md).

We also have a short tutorial in the **Discover** docs: [Using {{esql}}](../../../explore-analyze/discover/try-esql.md).
