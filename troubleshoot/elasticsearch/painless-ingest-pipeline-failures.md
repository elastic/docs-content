---
navigation_title: Ingest pipeline failures
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Troubleshoot ingest pipeline failures in Painless

Follow these guidelines to avoid [ingest pipeline](elasticsearch://reference/scripting-languages/painless/painless-ingest-processor-context.md) script errors in your Painless script.

## Date conversion

### Class cast exception when converting date data types

When converting time strings to nanoseconds in ingest pipelines, attempting to perform arithmetic operations directly on string values without proper date parsing leads to type casting errors. 

### Sample error

```json
{
  "docs": [
    {
      "error": {
        "root_cause": [
          {
            "type": "script_exception",
            "reason": "runtime error",
            "script_stack": [
              "ctx.nanoseconds = ctx.time_field * 1000000;",
              "                     ^---- HERE"
            ],
            "script": " ...",
            "lang": "painless",
            "position": {
              "offset": 32,
              "start": 11,
              "end": 63
            }
          }
        ],
        "type": "script_exception",
        "reason": "runtime error",
        "script_stack": [
          "ctx.nanoseconds = ctx.time_field * 1000000;",
          "                     ^---- HERE"
        ],
        "script": " ...",
        "lang": "painless",
        "position": {
          "offset": 32,
          "start": 11,
          "end": 63
        },
        "caused_by": {
          "type": "class_cast_exception",
          "reason": "Cannot apply [*] operation to types [java.lang.String] and [java.lang.Integer]."
        }
      }
    }
  ]
}
```

### Problematic code

```json
{
  "script": {
    "source": """
      ctx.nanoseconds = ctx.time_field * 1000000;
    """
  }
}
```

### Root cause

When accessing fields via `ctx.time_field` in ingest pipelines, the values are not automatically parsed to their mapped field types. The script attempts to multiply a string value (time field) directly with an integer. Time strings like `"00:00:00.022"` remain as strings and need to be properly parsed as dates and converted to epoch milliseconds before performing arithmetic operations.

### Solution: Use `SimpleDateFormat` in the script processor

Parse the time string directly using SimpleDateFormat and get epoch milliseconds:

```json
POST _ingest/pipeline/_simulate
{
  "pipeline": {
    "description": "Parse time and convert to nanoseconds",
    "processors": [
      {
        "script": {
          "source": """
            SimpleDateFormat sdf = new SimpleDateFormat("HH:mm:ss.SSS");
            long millis = sdf.parse(ctx.time_field).getTime();
            ctx.timestamp_nanos = millis * 1000000L;
          """
        }
      }
    ]
  },
  "docs": [
    {
      "_index": "index",
      "_id": "id",
      "_source": {
        "time_field": "00:00:00.022"
      }
    }
  ]
}
```

### Result

```json
{
  "docs": [
    {
      "doc": {
        "_index": "index",
        "_version": "-3",
        "_id": "id",
        "_source": {
          "time_field": "00:00:00.022",
          "timestamp_nanos": 22000000
        },
        "_ingest": {
          "timestamp": "2025-09-02T17:40:42.175772728Z"
        }
      }
    }
  ]
}
```

### Note

* Time strings like `"HH:mm:ss.SSS"` must be explicitly parsed before arithmetic operations.  
* Using `SimpleDateFormat` in a script processor allows custom parsing.
