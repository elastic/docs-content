---
navigation_title: Basics
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/aggregations-tutorial.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Tutorial: Analyze eCommerce data with aggregations using Query DSL [aggregations-tutorial]

This hands-on tutorial shows you how to analyze eCommerce data using {{es}} [aggregations](../aggregations.md) with the `_search` API and Query DSL.

You’ll learn how to:

* Calculate key business metrics such as average order value
* Analyze sales patterns over time
* Compare performance across product categories
* Track moving averages and cumulative totals

## Requirements [aggregations-tutorial-requirements]

You’ll need:

1. A running instance of [{{es}}](../../../get-started/deployment-options.md), either on {{serverless-full}} or together with {{kib}} on Elastic Cloud Hosted/Self Managed deployments.

    * If you don’t have a deployment, you can run the following command in your terminal to set up a [local dev environment](../../../solutions/search/get-started.md):

        ```sh
        curl -fsSL https://elastic.co/start-local | sh
        ```

2. The [sample eCommerce data](../../index.md#gs-get-data-into-kibana) loaded into {{es}}. To load sample data follow these steps in your UI:

    * Open the **Integrations** pages by searching in the global search field.
    * Search for `sample data` in the **Integrations** search field.
    * Open the **Sample data** page.
    * Select the **Other sample data sets** collapsible.
    * Add the **Sample eCommerce orders** data set. This will create and populate an index called `kibana_sample_data_ecommerce`.

## Inspect index structure [aggregations-tutorial-inspect-data]

Before we start analyzing the data, let’s examine the structure of the documents in our sample eCommerce index. Run this command to see the field [mappings](../../../manage-data/data-store/index-basics.md#elasticsearch-intro-documents-fields-mappings):

```console
GET kibana_sample_data_ecommerce/_mapping
```

The response shows the field mappings for the `kibana_sample_data_ecommerce` index.

::::{dropdown} Example response

```console-response
{
  "kibana_sample_data_ecommerce": {
    "mappings": {
      "properties": {
        "category": {
          "type": "text",
          "fields": { <1>
            "keyword": {
              "type": "keyword"
            }
          }
        },
        "currency": {
          "type": "keyword"
        },
        "customer_birth_date": {
          "type": "date"
        },
        "customer_first_name": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "customer_full_name": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "customer_gender": {
          "type": "keyword"
        },
        "customer_id": {
          "type": "keyword"
        },
        "customer_last_name": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "customer_phone": {
          "type": "keyword"
        },
        "day_of_week": {
          "type": "keyword"
        },
        "day_of_week_i": {
          "type": "integer"
        },
        "email": {
          "type": "keyword"
        },
        "event": {
          "properties": {
            "dataset": {
              "type": "keyword"
            }
          }
        },
        "geoip": {
          "properties": { <2>
            "city_name": {
              "type": "keyword"
            },
            "continent_name": {
              "type": "keyword"
            },
            "country_iso_code": {
              "type": "keyword"
            },
            "location": {
              "type": "geo_point" <3>
            },
            "region_name": {
              "type": "keyword"
            }
          }
        },
        "manufacturer": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword"
            }
          }
        },
        "order_date": {
          "type": "date"
        },
        "order_id": {
          "type": "keyword"
        },
        "products": {
          "properties": { <4>
            "_id": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword",
                  "ignore_above": 256
                }
              }
            },
            "base_price": {
              "type": "half_float"
            },
            "base_unit_price": {
              "type": "half_float"
            },
            "category": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword"
                }
              }
            },
            "created_on": {
              "type": "date"
            },
            "discount_amount": {
              "type": "half_float"
            },
            "discount_percentage": {
              "type": "half_float"
            },
            "manufacturer": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword"
                }
              }
            },
            "min_price": {
              "type": "half_float"
            },
            "price": {
              "type": "half_float"
            },
            "product_id": {
              "type": "long"
            },
            "product_name": {
              "type": "text",
              "fields": {
                "keyword": {
                  "type": "keyword"
                }
              },
              "analyzer": "english"
            },
            "quantity": {
              "type": "integer"
            },
            "sku": {
              "type": "keyword"
            },
            "tax_amount": {
              "type": "half_float"
            },
            "taxful_price": {
              "type": "half_float"
            },
            "taxless_price": {
              "type": "half_float"
            },
            "unit_discount_amount": {
              "type": "half_float"
            }
          }
        },
        "sku": {
          "type": "keyword"
        },
        "taxful_total_price": {
          "type": "half_float"
        },
        "taxless_total_price": {
          "type": "half_float"
        },
        "total_quantity": {
          "type": "integer"
        },
        "total_unique_products": {
          "type": "integer"
        },
        "type": {
          "type": "keyword"
        },
        "user": {
          "type": "keyword"
        }
      }
    }
  }
}
```

1. `fields`: Multi-field mapping that allows both full text and exact matching
2. `geoip.properties`: Object type field containing location-related properties
3. `geoip.location`: Geographic coordinates stored as geo_point for location-based queries
4. `products.properties`: Nested structure containing details about items in each order

::::

The sample data includes the following [field data types](elasticsearch://reference/elasticsearch/mapping-reference/field-data-types.md):

* [`text`](elasticsearch://reference/elasticsearch/mapping-reference/text.md) and [`keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md) for text fields
  * Most `text` fields have a `.keyword` subfield for exact matching using [multi-fields](elasticsearch://reference/elasticsearch/mapping-reference/multi-fields.md)

* [`date`](elasticsearch://reference/elasticsearch/mapping-reference/date.md) for date fields
* 3 [numeric](elasticsearch://reference/elasticsearch/mapping-reference/number.md) types:
  * `integer` for whole numbers
  * `long` for large whole numbers
  * `half_float` for floating-point numbers

* [`geo_point`](elasticsearch://reference/elasticsearch/mapping-reference/geo-point.md) for geographic coordinates
* [`object`](elasticsearch://reference/elasticsearch/mapping-reference/object.md) for nested structures such as `products`, `geoip`, `event`

Now that we understand the structure of our sample data, let’s start analyzing it.

## Get key business metrics [aggregations-tutorial-basic-metrics]

Let’s start by calculating important metrics about orders and customers.

### Get average order size [aggregations-tutorial-order-value]

Calculate the average order value across all orders in the dataset using the [`avg`](elasticsearch://reference/aggregations/search-aggregations-metrics-avg-aggregation.md) aggregation.

```console
GET kibana_sample_data_ecommerce/_search
{
 "size": 0, <1>
 "aggs": {
   "avg_order_value": { <2>
     "avg": { <3>
       "field": "taxful_total_price"
     }
   }
 }
}
```

1. Set `size` to 0 to avoid returning matched documents in the response and return only the aggregation results
2. A meaningful name that describes what this metric represents
3. Configures an `avg` aggregation, which calculates a simple arithmetic mean

::::{dropdown} Example response

```console-result
{
  "took": 0,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675, <1>
      "relation": "eq"
    },
    "max_score": null,
    "hits": [] <2>
  },
  "aggregations": {
    "avg_order_value": { <3>
      "value": 75.05542864304813 <4>
    }
  }
}
```

1. Total number of orders in the dataset
2. `hits` is empty because we set `size` to 0
3. Results appear under the name we specified in the request
4. The average order value is calculated dynamically from all the orders in the dataset

::::

### Get multiple order statistics at once [aggregations-tutorial-order-stats]

Calculate multiple statistics about orders in one request using the [`stats`](elasticsearch://reference/aggregations/search-aggregations-metrics-stats-aggregation.md) aggregation.

```console
GET kibana_sample_data_ecommerce/_search
{
 "size": 0,
 "aggs": {
   "order_stats": { <1>
     "stats": { <2>
       "field": "taxful_total_price"
     }
   }
 }
}
```

1. A descriptive name for this set of statistics
2. `stats` returns count, min, max, avg, and sum at once

::::{dropdown} Example response

```console-result
{
 "aggregations": {
   "order_stats": {
     "count": 4675, <1>
     "min": 6.98828125, <2>
     "max": 2250, <3>
     "avg": 75.05542864304813, <4>
     "sum": 350884.12890625 <5>
   }
 }
}
```

1. `"count"`: Total number of orders in the dataset
2. `"min"`: Lowest individual order value in the dataset
3. `"max"`: Highest individual order value in the dataset
4. `"avg"`: Average value per order across all orders
5. `"sum"`: Total revenue from all orders combined

::::

::::{tip}
The [stats aggregation](elasticsearch://reference/aggregations/search-aggregations-metrics-stats-aggregation.md) is more efficient than running individual min, max, avg, and sum aggregations.

::::

## Analyze sales patterns [aggregations-tutorial-sales-patterns]

Let’s group orders in different ways to understand sales patterns.

### Break down sales by category [aggregations-tutorial-category-breakdown]

Group orders by category to see which product categories are most popular, using the [`terms`](elasticsearch://reference/aggregations/search-aggregations-bucket-terms-aggregation.md) aggregation.

```console
GET kibana_sample_data_ecommerce/_search
{
 "size": 0,
 "aggs": {
   "sales_by_category": { <1>
     "terms": { <2>
       "field": "category.keyword", <3>
       "size": 5, <4>
       "order": { "_count": "desc" } <5>
     }
   }
 }
}
```

1. Name reflecting the business purpose of this breakdown
2. `terms` aggregation groups documents by field values
3. Use [`.keyword`](elasticsearch://reference/elasticsearch/mapping-reference/keyword.md) field for exact matching on text fields
4. Limit to top 5 categories
5. Order by number of orders (descending)

::::{dropdown} Example response

```console-result
{
  "took": 4,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "sales_by_category": {
      "doc_count_error_upper_bound": 0, <1>
      "sum_other_doc_count": 572, <2>
      "buckets": [ <3>
        {
          "key": "Men's Clothing", <4>
          "doc_count": 2024 <5>
        },
        {
          "key": "Women's Clothing",
          "doc_count": 1903
        },
        {
          "key": "Women's Shoes",
          "doc_count": 1136
        },
        {
          "key": "Men's Shoes",
          "doc_count": 944
        },
        {
          "key": "Women's Accessories",
          "doc_count": 830
        }
      ]
    }
  }
}
```

1. Due to Elasticsearch’s distributed architecture, when [terms aggregations](elasticsearch://reference/aggregations/search-aggregations-bucket-terms-aggregation.md) run across multiple shards, the doc counts may have a small margin of error. This value indicates the maximum possible error in the counts.
2. Count of documents in categories beyond the requested size.
3. Array of category buckets, ordered by count.
4. Category name.
5. Number of orders in this category.

::::

### Track daily sales patterns [aggregations-tutorial-daily-sales]

Group orders by day to track daily sales patterns using the [`date_histogram`](elasticsearch://reference/aggregations/search-aggregations-bucket-datehistogram-aggregation.md) aggregation.

```console
GET kibana_sample_data_ecommerce/_search
{
 "size": 0,
 "aggs": {
   "daily_orders": { <1>
     "date_histogram": { <2>
       "field": "order_date",
       "calendar_interval": "day", <3>
       "format": "yyyy-MM-dd", <4>
       "min_doc_count": 0 <5>
     }
   }
 }
}
```

1. Descriptive name for the time-series aggregation results.
2. The `date_histogram` aggregation groups documents into time-based buckets, similar to terms aggregation but for dates.
3. Uses [calendar and fixed time intervals](elasticsearch://reference/aggregations/search-aggregations-bucket-datehistogram-aggregation.md#calendar_and_fixed_intervals) to handle months with different lengths. `"day"` ensures consistent daily grouping regardless of timezone.
4. Formats dates in response using [date patterns](elasticsearch://reference/elasticsearch/mapping-reference/mapping-date-format.md) (e.g. "yyyy-MM-dd"). Refer to [date math expressions](elasticsearch://reference/elasticsearch/rest-apis/common-options.md#date-math) for additional options.
5. When `min_doc_count` is 0, returns buckets for days with no orders, useful for continuous time series visualization.

::::{dropdown} Example response

```console-result
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "daily_orders": { <1>
      "buckets": [ <2>
        {
          "key_as_string": "2024-11-28", <3>
          "key": 1732752000000, <4>
          "doc_count": 146 <5>
        },
        {
          "key_as_string": "2024-11-29",
          "key": 1732838400000,
          "doc_count": 153
        },
        {
          "key_as_string": "2024-11-30",
          "key": 1732924800000,
          "doc_count": 143
        },
        {
          "key_as_string": "2024-12-01",
          "key": 1733011200000,
          "doc_count": 140
        },
        {
          "key_as_string": "2024-12-02",
          "key": 1733097600000,
          "doc_count": 139
        },
        {
          "key_as_string": "2024-12-03",
          "key": 1733184000000,
          "doc_count": 157
        },
        {
          "key_as_string": "2024-12-04",
          "key": 1733270400000,
          "doc_count": 145
        },
        {
          "key_as_string": "2024-12-05",
          "key": 1733356800000,
          "doc_count": 152
        },
        {
          "key_as_string": "2024-12-06",
          "key": 1733443200000,
          "doc_count": 163
        },
        {
          "key_as_string": "2024-12-07",
          "key": 1733529600000,
          "doc_count": 141
        },
        {
          "key_as_string": "2024-12-08",
          "key": 1733616000000,
          "doc_count": 151
        },
        {
          "key_as_string": "2024-12-09",
          "key": 1733702400000,
          "doc_count": 143
        },
        {
          "key_as_string": "2024-12-10",
          "key": 1733788800000,
          "doc_count": 143
        },
        {
          "key_as_string": "2024-12-11",
          "key": 1733875200000,
          "doc_count": 142
        },
        {
          "key_as_string": "2024-12-12",
          "key": 1733961600000,
          "doc_count": 161
        },
        {
          "key_as_string": "2024-12-13",
          "key": 1734048000000,
          "doc_count": 144
        },
        {
          "key_as_string": "2024-12-14",
          "key": 1734134400000,
          "doc_count": 157
        },
        {
          "key_as_string": "2024-12-15",
          "key": 1734220800000,
          "doc_count": 158
        },
        {
          "key_as_string": "2024-12-16",
          "key": 1734307200000,
          "doc_count": 144
        },
        {
          "key_as_string": "2024-12-17",
          "key": 1734393600000,
          "doc_count": 151
        },
        {
          "key_as_string": "2024-12-18",
          "key": 1734480000000,
          "doc_count": 145
        },
        {
          "key_as_string": "2024-12-19",
          "key": 1734566400000,
          "doc_count": 157
        },
        {
          "key_as_string": "2024-12-20",
          "key": 1734652800000,
          "doc_count": 158
        },
        {
          "key_as_string": "2024-12-21",
          "key": 1734739200000,
          "doc_count": 153
        },
        {
          "key_as_string": "2024-12-22",
          "key": 1734825600000,
          "doc_count": 165
        },
        {
          "key_as_string": "2024-12-23",
          "key": 1734912000000,
          "doc_count": 153
        },
        {
          "key_as_string": "2024-12-24",
          "key": 1734998400000,
          "doc_count": 158
        },
        {
          "key_as_string": "2024-12-25",
          "key": 1735084800000,
          "doc_count": 160
        },
        {
          "key_as_string": "2024-12-26",
          "key": 1735171200000,
          "doc_count": 159
        },
        {
          "key_as_string": "2024-12-27",
          "key": 1735257600000,
          "doc_count": 152
        },
        {
          "key_as_string": "2024-12-28",
          "key": 1735344000000,
          "doc_count": 142
        }
      ]
    }
  }
}
```

1. Results of our named aggregation "daily_orders"
2. Time-based buckets from date_histogram aggregation
3. `key_as_string` is the human-readable date for this bucket
4. `key` is the same date represented as the Unix timestamp for this bucket
5. `doc_count` counts the number of documents that fall into this time bucket

::::

## Combine metrics with groupings [aggregations-tutorial-combined-analysis]

Now let’s calculate [metrics](elasticsearch://reference/aggregations/metrics.md) within each group to get deeper insights.

### Compare category performance [aggregations-tutorial-category-metrics]

Calculate metrics within each category to compare performance across categories.

```console
GET kibana_sample_data_ecommerce/_search
{
 "size": 0,
 "aggs": {
   "categories": {
     "terms": {
       "field": "category.keyword",
       "size": 5,
       "order": { "total_revenue": "desc" } <1>
     },
     "aggs": { <2>
       "total_revenue": { <3>
         "sum": {
           "field": "taxful_total_price"
         }
       },
       "avg_order_value": { <4>
         "avg": {
           "field": "taxful_total_price"
         }
       },
       "total_items": { <5>
         "sum": {
           "field": "total_quantity"
         }
       }
     }
   }
 }
}
```

1. Order categories by their total revenue instead of count
2. Define metrics to calculate within each category
3. Total revenue for the category
4. Average order value in the category
5. Total number of items sold

::::{dropdown} Example response

```console-result
{
 "aggregations": {
   "categories": {
     "buckets": [
       {
         "key": "Men's Clothing", <1>
         "doc_count": 2179, <2>
         "total_revenue": { <3>
           "value": 156729.453125
         },
         "avg_order_value": { <4>
           "value": 71.92726898715927
         },
         "total_items": { <5>
           "value": 8716
         }
       },
       {
         "key": "Women's Clothing",
         "doc_count": 2262,
         ...
       }
     ]
   }
 }
}
```

1. Category name
2. Number of orders
3. Total revenue for this category
4. Average order value for this category
5. Total quantity of items sold

::::

### Analyze daily sales performance [aggregations-tutorial-daily-metrics]

Let’s combine metrics to track daily trends: daily revenue, unique customers, and average basket size.

```console
GET kibana_sample_data_ecommerce/_search
{
 "size": 0,
 "aggs": {
   "daily_sales": {
     "date_histogram": {
       "field": "order_date",
       "calendar_interval": "day",
       "format": "yyyy-MM-dd"
     },
     "aggs": {
       "revenue": { <1>
         "sum": {
           "field": "taxful_total_price"
         }
       },
       "unique_customers": { <2>
         "cardinality": {
           "field": "customer_id"
         }
       },
       "avg_basket_size": { <3>
         "avg": {
           "field": "total_quantity"
         }
       }
     }
   }
 }
}
```

1. Daily revenue
2. Uses the [`cardinality`](elasticsearch://reference/aggregations/search-aggregations-metrics-cardinality-aggregation.md) aggregation to count unique customers per day
3. Average number of items per order

::::{dropdown} Example response

```console-result
{
  "took": 119,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "daily_sales": {
      "buckets": [
        {
          "key_as_string": "2024-11-14",
          "key": 1731542400000,
          "doc_count": 146,
          "unique_customers": {
            "value": 42
          },
          "revenue": {
            "value": 10578.53125
          },
          "avg_basket_size": {
            "value": 2.1780821917808217
          }
        },
        {
          "key_as_string": "2024-11-15",
          "key": 1731628800000,
          "doc_count": 153,
          "unique_customers": {
            "value": 44
          },
          "revenue": {
            "value": 10448
          },
          "avg_basket_size": {
            "value": 2.183006535947712
          }
        },
        {
          "key_as_string": "2024-11-16",
          "key": 1731715200000,
          "doc_count": 143,
          "unique_customers": {
            "value": 45
          },
          "revenue": {
            "value": 10283.484375
          },
          "avg_basket_size": {
            "value": 2.111888111888112
          }
        },
        {
          "key_as_string": "2024-11-17",
          "key": 1731801600000,
          "doc_count": 140,
          "unique_customers": {
            "value": 42
          },
          "revenue": {
            "value": 10145.5234375
          },
          "avg_basket_size": {
            "value": 2.142857142857143
          }
        },
        {
          "key_as_string": "2024-11-18",
          "key": 1731888000000,
          "doc_count": 139,
          "unique_customers": {
            "value": 42
          },
          "revenue": {
            "value": 12012.609375
          },
          "avg_basket_size": {
            "value": 2.158273381294964
          }
        },
        {
          "key_as_string": "2024-11-19",
          "key": 1731974400000,
          "doc_count": 157,
          "unique_customers": {
            "value": 43
          },
          "revenue": {
            "value": 11009.45703125
          },
          "avg_basket_size": {
            "value": 2.0955414012738856
          }
        },
        {
          "key_as_string": "2024-11-20",
          "key": 1732060800000,
          "doc_count": 145,
          "unique_customers": {
            "value": 44
          },
          "revenue": {
            "value": 10720.59375
          },
          "avg_basket_size": {
            "value": 2.179310344827586
          }
        },
        {
          "key_as_string": "2024-11-21",
          "key": 1732147200000,
          "doc_count": 152,
          "unique_customers": {
            "value": 43
          },
          "revenue": {
            "value": 11185.3671875
          },
          "avg_basket_size": {
            "value": 2.1710526315789473
          }
        },
        {
          "key_as_string": "2024-11-22",
          "key": 1732233600000,
          "doc_count": 163,
          "unique_customers": {
            "value": 44
          },
          "revenue": {
            "value": 13560.140625
          },
          "avg_basket_size": {
            "value": 2.2576687116564416
          }
        },
        {
          "key_as_string": "2024-11-23",
          "key": 1732320000000,
          "doc_count": 141,
          "unique_customers": {
            "value": 45
          },
          "revenue": {
            "value": 9884.78125
          },
          "avg_basket_size": {
            "value": 2.099290780141844
          }
        },
        {
          "key_as_string": "2024-11-24",
          "key": 1732406400000,
          "doc_count": 151,
          "unique_customers": {
            "value": 44
          },
          "revenue": {
            "value": 11075.65625
          },
          "avg_basket_size": {
            "value": 2.0927152317880795
          }
        },
        {
          "key_as_string": "2024-11-25",
          "key": 1732492800000,
          "doc_count": 143,
          "unique_customers": {
            "value": 41
          },
          "revenue": {
            "value": 10323.8515625
          },
          "avg_basket_size": {
            "value": 2.167832167832168
          }
        },
        {
          "key_as_string": "2024-11-26",
          "key": 1732579200000,
          "doc_count": 143,
          "unique_customers": {
            "value": 44
          },
          "revenue": {
            "value": 10369.546875
          },
          "avg_basket_size": {
            "value": 2.167832167832168
          }
        },
        {
          "key_as_string": "2024-11-27",
          "key": 1732665600000,
          "doc_count": 142,
          "unique_customers": {
            "value": 46
          },
          "revenue": {
            "value": 11711.890625
          },
          "avg_basket_size": {
            "value": 2.1971830985915495
          }
        },
        {
          "key_as_string": "2024-11-28",
          "key": 1732752000000,
          "doc_count": 161,
          "unique_customers": {
            "value": 43
          },
          "revenue": {
            "value": 12612.6640625
          },
          "avg_basket_size": {
            "value": 2.1180124223602483
          }
        },
        {
          "key_as_string": "2024-11-29",
          "key": 1732838400000,
          "doc_count": 144,
          "unique_customers": {
            "value": 42
          },
          "revenue": {
            "value": 10176.87890625
          },
          "avg_basket_size": {
            "value": 2.0347222222222223
          }
        },
        {
          "key_as_string": "2024-11-30",
          "key": 1732924800000,
          "doc_count": 157,
          "unique_customers": {
            "value": 43
          },
          "revenue": {
            "value": 11480.33203125
          },
          "avg_basket_size": {
            "value": 2.159235668789809
          }
        },
        {
          "key_as_string": "2024-12-01",
          "key": 1733011200000,
          "doc_count": 158,
          "unique_customers": {
            "value": 42
          },
          "revenue": {
            "value": 11533.265625
          },
          "avg_basket_size": {
            "value": 2.0822784810126582
          }
        },
        {
          "key_as_string": "2024-12-02",
          "key": 1733097600000,
          "doc_count": 144,
          "unique_customers": {
            "value": 43
          },
          "revenue": {
            "value": 10499.8125
          },
          "avg_basket_size": {
            "value": 2.201388888888889
          }
        },
        {
          "key_as_string": "2024-12-03",
          "key": 1733184000000,
          "doc_count": 151,
          "unique_customers": {
            "value": 40
          },
          "revenue": {
            "value": 12111.6875
          },
          "avg_basket_size": {
            "value": 2.172185430463576
          }
        },
        {
          "key_as_string": "2024-12-04",
          "key": 1733270400000,
          "doc_count": 145,
          "unique_customers": {
            "value": 40
          },
          "revenue": {
            "value": 10530.765625
          },
          "avg_basket_size": {
            "value": 2.0965517241379312
          }
        },
        {
          "key_as_string": "2024-12-05",
          "key": 1733356800000,
          "doc_count": 157,
          "unique_customers": {
            "value": 43
          },
          "revenue": {
            "value": 11872.5625
          },
          "avg_basket_size": {
            "value": 2.1464968152866244
          }
        },
        {
          "key_as_string": "2024-12-06",
          "key": 1733443200000,
          "doc_count": 158,
          "unique_customers": {
            "value": 42
          },
          "revenue": {
            "value": 12109.453125
          },
          "avg_basket_size": {
            "value": 2.151898734177215
          }
        },
        {
          "key_as_string": "2024-12-07",
          "key": 1733529600000,
          "doc_count": 153,
          "unique_customers": {
            "value": 42
          },
          "revenue": {
            "value": 11057.40625
          },
          "avg_basket_size": {
            "value": 2.111111111111111
          }
        },
        {
          "key_as_string": "2024-12-08",
          "key": 1733616000000,
          "doc_count": 165,
          "unique_customers": {
            "value": 42
          },
          "revenue": {
            "value": 13095.609375
          },
          "avg_basket_size": {
            "value": 2.1818181818181817
          }
        },
        {
          "key_as_string": "2024-12-09",
          "key": 1733702400000,
          "doc_count": 153,
          "unique_customers": {
            "value": 41
          },
          "revenue": {
            "value": 12574.015625
          },
          "avg_basket_size": {
            "value": 2.2287581699346406
          }
        },
        {
          "key_as_string": "2024-12-10",
          "key": 1733788800000,
          "doc_count": 158,
          "unique_customers": {
            "value": 42
          },
          "revenue": {
            "value": 11188.1875
          },
          "avg_basket_size": {
            "value": 2.151898734177215
          }
        },
        {
          "key_as_string": "2024-12-11",
          "key": 1733875200000,
          "doc_count": 160,
          "unique_customers": {
            "value": 42
          },
          "revenue": {
            "value": 12117.65625
          },
          "avg_basket_size": {
            "value": 2.20625
          }
        },
        {
          "key_as_string": "2024-12-12",
          "key": 1733961600000,
          "doc_count": 159,
          "unique_customers": {
            "value": 45
          },
          "revenue": {
            "value": 11558.25
          },
          "avg_basket_size": {
            "value": 2.1823899371069184
          }
        },
        {
          "key_as_string": "2024-12-13",
          "key": 1734048000000,
          "doc_count": 152,
          "unique_customers": {
            "value": 45
          },
          "revenue": {
            "value": 11921.1171875
          },
          "avg_basket_size": {
            "value": 2.289473684210526
          }
        },
        {
          "key_as_string": "2024-12-14",
          "key": 1734134400000,
          "doc_count": 142,
          "unique_customers": {
            "value": 45
          },
          "revenue": {
            "value": 11135.03125
          },
          "avg_basket_size": {
            "value": 2.183098591549296
          }
        }
      ]
    }
  }
}
```

::::

## Track trends and patterns [aggregations-tutorial-trends]

You can use [pipeline aggregations](elasticsearch://reference/aggregations/pipeline.md) on the results of other aggregations. Let’s analyze how metrics change over time.

### Smooth out daily fluctuations [aggregations-tutorial-moving-average]

Moving averages help identify trends by reducing day-to-day noise in the data. Let’s observe sales trends more clearly by smoothing daily revenue variations, using the [Moving Function](elasticsearch://reference/aggregations/search-aggregations-pipeline-movfn-aggregation.md) aggregation.

```console
GET kibana_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "daily_sales": {
      "date_histogram": {
        "field": "order_date",
        "calendar_interval": "day"
      },
      "aggs": {
        "daily_revenue": {  <1>
          "sum": {
            "field": "taxful_total_price"
          }
        },
        "smoothed_revenue": { <2>
          "moving_fn": { <3>
            "buckets_path": "daily_revenue", <4>
            "window": 3, <5>
            "script": "MovingFunctions.unweightedAvg(values)" <6>
          }
        }
      }
    }
  }
}
```

1. Calculate daily revenue first.
2. Create a smoothed version of the daily revenue.
3. Use `moving_fn` for moving window calculations.
4. Reference the revenue from our date histogram.
5. Use a 3-day window — use different window sizes to see trends at different time scales.
6. Use the built-in unweighted average function in the `moving_fn` aggregation.

::::{dropdown} Example response

```console-result
{
  "took": 13,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "daily_sales": {
      "buckets": [
        {
          "key_as_string": "2024-11-14T00:00:00.000Z",  <1>
          "key": 1731542400000,
          "doc_count": 146, <2>
          "daily_revenue": { <3>
            "value": 10578.53125
          },
          "smoothed_revenue": { <4>
            "value": null
          }
        },
        {
          "key_as_string": "2024-11-15T00:00:00.000Z",
          "key": 1731628800000,
          "doc_count": 153,
          "daily_revenue": {
            "value": 10448
          },
          "smoothed_revenue": { <5>
            "value": 10578.53125
          }
        },
        {
          "key_as_string": "2024-11-16T00:00:00.000Z",
          "key": 1731715200000,
          "doc_count": 143,
          "daily_revenue": {
            "value": 10283.484375
          },
          "smoothed_revenue": {
            "value": 10513.265625
          }
        },
        {
          "key_as_string": "2024-11-17T00:00:00.000Z",
          "key": 1731801600000,
          "doc_count": 140,
          "daily_revenue": {
            "value": 10145.5234375
          },
          "smoothed_revenue": {
            "value": 10436.671875
          }
        },
        {
          "key_as_string": "2024-11-18T00:00:00.000Z",
          "key": 1731888000000,
          "doc_count": 139,
          "daily_revenue": {
            "value": 12012.609375
          },
          "smoothed_revenue": {
            "value": 10292.3359375
          }
        },
        {
          "key_as_string": "2024-11-19T00:00:00.000Z",
          "key": 1731974400000,
          "doc_count": 157,
          "daily_revenue": {
            "value": 11009.45703125
          },
          "smoothed_revenue": {
            "value": 10813.872395833334
          }
        },
        {
          "key_as_string": "2024-11-20T00:00:00.000Z",
          "key": 1732060800000,
          "doc_count": 145,
          "daily_revenue": {
            "value": 10720.59375
          },
          "smoothed_revenue": {
            "value": 11055.86328125
          }
        },
        {
          "key_as_string": "2024-11-21T00:00:00.000Z",
          "key": 1732147200000,
          "doc_count": 152,
          "daily_revenue": {
            "value": 11185.3671875
          },
          "smoothed_revenue": {
            "value": 11247.553385416666
          }
        },
        {
          "key_as_string": "2024-11-22T00:00:00.000Z",
          "key": 1732233600000,
          "doc_count": 163,
          "daily_revenue": {
            "value": 13560.140625
          },
          "smoothed_revenue": {
            "value": 10971.805989583334
          }
        },
        {
          "key_as_string": "2024-11-23T00:00:00.000Z",
          "key": 1732320000000,
          "doc_count": 141,
          "daily_revenue": {
            "value": 9884.78125
          },
          "smoothed_revenue": {
            "value": 11822.033854166666
          }
        },
        {
          "key_as_string": "2024-11-24T00:00:00.000Z",
          "key": 1732406400000,
          "doc_count": 151,
          "daily_revenue": {
            "value": 11075.65625
          },
          "smoothed_revenue": {
            "value": 11543.4296875
          }
        },
        {
          "key_as_string": "2024-11-25T00:00:00.000Z",
          "key": 1732492800000,
          "doc_count": 143,
          "daily_revenue": {
            "value": 10323.8515625
          },
          "smoothed_revenue": {
            "value": 11506.859375
          }
        },
        {
          "key_as_string": "2024-11-26T00:00:00.000Z",
          "key": 1732579200000,
          "doc_count": 143,
          "daily_revenue": {
            "value": 10369.546875
          },
          "smoothed_revenue": {
            "value": 10428.096354166666
          }
        },
        {
          "key_as_string": "2024-11-27T00:00:00.000Z",
          "key": 1732665600000,
          "doc_count": 142,
          "daily_revenue": {
            "value": 11711.890625
          },
          "smoothed_revenue": {
            "value": 10589.684895833334
          }
        },
        {
          "key_as_string": "2024-11-28T00:00:00.000Z",
          "key": 1732752000000,
          "doc_count": 161,
          "daily_revenue": {
            "value": 12612.6640625
          },
          "smoothed_revenue": {
            "value": 10801.763020833334
          }
        },
        {
          "key_as_string": "2024-11-29T00:00:00.000Z",
          "key": 1732838400000,
          "doc_count": 144,
          "daily_revenue": {
            "value": 10176.87890625
          },
          "smoothed_revenue": {
            "value": 11564.700520833334
          }
        },
        {
          "key_as_string": "2024-11-30T00:00:00.000Z",
          "key": 1732924800000,
          "doc_count": 157,
          "daily_revenue": {
            "value": 11480.33203125
          },
          "smoothed_revenue": {
            "value": 11500.477864583334
          }
        },
        {
          "key_as_string": "2024-12-01T00:00:00.000Z",
          "key": 1733011200000,
          "doc_count": 158,
          "daily_revenue": {
            "value": 11533.265625
          },
          "smoothed_revenue": {
            "value": 11423.291666666666
          }
        },
        {
          "key_as_string": "2024-12-02T00:00:00.000Z",
          "key": 1733097600000,
          "doc_count": 144,
          "daily_revenue": {
            "value": 10499.8125
          },
          "smoothed_revenue": {
            "value": 11063.4921875
          }
        },
        {
          "key_as_string": "2024-12-03T00:00:00.000Z",
          "key": 1733184000000,
          "doc_count": 151,
          "daily_revenue": {
            "value": 12111.6875
          },
          "smoothed_revenue": {
            "value": 11171.13671875
          }
        },
        {
          "key_as_string": "2024-12-04T00:00:00.000Z",
          "key": 1733270400000,
          "doc_count": 145,
          "daily_revenue": {
            "value": 10530.765625
          },
          "smoothed_revenue": {
            "value": 11381.588541666666
          }
        },
        {
          "key_as_string": "2024-12-05T00:00:00.000Z",
          "key": 1733356800000,
          "doc_count": 157,
          "daily_revenue": {
            "value": 11872.5625
          },
          "smoothed_revenue": {
            "value": 11047.421875
          }
        },
        {
          "key_as_string": "2024-12-06T00:00:00.000Z",
          "key": 1733443200000,
          "doc_count": 158,
          "daily_revenue": {
            "value": 12109.453125
          },
          "smoothed_revenue": {
            "value": 11505.005208333334
          }
        },
        {
          "key_as_string": "2024-12-07T00:00:00.000Z",
          "key": 1733529600000,
          "doc_count": 153,
          "daily_revenue": {
            "value": 11057.40625
          },
          "smoothed_revenue": {
            "value": 11504.260416666666
          }
        },
        {
          "key_as_string": "2024-12-08T00:00:00.000Z",
          "key": 1733616000000,
          "doc_count": 165,
          "daily_revenue": {
            "value": 13095.609375
          },
          "smoothed_revenue": {
            "value": 11679.807291666666
          }
        },
        {
          "key_as_string": "2024-12-09T00:00:00.000Z",
          "key": 1733702400000,
          "doc_count": 153,
          "daily_revenue": {
            "value": 12574.015625
          },
          "smoothed_revenue": {
            "value": 12087.489583333334
          }
        },
        {
          "key_as_string": "2024-12-10T00:00:00.000Z",
          "key": 1733788800000,
          "doc_count": 158,
          "daily_revenue": {
            "value": 11188.1875
          },
          "smoothed_revenue": {
            "value": 12242.34375
          }
        },
        {
          "key_as_string": "2024-12-11T00:00:00.000Z",
          "key": 1733875200000,
          "doc_count": 160,
          "daily_revenue": {
            "value": 12117.65625
          },
          "smoothed_revenue": {
            "value": 12285.9375
          }
        },
        {
          "key_as_string": "2024-12-12T00:00:00.000Z",
          "key": 1733961600000,
          "doc_count": 159,
          "daily_revenue": {
            "value": 11558.25
          },
          "smoothed_revenue": {
            "value": 11959.953125
          }
        },
        {
          "key_as_string": "2024-12-13T00:00:00.000Z",
          "key": 1734048000000,
          "doc_count": 152,
          "daily_revenue": {
            "value": 11921.1171875
          },
          "smoothed_revenue": {
            "value": 11621.364583333334
          }
        },
        {
          "key_as_string": "2024-12-14T00:00:00.000Z",
          "key": 1734134400000,
          "doc_count": 142,
          "daily_revenue": {
            "value": 11135.03125
          },
          "smoothed_revenue": {
            "value": 11865.674479166666
          }
        }
      ]
    }
  }
}
```

1. Date of the bucket is in default ISO format because we didn’t specify a format
2. Number of orders for this day
3. Raw daily revenue before smoothing
4. First day has no smoothed value as it needs previous days for the calculation
5. Moving average starts from second day, using a 3-day window

::::

::::{tip}
Notice how the smoothed values lag behind the actual values - this is because they need previous days' data to calculate. The first day will always be null when using moving averages.

::::

### Track running totals [aggregations-tutorial-cumulative]

Track running totals over time using the [`cumulative_sum`](elasticsearch://reference/aggregations/search-aggregations-pipeline-cumulative-sum-aggregation.md) aggregation.

```console
GET kibana_sample_data_ecommerce/_search
{
 "size": 0,
 "aggs": {
   "daily_sales": {
     "date_histogram": {
       "field": "order_date",
       "calendar_interval": "day"
     },
     "aggs": {
       "revenue": {
         "sum": {
           "field": "taxful_total_price"
         }
       },
       "cumulative_revenue": { <1>
         "cumulative_sum": { <2>
           "buckets_path": "revenue" <3>
         }
       }
     }
   }
 }
}
```

1. Name for our running total
2. `cumulative_sum` adds up values across buckets
3. Reference the revenue we want to accumulate

::::{dropdown} Example response

```console-result
{
  "took": 4,
  "timed_out": false,
  "_shards": {
    "total": 5,
    "successful": 5,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4675,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "daily_sales": { <1>
      "buckets": [ <2>
        {
          "key_as_string": "2024-11-14T00:00:00.000Z", <3>
          "key": 1731542400000,
          "doc_count": 146,
          "revenue": { <4>
            "value": 10578.53125
          },
          "cumulative_revenue": { <5>
            "value": 10578.53125
          }
        },
        {
          "key_as_string": "2024-11-15T00:00:00.000Z",
          "key": 1731628800000,
          "doc_count": 153,
          "revenue": {
            "value": 10448
          },
          "cumulative_revenue": {
            "value": 21026.53125
          }
        },
        {
          "key_as_string": "2024-11-16T00:00:00.000Z",
          "key": 1731715200000,
          "doc_count": 143,
          "revenue": {
            "value": 10283.484375
          },
          "cumulative_revenue": {
            "value": 31310.015625
          }
        },
        {
          "key_as_string": "2024-11-17T00:00:00.000Z",
          "key": 1731801600000,
          "doc_count": 140,
          "revenue": {
            "value": 10145.5234375
          },
          "cumulative_revenue": {
            "value": 41455.5390625
          }
        },
        {
          "key_as_string": "2024-11-18T00:00:00.000Z",
          "key": 1731888000000,
          "doc_count": 139,
          "revenue": {
            "value": 12012.609375
          },
          "cumulative_revenue": {
            "value": 53468.1484375
          }
        },
        {
          "key_as_string": "2024-11-19T00:00:00.000Z",
          "key": 1731974400000,
          "doc_count": 157,
          "revenue": {
            "value": 11009.45703125
          },
          "cumulative_revenue": {
            "value": 64477.60546875
          }
        },
        {
          "key_as_string": "2024-11-20T00:00:00.000Z",
          "key": 1732060800000,
          "doc_count": 145,
          "revenue": {
            "value": 10720.59375
          },
          "cumulative_revenue": {
            "value": 75198.19921875
          }
        },
        {
          "key_as_string": "2024-11-21T00:00:00.000Z",
          "key": 1732147200000,
          "doc_count": 152,
          "revenue": {
            "value": 11185.3671875
          },
          "cumulative_revenue": {
            "value": 86383.56640625
          }
        },
        {
          "key_as_string": "2024-11-22T00:00:00.000Z",
          "key": 1732233600000,
          "doc_count": 163,
          "revenue": {
            "value": 13560.140625
          },
          "cumulative_revenue": {
            "value": 99943.70703125
          }
        },
        {
          "key_as_string": "2024-11-23T00:00:00.000Z",
          "key": 1732320000000,
          "doc_count": 141,
          "revenue": {
            "value": 9884.78125
          },
          "cumulative_revenue": {
            "value": 109828.48828125
          }
        },
        {
          "key_as_string": "2024-11-24T00:00:00.000Z",
          "key": 1732406400000,
          "doc_count": 151,
          "revenue": {
            "value": 11075.65625
          },
          "cumulative_revenue": {
            "value": 120904.14453125
          }
        },
        {
          "key_as_string": "2024-11-25T00:00:00.000Z",
          "key": 1732492800000,
          "doc_count": 143,
          "revenue": {
            "value": 10323.8515625
          },
          "cumulative_revenue": {
            "value": 131227.99609375
          }
        },
        {
          "key_as_string": "2024-11-26T00:00:00.000Z",
          "key": 1732579200000,
          "doc_count": 143,
          "revenue": {
            "value": 10369.546875
          },
          "cumulative_revenue": {
            "value": 141597.54296875
          }
        },
        {
          "key_as_string": "2024-11-27T00:00:00.000Z",
          "key": 1732665600000,
          "doc_count": 142,
          "revenue": {
            "value": 11711.890625
          },
          "cumulative_revenue": {
            "value": 153309.43359375
          }
        },
        {
          "key_as_string": "2024-11-28T00:00:00.000Z",
          "key": 1732752000000,
          "doc_count": 161,
          "revenue": {
            "value": 12612.6640625
          },
          "cumulative_revenue": {
            "value": 165922.09765625
          }
        },
        {
          "key_as_string": "2024-11-29T00:00:00.000Z",
          "key": 1732838400000,
          "doc_count": 144,
          "revenue": {
            "value": 10176.87890625
          },
          "cumulative_revenue": {
            "value": 176098.9765625
          }
        },
        {
          "key_as_string": "2024-11-30T00:00:00.000Z",
          "key": 1732924800000,
          "doc_count": 157,
          "revenue": {
            "value": 11480.33203125
          },
          "cumulative_revenue": {
            "value": 187579.30859375
          }
        },
        {
          "key_as_string": "2024-12-01T00:00:00.000Z",
          "key": 1733011200000,
          "doc_count": 158,
          "revenue": {
            "value": 11533.265625
          },
          "cumulative_revenue": {
            "value": 199112.57421875
          }
        },
        {
          "key_as_string": "2024-12-02T00:00:00.000Z",
          "key": 1733097600000,
          "doc_count": 144,
          "revenue": {
            "value": 10499.8125
          },
          "cumulative_revenue": {
            "value": 209612.38671875
          }
        },
        {
          "key_as_string": "2024-12-03T00:00:00.000Z",
          "key": 1733184000000,
          "doc_count": 151,
          "revenue": {
            "value": 12111.6875
          },
          "cumulative_revenue": {
            "value": 221724.07421875
          }
        },
        {
          "key_as_string": "2024-12-04T00:00:00.000Z",
          "key": 1733270400000,
          "doc_count": 145,
          "revenue": {
            "value": 10530.765625
          },
          "cumulative_revenue": {
            "value": 232254.83984375
          }
        },
        {
          "key_as_string": "2024-12-05T00:00:00.000Z",
          "key": 1733356800000,
          "doc_count": 157,
          "revenue": {
            "value": 11872.5625
          },
          "cumulative_revenue": {
            "value": 244127.40234375
          }
        },
        {
          "key_as_string": "2024-12-06T00:00:00.000Z",
          "key": 1733443200000,
          "doc_count": 158,
          "revenue": {
            "value": 12109.453125
          },
          "cumulative_revenue": {
            "value": 256236.85546875
          }
        },
        {
          "key_as_string": "2024-12-07T00:00:00.000Z",
          "key": 1733529600000,
          "doc_count": 153,
          "revenue": {
            "value": 11057.40625
          },
          "cumulative_revenue": {
            "value": 267294.26171875
          }
        },
        {
          "key_as_string": "2024-12-08T00:00:00.000Z",
          "key": 1733616000000,
          "doc_count": 165,
          "revenue": {
            "value": 13095.609375
          },
          "cumulative_revenue": {
            "value": 280389.87109375
          }
        },
        {
          "key_as_string": "2024-12-09T00:00:00.000Z",
          "key": 1733702400000,
          "doc_count": 153,
          "revenue": {
            "value": 12574.015625
          },
          "cumulative_revenue": {
            "value": 292963.88671875
          }
        },
        {
          "key_as_string": "2024-12-10T00:00:00.000Z",
          "key": 1733788800000,
          "doc_count": 158,
          "revenue": {
            "value": 11188.1875
          },
          "cumulative_revenue": {
            "value": 304152.07421875
          }
        },
        {
          "key_as_string": "2024-12-11T00:00:00.000Z",
          "key": 1733875200000,
          "doc_count": 160,
          "revenue": {
            "value": 12117.65625
          },
          "cumulative_revenue": {
            "value": 316269.73046875
          }
        },
        {
          "key_as_string": "2024-12-12T00:00:00.000Z",
          "key": 1733961600000,
          "doc_count": 159,
          "revenue": {
            "value": 11558.25
          },
          "cumulative_revenue": {
            "value": 327827.98046875
          }
        },
        {
          "key_as_string": "2024-12-13T00:00:00.000Z",
          "key": 1734048000000,
          "doc_count": 152,
          "revenue": {
            "value": 11921.1171875
          },
          "cumulative_revenue": {
            "value": 339749.09765625
          }
        },
        {
          "key_as_string": "2024-12-14T00:00:00.000Z",
          "key": 1734134400000,
          "doc_count": 142,
          "revenue": {
            "value": 11135.03125
          },
          "cumulative_revenue": {
            "value": 350884.12890625
          }
        }
      ]
    }
  }
}
```

1. `daily_sales`: Results from our daily sales date histogram
2. `buckets`: Array of time-based buckets
3. `key_as_string`: Date for this bucket (in ISO format since no format specified)
4. `revenue`: Daily revenue for this date
5. `cumulative_revenue`: Running total of revenue up to this date

::::

## Next steps [aggregations-tutorial-next-steps]

Refer to the [aggregations reference](../aggregations.md) for more details on all available aggregation types.
