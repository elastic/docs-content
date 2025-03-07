---
applies_to:
  stack: ga
  serverless: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/grok.html
---

# Grokking grok [grok]

Grok is a regular expression dialect that supports reusable aliased expressions. Grok works really well with syslog logs, Apache and other webserver logs, mysql logs, and generally any log format that is written for humans and not computer consumption.

Grok sits on top of the [Oniguruma](https://github.com/kkos/oniguruma/blob/master/doc/RE) regular expression library, so any regular expressions are valid in grok. Grok uses this regular expression language to allow naming existing patterns and combining them into more complex patterns that match your fields.

## Grok patterns [grok-syntax]

The {{stack}} ships with numerous [predefined grok patterns](https://github.com/elastic/elasticsearch/blob/master/libs/grok/src/main/resources/patterns/legacy/grok-patterns) that simplify working with grok. The syntax for reusing grok patterns takes one of the following forms:

|     |     |     |
| --- | --- | --- |
| `%{{SYNTAX}}` | `%{SYNTAX:ID}` | `%{SYNTAX:ID:TYPE}` |

`SYNTAX`
:   The name of the pattern that will match your text. For example, `NUMBER` and `IP` are both patterns that are provided within the default patterns set. The `NUMBER` pattern matches data like `3.44`, and the `IP` pattern matches data like `55.3.244.1`.

`ID`
:   The identifier you give to the piece of text being matched. For  example, `3.44` could be the duration of an event, so you might call it `duration`. The string `55.3.244.1` might identify the `client` making a request.

`TYPE`
:   The data type you want to cast your named field. `int`, `long`, `double`, `float` and `boolean` are supported types.

For example, let’s say you have message data that looks like this:

```txt
3.44 55.3.244.1
```

The first value is a number, followed by what appears to be an IP address. You can match this text by using the following grok expression:

```txt
%{NUMBER:duration} %{IP:client}
```


## Migrating to Elastic Common Schema (ECS) [grok-ecs]

To ease migration to the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/current), a new set of ECS-compliant patterns is available in addition to the existing patterns. The new ECS pattern definitions capture event field names that are compliant with the schema.

The ECS pattern set has all of the pattern definitions from the legacy set, and is a drop-in replacement. Use the [`ecs-compatability`](logstash://reference/plugins-filters-grok.md#plugins-filters-grok-ecs_compatibility) setting to switch modes.

New features and enhancements will be added to the ECS-compliant files. The legacy patterns may still receive bug fixes which are backwards compatible.


## Use grok patterns in Painless scripts [grok-patterns]

You can incorporate predefined grok patterns into Painless scripts to extract data. To test your script, use either the [field contexts](elasticsearch://reference/scripting-languages/painless/painless-api-examples.md#painless-execute-runtime-field-context) of the Painless execute API or create a runtime field that includes the script. Runtime fields offer greater flexibility and accept multiple documents, but the Painless execute API is a great option if you don’t have write access on a cluster where you’re testing a script.

::::{tip}
If you need help building grok patterns to match your data, use the [Grok Debugger](../query-filter/tools/grok-debugger.md) tool in {{kib}}.
::::


For example, if you’re working with Apache log data, you can use the `%{{COMMONAPACHELOG}}` syntax, which understands the structure of Apache logs. A sample document might look like this:

```js
"timestamp":"2020-04-30T14:30:17-05:00","message":"40.135.0.0 - -
[30/Apr/2020:14:30:17 -0500] \"GET /images/hm_bg.jpg HTTP/1.0\" 200 24736"
```
%  NOTCONSOLE

To extract the IP address from the `message` field, you can write a Painless script that incorporates the `%{{COMMONAPACHELOG}}` syntax. You can test this script using the [`ip` field context](elasticsearch://reference/scripting-languages/painless/painless-api-examples.md#painless-runtime-ip) of the Painless execute API, but let’s use a runtime field instead.

Based on the sample document, index the `@timestamp` and `message` fields. To remain flexible, use `wildcard` as the field type for `message`:

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

Next, use the [bulk API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-bulk) to index some log data into `my-index`.

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
%  TEST[continued]


## Incorporate grok patterns and scripts in runtime fields [grok-patterns-runtime]

Now you can define a runtime field in the mappings that includes your Painless script and grok pattern. If the pattern matches, the script emits the value of the matching IP address. If the pattern doesn’t match (`clientip != null`), the script just returns the field value without crashing.

```console
PUT my-index/_mappings
{
  "runtime": {
    "http.clientip": {
      "type": "ip",
      "script": """
        String clientip=grok('%{COMMONAPACHELOG}').extract(doc["message"].value)?.clientip;
        if (clientip != null) emit(clientip);
      """
    }
  }
}
```
%  TEST[continued]

Alternatively, you can define the same runtime field but in the context of a search request. The runtime definition and the script are exactly the same as the one defined previously in the index mapping. Just copy that definition into the search request under the `runtime_mappings` section and include a query that matches on the runtime field. This query returns the same results as if you [defined a search query](#grok-pattern-results) for the `http.clientip` runtime field in your index mappings, but only in the context of this specific search:

```console
GET my-index/_search
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


## Return calculated results [grok-pattern-results]

Using the `http.clientip` runtime field, you can define a simple query to run a search for a specific IP address and return all related fields. The [`fields`](elasticsearch://reference/elasticsearch/rest-apis/retrieve-selected-fields.md) parameter on the `_search` API works for all fields, even those that weren’t sent as part of the original `_source`:

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
%  TEST[continued]
%  TEST[s/_search/_search?filter_path=hits/]

The response includes the specific IP address indicated in your search query. The grok pattern within the Painless script extracted this value from the `message` field at runtime.

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
        "_id" : "1iN2a3kBw4xTzEDqyYE0",
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
%  TESTRESPONSE[s/"_id" : "1iN2a3kBw4xTzEDqyYE0"/"_id": $body.hits.hits.0._id/]


