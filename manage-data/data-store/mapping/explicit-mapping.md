---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/explicit-mapping.html
---

# Explicit mapping [explicit-mapping]

You know more about your data than {{es}} can guess, so while dynamic mapping can be useful to get started, at some point you will want to specify your own explicit mappings.

You can create field mappings when you [create an index](#create-mapping) and [add fields to an existing index](#add-field-mapping).


## Create an index with an explicit mapping [create-mapping] 

You can use the [create index](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) API to create a new index with an explicit mapping.

```console
PUT /my-index-000001
{
  "mappings": {
    "properties": {
      "age":    { "type": "integer" },  <1>
      "email":  { "type": "keyword"  }, <2>
      "name":   { "type": "text"  }     <3>
    }
  }
}
```

1. Creates `age`, an [`integer`](https://www.elastic.co/guide/en/elasticsearch/reference/current/number.html) field
2. Creates `email`, a [`keyword`](https://www.elastic.co/guide/en/elasticsearch/reference/current/keyword.html) field
3. Creates `name`, a [`text`](https://www.elastic.co/guide/en/elasticsearch/reference/current/text.html) field



## Add a field to an existing mapping [add-field-mapping] 

You can use the [update mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-put-mapping.html) API to add one or more new fields to an existing index.

The following example adds `employee-id`, a `keyword` field with an [`index`](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-index.html) mapping parameter value of `false`. This means values for the `employee-id` field are stored but not indexed or available for search.

```console
PUT /my-index-000001/_mapping
{
  "properties": {
    "employee-id": {
      "type": "keyword",
      "index": false
    }
  }
}
```


## Update the mapping of a field [update-mapping] 

Except for supported [mapping parameters](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-params.html), you can’t change the mapping or field type of an existing field. Changing an existing field could invalidate data that’s already indexed.

If you need to change the mapping of a field in a data stream’s backing indices, see [Change mappings and settings for a data stream](../index-types/modify-data-stream.md#data-streams-change-mappings-and-settings).

If you need to change the mapping of a field in other indices, create a new index with the correct mapping and [reindex](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-reindex.html) your data into that index.

Renaming a field would invalidate data already indexed under the old field name. Instead, add an [`alias`](https://www.elastic.co/guide/en/elasticsearch/reference/current/field-alias.html) field to create an alternate field name.


## View the mapping of an index [view-mapping] 

You can use the [get mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-get-mapping.html) API to view the mapping of an existing index.

```console
GET /my-index-000001/_mapping
```

The API returns the following response:

```console-result
{
  "my-index-000001" : {
    "mappings" : {
      "properties" : {
        "age" : {
          "type" : "integer"
        },
        "email" : {
          "type" : "keyword"
        },
        "employee-id" : {
          "type" : "keyword",
          "index" : false
        },
        "name" : {
          "type" : "text"
        }
      }
    }
  }
}
```


## View the mapping of specific fields [view-field-mapping] 

If you only want to view the mapping of one or more specific fields, you can use the [get field mapping](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-get-field-mapping.html) API.

This is useful if you don’t need the complete mapping of an index or your index contains a large number of fields.

The following request retrieves the mapping for the `employee-id` field.

```console
GET /my-index-000001/_mapping/field/employee-id
```

The API returns the following response:

```console-result
{
  "my-index-000001" : {
    "mappings" : {
      "employee-id" : {
        "full_name" : "employee-id",
        "mapping" : {
          "employee-id" : {
            "type" : "keyword",
            "index" : false
          }
        }
      }
    }
  }
}
```

