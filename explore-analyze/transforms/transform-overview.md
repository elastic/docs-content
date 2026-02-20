---
navigation_title: Overview
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/transform-overview.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Transforms overview [transform-overview]

You can choose either of the following methods to transform your data: [pivot](#pivot-transform-overview) or [latest](#latest-transform-overview).

::::{important}

* All transforms leave your source index intact. They create a new index that is dedicated to the transformed data.
* Transforms might have more configuration options provided by the APIs than the options available in {{kib}}. For all the transform configuration options, refer to the [API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-transform).

::::

Transforms are persistent tasks; they are stored in cluster state which makes them resilient for node failures. Refer to [How checkpoints work](transform-checkpoints.md) and [Error handling](transform-checkpoints.md#ml-transform-checkpoint-errors) to learn more about the machinery behind transforms.

## Pivot transforms [pivot-transform-overview]

You can use transforms to *pivot* your data into a new entity-centric index. By transforming and summarizing your data, it becomes possible to visualize and analyze it in alternative and interesting ways.

A lot of {{es}} indices are organized as a stream of events: each event is an individual document, for example a single item purchase. Transforms enable you to summarize this data, bringing it into an organized, more analysis-friendly format. For example, you can summarize all the purchases of a single customer.

Transforms enable you to define a pivot, which is a set of features that transform the index into a different, more digestible format. Pivoting results in a summary of your data in a new index.

To define a pivot, first you select one or more fields that you will use to group your data. You can select categorical fields (terms) and numerical fields for grouping. If you use numerical fields, the field values are bucketed using an interval that you specify.

The second step is deciding how you want to aggregate the grouped data. When using aggregations, you practically ask questions about the index. There are different types of aggregations, each with its own purpose and output. To learn more about the supported aggregations and group-by fields, see [Create transform](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-put-transform).

As an optional step, you can also add a query to further limit the scope of the aggregation.

The transform performs a composite aggregation that paginates through all the data defined by the source index query. The output of the aggregation is stored in a *destination index*. Each time the transform queries the source index, it creates a *checkpoint*. You can decide whether you want the transform to run once or continuously. A *batch transform* is a single operation that has a single checkpoint. *{{ctransforms-cap}}* continually increment and process checkpoints as new source data is ingested.

Imagine that you run a webshop that sells clothes. Every order creates a document that contains a unique order ID, the name and the category of the ordered product, its price, the ordered quantity, the exact date of the order, and some customer information (name, gender, location, and so on). Your data set contains all the transactions from last year.

If you want to check the sales in the different categories in your last fiscal year, define a transform that groups the data by the product categories (women's shoes, men's clothing, and so on) and the order date. Use the last year as the interval for the order date. Then add a sum aggregation on the ordered quantity. The result is an entity-centric index that shows the number of sold items in every product category in the last year.

:::{image} /explore-analyze/images/elasticsearch-reference-pivot-preview.png
:alt: Example of a pivot transform preview in {{kib}}
:screenshot:
:::

## Latest transforms [latest-transform-overview]

You can use the `latest` type of transform to copy the most recent documents into a new index. You must identify one or more fields as the unique key for grouping your data, as well as a date field that sorts the data chronologically. For example, you can use this type of transform to keep track of the latest purchase for each customer or the latest event for each host.

:::{image} /explore-analyze/images/elasticsearch-reference-latest-preview.png
:alt: Example of a latest transform preview in {{kib}}
:screenshot:
:::

As in the case of a pivot, a latest transform can run once or continuously. It performs a composite aggregation on the data in the source index and stores the output in the destination index. If the transform runs continuously, new unique key values are automatically added to the destination index and the most recent documents for existing key values are automatically updated at each checkpoint.

## Performance considerations [transform-performance]

Transforms perform search aggregations on the source indices then index the results into the destination index. Therefore, a transform never takes less time or uses less resources than the aggregation and indexing processes.

If your transform must process a lot of historic data, it has high resource usage initially—particularly during the first checkpoint.

For better performance, make sure that your search aggregations and queries are optimized and that your transform is processing only necessary data. Consider whether you can apply a source query to the transform to reduce the scope of data it processes. Also consider whether the cluster has sufficient resources in place to support both the composite aggregation search and the indexing of its results.

If you prefer to spread out the impact on your cluster (at the cost of a slower transform), you can throttle the rate at which it performs search and index requests. Set the `docs_per_second` limit when you [create](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-put-transform) or [update](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-update-transform) your transform. If you want to calculate the current rate, use the following information from the [get transform stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-get-transform-stats):

```
documents_processed / search_time_in_ms * 1000
```
