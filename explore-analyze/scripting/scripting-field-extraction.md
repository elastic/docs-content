---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/scripting-field-extraction.html
---

# Field extraction [scripting-field-extraction]

The goal of field extraction is simple; you have fields in your data with a bunch of information, but you only want to extract pieces and parts.

There are two options at your disposal:

* [Grok](grok.md) is a regular expression dialect that supports aliased expressions that you can reuse. Because Grok sits on top of regular expressions (regex), any regular expressions are valid in grok as well.
* [Dissect](dissect.md) extracts structured fields out of text, using delimiters to define the matching pattern. Unlike grok, dissect doesn’t use regular expressions.

Let’s start with a simple example by adding the `@timestamp` and `message` fields to the `my-index` mapping as indexed fields. To remain flexible, use `wildcard` as the field type for `message`:

```console
PUT /my-index/
{
  "mappings": {
    "properties": {
      "@timestamp": {
        "format": "strict_date_optional_time||epoch_second",
        "type": "date"
      },
      "message": {
        "type": "wildcard"
      }
    }
  }
}
```

After mapping the fields you want to retrieve, index a few records from your log data into {{es}}. The following request uses the [bulk API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html) to index raw log data into `my-index`. Instead of indexing all of your log data, you can use a small sample to experiment with runtime fields.

```console
POST /my-index/_bulk?refresh
{"index":{}}
{"timestamp":"2020-04-30T14:30:17-05:00","message":"40.135.0.0 - - [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
{"index":{}}
{"timestamp":"2020-04-30T14:30:53-05:00","message":"232.0.0.0 - - [30/Apr/2020:14:30:53 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
{"index":{}}
{"timestamp":"2020-04-30T14:31:12-05:00","message":"26.1.0.0 - - [30/Apr/2020:14:31:12 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
{"index":{}}
{"timestamp":"2020-04-30T14:31:19-05:00","message":"247.37.0.0 - - [30/Apr/2020:14:31:19 -0500] \"GET /french/splash_inet.html HTTP/1.0\" 200 3781"}
{"index":{}}
{"timestamp":"2020-04-30T14:31:22-05:00","message":"247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0"}
{"index":{}}
{"timestamp":"2020-04-30T14:31:27-05:00","message":"252.0.0.0 - - [30/Apr/2020:14:31:27 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
{"index":{}}
{"timestamp":"2020-04-30T14:31:28-05:00","message":"not a valid apache log"}
```


## Extract an IP address from a log message (Grok) [field-extraction-ip]

If you want to retrieve results that include `clientip`, you can add that field as a runtime field in the mapping. The following runtime script defines a grok pattern that extracts structured fields out of the `message` field.

The script matches on the `%{{COMMONAPACHELOG}}` log pattern, which understands the structure of Apache logs. If the pattern matches (`clientip != null`), the script emits the value of the matching IP address. If the pattern doesn’t match, the script just returns the field value without crashing.

```console
PUT my-index/_mappings
{
  "runtime": {
    "http.clientip": {
      "type": "ip",
      "script": """
        String clientip=grok('%{COMMONAPACHELOG}').extract(doc["message"].value)?.clientip;
        if (clientip != null) emit(clientip); <1>
      """
    }
  }
}
```

1. This condition ensures that the script doesn’t emit anything even if the pattern of the message doesn’t match.


You can define a simple query to run a search for a specific IP address and return all related fields. Use the `fields` parameter of the search API to retrieve the `http.clientip` runtime field.

```console
GET my-index/_search
{
  "query": {
    "match": {
      "http.clientip": "40.135.0.0"
    }
  },
  "fields" : ["http.clientip"]
}
```

The response includes documents where the value for `http.clientip` matches `40.135.0.0`.

```console-result
{
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my-index",
        "_id" : "Rq-ex3gBA_A0V6dYGLQ7",
        "_score" : 1.0,
        "_source" : {
          "timestamp" : "2020-04-30T14:30:17-05:00",
          "message" : "40.135.0.0 - - [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"
        },
        "fields" : {
          "http.clientip" : [
            "40.135.0.0"
          ]
        }
      }
    ]
  }
}
```


## Parse a string to extract part of a field (Dissect) [field-extraction-parse]

Instead of matching on a log pattern like in the [previous example](#field-extraction-ip), you can just define a dissect pattern to include the parts of the string that you want to discard.

For example, the log data at the start of this section includes a `message` field. This field contains several pieces of data:

```js
"message" : "247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0"
```

You can define a dissect pattern in a runtime field to extract the [HTTP response code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status), which is `304` in the previous example.

```console
PUT my-index/_mappings
{
  "runtime": {
    "http.response": {
      "type": "long",
      "script": """
        String response=dissect('%{clientip} %{ident} %{auth} [%{@timestamp}] "%{verb} %{request} HTTP/%{httpversion}" %{response} %{size}').extract(doc["message"].value)?.response;
        if (response != null) emit(Integer.parseInt(response));
      """
    }
  }
}
```

You can then run a query to retrieve a specific HTTP response using the `http.response` runtime field:

```console
GET my-index/_search
{
  "query": {
    "match": {
      "http.response": "304"
    }
  },
  "fields" : ["http.response"]
}
```

The response includes a single document where the HTTP response is `304`:

```console-result
{
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my-index",
        "_id" : "Sq-ex3gBA_A0V6dYGLQ7",
        "_score" : 1.0,
        "_source" : {
          "timestamp" : "2020-04-30T14:31:22-05:00",
          "message" : "247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0"
        },
        "fields" : {
          "http.response" : [
            304
          ]
        }
      }
    ]
  }
}
```


## Split values in a field by a separator (Dissect) [field-extraction-split]

Let’s say you want to extract part of a field like in the previous example, but you want to split on specific values. You can use a dissect pattern to extract only the information that you want, and also return that data in a specific format.

For example, let’s say you have a bunch of garbage collection (gc) log data from {{es}} in this format:

```txt
[2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]   class space    used 266K, capacity 384K, committed 384K, reserved 1048576K
```

You only want to extract the `used`, `capacity`, and `committed` data, along with the associated values. Let’s index some a few documents containing log data to use as an example:

```console
POST /my-index/_bulk?refresh
{"index":{}}
{"gc": "[2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]   class space    used 266K, capacity 384K, committed 384K, reserved 1048576K"}
{"index":{}}
{"gc": "[2021-03-24T20:27:24.184+0000][90239][gc,heap,exit]   class space    used 15255K, capacity 16726K, committed 16844K, reserved 1048576K"}
{"index":{}}
{"gc": "[2021-03-24T20:27:24.184+0000][90239][gc,heap,exit]  Metaspace       used 115409K, capacity 119541K, committed 120248K, reserved 1153024K"}
{"index":{}}
{"gc": "[2021-04-19T15:03:21.735+0000][84408][gc,heap,exit]   class space    used 14503K, capacity 15894K, committed 15948K, reserved 1048576K"}
{"index":{}}
{"gc": "[2021-04-19T15:03:21.735+0000][84408][gc,heap,exit]  Metaspace       used 107719K, capacity 111775K, committed 112724K, reserved 1146880K"}
{"index":{}}
{"gc": "[2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]  class space  used 266K, capacity 367K, committed 384K, reserved 1048576K"}
```

Looking at the data again, there’s a timestamp, some other data that you’re not interested in, and then the `used`, `capacity`, and `committed` data:

```txt
[2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]   class space    used 266K, capacity 384K, committed 384K, reserved 1048576K
```

You can assign variables to each part of the data in the `gc` field, and then return only the parts that you want. Anything in curly braces `{}` is considered a variable. For example, the variables `[%{@timestamp}][%{{code}}][%{{desc}}]` will match the first three chunks of data, all of which are in square brackets `[]`.

```txt
[%{@timestamp}][%{code}][%{desc}]  %{ident} used %{usize}, capacity %{csize}, committed %{comsize}, reserved %{rsize}
```

Your dissect pattern can include the terms `used`, `capacity`, and `committed` instead of using variables, because you want to return those terms exactly. You also assign variables to the values you want to return, such as `%{{usize}}`, `%{{csize}}`, and `%{{comsize}}`. The separator in the log data is a comma, so your dissect pattern also needs to use that separator.

Now that you have a dissect pattern, you can include it in a Painless script as part of a runtime field. The script uses your dissect pattern to split apart the `gc` field, and then returns exactly the information that you want as defined by the `emit` method. Because dissect uses simple syntax, you just need to tell it exactly what you want.

The following pattern tells dissect to return the term `used`, a blank space, the value from `gc.usize`, and a comma. This pattern repeats for the other data that you want to retrieve. While this pattern might not be as useful in production, it provides a lot of flexibility to experiment with and manipulate your data. In a production setting, you might just want to use `emit(gc.usize)` and then aggregate on that value or use it in computations.

```painless
emit("used" + ' ' + gc.usize + ', ' + "capacity" + ' ' + gc.csize + ', ' + "committed" + ' ' + gc.comsize)
```

Putting it all together, you can create a runtime field named `gc_size` in a search request. Using the [`fields` option](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-fields.html#search-fields-param), you can retrieve all values for the `gc_size` runtime field. This query also includes a bucket aggregation to group your data.

```console
GET my-index/_search
{
  "runtime_mappings": {
    "gc_size": {
      "type": "keyword",
      "script": """
        Map gc=dissect('[%{@timestamp}][%{code}][%{desc}]  %{ident} used %{usize}, capacity %{csize}, committed %{comsize}, reserved %{rsize}').extract(doc["gc.keyword"].value);
        if (gc != null) emit("used" + ' ' + gc.usize + ', ' + "capacity" + ' ' + gc.csize + ', ' + "committed" + ' ' + gc.comsize);
      """
    }
  },
  "size": 1,
  "aggs": {
    "sizes": {
      "terms": {
        "field": "gc_size",
        "size": 10
      }
    }
  },
  "fields" : ["gc_size"]
}
```

The response includes the data from the `gc_size` field, formatted exactly as you defined it in the dissect pattern!

```console-result
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 6,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my-index",
        "_id" : "GXx3H3kBKGE42WRNlddJ",
        "_score" : 1.0,
        "_source" : {
          "gc" : "[2021-04-27T16:16:34.699+0000][82460][gc,heap,exit]   class space    used 266K, capacity 384K, committed 384K, reserved 1048576K"
        },
        "fields" : {
          "gc_size" : [
            "used 266K, capacity 384K, committed 384K"
          ]
        }
      }
    ]
  },
  "aggregations" : {
    "sizes" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : "used 107719K, capacity 111775K, committed 112724K",
          "doc_count" : 1
        },
        {
          "key" : "used 115409K, capacity 119541K, committed 120248K",
          "doc_count" : 1
        },
        {
          "key" : "used 14503K, capacity 15894K, committed 15948K",
          "doc_count" : 1
        },
        {
          "key" : "used 15255K, capacity 16726K, committed 16844K",
          "doc_count" : 1
        },
        {
          "key" : "used 266K, capacity 367K, committed 384K",
          "doc_count" : 1
        },
        {
          "key" : "used 266K, capacity 384K, committed 384K",
          "doc_count" : 1
        }
      ]
    }
  }
}
```

