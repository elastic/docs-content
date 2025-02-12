---
applies:
  stack:
  serverless:
navigation_title: "Painless examples"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-painless-examples.html
---

# Painless examples [transform-painless-examples]

::::{important} 
The examples that use the `scripted_metric` aggregation are not supported on {{es}} Serverless.
::::

These examples demonstrate how to use Painless in {{transforms}}. You can learn more about the Painless scripting language in the [Painless guide](https://www.elastic.co/guide/en/elasticsearch/painless/current/painless-guide.html).

* [Getting top hits by using scripted metric aggregation](#painless-top-hits)
* [Getting time features by using aggregations](#painless-time-features)
* [Getting duration by using bucket script](#painless-bucket-script)
* [Counting HTTP responses by using scripted metric aggregation](#painless-count-http)
* [Comparing indices by using scripted metric aggregations](#painless-compare)
* [Getting web session details by using scripted metric aggregation](#painless-web-session)

::::{note}

* While the context of the following examples is the {{transform}} use case, the Painless scripts in the snippets below can be used in other {{es}} search aggregations, too.
* All the following examples use scripts, {{transforms}} cannot deduce mappings of output fields when the fields are created by a script. {{transforms-cap}} don’t create any mappings in the destination index for these fields, which means they get dynamically mapped. Create the destination index prior to starting the {{transform}} in case you want explicit mappings.

::::

## Getting top hits by using scripted metric aggregation [painless-top-hits]

This snippet shows how to find the latest document, in other words the document with the latest timestamp. From a technical perspective, it helps to achieve the function of a [Top hits](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-top-hits-aggregation.html) by using scripted metric aggregation in a {{transform}}, which provides a metric output.

::::{important}
This example uses a `scripted_metric` aggregation which is not supported on {{es}} Serverless.
::::

```js
"aggregations": {
  "latest_doc": {
    "scripted_metric": {
      "init_script": "state.timestamp_latest = 0L; state.last_doc = ''", <1>
      "map_script": """ <2>
        def current_date = doc['@timestamp'].getValue().toInstant().toEpochMilli();
        if (current_date > state.timestamp_latest)
        {state.timestamp_latest = current_date;
        state.last_doc = new HashMap(params['_source']);}
      """,
      "combine_script": "return state", <3>
      "reduce_script": """ <4>
        def last_doc = '';
        def timestamp_latest = 0L;
        for (s in states) {if (s.timestamp_latest > (timestamp_latest))
        {timestamp_latest = s.timestamp_latest; last_doc = s.last_doc;}}
        return last_doc
      """
    }
  }
}
```

1. The `init_script` creates a long type `timestamp_latest` and a string type `last_doc` in the `state` object.
2. The `map_script` defines `current_date` based on the timestamp of the document, then compares `current_date` with `state.timestamp_latest`, finally returns `state.last_doc` from the shard. By using `new HashMap(...)` you copy the source document, this is important whenever you want to pass the full source object from one phase to the next.
3. The `combine_script` returns `state` from each shard.
4. The `reduce_script` iterates through the value of `s.timestamp_latest` returned by each shard and returns the document with the latest timestamp (`last_doc`). In the response, the top hit (in other words, the `latest_doc`) is nested below the `latest_doc` field.

Check the [scope of scripts](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-scripted-metric-aggregation.html#scripted-metric-aggregation-scope) for detailed explanation on the respective scripts.

You can retrieve the last value in a similar way:

```js
"aggregations": {
  "latest_value": {
    "scripted_metric": {
      "init_script": "state.timestamp_latest = 0L; state.last_value = ''",
      "map_script": """
        def current_date = doc['@timestamp'].getValue().toInstant().toEpochMilli();
        if (current_date > state.timestamp_latest)
        {state.timestamp_latest = current_date;
        state.last_value = params['_source']['value'];}
      """,
      "combine_script": "return state",
      "reduce_script": """
        def last_value = '';
        def timestamp_latest = 0L;
        for (s in states) {if (s.timestamp_latest > (timestamp_latest))
        {timestamp_latest = s.timestamp_latest; last_value = s.last_value;}}
        return last_value
      """
    }
  }
}
```

### Getting top hits by using stored scripts [top-hits-stored-scripts]

You can also use the power of [stored scripts](https://www.elastic.co/guide/en/elasticsearch/reference/current/create-stored-script-api.html) to get the latest value. Stored scripts are updatable, enable collaboration, and avoid duplication across queries.

1. Create the stored scripts:

    ```js
    POST _scripts/last-value-map-init
    {
      "script": {
        "lang": "painless",
        "source": """
            state.timestamp_latest = 0L; state.last_value = ''
        """
      }
    }

    POST _scripts/last-value-map
    {
      "script": {
        "lang": "painless",
        "source": """
          def current_date = doc['@timestamp'].getValue().toInstant().toEpochMilli();
            if (current_date > state.timestamp_latest)
            {state.timestamp_latest = current_date;
            state.last_value = doc[params['key']].value;}
        """
      }
    }

    POST _scripts/last-value-combine
    {
      "script": {
        "lang": "painless",
        "source": """
            return state
        """
      }
    }

    POST _scripts/last-value-reduce
    {
      "script": {
        "lang": "painless",
        "source": """
            def last_value = '';
            def timestamp_latest = 0L;
            for (s in states) {if (s.timestamp_latest > (timestamp_latest))
            {timestamp_latest = s.timestamp_latest; last_value = s.last_value;}}
            return last_value
        """
      }
    }
    ```

2. Use the stored scripts in a scripted metric aggregation.

    ```js
    "aggregations":{
       "latest_value":{
          "scripted_metric":{
             "init_script":{
                "id":"last-value-map-init"
             },
             "map_script":{
                "id":"last-value-map",
                "params":{
                   "key":"field_with_last_value" <1>
                }
             },
             "combine_script":{
                "id":"last-value-combine"
             },
             "reduce_script":{
                "id":"last-value-reduce"
             }
    ```

    1. The parameter `field_with_last_value` can be set any field that you want the latest value for.

## Getting time features by using aggregations [painless-time-features]

This snippet shows how to extract time based features by using Painless in a {{transform}}. The snippet uses an index where `@timestamp` is defined as a `date` type field.

```js
"aggregations": {
  "avg_hour_of_day": { <1>
    "avg":{
      "script": { <2>
        "source": """
          ZonedDateTime date =  doc['@timestamp'].value; <3>
          return date.getHour(); <4>
        """
      }
    }
  },
  "avg_month_of_year": { <5>
    "avg":{
      "script": { <6>
        "source": """
          ZonedDateTime date =  doc['@timestamp'].value; <7>
          return date.getMonthValue(); <8>
        """
      }
    }
  },
 ...
}
```

1. Name of the aggregation.
2. Contains the Painless script that returns the hour of the day.
3. Sets `date` based on the timestamp of the document.
4. Returns the hour value from `date`.
5. Name of the aggregation.
6. Contains the Painless script that returns the month of the year.
7. Sets `date` based on the timestamp of the document.
8. Returns the month value from `date`.

## Getting duration by using bucket script [painless-bucket-script]

This example shows you how to get the duration of a session by client IP from a data log by using [bucket script](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-pipeline-bucket-script-aggregation.html). The example uses the {{kib}} sample web logs dataset.

```console
PUT _transform/data_log
{
  "source": {
    "index": "kibana_sample_data_logs"
  },
  "dest": {
    "index": "data-logs-by-client"
  },
  "pivot": {
    "group_by": {
      "machine.os": {"terms": {"field": "machine.os.keyword"}},
      "machine.ip": {"terms": {"field": "clientip"}}
    },
    "aggregations": {
      "time_frame.lte": {
        "max": {
          "field": "timestamp"
        }
      },
      "time_frame.gte": {
        "min": {
          "field": "timestamp"
        }
      },
      "time_length": { <1>
        "bucket_script": {
          "buckets_path": { <2>
            "min": "time_frame.gte.value",
            "max": "time_frame.lte.value"
          },
          "script": "params.max - params.min" <3>
        }
      }
    }
  }
}
```

1. To define the length of the sessions, we use a bucket script.
2. The bucket path is a map of script variables and their associated path to the buckets you want to use for the variable. In this particular case, `min` and `max` are variables mapped to `time_frame.gte.value` and `time_frame.lte.value`.
3. Finally, the script substracts the start date of the session from the end date which results in the duration of the session.

## Counting HTTP responses by using scripted metric aggregation [painless-count-http]

You can count the different HTTP response types in a web log data set by using scripted metric aggregation as part of the {{transform}}. You can achieve a similar function with filter aggregations, check the [Finding suspicious client IPs](transform-examples.md#example-clientips) example for details.

The example below assumes that the HTTP response codes are stored as keywords in the `response` field of the documents.

::::{important}
This example uses a `scripted_metric` aggregation which is not supported on {{es}} Serverless.
::::

```js
"aggregations": { <1>
  "responses.counts": { <2>
    "scripted_metric": { <3>
      "init_script": "state.responses = ['error':0L,'success':0L,'other':0L]", <4>
      "map_script": """ <5>
        def code = doc['response.keyword'].value;
        if (code.startsWith('5') || code.startsWith('4')) {
          state.responses.error += 1 ;
        } else if(code.startsWith('2')) {
          state.responses.success += 1;
        } else {
          state.responses.other += 1;
        }
        """,
      "combine_script": "state.responses", <6>
      "reduce_script": """ <7>
        def counts = ['error': 0L, 'success': 0L, 'other': 0L];
        for (responses in states) {
          counts.error += responses['error'];
          counts.success += responses['success'];
          counts.other += responses['other'];
        }
        return counts;
        """
      }
    },
  ...
}
```

1. The `aggregations` object of the {{transform}} that contains all aggregations.
2. Object of the `scripted_metric` aggregation.
3. This `scripted_metric` performs a distributed operation on the web log data to count specific types of HTTP responses (error, success, and other).
4. The `init_script` creates a `responses` array in the `state` object with three properties (`error`, `success`, `other`) with long data type.
5. The `map_script` defines `code` based on the `response.keyword` value of the document, then it counts the errors, successes, and other responses based on the first digit of the responses.
6. The `combine_script` returns `state.responses` from each shard.
7. The `reduce_script` creates a `counts` array with the `error`, `success`, and `other` properties, then iterates through the value of `responses` returned by each shard and assigns the different response types to the appropriate properties of the `counts` object; error responses to the error counts, success responses to the success counts, and other responses to the other counts. Finally, returns the `counts` array with the response counts.

## Comparing indices by using scripted metric aggregations [painless-compare]

This example shows how to compare the content of two indices by a {{transform}} that uses a scripted metric aggregation.

::::{important}
This example uses a `scripted_metric` aggregation which is not supported on {{es}} Serverless.
::::

```console
POST _transform/_preview
{
  "id" : "index_compare",
  "source" : { <1>
    "index" : [
      "index1",
      "index2"
    ],
    "query" : {
      "match_all" : { }
    }
  },
  "dest" : { <2>
    "index" : "compare"
  },
  "pivot" : {
    "group_by" : {
      "unique-id" : {
        "terms" : {
          "field" : "<unique-id-field>" <3>
        }
      }
    },
    "aggregations" : {
      "compare" : { <4>
        "scripted_metric" : {
          "map_script" : "state.doc = new HashMap(params['_source'])", <5>
          "combine_script" : "return state", <6>
          "reduce_script" : """ <7>
            if (states.size() != 2) {
              return "count_mismatch"
            }
            if (states.get(0).equals(states.get(1))) {
              return "match"
            } else {
              return "mismatch"
            }
            """
        }
      }
    }
  }
}
```

1. The indices referenced in the `source` object are compared to each other.
2. The `dest` index contains the results of the comparison.
3. The `group_by` field needs to be a unique identifier for each document.
4. Object of the `scripted_metric` aggregation.
5. The `map_script` defines `doc` in the state object. By using `new HashMap(...)` you copy the source document, this is important whenever you want to pass the full source object from one phase to the next.
6. The `combine_script` returns `state` from each shard.
7. The `reduce_script` checks if the size of the indices are equal. If they are not equal, than it reports back a `count_mismatch`. Then it iterates through all the values of the two indices and compare them. If the values are equal, then it returns a `match`, otherwise returns a `mismatch`.

## Getting web session details by using scripted metric aggregation [painless-web-session]

This example shows how to derive multiple features from a single transaction. Let’s take a look on the example source document from the data:

::::{dropdown} Source document
```js
{
  "_index":"apache-sessions",
  "_type":"_doc",
  "_id":"KvzSeGoB4bgw0KGbE3wP",
  "_score":1.0,
  "_source":{
    "@timestamp":1484053499256,
    "apache":{
      "access":{
        "sessionid":"571604f2b2b0c7b346dc685eeb0e2306774a63c2",
        "url":"http://www.leroymerlin.fr/v3/search/search.do?keyword=Carrelage%20salle%20de%20bain",
        "path":"/v3/search/search.do",
        "query":"keyword=Carrelage%20salle%20de%20bain",
        "referrer":"http://www.leroymerlin.fr/v3/p/produits/carrelage-parquet-sol-souple/carrelage-sol-et-mur/decor-listel-et-accessoires-carrelage-mural-l1308217717?resultOffset=0&resultLimit=51&resultListShape=MOSAIC&priceStyle=SALEUNIT_PRICE",
        "user_agent":{
          "original":"Mobile Safari 10.0 Mac OS X (iPad) Apple Inc.",
          "os_name":"Mac OS X (iPad)"
        },
        "remote_ip":"0337b1fa-5ed4-af81-9ef4-0ec53be0f45d",
        "geoip":{
          "country_iso_code":"FR",
          "location":{
            "lat":48.86,
            "lon":2.35
          }
        },
        "response_code":200,
        "method":"GET"
      }
    }
  }
}
...
```

::::

By using the `sessionid` as a group-by field, you are able to enumerate events through the session and get more details of the session by using scripted metric aggregation.

::::{important}
This example uses a `scripted_metric` aggregation which is not supported on {{es}} Serverless.
::::

```js
POST _transform/_preview
{
  "source": {
    "index": "apache-sessions"
  },
  "pivot": {
    "group_by": {
      "sessionid": { <1>
        "terms": {
          "field": "apache.access.sessionid"
        }
      }
    },
    "aggregations": { <2>
      "distinct_paths": {
        "cardinality": {
          "field": "apache.access.path"
        }
      },
      "num_pages_viewed": {
        "value_count": {
          "field": "apache.access.url"
        }
      },
      "session_details": {
        "scripted_metric": {
          "init_script": "state.docs = []", <3>
          "map_script": """ <4>
            Map span = [
              '@timestamp':doc['@timestamp'].value,
              'url':doc['apache.access.url'].value,
              'referrer':doc['apache.access.referrer'].value
            ];
            state.docs.add(span)
          """,
          "combine_script": "return state.docs;", <5>
          "reduce_script": """ <6>
            def all_docs = [];
            for (s in states) {
              for (span in s) {
                all_docs.add(span);
              }
            }
            all_docs.sort((HashMap o1, HashMap o2)->o1['@timestamp'].toEpochMilli().compareTo(o2['@timestamp'].toEpochMilli()));
            def size = all_docs.size();
            def min_time = all_docs[0]['@timestamp'];
            def max_time = all_docs[size-1]['@timestamp'];
            def duration = max_time.toEpochMilli() - min_time.toEpochMilli();
            def entry_page = all_docs[0]['url'];
            def exit_path = all_docs[size-1]['url'];
            def first_referrer = all_docs[0]['referrer'];
            def ret = new HashMap();
            ret['first_time'] = min_time;
            ret['last_time'] = max_time;
            ret['duration'] = duration;
            ret['entry_page'] = entry_page;
            ret['exit_path'] = exit_path;
            ret['first_referrer'] = first_referrer;
            return ret;
          """
        }
      }
    }
  }
}
```

1. The data is grouped by `sessionid`.
2. The aggregations counts the number of paths and enumerate the viewed pages during the session.
3. The `init_script` creates an array type `doc` in the `state` object.
4. The `map_script` defines a `span` array with a timestamp, a URL, and a referrer value which are based on the corresponding values of the document, then adds the value of the `span` array to the `doc` object.
5. The `combine_script` returns `state.docs` from each shard.
6. The `reduce_script` defines various objects like `min_time`, `max_time`, and `duration` based on the document fields, then declares a `ret` object, and copies the source document by using `new HashMap ()`. Next, the script defines `first_time`, `last_time`, `duration` and other fields inside the `ret` object based on the corresponding object defined earlier, finally returns `ret`.

The API call results in a similar response:

```js
{
  "num_pages_viewed" : 2.0,
  "session_details" : {
    "duration" : 100300001,
    "first_referrer" : "https://www.bing.com/",
    "entry_page" : "http://www.leroymerlin.fr/v3/p/produits/materiaux-menuiserie/porte-coulissante-porte-interieure-escalier-et-rambarde/barriere-de-securite-l1308218463",
    "first_time" : "2017-01-10T21:22:52.982Z",
    "last_time" : "2017-01-10T21:25:04.356Z",
    "exit_path" : "http://www.leroymerlin.fr/v3/p/produits/materiaux-menuiserie/porte-coulissante-porte-interieure-escalier-et-rambarde/barriere-de-securite-l1308218463?__result-wrapper?pageTemplate=Famille%2FMat%C3%A9riaux+et+menuiserie&resultOffset=0&resultLimit=50&resultListShape=PLAIN&nomenclatureId=17942&priceStyle=SALEUNIT_PRICE&fcr=1&*4294718806=4294718806&*14072=14072&*4294718593=4294718593&*17942=17942"
  },
  "distinct_paths" : 1.0,
  "sessionid" : "000046f8154a80fd89849369c984b8cc9d795814"
},
{
  "num_pages_viewed" : 10.0,
  "session_details" : {
    "duration" : 343100405,
    "first_referrer" : "https://www.google.fr/",
    "entry_page" : "http://www.leroymerlin.fr/",
    "first_time" : "2017-01-10T16:57:39.937Z",
    "last_time" : "2017-01-10T17:03:23.049Z",
    "exit_path" : "http://www.leroymerlin.fr/v3/p/produits/porte-de-douche-coulissante-adena-e168578"
  },
  "distinct_paths" : 8.0,
  "sessionid" : "000087e825da1d87a332b8f15fa76116c7467da6"
}
...
```
