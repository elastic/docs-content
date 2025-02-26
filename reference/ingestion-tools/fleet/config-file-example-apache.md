---
navigation_title: "Apache HTTP Server"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/config-file-example-apache.html
---

# Config file example: Apache HTTP Server [config-file-example-apache]


Include these sample settings in your standalone {{agent}} `elastic-agent.yml` configuration file to ingest data from Apache HTTP server.

* [Apache HTTP Server logs](#config-file-example-apache-logs)
* [Apache HTTP Server metrics](#config-file-example-apache-metrics)

## Apache HTTP Server logs [config-file-example-apache-logs]

```yaml
outputs: <1>
  default:
    type: elasticsearch <2>
    hosts:
      - '{elasticsearch-host-url}' <3>
    api_key: "my_api_key" <4>
agent:
  download: <5>
    sourceURI: 'https://artifacts.elastic.co/downloads/'
  monitoring: <6>
    enabled: true
    use_output: default
    namespace: default
    logs: true
    metrics: true
inputs: <7>
  - id: "insert a unique identifier here" <8>
    name: apache-1
    type: logfile <9>
    use_output: default
    data_stream: <10>
      namespace: default
    streams:
      - id: "insert a unique identifier here" <11>
        data_stream:
          dataset: apache.access <12>
          type: logs
        paths: <13>
          - /var/log/apache2/access.log*
          - /var/log/apache2/other_vhosts_access.log*
          - /var/log/httpd/access_log*
        tags:
          - apache-access
        exclude_files:
          - .gz$
      - id: "insert a unique identifier here" <11>
        data_stream:
          dataset: apache.error <12>
          type: logs
        paths: <13>
          - /var/log/apache2/error.log*
          - /var/log/httpd/error_log*
        exclude_files:
          - .gz$
        tags:
          - apache-error
        processors:
          - add_locale: null
```

1. For available output settings, refer to [Configure outputs for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-output-configuration.md).
2. For settings specific to the {{es}} output, refer to [Configure the {{es}} output](/reference/ingestion-tools/fleet/elasticsearch-output.md).
3. The URL of the Elasticsearch cluster where output should be sent, including the port number. For example `https://12345ab6789cd12345ab6789cd.us-central1.gcp.cloud.es.io:443`.
4. An [API key](/reference/ingestion-tools/fleet/grant-access-to-elasticsearch.md#create-api-key-standalone-agent) used to authenticate with the {{es}} cluster.
5. For available download settings, refer to [Configure download settings for standalone Elastic Agent upgrades](/reference/ingestion-tools/fleet/elastic-agent-standalone-download.md).
6. For available monitoring settings, refer to [Configure monitoring for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-monitoring-configuration.md).
7. For available input settings, refer to [Configure inputs for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-input-configuration.md).
8. Specify a unique ID for the input.
9. For available input types, refer to [{{agent}} inputs](/reference/ingestion-tools/fleet/elastic-agent-inputs-list.md).
10. Learn about [Data streams](/reference/ingestion-tools/fleet/data-streams.md) for time series data.
11. Specify a unique ID for each individual input stream. Naming the ID by appending the associated `data_stream` dataset (for example `{{user-defined-unique-id}}-apache.access` or `{{user-defined-unique-id}}-apache.error`) is a recommended practice, but any unique ID will work.
12. Refer to [Logs](integration-docs://docs/reference/apache.md#apache-logs) in the Apache HTTP Server integration documentation for the logs available to ingest and exported fields.
13. Path to the log files to be monitored.



## Apache HTTP Server metrics [config-file-example-apache-metrics]

```yaml
outputs: <1>
  default:
    type: elasticsearch <2>
    hosts:
      - '{elasticsearch-host-url}' <3>
    api_key: "my_api_key" <4>
agent:
  download: <5>
    sourceURI: 'https://artifacts.elastic.co/downloads/'
  monitoring: <6>
    enabled: true
    use_output: default
    namespace: default
    logs: true
    metrics: true
inputs: <7>
    type: apache/metrics <8>
    use_output: default
    data_stream: <9>
      namespace: default
    streams:
      - id: "insert a unique identifier here" <10>
        data_stream: <8>
          dataset: apache.status <11>
          type: metrics
        metricsets: <12>
          - status
        hosts:
          - 'http://127.0.0.1'
        period: 30s
        server_status_path: /server-status
```

1. For available output settings, refer to [Configure outputs for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-output-configuration.md).
2. For settings specific to the {{es}} output, refer to [Configure the {{es}} output](/reference/ingestion-tools/fleet/elasticsearch-output.md).
3. The URL of the Elasticsearch cluster where output should be sent, including the port number. For example `https://12345ab6789cd12345ab6789cd.us-central1.gcp.cloud.es.io:443`.
4. An [API key](/reference/ingestion-tools/fleet/grant-access-to-elasticsearch.md#create-api-key-standalone-agent) used to authenticate with the {{es}} cluster.
5. For available download settings, refer to [Configure download settings for standalone Elastic Agent upgrades](/reference/ingestion-tools/fleet/elastic-agent-standalone-download.md).
6. For available monitoring settings, refer to [Configure monitoring for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-monitoring-configuration.md).
7. For available input settings, refer to [Configure inputs for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-input-configuration.md).
8. For available input types, refer to [{{agent}} inputs](/reference/ingestion-tools/fleet/elastic-agent-inputs-list.md).
9. Learn about [Data streams](/reference/ingestion-tools/fleet/data-streams.md) for time series data.
10. Specify a unique ID for each individual input stream. Naming the ID by appending the associated `data_stream` dataset (for example `{{user-defined-unique-id}}-apache.status`) is a recommended practice, but any unique ID will work.
11. A user-defined dataset. You can specify anything that makes sense to signify the source of the data.
12. Refer to [Metrics](integration-docs://docs/reference/apache.md#apache-metrics) in the Apache HTTP Server integration documentation for the type of metrics collected and exported fields.



