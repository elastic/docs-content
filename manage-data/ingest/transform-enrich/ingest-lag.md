---
applies_to:
  stack: ga
  serverless: ga
---

# Calculate the ingest lag metadata

Ingest lag is the time it takes from when a document is read to when it is received by {{es}}. Store this value in minutes, seconds, or milliseconds, and use it to create visualizations and alerts.

The basic calculation is:

`event.ingested - @timestamp`

## Understanding `event.ingested`

You can obtain `event.ingested` timestamp in two ways:

- `_ingest.timestamp`  
  Available through the mustache notation `{{_ingest.timestamp}}` in all processors except `script`.

- `metadata().now`
  Available only in the `script` processor. Use this instead of `_ingest.timestamp` when working with scripts.

::::{note}
The `event.ingested` option is typically set in the Fleet final pipeline, which runs as the last step in the ingest process. Calculating the latency in seconds is sufficient for most use cases.
::::

## Calculating ingestion latency

The following script is the core of the solution. It creates a new field, `event.ingestion.latency`, which you can use to monitor ingestion performance across your pipelines.

```json
{
  "script": {
    "description": "Calculates entire ingestion flow latency",
    "if": "ctx['@timestamp'] != null",
    "source": """
      ZonedDateTime start = ZonedDateTime.parse(ctx['@timestamp']);
      ctx.putIfAbsent("event", [:]);
      ctx.event.putIfAbsent("ingestion", [:]);
      ctx.event.ingestion.latency= ChronoUnit.SECONDS.between(start, metadata().now);
    """
  }
}
```

## @timestamp

The value of `@timestamp` can vary depending on the data source. It might represent the time the Elastic Agent read the document, or it might be the actual timestamp extracted from the document itself after parsing.

This distinction affects how ingest lag is calculated. For example, when Elastic Agent reads Windows Event Logs, it sets `@timestamp` based on the log's original timestamp. However, this behavior does not apply to all sources, such as syslog messages or Linux log files, where `@timestamp` is often set later in the pipeline, after parsing.

This inconsistency can lead to inaccurate latency measurements if not accounted for.

```json
POST _ingest/pipeline/_simulate
{
    "docs": [{
        "_source": {
            "@timestamp": "2025-04-03T10:00:00.000Z",
            "message": "2025-03-01T09:00:00.000Z user: philipp has logged in"
        }
    }],
    "pipeline": {
        "processors": [
          {"script": {
            "if": "ctx['@timestamp'] != null",
            "source": """
              ZonedDateTime start = ZonedDateTime.parse(ctx['@timestamp']);
              ctx.latency= ChronoUnit.SECONDS.between(start, metadata().now);
            """
          }}
        ]
    }
}
```

In the previous example, the read timestamp was `3rd April at 10:00`, while the actual log message on storage is from `3rd March`. If you calculate the difference at the first step, before any parsing, the result will be accurate. However, if you calculate as the final step in the pipeline, which is typically the case with Elastic Integrations that use `@custom` pipelines, the timestamp of `2025-03-01` will be used as `@timestamp`, leading to an erroneous latency calculation.

For many use cases, simply using `@timestamp` is sufficient, as we expect the Elastic Agent to pick up logs as quickly as possible. During the initial onboarding of new data sources, there might be higher latency due to the ingestion of historical or older data.

## The importance of `event.created`

As discussed above `@timestamp` is set to the timestamp from within the collected log. Whenever we need to calculate a true value, it can be off, because it can take Elastic Agent seconds, minutes, hours, days, ... to pick up something. Imagine you onboard an old server for the first time, your latency will shoot through the roof, since you might collect year old data. `event.created` is not automatically added to any log in Elastic Agent. For that you need to add the following processor to the advanced settings within an integration.

```yaml
- script:
    lang: javascript
    source: >
      function process(event) {
          event.Put("event.created", Date.now());
      }
```

## Architectures

Regardless of the chosen architecture, add a `remove` processor at the end of the pipeline to drop the `_tmp` field. The raw timestamps from the various processing steps are not needed, as the latency in seconds should be sufficient. For additional pipeline architectures, refer to [Ingest architectures](../ingest-reference-architectures.md).

### Elastic Agent to Elasticsearch

Use `@timestamp` and `event.ingested` to calculate the difference. This will give you the following document. The `event.ingestion.latency` is in seconds.

```json
{
  "event": {
    "ingestion": {
      "latency": 443394
    }
  }
}
```

This script contains the processors needed for an ingest pipeline to calculate the ingest lag.

```json
POST _ingest/pipeline/_simulate
{
    "docs": [{
        "_source": {
            "@timestamp": "2025-04-03T10:00:00.000Z",
            "message": "user: philipp has logged in",
            "_tmp": {
              "logstash": "2025-04-03T10:00:02.456Z"
            }

        }
    }],
    "pipeline": {
        "processors": [
          {
            "script": {
              "description": "Calculates entire ingestion flow latency",
              "if": "ctx['@timestamp'] != null",
              "source": """
                ZonedDateTime start = ZonedDateTime.parse(ctx['@timestamp']);
                ctx.putIfAbsent("event", [:]);
                ctx.event.putIfAbsent("ingestion", [:]);
                ctx.event.ingestion.latency= ChronoUnit.SECONDS.between(start, metadata().now);
              """
            }
          }
        ]
    }
}
```
### Logstash

When Logstash is added to the architecture we must add a timestamp, this can only be done by using Ruby and the simplest form is this:

```
ruby {
  code => "event.set('[_tmp][logstash_seen]', Time.now());"
}
```

### Elastic Agent => Logstash => Elasticsearch

Elastic Agent populates the `@timestamp` field, but Logstash doesn't add any timestamp by default. Add a temporary timestamp, for example by setting `_tmp.logstash_seen`. With this, you can calculate the following latency values:

- Total latency: (`@timestamp - event.ingested`)
- Elastic Agent to Logstash: (`@timestamp - _tmp.logstash_seen`)
- Logstash to Elasticsearch: (`_tmp.logstash_seen - event.ingested`)

These values can be especially helpful for debugging, as they allow you to quickly determine where the lag is introduced, and whether the delay is caused by the transfer from Elastic Agent to Logstash or from Logstash to Elasticsearch.

This script calculates these differences, providing latency values for each of the stages previously mentioned.

```json
{
  "event": {
    "ingestion": {
      "latency_logstash_to_elasticsearch": 443091,
      "latency": 443093,
      "latency_elastic_agent_to_logstash": 1
    }
  }
}
```

This script contains the processors needed for an ingest pipeline to calculate the ingest lag. If you want to remove the first calculation, ensure that the object `event.ingestion` is available.

```json
POST _ingest/pipeline/_simulate
{
    "docs": [{
        "_source": {
            "@timestamp": "2025-04-03T10:00:00.000Z",
            "message": "user: philipp has logged in",
            "_tmp": {
              "logstash": "2025-04-03T10:00:02.456Z"
            }

        }
    }],
    "pipeline": {
        "processors": [
          {
            "script": {
              "description": "Calculates entire ingestion flow latency",
              "if": "ctx['@timestamp'] != null",
              "source": """
                ZonedDateTime start = ZonedDateTime.parse(ctx['@timestamp']);
                ctx.putIfAbsent("event", [:]);
                ctx.event.putIfAbsent("ingestion", [:]);
                ctx.event.ingestion.latency= ChronoUnit.SECONDS.between(start, metadata().now);
              """
            }
          },
          {
            "script": {
              "description": "Calculates logstash to Elasticsearch latency",
              "if": "ctx._tmp?.logstash_seen != null",
              "source": """
                ZonedDateTime start = ZonedDateTime.parse(ctx._tmp.logstash_seen);
                ctx.event.ingestion.latency_logstash_to_elasticsearch=ChronoUnit.SECONDS.between(start, metadata().now);
              """
            }
          },
          {
            "script": {
              "description": "Calculates Elastic Agent to Logstash latency",
              "if": "ctx._tmp?.logstash_seen != null",
              "source": """
                ZonedDateTime start = ZonedDateTime.parse(ctx['@timestamp']);
                ZonedDateTime end = ZonedDateTime.parse(ctx._tmp.logstash_seen);
                ctx.event.ingestion.latency_elastic_agent_to_logstash=ChronoUnit.SECONDS.between(start, end);
              """
            }
          }
        ]
    }
}
```

### Elastic Agent => Logstash => Kafka => Logstash => Elasticsearch

As with the previous scenario, adding an additional hop introduces another point where latency can occur. The recommendation is to add another temporary timestamp field. For more details, refer to the previous section.

This is a script that calculates the latency for each step in the pipeline. The following values will be generated:

```json
{
  "event": {
    "ingestion": {
      "latency_logstash_to_elasticsearch": 443091,
      "latency_logstash_to_logstash": 1,
      "latency": 443093,
      "latency_elastic_agent_to_logstash": 1
    }
  }
}
```

This script contains the processors needed for an ingest pipeline to calculate the ingest lag. To remove the first calculation, ensure that the object `event.ingestion` is available. You can also merge all of the steps into one larger script.

```json
POST _ingest/pipeline/_simulate
{
    "docs": [{
        "_source": {
            "@timestamp": "2025-04-03T10:00:00.000Z",
            "message": "user: philipp has logged in",
            "_tmp": {
              "logstash_pre_kafka": "2025-04-03T10:00:01.233Z",
              "logstash_post_kafka": "2025-04-03T10:00:02.456Z"
            }

        }
    }],
    "pipeline": {
        "processors": [
          {
            "script": {
              "description": "Calculates entire ingestion flow latency",
              "if": "ctx['@timestamp'] != null",
              "source": """
                ZonedDateTime start = ZonedDateTime.parse(ctx['@timestamp']);
                ctx.putIfAbsent("event", [:]);
                ctx.event.putIfAbsent("ingestion", [:]);
                ctx.event.ingestion.latency= ChronoUnit.SECONDS.between(start, metadata().now);
              """
            }
          },
          {
            "script": {
              "description": "Calculates logstash to logstash latency",
              "if": "ctx._tmp?.logstash_pre_kafka != null && ctx._tmp?.logstash_post_kafka != null",
              "source": """
                ZonedDateTime start = ZonedDateTime.parse(ctx._tmp.logstash_pre_kafka);
                ZonedDateTime end = ZonedDateTime.parse(ctx._tmp.logstash_post_kafka);
                ctx.event.ingestion.latency_logstash_to_logstash=ChronoUnit.SECONDS.between(start, end);
              """
            }
          },
          {
            "script": {
              "description": "Calculates logstash post Kafka to Elasticsearch latency",
              "if": "ctx._tmp?.logstash_post_kafka != null",
              "source": """
                ZonedDateTime start = ZonedDateTime.parse(ctx._tmp.logstash_post_kafka);
                ctx.event.ingestion.latency_logstash_to_elasticsearch=ChronoUnit.SECONDS.between(start, metadata().now);
              """
            }
          },
          {
            "script": {
              "description": "Calculates Elastic Agent to pre kafka Logstash latency",
              "if": "ctx._tmp?.logstash_pre_kafka != null",
              "source": """
                ZonedDateTime start = ZonedDateTime.parse(ctx['@timestamp']);
                ZonedDateTime end = ZonedDateTime.parse(ctx._tmp.logstash_pre_kafka);
                ctx.event.ingestion.latency_elastic_agent_to_logstash=ChronoUnit.SECONDS.between(start, end);
              """
            }
          }
        ]
    }
}
```
