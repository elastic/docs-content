Use the [get index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) API to retrieve the configured value for the `index.routing.allocation.include._tier_preference` setting:

```console
GET /my-index-000001/_settings/index.routing.allocation.include._tier_preference?flat_settings
```

The response looks like this:

```console-result
{
  "my-index-000001": {
    "settings": {
      "index.routing.allocation.include._tier_preference": "data_warm,data_hot" <1>
    }
  }
}
```

1. Represents a comma-separated list of data tier node roles this index is allowed to be allocated on. The first tier in the list has the highest priority and is the tier the index is targeting. In this example, the tier preference is `data_warm,data_hot`, so the index is targeting the `warm` tier. If the warm tier lacks capacity, the index will fall back to the `data_hot` tier.