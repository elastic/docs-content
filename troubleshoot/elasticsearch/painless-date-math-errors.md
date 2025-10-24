---
navigation_title: Date math errors
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Troubleshoot date math errors in Painless

Follow these guidelines to avoid [date](elasticsearch://reference/scripting-languages/painless/using-datetime-in-painless.md) operation errors in your Painless script.

## Runtime mappings context

### Dynamic method not found error

When working with date fields in runtime mappings, accessing methods directly on the document field object can cause errors if the proper value accessor is not used.

### Error

```json
{
  "error": {
    "root_cause": [
      {
        "type": "script_exception",
        "reason": "runtime error",
        "script_stack": [
          """emit(orderDate.toInstant().toEpochMilli() + 14400000);
        """,
          "              ^---- HERE"
        ],
        "script": " ...",
        "lang": "painless",
        "position": {
          "offset": 75,
          "start": 61,
          "end": 124
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
        "index": "kibana_sample_data_ecommerce",
        "node": "CxMTEjvKSEC0k0aTr4OM3A",
        "reason": {
          "type": "script_exception",
          "reason": "runtime error",
          "script_stack": [
            """emit(orderDate.toInstant().toEpochMilli() + 14400000);
        """,
            "              ^---- HERE"
          ],
          "script": " ...",
          "lang": "painless",
          "position": {
            "offset": 75,
            "start": 61,
            "end": 124
          },
          "caused_by": {
            "type": "illegal_argument_exception",
            "reason": "dynamic method [org.elasticsearch.index.fielddata.ScriptDocValues.Dates, toInstant/0] not found"
          }
        }
      }
    ]
  },
  "status": 400
}
```

### Problematic code

```json
"script": {
  "lang": "painless",
  "source": """
    def orderDate = doc['order_date'];
    emit(orderDate.toInstant().toEpochMilli() + 14400000);
  """
}
```

### Root cause

The script attempts to call `toInstant()` directly on a `ScriptDocValues.Dates` object. Date fields in Painless require accessing the `.value` property to get the actual date value before calling date methods.

### Solution

Access the date value using `.value` before calling date methods:

```json
"script": {
  "lang": "painless",
  "source": """
    def orderDate = doc['order_date'].value; // added .value here
    emit(orderDate.toInstant().toEpochMilli() + 14400000);
  """
}
```

### Notes

* Always use `.value` when accessing single values from document fields in Painless.  
* Check for empty fields when the field might not exist in all documents.  
* Date arithmetic should be performed on the actual date value, not the field container object.
