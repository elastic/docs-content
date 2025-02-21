---
navigation_title: "View events"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/behavioral-analytics-event.html
applies_to:
  stack:
---



# View events [behavioral-analytics-event]


::::{tip}
Refer to [Events reference](behavioral-analytics-event-reference.md) for a complete list of the fields logged by events.

::::


Once you’ve started **tracking events** using the [Behavioral Analytics Tracker](https://github.com/elastic/behavioral-analytics-tracker/tree/main#readme), you can view them on a pre-built dashboard in {{kib}}.


## View events in the Overview dashboard [behavioral-analytics-event-send-view-events-overview]

The **Overview** dashboard provides a quick overview of the following:

* Searches
* No results
* Clicks
* Sessions

This allows you to quickly check both absolute numbers and trends (tracked in percentage changes) about these events. Find this dashboard under **Search > Behavioral Analytics>** *your-collection* **> Overview**.

The following screenshot shows an example **Overview** dashboard:

:::{image} ../../../images/elasticsearch-reference-analytics-overview-dashboard.png
:alt: Analytics Overview dashboard showing the number of searches
:class: screenshot
:::


## View events in the Explorer dashboard [behavioral-analytics-event-send-view-events-dashboard]

The **Explorer** dashboard provides a more detailed view of your events. Find this dashboard under **Search > Behavioral Analytics>** *your-collection* **> Explorer**.

Here you can find and search over the following:

* Search terms
* Top clicked results
* No results
* Locations
* Referrers

You can also easily sort in ascending or descending order by clicking on the header arrows.

The following screenshot shows the **Locations** tab of an **Explorer** dashboard, with a list of top locations in descending order:

:::{image} ../../../images/elasticsearch-reference-analytics-explorer-dashboard.png
:alt: Explorer dashboard showing the top locations in descending order
:class: screenshot
:::


## Discover and Lens [behavioral-analytics-event-send-view-events-discover]

For more detailed analysis, you can view events in the Kibana [Discover^](../../../explore-analyze/discover.md) app. The Behavioral Analytics UI will guide you here from the **Explorer** dashboard. You can dig into the details using Discover and then generate visualizations using [Lens^](../../../explore-analyze/visualize/lens.md).

Discover works with [data views^](../../../explore-analyze/find-and-organize/data-views.md). You’ll find a data view automatically created for your collection, named `behavioral_analytics.events-<your-collection>`. This data view will be pre-selected in the data view dropdown menu. Use this menu to switch between data views for different collections.

The following screenshot shows you where to find the data view dropdown menu in Discover:

:::{image} ../../../images/elasticsearch-reference-discover-data-view-analytics.png
:alt: Analytics Discover app showing the data view dropdown menu
:class: screenshot
:::

Discover has a lot of options, but here’s a quick overview of how to get started:

* Filter your data by searching for terms, such as `search`, `page_view`, and `search_click`. You’ll see a time series of hits that match your search.
* Search for "event" in the field name search bar. For example:

    * Select `event.action`. You’ll find a list of all the events you’ve sent and their frequency distribution.

* Search for `search.query` to find all search queries.
* Select **Visualize** to create a Lens visualization.

The following screenshot shows a Lens visualization of an `event.action` distribution:

:::{image} ../../../images/elasticsearch-reference-discover-lens-analytics.png
:alt: Analytics Discover app showing a Lens visualization of an event action distribution
:class: screenshot
:::


### Learn more [behavioral-analytics-event-send-view-events-learn-more]

Read the [Discover documentation^](../../../explore-analyze/discover.md).

Read the [Lens documentation^](../../../explore-analyze/visualize/lens.md).

