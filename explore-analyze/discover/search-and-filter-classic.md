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

# Search and filter with KQL, Lucene, and filters

In classic mode, **Discover** lets you combine free text search with filtering on structured data. Search with Kibana Query Language (KQL) or Lucene, add filters, and the chart and the results table update to show only the matching documents.

## Before you begin

- Open **Discover** in classic mode and select a data view. If **Discover** opens in {{esql}} mode, refer to [Switch to Discover's classic mode](switch-esql-mode.md#revert-to-classic-mode).
- To follow the examples, add the [ecommerce sample data](/manage-data/ingest/sample-data.md) and select its data view.

## Search with KQL or Lucene

To search all fields, enter a text string in the query bar.

![Search field in Discover](/explore-analyze/images/kibana-discover-search-field.png "")

:::{note}
Free text searches that don't specify a field might not return the results you expect, depending on how the [`index.query.default_field` index setting](elasticsearch://reference/elasticsearch/index-settings/index-modules.md#index-query-default-field) is configured for the indices that match the current data view.
:::

To search particular fields and build more complex queries, use [KQL](../query-filter/languages/kql.md). As you enter text, KQL prompts you with the fields you can search and the operators you can use to build a structured query. To use [Lucene](../query-filter/languages/lucene-query-syntax.md) instead, switch the query language of the query bar.

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

Besides the query bar, you can build filters one by one with **Add filter**, or define them as [Query DSL](../query-filter/languages/querydsl.md).

For example, exclude results from the ecommerce sample data view where the day of the week is Wednesday:

1. Select ![Add filter icon](/explore-analyze/images/kibana-add-icon.png "") next to the query bar.
2. In the **Add filter** pop-up, set the field to **day_of_week**, the operator to **is not**, and the value to **Wednesday**.

    ![Add filter dialog in Discover](/explore-analyze/images/kibana-discover-add-filter.png "")

3. Select **Add filter**.
4. Continue your exploration by adding more filters.
5. To remove a filter, select the close icon (x) next to its name in the filter bar.

**Result:** The filter appears in the filter bar, and the chart and the table exclude the documents that it matches.

### Filter pill actions

:::{include} ../_snippets/global-filters.md
:::

## Related pages

- [Use Discover in classic mode](use-classic-mode.md)
- [Search for relevance](discover-search-for-relevance.md)
- [Kibana Query Language](../query-filter/languages/kql.md)
