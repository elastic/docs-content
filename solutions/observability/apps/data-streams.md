---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-data-streams.html
---

# Data streams [apm-data-streams]

::::{note}
{{agent}} uses data streams to store append-only time series data across multiple indices. Data streams are well-suited for logs, metrics, traces, and other continuously generated data, and offer a host of benefits over other indexing strategies:

* Reduced number of fields per index
* More granular data control
* Flexible naming scheme
* Fewer ingest permissions required

See the [{{fleet}} and {{agent}} Guide](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/data-streams.md) to learn more.

::::



## Data stream naming scheme [apm-data-streams-naming-scheme]

APM data follows the `<type>-<dataset>-<namespace>` naming scheme. The `type` and `dataset` are predefined by the {{es}} apm-data plugin, but the `namespace` is your opportunity to customize how different types of data are stored in {{es}}. There is no recommendation for what to use as your namespace—​it is intentionally flexible. For example, you might create namespaces for each of your environments, like `dev`, `prod`, `production`, etc. Or, you might create namespaces that correspond to strategic business units within your organization.


## APM data streams [apm-data-streams-list]

By type, the APM data streams are:

Traces
:   Traces are comprised of [spans and transactions](learn-about-application-data-types.md). Traces are stored in the following data streams:

    * Application traces: `traces-apm-<namespace>`
    * RUM and iOS agent application traces: `traces-apm.rum-<namespace>`


Metrics
:   Metrics include application-based metrics, aggregation metrics, and basic system metrics. Metrics are stored in the following data streams:

    * APM internal metrics: `metrics-apm.internal-<namespace>`
    * APM transaction metrics: `metrics-apm.transaction.<metricset.interval>-<namespace>`
    * APM service destination metrics: `metrics-apm.service_destination.<metricset.interval>-<namespace>`
    * APM service transaction metrics: `metrics-apm.service_transaction.<metricset.interval>-<namespace>`
    * APM service summary metrics: `metrics-apm.service_summary.<metricset.interval>-<namespace>`
    * Application metrics: `metrics-apm.app.<service.name>-<namespace>`

        Application metrics include the instrumented service’s name—​defined in each {{apm-agent}}'s configuration—​in the data stream name. Service names therefore must follow certain index naming rules.

        ::::{dropdown} Service name rules
        * Service names are case-insensitive and must be unique. For example, you cannot have a service named `Foo` and another named `foo`.
        * Special characters will be removed from service names and replaced with underscores (`_`). Special characters include:

            ```text
            '\\', '/', '*', '?', '"', '<', '>', '|', ' ', ',', '#', ':', '-'
            ```


        ::::


        ::::{important}
        Additional storage efficiencies provided by [Synthetic `_source`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/mapping-reference/mapping-source-field.md) are available to users with an [appropriate license](https://www.elastic.co/subscriptions).

        ::::


Logs
:   Logs include application error events and application logs. Logs are stored in the following data streams:

    * APM error/exception logging: `logs-apm.error-<namespace>`
    * Applications UI logging: `logs-apm.app.<service.name>-<namespace>`



## APM data stream rerouting [apm-data-stream-rerouting]

APM supports rerouting APM data to user-defined APM data stream names other than the defaults. This can be achieved by using a [`reroute` processor](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/enrich-processor/reroute-processor.md) in ingest pipelines to set the data stream dataset or namespace. The benefit of separating APM data streams is that custom retention and security policies can be used.

For example, consider traces that would originally be indexed to `traces-apm-default`. To set the data stream namespace from the trace’s `service.environment` and fallback to a static string `"default"`, create an ingest pipeline named `traces-apm@custom` which will be used automatically:

```json
[
  {
    "reroute": {
      "namespace": [
        "{{service.environment}}",
        "default"
      ]
    }
  }
]
```

To find other ingest pipelines from the {{es}} apm-data plugin that are called by default, go to **Stack management** → **Ingest pipelines** [in Kibana](../../../deploy-manage/index.md) and search for `apm`. Default APM ingest pipelines will follow the pattern `*-apm*@default-pipeline`.

For more custom APM ingest pipeline guides, see [parse data using ingest pipelines](parse-data-using-ingest-pipelines.md).


## What’s next? [apm-data-streams-next]

* Data streams define not only how data is stored in {{es}}, but also how data is retained over time. See [{{ilm-cap}}](index-lifecycle-management.md) to learn how to create your own data retention policies.
* See [Manage storage](manage-storage.md) for information on APM storage and processing costs, processing and performance, and other index management features.

