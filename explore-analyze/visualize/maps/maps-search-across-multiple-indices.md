---
applies:
  stack:
  serverless:
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-search-across-multiple-indices.html
---

# Search across multiple indices [maps-search-across-multiple-indices]

Your map might contain multiple {{es}} indices. This can occur when your map contains two or more layers with {{es}} sources from different indices. This can also occur with a single layer with an {{es}} source and a [Term join](terms-join.md).

Searching across multiple indices might sometimes result in empty layers. The most common cause for empty layers are searches for a field that exists in one index, but does not exist in other indices.


## Disable global search for a layer [maps-disable-search-for-layer]

One strategy for eliminating unintentional empty layers from a cross index search is to [disable global search for a layer](maps-search.md#maps-narrow-layer-by-global-search).


## Use _index in a search [maps-add-index-search]

Add [_index](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-index-field.html) to your search to include documents from indices that do not contain a search field.

For example, suppose you have a vector layer showing the `kibana_sample_data_logs` documents and another vector layer with `kibana_sample_data_flights` documents. (See [adding sample data](https://www.elastic.co/guide/en/kibana/current/get-started.html) to install the `kibana_sample_data_logs` and `kibana_sample_data_flights` indices.)

If you query for

```
machine.os.keyword : "osx"
```

the `kibana_sample_data_flights` layer is empty because the index `kibana_sample_data_flights` does not contain the field `machine.os.keyword` and no documents match the query.

:::{image} ../../../images/kibana-global_search_multiple_indices_query1.png
:alt: global search multiple indices query1
:class: screenshot
:::

If you instead query for

```
machine.os.keyword : "osx" or _index : "kibana_sample_data_flights"
```

the `kibana_sample_data_flights` layer includes data.

:::{image} ../../../images/kibana-global_search_multiple_indices_query2.png
:alt: global search multiple indices query2
:class: screenshot
:::

