---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/runtime-indexed.html
applies_to:
  stack: ga
  serverless: ga
---

# Index a runtime field [runtime-indexed]

Runtime fields are defined by the context where they run. For example, you can define runtime fields in the [context of a search query](define-runtime-fields-in-search-request.md) or within the [`runtime` section](map-runtime-field.md) of an index mapping. If you decide to index a runtime field for greater performance, just move the full runtime field definition (including the script) to the context of an index mapping. {{es}} automatically uses these indexed fields to drive queries, resulting in a fast response time. This capability means you can write a script only once, and apply it to any context that supports runtime fields.

::::{note}
Indexing a `composite` runtime field is currently not supported.
::::


You can then use runtime fields to limit the number of fields that {{es}} needs to calculate values for. Using indexed fields in tandem with runtime fields provides flexibility in the data that you index and how you define queries for other fields.

::::{important}
After indexing a runtime field, you cannot update the included script. If you need to change the script, create a new field with the updated script.
::::


For example, let’s say your company wants to replace some old pressure valves. The connected sensors are only capable of reporting a fraction of the true readings. Rather than outfit the pressure valves with new sensors, you decide to calculate the values based on reported readings. Based on the reported data, you define the following fields in your mapping for `my-index-000001`:

```console
PUT my-index-000001/
{
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date"
      },
      "temperature": {
        "type": "long"
      },
      "voltage": {
        "type": "double"
      },
      "node": {
        "type": "keyword"
      }
    }
  }
}
```

You then bulk index some sample data from your sensors. This data includes `voltage` readings for each sensor:

```console
POST my-index-000001/_bulk?refresh=true
{"index":{}}
{"timestamp": 1516729294000, "temperature": 200, "voltage": 5.2, "node": "a"}
{"index":{}}
{"timestamp": 1516642894000, "temperature": 201, "voltage": 5.8, "node": "b"}
{"index":{}}
{"timestamp": 1516556494000, "temperature": 202, "voltage": 5.1, "node": "a"}
{"index":{}}
{"timestamp": 1516470094000, "temperature": 198, "voltage": 5.6, "node": "b"}
{"index":{}}
{"timestamp": 1516383694000, "temperature": 200, "voltage": 4.2, "node": "c"}
{"index":{}}
{"timestamp": 1516297294000, "temperature": 202, "voltage": 4.0, "node": "c"}
```
%  TEST[continued]

After talking to a few site engineers, you realize that the sensors should be reporting at least *double* the current values, but potentially higher. You create a runtime field named `voltage_corrected` that retrieves the current voltage and multiplies it by `2`:

```console
PUT my-index-000001/_mapping
{
  "runtime": {
    "voltage_corrected": {
      "type": "double",
      "script": {
        "source": """
        emit(doc['voltage'].value * params['multiplier'])
        """,
        "params": {
          "multiplier": 2
        }
      }
    }
  }
}
```
%  TEST[continued]

You retrieve the calculated values using the [`fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md) parameter on the `_search` API:

```console
GET my-index-000001/_search
{
  "fields": [
    "voltage_corrected",
    "node"
  ],
  "size": 2
}
```
%  TEST[continued]
%  TEST[s/_search/_search?filter_path=hits/]

After reviewing the sensor data and running some tests, you determine that the multiplier for reported sensor data should be `4`. To gain greater performance, you decide to index the `voltage_corrected` runtime field with the new `multiplier` parameter.

In a new index named `my-index-000001`, copy the `voltage_corrected` runtime field definition into the mappings of the new index. It’s that simple! You can add an optional parameter named `on_script_error` that determines whether to reject the entire document if the script throws an error at index time (default).

```console
PUT my-index-000001/
{
  "mappings": {
    "properties": {
      "timestamp": {
        "type": "date"
      },
      "temperature": {
        "type": "long"
      },
      "voltage": {
        "type": "double"
      },
      "node": {
        "type": "keyword"
      },
      "voltage_corrected": {
        "type": "double",
        "on_script_error": "fail", <1>
        "script": {
          "source": """
        emit(doc['voltage'].value * params['multiplier'])
        """,
          "params": {
            "multiplier": 4
          }
        }
      }
    }
  }
}
```

1. Causes the entire document to be rejected if the script throws an error at index time. Setting the value to `ignore` will register the field in the document’s `_ignored` metadata field and continue indexing.


Bulk index some sample data from your sensors into the `my-index-000001` index:

```console
POST my-index-000001/_bulk?refresh=true
{ "index": {}}
{ "timestamp": 1516729294000, "temperature": 200, "voltage": 5.2, "node": "a"}
{ "index": {}}
{ "timestamp": 1516642894000, "temperature": 201, "voltage": 5.8, "node": "b"}
{ "index": {}}
{ "timestamp": 1516556494000, "temperature": 202, "voltage": 5.1, "node": "a"}
{ "index": {}}
{ "timestamp": 1516470094000, "temperature": 198, "voltage": 5.6, "node": "b"}
{ "index": {}}
{ "timestamp": 1516383694000, "temperature": 200, "voltage": 4.2, "node": "c"}
{ "index": {}}
{ "timestamp": 1516297294000, "temperature": 202, "voltage": 4.0, "node": "c"}
```
%  TEST[continued]

You can now retrieve calculated values in a search query, and find documents based on precise values. The following range query returns all documents where the calculated `voltage_corrected` is greater than or equal to `16`, but less than or equal to `20`. Again, use the [`fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md) parameter on the `_search` API to retrieve the fields you want:

```console
POST my-index-000001/_search
{
  "query": {
    "range": {
      "voltage_corrected": {
        "gte": 16,
        "lte": 20,
        "boost": 1.0
      }
    }
  },
  "fields": ["voltage_corrected", "node"]
}
```
%  TEST[continued]
%  TEST[s/_search/_search?filter_path=hits/]

The response includes the `voltage_corrected` field for the documents that match the range query, based on the calculated value of the included script:

```console-result
{
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my-index-000001",
        "_id" : "yoSLrHgBdg9xpPrUZz_P",
        "_score" : 1.0,
        "_source" : {
          "timestamp" : 1516383694000,
          "temperature" : 200,
          "voltage" : 4.2,
          "node" : "c"
        },
        "fields" : {
          "voltage_corrected" : [
            16.8
          ],
          "node" : [
            "c"
          ]
        }
      },
      {
        "_index" : "my-index-000001",
        "_id" : "y4SLrHgBdg9xpPrUZz_P",
        "_score" : 1.0,
        "_source" : {
          "timestamp" : 1516297294000,
          "temperature" : 202,
          "voltage" : 4.0,
          "node" : "c"
        },
        "fields" : {
          "voltage_corrected" : [
            16.0
          ],
          "node" : [
            "c"
          ]
        }
      }
    ]
  }
}
```
%  TESTRESPONSE[s/"_id" : "yoSLrHgBdg9xpPrUZz_P"/"_id": $body.hits.hits.0._id/]
%  TESTRESPONSE[s/"_id" : "y4SLrHgBdg9xpPrUZz_P"/"_id": $body.hits.hits.1._id/]

