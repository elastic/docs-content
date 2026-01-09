---
navigation_title: Search and filter data
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/discover.html#search-in-discover
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
description: Search and filter your Elasticsearch data in Discover using KQL, Lucene, or ES|QL queries. Apply filters to narrow results and find the data you need.
---

# Search and filter data in Discover [search-in-discover]

**Discover** combines powerful text search with structured filtering to help you find specific data quickly. Use KQL for user-friendly querying, Lucene for advanced patterns, or {{esql}} for piped queries. Apply visual filters to narrow results based on field values, ranges, or complex conditions.

This guide shows you how to query your data effectively, build filters, and use the different query languages available in **Discover**.

## Search with KQL or Lucene

In the default mode of **Discover**, you can search your data using the [{{kib}} Query Language (KQL)](../query-filter/languages/kql.md) or [Lucene query syntax](../query-filter/languages/lucene-query-syntax.md).

### Simple text search

To search all fields, enter a simple string in the query bar:

![Search field in Discover](/explore-analyze/images/kibana-discover-search-field.png "")

:::{note}
Free text searches that don't specify a field may not return expected results depending on how the `index.query.default_field` index setting is configured for the indices matching the current {{data-source}}.
:::

### Structured search with KQL

To search particular fields and build more complex queries, use KQL. As you type, KQL prompts you with the fields you can search and the operators you can use to build a structured query.

For example, to search the ecommerce sample data for documents where the country matches US:

1. Enter `g`, and then select **geoip.country_iso_code**.
2. Select **:** for equals, and **US** for the value.
3. Press Enter or click the refresh button to run the query.

For a more complex search, try:

```ts
geoip.country_iso_code : US and products.taxless_price >= 75
```

Learn more about [KQL syntax](../query-filter/languages/kql.md).

## Apply filters

In addition to the query bar, you can use filters to narrow down your results. Filters provide a visual way to build conditions and are particularly useful when you want to:

* Exclude specific values
* Filter on multiple values for a field
* Build complex filter combinations
* Share filters across other applications

### Add a filter

To add a filter:

1. Click the **Add filter** button (![Add icon](/explore-analyze/images/kibana-add-icon.png "")) next to the query bar.
2. In the **Add filter** pop-up:
   * Select the **field** you want to filter on
   * Choose an **operator** (is, is not, is one of, exists, and so on)
   * Enter or select the **value** to filter by
3. Optionally, you can switch to **Edit as Query DSL** to write the filter as JSON.
4. Click **Add filter**.

![Add filter dialog in Discover](/explore-analyze/images/kibana-discover-add-filter.png "")

For example, to exclude results where the day of week is Wednesday:

1. Set **Field** to `day_of_week`
2. Set **Operator** to `is not`
3. Set **Value** to `Wednesday`
4. Click **Add filter**

### Quick filters from field values

You can also create filters directly from the fields sidebar:

1. Find a field in the sidebar and click it to see its top values.
2. Click the **+** icon next to a value to filter for that value, or the **-** icon to filter it out.

### Filter pill actions

Once added, filter pills appear below the query bar. You can interact with them in several ways:

:::{include} ../_snippets/global-filters.md
:::

## Search with {{esql}}

You can use **Discover** with the {{es}} Query Language, {{esql}}. When using {{esql}}, you don't have to select a {{data-source}} - your query determines the data to explore.

To switch to {{esql}} mode:

1. Select **Try {{esql}}** from the **Discover** application menu bar.
2. If you've entered a KQL or Lucene query in the default mode, it automatically converts to {{esql}}.

In {{esql}} mode, the **Documents** tab is renamed to **Results**.

:::{important}
{applies_to}`stack: ga 9.1` When an {{esql}} query times out, partial results that are available are shown. The timeout is defined by the `search:timeout` advanced setting, which is set to 10 minutes (600000 ms) by default. In serverless projects, this advanced setting is not customizable and the timeout is set to 10 minutes.
:::

Learn more about using {{esql}} in [Using {{esql}}](try-esql.md).

## Find and highlight values in the table

Use the in-table search to find and highlight specific values beyond what's currently visible on your screen.

The in-table search looks for all matching values in all results and pages currently loaded in the table. The number of results loaded depends on the [Sample size](document-explorer.md#document-explorer-sample-size). If you load more results, the search automatically updates and reflects the new number of matching values, if any are found.

```{tip}
You can navigate between results with your keyboard by pressing "Enter" to go to the next result, and "Shift + Enter" to go to the previous result.
```

![Using the in-table search and navigating through the matches](https://images.contentstack.io/v3/assets/bltefdd0b53724fa2ce/blt30bf5f8b9a45ab74/67c234a787966d9fbc994ce0/in-table-search-demo.gif)

## Inspect your queries

To see the exact {{es}} query that **Discover** sent:

:::{include} ../_snippets/inspect-request.md
:::

This is useful for debugging queries, understanding how filters are translated to {{es}} queries, or copying queries to use in other tools.

## Learn more

* [{{kib}} Query Language (KQL)](../query-filter/languages/kql.md)
* [Lucene query syntax](../query-filter/languages/lucene-query-syntax.md)
* [Using {{esql}}](try-esql.md)
* [Filtering data](../query-filter/filtering.md)

