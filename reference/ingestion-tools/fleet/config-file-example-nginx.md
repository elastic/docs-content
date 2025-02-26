---
navigation_title: "Nginx HTTP Server"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/config-file-example-nginx.html
---

# Config file example: Nginx HTTP Server [config-file-example-nginx]


Include these sample settings in your standalone {{agent}} `elastic-agent.yml` configuration file to ingest data from Nginx HTTP Server.

* [Nginx HTTP Server logs](#config-file-example-nginx-logs)
* [Nginx HTTP Server metrics](#config-file-example-nginx-metrics)

## Nginx HTTP Server logs [config-file-example-nginx-logs]

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
    name: nginx-1
    type: logfile <9>
    use_output: default
    data_stream: <10>
      namespace: default
    streams:
      - id: "insert a unique identifier here" <11>
        data_stream:
          dataset: nginx.access <12>
          type: logs
        ignore_older: 72h
        paths: <13>
          - /var/log/nginx/access.log*
        tags:
          - nginx-access
        exclude_files:
          - .gz$
        processors:
          - add_locale: null
      - id: "insert a unique identifier here" <11>
        data_stream:
          dataset: nginx.error <12>
          type: logs
        ignore_older: 72h
        paths: <13>
          - /var/log/nginx/error.log*
        tags:
          - nginx-error
        exclude_files:
          - .gz$
        multiline:
          pattern: '^\d{4}\/\d{2}\/\d{2} '
          negate: true
          match: after
        processors:
          - add_locale: null
```

1. For available output settings, refer to [Configure outputs for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-output-configuration.md).
2. For settings specific to the {{es}} output, refer to [Configure the {{es}} output](/reference/ingestion-tools/fleet/elasticsearch-output.md).
3. The URL of the {{es}} cluster where output should be sent, including the port number. For example `https://12345ab6789cd12345ab6789cd.us-central1.gcp.cloud.es.io:443`.
4. An [API key](/reference/ingestion-tools/fleet/grant-access-to-elasticsearch.md#create-api-key-standalone-agent) used to authenticate with the {{es}} cluster.
5. For available download settings, refer to [Configure download settings for standalone Elastic Agent upgrades](/reference/ingestion-tools/fleet/elastic-agent-standalone-download.md).
6. For available monitoring settings, refer to [Configure monitoring for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-monitoring-configuration.md).
7. For available input settings, refer to [Configure inputs for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-input-configuration.md).
8. A user-defined ID to uniquely identify the input stream.
9. For available input types, refer to [{{agent}} inputs](/reference/ingestion-tools/fleet/elastic-agent-inputs-list.md).
10. Learn about [Data streams](/reference/ingestion-tools/fleet/data-streams.md) for time series data.
11. Specify a unique ID for each individual input stream. Naming the ID by appending the associated `data_stream` dataset (for example `{{user-defined-unique-id}}-nginx.access` or `{{user-defined-unique-id}}-nginx.error`) is a recommended practice, but any unique ID will work.
12. Refer to [Logs reference](integration-docs://docs/reference/nginx.md#nginx-logs-reference) in the Nginx HTTP integration documentation for the logs available to ingest and exported fields.
13. Path to the log files to be monitored.



### Nginx HTTP Server metrics [config-file-example-nginx-metrics]

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
    type: nginx/metrics <9>
    use_output: default
    data_stream: <10>
      namespace: default
    streams:
      - id: "insert a unique identifier here" <11>
        data_stream: <10>
          dataset: nginx.stubstatus <12>
          type: metrics
        metricsets: <13>
          - stubstatus
        hosts:
          - 'http://127.0.0.1:80'
        period: 10s
        server_status_path: /nginx_status
```

1. For available output settings, refer to [Configure outputs for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-output-configuration.md).
2. For settings specific to the {{es}} output, refer to [Configure the {{es}} output](/reference/ingestion-tools/fleet/elasticsearch-output.md).
3. The URL of the Elasticsearch cluster where output should be sent, including the port number. For example `https://12345ab6789cd12345ab6789cd.us-central1.gcp.cloud.es.io:443`.
4. An [API key](/reference/ingestion-tools/fleet/grant-access-to-elasticsearch.md#create-api-key-standalone-agent) used to authenticate with the {{es}} cluster.
5. For available download settings, refer to [Configure download settings for standalone Elastic Agent upgrades](/reference/ingestion-tools/fleet/elastic-agent-standalone-download.md).
6. For available monitoring settings, refer to [Configure monitoring for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-monitoring-configuration.md).
7. For available input settings, refer to [Configure inputs for standalone {{agents}}](/reference/ingestion-tools/fleet/elastic-agent-input-configuration.md).
8. A user-defined ID to uniquely identify the input stream.
9. For available input types, refer to [{{agent}} inputs](/reference/ingestion-tools/fleet/elastic-agent-inputs-list.md).
10. Learn about [Data streams](/reference/ingestion-tools/fleet/data-streams.md) for time series data.
11. Specify a unique ID for each individual input stream. Naming the ID by appending the associated `data_stream` dataset (for example `{{user-defined-unique-id}}-nginx.stubstatus`) is a recommended practice, but any unique ID will work.
12. A user-defined dataset. You can specify anything that makes sense to signify the source of the data.
13. Refer to [Metrics reference](integration-docs://docs/reference/nginx.md#nginx-metrics-reference) in the Nginx integration documentation for the type of metrics collected and exported fields.



