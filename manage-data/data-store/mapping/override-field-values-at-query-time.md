---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/runtime-override-values.html
applies_to:
  stack: ga
  serverless: ga
---

# Override field values at query time [runtime-override-values]

If you create a runtime field with the same name as a field that already exists in the mapping, the runtime field shadows the mapped field. At query time, {{es}} evaluates the runtime field, calculates a value based on the script, and returns the value as part of the query. Because the runtime field shadows the mapped field, you can override the value returned in search without modifying the mapped field.

For example, let’s say you indexed the following documents into `my-index-000001`:

```console
POST my-index-000001/_bulk?refresh=true
{"index":{}}
{"@timestamp":1516729294000,"model_number":"QVKC92Q","measures":{"voltage":5.2}}
{"index":{}}
{"@timestamp":1516642894000,"model_number":"QVKC92Q","measures":{"voltage":5.8}}
{"index":{}}
{"@timestamp":1516556494000,"model_number":"QVKC92Q","measures":{"voltage":5.1}}
{"index":{}}
{"@timestamp":1516470094000,"model_number":"QVKC92Q","measures":{"voltage":5.6}}
{"index":{}}
{"@timestamp":1516383694000,"model_number":"HG537PU","measures":{"voltage":4.2}}
{"index":{}}
{"@timestamp":1516297294000,"model_number":"HG537PU","measures":{"voltage":4.0}}
```

You later realize that the `HG537PU` sensors aren’t reporting their true voltage. The indexed values are supposed to be 1.7 times higher than the reported values! Instead of reindexing your data, you can define a script in the `runtime_mappings` section of the `_search` request to shadow the `voltage` field and calculate a new value at query time.

If you search for documents where the model number matches `HG537PU`:

```console
GET my-index-000001/_search
{
  "query": {
    "match": {
      "model_number": "HG537PU"
    }
  }
}
```
% TEST[continued]

The response includes indexed values for documents matching model number `HG537PU`:

```console-result
{
  ...
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0296195,
    "hits" : [
      {
        "_index" : "my-index-000001",
        "_id" : "F1BeSXYBg_szTodcYCmk",
        "_score" : 1.0296195,
        "_source" : {
          "@timestamp" : 1516383694000,
          "model_number" : "HG537PU",
          "measures" : {
            "voltage" : 4.2
          }
        }
      },
      {
        "_index" : "my-index-000001",
        "_id" : "l02aSXYBkpNf6QRDO62Q",
        "_score" : 1.0296195,
        "_source" : {
          "@timestamp" : 1516297294000,
          "model_number" : "HG537PU",
          "measures" : {
            "voltage" : 4.0
          }
        }
      }
    ]
  }
}
```
%  TESTRESPONSE[s/.../"took" : $body.took,"timed_out" : $body.timed_out,"_shards" : $body._shards,/]
%  TESTRESPONSE[s/"_id" : "F1BeSXYBg_szTodcYCmk"/"_id": $body.hits.hits.0._id/]
%  TESTRESPONSE[s/"_id" : "l02aSXYBkpNf6QRDO62Q"/"_id": $body.hits.hits.1._id/]

The following request defines a runtime field where the script evaluates the `model_number` field where the value is `HG537PU`. For each match, the script multiplies the value for the `voltage` field by `1.7`.

Using the [`fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md) parameter on the `_search` API, you can retrieve the value that the script calculates for the `measures.voltage` field for documents matching the search request:

```console
POST my-index-000001/_search
{
  "runtime_mappings": {
    "measures.voltage": {
      "type": "double",
      "script": {
        "source":
        """if (doc['model_number.keyword'].value.equals('HG537PU'))
        {emit(1.7 * params._source['measures']['voltage']);}
        else{emit(params._source['measures']['voltage']);}"""
      }
    }
  },
  "query": {
    "match": {
      "model_number": "HG537PU"
    }
  },
  "fields": ["measures.voltage"]
}
```
% TEST[continued]

Looking at the response, the calculated values for `measures.voltage` on each result are `7.14` and `6.8`. That’s more like it! The runtime field calculated this value as part of the search request without modifying the mapped value, which still returns in the response:

```console-result
{
  ...
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0296195,
    "hits" : [
      {
        "_index" : "my-index-000001",
        "_id" : "F1BeSXYBg_szTodcYCmk",
        "_score" : 1.0296195,
        "_source" : {
          "@timestamp" : 1516383694000,
          "model_number" : "HG537PU",
          "measures" : {
            "voltage" : 4.2
          }
        },
        "fields" : {
          "measures.voltage" : [
            7.14
          ]
        }
      },
      {
        "_index" : "my-index-000001",
        "_id" : "l02aSXYBkpNf6QRDO62Q",
        "_score" : 1.0296195,
        "_source" : {
          "@timestamp" : 1516297294000,
          "model_number" : "HG537PU",
          "measures" : {
            "voltage" : 4.0
          }
        },
        "fields" : {
          "measures.voltage" : [
            6.8
          ]
        }
      }
    ]
  }
}
```
%  TESTRESPONSE[s/.../"took" : $body.took,"timed_out" : $body.timed_out,"_shards" : $body._shards,/]
%  TESTRESPONSE[s/"_id" : "F1BeSXYBg_szTodcYCmk"/"_id": $body.hits.hits.0._id/]
%  TESTRESPONSE[s/"_id" : "l02aSXYBkpNf6QRDO62Q"/"_id": $body.hits.hits.1._id/]

