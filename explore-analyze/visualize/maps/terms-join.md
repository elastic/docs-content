---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/terms-join.html
description: Enrich map layers with terms joins to combine metrics from Elasticsearch with vector boundaries. Calculate and visualize aggregated statistics by region.
applies_to:
  stack: ga
  serverless: ga
products:
  - id: kibana
---

# Term joins [terms-join]

Term joins enrich vector layer features with metrics calculated from {{es}} aggregations, enabling data-driven styling and detailed tooltips. A term join matches vector features to aggregated metrics using a common field value, allowing you to visualize statistics like traffic counts, sales totals, or error rates on geographic boundaries.

Term joins work with Documents, Configured GeoJSON, and {{ems-init}} Boundaries vector layers, providing flexibility for combining boundary data with your metrics.

Term joins are available for the following [vector layers](vector-layer.md):

* Configured GeoJSON
* Documents
* EMS Boundaries

## Example term join [_example_term_join]

The [choropleth layer example](maps-getting-started.md#maps-add-choropleth-layer) uses a term join to shade world countries by web log traffic. Darker shades symbolize countries with more web log traffic, and lighter shades symbolize countries with less traffic.

:::{image} /explore-analyze/images/kibana-gs_add_cloropeth_layer.png
:alt: gs add cloropeth layer
:screenshot:
:::

### How a term join works [_how_a_term_join_works]

A term join uses a shared key to combine vector features, the left source, with the results of an {{es}} terms aggregation, the right source.

The cloropeth example uses the shared key, [ISO 3166-1 alpha-2 code](https://wikipedia.org/wiki/ISO_3166-1_alpha-2), to join world countries and web log traffic. ISO 3166-1 alpha-2 code is an international standard that identifies countries by a two-letter country code. For example, **Sweden** has an ISO 3166-1 alpha-2 code of **SE**.

:::{image} /explore-analyze/images/kibana-terms_join_shared_key_config.png
:alt: terms join shared key config
:screenshot:
:::


### Left source [_left_source]

The left source for the term join is the [Elastic Maps Service (EMS)](https://www.elastic.co/elastic-maps-service) World Countries. Vector features for this source are provided by EMS. You can also use your own vector features.

In the following example, **iso2** property defines the shared key for the left source.

```
{
  geometry: {
    coordinates: [...],
    type: "Polygon"
  },
  properties: {
    name: "Sweden",
    iso2: "SE"
  },
  type: "Feature"
}
```


### Right source [_right_source]

The right source uses the Kibana sample data set "Sample web logs". In this data set, the **geo.src** field contains the ISO 3166-1 alpha-2 code of the country of origin.

A [terms aggregation](elasticsearch://reference/aggregations/search-aggregations-bucket-terms-aggregation.md) groups the sample web log documents by **geo.src** and calculates metrics for each term.

The METRICS configuration defines two metric aggregations:

* The count of all documents in the terms bucket.
* The average of the field "bytes" for all documents in the terms bucket.

:::{image} /explore-analyze/images/kibana-terms_join_metric_config.png
:alt: terms join metric config
:screenshot:
:::

The right source does not provide individual documents, but instead provides the metrics from a terms aggregation. The metrics are calculated from the following sample web logs documents.

```
{
  bytes: 1837,
  geo: {
    src: "SE"
  },
  timestamp: "Feb 28, 2019 @ 07:23:08.754"
},
{
  bytes: 971,
  geo: {
    src: "SE"
  },
  timestamp: "Feb 27, 2019 @ 08:10:45.205"
},
{
  bytes: 4277,
  geo: {
    src: "SE"
  },
  timestamp: "Feb 21, 2019 @ 05:24:33.945"
},
{
  bytes: 5624,
  geo: {
    src: "SE"
  },
  timestamp: "Feb 21, 2019 @ 04:57:05.921"
}
```

The terms aggregation creates a bucket for each unique **geo.src** value. Metrics are calucated for all documents in a bucket.

The following shows an example terms aggregation response. Note the **key** property, which defines the shared key for the right source.

```
{
  aggregations: {
    join: {
      buckets: [
        {
          doc_count: 4,
          key: "SE",
          avg_of_bytes: {
            value: 3177.25
          }
        },
        ...
      ]
    }
  }
}
```



## Augment the left source with metrics from the right source [_augment_the_left_source_with_metrics_from_the_right_source]

The join adds metrics for each terms aggregation bucket to the world country feature with the corresponding ISO 3166-1 alpha-2 code. Features that do not have a corresponding terms aggregation bucket are not visible on the map.

The world country features now have two additional properties:

* Count of web log traffic originating from the world country
* Average bytes of web log traffic originating from the world country

The cloropeth example uses the count of web log traffic to symbolize countries by web log traffic.


