---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/ml-configuring-transform.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Altering data in your datafeed with runtime fields [ml-configuring-transform]

If you use {{dfeeds}}, you can use runtime fields to alter your data before it is analyzed. You can add an optional `runtime_mappings` property to your {{dfeeds}}, where you can specify field types and scripts that evaluate custom expressions without affecting the indices that you’re retrieving the data from.

If your {{dfeed}} defines runtime fields, you can use those fields in your {{anomaly-job}}. For example, you can use the runtime fields in the analysis functions in one or more detectors. Runtime fields can impact search performance based on the computation defined in the runtime script.

::::{note}
Some of these examples use regular expressions. By default, regular expressions are disabled because they circumvent the protection that Painless provides against long running and memory hungry scripts. For more information, see [Painless scripting language](../../scripting/modules-scripting-painless.md).

{{ml-cap}} analysis is case sensitive. For example, "John" is considered to be different than "john". This is one reason you might consider using scripts that convert your strings to upper or lowercase letters.

::::

* [Example 1: Adding two numerical fields](#ml-configuring-transform1)
* [Example 2: Concatenating strings](#ml-configuring-transform2)
* [Example 3: Trimming strings](#ml-configuring-transform3)
* [Example 4: Converting strings to lowercase](#ml-configuring-transform4)
* [Example 5: Converting strings to mixed case formats](#ml-configuring-transform5)
* [Example 6: Replacing tokens](#ml-configuring-transform6)
* [Example 7: Regular expression matching and concatenation](#ml-configuring-transform7)
* [Example 8: Transforming geopoint data](#ml-configuring-transform8)

The following index APIs create and add content to an index that is used in subsequent examples:

```console
PUT /my-index-000001
{
  "mappings":{
    "properties": {
      "@timestamp": { "type": "date" },
      "aborted_count": { "type": "long" },
      "another_field": { "type": "keyword" }, <1>
      "clientip": { "type": "keyword" },
      "coords": {
        "properties": {
          "lat": { "type": "keyword" },
          "lon": { "type": "keyword" }
        }
      },
      "error_count": { "type": "long" },
      "query": { "type": "keyword" },
      "some_field": { "type": "keyword" },
      "tokenstring1":{ "type":"keyword" },
      "tokenstring2":{ "type":"keyword" },
      "tokenstring3":{ "type":"keyword" }
    }
  }
}

PUT /my-index-000001/_doc/1
{
  "@timestamp":"2017-03-23T13:00:00",
  "error_count":36320,
  "aborted_count":4156,
  "some_field":"JOE",
  "another_field":"SMITH  ",
  "tokenstring1":"foo-bar-baz",
  "tokenstring2":"foo bar baz",
  "tokenstring3":"foo-bar-19",
  "query":"www.ml.elastic.co",
  "clientip":"123.456.78.900",
  "coords": {
    "lat" : 41.44,
    "lon":90.5
  }
}
```

1. In this example, string fields are mapped as `keyword` fields to support aggregation. If you want both a full text (`text`) and a keyword (`keyword`) version of the same field, use multi-fields. For more information, see [fields](elasticsearch://reference/elasticsearch/mapping-reference/multi-fields.md).


$$$ml-configuring-transform1$$$

```console
PUT _ml/anomaly_detectors/test1
{
  "analysis_config":{
    "bucket_span": "10m",
    "detectors":[
      {
        "function":"mean",
        "field_name": "total_error_count" <1>
      }
    ]
  },
  "data_description": {
    "time_field":"@timestamp"
  },
  "datafeed_config":{
    "datafeed_id": "datafeed-test1",
    "indices": ["my-index-000001"],
    "runtime_mappings": {
      "total_error_count": { <2>
        "type": "long",
        "script": {
          "source": "emit(doc['error_count'].value + doc['aborted_count'].value)"
        }
      }
    }
  }
}
```

1. A runtime field named `total_error_count` is referenced in the detector within the job.
2. The runtime field is defined in the {{dfeed}}.

This `test1` {{anomaly-job}} contains a detector that uses a runtime field in a mean analysis function. The `datafeed-test1` {{dfeed}} defines the runtime field. It contains a script that adds two fields in the document to produce a "total" error count.

The syntax for the `runtime_mappings` property is identical to that used by {{es}}. For more information, see [Runtime fields](../../../manage-data/data-store/mapping/runtime-fields.md).

You can preview the contents of the {{dfeed}} by using the following API:

```console
GET _ml/datafeeds/datafeed-test1/_preview
```

In this example, the API returns the following results, which contain a sum of the `error_count` and `aborted_count` values:

```js
[
  {
    "@timestamp": 1490274000000,
    "total_error_count": 40476
  }
]
```

::::{note}
This example demonstrates how to use runtime fields, but it contains insufficient data to generate meaningful results.
::::

You can alternatively use {{kib}} to create an advanced {{anomaly-job}} that uses runtime fields. To add the `runtime_mappings` property to your {{dfeed}}, you must use the **Edit JSON** tab. For example:

:::{image} /explore-analyze/images/machine-learning-ml-runtimefields.jpg
:alt: Using runtime_mappings in {{dfeed}} config via {{kib}}
:screenshot:
:::

$$$ml-configuring-transform2$$$

```console
PUT _ml/anomaly_detectors/test2
{
  "analysis_config":{
    "bucket_span": "10m",
    "detectors":[
      {
        "function":"low_info_content",
        "field_name":"my_runtime_field" <1>
      }
    ]
  },
  "data_description": {
    "time_field":"@timestamp"
  },
  "datafeed_config":{
    "datafeed_id": "datafeed-test2",
    "indices": ["my-index-000001"],
    "runtime_mappings": {
      "my_runtime_field": {
        "type": "keyword",
        "script": {
          "source": "emit(doc['some_field'].value + '_' + doc['another_field'].value)" <2>
        }
      }
    }
  }
}

GET _ml/datafeeds/datafeed-test2/_preview
```

1. The runtime field has a generic name in this case, since it is used for various tests in the examples.
2. The runtime field uses the plus (+) operator to concatenate strings.

The preview {{dfeed}} API returns the following results, which show that "JOE" and "SMITH  " have been concatenated and an underscore was added:

```js
[
  {
    "@timestamp": 1490274000000,
    "my_runtime_field": "JOE_SMITH  "
  }
]
```

$$$ml-configuring-transform3$$$

```console
POST _ml/datafeeds/datafeed-test2/_update
{
  "runtime_mappings": {
    "my_runtime_field": {
      "type": "keyword",
      "script": {
        "source": "emit(doc['another_field'].value.trim())" <1>
      }
    }
  }
}

GET _ml/datafeeds/datafeed-test2/_preview
```

1. This runtime field uses the `trim()` function to trim extra white space from a string.

The preview {{dfeed}} API returns the following results, which show that "SMITH  " has been trimmed to "SMITH":

```js
[
  {
    "@timestamp": 1490274000000,
    "my_script_field": "SMITH"
  }
]
```

$$$ml-configuring-transform4$$$

```console
POST _ml/datafeeds/datafeed-test2/_update
{
  "runtime_mappings": {
    "my_runtime_field": {
      "type": "keyword",
      "script": {
        "source": "emit(doc['some_field'].value.toLowerCase())" <1>
      }
    }
  }
}

GET _ml/datafeeds/datafeed-test2/_preview
```

1. This runtime field uses the `toLowerCase` function to convert a string to all lowercase letters. Likewise, you can use the `toUpperCase` function to convert a string to uppercase letters.

The preview {{dfeed}} API returns the following results, which show that "JOE" has been converted to "joe":

```js
[
  {
    "@timestamp": 1490274000000,
    "my_script_field": "joe"
  }
]
```

$$$ml-configuring-transform5$$$

```console
POST _ml/datafeeds/datafeed-test2/_update
{
  "runtime_mappings": {
    "my_runtime_field": {
      "type": "keyword",
      "script": {
        "source": "emit(doc['some_field'].value.substring(0, 1).toUpperCase() + doc['some_field'].value.substring(1).toLowerCase())" <1>
      }
    }
  }
}

GET _ml/datafeeds/datafeed-test2/_preview
```

1. This runtime field is a more complicated example of case manipulation. It uses the `subString()` function to capitalize the first letter of a string and converts the remaining characters to lowercase.

The preview {{dfeed}} API returns the following results, which show that "JOE" has been converted to "Joe":

```js
[
  {
    "@timestamp": 1490274000000,
    "my_script_field": "Joe"
  }
]
```

$$$ml-configuring-transform6$$$

```console
POST _ml/datafeeds/datafeed-test2/_update
{
  "runtime_mappings": {
    "my_runtime_field": {
      "type": "keyword",
      "script": {
        "source": "emit(/\\s/.matcher(doc['tokenstring2'].value).replaceAll('_'))" <1>
      }
    }
  }
}

GET _ml/datafeeds/datafeed-test2/_preview
```

1. This script uses regular expressions to replace white space with underscores.

The preview {{dfeed}} API returns the following results, which show that "foo bar baz" has been converted to "foo_bar_baz":

```js
[
  {
    "@timestamp": 1490274000000,
    "my_script_field": "foo_bar_baz"
  }
]
```

$$$ml-configuring-transform7$$$

```console
POST _ml/datafeeds/datafeed-test2/_update
{
  "runtime_mappings": {
    "my_runtime_field": {
      "type": "keyword",
      "script": {
        "source": "def m = /(.*)-bar-([0-9][0-9])/.matcher(doc['tokenstring3'].value); emit(m.find() ? m.group(1) + '_' + m.group(2) : '');" <1>
      }
    }
  }
}

GET _ml/datafeeds/datafeed-test2/_preview
```

1. This script looks for a specific regular expression pattern and emits the matched groups as a concatenated string. If no match is found, it emits an empty string.

The preview {{dfeed}} API returns the following results, which show that "foo-bar-19" has been converted to "foo_19":

```js
[
  {
    "@timestamp": 1490274000000,
    "my_script_field": "foo_19"
  }
]
```


```console
PUT _ml/anomaly_detectors/test3
{
  "analysis_config":{
    "bucket_span": "10m",
    "detectors":[
      {
        "function":"lat_long",
        "field_name": "my_coordinates"
      }
    ]
  },
  "data_description": {
    "time_field":"@timestamp"
  },
  "datafeed_config":{
    "datafeed_id": "datafeed-test3",
    "indices": ["my-index-000001"],
    "runtime_mappings": {
      "my_coordinates": {
        "type": "keyword",
        "script": {
          "source": "emit(doc['coords.lat'].value + ',' + doc['coords.lon'].value)"
        }
      }
    }
  }
}

GET _ml/datafeeds/datafeed-test3/_preview
```

In {{es}}, location data can be stored in `geo_point` fields but this data type is not supported natively in {{ml}} analytics. This example of a runtime field transforms the data into an appropriate format. For more information, see [Geographic functions](/reference/machine-learning/ml-geo-functions.md).

The preview {{dfeed}} API returns the following results, which show that `41.44` and `90.5` have been combined into "41.44,90.5":

```js
[
  {
    "@timestamp": 1490274000000,
    "my_coordinates": "41.44,90.5"
  }
]
```

$$$ml-configuring-transform8$$$