---
navigation_title: Search and filter
applies_to:
  serverless: ga
  stack: ga
products:
  - id: kibana
type: how-to
description: Narrow the documents in a data view to the ones you need by searching with Kibana Query Language (KQL) or Lucene and adding filters in classic mode.
---

# Search and filter with KQL, Lucene, and filters in Discover's classic mode

If **Discover** returns more documents than you need, you can narrow them to the ones that matter. Classic mode is the **Discover** mode where you pick a data view and search it with [Kibana Query Language (KQL)](../query-filter/languages/kql.md) or [Lucene](../query-filter/languages/lucene-query-syntax.md), two syntaxes for writing search queries, and add filters from the interface. The chart and the results table then show only the matching documents.

## Before you begin

- Open **Discover** in classic mode. If **Discover** opens in {{esql}} mode, refer to [Switch to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode).
- A [data view](../find-and-organize/data-views.md) for the data you want to search. It can point to one or more indices, [data streams](../../manage-data/data-store/data-streams.md), or [index aliases](/manage-data/data-store/aliases.md). Integrations sometimes create data views for you, and you can also [create your own](../find-and-organize/data-views/create-data-view.md). If **Discover** asks you to add data or create a data view instead of opening, refer to [](/troubleshoot/kibana/discover-dashboards-no-data-screen.md).
- To follow the examples, add the [ecommerce sample data](/manage-data/ingest/sample-data.md) and select its data view.

## Select a data view and a time range [find-the-data-you-want-to-use]

To explore data in classic mode, select a data view, then set the time range for the data you want to see.

1. Select the data view that contains the data you want to explore.
   If you're using sample data, data views are automatically created and are ready to use.
   :::{image} /explore-analyze/images/kibana-discover-data-view.png
   :alt: Data view menu in Discover with a data view selected
   :screenshot:
   :width: 300px
   :::

2. If needed, adjust the [time range](../query-filter/filtering.md), for example by setting it to the **Last 7 days**.
    The range selection is based on the default time field in your data view. If you are using the sample data, this value was set when the data view was created. If you are using your own data view and it does not have a time field:

    - {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` The time filter stays visible, shows **All time**, and you can't change it.
    - {applies_to}`stack: ga 9.0-9.5` The range selection is not available.

3. Select **Update** or **Refresh**.

**Result:** **Discover** shows your data. By default, the table includes a column for the time field and a **Summary** column with an overview of each result.

## Search with KQL or Lucene

To search all fields, enter a text string in the search bar, the query input at the top of **Discover**.

:::{image} /explore-analyze/images/kibana-discover-search-field.png
:alt: Search bar in Discover with a text string entered
:screenshot:
:::

:::{note}
If a free text search that doesn't name a field returns unexpected results, search a specific field instead. The results depend on the [`index.query.default_field` index setting](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-query-default-field) of the indices behind the current data view.
:::

To search particular fields and build more complex queries, use [KQL](../query-filter/languages/kql.md). As you enter text, KQL prompts you with the fields you can search and the operators you can use to build a structured query.

To use [Lucene](../query-filter/languages/lucene-query-syntax.md) instead, open the query menu next to the search bar, select **Language: KQL**, and then select **Lucene**.

For example, search the ecommerce sample data for documents where the country matches US:

1. Enter `g`, and then select **geoip.country_iso_code**.
2. Select **:** for equals, and **US** for the value, and then select the refresh button or press Enter.
3. For a more complex search, try:

    ```ts
    geoip.country_iso_code : US and products.taxless_price >= 75
    ```

**Result:** The chart and the table show only the documents that match your query.

$$$filter-in-discover$$$

## Filter with the filter bar

Besides the search bar, you can build filters one by one with **Add filter**, or define them as [Query DSL](../query-filter/languages/querydsl.md), the JSON query language of {{es}}. Filters appear as pills in the filter bar.

For example, exclude results from the ecommerce sample data view where the day of the week is Wednesday:

1. Select **Add filter** ![Add filter icon](/explore-analyze/images/kibana-add-icon.png "") next to the search bar.
2. In the **Add filter** pop-up, set the field to **day_of_week**, the operator to **is not**, and the value to **Wednesday**.

    :::{image} /explore-analyze/images/kibana-discover-add-filter.png
    :alt: Add filter dialog with the field day_of_week, the operator is not, and the value Wednesday
    :screenshot:
    :::

3. Select **Add filter**.
4. To remove a filter, select the close icon (x) next to its name in the filter bar.

**Result:** The filter appears in the filter bar, and the chart and the table exclude the documents that it matches.

### Filter pill actions

:::{include} ../_snippets/global-filters.md
:::

## Cancel a running query [cancel-query-in-discover]

:::{include} ../_snippets/discover-cancel-query.md
:::

## Next steps

- To rank documents by how well they match, refer to [Sort Discover results by relevance](discover-search-for-relevance.md).
- To select which fields the table shows, refer to [Explore fields in Discover](explore-fields.md).

## Related pages

- [How to query in Discover's classic mode](use-classic-mode.md)
- [{{kib}} Query Language (KQL) overview](../query-filter/languages/kql.md)
- [Lucene query syntax in {{kib}}](../query-filter/languages/lucene-query-syntax.md)
