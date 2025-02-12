---
navigation_title: "Search Application client guide"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/search-application-client.html
applies:
  stack:
  serverless:
---



# Search Application client guide [search-application-client]


This document is a how-to guide to building a search experience with a [search application](../search-applications.md), using the [Search Application client](https://github.com/elastic/search-application-client). The client is a JavaScript library designed to be used in the browser. You’ll integrate this library into your web app to simplify querying your search application.

::::{tip} 
A [sandbox environment](https://github.com/elastic/search-application-client/blob/main/examples/sandbox/README.md) is available for testing and experimenting with the `search-application-client` library. Jump there if you’d like to try out the client without setting up your own web app.

Clone the [repository](https://github.com/elastic/search-application-client) and follow the instructions in the README to get started.

::::



## Goal [search-application-client-client-goal] 

This guide assumes you want to build a web app with the following search features:

* Search bar and results with custom relevance
* Control over the presentation of results, such as inclusion/exclusion of fields and highlighting of matching terms
* UI controls such as facets, filters, sorts, pagination

You can think of the search application as the "server side" that persists changes to {{es}}. Your web app acts as the "client side" that queries the search application. You’ll be making edits to both your search application and your web app to complete the implementation.


## Prerequisites [search-application-client-client-prerequisites] 

To follow this guide, you’ll need:

* An **Elastic deployment**, that satisfies the [prerequisites](../search-applications.md#search-application-overview-prerequisites) for running a search application.

    * If you don’t have an Elastic deployment, start a free trial on [Elastic Cloud](https://cloud.elastic.co).

* A **search application**.

    * Create and manage search applications in the [{{kib}} UI](../search-applications.md#search-application-overview-get-started-ui) or using the [API](https://www.elastic.co/guide/en/elasticsearch/reference/current/put-search-application.html).

* A **web app** to query your search application, using [Search Application client](https://github.com/elastic/search-application-client#installation).


## Install and configure the client [search-application-client-client-configuration] 


### Install the client [search-application-client-client-configuration-install] 

[Install](https://github.com/elastic/search-application-client/blob/main/README.md#installation) the client using npm, yarn, or a CDN.

**Option 1: Using package manager**

To install the client using **npm**, run the following command:

```bash
npm install @elastic/search-application-client
```

To install the client using **yarn**, run the following command:

```bash
yarn add @elastic/search-application-client
```

**Option 2: Using CDN with HTML `<script>` tag**

Alternatively, you can install the client using a CDN. Add the following `<script>` tag to your web app’s HTML:

```html
<script src="https://cdn.jsdelivr.net/npm/@elastic/search-application-client@latest"></script>
```


### Import and initialize the client [search-application-client-client-configuration-import] 

Once installed, you can import the client into your web app. You’ll need the following information to initialize the client:

* The **name** of your search application
* The **URL endpoint** for your search application
* The **API key** for your search application

Find this information on the **Connect** page in the {{kib}} UI.


#### Option 1: Using JavaScript modules [search-application-client-client-configuration-import-js] 

Use the following import statement:

```js
import SearchApplicationClient from '@elastic/search-application-client';
```

Configure the client with your deployment details to start making search requests. You can generate an API key on the **Connect** page in the {{kib}} UI. Go to **Search > Search Applications >** <MY_SEARCH_APPLICATION> **> Connect**. You’ll find the following information prepopulated to initialize the client:

```js
import Client from '@elastic/search-application-client'

const request = Client(
  'my-search-application', // search application name
  'url-from-connect-page', // url-host
  'api-key-from-connect-page',  // api-key
  {
    // optional configuration
  }
)
```

Once configured you’ll be able to make search requests to your search application using the [client API](https://github.com/elastic/search-application-client#api-reference), like this:

```js
const results = await request()
  .query('star wars')
  .search()
```


#### Option 2: Using CDN [search-application-client-client-configuration-import-cdn] 

Alternatively, if you’re using a CDN, you can import the client using the following statement:

```html
<script>
  const Client = window['SearchApplicationClient'];
</script>
```

Configure the client with your deployment details to start making search requests. You can generate an API key on the **Connect** page in the {{kib}} UI. Go to **Search > Search Applications >** <MY_SEARCH_APPLICATION> **> Connect**. You’ll find the following information prepopulated to initialize the client:

```html
<script>
  const request = Client(
    'my-example-app', // search application name
    'url-from-connect-page', // url-host
    'api-key-from-connect-page',  // api-key
    {
    // optional configuration
    }
)
</script>
```

Once configured you’ll be able to make search requests to your search application using the [client API](https://github.com/elastic/search-application-client#api-reference), like this:

```html
<script>
  const results = await request()
    .query('star wars')
    .search()
</script>
```


## Working with your search template [search-application-client-client-template] 

The Search Application client is designed to work with any [search template](search-application-api.md) you create. You’ll use the Search Application APIs to create and manage your search templates.

::::{tip} 
When working with the Search Application APIs to manage templates, we provide the API examples using [{{kib}} Console^](../../../explore-analyze/query-filter/tools/console.md) syntax.

::::


Here’s an example template:

```console
PUT _application/search_application/my-example-app
{
  "indices": ["my-example-app"],
  "template": {
    "script": {
      "lang": "mustache",
      "source": """
        {
          "query": {
            "bool": {
              "must": [
              {{#query}}
              {
                "query_string": {
                  "query": "{{query}}",
                  "search_fields": {{#toJson}}search_fields{{/toJson}}
                }
              }
              {{/query}}
            ]
            }
          }
        }
      """,
      "params": {
        "query": "",
        "search_fields": ""
      }
    }
  }
}
```

This will allow you to add any template parameters you need to your template and then provide the values in your client request. Use `addParameter` to inject actual values into your template parameters.

For example, pass in values for `search_fields` like this:

```js
const results = await request()
  .query('star wars') // requires the template to use query parameter
  .addParameter('search_fields', ['title', 'description'])
  .search()
```


### Example template [search-application-client-client-template-example] 

We recommend getting started with the [boilerplate template](https://github.com/elastic/search-application-client#boilerplate-template) provided in the client repository. [View this script](https://github.com/elastic/search-application-client/blob/main/bin/boilerplate_template.js) to see how this is used. The `dictionary` parameter is used to pass in a JSON schema definition that describes structure and validation rules for the request object. This schema is important, because it restricts the use of certain features in the {{es}} query. [View the schema](https://github.com/elastic/search-application-client/blob/main/bin/request_schema.json).

Each search functionality in this guide requires a feature included in this template. These features require specific parameters to be present in the template:

* Query: `query`
* Filters: `_es_filters`
* Faceting: `_es_filters` and  `_es_aggs`
* Sorting: `_es_sort_fields`
* Pagination: `from` and `size`


## Search features [search-application-client-client-features] 

We will explore all the essential basics you’ll need for a search experience. You’ll learn how to implement them using your search application and query them using the client.

::::{tip} 
Refer to the [client repo](https://github.com/elastic/search-application-client#api-reference) for information on the available methods and their parameters.

::::



### Customizing relevance [search-application-client-client-features-relevance] 

Our simple template uses `query_string` searching across all fields, but this may not suit your use case. You can update the template to provide better relevance recall.

In the below example, we’re using a `multi-match` query against our template, with `best_fields` and `phrase_prefix` queries targeting different search fields.

```console
PUT _application/search_application/my-example-app
{
  "indices": ["example-index"],
  "template": {
    "script": {
      "lang": "mustache",
      "source": """
        {
          "query": {
            "bool": {
              "must": [
              {{#query}}
              {
                "multi_match" : {
                  "query":    "{{query}}",
                  "fields": [ "title^4", "plot", "actors", "directors" ]
                }
              },
              {
                "multi_match" : {
                  "query":    "{{query}}",
                  "type": "phrase_prefix",
                  "fields": [ "title^4", "plot"]
                }
              },
              {{/query}}
            ],
            "filter": {{#toJson}}_es_filters{{/toJson}}
            }
          },
          "aggs": {{#toJson}}_es_aggs{{/toJson}},
          "from": {{from}},
          "size": {{size}},
          "sort": {{#toJson}}_es_sort_fields{{/toJson}}
        }
      """,
      "params": {
        "query": "",
        "_es_filters": {},
        "_es_aggs": {},
        "_es_sort_fields": {},
        "size": 10,
        "from": 0
      },
      "dictionary": {
          //  add dictionary restricting
          // _es_filters, _es_sort_fields & _es_aggs params
          // Use example provided in repo: https://github.com/elastic/search-application-client/blob/main/bin/request_schema.json
      }
    }
  }
}
```

Refer to for examples of different types of queries, including combinations of text search, kNN search, ELSER search, hybrid search with RRF, and more.

**Use case: I want to dynamically adjust the search fields**

If you need to adjust `search_fields` at query request time, you can add a new parameter to the template (for example: `search_fields`) and use the `addParameter` method to provide the fields to the template.

**Use case: I want to boost results given a certain proximity to the user**

You can add additional template parameters to send the geo-coordinates of the user. Then use [`function_score`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-function-score-query.html) to boost documents which match a certain [`geo_distance`](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-geo-distance-query.html) from the user.


## Result fields [search-application-client-client-features-result-fields] 

By default, all fields are returned in the `_source` field. To restrict the fields returned, specify the fields in the template.

```console
PUT _application/search_application/my-example-app
{
  "indices": ["example-index"],
  "template": {
    "script": {
      "lang": "mustache",
      "source": """
        {
          "query": {
            "bool": {
              "must": [
              {{#query}}
                // ...
              {{/query}}
            ],
            "filter": {{#toJson}}_es_filters{{/toJson}}
            }
          },
          "_source": {
            "includes": ["title", "plot"]
          },
          "aggs": {{#toJson}}_es_aggs{{/toJson}},
          "from": {{from}},
          "size": {{size}},
          "sort": {{#toJson}}_es_sort_fields{{/toJson}}
        }
      """,
      "params": {
        "query": "",
        "_es_filters": {},
        "_es_aggs": {},
        "_es_sort_fields": {},
        "size": 10,
        "from": 0
      },
      "dictionary": {
          //  add dictionary restricting _es_filters and _es_aggs params
          // Use the dictionary example provided in repo: https://github.com/elastic/search-application-client/blob/main/bin/request_schema.json
      }
    }
  }
}
```

**Use case: I want to dynamically adjust the result fields**

If you need to adjust the fields returned at query request time, you can add a new parameter to the template (for example: `result_fields`) and use the `addParameter` method to provide the fields to the template.


### Highlighting and snippets [search-application-client-client-features-highlight-snippets] 

Highlighting support is straightforward to add to the template. With the [highlighting API](https://www.elastic.co/guide/en/elasticsearch/reference/current/highlighting.html), you can specify which fields you want to highlight for matches.

In the following example, we specify `title` and `plot` as the highlighted fields. `title` typically has a short value length, compared to `plot` which is variable and tends to be longer.

We specify the title to be `fragment_size` of `0` to return all of the text when there is a highlight. We specify the plot to be `fragment_size` of `200`, where each highlighted fragment will be up to 200 characters long.

```console
PUT _application/search_application/my-example-app
{
  "indices": ["example-index"],
  "template": {
    "script": {
      "lang": "mustache",
      "source": """
        {
          "query": {
            "bool": {
              "must": [
              {{#query}}
                // ...
              {{/query}}
            ],
            "filter": {{#toJson}}_es_filters{{/toJson}}
            }
          },
          "_source": {
            "includes": ["title", "plot"]
            },
            "highlight": {
              "fields": {
                "title": { "fragment_size": 0 },
                "plot": { "fragment_size": 200 }
                }
                },
                "aggs": {{#toJson}}_es_aggs{{/toJson}},
                "from": {{from}},
                "size": {{size}},
                "sort": {{#toJson}}_es_sort_fields{{/toJson}}
                }
                """,
                "params": {
                  "query": "",
                  "_es_filters": {},
                  "_es_aggs": {},
                  "_es_sort_fields": {},
                  "size": 10,
                  "from": 0
                  },
                  "dictionary": {
                    //  add dictionary restricting _es_filters and _es_aggs params
                    // Use the dictionary example provided in repo: https://github.com/elastic/search-application-client/blob/main/bin/request_schema.json
                    }
                }
           }
}
```

If a match was found, this will return the results with a highlight field. For example:

```js
{
  "hits": [
    {
      "_index": "movies",
      "_type": "_doc",
      "_id": "1",
      "_score": 0.2876821,
      "_source": {
        "title": "The Great Gatsby",
        "plot": "The Great Gatsby is a novel by F. Scott Fitzgerald that follows the story of Jay Gatsby, a wealthy and mysterious man, as he tries to win back the love of his life, Daisy Buchanan."
      },
      "highlight": {
        "title": ["The Great <em>Gatsby</em>"],
        "plot": [
          "The Great <em>Gatsby</em> is a novel by F. Scott Fitzgerald that follows the story of <em>Jay</em> <em>Gatsby</em>, a wealthy and mysterious man, as he tries to win back the love of his life, Daisy Buchanan."
        ]
      }
    }
  ]
}
```


#### Highlighting helper [search-application-client-client-features-highlight-helpers] 

When displaying the fields in the frontend, you will need to first determine if the field has a highlight. To simplify this, we provide a helper.

```js
import Client, { Highlight } from '@elastic/search-application-client'

// example React component
const ResultsList = ({ hits } ) => {
  return hits.map((hit) => (
    <div className="result">
       <div className="title">{Highlight(hit, "title")}</div>
       <div className="description">{Highlight(hit, "plot")}</div>
    </div>
  ))
}
```


### Pagination [search-application-client-client-features-pagination] 

To use pagination, set the page number and the page size. By default, the page size is 10. The `size` and `from` parameters allow you to control the page and number of hits returned in the response.

We can do this using the client with the `setSize` and `setFrom` methods.

```js
// page 1
const results = await request()
 .setSize(20)
 .setFrom(0)
 .search()

// page 2
const results = await request()
 .setSize(20)
 .setFrom(20)
 .search()
```


## Sorting [search-application-client-client-features-sorting] 

To use sorting, specify the field name and the sort order or `pass _score` to sort by relevance. Requires the `_es_sort_fields_fields` param in the search template. Refer to our [example template](#search-application-client-client-template-example) to see where this is used.

By default, the results will be sorted in order of score. If you need to sort on a field other than the score, use the `setSort` method with an array of objects.

```js
const results = await request()
 .setSort([{ year: 'asc' }, '_score'])
 .search()
```


### Filtering [search-application-client-client-features-filter] 

The Search application client also supports filters and facets. To use these, you need to add two parameters:

* `_es_filters`
* `_es_aggs`

Refer to our [example template](#search-application-client-client-template-example) to see where these are used.


#### Base Filtering [search-application-client-client-features-filter-base] 

With a template that’s configured to use filters, use the `setFilter` method to add filters to your query.

The boilerplate template schema only supports term, range, match, nested, geo_bounding_box and geo_distance filters. If you need to use a particular clause, you can update the template schema.

Below is an example of using `setFilter`.

```js
// return only "star wars" movies that are rated PG
const results = await request()
  .query('star wars')
  .setFilter({
    term: {
      'rated.enum': 'PG',
    },
  })
  .search()
```


### Facets [search-application-client-client-features-facets] 

The client supports the ability to configure facets with your results. Specify facets in the client initialization call. For example, say we want to add facets for actors, directors and IMDB rating.

```js
const request = Client(
  'my-example-app', // search application name
  'https://d1bd36862ce54c7b903e2aacd4cd7f0a.us-east4.gcp.elastic-cloud.com:443', // api-host
  'api-key-from-connect-page', // api-key
  {
    facets: {
      actors: {
        type: 'terms',
        field: 'actors.keyword',
        disjunctive: true,
      },
      directors: {
        type: 'terms',
        field: 'director.keyword',
        size: 20,
        disjunctive: true,
      },
      imdbrating: {
        type: 'stats',
        field: 'imdbrating',
      },
    },
  }
)
```

::::{note} 
In {{es}}, the `keyword` type is used for fields that need to be searchable in their exact, unmodified form. This means these queries are case-sensitive. We use this type for facets because facets require aggregating and filtering data based on exact values or terms.

::::


Use the `addFacetFilter` method to add facets to your query.

In the following example, we only want to return movies:

* Featuring Harrison Ford as actor
* Directed by George Lucas *or* Ridley Scott
* With an IMBD rating greater than 7.5

```js
const results = await request()
  .addFacetFilter('actors', 'Harrison Ford')
  .addFacetFilter('directors', 'George Lucas')
  .addFacetFilter('directors', 'Ridley Scott')
  .addFacetFilter('imdbrating', {
    gte: 7.5,
  })
  .search()
```

You can access the facets in the results:

```js
{
  "took": 1,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0,
    "hits": [
      {
        "_index": "imdb_movies",
        "_id": "tt0076759",
        "_score": 0,
        "_source": {
          "title": "Star Wars: Episode IV - A New Hope",
          "actors": [
            "Mark Hamill",
            "Harrison Ford",
            "Carrie Fisher",
            "Peter Cushing"
          ],
          "plot": "Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, a wookiee and two droids to save the universe from the Empire's world-destroying battle-station, while also attempting to rescue Princess Leia from the evil Darth Vader.",
          "poster": "https://s3-eu-west-1.amazonaws.com/imdbimages/images/MV5BMTU4NTczODkwM15BMl5BanBnXkFtZTcwMzEyMTIyMw@@._V1_SX300.jpg"
        }
      },
      {
        "_index": "imdb_movies",
        "_id": "tt0083658",
        "_score": 0,
        "_source": {
          "title": "Blade Runner",
          "actors": [
            "Harrison Ford",
            "Rutger Hauer",
            "Sean Young",
            "Edward James Olmos"
          ],
          "plot": "Deckard, a blade runner, has to track down and terminate 4 replicants who hijacked a ship in space and have returned to Earth seeking their maker.",
          "poster": "https://s3-eu-west-1.amazonaws.com/imdbimages/images/MV5BMTA4MDQxNTk2NDheQTJeQWpwZ15BbWU3MDE2NjIyODk@._V1_SX300.jpg"
        }
      }
    ]
  },
  "aggregations": {},
  "facets": [
    {
      "name": "imdbrating_facet",
      "stats": {
        "min": 8.300000190734863,
        "max": 8.800000190734863,
        "avg": 8.550000190734863,
        "sum": 17.100000381469727,
        "count": 2
      }
    },
    {
      "name": "actors_facet",
      "entries": [
        {
          "value": "Harrison Ford",
          "count": 2
        },
        {
          "value": "Carrie Fisher",
          "count": 1
        },
        {
          "value": "Edward James Olmos",
          "count": 1
        },
        {
          "value": "Mark Hamill",
          "count": 1
        },
        {
          "value": "Peter Cushing",
          "count": 1
        },
        {
          "value": "Rutger Hauer",
          "count": 1
        },
        {
          "value": "Sean Young",
          "count": 1
        }
      ]
    },
    {
      "name": "directors_facet",
      "entries": [
        {
          "value": "Steven Spielberg",
          "count": 3
        },
        {
          "value": "Andrew Davis",
          "count": 1
        },
        {
          "value": "George Lucas",
          "count": 1
        },
        {
          "value": "Irvin Kershner",
          "count": 1
        },
        {
          "value": "Richard Marquand",
          "count": 1
        },
        {
          "value": "Ridley Scott",
          "count": 1
        }
      ]
    }
  ]
}
```

