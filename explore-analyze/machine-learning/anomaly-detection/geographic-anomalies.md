---
mapped_pages:
  - https://www.elastic.co/guide/en/machine-learning/current/geographic-anomalies.html
---

# Detecting anomalous locations in geographic data [geographic-anomalies]

If your data includes geographic fields, you can use {{ml-features}} to detect anomalous behavior, such as a credit card transaction that occurs in an unusual location or a web request that has an unusual source location.

## Prerequisites [geographic-anomalies-prereqs]

To run this type of {{anomaly-job}}, you must have [{{ml-features}} set up](../setting-up-machine-learning.md). You must also have time series data that contains spatial data types. In particular, you must have:

* two comma-separated numbers of the form `latitude,longitude`,
* a [`geo_point`](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html) field,
* a [`geo_shape`](https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-shape.html) field that contains point values, or
* a [`geo_centroid`](https://www.elastic.co/guide/en/elasticsearch/reference/current/search-aggregations-metrics-geocentroid-aggregation.html) aggregation

The latitude and longitude must be in the range -180 to 180 and represent a point on the surface of the Earth.

This example uses the sample eCommerce orders and sample web logs data sets. For more information, see [Add the sample data](../../overview/kibana-quickstart.md#gs-get-data-into-kibana).

## Explore your geographic data [geographic-anomalies-visualize]

To get the best results from {{ml}} analytics, you must understand your data. You can use the **{{data-viz}}** in the **{{ml-app}}** app for this purpose. Search for specific fields or field types, such as geo-point fields in the sample data sets. You can see how many documents contain those fields within a specific time period and sample size. You can also see the number of distinct values, a list of example values, and preview them on a map. For example:

:::{image} ../../../images/machine-learning-weblogs-data-visualizer-geopoint.jpg
:alt: A screenshot of a geo_point field in {data-viz}
:class: screenshot
:::

## Create an {{anomaly-job}} [geographic-anomalies-jobs]

There are a few limitations to consider before you create this type of job:

1. You cannot create forecasts for {{anomaly-jobs}} that contain geographic functions.
2. You cannot add [custom rules with conditions](https://www.elastic.co/guide/en/machine-learning/current/ml-rules.html) to detectors that use geographic functions.

If those limitations are acceptable, try creating an {{anomaly-job}} that uses the [`lat_long` function](https://www.elastic.co/guide/en/machine-learning/current/ml-geo-functions.html#ml-lat-long) to analyze your own data or the sample data sets.

To create an {{anomaly-job}} that uses the `lat_long` function, in {{kib}} you must click **Create job** on the **{{ml-cap}} > {{anomaly-detect-cap}} > Jobs** page and select the advanced job wizard. Alternatively, use the [create {{anomaly-jobs}} API](https://www.elastic.co/guide/en/elasticsearch/reference/current/ml-put-job.html).

For example, create a job that analyzes the sample eCommerce orders data set to find orders with unusual coordinates (`geoip.location` values) relative to the past behavior of each customer (`user` ID):

:::{image} ../../../images/machine-learning-ecommerce-advanced-wizard-geopoint.jpg
:alt: A screenshot of creating an {{anomaly-job}} using the eCommerce data in {kib}
:class: screenshot
:::

::::{dropdown} API example

```console
PUT _ml/anomaly_detectors/ecommerce-geo <1>
{
  "analysis_config" : {
    "bucket_span":"15m",
    "detectors": [
      {
        "detector_description": "Unusual coordinates by user",
        "function": "lat_long",
        "field_name": "geoip.location",
        "by_field_name": "user"
      }
    ],
    "influencers": [
      "geoip.country_iso_code",
      "day_of_week",
      "category.keyword"
      ]
  },
  "data_description" : {
    "time_field": "order_date"
  },
  "datafeed_config":{ <2>
    "datafeed_id": "datafeed-ecommerce-geo",
    "indices": ["kibana_sample_data_ecommerce"],
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

POST _ml/anomaly_detectors/ecommerce-geo/_open <3>

POST _ml/datafeeds/datafeed-ecommerce-geo/_start <4>
{
  "end": "2022-03-22T23:00:00Z"
}
```

1. Create the {{anomaly-job}}.
2. Create the {{dfeed}}.
3. Open the job.
4. Start the {{dfeed}}. Since the sample data sets often contain timestamps that are later than the current date, it is a good idea to specify the appropriate end date for the {{dfeed}}.

::::

Alternatively, create a job that analyzes the sample web logs data set to detect events with unusual coordinates (`geo.coordinates` values) or unusually high sums of transferred data (`bytes` values):

:::{image} ../../../images/machine-learning-weblogs-advanced-wizard-geopoint.jpg
:alt: A screenshot of creating an {{anomaly-job}} using the web logs data in {kib}
:class: screenshot
:::

::::{dropdown} API example

```console
PUT _ml/anomaly_detectors/weblogs-geo <1>
{
  "analysis_config" : {
    "bucket_span":"15m",
    "detectors": [
      {
        "detector_description": "Unusual coordinates",
        "function": "lat_long",
        "field_name": "geo.coordinates"
      },
      {
        "function": "high_sum",
        "field_name": "bytes"
      }
    ],
    "influencers": [
      "geo.src",
      "extension.keyword",
      "geo.dest"
    ]
  },
  "data_description" : {
    "time_field": "timestamp",
     "time_format": "epoch_ms"
  },
  "datafeed_config":{ <2>
    "datafeed_id": "datafeed-weblogs-geo",
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

POST _ml/anomaly_detectors/weblogs-geo/_open <3>

POST _ml/datafeeds/datafeed-weblogs-geo/_start <4>
{
  "end": "2022-04-15T22:00:00Z"
}
```

1. Create the {{anomaly-job}}.
2. Create the {{dfeed}}.
3. Open the job.
4. Start the {{dfeed}}. Since the sample data sets often contain timestamps that are later than the current date, it is a good idea to specify the appropriate end date for the {{dfeed}}.

::::

## Analyze the results [geographic-anomalies-results]

After the {{anomaly-jobs}} have processed some data, you can view the results in {{kib}}.

::::{tip}
If you used APIs to create the jobs and {{dfeeds}}, you cannot see them in {{kib}} until you follow the prompts to synchronize the necessary saved objects.
::::

When you select a period that contains an anomaly in the **Anomaly Explorer** swim lane results, you can see a map of the typical and actual coordinates. For example, in the eCommerce sample data there is a user with anomalous shopping behavior:

:::{image} ../../../images/machine-learning-ecommerce-anomaly-explorer-geopoint.jpg
:alt: A screenshot of an anomalous event in the eCommerce data in Anomaly Explorer
:class: screenshot
:::

A "typical" value indicates a centroid of a cluster of previously observed locations that is closest to the "actual" location at that time. For example, there may be one centroid near the user’s home and another near the user’s work place since there are many records associated with these distinct locations.

Likewise, there are time periods in the web logs sample data where there are both unusually high sums of data transferred and unusual geographical coordinates:

:::{image} ../../../images/machine-learning-weblogs-anomaly-explorer-geopoint.jpg
:alt: A screenshot of an anomalous event in the web logs data in Anomaly Explorer
:class: screenshot
:::

You can use the top influencer values to further filter your results and identify possible contributing factors or patterns of behavior.

You can also view the anomaly in **Maps** by clicking **View in Maps** in the action menu in the anomaly table.

:::{image} ../../../images/machine-learning-view-in-maps.jpg
:alt: A screenshot of the anomaly table with the Action menu opened and the "View in Maps" option selected
:class: screenshot
:::

When you try this type of {{anomaly-job}} with your own data, it might take some experimentation to find the best combination of buckets, detectors, and influencers to detect the type of behavior you’re seeking.

For more information about {{anomaly-detect}} concepts, see [Concepts](https://www.elastic.co/guide/en/machine-learning/current/ml-concepts.html). For the full list of functions that you can use in {{anomaly-jobs}}, see [*Function reference*](ml-functions.md). For more {{anomaly-detect}} examples, see [Examples](https://www.elastic.co/guide/en/machine-learning/current/anomaly-examples.html).

## Add anomaly layers to your maps [geographic-anomalies-map-layer]

To integrate the results from your {{anomaly-job}} in **Maps**, click **Add layer**, then select **ML Anomalies**. You must then select or create an {{anomaly-job}} that uses the `lat_long` function.

For example, you can extend the map example from [Build a map to compare metrics by country or region](../../visualize/maps/maps-getting-started.md) to include a layer that uses your web logs {{anomaly-job}}:

:::{image} ../../../images/machine-learning-weblogs-anomaly-map.jpg
:alt: A screenshot of an anomaly within the Maps app
:class: screenshot
:::

## What’s next [geographic-anomalies-next]

* [Learn more about **Maps**](../../visualize/maps.md)
* [Generate alerts for your {{anomaly-jobs}}](ml-configuring-alerts.md)
