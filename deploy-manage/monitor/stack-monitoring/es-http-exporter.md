---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/http-exporter.html
applies:
  stack: deprecated 7.16.0
---

# HTTP exporters [http-exporter]

::::{important} 
{{agent}} and {{metricbeat}} are the recommended methods for collecting and shipping monitoring data to a monitoring cluster.

If you have previously configured legacy collection methods, you should migrate to using [{{agent}}](collecting-monitoring-data-with-elastic-agent.md) or [{{metricbeat}}](collecting-monitoring-data-with-metricbeat.md) collection. Do not use legacy collection alongside other collection methods.

::::


The `http` exporter is the preferred exporter in the {{es}} {{monitor-features}} because it enables the use of a separate monitoring cluster. As a secondary benefit, it avoids using a production cluster node as a coordinating node for indexing monitoring data because all requests are HTTP requests to the monitoring cluster.

The `http` exporter uses the low-level {{es}} REST Client, which enables it to send its data to any {{es}} cluster it can access through the network. Its requests make use of the [`filter_path`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/common-options.md#common-options-response-filtering) parameter to reduce bandwidth whenever possible, which helps to ensure that communications between the production and monitoring clusters are as lightweight as possible.

The `http` exporter supports a number of settings that control how it communicates over HTTP to remote clusters. In most cases, it is not necessary to explicitly configure these settings. For detailed descriptions, see [Monitoring settings](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/monitoring-settings.md).

```yaml
xpack.monitoring.exporters:
  my_local: <1>
    type: local
  my_remote: <2>
    type: http
    host: [ "10.1.2.3:9200", ... ] <3>
    auth: <4>
      username: my_username
      # "xpack.monitoring.exporters.my_remote.auth.secure_password" must be set in the keystore
    connection:
      timeout: 6s
      read_timeout: 60s
    ssl: ... <5>
    proxy:
      base_path: /some/base/path <6>
    headers: <7>
      My-Proxy-Header: abc123
      My-Other-Thing: [ def456, ... ]
    index.name.time_format: YYYY-MM <8>
```

1. A `local` exporter defined explicitly whose arbitrary name is `my_local`.
2. An `http` exporter defined whose arbitrary name is `my_remote`. This name uniquely defines the exporter but is otherwise unused.
3. `host` is a required setting for `http` exporters. It must specify the HTTP port rather than the transport port. The default port value is `9200`.
4. User authentication for those using {{stack}} {{security-features}} or some other form of user authentication protecting the cluster.
5. See [HTTP exporter settings](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/monitoring-settings.md#http-exporter-settings) for all TLS/SSL settings. If not supplied, the default node-level TLS/SSL settings are used.
6. Optional base path to prefix any outgoing request with in order to work with proxies.
7. Arbitrary key/value pairs to define as headers to send with every request. The array-based key/value format sends one header per value.
8. A mechanism for changing the date suffix used by default.


::::{note} 
The `http` exporter accepts an array of `hosts` and it will round robin through the list. It is a good idea to take advantage of that feature when the monitoring cluster contains more than one node.
::::


Unlike the `local` exporter, *every* node that uses the `http` exporter attempts to check and create the resources that it needs. The `http` exporter avoids re-checking the resources unless something triggers it to perform the checks again. These triggers include:

* The production cluster’s node restarts.
* A connection failure to the monitoring cluster.
* The license on the production cluster changes.
* The `http` exporter is dynamically updated (and it is therefore replaced).

The easiest way to trigger a check is to disable, then re-enable the exporter.

::::{warning} 
This resource management behavior can create a hole for users that delete monitoring resources. Since the `http` exporter does not re-check its resources unless one of the triggers occurs, this can result in malformed index mappings.
::::


Unlike the `local` exporter, the `http` exporter is inherently routing requests outside of the cluster. This situation means that the exporter must provide a username and password when the monitoring cluster requires one (or other appropriate security configurations, such as TLS/SSL settings).

::::{important} 
When discussing security relative to the `http` exporter, it is critical to remember that all users are managed on the monitoring cluster. This is particularly important to remember when you move from development environments to production environments, where you often have dedicated monitoring clusters.
::::


For more information about the configuration options for the `http` exporter, see [HTTP exporter settings](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/configuration-reference/monitoring-settings.md#http-exporter-settings).

