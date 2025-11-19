---
applies_to:
  stack: ga
  serverless: ga
---

# Error handling

Ingest pipelines in Elasticsearch are powerful tools for transforming and enriching data before indexing. However, errors can occur during processing. This guide outlines strategies for handling such errors effectively.

:::{important}
Ingest pipelines are executed before the document is indexed by Elasticsearch. You can handle the errors occurring while processing the document (that is, transforming the json object) but not the errors triggered while indexing like mapping conflict. For this is the Elasticsearch Failure Store.
:::

Errors in ingest pipelines typically fall into the following categories:

- Parsing Errors: Occur when a processor fails to parse a field, such as a date or number.
- Missing Fields: Happen when a required field is absent in the document.

:::{tip}
Create an `error-handling-pipeline` that sets `event.kind` to `pipeline_error` and stores the error message, along with the tag from the failed processor, in the `error.message` field. Including a tag is especially helpful when using multiple `grok`, `dissect`, or `script` processors, as it helps identify which one caused the failure.
:::

The `on_failure` parameter can be defined either for individual processors or at the pipeline level to catch exceptions that may occur during document processing. The `ignore_failure` option allows a specific processor to silently skip errors without affecting the rest of the pipeline.

## Global versus processor-specific

The following example demonstrates how to use the `on_failure` handler at the pipeline level rather than within individual processors. While this approach ensures the pipeline exits gracefully on failure, it also means that processing stops at the point of error.

In this example, a typo was made in the configuration of the `dissect` processor intended to extract `user.name` from the message. A comma (`,`) was used instead of the correct colon (`:`).

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "@timestamp": "2025-04-03T10:00:00.000Z",
        "message": "user: philipp has logged in"
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "dissect": {
          "field": "message",
          "pattern": "%{}, %{user.name} %{}",
          "tag": "dissect for user.name"
        }
      },
      {
        "append": {
          "field": "event.category",
          "value": "authentication"
        }
      }
    ],
    "on_failure": [
      {
        "set": {
          "field": "event.kind",
          "value": "pipeline_error"
        }
      },
      {
        "append": {
          "field": "error.message",
          "value": "Processor {{ _ingest.on_failure_processor_type }} with tag {{ _ingest.on_failure_processor_tag }} in pipeline {{ _ingest.on_failure_pipeline }} failed with message: {{ _ingest.on_failure_message }}"
        }
      }
    ]
  }
}
```

The second processor, which sets `event.category` to `authentication`, is no longer executed because the first `dissect` processor fails and triggers the global `on_failure` handler. The resulting document shows which processor caused the error, the pattern it attempted to apply, and the input it received.

```json
"@timestamp": "2025-04-03T10:00:00.000Z",
"message": "user: philipp has logged in",
"event": {
    "kind": "pipeline_error"
},
"error": {
  "message": "Processor dissect with tag dissect for user.name in pipeline _simulate_pipeline failed with message: Unable to find match for dissect pattern: %{}, %{user.name} %{} against source: user: philipp has logged in"
}
```

We can restructure the pipeline by moving the `on_failure` handling directly into the processor itself. This allows the pipeline to continue execution. In this case, the `event.category` processor still runs. You can also retain the global `on_failure` to handle errors from other processors, while adding processor-specific error handling where needed.

:::{note}
While executing two `set` processors within the `dissect` error handler may not always be ideal, it serves as a demonstration.
:::

For the `dissect` processor, consider setting a temporary field like `_tmp.error: dissect_failure`. You can then use `if` conditions in later processors to execute them only if parsing failed, allowing for more controlled and flexible error handling.

```json
POST _ingest/pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "@timestamp": "2025-04-03T10:00:00.000Z",
        "message": "user: philipp has logged in"
      }
    }
  ],
  "pipeline": {
    "processors": [
      {
        "dissect": {
          "field": "message",
          "pattern": "%{}, %{user.name} %{}",
          "on_failure": [
            {
              "set": {
                "field": "event.kind",
                "value": "pipeline_error"
              }
            },
            {
              "append": {
                "field": "error.message",
                "value": "Processor {{ _ingest.on_failure_processor_type }} with tag {{ _ingest.on_failure_processor_tag }} in pipeline {{ _ingest.on_failure_pipeline }} failed with message: {{ _ingest.on_failure_message }}"
              }
            }
          ],
          "tag": "dissect for user.name"
        }
      },
      {
        "append": {
          "field": "event.category",
          "value": "authentication"
        }
      }
    ],
    "on_failure": [
      {
        "set": {
          "field": "event.kind",
          "value": "pipeline_error"
        }
      },
      {
        "set": {
          "field": "error.message",
          "value": "Processor {{ _ingest.on_failure_processor_type }} with tag {{ _ingest.on_failure_processor_tag }} in pipeline {{ _ingest.on_failure_pipeline }} failed with message: {{ _ingest.on_failure_message }}"
        }
      }
    ]
  }
}
```
