---
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Painless syntax-context bridge [painless-syntax-context-bridge]

One of the most distinctive aspects of Painless scripting is how data access methods (`doc`, `ctx`, and `_source`) are directly tied to the context of use. Unlike other scripting languages where data access patterns remain consistent, Painless provides different access mechanisms that are optimized for specific use cases and contexts within {{es}}.  
Understanding when and why to use each access method is crucial for writing efficient Painless scripts.

:::{tip}
If you're new to Painless contexts, refer to [Painless contexts](elasticsearch://reference/scripting-languages/painless/painless-contexts.md) in the Reference section for comprehensive context documentation. For hands-on examples of field access, refer to our set of [Painless script tutorials](/explore-analyze/scripting/common-script-uses.md).
:::

## Technical differences

* [**`doc` values**](#when-to-use-doc-values)) use columnar field value store enabled by default on all the fields except analyzed text fields. They can only return simple field values such as numbers, dates, geo-points, and terms.  
* [**`ctx` access**](#when-to-use-ctx) provides structured access to document content during modification contexts, with fields accessible as map and list structures for existing document fields.  
* [**`_source` access**](#when-to-use-source) loads the complete document as a map-of-maps, optimized for returning several fields per result but slower than doc values for single field access.


Check the [decision matrix](#decision-matrix) to decide between these.




## When to use `doc` values (recommended) [when-to-use-doc-values]

* **You should always start with `doc` values** as your first option for field access. This is the fastest and most efficient way to access field values in Painless scripts. Refer to [Doc values](/explore-analyze/scripting/modules-scripting-fields.md#modules-scripting-doc-vals) to learn more.  
* **Painless context examples:**   
  * [Sort context](elasticsearch://reference/scripting-languages/painless/painless-sort-context.md)  
  * [Aggregation scripts](elasticsearch://reference/scripting-languages/painless/painless-metric-agg-init-context.md)  
  * [Score scripts](elasticsearch://reference/scripting-languages/painless/painless-score-context.md)  
* **Syntax pattern:** `doc[‘field_name’].value`

### Example: Aggregation calculation

The following example calculates the average price per item across all orders by dividing `taxful_total_price` by `total_quantity` for each document. The `avg` [aggregation](/explore-analyze/query-filter/aggregations.md) then computes the average of these calculated values.

```java

GET kibana_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "avg_price_per_item": {
      "avg": {
        "script": {
          "source": "doc['taxful_total_price'].value / doc['total_quantity'].value"
        }
      }
    }
  }
}
```

## When to use `ctx` [when-to-use-ctx]

* Use `ctx` for document modification and pipeline processing where you need access to document metadata, content, and operational control.  
* **Painless context examples:**   
  * [Update context](elasticsearch://reference/scripting-languages/painless/painless-update-context.md)  
  * [Ingest processor context](elasticsearch://reference/scripting-languages/painless/painless-ingest-processor-context.md)  
  * [Reindex context](elasticsearch://reference/scripting-languages/painless/painless-reindex-context.md)  
* **Syntax pattern:** `ctx.field_name,` `` ctx._source.field_name, and `ctx[‘field_name’]` ``

### Example: Ingest pipeline processing

The following example creates an [ingest pipeline](/manage-data/ingest/transform-enrich/ingest-pipelines.md) named `create_summary` with a [script processor](elasticsearch://reference/enrich-processor/script-processor.md). This script assigns a text value to the field `order_summary` by combining the customer name and the price.

```java
PUT _ingest/pipeline/create_summary
{
  "processors": [
    {
      "script": {
        "source": """
          ctx.order_summary = ctx.customer_full_name + ' - $' + ctx.taxful_total_price;
        """
      }
    }
  ]
}
```

## When to use `_source` [when-to-use-source]

* **Use `_source` for** document updates and transformations where you need full JSON document access.  
* **Painless context examples:**   
  * [Update by query](elasticsearch://reference/scripting-languages/painless/painless-update-by-query-context.md)  
  * [Runtime fields contexts](elasticsearch://reference/scripting-languages/painless/painless-runtime-fields-context.md)  
* **Syntax patterns:** `ctx._source.field_name`

### Example: Document transformation with calculations

Let’s use `_update_by_query` to calculate loyalty points from the order’s total price multiplied by a parameter rate for high-value orders.

```java
POST /kibana_sample_data_ecommerce/_update_by_query
{
  "query": {
    "range": {
      "taxful_total_price": {"gte": 1000}
    }
  },
  "script": {
    "source": """
      ctx._source.loyalty_points = Math.round(ctx._source.taxful_total_price * params.points_rate);
    """,
    "params": {
      "points_rate": 2.0
    }
  }
}
```

## Decision matrix [decision-matrix]

| Scenario | Required Access Method | Reason |
| :---- | :---- | :---- |
| [Aggregation calculations](/explore-analyze/scripting/modules-scripting-fields.md#modules-scripting-source) | `doc` | Columnar storage provides fastest performance |
| [Document scoring](/explore-analyze/scripting/modules-scripting-fields.md#_search_and_aggregation_scripts)  | `doc` | Optimized for search-time calculations |
| [Script fields (top results)](/explore-analyze/scripting/modules-scripting-fields.md#modules-scripting-source) | `_source` | Optimized for returning several fields per result |
| [Adding fields during ingest](elasticsearch://reference/scripting-languages/painless/painless-ingest-processor-context.md) | `ctx` | Direct field access during pipeline processing |
| [Updating existing documents](/explore-analyze/scripting/modules-scripting-fields.md#_update_scripts) | `ctx._source` | Full document modification capabilities |
| [Document transformation during reindex](elasticsearch://reference/scripting-languages/painless/painless-reindex-context.md) | `ctx._source` | Complete document restructuring with metadata access |
| [Sort operations](elasticsearch://reference/scripting-languages/painless/painless-sort-context.md) | `doc` | Single-field performance optimization for sorting |
| [Runtime field with simple values](elasticsearch://reference/scripting-languages/painless/painless-runtime-fields-context.md) | `doc` | Performance advantage for repeated calculations |
| [Runtime field with complex logic](elasticsearch://reference/scripting-languages/painless/painless-runtime-fields-context.md) | `params[‘_source’]` | Access to complete document structure with `emit` |

## Next steps

* **New users:** Explore Accessing [Accessing document fields and special variables](/explore-analyze/scripting/modules-scripting-fields.md)  
* **Advanced users:** Review [Painless contexts](elasticsearch://reference/scripting-languages/painless/painless-contexts.md) for context-specific implementation details


