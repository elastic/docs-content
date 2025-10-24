---
navigation_title: Script score calculation errors
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Troubleshoot script score calculation errors in Painless

Follow these guidelines to avoid scoring calculation errors in your Painless script.

## script\_score script returned an invalid score

When using [`script_score`](elasticsearch://reference/query-languages/query-dsl/query-dsl-script-score-query.md) with type `double`,
 it can return unexpected null values, negative values `0.0` or Infinity, causing documents to receive a score of `0` or be excluded from results entirely. This commonly occurs when field access patterns don't account for missing values or when mathematical operations result in null propagation.

### Sample error

```json
{
  "error": {
    "root_cause": [
      {
        "type": "illegal_argument_exception",
        "reason": "script_score script returned an invalid score [-Infinity] for doc [0]. Must be a non-negative score!"
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
          "type": "illegal_argument_exception",
          "reason": "script_score script returned an invalid score [-Infinity] for doc [0]. Must be a non-negative score!"
        }
      }
    ],
    "caused_by": {
      "type": "illegal_argument_exception",
      "reason": "script_score script returned an invalid score [-Infinity] for doc [0]. Must be a non-negative score!",
      "caused_by": {
        "type": "illegal_argument_exception",
        "reason": "script_score script returned an invalid score [-Infinity] for doc [0]. Must be a non-negative score!"
      }
    }
  },
  "status": 400
}
```

### Problematic code

```json
{
  "query": {
    "script_score": {
      "query": {
        "match_all": {}
      },
      "script": {
        "lang": "painless",
        "source": """
          double price = 0.0;  // Simulating problematic calculation
          double rating = 5.0;

          return Math.log(price) * rating;
        """
      }
    }
  }
}
```

### Root cause

The error occurs because of mathematical edge cases in calculations:

1. **Math.log() with zero or negative values:** `Math.log(0)` returns negative infinity, `Math.log(-x)` returns `NaN`.  
2. **Division by zero:** Operations like `x/0` throw an arithmetic\_exception.  
3. **NaN propagation:** Any mathematical operation involving `NaN` results in `NaN`.  
4. **Infinity calculations:** Operations with infinity often result in `NaN` or unexpected values.

When a script returns `NaN`, negative infinity, or other invalid numbers, Painless converts the score to 0.0, causing unexpected ranking behavior.

### Solution: Add mathematical safety checks

Always validate mathematical inputs and handle edge cases:

```json
GET products/_search
{
  "query": {
    "script_score": {
      "query": {
        "match_all": {}
      },
      "script": {
        "lang": "painless",
        "source": """
          double price = 0.0;
          double rating = 5.0;
          
          double safePrice = Math.max(price, 1.0);  // Ensure > 0 for log
          
          // Calculate score with safety checks
          double logPrice = Math.log(safePrice);
          double score = logPrice * rating;
          
          // Handle NaN or infinity results
          if (Double.isNaN(score) || Double.isInfinite(score)) {
            return 1.0;
          }
          
          return Math.max(score, 0.1);  // Ensure minimum positive score
        """
      }
    }
  }
}
```

### Sample documents

```json
POST products/_doc
{
  "name": "Premium Laptop",
  "price": 999.99,
  "rating": 4.7,
  "category": "electronics"
}

POST products/_doc
{
  "name": "Free Software",
  "price": 0,
  "rating": 5.0,
  "category": "software"
}
```

### Results

```json
{
  ...,
  "hits": {
    ...,
    "hits": [
      {
        "_index": "products",
        "_id": "j6gZNZkB0eMypkDYmmSC",
        "_score": 0.1,
        "_source": {
          "name": "Premium Laptop",
          "price": 999.99,
          "rating": 4.7,
          "category": "electronics"
        }
      },
      {
        "_index": "products",
        "_id": "kKgZNZkB0eMypkDYn2SP",
        "_score": 0.1,
        "_source": {
          "name": "Free Software",
          "price": 0,
          "rating": 5,
          "category": "software"
        }
      }
    ]
  }
}
```

### Notes

* **Mathematical safety:** Validate inputs for functions like `Math.log()`.  
* **Default values:** Provide meaningful defaults for missing fields to maintain consistent scoring.  
* **Minimum scores:** Ensure scripts return positive values to avoid zero scores.  
* **Null handling:** Mathematical operations with null values propagate null throughout the calculation.

