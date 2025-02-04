# Parse and organize logs [logs-parse]

If your log data is unstructured or semi-structured, you can parse it and break it into meaningful fields. You can use those fields to explore and analyze your data. For example, you can find logs within a specific timestamp range or filter logs by log level to focus on potential issues.

After parsing, you can use the structured fields to further organize your logs by configuring a reroute processor to send specific logs to different target data streams.

Refer to the following sections for more on parsing and organizing your log data:

* [Extract structured fields](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-parse): Extract structured fields like timestamps, log levels, or IP addresses to make querying and filtering your data easier.
* [Reroute log data to specific data streams](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-reroute): Route data from the generic data stream to a target data stream for more granular control over data retention, permissions, and processing.


## Extract structured fields [logs-stream-parse]

Make your logs more useful by extracting structured fields from your unstructured log data. Extracting structured fields makes it easier to search, analyze, and filter your log data.

Follow the steps below to see how the following unstructured log data is indexed by default:

```log
2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.
```

Start by storing the document in the `logs-example-default` data stream:

1. To open **Console**, find `Dev Tools` in the [global search field](../../../get-started/the-stack.md#kibana-navigation-search).
2. In the **Console** tab, add the example log to {{es}} using the following command:

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

```JSON
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

{{es}} indexes the `message` field by default and adds a `@timestamp` field. Since there was no timestamp set, it’s set to `now`. At this point, you can search for phrases in the `message` field like `WARN` or `Disk usage exceeds`. For example, use the following command to search for the phrase `WARN` in the log’s `message` field:

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
These fields are part of the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/{{ecs_version}}/ecs-reference.html). The ECS defines a common set of fields that you can use across Elasticsearch when storing data, including log and metric data.
::::



### Extract the `@timestamp` field [logs-stream-extract-timestamp]

When you added the log to {{es}} in the previous section, the `@timestamp` field showed when the log was added. The timestamp showing when the log actually occurred was in the unstructured `message` field:

```JSON
        ...
        "_source": {
          "message": "2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.",<1>
          "@timestamp": "2023-08-09T17:19:27.73312243Z"<2>
        }
        ...
```

1. The timestamp in the `message` field shows when the log occurred.
2. The timestamp in the `@timestamp` field shows when the log was added to {{es}}.


When looking into issues, you want to filter for logs by when the issue occurred not when the log was added to your project. To do this, extract the timestamp from the unstructured `message` field to the structured `@timestamp` field by completing the following:

1. [Use an ingest pipeline to extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-ingest-pipeline)
2. [Test the pipeline with the simulate pipeline API](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-simulate-api)
3. [Configure a data stream with an index template](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-index-template)
4. [Create a data stream](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-create-data-stream)


#### Use an ingest pipeline to extract the `@timestamp` field [logs-stream-ingest-pipeline]

Ingest pipelines consist of a series of processors that perform common transformations on incoming documents before they are indexed. To extract the `@timestamp` field from the example log, use an ingest pipeline with a dissect processor. The [dissect processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/dissect-processor.html) extracts structured fields from unstructured log messages based on a pattern you set.

{{es}} can parse string timestamps that are in `yyyy-MM-dd'T'HH:mm:ss.SSSZ` and `yyyy-MM-dd` formats into date fields. Since the log example’s timestamp is in one of these formats, you don’t need additional processors. More complex or nonstandard timestamps require a [date processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/date-processor.html) to parse the timestamp into a date field.

Use the following command to extract the timestamp from the `message` field into the `@timestamp` field:

```console
PUT _ingest/pipeline/logs-example-default<1>
{
  "description": "Extracts the timestamp",
  "processors": [
    {
      "dissect": {
        "field": "message",<2>
        "pattern": "%{@timestamp} %{message}"<3>
      }
    }
  ]
}
```

1. The name of the pipeline,`logs-example-default`, needs to match the name of your data stream. You’ll set up your data stream in the next section. For more information, refer to the [data stream naming scheme](https://www.elastic.co/guide/en/fleet/current/data-streams.html#data-streams-naming-scheme).
2. The field you’re extracting data from, `message` in this case.
3. The pattern of the elements in your log data. The `%{@timestamp} %{{message}}` pattern extracts the timestamp, `2023-08-08T13:45:12.123Z`, to the `@timestamp` field, while the rest of the message, `WARN 192.168.1.101 Disk usage exceeds 90%.`, stays in the `message` field. The dissect processor looks for the space as a separator defined by the pattern.



#### Test the pipeline with the simulate pipeline API [logs-stream-simulate-api]

The [simulate pipeline API](https://www.elastic.co/guide/en/elasticsearch/reference/current/simulate-pipeline-api.html#ingest-verbose-param) runs the ingest pipeline without storing any documents. This lets you verify your pipeline works using multiple documents. Run the following command to test your ingest pipeline with the simulate pipeline API.

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



#### Configure a data stream with an index template [logs-stream-index-template]

After creating your ingest pipeline, run the following command to create an index template to configure your data stream’s backing indices:

```console
PUT _index_template/logs-example-default-template
{
  "index_patterns": [ "logs-example-*" ],<1>
  "data_stream": { },<2>
  "priority": 500,<3>
  "template": {
    "settings": {
      "index.default_pipeline":"logs-example-default"<4>
    }
  },
  "composed_of": [<5>
    "logs@mappings",
    "logs@settings",
    "logs@custom",
    "ecs@mappings"
  ],
  "ignore_missing_component_templates": ["logs@custom"]
}
```

1. `index_pattern`: Needs to match your log data stream. Naming conventions for data streams are `<type>-<dataset>-<namespace>`. In this example, your logs data stream is named `logs-example-*`. Data that matches this pattern will go through your pipeline.
2. `data_stream`: Enables data streams.
3. `priority`: Sets the priority of you Index Template. Index templates with higher priority take precedence over lower priority. If a data stream matches multiple index templates, {{es}} uses the template with the higher priority. Built-in templates have a priority of `200`, so use a priority higher than `200` for custom templates.
4. `index.default_pipeline`: The name of your ingest pipeline. `logs-example-default` in this case.
5. `composed_of`: Here you can set component templates. Component templates are building blocks for constructing index templates that specify index mappings, settings, and aliases. Elastic has several built-in templates to help when ingesting your log data.


The example index template above sets the following component templates:

* `logs@mappings`: general mappings for log data streams that include disabling automatic date detection from `string` fields and specifying mappings for [`data_stream` ECS fields](https://www.elastic.co/guide/en/ecs/{{ecs_version}}/ecs-data_stream.html).
* `logs@settings`: general settings for log data streams including the following:

    * The default lifecycle policy that rolls over when the primary shard reaches 50 GB or after 30 days.
    * The default pipeline uses the ingest timestamp if there is no specified `@timestamp` and places a hook for the `logs@custom` pipeline. If a `logs@custom` pipeline is installed, it’s applied to logs ingested into this data stream.
    * Sets the [`ignore_malformed`](https://www.elastic.co/guide/en/elasticsearch/reference/current/ignore-malformed.html) flag to `true`. When ingesting a large batch of log data, a single malformed field like an IP address can cause the entire batch to fail. When set to true, malformed fields with a mapping type that supports this flag are still processed.

* `logs@custom`: a predefined component template that is not installed by default. Use this name to install a custom component template to override or extend any of the default mappings or settings.
* `ecs@mappings`: dynamic templates that automatically ensure your data stream mappings comply with the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/{{ecs_version}}/ecs-reference.html).


#### Create a data stream [logs-stream-create-data-stream]

Create your data stream using the [data stream naming scheme](https://www.elastic.co/guide/en/fleet/current/data-streams.html#data-streams-naming-scheme). Name your data stream to match the name of your ingest pipeline, `logs-example-default` in this case. Post the example log to your data stream with this command:

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

```JSON
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
          "@timestamp": "2023-08-08T13:45:12.123Z"<1>
        }
      }
    ]
  }
}
```

1. The extracted `@timestamp` field.


You can now use the `@timestamp` field to sort your logs by the date and time they happened.


#### Troubleshoot the `@timestamp` field [logs-stream-timestamp-troubleshooting]

Check the following common issues and solutions with timestamps:

* **Timestamp failure**: If your data has inconsistent date formats, set `ignore_failure` to `true` for your date processor. This processes logs with correctly formatted dates and ignores those with issues.
* **Incorrect timezone**: Set your timezone using the `timezone` option on the [date processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/date-processor.html).
* **Incorrect timestamp format**: Your timestamp can be a Java time pattern or one of the following formats: ISO8601, UNIX, UNIX_MS, or TAI64N. For more information on timestamp formats, refer to the [mapping date format](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-date-format.html).


### Extract the `log.level` field [logs-stream-extract-log-level]

Extracting the `log.level` field lets you filter by severity and focus on critical issues. This section shows you how to extract the `log.level` field from this example log:

```log
2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.
```

To extract and use the `log.level` field:

1. [Add the `log.level` field to the dissect processor pattern in your ingest pipeline.](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-log-level-pipeline)
2. [Test the pipeline with the simulate API.](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-log-level-simulate)
3. [Query your logs based on the `log.level` field.](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-log-level-query)


#### Add `log.level` to your ingest pipeline [logs-stream-log-level-pipeline]

Add the `%{log.level}` option to the dissect processor pattern in the ingest pipeline you created in the [Extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-ingest-pipeline) section with this command:

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

In addition to setting an ingest pipeline, you need to set an index template. You can use the index template created in the [Extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-index-template) section.


#### Test the pipeline with the simulate API [logs-stream-log-level-simulate]

Test that your ingest pipeline works as expected with the [simulate pipeline API](https://www.elastic.co/guide/en/elasticsearch/reference/current/simulate-pipeline-api.html#ingest-verbose-param):

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

```JSON
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


#### Query logs based on `log.level` [logs-stream-log-level-query]

Once you’ve extracted the `log.level` field, you can query for high-severity logs like `WARN` and `ERROR`, which may need immediate attention, and filter out less critical `INFO` and `DEBUG` logs.

Let’s say you have the following logs with varying severities:

```log
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

```JSON
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


### Extract the `host.ip` field [logs-stream-extract-host-ip]

Extracting the `host.ip` field lets you filter logs by host IP addresses allowing you to focus on specific hosts that you’re having issues with or find disparities between hosts.

The `host.ip` field is part of the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/{{ecs_version}}/ecs-reference.html). Through the ECS, the `host.ip` field is mapped as an [`ip` field type](https://www.elastic.co/guide/en/elasticsearch/reference/current/ip.html). `ip` field types allow range queries so you can find logs with IP addresses in a specific range. You can also query `ip` field types using Classless Inter-Domain Routing (CIDR) notation to find logs from a particular network or subnet.

This section shows you how to extract the `host.ip` field from the following example logs and query based on the extracted fields:

```log
2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.
2023-08-08T13:45:14.003Z ERROR 192.168.1.103 Database connection failed.
2023-08-08T13:45:15.004Z DEBUG 192.168.1.104 Debugging connection issue.
2023-08-08T13:45:16.005Z INFO 192.168.1.102 User changed profile picture.
```

To extract and use the `host.ip` field:

1. [Add the `host.ip` field to your dissect processor in your ingest pipeline.](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-host-ip-pipeline)
2. [Test the pipeline with the simulate API.](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-host-ip-simulate)
3. [Query your logs based on the `host.ip` field.](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-host-ip-query)


#### Add `host.ip` to your ingest pipeline [logs-stream-host-ip-pipeline]

Add the `%{host.ip}` option to the dissect processor pattern in the ingest pipeline you created in the [Extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-ingest-pipeline) section:

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

In addition to setting an ingest pipeline, you need to set an index template. You can use the index template created in the [Extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-index-template) section.


#### Test the pipeline with the simulate API [logs-stream-host-ip-simulate]

Test that your ingest pipeline works as expected with the [simulate pipeline API](https://www.elastic.co/guide/en/elasticsearch/reference/current/simulate-pipeline-api.html#ingest-verbose-param):

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

```JSON
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


#### Query logs based on `host.ip` [logs-stream-host-ip-query]

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


##### CIDR notation [logs-stream-ip-cidr]

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

```JSON
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


##### Range queries [logs-stream-range-query]

Use [range queries](https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html) to query logs in a specific range.

The following command searches for IP addresses greater than or equal to `192.168.1.100` and less than or equal to `192.168.1.102`.

```console
GET logs-example-default/_search
{
  "query": {
    "range": {
      "host.ip": {
        "gte": "192.168.1.100",<1>
        "lte": "192.168.1.102"<2>
      }
    }
  }
}
```

1. Greater than or equal to `192.168.1.100`.
2. Less than or equal to `192.168.1.102`.


You’ll get the following results only showing logs in the range you’ve set:

```JSON
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


## Reroute log data to specific data streams [logs-stream-reroute]

By default, an ingest pipeline sends your log data to a single data stream. To simplify log data management, use a [reroute processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/reroute-processor.html) to route data from the generic data stream to a target data stream. For example, you might want to send high-severity logs to a specific data stream to help with categorization.

This section shows you how to use a reroute processor to send the high-severity logs (`WARN` or `ERROR`) from the following example logs to a specific data stream and keep the regular logs (`DEBUG` and `INFO`) in the default data stream:

```log
2023-08-08T13:45:12.123Z WARN 192.168.1.101 Disk usage exceeds 90%.
2023-08-08T13:45:14.003Z ERROR 192.168.1.103 Database connection failed.
2023-08-08T13:45:15.004Z DEBUG 192.168.1.104 Debugging connection issue.
2023-08-08T13:45:16.005Z INFO 192.168.1.102 User changed profile picture.
```

::::{note}
When routing data to different data streams, we recommend picking a field with a limited number of distinct values to prevent an excessive increase in the number of data streams. For more details, refer to the [Size your shards](../../../deploy-manage/production-guidance/optimize-performance/size-shards.md) documentation.
::::


To use a reroute processor:

1. [Add a reroute processor to your ingest pipeline.](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-reroute-pipeline)
2. [Add the example logs to your data stream.](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-reroute-add-logs)
3. [Query your logs and verify the high-severity logs were routed to the new data stream.](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-reroute-verify)


### Add a reroute processor to the ingest pipeline [logs-stream-reroute-pipeline]

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
      },
      "reroute": {
        "tag": "high_severity_logs",<1>
        "if" : "ctx.log?.level == 'WARN' || ctx.log?.level == 'ERROR'",<2>
        "dataset": "critical"<3>
      }
    }
  ]
}
```

1. `tag`: Identifier for the processor that you can use for debugging and metrics. In the example, the tag is set to `high_severity_logs`.
2. `if`: Conditionally runs the processor. In the example, `"ctx.log?.level == 'WARN' || ctx.log?.level == 'ERROR'",` means the processor runs when the `log.level` field is `WARN` or `ERROR`.
3. `dataset`: the data stream dataset to route your document to if the previous condition is `true`. In the example, logs with a `log.level` of `WARN` or `ERROR` are routed to the `logs-critical-default` data stream.


In addition to setting an ingest pipeline, you need to set an index template. You can use the index template created in the [Extract the `@timestamp` field](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-index-template) section.


### Add logs to a data stream [logs-stream-reroute-add-logs]

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


### Verify the reroute processor worked [logs-stream-reroute-verify]

The reroute processor should route any logs with a `log.level` of `WARN` or `ERROR` to the `logs-critical-default` data stream. Query the the data stream using the following command to verify the log data was routed as intended:

```console
GET logs-critical-default/_search
```

Your should see similar results to the following showing that the high-severity logs are now in the `critical` dataset:

```JSON
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
