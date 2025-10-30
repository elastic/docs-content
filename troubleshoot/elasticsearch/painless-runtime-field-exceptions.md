---
navigation_title: Runtime field exceptions
applies_to:
  stack: ga
  serverless: ga
products:
  - id: elasticsearch
---

# Troubleshoot runtime field exceptions in Painless

Follow these guidelines to avoid [runtime field](elasticsearch://reference/scripting-languages/painless/painless-runtime-fields-context.md) exceptions in your Painless scripts.

## Using `return` instead of `emit` in runtime field in runtime mappings

When you create runtime mappings in a Painless script, using `return` instead of `emit` to output values leads to compilation errors, as runtime field scripts require the `emit()` function to produce field values.

## Sample error

```json
{
  "error": {
    "root_cause": [
      {
        "type": "class_cast_exception",
        "reason": "class_cast_exception: Cannot cast from [java.lang.String] to [void]."
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "users",
        "node": "hupWdkj_RtmThGjNUiIt_w",
        "reason": {
          "type": "script_exception",
          "reason": "compile error",
          "script_stack": [
            """... Doe";
	
          return firstName + " " + lastNam ...""",
            "                             ^---- HERE"
          ],
          "script": """
          String firstName = "John";
          String lastName = "Doe";
	
          return firstName + " " + lastName;
        """,
          "lang": "painless",
          "position": {
            "offset": 92,
            "start": 67,
            "end": 117
          },
          "caused_by": {
            "type": "class_cast_exception",
            "reason": "class_cast_exception: Cannot cast from [java.lang.String] to [void]."
          }
        }
      }
    ],
    "caused_by": {
      "type": "class_cast_exception",
      "reason": "class_cast_exception: Cannot cast from [java.lang.String] to [void]."
    }
  },
  "status": 400
}
```

## Problematic code

```json
{
 "runtime_mappings": {
    "full_name": {
      "type": "keyword",
      "script": {
        "source": """
          String firstName = "John";
          String lastName = "Doe";
	
          return firstName + " " + lastName;
        """
      }
    }
  }
}
```

## Root cause

Runtime field scripts use `emit()` to produce values, rather than `return`. The `emit()` function is specifically designed for runtime mappings to output field values, while `return` is used in other Painless contexts such as script queries or update scripts. The error occurs because runtime field scripts expect a void return type, but the script attempts to return a String value. 

## Solution: Replace return with emit

Replace `return` statements with `emit()` calls:

```json
POST users/_search
{
  "fields": [
    {
      "field": "*",
      "include_unmapped": "true"
    }
  ],
  "runtime_mappings": {
    "full_name": {
      "type": "keyword",
      "script": {
        "source": """
          String firstName = "John";
          String lastName = "Doe";

          emit(firstName + " " + lastName);
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
        ...,
        "_source": {
          "user": {
            "name": "Jane Doe"
          }
        },
        "fields": {
          "user.name.keyword": [
            "Jane Doe"
          ],
          "user_info": [
            "incomplete: Jane Doe"
          ],
          "user.name": [
            "Jane Doe"
          ]
        }
      }
    ]
  }
}
```

## Notes

* Runtime field scripts must use `emit()` to output values, not `return`.  
* `emit()` can be called multiple times in a script to emit multiple values.
