---
navigation_title: "Events reference"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/behavioral-analytics-event-reference.html
applies:
  stack:
  serverless:
---



# Events reference [behavioral-analytics-event-reference]


Behavioral Analytics logs events using the [Elastic Common Schema^](https://www.elastic.co/guide/en/ecs/current/ecs-reference.html), including a custom field set for analytics events. Refer to [examples](#behavioral-analytics-event-reference-examples) of the full data objects that are logged.


## Fields overview [behavioral-analytics-event-reference-fields] 

* [Common event fields](#behavioral-analytics-event-reference-common-fields)
* [Search event fields](#behavioral-analytics-event-reference-search-fields)
* [Search click event fields](#behavioral-analytics-event-reference-search_click-fields)
* [Pageview event fields](#behavioral-analytics-event-reference-pageview-fields)


## Common event fields [behavioral-analytics-event-reference-common-fields] 

`@timestamp`
:   Timestamp of the event.

`event.action`
:   The type of event. Possible values are `search`, `search_click`, and `pageview`.

`event.source`
:   The source of the event. Possible values are `client` and `server`.

`session.id`
:   A unique identifier for the session.

`user.id`
:   A unique identifier for the user.

`_id`
:   The document ID.

`_index`
:   The index name.

`_score`
:   The score of the document.


## Search event fields [behavioral-analytics-event-reference-search-fields] 

`search.filters`
:   The filters applied to the search query.

`search.query`
:   The search query.

`search.results.items.document.id`
:   The ID of the document in the search results.

`search.results.items.document.index`
:   The index of the document in the search results.

`search.results.items.page.url.domain`
:   The URL domain of the page in the search results.

`search.results.items.page.url.original`
:   The original URL of the page in the search results.

`search.results.items.page.url.path`
:   The URL path of the page in the search results.

`search.results.items.page.url.scheme`
:   The URL scheme of the page in the search results.

`search.results.total_results`
:   The total number of results returned by the search query.

`search.search_application`
:   The search application used to perform the search query.

`search.sort.name`
:   The name of the sort applied to the search query.


## Search click event fields [behavioral-analytics-event-reference-search_click-fields] 

`document.id`
:   The ID of the document that was clicked.

`document.index`
:   The index containing the document that was clicked.

`page.url.domain`
:   The URL domain of the page that was clicked.

`page.url.original`
:   The original URL of the page that was clicked.

`page.url.path`
:   The URL path of the page that was clicked.

`page.url.scheme`
:   The URL scheme of the page that was clicked.

`search.filters`
:   The filters applied to the search query.

`search.query`
:   The search query.

`search.results.items.document.id`
:   The ID of the document in the search results.

`search.results.items.document.index`
:   The index of the document in the search results.

`search.results.items.page.url.domain`
:   The URL domain of the page in the search results.

`search.results.items.page.url.original`
:   The original URL of the page in the search results.

`search.results.items.page.url.path`
:   The URL path of the page in the search results.

`search.results.items.page.url.scheme`
:   The URL scheme of the page in the search results.

`search.results.total_results`
:   The total number of results returned by the search query.

`search.search_application`
:   The search application used to perform the search query.

`search.sort.name`
:   The name of the sort applied to the search query.

`session.location.country_iso_code`
:   The ISO code of the country where the search click occurred.

`session.location.country_name`
:   The name of the country where the search click occurred.


## Pageview event fields [behavioral-analytics-event-reference-pageview-fields] 

`document.id`
:   The ID of the document that was viewed.

`document.index`
:   The index containing the document that was viewed.

`page.referrer.domain`
:   The URL domain of the page that referred to the viewed page.

`page.referrer.original`
:   The original URL of the page that referred to the viewed page.

`page.referrer.path`
:   The path of the page that referred to the viewed page.

`page.referrer.scheme`
:   The URL scheme of the page that referred to the viewed page.

`page.title`
:   The title of the viewed page.

`page.url.domain`
:   The URL domain of the viewed page.

`page.url.original`
:   The original URL of the viewed page.

`page.url.path`
:   The URL path of the viewed page.

`page.url.scheme`
:   The URL scheme of the viewed page.

`session.location.country_iso_code`
:   The ISO code of the country where the pageview occurred.

`session.location.country_name`
:   The name of the country where the pageview occurred.


## Examples [behavioral-analytics-event-reference-examples] 

::::{dropdown} Expand to see a full example of a search event data object:
```js
{
  "@timestamp": [
    "2023-05-16T12:52:29.003Z"
  ],
  "event.action": [
    "search"
  ],
  "event.source": [
    "client"
  ],
  "search.filters": [
    {
      "color": [
        "silver"
      ],
      "brand": [
        "Robel, Klocko and Ziemann",
        "McClure, Marks and Mertz"
      ]
    }
  ],
  "search.query": [
    "transformation"
  ],
  "search.results.items.document.id": [
    "045a164b-229e-40b5-ba66-b2ebabd2a251"
  ],
  "search.results.items.document.index": [
    "products"
  ],
  "search.results.items.page.url.domain": [
    "fancy-overcoat.org"
  ],
  "search.results.items.page.url.original": [
    "http://fancy-overcoat.org/happy/pancakes/deals"
  ],
  "search.results.items.page.url.path": [
    "/happy/pancakes/deals"
  ],
  "search.results.items.page.url.scheme": [
    "http"
  ],
  "search.results.total_results": [
    67
  ],
  "search.search_application": [
    "search-ui"
  ],
  "search.sort.name": [
    "relevance"
  ],
  "session.id": [
    "2bc31b08-d443-4b7a-81ea-65edf3dd82e7"
  ],
  "user.id": [
    "42704a4b-692b-4654-bb67-a65eb0c72f15"
  ],
  "_id": "y3IBBogBWHKTU-4a543S",
  "_index": ".ds-behavioral_behavioral-analytics-event-website-2023.05.10-000001",
  "_score": null
}
```

::::


::::{dropdown} Expand to see a full example of a searchclick event data object:
```js
{
  "@timestamp": [
    "2023-05-16T12:22:23.468Z"
  ],
  "document.id": [
    "38cca784-109a-4ea0-a4e8-60c3be667ffd"
  ],
  "document.index": [
    "products"
  ],
  "event.action": [
    "search_click"
  ],
  "event.source": [
    "client"
  ],
  "page.url.domain": [
    "unfurnished-appartments"
  ],
  "page.url.original": [
    "https://unfurnished-appartments/new/europe"
  ],
  "page.url.path": [
    "/new/europe"
  ],
  "page.url.scheme": [
    "https"
  ],
  "search.filters": [
    {
      "brand": [
        "McClure, Marks and Mertz",
        "Ondricka - Rath"
      ]
    }
  ],
  "search.query": [
    "ferryboat"
  ],
  "search.results.items.document.id": [
    "0c76967b-4915-446e-9b2c-b1bfb9e39e1e"
  ],
  "search.results.items.document.index": [
    "products"
  ],
  "search.results.items.page.url.domain": [
    "dependent-lecture.info"
  ],
  "search.results.items.page.url.original": [
    "http://dependent-lecture.info/documents/additional/latest"
  ],
  "search.results.items.page.url.path": [
    "/documents/additional/latest"
  ],
  "search.results.items.page.url.scheme": [
    "http"
  ],
  "search.results.total_results": [
    54
  ],
  "search.search_application": [
    "search-ui"
  ],
  "search.sort.name": [
    "relevance"
  ],
  "session.id": [
    "9411fb93-8707-49a4-baab-cec4d6aef753"
  ],
  "session.location.country_iso_code": [
    "GP"
  ],
  "session.location.country_name": [
    "Guadeloupe"
  ],
  "user.id": [
    "911d0c19-e713-4413-8f4c-c6c612bc37c4"
  ],
  "_id": "m8cBBogBG4-Ak0Iy7LME",
  "_index": ".ds-behavioral_behavioral-analytics-event-website-2023.05.10-000001",
  "_score": null
}
```

::::


::::{dropdown} Expand to see a full example of a pageview event data object:
```js
{
  "@timestamp": [
    "2023-05-16T12:52:51.309Z"
  ],
  "document.id": [
    "c98ppfc8-3a04-4a20-888a-f87292b31181"
  ],
  "document.index": [
    "products"
  ],
  "event.action": [
    "page_view"
  ],
  "event.source": [
    "client"
  ],
  "page.referrer.domain": [
    "happy-pancakes.name"
  ],
  "page.referrer.original": [
    "https://happy-pancakes.name/magnam"
  ],
  "page.referrer.path": [
    "/magnam"
  ],
  "page.referrer.scheme": [
    "https"
  ],
  "page.title": [
    "Super fast delivery"
  ],
  "page.url.domain": [
    "happy-staircase.net"
  ],
  "page.url.original": [
    "http://happy-staircase.net/quam"
  ],
  "page.url.path": [
    "/quam"
  ],
  "page.url.scheme": [
    "http"
  ],
  "session.id": [
    "2bc31b08-d443-4b7a-81ea-65edf3dd82e7"
  ],
  "session.location.country_iso_code": [
    "SN"
  ],
  "session.location.country_name": [
    "Senegal"
  ],
  "user.id": [
    "42704a4b-692b-4654-bb67-a65eb0c72f15"
  ],
  "_id": "zHIBBogBWHKTU-4a543S",
  "_index": ".ds-behavioral_behavioral-analytics-event-website-2023.05.10-000001",
  "_score": null
}
```

::::


