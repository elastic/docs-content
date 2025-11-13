---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/maps-search-across-multiple-indices.html
description: Query data from multiple Elasticsearch indices in Maps to visualize combined datasets. Build maps with layers from different data sources and indices.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Search across multiple indices [maps-search-across-multiple-indices]

When maps contain layers from different {{es}} indices, global searches may produce unexpected results or empty layers. This occurs when search queries reference fields that exist in some indices but not others.

Understanding how to handle multi-index scenarios helps you avoid empty layers and create effective search strategies across diverse data sources.


## Disable global search for a layer [maps-disable-search-for-layer]

One strategy for eliminating unintentional empty layers from a cross index search is to [disable global search for a layer](maps-search.md#maps-narrow-layer-by-global-search).


## Use _index in a search [maps-add-index-search]

Add [_index](elasticsearch://reference/elasticsearch/mapping-reference/mapping-index-field.md) to your search to include documents from indices that do not contain a search field.

For example, suppose you have a vector layer showing the `kibana_sample_data_logs` documents and another vector layer with `kibana_sample_data_flights` documents. (See [adding sample data](/explore-analyze/index.md) to install the `kibana_sample_data_logs` and `kibana_sample_data_flights` indices.)

If you query for

```
machine.os.keyword : "osx"
```

the `kibana_sample_data_flights` layer is empty because the index `kibana_sample_data_flights` does not contain the field `machine.os.keyword` and no documents match the query.

:::{image} /explore-analyze/images/kibana-global_search_multiple_indices_query1.png
:alt: global search multiple indices query1
:screenshot:
:::

If you instead query for

```
machine.os.keyword : "osx" or _index : "kibana_sample_data_flights"
```

the `kibana_sample_data_flights` layer includes data.

:::{image} /explore-analyze/images/kibana-global_search_multiple_indices_query2.png
:alt: global search multiple indices query2
:screenshot:
:::

