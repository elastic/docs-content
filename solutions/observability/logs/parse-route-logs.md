---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/logs-parse.html
  - https://www.elastic.co/guide/en/serverless/current/observability-parse-log-data.html
applies_to:
  stack: all
  serverless: all
---

# Parse and route logs [observability-parse-log-data]

::::{note}

**For Observability serverless projects**, the **Admin** role or higher is required to create ingest pipelines that parse and route logs. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


If your log data is unstructured or semi-structured, you can parse it and break it into meaningful fields. You can use those fields to explore and analyze your data. For example, you can find logs within a specific timestamp range or filter logs by log level to focus on potential issues.

After parsing, you can use the structured fields to further organize your logs by configuring a reroute processor to send specific logs to different target data streams.

Refer to the following sections for more on parsing and organizing your log data:

* [Extract structured fields](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-extract-structured-fields): Extract structured fields like timestamps, log levels, or IP addresses to make querying and filtering your data easier.
* [Reroute log data to specific data streams](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-reroute-log-data-to-specific-data-streams): Route data from the generic data stream to a target data stream for more granular control over data retention, permissions, and processing.


## Extract structured fields [observability-parse-log-data-extract-structured-fields]

Make your logs more useful by extracting structured fields from your unstructured log data. Extracting structured fields makes it easier to search, analyze, and filter your log data.

Follow the steps below to see how the following unstructured log data is indexed by default:

```txt
2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.
```

Start by storing the document in the `logs-example-default` data stream:

1. To open **Console**, find `Dev Tools` in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the **Console** tab, add the example log to Elastic using the following command:

    ```console
    POST logs-example-default/_doc
    {
    "message": "2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%."
    }
    ```

3. Then, you can retrieve the document with the following search:

    ```console
    GET /logs-example-default/_search
    ```


The results should look like this:

```json
{
  ...
  "hits": {
    ...
    "hits": [
      {
        "_index": ".ds-logs-example-default-2023.08.09-000001",
        ...
        "_source": {
          "message": "2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.",
          "@timestamp": "2023-08-09T17:19:27.73312243Z"
        }
      }
    ]
  }
}
```

Elastic indexes the `message` field by default and adds a `@timestamp` field. Since there was no timestamp set, it’s set to `now`. At this point, you can search for phrases in the `message` field like `WARN` or `Disk usage exceeds`. For example, run the following command to search for the phrase `WARN` in the log’s `message` field:

```console
GET logs-example-default/_search
{
  "query": {
    "match": {
      "message": {
        "query": "WARN"
      }
    }
  }
}
```

While you can search for phrases in the `message` field, you can’t use this field to filter log data. Your message, however, contains all of the following potential fields you can extract and use to filter and aggregate your log data:

* **@timestamp** (`2023-08-08T13:45:12.123Z`): Extracting this field lets you sort logs by date and time. This is helpful when you want to view your logs in the order that they occurred or identify when issues happened.
* **log.level** (`WARN`): Extracting this field lets you filter logs by severity. This is helpful if you want to focus on high-severity WARN or ERROR-level logs, and reduce noise by filtering out low-severity INFO-level logs.
* **host.ip** (`192.168.1.101`): Extracting this field lets you filter logs by the host IP addresses. This is helpful if you want to focus on specific hosts that you’re having issues with or if you want to find disparities between hosts.
* **message** (`Disk usage exceeds 90%.`): You can search for phrases or words in the message field.

::::{note}
These fields are part of the [Elastic Common Schema (ECS)](asciidocalypse://docs/ecs/docs/reference/index.md). The ECS defines a common set of fields that you can use across Elastic when storing data, including log and metric data.

::::



### Extract the `@timestamp` field [observability-parse-log-data-extract-the-timestamp-field]

When you added the log to Elastic in the previous section, the `@timestamp` field showed when the log was added. The timestamp showing when the log actually occurred was in the unstructured `message` field:

```json
        ...
        "_source": {
          "message": "2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.",  <1>
          "@timestamp": "2023-08-09T17:19:27.73312243Z"  <2>
        }
        ...
```

1. The timestamp in the `message` field shows when the log occurred.
2. The timestamp in the `@timestamp` field shows when the log was added to Elastic.


When looking into issues, you want to filter for logs by when the issue occurred not when the log was added to Elastic. To do this, extract the timestamp from the unstructured `message` field to the structured `@timestamp` field by completing the following:

1. [Use an ingest pipeline to extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-use-an-ingest-pipeline-to-extract-the-timestamp-field)
2. [Test the pipeline with the simulate pipeline API](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-test-the-pipeline-with-the-simulate-pipeline-api)
3. [Configure a data stream with an index template](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-configure-a-data-stream-with-an-index-template)
4. [Create a data stream](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-create-a-data-stream)


#### Use an ingest pipeline to extract the `@timestamp` field [observability-parse-log-data-use-an-ingest-pipeline-to-extract-the-timestamp-field]

Ingest pipelines consist of a series of processors that perform common transformations on incoming documents before they are indexed. To extract the `@timestamp` field from the example log, use an ingest pipeline with a [dissect processor](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/enrich-processor/dissect-processor.md). The dissect processor extracts structured fields from unstructured log messages based on a pattern you set.

Elastic can parse string timestamps that are in `yyyy-MM-dd'T'HH:mm:ss.SSSZ` and `yyyy-MM-dd` formats into date fields. Since the log example’s timestamp is in one of these formats, you don’t need additional processors. More complex or nonstandard timestamps require a [date processor](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/enrich-processor/date-processor.md) to parse the timestamp into a date field.

Use the following command to extract the timestamp from the `message` field into the `@timestamp` field:

```console
PUT _ingest/pipeline/logs-example-default
{
  "description": "Extracts the timestamp",
  "processors": [
    {
      "dissect": {
        "field": "message",
        "pattern": "%{@timestamp} %{message}"
      }
    }
  ]
}
```

The previous command sets the following values for your ingest pipeline:

* `_ingest/pipeline/logs-example-default`: The name of the pipeline,`logs-example-default`, needs to match the name of your data stream. You’ll set up your data stream in the next section. For more information, refer to the [data stream naming scheme](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/data-streams.md#data-streams-naming-scheme).
* `field`: The field you’re extracting data from, `message` in this case.
* `pattern`: The pattern of the elements in your log data. The `%{@timestamp} %{{message}}` pattern extracts the timestamp, `2023-08-08T13:45:12.123Z`, to the `@timestamp` field, while the rest of the message, `WARN 192.168.1.101 Disk usage exceeds 90%.`, stays in the `message` field. The dissect processor looks for the space as a separator defined by the pattern.


#### Test the pipeline with the simulate pipeline API [observability-parse-log-data-test-the-pipeline-with-the-simulate-pipeline-api]

The [simulate pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-simulate) runs the ingest pipeline without storing any documents. This lets you verify your pipeline works using multiple documents.

Run the following command to test your ingest pipeline with the simulate pipeline API.

```console
POST _ingest/pipeline/logs-example-default/_simulate
{
  "docs": [
    {
      "_source": {
        "message": "2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%."
      }
    }
  ]
}
```

The results should show the `@timestamp` field extracted from the `message` field:

```console
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_version": "-3",
        "_source": {
          "message": "WARN 192.168.1.101 Disk usage exceeds 90%.",
          "@timestamp": "2023-08-08T13:45:12.123Z"
        },
        ...
      }
    }
  ]
}
```

::::{note}
Make sure you’ve created the ingest pipeline using the `PUT` command in the previous section before using the simulate pipeline API.

::::



#### Configure a data stream with an index template [observability-parse-log-data-configure-a-data-stream-with-an-index-template]

After creating your ingest pipeline, run the following command to create an index template to configure your data stream’s backing indices:

```console
PUT _index_template/logs-example-default-template
{
  "index_patterns": [ "logs-example-*" ],
  "data_stream": { },
  "priority": 500,
  "template": {
    "settings": {
      "index.default_pipeline":"logs-example-default"
    }
  },
  "composed_of": [
    "logs@mappings",
    "logs@settings",
    "logs@custom",
    "ecs@mappings"
  ],
  "ignore_missing_component_templates": ["logs@custom"]
}
```

The previous command sets the following values for your index template:

* `index_pattern`: Needs to match your log data stream. Naming conventions for data streams are `<type>-<dataset>-<namespace>`. In this example, your logs data stream is named `logs-example-*`. Data that matches this pattern will go through your pipeline.
* `data_stream`: Enables data streams.
* `priority`: Sets the priority of your index templates. Index templates with a higher priority take precedence. If a data stream matches multiple index templates, Elastic uses the template with the higher priority. Built-in templates have a priority of `200`, so use a priority higher than `200` for custom templates.
* `index.default_pipeline`: The name of your ingest pipeline. `logs-example-default` in this case.
* `composed_of`: Here you can set component templates. Component templates are building blocks for constructing index templates that specify index mappings, settings, and aliases. Elastic has several built-in templates to help when ingesting your log data.

The example index template above sets the following component templates:

* `logs@mappings`: general mappings for log data streams that include disabling automatic date detection from `string` fields and specifying mappings for [`data_stream` ECS fields](asciidocalypse://docs/ecs/docs/reference/ecs-data_stream.md).
* `logs@settings`: general settings for log data streams including the following:

    * The default lifecycle policy that rolls over when the primary shard reaches 50 GB or after 30 days.
    * The default pipeline uses the ingest timestamp if there is no specified `@timestamp` and places a hook for the `logs@custom` pipeline. If a `logs@custom` pipeline is installed, it’s applied to logs ingested into this data stream.
    * Sets the [`ignore_malformed`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/ignore-malformed.md) flag to `true`. When ingesting a large batch of log data, a single malformed field like an IP address can cause the entire batch to fail. When set to true, malformed fields with a mapping type that supports this flag are still processed.
    * `logs@custom`: a predefined component template that is not installed by default. Use this name to install a custom component template to override or extend any of the default mappings or settings.
    * `ecs@mappings`: dynamic templates that automatically ensure your data stream mappings comply with the [Elastic Common Schema (ECS)](asciidocalypse://docs/ecs/docs/reference/index.md).



#### Create a data stream [observability-parse-log-data-create-a-data-stream]

Create your data stream using the [data stream naming scheme](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/data-streams.md#data-streams-naming-scheme). Name your data stream to match the name of your ingest pipeline, `logs-example-default` in this case. Post the example log to your data stream with this command:

```console
POST logs-example-default/_doc
{
  "message": "2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%."
}
```

View your documents using this command:

```console
GET /logs-example-default/_search
```

You should see the pipeline has extracted the `@timestamp` field:

```json
{
  ...
  {
    ...
    "hits": {
      ...
      "hits": [
        {
          "_index": ".ds-logs-example-default-2023.08.09-000001",
          "_id": "RsWy3IkB8yCtA5VGOKLf",
          "_score": 1,
          "_source": {
            "message": "WARN 192.168.1.101 Disk usage exceeds 90%.",
            "@timestamp": "2023-08-08T13:45:12.123Z"  <1>
          }
        }
      ]
    }
  }
}
```

1. The extracted `@timestamp` field.


You can now use the `@timestamp` field to sort your logs by the date and time they happened.


#### Troubleshoot the `@timestamp` field [observability-parse-log-data-troubleshoot-the-timestamp-field]

Check the following common issues and solutions with timestamps:

* **Timestamp failure:** If your data has inconsistent date formats, set `ignore_failure` to `true` for your date processor. This processes logs with correctly formatted dates and ignores those with issues.
* **Incorrect timezone:** Set your timezone using the `timezone` option on the [date processor](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/enrich-processor/date-processor.md).
* **Incorrect timestamp format:** Your timestamp can be a Java time pattern or one of the following formats: ISO8601, UNIX, UNIX_MS, or TAI64N. For more information on timestamp formats, refer to the [mapping date format](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/mapping-date-format.md).


### Extract the `log.level` field [observability-parse-log-data-extract-the-loglevel-field]

Extracting the `log.level` field lets you filter by severity and focus on critical issues. This section shows you how to extract the `log.level` field from this example log:

```txt
2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.
```

To extract and use the `log.level` field:

1. [Add the `log.level` field to the dissect processor pattern in your ingest pipeline.](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-add-loglevel-to-your-ingest-pipeline)
2. [Test the pipeline with the simulate API.](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-test-the-pipeline-with-the-simulate-api)
3. [Query your logs based on the `log.level` field.](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-query-logs-based-on-loglevel)


#### Add `log.level` to your ingest pipeline [observability-parse-log-data-add-loglevel-to-your-ingest-pipeline]

Add the `%{log.level}` option to the dissect processor pattern in the ingest pipeline you created in the [Extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-use-an-ingest-pipeline-to-extract-the-timestamp-field) section with this command:

```console
PUT _ingest/pipeline/logs-example-default
{
  "description": "Extracts the timestamp and log level",
  "processors": [
    {
      "dissect": {
        "field": "message",
        "pattern": "%{@timestamp} %{log.level} %{message}"
      }
    }
  ]
}
```

Now your pipeline will extract these fields:

* The `@timestamp` field: `2023-08-08T13:45:12.123Z`
* The `log.level` field: `WARN`
* The `message` field: `192.168.1.101 Disk usage exceeds 90%.`

In addition to setting an ingest pipeline, you need to set an index template. Use the index template created in the [Extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-configure-a-data-stream-with-an-index-template) section.


#### Test the pipeline with the simulate API [observability-parse-log-data-test-the-pipeline-with-the-simulate-api]

Test that your ingest pipeline works as expected with the [simulate pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-simulate):

```console
POST _ingest/pipeline/logs-example-default/_simulate
{
  "docs": [
    {
      "_source": {
        "message": "2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%."
      }
    }
  ]
}
```

The results should show the `@timestamp` and the `log.level` fields extracted from the `message` field:

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_version": "-3",
        "_source": {
          "message": "192.168.1.101 Disk usage exceeds 90%.",
          "log": {
            "level": "WARN"
          },
          "@timestamp": "2023-8-08T13:45:12.123Z",
        },
        ...
      }
    }
  ]
}
```


#### Query logs based on `log.level` [observability-parse-log-data-query-logs-based-on-loglevel]

Once you’ve extracted the `log.level` field, you can query for high-severity logs like `WARN` and `ERROR`, which may need immediate attention, and filter out less critical `INFO` and `DEBUG` logs.

Let’s say you have the following logs with varying severities:

```txt
2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.
2023-08-08T13:45:14.003Z ERROR 192.168.1.103 Database connection failed.
2023-08-08T13:45:15.004Z DEBUG 192.168.1.104 Debugging connection issue.
2023-08-08T13:45:16.005Z INFO 192.168.1.102 User changed profile picture.
```

Add them to your data stream using this command:

```console
POST logs-example-default/_bulk
{ "create": {} }
{ "message": "2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%." }
{ "create": {} }
{ "message": "2023-08-08T13:45:14.003Z ERROR 192.168.1.103 Database connection failed." }
{ "create": {} }
{ "message": "2023-08-08T13:45:15.004Z DEBUG 192.168.1.104 Debugging connection issue." }
{ "create": {} }
{ "message": "2023-08-08T13:45:16.005Z INFO 192.168.1.102 User changed profile picture." }
```

Then, query for documents with a log level of `WARN` or `ERROR` with this command:

```console
GET logs-example-default/_search
{
  "query": {
    "terms": {
      "log.level": ["WARN", "ERROR"]
    }
  }
}
```

The results should show only the high-severity logs:

```json
{
...
  },
  "hits": {
  ...
    "hits": [
      {
        "_index": ".ds-logs-example-default-2023.08.14-000001",
        "_id": "3TcZ-4kB3FafvEVY4yKx",
        "_score": 1,
        "_source": {
          "message": "192.168.1.101 Disk usage exceeds 90%.",
          "log": {
            "level": "WARN"
          },
          "@timestamp": "2023-08-08T13:45:12.123Z"
        }
      },
      {
        "_index": ".ds-logs-example-default-2023.08.14-000001",
        "_id": "3jcZ-4kB3FafvEVY4yKx",
        "_score": 1,
        "_source": {
          "message": "192.168.1.103 Database connection failed.",
          "log": {
            "level": "ERROR"
          },
          "@timestamp": "2023-08-08T13:45:14.003Z"
        }
      }
    ]
  }
}
```


### Extract the `host.ip` field [observability-parse-log-data-extract-the-hostip-field]

Extracting the `host.ip` field lets you filter logs by host IP addresses allowing you to focus on specific hosts that you’re having issues with or find disparities between hosts.

The `host.ip` field is part of the [Elastic Common Schema (ECS)](asciidocalypse://docs/ecs/docs/reference/index.md). Through the ECS, the `host.ip` field is mapped as an [`ip` field type](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/ip.md). `ip` field types allow range queries so you can find logs with IP addresses in a specific range. You can also query `ip` field types using Classless Inter-Domain Routing (CIDR) notation to find logs from a particular network or subnet.

This section shows you how to extract the `host.ip` field from the following example logs and query based on the extracted fields:

```txt
2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.
2023-08-08T13:45:14.003Z ERROR 192.168.1.103 Database connection failed.
2023-08-08T13:45:15.004Z DEBUG 192.168.1.104 Debugging connection issue.
2023-08-08T13:45:16.005Z INFO 192.168.1.102 User changed profile picture.
```

To extract and use the `host.ip` field:

1. [Add the `host.ip` field to your dissect processor in your ingest pipeline.](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-add-hostip-to-your-ingest-pipeline)
2. [Test the pipeline with the simulate API.](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-test-the-pipeline-with-the-simulate-api)
3. [Query your logs based on the `host.ip` field.](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-query-logs-based-on-hostip)


#### Add `host.ip` to your ingest pipeline [observability-parse-log-data-add-hostip-to-your-ingest-pipeline]

Add the `%{host.ip}` option to the dissect processor pattern in the ingest pipeline you created in the [Extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-use-an-ingest-pipeline-to-extract-the-timestamp-field) section:

```console
PUT _ingest/pipeline/logs-example-default
{
  "description": "Extracts the timestamp log level and host ip",
  "processors": [
    {
      "dissect": {
        "field": "message",
        "pattern": "%{@timestamp} %{log.level} %{host.ip} %{message}"
      }
    }
  ]
}
```

Your pipeline will extract these fields:

* The `@timestamp` field: `2023-08-08T13:45:12.123Z`
* The `log.level` field: `WARN`
* The `host.ip` field: `192.168.1.101`
* The `message` field: `Disk usage exceeds 90%.`

In addition to setting an ingest pipeline, you need to set an index template. Use the index template created in the [Extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-configure-a-data-stream-with-an-index-template) section.


#### Test the pipeline with the simulate API [observability-parse-log-data-test-the-pipeline-with-the-simulate-api-1]

Test that your ingest pipeline works as expected with the [simulate pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-simulate):

```console
POST _ingest/pipeline/logs-example-default/_simulate
{
  "docs": [
    {
      "_source": {
        "message": "2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%."
      }
    }
  ]
}
```

The results should show the `host.ip`, `@timestamp`, and `log.level` fields extracted from the `message` field:

```json
{
  "docs": [
    {
      "doc": {
        ...
        "_source": {
          "host": {
            "ip": "192.168.1.101"
          },
          "@timestamp": "2023-08-08T13:45:12.123Z",
          "message": "Disk usage exceeds 90%.",
          "log": {
            "level": "WARN"
          }
        },
        ...
      }
    }
  ]
}
```


#### Query logs based on `host.ip` [observability-parse-log-data-query-logs-based-on-hostip]

You can query your logs based on the `host.ip` field in different ways, including using CIDR notation and range queries.

Before querying your logs, add them to your data stream using this command:

```console
POST logs-example-default/_bulk
{ "create": {} }
{ "message": "2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%." }
{ "create": {} }
{ "message": "2023-08-08T13:45:14.003Z ERROR 192.168.1.103 Database connection failed." }
{ "create": {} }
{ "message": "2023-08-08T13:45:15.004Z DEBUG 192.168.1.104 Debugging connection issue." }
{ "create": {} }
{ "message": "2023-08-08T13:45:16.005Z INFO 192.168.1.102 User changed profile picture." }
```


##### CIDR notation [observability-parse-log-data-cidr-notation]

You can use [CIDR notation](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation) to query your log data using a block of IP addresses that fall within a certain network segment. CIDR notations uses the format of `[IP address]/[prefix length]`. The following command queries IP addresses in the `192.168.1.0/24` subnet meaning IP addresses from `192.168.1.0` to `192.168.1.255`.

```console
GET logs-example-default/_search
{
  "query": {
    "term": {
      "host.ip": "192.168.1.0/24"
    }
  }
}
```

Because all of the example logs are in this range, you’ll get the following results:

```json
{
  ...
  },
  "hits": {
    ...
      {
        "_index": ".ds-logs-example-default-2023.08.16-000001",
        "_id": "ak4oAIoBl7fe5ItIixuB",
        "_score": 1,
        "_source": {
          "host": {
            "ip": "192.168.1.101"
          },
          "@timestamp": "2023-08-08T13:45:12.123Z",
          "message": "Disk usage exceeds 90%.",
          "log": {
            "level": "WARN"
          }
        }
      },
      {
        "_index": ".ds-logs-example-default-2023.08.16-000001",
        "_id": "a04oAIoBl7fe5ItIixuC",
        "_score": 1,
        "_source": {
          "host": {
            "ip": "192.168.1.103"
          },
          "@timestamp": "2023-08-08T13:45:14.003Z",
          "message": "Database connection failed.",
          "log": {
            "level": "ERROR"
          }
        }
      },
      {
        "_index": ".ds-logs-example-default-2023.08.16-000001",
        "_id": "bE4oAIoBl7fe5ItIixuC",
        "_score": 1,
        "_source": {
          "host": {
            "ip": "192.168.1.104"
          },
          "@timestamp": "2023-08-08T13:45:15.004Z",
          "message": "Debugging connection issue.",
          "log": {
            "level": "DEBUG"
          }
        }
      },
      {
        "_index": ".ds-logs-example-default-2023.08.16-000001",
        "_id": "bU4oAIoBl7fe5ItIixuC",
        "_score": 1,
        "_source": {
          "host": {
            "ip": "192.168.1.102"
          },
          "@timestamp": "2023-08-08T13:45:16.005Z",
          "message": "User changed profile picture.",
          "log": {
            "level": "INFO"
          }
        }
      }
    ]
  }
}
```


##### Range queries [observability-parse-log-data-range-queries]

Use [range queries](asciidocalypse://docs/elasticsearch/docs/reference/query-languages/query-dsl-range-query.md) to query logs in a specific range.

The following command searches for IP addresses greater than or equal to `192.168.1.100` and less than or equal to `192.168.1.102`.

```console
GET logs-example-default/_search
{
  "query": {
    "range": {
      "host.ip": {
        "gte": "192.168.1.100",  <1>
        "lte": "192.168.1.102"  <2>
      }
    }
  }
}
```

1. Greater than or equal to `192.168.1.100`.
2. Less than or equal to `192.168.1.102`.


You’ll get the following results only showing logs in the range you’ve set:

```json
{
  ...
  },
  "hits": {
    ...
      {
        "_index": ".ds-logs-example-default-2023.08.16-000001",
        "_id": "ak4oAIoBl7fe5ItIixuB",
        "_score": 1,
        "_source": {
          "host": {
            "ip": "192.168.1.101"
          },
          "@timestamp": "2023-08-08T13:45:12.123Z",
          "message": "Disk usage exceeds 90%.",
          "log": {
            "level": "WARN"
          }
        }
      },
      {
        "_index": ".ds-logs-example-default-2023.08.16-000001",
        "_id": "bU4oAIoBl7fe5ItIixuC",
        "_score": 1,
        "_source": {
          "host": {
            "ip": "192.168.1.102"
          },
          "@timestamp": "2023-08-08T13:45:16.005Z",
          "message": "User changed profile picture.",
          "log": {
            "level": "INFO"
          }
        }
      }
    ]
  }
}
```


## Reroute log data to specific data streams [observability-parse-log-data-reroute-log-data-to-specific-data-streams]

By default, an ingest pipeline sends your log data to a single data stream. To simplify log data management, use a [reroute processor](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/enrich-processor/reroute-processor.md) to route data from the generic data stream to a target data stream. For example, you might want to send high-severity logs to a specific data stream to help with categorization.

This section shows you how to use a reroute processor to send the high-severity logs (`WARN` or `ERROR`) from the following example logs to a specific data stream and keep the regular logs (`DEBUG` and `INFO`) in the default data stream:

```txt
2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.
2023-08-08T13:45:14.003Z ERROR 192.168.1.103 Database connection failed.
2023-08-08T13:45:15.004Z DEBUG 192.168.1.104 Debugging connection issue.
2023-08-08T13:45:16.005Z INFO 192.168.1.102 User changed profile picture.
```

::::{note}
When routing data to different data streams, we recommend picking a field with a limited number of distinct values to prevent an excessive increase in the number of data streams. For more details, refer to the [Size your shards](../../../deploy-manage/production-guidance/optimize-performance/size-shards.md) documentation.

::::


To use a reroute processor:

1. [Add a reroute processor to your ingest pipeline.](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-add-a-reroute-processor-to-the-ingest-pipeline)
2. [Add the example logs to your data stream.](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-add-logs-to-a-data-stream)
3. [Query your logs and verify the high-severity logs were routed to the new data stream.](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-verify-the-reroute-processor-worked)


### Add a reroute processor to the ingest pipeline [observability-parse-log-data-add-a-reroute-processor-to-the-ingest-pipeline]

Add a reroute processor to your ingest pipeline with the following command:

```console
PUT _ingest/pipeline/logs-example-default
{
  "description": "Extracts fields and reroutes WARN",
  "processors": [
    {
      "dissect": {
        "field": "message",
        "pattern": "%{@timestamp} %{log.level} %{host.ip} %{message}"
      }
    },
    {
      "reroute": {
        "tag": "high_severity_logs",
        "if" : "ctx.log?.level == 'WARN' || ctx.log?.level == 'ERROR'",
        "dataset": "critical"
      }
    }
  ]
}
```

The previous command sets the following values for your reroute processor:

* `tag`: Identifier for the processor that you can use for debugging and metrics. In the example, the tag is set to `high_severity_logs`.
* `if`: Conditionally runs the processor. In the example, `"ctx.log?.level == 'WARN' || ctx.log?.level == 'ERROR'",` means the processor runs when the `log.level` field is `WARN` or `ERROR`.
* `dataset`: the data stream dataset to route your document to if the previous condition is `true`. In the example, logs with a `log.level` of `WARN` or `ERROR` are routed to the `logs-critical-default` data stream.

In addition to setting an ingest pipeline, you need to set an index template. Use the index template created in the [Extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-configure-a-data-stream-with-an-index-template) section.


### Add logs to a data stream [observability-parse-log-data-add-logs-to-a-data-stream]

Add the example logs to your data stream with this command:

```console
POST logs-example-default/_bulk
{ "create": {} }
{ "message": "2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%." }
{ "create": {} }
{ "message": "2023-08-08T13:45:14.003Z ERROR 192.168.1.103 Database connection failed." }
{ "create": {} }
{ "message": "2023-08-08T13:45:15.004Z DEBUG 192.168.1.104 Debugging connection issue." }
{ "create": {} }
{ "message": "2023-08-08T13:45:16.005Z INFO 192.168.1.102 User changed profile picture." }
```


### Verify the reroute processor worked [observability-parse-log-data-verify-the-reroute-processor-worked]

The reroute processor should route any logs with a `log.level` of `WARN` or `ERROR` to the `logs-critical-default` data stream. Query the data stream using the following command to verify the log data was routed as intended:

```console
GET logs-critical-default/_search
```

Your should see similar results to the following showing that the high-severity logs are now in the `critical` dataset:

```json
{
  ...
  "hits": {
    ...
    "hits": [
        ...
        "_source": {
          "host": {
            "ip": "192.168.1.101"
          },
          "@timestamp": "2023-08-08T13:45:12.123Z",
          "message": "Disk usage exceeds 90%.",
          "log": {
            "level": "WARN"
          },
          "data_stream": {
            "namespace": "default",
            "type": "logs",
            "dataset": "critical"
          },
          {
        ...
        "_source": {
          "host": {
            "ip": "192.168.1.103"
           },
          "@timestamp": "2023-08-08T13:45:14.003Z",
          "message": "Database connection failed.",
          "log": {
            "level": "ERROR"
          },
          "data_stream": {
            "namespace": "default",
            "type": "logs",
            "dataset": "critical"
          }
        }
      }
    ]
  }
}
```