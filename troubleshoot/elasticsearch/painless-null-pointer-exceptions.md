---
navigation_title: Null pointer exceptions
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Troubleshoot null pointer exceptions in Painless

Follow these guidelines to avoid null pointer exceptions in your Painless scripts.

In Painless, field access methods vary depending on the script execution [context](elasticsearch://reference/scripting-languages/painless/painless-contexts.md). Using a field access pattern that is not valid for the current script context causes a `null_pointer_exception`.

## Sample error

```json
{
  "error": {
    "root_cause": [
      {
        "type": "script_exception",
        "reason": "runtime error",
        "script_stack": [
          "params['_source'].tags.size() > 2",
          "                 ^---- HERE"
        ],
        "script": "params['_source'].tags.size() > 2",
        "lang": "painless",
        "position": {
          "offset": 17,
          "start": 0,
          "end": 33
        }
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
        "node": "hupWdkj_RtmThGjNUiIt_w",
        "reason": {
          "type": "script_exception",
          "reason": "runtime error",
          "script_stack": [
            "params['_source'].tags.size() > 2",
            "                 ^---- HERE"
          ],
          "script": "params['_source'].tags.size() > 2",
          "lang": "painless",
          "position": {
            "offset": 17,
            "start": 0,
            "end": 33
          },
          "caused_by": {
            "type": "null_pointer_exception",
            "reason": "cannot access method/field [tags] from a null def reference"
          }
        }
      }
    ]
  },
  "status": 400
}á
```

### Problematic code

```json
{
  "query": {
    "bool": {
      "filter": {
        "script": {
          "script": {
            "source": "params['_source'].tags.size() > 2",
            "lang": "painless"
          }
        }
      }
    }
  }
}
```

### Sample data

```json
POST products/_doc
{
  "name": "Laptop",
  "price": 999.99,
  "category": "electronics",
  "tags": ["premium", "gaming", "portable"]
}
```

### Root cause

A common cause of null pointer exceptions in Painless scripts is attempting to access document fields using incorrect access patterns for the specific [script context](elasticsearch://reference/scripting-languages/painless/painless-contexts.md). To learn more about the context-dependent field access methods in Painless, refer to Painless syntax-context bridge in the Explore and Analyze documentation. 
% Link to come after E&A PR is merged.

The error occurs because `params['_source']` is not available in script filter contexts. In script filters, field values must be accessed through `doc` values, not through the `params['_source']` map.

### Solution: Use correct field access pattern for context

For script filter contexts, use `doc` values instead of `params._source`:

```json
GET products/_search
{
  "query": {
    "bool": {
      "filter": {
        "script": {
          "script": {
            "source": "doc['tags.keyword'].size() > 2",
            "lang": "painless"
          }
        }
      }
    }
  }
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
        ...,
        "_source": {
          "name": "Laptop",
          "price": 999.99,
          "category": "electronics",
          "tags": [
            "premium",
            "gaming",
            "portable"
          ]
        }
      }
    ]
  }
}
```

### Notes

* **Context matters:** Always verify the correct field access pattern for your script context.  
* **Context limitations:** Script filters cannot access `params['_source']` .  
* **Field mapping:** Use `.keyword` suffix for text fields when accessing via doc values.

