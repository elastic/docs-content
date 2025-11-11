---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-custom-filter.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: apm
---

# Custom filters [apm-custom-filter]

Custom filters, including [ingest pipeline filters](#apm-filters-ingest-pipeline) and [APM agent filters](#apm-filters-in-agent), allow you to filter or redact APM data on ingestion.

## Ingest pipeline filters [apm-filters-ingest-pipeline]

```{applies_to}
stack: ga
serverless: unavailable
```

Ingest pipelines specify a series of processors that transform data in a specific way. Transformation happens prior to indexing—inflicting no performance overhead on the monitored application. Pipelines are a flexible and easy way to filter or obfuscate Elastic APM data.

Features of this approach:

* Filters are applied at ingestion time.
* All Elastic APM agents and fields are supported.
* Data leaves the instrumented service.
* There are no performance overhead implications on the instrumented service.

For a step-by-step example, refer to [Tutorial: Use an ingest pipeline to redact sensitive information](#apm-filters-ingest-pipeline-tutorial).

## APM agent filters [apm-filters-in-agent]

```{applies_to}
stack: ga
serverless: ga
```

Some APM agents offer a way to manipulate or drop APM events *before* they are sent to APM Server.

Features of this approach:

* Data is sanitized before leaving the instrumented service.
* Not supported by all Elastic APM agents.
* Potential overhead implications on the instrumented service.

Refer to the relevant agent’s documentation for more information and examples:

* .NET: [Filter API](apm-agent-dotnet://reference/public-api.md#filter-api).
* Node.js: [`addFilter()`](apm-agent-nodejs://reference/agent-api.md#apm-add-filter).
* Python: [custom processors](apm-agent-python://reference/sanitizing-data.md).
* Ruby: [`add_filter()`](apm-agent-ruby://reference/api-reference.md#api-agent-add-filter).

## Tutorial: Use an ingest pipeline to redact sensitive information [apm-filters-ingest-pipeline-tutorial]

```{applies_to}
stack: ga
serverless: unavailable
```

Say you decide to [capture HTTP request bodies](/solutions/observability/apm/built-in-data-filters.md#apm-filters-http-body) but quickly notice that sensitive information is being collected in the `http.request.body.original` field:

```json
{
  "email": "test@example.com",
  "password": "hunter2"
}
```

To obfuscate the passwords stored in the request body, you can use a series of [ingest processors](elasticsearch://reference/enrich-processor/index.md).

### Create a pipeline [_create_a_pipeline]

::::{tip}
This tutorial uses the [Ingest APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-ingest), but it’s also possible to create a pipeline using the UI. Open the **Ingest Pipelines** management page in the navigation menu or using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Create pipeline** → **New pipeline**.
::::

To start, create a pipeline with a simple description and an empty array of processors:

```json
{
  "pipeline": {
    "description": "redact http.request.body.original.password",
    "processors": [] <1>
  }
}
```

1. The processors defined below will go in this array

#### Add a JSON processor [_add_a_json_processor]

Add your first processor to the processors array. Because the agent captures the request body as a string, use the [JSON processor](elasticsearch://reference/enrich-processor/json-processor.md) to convert the original field value into a structured JSON object. Save this JSON object in a new field:

```json
{
  "json": {
    "field": "http.request.body.original",
    "target_field": "http.request.body.original_json",
    "ignore_failure": true
  }
}
```

#### Add a set processor [_add_a_set_processor]

If `body.original_json` is not `null`, i.e., it exists, we’ll redact the `password` with the [set processor](elasticsearch://reference/enrich-processor/set-processor.md), by setting the value of `body.original_json.password` to `"redacted"`:

```json
{
  "set": {
    "field": "http.request.body.original_json.password",
    "value": "redacted",
    "if": "ctx?.http?.request?.body?.original_json != null"
  }
}
```

#### Add a convert processor [_add_a_convert_processor]

Use the [convert processor](elasticsearch://reference/enrich-processor/convert-processor.md) to convert the JSON value of `body.original_json` to a string and set it as the `body.original` value:

```json
{
  "convert": {
    "field": "http.request.body.original_json",
    "target_field": "http.request.body.original",
    "type": "string",
    "if": "ctx?.http?.request?.body?.original_json != null",
    "ignore_failure": true
  }
}
```

#### Add a remove processor [_add_a_remove_processor]

Finally, use the [remove processor](elasticsearch://reference/enrich-processor/remove-processor.md) to remove the `body.original_json` field:

```json
{
  "remove": {
    "field": "http.request.body.original_json",
    "if": "ctx?.http?.request?.body?.original_json != null",
    "ignore_failure": true
  }
}
```

#### Register the pipeline [_register_the_pipeline]

Then put it all together, and use the [create or update pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline) to register the new pipeline in {{es}}. Name the pipeline `apm_redacted_body_password`:

```console
PUT _ingest/pipeline/apm_redacted_body_password
{
  "description": "redact http.request.body.original.password",
  "processors": [
    {
      "json": {
        "field": "http.request.body.original",
        "target_field": "http.request.body.original_json",
        "ignore_failure": true
      }
    },
    {
      "set": {
        "field": "http.request.body.original_json.password",
        "value": "redacted",
        "if": "ctx?.http?.request?.body?.original_json != null"
      }
    },
    {
      "convert": {
        "field": "http.request.body.original_json",
        "target_field": "http.request.body.original",
        "type": "string",
        "if": "ctx?.http?.request?.body?.original_json != null",
        "ignore_failure": true
      }
    },
    {
      "remove": {
        "field": "http.request.body.original_json",
        "if": "ctx?.http?.request?.body?.original_json != null",
        "ignore_failure": true
      }
    }
  ]
}
```

### Test the pipeline [_test_the_pipeline]

Prior to enabling this new pipeline, you can test it with the [simulate pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-simulate). This API allows you to run multiple documents through a pipeline to ensure it is working correctly.

The request below simulates running three different documents through the pipeline:

```console
POST _ingest/pipeline/apm_redacted_body_password/_simulate
{
  "docs": [
    {
      "_source": { <1>
        "http": {
          "request": {
            "body": {
              "original": """{"email": "test@example.com", "password": "hunter2"}"""
            }
          }
        }
      }
    },
    {
      "_source": { <2>
        "some-other-field": true
      }
    },
    {
      "_source": { <3>
        "http": {
          "request": {
            "body": {
              "original": """["invalid json" """
            }
          }
        }
      }
    }
  ]
}
```

1. This document features the same sensitive data from the original example above
2. This document only contains an unrelated field
3. This document contains invalid JSON

The API response should be similar to this:

```json
{
  "docs" : [
    {
      "doc" : {
        "_source" : {
          "http" : {
            "request" : {
              "body" : {
                "original" : {
                  "password" : "redacted",
                  "email" : "test@example.com"
                }
              }
            }
          }
        }
      }
    },
    {
      "doc" : {
        "_source" : {
          "nobody" : true
        }
      }
    },
    {
      "doc" : {
        "_source" : {
          "http" : {
            "request" : {
              "body" : {
                "original" : """["invalid json" """
              }
            }
          }
        }
      }
    }
  ]
}
```

As expected, only the first simulated document has a redacted password field. All other documents are unaffected.

### Create a `@custom` pipeline [_create_a_custom_pipeline]

The final step in this process is to call the newly created `apm_redacted_body_password` pipeline from the `@custom` pipeline of the data stream you wish to edit.

`@custom` pipelines are specific to each data stream and follow a similar naming convention: `<type>-<dataset>@custom`. As a reminder, the default APM data streams are:

* Application traces: `traces-apm-<namespace>`
* RUM and iOS agent application traces: `traces-apm.rum-<namespace>`
* APM internal metrics: `metrics-apm.internal-<namespace>`
* APM transaction metrics: `metrics-apm.transaction.<metricset.interval>-<namespace>`
* APM service destination metrics: `metrics-apm.service_destination.<metricset.interval>-<namespace>`
* APM service transaction metrics: `metrics-apm.service_transaction.<metricset.interval>-<namespace>`
* APM service summary metrics: `metrics-apm.service_summary.<metricset.interval>-<namespace>`
* Application metrics: `metrics-apm.app.<service.name>-<namespace>`
* APM error/exception logging: `logs-apm.error-<namespace>`
* Applications UI logging: `logs-apm.app.<service.name>-<namespace>`

To match a custom ingest pipeline with a data stream, follow the `<type>-<dataset>@custom` template, or replace `-namespace` with `@custom` in the table above. For example, to target application traces, you’d create a pipeline named `traces-apm@custom`.

Use the [create or update pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline) to register the new pipeline in {{es}}. Name the pipeline `traces-apm@custom`:

```console
PUT _ingest/pipeline/traces-apm@custom
{
  "processors": [
    {
      "pipeline": {
        "name": "apm_redacted_body_password" <1>
      }
    }
  ]
}
```

1. The name of the pipeline we previously created

That’s it! Passwords will now be redacted from your APM HTTP body data.

### Next steps [_next_steps]

To learn more about ingest pipelines, see [View the {{es}} index template](/solutions/observability/apm/view-elasticsearch-index-template.md).

