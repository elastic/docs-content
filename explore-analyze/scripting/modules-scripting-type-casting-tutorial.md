---
navigation_title: Converting data types
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Converting data types [type-casting-tutorial]

In this tutorial you’ll learn how to use Painless scripts to convert data types in two scenarios:

* Tax corrections using type casting for precise calculations  
* Convert calculated scores to boolean flags

## Prerequisites

This tutorial uses the `kibana_sample_data_ecommerce` dataset. Refer to [Context example data](elasticsearch://reference/scripting-languages/painless/painless-context-examples.md) to get started.

## Type casting used in this tutorial

Painless supports multiple [casting](elasticsearch://reference/scripting-languages/painless/painless-casting.md) approaches. In this tutorial we use:

* **Explicit casting** uses the `(type)` operator to force a conversion, for example `(long)value`.  
* **Implicit casting** happens automatically when combining types in expressions, such as dividing a `long` by a `double`, which promotes the result to `double`.

## Tax Corrections using type casting for precise calculations (ingest context)

In this example, we will recalculate taxes by region using explicit and implicit type casting in Painless. This ensures precise totals across orders and products in line with regional tax policies.

### Understanding the precision in financial calculations

Binary floating-point arithmetic introduces errors in monetary calculations (0.1 \+ 0.2 \= 0.30000000000000004). To avoid this, {{es}} recommends using integers for the smallest currency unit. The [`scaled_float`](elasticsearch://reference/elasticsearch/mapping-reference/number.md) field type uses this pattern, storing prices as integer cents, while the API treats them as doubles. This ensures exact arithmetic, such as 10 \+ 20 \= 30 cents. 

### Writing the Painless script

The script recalculates regional taxes using explicit casting to convert prices to cents (long), applies country-specific tax rates (5% for AE, 20% for GB), and uses implicit casting when dividing the result back to decimal format. This avoids floating-point errors during tax computations.

Create an ingest pipeline that recalculates regional taxes using type casting for precision:

```json
PUT _ingest/pipeline/kibana_sample_data_ecommerce-tax_correction
{
  "description": "Recalculate taxes by region using type casting",
  "processors": [
    {
      "script": {
        "lang": "painless",
        "source": """
          // Explicit casting: convert prices to long for high-precision calculations
          if (ctx.taxless_total_price != null) {
            long taxlessAmountCents = (long) (ctx.taxless_total_price * 100);
            
            // Regional tax rates by country
            Map taxRates = [
              'US': 0.08, 'GB': 0.20, 'DE': 0.19, 'FR': 0.20,
              'AE': 0.05, 'EG': 0.14, 'default': 0.10
            ];
            
            String countryCode = ctx.geoip?.country_iso_code ?: 'default';
            double taxRate = taxRates.getOrDefault(countryCode, 0.10);
            
            // Explicit casting: double to long
            long taxAmountCents = (long) (taxlessAmountCents * taxRate);
            // Implicit casting: long to double
            double correctedTaxAmount = taxAmountCents / 100.0;
            
            ctx.corrected_tax_amount = correctedTaxAmount;
            ctx.corrected_total_price = ctx.taxless_total_price + correctedTaxAmount;
            ctx.tax_country_code = countryCode;
          }
        """
      }
    }
  ]
}
```

This script includes the following steps:

* **Explicit casting:** `(long) (taxlessAmountCents * taxRate)` converts the double result to long for precise calculations  
* **Implicit casting:** `taxAmountCents / 100.0` automatically promotes long to double during division


For more details about Painless scripting in the ingest context, refer to [Ingest processor context](elasticsearch://reference/scripting-languages/painless/painless-ingest-processor-context.md). 

### Test the pipeline

Simulate the pipeline with sample documents to confirm tax calculations works correctly:

```json
POST _ingest/pipeline/kibana_sample_data_ecommerce-tax_correction/_simulate
{
  "docs": [
    {
      "_source": {
        "taxless_total_price": 44.98,
        "geoip": {
          "country_iso_code": "AE"
        }
      }
    },
    {
      "_source": {
        "taxless_total_price": 189.50,
        "geoip": {
          "country_iso_code": "GB"
        }
      }
    }
  ]
}
```

The simulation confirms precise tax calculations by region:

:::{dropdown} Response

```json
{
  "docs": [
    {
      "doc": {
        ...,
        "_source": {
          "corrected_total_price": 47.22,
          "taxless_total_price": 44.98,
          "corrected_tax_amount": 2.24,
          "geoip": {
            "country_iso_code": "AE"
          },
          "tax_country_code": "AE"
        },
        "_ingest": {
          "timestamp": "2025-08-28T21:01:03.54255615Z"
        }
      }
    },
    {
      "doc": {
        ...,
        "_source": {
          "corrected_total_price": 227.4,
          "taxless_total_price": 189.5,
          "corrected_tax_amount": 37.9,
          "geoip": {
            "country_iso_code": "GB"
          },
          "tax_country_code": "GB"
        },
        "_ingest": {
          "timestamp": "2025-08-28T21:01:03.542605776Z"
        }
      }
    }
  ]
}
```

:::

## Convert calculated scores to boolean flags (runtime field context)

The goal is to create a dynamic “high value” flag by combining order price and product diversity into a weighted score. This makes it easy to identify valuable orders. In this example, type casting ensures accurate calculations when combining integer and double values. The score is rounded to an integer, then compared to create a boolean classification. 

### Understanding weighted scoring for boolean classification

Business analytics often requires combining multiple factors into a simple true/false classification. This weighted scoring model assigns different importance levels to various metrics. Order price carries 70% weight while product diversity carries 30%. The combined score is then rounded to create clear boolean categories.

### Writing the runtime field script

This script calculates a weighted score for each order by combining the total price and the number of unique products, applying explicit and implicit type casting where needed. The score is then rounded to an integer and converted into a boolean flag, indicating whether the order qualifies as “high value.”

Create a runtime field that calculates weighted scores and classifies them to boolean values:

```json
PUT kibana_sample_data_ecommerce/_mapping
{
  "runtime": {
    "is_high_value_order": {
      "type": "boolean",
      "script": {
        "lang": "painless",
        "source": """
          double price = doc['taxful_total_price'].value;
          long productsLong = doc['total_unique_products'].value;
          
          // Explicit casting: convert long to double for calculations
          double products = (double) productsLong;
          
          // Weighted score: 70% price weight + 30% product diversity weight
          // Implicit casting: integer literals (200 and 5) promote to double in division
          double priceWeight = (price / 200) * 0.7;
          double productWeight = (products / 5) * 0.3;
          double totalScore = priceWeight + productWeight;
          
          // Round to nearest integer: scores ≥0.5 become 1 (high value), <0.5 become 0 (regular)
          long rounded = Math.round(totalScore);
          boolean result = (rounded == 1);

          emit(result);
        """
      }
    }
  }
}
```

This script includes the following steps:

* **Explicit casting:** `(double) productsLong` converts long integer to double for mathematical operations  
* **Implicit casting:** Division operations automatically handle type promotion during arithmetic  
* **Weighted scoring:** Combines order price (70%) and product diversity (30%) to calculate order value  
* **Normalization:** Scales values using realistic maximums (price/200, products/5) for consistent scoring  
* **Boolean classification:** Uses `Math.round()` and comparison logic to create true/false flags for business classification


For more details about Painless scripting in runtime fields, refer to [Runtime field context](elasticsearch://reference/scripting-languages/painless/painless-runtime-fields-context.md).

### Test the runtime fields

Query the runtime field to see boolean conversion results:

```json
GET kibana_sample_data_ecommerce/_search
{
  "fields": [
    "is_high_value_order"
  ],
  "_source": {
    "includes": [
      "customer_id",
      "taxful_total_price",
      "total_unique_products"
    ]
  }
}
```

The results show how the calculated scores are classified into boolean values:

:::{dropdown} Response

```json
{
  "hits": {
    "hits": [
      {
        "_source": {
          "customer_id": 38,
          "taxful_total_price": 36.98,
          "total_unique_products": 2
        },
        "fields": {
          "is_high_value_order": [
            false
          ]
        }
      },
      {
        "_source": {
          "customer_id": 24,
          "taxful_total_price": 103.94,
          "total_unique_products": 4
        },
        "fields": {
          "is_high_value_order": [
            true
          ]
        }
      }
    ]
  }
}
```

:::

## Learn more about type casting in Painless

This tutorial showed you practical type conversion scenarios across ingest pipelines and runtime fields. To expand your Painless scripting:

* **Painless Casting Table:** See the full list of allowed type conversions, explicit and implicit [casting](elasticsearch://reference/scripting-languages/painless/painless-casting.md) rules, and examples for supported types in Painless.  
* **Apply to other contexts:** Use these casting techniques in update scripts, aggregations, and search queries. For context-specific data access patterns (`doc`, `ctx`, `_source`), refer to Painless syntax-context bridge.  
* **Explore advanced casting:** The [Painless language specification](elasticsearch://reference/scripting-languages/painless/painless-language-specification.md) covers explicit versus implicit casting rules, numeric precision handling, and reference type conversions.
