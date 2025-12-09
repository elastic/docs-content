---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/ecommerce-transforms.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Tutorial: Transforming the eCommerce sample data [ecommerce-transforms]

[Transforms](../transforms.md) enable you to retrieve information from an {{es}} index, transform it, and store it in another index. Let’s use the [{{kib}} sample data](/explore-analyze/index.md) to demonstrate how you can pivot and summarize your data with transforms.

1. Verify that your environment is set up properly to use transforms. If the {{es}} {{security-features}} are enabled, to complete this tutorial you need a user that has authority to preview and create transforms. You must also have specific index privileges for the source and destination indices. See [Setup](transform-setup.md).
2. Choose your *source index*.

    In this example, we’ll use the eCommerce orders sample data. If you’re not already familiar with the `kibana_sample_data_ecommerce` index, use the **Revenue** dashboard in {{kib}} to explore the data. Consider what insights you might want to derive from this eCommerce data.

3. Choose the pivot type of transform and play with various options for grouping and aggregating the data.

   There are two types of transforms, but first we’ll try out *pivoting* your data, which involves using at least one field to group it and applying at least one aggregation. You can preview what the transformed data will look like, so go ahead and play with it! You can also enable histogram charts to get a better understanding of the distribution of values in your data.

   For example, you might want to group the data by product ID and calculate the total number of sales for each product and its average price. Alternatively, you might want to look at the behavior of individual customers and calculate how much each customer spent in total and how many different categories of products they purchased. Or you might want to take the currencies or geographies into consideration. What are the most interesting ways you can transform and interpret this data?

   Go to the **Transforms** management page in {{kib}} using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then use the wizard to create a transform:
   :::{image} /explore-analyze/images/elasticsearch-reference-ecommerce-pivot1.png
   :alt: Creating a simple transform in {{kib}}
   :screenshot:
   :::

   Group the data by customer ID and add one or more aggregations to learn more about each customer’s orders. For example, let’s calculate the sum of products they purchased, the total price of their purchases, the maximum number of products that they purchased in a single order, and their total number of orders. We’ll accomplish this by using the [`sum` aggregation](elasticsearch://reference/aggregations/search-aggregations-metrics-sum-aggregation.md) on the `total_quantity` and `taxless_total_price` fields, the [`max` aggregation](elasticsearch://reference/aggregations/search-aggregations-metrics-max-aggregation.md) on the `total_quantity` field, and the [`cardinality` aggregation](elasticsearch://reference/aggregations/search-aggregations-metrics-cardinality-aggregation.md) on the `order_id` field:

   :::{image} /explore-analyze/images/elasticsearch-reference-ecommerce-pivot2.png
   :alt: Adding multiple aggregations to a transform in {{kib}}
   :screenshot:
   :::

   ::::{tip}
   If you’re interested in a subset of the data, you can optionally include a [query](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search) element. In this example, we’ve filtered the data so that we’re only looking at orders with a `currency` of `EUR`. Alternatively, we could group the data by that field too. If you want to use more complex queries, you can create your {{dataframe}} from a [saved search](../discover/save-open-search.md).
   ::::

   If you prefer, you can use the [preview transforms API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-preview-transform).

   ::::{dropdown} API example
   ```console
   POST _transform/_preview
    {
      "source": {
        "index": "kibana_sample_data_ecommerce",
        "query": {
          "bool": {
            "filter": {
              "term": {"currency": "EUR"}
            }
          }
        }
      },
      "pivot": {
        "group_by": {
          "customer_id": {
            "terms": {
              "field": "customer_id"
            }
          }
        },
        "aggregations": {
          "total_quantity.sum": {
            "sum": {
              "field": "total_quantity"
            }
          },
          "taxless_total_price.sum": {
            "sum": {
              "field": "taxless_total_price"
            }
          },
          "total_quantity.max": {
            "max": {
              "field": "total_quantity"
            }
          },
          "order_id.cardinality": {
            "cardinality": {
              "field": "order_id"
            }
          }
        }
      }
    }
   ```

   ::::

4. When you are satisfied with what you see in the preview, create the transform.
   1. Supply a transform ID, the name of the destination index and optionally a description. If the destination index does not exist, it will be created automatically when you start the transform.
   2. Decide whether you want the transform to run once or continuously. Since this sample data index is unchanging, let's use the default behavior and run the transform once. If you want to try it out, however, go ahead and click on **Continuous mode**. You must choose a field that the transform can use to check which entities have changed. In general, it's a good idea to use the ingest timestamp field. In this example, however, you can use the `order_date` field.
   3. Optionally, you can configure a retention policy that applies to your transform. Select a date field that is used to identify old documents in the destination index and provide a maximum age. Documents that are older than the configured value are removed from the destination index.
   :::{image} /explore-analyze/images/elasticsearch-reference-ecommerce-pivot3.png
   :alt: Adding transfrom ID and retention policy to a transform in {{kib}}
   :screenshot:
   :::

   In {{kib}}, before you finish creating the transform, you can copy the preview transform API request to your clipboard. This information is useful later when you’re deciding whether you want to manually create the destination index.
   :::{image} /explore-analyze/images/elasticsearch-reference-ecommerce-pivot4.png
   :alt: Copy the Dev Console statement of the transform preview to the clipboard
   :screenshot:
   :::

   If you prefer, you can use the [create transforms API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-put-transform).

   ::::{dropdown} API example
   ```console
   PUT _transform/ecommerce-customer-transform
    {
      "source": {
        "index": [
          "kibana_sample_data_ecommerce"
        ],
        "query": {
          "bool": {
            "filter": {
              "term": {
                "currency": "EUR"
              }
            }
          }
        }
      },
      "pivot": {
        "group_by": {
          "customer_id": {
            "terms": {
              "field": "customer_id"
            }
          }
        },
        "aggregations": {
          "total_quantity.sum": {
            "sum": {
              "field": "total_quantity"
            }
          },
          "taxless_total_price.sum": {
            "sum": {
              "field": "taxless_total_price"
            }
          },
          "total_quantity.max": {
            "max": {
              "field": "total_quantity"
            }
          },
          "order_id.cardinality": {
            "cardinality": {
              "field": "order_id"
            }
          }
        }
      },
      "dest": {
        "index": "ecommerce-customers"
      },
      "retention_policy": {
        "time": {
          "field": "order_date",
          "max_age": "60d"
        }
      }
    }
   ```

   ::::

5. Optional: Create the destination index.
   If the destination index does not exist, it is created the first time you start your transform. A pivot transform deduces the mappings for the destination index from the source indices and the transform aggregations. If there are fields in the destination index that are derived from scripts (for example, if you use [`scripted_metrics`](elasticsearch://reference/aggregations/search-aggregations-metrics-scripted-metric-aggregation.md) or [`bucket_scripts`](elasticsearch://reference/aggregations/search-aggregations-pipeline-bucket-script-aggregation.md) aggregations), they’re created with [dynamic mappings](../../manage-data/data-store/mapping/dynamic-mapping.md). You can use the preview transform API to preview the mappings it will use for the destination index. In {{kib}}, if you copied the API request to your clipboard, paste it into the console, then refer to the `generated_dest_index` object in the API response.
   ::::{note}
   Transforms might have more configuration options provided by the APIs than the options available in {{kib}}. For example, you can set an ingest pipeline for `dest` by calling the [Create transform](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-put-transform). For all the transform configuration options, refer to the [documentation](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-transform).
   ::::

   ::::{dropdown} API example
   ```console-result
    {
      "preview" : [
        {
          "total_quantity" : {
            "max" : 2,
            "sum" : 118.0
          },
          "taxless_total_price" : {
            "sum" : 3946.9765625
          },
          "customer_id" : "10",
          "order_id" : {
            "cardinality" : 59
          }
        },
        ...
      ],
      "generated_dest_index" : {
        "mappings" : {
          "_meta" : {
            "_transform" : {
              "transform" : "transform-preview",
              "version" : {
                "created" : "8.0.0"
              },
              "creation_date_in_millis" : 1621991264061
            },
            "created_by" : "transform"
          },
          "properties" : {
            "total_quantity.sum" : {
              "type" : "double"
            },
            "total_quantity" : {
              "type" : "object"
            },
            "taxless_total_price" : {
              "type" : "object"
            },
            "taxless_total_price.sum" : {
              "type" : "double"
            },
            "order_id.cardinality" : {
              "type" : "long"
            },
            "customer_id" : {
              "type" : "keyword"
            },
            "total_quantity.max" : {
              "type" : "integer"
            },
            "order_id" : {
              "type" : "object"
            }
          }
        },
        "settings" : {
          "index" : {
            "number_of_shards" : "1",
            "auto_expand_replicas" : "0-1"
          }
        },
        "aliases" : { }
      }
    }
   ```

   ::::

   In some instances the deduced mappings might be incompatible with the actual data. For example, numeric overflows might occur or dynamically mapped fields might contain both numbers and strings. To avoid this problem, create your destination index before you start the transform. For more information, see the [create index API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-create).

   ::::{dropdown} API example
   You can use the information from the transform preview to create the destination index. For example:

   ```console
   PUT /ecommerce-customers
    {
      "mappings": {
        "properties": {
          "total_quantity.sum" : {
            "type" : "double"
          },
          "total_quantity" : {
            "type" : "object"
          },
          "taxless_total_price" : {
            "type" : "object"
          },
          "taxless_total_price.sum" : {
            "type" : "double"
          },
          "order_id.cardinality" : {
            "type" : "long"
          },
          "customer_id" : {
            "type" : "keyword"
          },
          "total_quantity.max" : {
            "type" : "integer"
          },
          "order_id" : {
            "type" : "object"
          }
        }
      }
    }
   ```

   ::::

6. Start the transform.
   ::::{tip}
   Even though resource utilization is automatically adjusted based on the cluster load, a transform increases search and indexing load on your cluster while it runs. If you’re experiencing an excessive load, however, you can stop it.
   ::::

   You can start, stop, reset, and manage transforms in {{kib}}:
   :::{image} /explore-analyze/images/elasticsearch-reference-manage-transforms.png
   :alt: Managing transforms in {{kib}}
   :screenshot:
   :::

   Alternatively, you can use the [start transforms](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-start-transform), [stop transforms](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-stop-transform) and [reset transforms](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-reset-transform) APIs.

   If you reset a transform, all checkpoints, states, and the destination index (if it was created by the transform) are deleted. The transform is ready to start again as if it were newly created.

   ::::{dropdown} API example
   ```console
   POST _transform/ecommerce-customer-transform/_start
   ```

   ::::

   ::::{tip}
   If you chose a batch transform, it is a single operation that has a single checkpoint. You cannot restart it when it’s complete. {{ctransforms-cap}} differ in that they continually increment and process checkpoints as new source data is ingested.
   ::::

7. Explore the data in your new index.
   For example, use the **Discover** application in {{kib}}:
   :::{image} /explore-analyze/images/elasticsearch-reference-ecommerce-results.png
   :alt: Exploring the new index in {{kib}}
   :screenshot:
   :::

8. Optional: Create another transform, this time using the `latest` method.
   This method populates the destination index with the latest documents for each unique key value. For example, you might want to find the latest orders (sorted by the `order_date` field) for each customer or for each country and region.
   :::{image} /explore-analyze/images/elasticsearch-reference-ecommerce-latest1.png
   :alt: Creating a latest transform in {{kib}}
   :screenshot:
   :::

   ::::{dropdown} API example
   ```console
   POST _transform/_preview
    {
      "source": {
        "index": "kibana_sample_data_ecommerce",
        "query": {
          "bool": {
            "filter": {
              "term": {"currency": "EUR"}
            }
          }
        }
      },
      "latest": {
        "unique_key": ["geoip.country_iso_code", "geoip.region_name"],
        "sort": "order_date"
      }
    }
   ```

   ::::

   ::::{tip}
   If the destination index does not exist, it is created the first time you start your transform. Unlike pivot transforms, however, latest transforms do not deduce mapping definitions when they create the index. Instead, they use dynamic mappings. To use explicit mappings, create the destination index before you start the transform.
   ::::

9. If you do not want to keep a transform, you can delete it in {{kib}} or use the [delete transform API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-delete-transform). By default, when you delete a transform, its destination index and {{kib}} index patterns remain.

Now that you’ve created simple transforms for {{kib}} sample data, consider possible use cases for your own data. For more ideas, see [When to use transforms](transform-usage.md) and [Examples](transform-examples.md).
