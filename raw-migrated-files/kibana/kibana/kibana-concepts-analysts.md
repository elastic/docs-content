# {{kib}} concepts [kibana-concepts-analysts]

***Learn the shared concepts for analyzing and visualizing your data***

As an analyst, you will use a combination of {{kib}} apps to analyze and visualize your data. {{kib}} contains both general-purpose apps and apps for the [**Enterprise Search**](https://www.elastic.co/guide/en/enterprise-search/current/index.html), [**Elastic Observability**](../../../solutions/observability/get-started/what-is-elastic-observability.md), and [**Elastic Security**](../../../solutions/security.md) solutions. These apps share a common set of concepts.


## Three things to know about {{es}} [_three_things_to_know_about_es]

You don’t need to know everything about {{es}} to use {{kib}}, but the most important concepts follow:

* **{{es}} makes JSON documents searchable and aggregatable.** The documents are stored in an [index](../../../manage-data/data-store/index-basics.md) or [data stream](../../../manage-data/data-store/index-types/data-streams.md), which represent one type of data.
* ***Searchable* means that you can filter the documents for conditions.** For example, you can filter for data "within the last 7 days" or data that "contains the word {{kib}}". {{kib}} provides many ways for you to construct filters, which are also called queries or search terms.
* ***Aggregatable* means that you can extract summaries from matching documents.** The simplest aggregation is **count**, and it is frequently used in combination with the **date histogram**, to see count over time. The **terms** aggregation shows the most frequent values.


## Finding your apps and objects [_finding_your_apps_and_objects]

$$$kibana-concepts-finding-your-apps-objects$$$
{{kib}} offers a [global search bar](../../../get-started/the-stack.md#kibana-navigation-search) on every page that you can use to find any app or saved object. Open the search bar using the keyboard shortcut Ctrl+/ on Windows and Linux, Command+/ on MacOS.

![Global search showing matches to apps and saved objects for the word visualize](../../../images/kibana-global-search.png "")


## Accessing data with data views [_accessing_data_with_data_views]

{{kib}} requires a data view to tell it which {{es}} data you want to access, and whether the data is time-based. A data view can point to one or more {{es}} data streams, indices, or index aliases by name.

Data views are typically created by an administrator when sending data to {{es}}. You can [create or update data views](../../../explore-analyze/find-and-organize/data-views.md) in **Stack Management**, or by using a script that accesses the {{kib}} API.

{{kib}} uses the data view to show you a list of fields, such as `event.duration`. You can customize the display name and format for each field. For example, you can tell {{kib}} to display `event.duration` in seconds. {{kib}} has [field formatters](../../../explore-analyze/find-and-organize/data-views.md#managing-fields) for strings, dates, geopoints, and numbers.


## Searching your data [kibana-concepts-searching-your-data]

{{kib}} provides you several ways to build search queries, which will reduce the number of document matches that you get from {{es}}. {{kib}} apps provide a time filter, and most apps also include semi-structured search and extra filters.

![Time filter, semi-structured search, and filters in a {{kib}} app](../../../images/kibana-top-bar.png "")

If you frequently use any of the search options, click ![save icon](../../../images/kibana-saved-query-icon.png "") next to the semi-structured search to save or load a previously saved query. The saved query always contains the semi-structured search query, and optionally the time filter and extra filters.


### Time filter [_time_filter]

The [global time filter](../../../explore-analyze/query-filter/filtering.md) limits the time range of data displayed. In most cases, the time filter applies to the time field in the data view, but some apps allow you to use a different time field.

Using the time filter, you can configure a refresh rate to periodically resubmit your searches.

![section of time filter where you can configure a refresh rate](../../../images/kibana-refresh-every.png "")

To manually resubmit a search, click the **Refresh** button. This is useful when you use {{kib}} to view the underlying data.


### Semi-structured search [semi-structured-search]

Combine free text search with field-based search using the Kibana Query Language (KQL). Type a search term to match across all fields, or start typing a field name to get suggestions for field names and operators that you can use to build a structured query. The semi-structured search will filter documents for matches, and only return matching documents.

Following are some example KQL queries.  For more detailed examples, refer to [Kibana Query Language](../../../explore-analyze/query-filter/languages/kql.md).

|     |     |
| --- | --- |
| Exact phrase query | `http.response.body.content.text:"quick brown fox"` |
| Terms query | http.response.status_code:400 401 404 |
| Boolean query | `response:200 or extension:php` |
| Range query | `account_number >= 100 and items_sold <= 200` |
| Wildcard query | `machine.os:win*` |


### Additional filters with AND [autocomplete-suggestions]

Structured filters are a more interactive way to create {{es}} queries, and are commonly used when building dashboards that are shared by multiple analysts. Each filter can be disabled, inverted, or pinned across all apps. Each of the structured filters is combined with AND logic on the rest of the query.

![Add filter popup](../../../images/kibana-add-filter-popup.png "")


## Saving objects [_saving_objects]

{{kib}} lets you save objects for your own future use or for sharing with others. Each [saved object](/explore-analyze/find-and-organize/saved-objects.md) type has different abilities. For example, you can save your search queries made with **Discover**, which lets you:

* Share a link to your search
* Download the full search results in CSV form
* Start an aggregated visualization using the same search query
* Embed the **Discover** search results into a dashboard
* Embed the **Discover** search results into a Canvas workpad

For organization, every saved object can have a name, [tags](../../../get-started/the-stack.md#kibana-navigation-search), and type. Use the global search to quickly open a saved object.


## What’s next? [_whats_next]

* Try the {{kib}} [Quick start](../../../explore-analyze/overview/kibana-quickstart.md), which shows you how to put these concepts into action.
* Go to [Discover](../../../explore-analyze/discover.md) for instructions on searching your data.
