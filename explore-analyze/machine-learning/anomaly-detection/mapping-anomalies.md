---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/mapping-anomalies.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: machine-learning
---

# Mapping anomalies by location [mapping-anomalies]

If your data includes vector layers that are defined in the [{{ems}} ({{ems-init}})](../../visualize/maps/maps-connect-to-ems.md), your {{anomaly-jobs}} can generate a map of the anomalies by location.

## Prerequisites [mapping-anomalies-prereqs]

If you want to view choropleth maps in **{{data-viz}}** or {{anomaly-job}} results, you must have fields that contain valid vector layers (such as [country codes](https://maps.elastic.co/#file/world_countries) or [postal codes](https://maps.elastic.co/#file/usa_zip_codes)).

This example uses the sample web logs data set. For more information, see [Add the sample data](../../index.md#gs-get-data-into-kibana).

## Explore your data [visualize-vector-layers]

If you have fields that contain valid vector layers, you can use the **{{data-viz}}** in the **{{ml-app}}** app to see a choropleth map, in which each area is colored based on its document count. For example:

:::{image} /explore-analyze/images/machine-learning-weblogs-data-visualizer-choropleth.png
:alt: A screenshot of a field that contains vector layer values in {{data-viz}}
:screenshot:
:::

## Create an {{anomaly-job}} [mapping-anomalies-jobs]

To create an {{anomaly-job}}, navigate to the **Anomaly Detection Jobs** page in the main menu, or use the [global search field](../../find-and-organize/find-apps-and-objects.md). Then click **Create job** and select the appropriate job wizard. Alternatively, use the [create {{anomaly-jobs}} API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-put-job).

For example, use the multi-metric job wizard to create a job that analyzes the sample web logs data set to detect anomalous behavior in the sum of the data transferred (`bytes` values) for each destination country (`geo.dest` values):

:::{image} /explore-analyze/images/machine-learning-weblogs-multimetric-wizard-vector.png
:alt: A screenshot of creating an {{anomaly-job}} using the web logs data in {{kib}}
:screenshot:
:::

::::{dropdown} API example

```console
PUT _ml/anomaly_detectors/weblogs-vectors <1>
{
  "analysis_config" : {
    "bucket_span":"15m",
    "detectors": [
      {
        "detector_description": "Sum of bytes",
        "function": "sum",
        "field_name": "bytes",
        "partition_field_name": "geo.dest"
      }
    ],
    "influencers": [
    "geo.src",
    "agent.keyword",
    "geo.dest"
    ]
  },
  "data_description" : {
    "time_field": "timestamp"
  },
  "datafeed_config": { <2>
    "datafeed_id": "datafeed-weblogs-vectors",
    "indices": ["kibana_sample_data_logs"],
    "query": {
      "bool": {
        "must": [
          {
            "match_all": {}
          }
        ]
      }
    }
  }
}

POST _ml/anomaly_detectors/weblogs-vectors/_open <3>

POST _ml/datafeeds/datafeed-weblogs-vectors/_start <4>
{
  "end": "2021-07-15T22:00:00Z"
}
```

1. Create the {{anomaly-job}}.
2. Create the {{dfeed}}.
3. Open the job.
4. Start the {{dfeed}}. Since the sample data sets often contain timestamps that are later than the current date, it is a good idea to specify the appropriate end date for the {{dfeed}}.

::::

## Analyze the results [mapping-anomalies-results]

After the {{anomaly-jobs}} have processed some data, you can view the results in {{kib}}.

::::{tip}
If you used APIs to create the jobs and {{dfeeds}}, you cannot see them in {{kib}} until you follow the prompts to synchronize the necessary saved objects.
::::

:::{image} /explore-analyze/images/machine-learning-weblogs-anomaly-explorer-vectors.png
:alt: A screenshot of the anomaly count by location in Anomaly Explorer
:screenshot:
:::

The **Anomaly Explorer** contains a map, which is affected by your swim lane selections. It colors each location to reflect the number of anomalies in that selected time period. Locations that have few anomalies are indicated in blue; locations with many anomalies are red. Thus you can quickly see the locations that are generating the most anomalies. If your vector layers define regions, counties, or postal codes, you can zoom in for fine details.

## What’s next [mapping-anomalies-next]

* [Learn more about **Maps**](../../visualize/maps.md)
* [Generate alerts for your {{anomaly-jobs}}](ml-configuring-alerts.md)
