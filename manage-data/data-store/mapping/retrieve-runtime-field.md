---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/runtime-retrieving-fields.html
applies_to:
  stack: ga
  serverless: ga
---

# Retrieve a runtime field [runtime-retrieving-fields]

Use the [`fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md) parameter on the `_search` API to retrieve the values of runtime fields. Runtime fields won’t display in `_source`, but the `fields` API works for all fields, even those that were not sent as part of the original `_source`.

## Define a runtime field to calculate the day of week [runtime-define-field-dayofweek]

For example, the following request adds a runtime field called `day_of_week`. The runtime field includes a script that calculates the day of the week based on the value of the `@timestamp` field. We’ll include `"dynamic":"runtime"` in the request so that new fields are added to the mapping as runtime fields.

```console
PUT my-index-000001/
{
  "mappings": {
    "dynamic": "runtime",
    "runtime": {
      "day_of_week": {
        "type": "keyword",
        "script": {
          "source": "emit(doc['@timestamp'].value.dayOfWeekEnum.getDisplayName(TextStyle.FULL, Locale.ENGLISH))"
        }
      }
    },
    "properties": {
      "@timestamp": {"type": "date"}
    }
  }
}
```


## Ingest some data [runtime-ingest-data]

Let’s ingest some sample data, which will result in two indexed fields: `@timestamp` and `message`.

```console
POST /my-index-000001/_bulk?refresh
{ "index": {}}
{ "@timestamp": "2020-06-21T15:00:01-05:00", "message" : "211.11.9.0 - - [2020-06-21T15:00:01-05:00] \"GET /english/index.html HTTP/1.0\" 304 0"}
{ "index": {}}
{ "@timestamp": "2020-06-21T15:00:01-05:00", "message" : "211.11.9.0 - - [2020-06-21T15:00:01-05:00] \"GET /english/index.html HTTP/1.0\" 304 0"}
{ "index": {}}
{ "@timestamp": "2020-04-30T14:30:17-05:00", "message" : "40.135.0.0 - - [2020-04-30T14:30:17-05:00] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
{ "index": {}}
{ "@timestamp": "2020-04-30T14:30:53-05:00", "message" : "232.0.0.0 - - [2020-04-30T14:30:53-05:00] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
{ "index": {}}
{ "@timestamp": "2020-04-30T14:31:12-05:00", "message" : "26.1.0.0 - - [2020-04-30T14:31:12-05:00] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
{ "index": {}}
{ "@timestamp": "2020-04-30T14:31:19-05:00", "message" : "247.37.0.0 - - [2020-04-30T14:31:19-05:00] \"GET /french/splash_inet.html HTTP/1.0\" 200 3781"}
{ "index": {}}
{ "@timestamp": "2020-04-30T14:31:27-05:00", "message" : "252.0.0.0 - - [2020-04-30T14:31:27-05:00] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"}
{ "index": {}}
{ "@timestamp": "2020-04-30T14:31:29-05:00", "message" : "247.37.0.0 - - [2020-04-30T14:31:29-05:00] \"GET /images/hm_brdl.gif HTTP/1.0\" 304 0"}
{ "index": {}}
{ "@timestamp": "2020-04-30T14:31:29-05:00", "message" : "247.37.0.0 - - [2020-04-30T14:31:29-05:00] \"GET /images/hm_arw.gif HTTP/1.0\" 304 0"}
{ "index": {}}
{ "@timestamp": "2020-04-30T14:31:32-05:00", "message" : "247.37.0.0 - - [2020-04-30T14:31:32-05:00] \"GET /images/nav_bg_top.gif HTTP/1.0\" 200 929"}
{ "index": {}}
{ "@timestamp": "2020-04-30T14:31:43-05:00", "message" : "247.37.0.0 - - [2020-04-30T14:31:43-05:00] \"GET /french/images/nav_venue_off.gif HTTP/1.0\" 304 0"}
```
% TEST[continued]


## Search for the calculated day of week [runtime-search-dayofweek]

The following request uses the search API to retrieve the `day_of_week` field that the original request defined as a runtime field in the mapping. The value for this field is calculated dynamically at query time without reindexing documents or indexing the `day_of_week` field. This flexibility allows you to modify the mapping without changing any field values.

```console
GET my-index-000001/_search
{
  "fields": [
    "@timestamp",
    "day_of_week"
  ],
  "_source": false
}
```
%  TEST[continued]

The previous request returns the `day_of_week` field for all matching documents. We can define another runtime field called `client_ip` that also operates on the `message` field and will further refine the query:

```console
PUT /my-index-000001/_mapping
{
  "runtime": {
    "client_ip": {
      "type": "ip",
      "script" : {
      "source" : "String m = doc[\"message\"].value; int end = m.indexOf(\" \"); emit(m.substring(0, end));"
      }
    }
  }
}
```
% TEST[continued]

Run another query, but search for a specific IP address using the `client_ip` runtime field:

```console
GET my-index-000001/_search
{
  "size": 1,
  "query": {
    "match": {
      "client_ip": "211.11.9.0"
    }
  },
  "fields" : ["*"]
}
```
% TEST[continued]

This time, the response includes only two hits. The value for `day_of_week` (`Sunday`) was calculated at query time using the runtime script defined in the mapping, and the result includes only documents matching the `211.11.9.0` IP address.

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
        "_id" : "oWs5KXYB-XyJbifr9mrz",
        "_score" : 1.0,
        "_source" : {
          "@timestamp" : "2020-06-21T15:00:01-05:00",
          "message" : "211.11.9.0 - - [2020-06-21T15:00:01-05:00] \"GET /english/index.html HTTP/1.0\" 304 0"
        },
        "fields" : {
          "@timestamp" : [
            "2020-06-21T20:00:01.000Z"
          ],
          "client_ip" : [
            "211.11.9.0"
          ],
          "message" : [
            "211.11.9.0 - - [2020-06-21T15:00:01-05:00] \"GET /english/index.html HTTP/1.0\" 304 0"
          ],
          "day_of_week" : [
            "Sunday"
          ]
        }
      }
    ]
  }
}
```
%  TESTRESPONSE[s/.../"took" : $body.took,"timed_out" : $body.timed_out,"_shards" : $body._shards,/]
%  TESTRESPONSE[s/"_id" : "oWs5KXYB-XyJbifr9mrz"/"_id": $body.hits.hits.0._id/]
%  TESTRESPONSE[s/"day_of_week" : [\n\s+"Sunday"\n\s]/"day_of_week": $body.hits.hits.0.fields.day_of_week/]


## Retrieve fields from related indices [lookup-runtime-fields]

The [`fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md) parameter on the `_search` API can also be used to retrieve fields from the related indices via runtime fields with a type of `lookup`.

::::{note}
Fields that are retrieved by runtime fields of type `lookup` can be used to enrich the hits in a search response. It’s not possible to query or aggregate on these fields.
::::


```console
POST ip_location/_doc?refresh
{
  "ip": "192.168.1.1",
  "country": "Canada",
  "city": "Montreal"
}

PUT logs/_doc/1?refresh
{
  "host": "192.168.1.1",
  "message": "the first message"
}

PUT logs/_doc/2?refresh
{
  "host": "192.168.1.2",
  "message": "the second message"
}

POST logs/_search
{
  "runtime_mappings": {
    "location": {
        "type": "lookup", <1>
        "target_index": "ip_location", <2>
        "input_field": "host", <3>
        "target_field": "ip", <4>
        "fetch_fields": ["country", "city"] <5>
    }
  },
  "fields": [
    "host",
    "message",
    "location"
  ],
  "_source": false
}
```

1. Define a runtime field in the main search request with a type of `lookup` that retrieves fields from the target index using the [`term`](elasticsearch://reference/query-languages/query-dsl-term-query.md) queries.
2. The target index where the lookup query executes against
3. A field on the main index whose values are used as the input values of the lookup term query
4. A field on the lookup index which the lookup query searches against
5. A list of fields to retrieve from the lookup index. See the [`fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md) parameter of a search request.


The above search returns the country and city from the `ip_location` index for each ip address of the returned search hits.

```console-result
{
  "took": 3,
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
    "max_score": 1.0,
    "hits": [
      {
        "_index": "logs",
        "_id": "1",
        "_score": 1.0,
        "fields": {
          "host": [ "192.168.1.1" ],
          "location": [
            {
              "city": [ "Montreal" ],
              "country": [ "Canada" ]
            }
          ],
          "message": [ "the first message" ]
        }
      },
      {
        "_index": "logs",
        "_id": "2",
        "_score": 1.0,
        "fields": {
          "host": [ "192.168.1.2" ],
          "message": [ "the second message" ]
        }
      }
    ]
  }
}
```
%  TESTRESPONSE[s/"took": 3/"took": $body.took/]

The response of lookup fields are grouped to maintain the independence of each document from the lookup index. The lookup query for each input value is expected to match at most one document on the lookup index. If the lookup query matches more than one documents, then a random document will be selected.


