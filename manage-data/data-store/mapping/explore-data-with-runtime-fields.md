---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/runtime-examples.html
applies_to:
  stack: ga
  serverless: ga
---

# Explore your data with runtime fields [runtime-examples]

Consider a large set of log data that you want to extract fields from. Indexing the data is time consuming and uses a lot of disk space, and you just want to explore the data structure without committing to a schema up front.

You know that your log data contains specific fields that you want to extract. In this case, we want to focus on the `@timestamp` and `message` fields. By using runtime fields, you can define scripts to calculate values at search time for these fields.

## Define indexed fields as a starting point [runtime-examples-define-fields]

You can start with a simple example by adding the `@timestamp` and `message` fields to the `my-index-000001` mapping as indexed fields. To remain flexible, use `wildcard` as the field type for `message`:

```console
PUT /my-index-000001/
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


## Ingest some data [runtime-examples-ingest-data]

After mapping the fields you want to retrieve, index a few records from your log data into {{es}}. The following request uses the [bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) to index raw log data into `my-index-000001`. Instead of indexing all of your log data, you can use a small sample to experiment with runtime fields.

The final document is not a valid Apache log format, but we can account for that scenario in our script.

```console
POST /my-index-000001/_bulk?refresh
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
%  TEST[continued]

At this point, you can view how {{es}} stores your raw data.

```console
GET /my-index-000001
```
%  TEST[continued]

The mapping contains two fields: `@timestamp` and `message`.

```console-result
{
  "my-index-000001" : {
    "aliases" : { },
    "mappings" : {
      "properties" : {
        "@timestamp" : {
          "type" : "date",
          "format" : "strict_date_optional_time||epoch_second"
        },
        "message" : {
          "type" : "wildcard"
        },
        "timestamp" : {
          "type" : "date"
        }
      }
    },
    ...
  }
}
```
%  TESTRESPONSE[s/.../"settings": $body.my-index-000001.settings/]


## Define a runtime field with a grok pattern [runtime-examples-grok]

If you want to retrieve results that include `clientip`, you can add that field as a runtime field in the mapping. The following runtime script defines a [grok pattern](../../../explore-analyze/scripting/grok.md) that extracts structured fields out of a single text field within a document. A grok pattern is like a regular expression that supports aliased expressions that you can reuse.

The script matches on the `%{{COMMONAPACHELOG}}` log pattern, which understands the structure of Apache logs. If the pattern matches (`clientip != null`), the script emits the value of the matching IP address. If the pattern doesn’t match, the script just returns the field value without crashing.

```console
PUT my-index-000001/_mappings
{
  "runtime": {
    "http.client_ip": {
      "type": "ip",
      "script": """
        String clientip=grok('%{COMMONAPACHELOG}').extract(doc["message"].value)?.clientip;
        if (clientip != null) emit(clientip); <1>
      """
    }
  }
}
```
%  TEST[continued]

1. This condition ensures that the script doesn’t crash even if the pattern of the message doesn’t match.


Alternatively, you can define the same runtime field but in the context of a search request. The runtime definition and the script are exactly the same as the one defined previously in the index mapping. Just copy that definition into the search request under the `runtime_mappings` section and include a query that matches on the runtime field. This query returns the same results as if you defined a search query for the `http.clientip` runtime field in your index mappings, but only in the context of this specific search:

```console
GET my-index-000001/_search
{
  "runtime_mappings": {
    "http.clientip": {
      "type": "ip",
      "script": """
        String clientip=grok('%{COMMONAPACHELOG}').extract(doc["message"].value)?.clientip;
        if (clientip != null) emit(clientip);
      """
    }
  },
  "query": {
    "match": {
      "http.clientip": "40.135.0.0"
    }
  },
  "fields" : ["http.clientip"]
}
```
%  TEST[continued]


## Define a composite runtime field [runtime-examples-grok-composite]

You can also define a *composite* runtime field to emit multiple fields from a single script. You can define a set of typed subfields and emit a map of values. At search time, each subfield retrieves the value associated with their name in the map. This means that you only need to specify your grok pattern one time and can return multiple values:

```console
PUT my-index-000001/_mappings
{
  "runtime": {
    "http": {
      "type": "composite",
      "script": "emit(grok(\"%{COMMONAPACHELOG}\").extract(doc[\"message\"].value))",
      "fields": {
        "clientip": {
          "type": "ip"
        },
        "verb": {
          "type": "keyword"
        },
        "response": {
          "type": "long"
        }
      }
    }
  }
}
```
%  TEST[continued]

### Search for a specific IP address [runtime-examples-grok-ip]

Using the `http.clientip` runtime field, you can define a simple query to run a search for a specific IP address and return all related fields.

```console
GET my-index-000001/_search
{
  "query": {
    "match": {
      "http.clientip": "40.135.0.0"
    }
  },
  "fields" : ["*"]
}
```
%  TEST[continued]

The API returns the following result. Because `http` is a `composite` runtime field, the response includes each of the sub-fields under `fields`, including any associated values that match the query. Without building your data structure in advance, you can search and explore your data in meaningful ways to experiment and determine which fields to index.

```console-result
{
  ...
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my-index-000001",
        "_id" : "sRVHBnwBB-qjgFni7h_O",
        "_score" : 1.0,
        "_source" : {
          "timestamp" : "2020-04-30T14:30:17-05:00",
          "message" : "40.135.0.0 - - [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"
        },
        "fields" : {
          "http.verb" : [
            "GET"
          ],
          "http.clientip" : [
            "40.135.0.0"
          ],
          "http.response" : [
            200
          ],
          "message" : [
            "40.135.0.0 - - [30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"
          ],
          "http.client_ip" : [
            "40.135.0.0"
          ],
          "timestamp" : [
            "2020-04-30T19:30:17.000Z"
          ]
        }
      }
    ]
  }
}
```
%  TESTRESPONSE[s/.../"took" : $body.took,"timed_out" : $body.timed_out,"_shards" : $body._shards,/]
%  TESTRESPONSE[s/"_id" : "sRVHBnwBB-qjgFni7h_O"/"_id": $body.hits.hits.0._id/]

Also, remember that `if` statement in the script?

```painless
if (clientip != null) emit(clientip);
```

If the script didn’t include this condition, the query would fail on any shard that doesn’t match the pattern. By including this condition, the query skips data that doesn’t match the grok pattern.


### Search for documents in a specific range [runtime-examples-grok-range]

You can also run a [range query](elasticsearch://reference/query-languages/query-dsl-range-query.md) that operates on the `timestamp` field. The following query returns any documents where the `timestamp` is greater than or equal to `2020-04-30T14:31:27-05:00`:

```console
GET my-index-000001/_search
{
  "query": {
    "range": {
      "timestamp": {
        "gte": "2020-04-30T14:31:27-05:00"
      }
    }
  }
}
```
%  TEST[continued]

The response includes the document where the log format doesn’t match, but the timestamp falls within the defined range.

```console-result
{
  ...
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my-index-000001",
        "_id" : "hdEhyncBRSB6iD-PoBqe",
        "_score" : 1.0,
        "_source" : {
          "timestamp" : "2020-04-30T14:31:27-05:00",
          "message" : "252.0.0.0 - - [30/Apr/2020:14:31:27 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"
        }
      },
      {
        "_index" : "my-index-000001",
        "_id" : "htEhyncBRSB6iD-PoBqe",
        "_score" : 1.0,
        "_source" : {
          "timestamp" : "2020-04-30T14:31:28-05:00",
          "message" : "not a valid apache log"
        }
      }
    ]
  }
}
```
%  TESTRESPONSE[s/.../"took" : $body.took,"timed_out" : $body.timed_out,"_shards" : $body._shards,/]
%  TESTRESPONSE[s/"_id" : "hdEhyncBRSB6iD-PoBqe"/"_id": $body.hits.hits.0._id/]
%  TESTRESPONSE[s/"_id" : "htEhyncBRSB6iD-PoBqe"/"_id": $body.hits.hits.1._id/]



## Define a runtime field with a dissect pattern [runtime-examples-dissect]

If you don’t need the power of regular expressions, you can use [dissect patterns](elasticsearch://reference/ingestion-tools/enrich-processor/dissect-processor.md) instead of grok patterns. Dissect patterns match on fixed delimiters but are typically faster than grok.

You can use dissect to achieve the same results as parsing the Apache logs with a [grok pattern](#runtime-examples-grok). Instead of matching on a log pattern, you include the parts of the string that you want to discard. Paying special attention to the parts of the string you want to discard will help build successful dissect patterns.

```console
PUT my-index-000001/_mappings
{
  "runtime": {
    "http.client.ip": {
      "type": "ip",
      "script": """
        String clientip=dissect('%{clientip} %{ident} %{auth} [%{@timestamp}] "%{verb} %{request} HTTP/%{httpversion}" %{status} %{size}').extract(doc["message"].value)?.clientip;
        if (clientip != null) emit(clientip);
      """
    }
  }
}
```
%  TEST[continued]

Similarly, you can define a dissect pattern to extract the [HTTP response code](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status):

```console
PUT my-index-000001/_mappings
{
  "runtime": {
    "http.responses": {
      "type": "long",
      "script": """
        String response=dissect('%{clientip} %{ident} %{auth} [%{@timestamp}] "%{verb} %{request} HTTP/%{httpversion}" %{response} %{size}').extract(doc["message"].value)?.response;
        if (response != null) emit(Integer.parseInt(response));
      """
    }
  }
}
```
%  TEST[continued]

You can then run a query to retrieve a specific HTTP response using the `http.responses` runtime field. Use the `fields` parameter of the `_search` request to indicate which fields you want to retrieve:

```console
GET my-index-000001/_search
{
  "query": {
    "match": {
      "http.responses": "304"
    }
  },
  "fields" : ["http.client_ip","timestamp","http.verb"]
}
```
%  TEST[continued]

The response includes a single document where the HTTP response is `304`:

```console-result
{
  ...
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my-index-000001",
        "_id" : "A2qDy3cBWRMvVAuI7F8M",
        "_score" : 1.0,
        "_source" : {
          "timestamp" : "2020-04-30T14:31:22-05:00",
          "message" : "247.37.0.0 - - [30/Apr/2020:14:31:22 -0500] \"GET /images/hm_nbg.jpg HTTP/1.0\" 304 0"
        },
        "fields" : {
          "http.verb" : [
            "GET"
          ],
          "http.client_ip" : [
            "247.37.0.0"
          ],
          "timestamp" : [
            "2020-04-30T19:31:22.000Z"
          ]
        }
      }
    ]
  }
}
```
%  TESTRESPONSE[s/.../"took" : $body.took,"timed_out" : $body.timed_out,"_shards" : $body._shards,/]
%  TESTRESPONSE[s/"_id" : "A2qDy3cBWRMvVAuI7F8M"/"_id": $body.hits.hits.0._id/]


