---
navigation_title: "API overview"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/behavioral-analytics-api.html
applies:
  stack:
---



# API overview [behavioral-analytics-api]


This page outlines all the APIs available for behavioral analytics and links to their documentation.


## Behavioral Analytics REST APIs [behavioral-analytics-api-es-rest] 

Behavioral Analytics relies on a number of {{es}} APIs to manage analytics collections. Refer to the [API documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/behavioral-analytics-apis.html) for the details.


## Behavioral Analytics Clients [behavioral-analytics-api-clients] 

Behavioral Analytics integrates onto your website using one of our JavaScript clients:

* **Browser tracker** - integrated into your website using a `<script>` tag.

    * View the [`README` in GitHub](https://github.com/elastic/behavioral-analytics-tracker/tree/main/packages/browser-tracker).

* **Javascript Tracker** - integrated into your website using a JavaScript module.

    * View the [`README` in GitHub](https://github.com/elastic/behavioral-analytics-tracker/tree/main/packages/javascript-tracker).



## Search UI integration [behavioral-analytics-api-search-ui] 

To simplify the integration of Behavioral Analytics into your website, we provide a Search UI integration. This integration automatically sends Behavioral Analytics events to your collection as your customer interacts with your search experience.

Refer to the [Search UI analytics plugin documentation](https://docs.elastic.co/search-ui/api/core/plugins/analytics-plugin).


## Searchkit integration [behavioral-analytics-api-searchkit] 

Behavioral Analytics also integrates with [Searchkit](https://www.searchkit.co), an open source library for building UIs on top of {{es}}.

