---
navigation_title: Array/list manipulation errors
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Troubleshoot array manipulation errors in Painless

Follow these guidelines to avoid array (list) access errors in your Painless scripts.

An array `index_out_of_bounds_exception` occurs when a script tries to access an element at a position that does not exist in the array. For example, if an array has two elements, trying to access a third element triggers this exception. 

## Sample error

```json
{
  "error": {
    "root_cause": [
      {
        "type": "index_out_of_bounds_exception",
        "reason": "index_out_of_bounds_exception: Index 2 out of bounds for length 2"
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "blog_posts",
        "node": "hupWdkj_RtmThGjNUiIt_w",
        "reason": {
          "type": "script_exception",
          "reason": "runtime error",
          "script_stack": [
            "java.base/jdk.internal.util.Preconditions.outOfBounds(Preconditions.java:100)",
            "java.base/jdk.internal.util.Preconditions.outOfBoundsCheckIndex(Preconditions.java:106)",
            "java.base/jdk.internal.util.Preconditions.checkIndex(Preconditions.java:302)",
            "java.base/java.util.Objects.checkIndex(Objects.java:365)",
            "java.base/java.util.ArrayList.get(ArrayList.java:428)",
            """return keywords[2].toUpperCase();
          """,
            "               ^---- HERE"
          ],
          "script": " ...",
          "lang": "painless",
          "position": {
            "offset": 76,
            "start": 61,
            "end": 105
          },
          "caused_by": {
            "type": "index_out_of_bounds_exception",
            "reason": "index_out_of_bounds_exception: Index 2 out of bounds for length 2"
          }
        }
      }
    ],
    "caused_by": {
      "type": "index_out_of_bounds_exception",
      "reason": "index_out_of_bounds_exception: Index 2 out of bounds for length 2"
    }
  },
  "status": 400
}
```

## Problematic code

```json
{
  "aggs": {
    "third_tag_stats": {
      "terms": {
        "script": {
          "source": """
            def keywords = params._source.tags;

            return keywords[2].toUpperCase();
          """,
          "lang": "painless"
        }
      }
    }
  }
}
```

## Root cause

The error occurs because the script tries to access index 2 (the third element) in an array that only has two elements (indices 0, 1). Arrays in Painless are zero-indexed, so accessing an index greater than or equal to the array size causes an exception.

## Solution: Check array bounds before accessing

Always verify the size of an array before accessing specific indices:

```json
GET blog_posts/_search
{
  "size": 0,
  "aggs": {
    "third_tag_stats": {
      "terms": {
        "script": {
          "source": """
            def keywords = params._source.tags;

            if (keywords.size() > 2) {
              return keywords[2].toUpperCase();
            } else {
              return "NO_THIRD_TAG";
            }
          """,
          "lang": "painless"
        }
      }
    }
  }
}
```

## Sample document

```json
POST blog_posts/_doc
{
  "title": "Getting Started with Elasticsearch",
  "content": "Learn the basics...",
  "tags": ["elasticsearch", "tutorial"]
}
```

## Results

```json
{
  ...,
  "hits": {
    ...
  },
  "aggregations": {
    "third_tag_stats": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "NO_THIRD_TAG",
          "doc_count": 1
        }
      ]
    }
  }
}
```

## Notes

* **Array bounds:** Always check the size of an array before accessing specific indices.  
* **Zero-indexed:** Remember that arrays start at index 0, so `size() - 1` is the last valid index.  
* **Empty arrays:** Handle cases where arrays might be completely empty (`size() == 0`).
