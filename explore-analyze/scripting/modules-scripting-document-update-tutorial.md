---
navigation_title: Updating documents
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Updating documents [updating-documents-tutorial]

In this tutorial you’ll learn how to use Painless scripts to update documents in three scenarios:

* Update a single document with `_update`   
* Update multiple documents that match a query with `_update_by_query`   
* Apply tax calculations across product categories with `_update_by_query`

## Prerequisites

This tutorial uses the kibana\_sample\_data\_ecommerce dataset. Refer to [Context example data](elasticsearch://reference/scripting-languages/painless/painless-context-examples.md) to get started.

## Update a single document with `_update`

The goal is to change the price of a specific product in an order and then update the total price. This tutorial shows how to find a product in an order by its ID, update all of its price fields, and recalculate the order total automatically.

### Understanding the document structure

First, you need to find a valid document ID:

```json
GET kibana_sample_data_ecommerce/_search
{
  "size": 1,
  "_source": false
}
```

Then you run the script, with your ID to check how the document is structured:

```json
GET kibana_sample_data_ecommerce/_doc/YOUR_DOCUMENT_ID  
```

The request returns the following document. Notice the product structure within the `products` array. We will target the price-related fields:

* `products.price`  
* `products.base_price`   
* `products.taxful_price`   
* `products.taxless_price`  
* `products.base_unit_price`


This way, all price-related fields are updated together:

:::{dropdown} Response

```json
{
  ...
  "_source": {
    ...
    "products": [
      {
        "tax_amount": 0,
        "taxful_price": 11.99,
        "quantity": 1,
        "taxless_price": 11.99,
        "discount_amount": 0,
        "base_unit_price": 11.99,
        "discount_percentage": 0,
        "product_name": "Basic T-shirt - dark blue/white",
        "manufacturer": "Elitelligence",
        "min_price": 6.35,
        "created_on": "2016-12-26T09:28:48+00:00",
        "unit_discount_amount": 0,
        "price": 11.99,
        "product_id": 6283,
        "base_price": 11.99,
        "_id": "sold_product_584677_6283",
        "category": "Men's Clothing",
        "sku": "ZO0549605496"
      }
    ],
    ...
  }
}
```

:::

### Writing the update script

Next, we use the `_update` API to change the price of a specific product inside an order. This ensures that only the document with a specific ID is updated.

:::{important} 
Before running this script, make sure to use a `product_id` that exists in your dataset. You can find valid product IDs by examining the document structure as shown in the previous step, or by running a search query to return a list of available products. 
:::

```json
POST kibana_sample_data_ecommerce/_update/YOUR_DOCUMENT_ID
{
  "script": {
    "lang": "painless",
    "source": """
      for (product in ctx._source.products) {
        if (product.product_id == params.product_id) {
          double old_price = product.taxful_price;
          double new_price = params.new_price;
          double price_diff = (new_price - old_price) * product.quantity;
          
          // Update products prices
          product.price = new_price;
          product.taxful_price = new_price;
          product.taxless_price = new_price;
          product.base_price = new_price;
          product.base_unit_price = new_price;
          
          // Total amount of the order
          ctx._source.taxful_total_price += price_diff;
          ctx._source.taxless_total_price += price_diff;
          
          break;
        }
      }
    """,
    "params": {
      "product_id": 6283, 
      "new_price": 70
    }
  }
}
```

This script includes the following steps:

1. **Iterate through products:** The script loops through each product in the `ctx._source.products` array  
2. **Find the target product:** It compares each `product.product_id` with the parameter value  
3. **Calculate price difference:** It determines how much the total order amount should change   
4. **Update all price fields:** Multiple price fields are updated to maintain data consistency  
5. **Update order totals:** The script adjusts the total order amounts  
6. **Exit the loop:** The `break` statement prevents unnecessary iterations after finding the product  
   

For more details about Painless scripting in the update context, refer to the [Painless update context documentation](elasticsearch://reference/scripting-languages/painless/painless-update-context.md).

:::{dropdown} Response

```json
{
  "_index": "kibana_sample_data_ecommerce",
  "_id": "MnacyJgBTbKqUnB54Eep",
  "_version": 2,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 2,
    "failed": 0
  },
  "_seq_no": 4675,
  "_primary_term": 1
}
```

:::

### Verifying the update

To confirm the update worked correctly, search for the document again:

```json
GET kibana_sample_data_ecommerce/_doc/YOUR_DOCUMENT_ID
```

If everything works correctly, when we update the price, all fields that include it will also be updated. The final document will look like the following if the price is changed to 70.00:

```json
{
  ...
  "_source": {
    ...
    "products": [
      {
        "tax_amount": 0,
        "taxful_price": 70,
        "quantity": 1,
        "taxless_price": 70,
        "discount_amount": 0,
        "base_unit_price": 70,
        "discount_percentage": 0,
        "product_name": "Basic T-shirt - dark blue/white",
        "manufacturer": "Elitelligence",
        "min_price": 6.35,
        "created_on": "2016-12-26T09:28:48+00:00",
        "unit_discount_amount": 0,
        "price": 70,
        "product_id": 6283,
        "base_price": 70,
        "_id": "sold_product_584677_6283",
        "category": "Men's Clothing",
        "sku": "ZO0549605496"
      }
    ],
    ...
    "taxful_total_price": 94.99000000000001,
    "taxless_total_price": 94.99000000000001,
    ...
  }
}
```

## Update multiple documents with `_update_by_query`

The `_update_by_query` API allows you to update multiple documents that match a specific query. You can apply changes to different documents at the same time for tasks like data cleanup, standardization, or any other case where you need to update multiple documents at once.

### Finding documents to update

In the following example, we will update all orders where the customer phone number is empty by setting it to “N/A”.

Let’s find orders with empty customer phone numbers that need to be standardized:

```json
GET kibana_sample_data_ecommerce/_search
{
  "size": 5,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "customer_phone": ""
          }
        }
      ]
    }
  }
}
```

This returns documents where the `customer_phone` field is empty:

```json
{
  ...
  "hits": {
   ...
    "hits": [
      {
        ...
        "_source": {
          ...
          "customer_phone": "",
          ...
        }
      },
      ...
    ]
  }
}
```

### Writing the update script for multiple documents

Now we’ll update all documents with empty phone numbers to have a standardized “N/A” value and add audit fields:

```json
POST kibana_sample_data_ecommerce/_update_by_query
{
  "query": {
    "bool": {
      "filter": [
        {"term": {"customer_phone": ""}}
      ]
    }
  },
  "script": {
    "lang": "painless",
    "source": """
      ctx._source.customer_phone = 'N/A';
      ctx._source.updated_at = new Date();
    """
  }
}
```

This script includes the following steps:

1. **Set a standard value:** Changes empty phone numbers to “N/A”  
2. **Record timestamps:** Captures when the update occurred

For more details about the update by query API parameters and options, refer to the [Update by query API documentation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-update-by-query).

:::{dropdown} Response

```json
{
  "took": 1997,
  "timed_out": false,
  "total": 4675,
  "updated": 4675,
  "deleted": 0,
  "batches": 5,
  "version_conflicts": 0,
  "noops": 0,
  "retries": {
    "bulk": 0,
    "search": 0
  },
  "throttled_millis": 0,
  "requests_per_second": -1,
  "throttled_until_millis": 0,
  "failures": []
}
```

:::

### Verifying the update

Confirm the updates were applied by searching for documents with the new phone value:

```json
GET kibana_sample_data_ecommerce/_search
{
  "size": 5,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "customer_phone": "N/A"
          }
        }
      ]
    }
  }
}
```

:::{dropdown} Response

```json
{
  ...
  "hits": {
   ...
    "hits": [
      {
        ...
        "_source": {
          ...
          "customer_phone": "N/A",
          ...
        }
      }
    ]
  }
}


```

:::

## Apply tax calculations with `_update_by_query`

In this example, we need to fix an incorrect tax assignment for a specific product category. Many e-commerce systems need to apply tax corrections after the initial data import or when tax regulations change.  

### Understanding the tax correction scenario

Currently, some products in the “Men’s Clothing” category have incorrect tax information where taxes haven’t been applied:

```json
{
  "tax_amount": 0,
  "taxful_price": 24.99,
  "taxless_price": 24.99,
  "category": "Men's Clothing"
}
```

We need to apply a 21% VAT to all untaxed “Men’s Clothing” products and recalculate both individual product prices and order totals.

### Writing the tax calculation script

To update all affected documents, we use a query filtered by category and a script that recalculates taxes.

```json
POST kibana_sample_data_ecommerce/_update_by_query
{
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "products.category.keyword": "Men's Clothing"
          }
        }
      ]
    }
  },
  "script": {
    "lang": "painless",
    "source": """
      double tax_rate = params.tax_rate; // 21% VAT
      double total_tax_adjustment = 0;
      
      for (product in ctx._source.products) {
        if (product.category == "Men's Clothing" && product.tax_amount == 0) {
          // Calculate tax based on the taxless price
          double tax_amount = Math.round((product.taxless_price * tax_rate) * 100.0) / 100.0;
          double new_taxful_price = product.taxless_price + tax_amount;
          
          // Update tax fields of the product
          product.tax_amount = tax_amount;
          product.taxful_price = new_taxful_price;
          product.price = new_taxful_price;
          
          total_tax_adjustment += tax_amount * product.quantity;
        }
      }
      
      // Update order totals
      if (total_tax_adjustment > 0) {
        ctx._source.taxful_total_price += total_tax_adjustment;
        ctx._source.updated_timestamp = new Date();
      }
    """,
    "params": {
      "tax_rate": 0.21
    }
  }
}
```

This script includes the following steps:

1. **Filter by category:** Only processes orders containing “Men’s Clothing” products  
2. **Identify untaxed items:** Checks for products where `tax_amount` equals 0  
3. **Calculate VAT:** Applies 21% tax rate to the `taxless_price`  
4. **Update product fields:** Sets `tax_amount`, `taxful_price`, and `price`  
5. **Accumulate adjustments:** Tracks total tax changes across all products  
6. **Update order totals:** Adjusts the overall order `taxful_total_price`

For more details and examples, refer to the [Update by query context documentation](elasticsearch://reference/scripting-languages/painless/painless-update-by-query-context.md).

:::{dropdown} Response

```json

{
  "took": 789,
  "timed_out": false,
  "total": 2024,
  "updated": 2024,
  "deleted": 0,
  "batches": 3,
  "version_conflicts": 0,
  "noops": 0,
  "retries": {
    "bulk": 0,
    "search": 0
  },
  "throttled_millis": 0,
  "requests_per_second": -1,
  "throttled_until_millis": 0,
  "failures": []
}
```

:::

### Verifying the tax calculation update

Finally, running a search confirms that the tax update was applied:

```json

GET kibana_sample_data_ecommerce/_search
{
  "size": 1,
  "query": {
    "bool": {
      "filter": [
        {
          "term": {
            "products.category.keyword": "Men's Clothing"
          }
        }
      ]
    }
  }
}
```

:::{dropdown} Response

```json

{
  ...
  "hits": {
    ...
    "hits": [
      {
        ...
        "_source": {
          ...
          "products": [
            {
              "tax_amount": 226.8,
              "taxful_price": 1306.78,
              "quantity": 2,
              "taxless_price": 1079.98,
              "discount_amount": 0,
              "base_unit_price": 539.99,
              "discount_percentage": 0,
              "product_name": "Leather jacket - black",
              "manufacturer": "Oceanavigations",
              "min_price": 259.2,
              "created_on": "2016-12-05T06:16:12+00:00",
              "unit_discount_amount": 0,
              "price": 1306.78,
              "product_id": 2669,
              "base_price": 1079.98,
              "_id": "sold_product_739290_2669",
              "category": "Men's Clothing",
              "sku": "ZO0288302883"
            },
            ...
          ],
          ...
          "taxless_total_price": 2249.92,
          ...
          "taxful_total_price": 3194.92
        }
      }
    ]
  }
}
```

:::

## When to use each method

Choose the right API based on your use case:

### Use `_update` when:

* Updating, deleting or skipping the modification of a document  
* [Updating a part of a document](elasticsearch://reference/elasticsearch/rest-apis/update-document.md#update-part-document)  
* [Inserting or updating documents with upsert](elasticsearch://reference/elasticsearch/rest-apis/update-document.md#upsert)

### Use `_update_by_query` when:

* [Running a basic update](elasticsearch://reference/elasticsearch/rest-apis/update-by-query-api.md#run-basic-updates)  
* Updating multiple documents based on search criteria  
* [Updating the document source](elasticsearch://reference/elasticsearch/rest-apis/update-by-query-api.md#update-the-document-source)   
* [Updating documents using an ingest pipeline](elasticsearch://reference/elasticsearch/rest-apis/update-by-query-api.md#update-documents-using-an-ingest-pipeline)

For detailed API specifications, refer to the [Update a document](elasticsearch://reference/elasticsearch/rest-apis/update-document.md) and [Update by query API documentation](elasticsearch://reference/elasticsearch/rest-apis/update-by-query-api.md).
