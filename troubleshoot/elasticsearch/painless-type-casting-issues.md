---
navigation_title: Type casting issues
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Troubleshoot type casting issues in Painless

Follow these guidelines to avoid type conversion errors in your Painless scripts.

When you perform [type casting](elasticsearch://reference/scripting-languages/painless/painless-casting.md) in Painless scripts, attempting implicit conversions or casting incompatible types without proper validation leads to compilation and runtime errors.

## Sample error

```json
{
  "error": {
    "root_cause": [
      {
        "type": "class_cast_exception",
        "reason": "class_cast_exception: Cannot cast from [double] to [int]."
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "products",
        "node": "CxMTEjvKSEC0k0aTr4OM3A",
        "reason": {
          "type": "script_exception",
          "reason": "compile error",
          "script_stack": [
            "...    int discountedPrice = price * discount;  // Err ...",
            "                             ^---- HERE"
          ],
          "script": """
          double price = doc['price'].value;
          double discount = 0.85;
          int discountedPrice = price * discount;  // Error: implicit cast
          emit(discountedPrice);
        """,
          "lang": "painless",
          "position": {
            "offset": 112,
            "start": 87,
            "end": 137
          },
          "caused_by": {
            "type": "class_cast_exception",
            "reason": "class_cast_exception: Cannot cast from [double] to [int]."
          }
        }
      }
    ],
    "caused_by": {
      "type": "class_cast_exception",
      "reason": "class_cast_exception: Cannot cast from [double] to [int]."
    }
  },
  "status": 400
}
```

## Problematic code

```json
{
  "runtime_mappings": {
    "discounted_price": {
      "type": "long",
      "script": {
        "source": """
          double price = doc['price'].value;
          double discount = 0.85;
          int discountedPrice = price * discount;  // Error: implicit cast
          emit(discountedPrice);
        """
      }
    }
  }
}
```

## Sample data

```json
PUT products/_doc/1
{
  "name": "Laptop",
  "price": 999.99
}

PUT products/_doc/2
{
  "name": "Mouse", 
  "price": 25
}
```

## Root cause

Painless has [specific rules](https://www.elastic.co/docs/reference/scripting-languages/painless/painless-casting) for implicit and explicit type casting between numeric types. While some numeric conversions are allowed implicitly (widening conversions such as `int` into `double`), narrowing conversions such as `double` to `int` require explicit casting. The script attempts to assign a `double` result to an `int` variable without explicit casting, which causes a compilation error since this is a narrowing conversion that could lose precision. Additionally, field values may be null or of unexpected types, requiring proper validation before casting.

## Solution: Use explicit numeric type casting

Use explicit casting with proper validation:

```json
POST products/_search
{
  "fields": [
    {
      "field": "*",
      "include_unmapped": "true"
    }
  ],
  "runtime_mappings": {
    "discounted_price": {
      "type": "long",
      "script": {
        "source": """
          if (doc['price'].size() > 0) {
            def value = doc['price'].value;
            
            if (value != null && value instanceof Number) {
              double price = (double) value;
              double discount = 0.85;
              long discountedPrice = (long)(price * discount);
              emit(discountedPrice);
            } else {
              emit(0L);
            }
          } else {
            emit(0L);
          }
        """
      }
    }
  }
}
```

## Results

```json
{
  ...,
  "hits": {
    ...,
    "hits": [
      {
        "_index": "products",
        "_id": "1",
        "_score": 1,
        "_source": {
          "name": "Laptop",
          "price": 999.99
        },
        "fields": {
          "name": [
            "Laptop"
          ],
          "name.keyword": [
            "Laptop"
          ],
          "price": [
            999.99
          ],
          "discounted_price": [
            849
          ]
        }
      },
      {
        "_index": "products",
        "_id": "2",
        "_score": 1,
        "_source": {
          "name": "Mouse",
          "price": 25
        },
        "fields": {
          "name": [
            "Mouse"
          ],
          "name.keyword": [
            "Mouse"
          ],
          "price": [
            25
          ],
          "discounted_price": [
            21
          ]
        }
      }
    ]
  }
}
```

## Notes

* Validate the existence of a field using `.size() > 0` before accessing values.  
* Check for null values using `value != null` before casting.  
* Use `instanceof Number` to verify the value is numeric before casting.  
* Handle missing fields gracefully with default values.  
* When working with {{es}} field values, always validate the actual field type.
