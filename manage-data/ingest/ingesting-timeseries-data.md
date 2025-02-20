---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest-overview/current/ingest-tools.html
---

# Ingesting time series data [ingest-tools]

Elastic and others offer tools to help you get your data from the original data source into {{es}}. Some tools are designed for particular data sources, and others are multi-purpose.

In this section, we’ll help you determine which option is best for you.

* [{{agent}} and Elastic integrations](/manage-data/ingest/ingesting-timeseries-data.md#ingest-ea)
* [{{beats}}](/manage-data/ingest/ingesting-timeseries-data.md#ingest-beats)
* [OpenTelemetry (OTel) collectors](/manage-data/ingest/ingesting-timeseries-data.md#ingest-otel)
* [Logstash](/manage-data/ingest/ingesting-timeseries-data.md#ingest-logstash)


## {{agent}} and Elastic integrations [ingest-ea]

A single [{{agent}}](https://www.elastic.co/guide/en/fleet/current) can collect multiple types of data when it is [installed](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/install-elastic-agents.md) on a host computer. You can use standalone {{agent}}s and manage them locally on the systems where they are installed, or you can manage all of your agents and policies with the [Fleet UI in {{kib}}](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/manage-elastic-agents-in-fleet.md).

Use {{agent}} with one of hundreds of [Elastic integrations](https://docs.elastic.co/en/integrations) to simplify collecting, transforming, and visualizing data. Integrations include default ingestion rules, dashboards, and visualizations to help you start analyzing your data right away. Check out the [Integration quick reference](https://docs.elastic.co/en/integrations/all_integrations) to search for available integrations that can reduce your time to value.

{{agent}} is the best option for collecting timestamped data for most data sources and use cases. If your data requires additional processing before going to {{es}}, you can use [{{agent}} processors](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/agent-processors.md), [{{ls}}](https://www.elastic.co/guide/en/logstash/current), or additional processing features in {{es}}. Check out [additional processing](/manage-data/ingest/transform-enrich.md) to see options.

Ready to try [{{agent}}](https://www.elastic.co/guide/en/fleet/current)? Check out the [installation instructions](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/install-elastic-agents.md).


## {{beats}} [ingest-beats]

[Beats](asciidocalypse://docs/beats/docs/reference/ingestion-tools/index.md) are the original Elastic lightweight data shippers, and their capabilities live on in Elastic Agent. When you use Elastic Agent, you’re getting core Beats functionality, but with more added features.

Beats require that you install a separate Beat for each type of data you want to collect. A single Elastic Agent installed on a host can collect and transport multiple types of data.

**Best practice:** Use [{{agent}}](https://www.elastic.co/guide/en/fleet/current) whenever possible. If your data source is not yet supported by {{agent}}, use {{beats}}. Check out the {{beats}} and {{agent}} [comparison](/manage-data/ingest/tools.md#additional-capabilities-beats-and-agent) for more info. When you are ready to upgrade, check out [Migrate from {{beats}} to {{agent}}](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/migrate-from-beats-to-elastic-agent.md).


## OpenTelemetry (OTel) collectors [ingest-otel]

[OpenTelemetry](https://opentelemetry.io/docs) is a vendor-neutral observability framework for collecting, processing, and exporting telemetry data. Elastic is a member of the Cloud Native Computing Foundation (CNCF) and active contributor to the OpenTelemetry project.

In addition to supporting upstream OTel development, Elastic provides [Elastic Distributions of OpenTelemetry](https://github.com/elastic/opentelemetry), specifically designed to work with Elastic Observability. We’re also expanding [{{agent}}](https://www.elastic.co/guide/en/fleet/current) to use OTel collection.


## Logstash [ingest-logstash]

[{{ls}}](https://www.elastic.co/guide/en/logstash/current) is a versatile open source data ETL (extract, transform, load) engine that can expand your ingest capabilities. {{ls}} can *collect data* from a wide variety of data sources with {{ls}} [input plugins](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/input-plugins.md), *enrich and transform* the data with {{ls}} [filter plugins](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/filter-plugins.md), and *output* the data to {{es}} and other destinations with the {{ls}} [output plugins](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/output-plugins.md).

Many users never need to use {{ls}}, but it’s available if you need it for:

* **Data collection** (if an Elastic integration isn’t available). {{agent}} and Elastic [integrations](https://docs.elastic.co/en/integrations/all_integrations) provide many features out-of-the-box, so be sure to search or browse integrations for your data source. If you don’t find an Elastic integration for your data source, check {{ls}} for an [input plugin](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/input-plugins.md) for your data source.
* **Additional processing.** One of the most common {{ls}} use cases is [extending Elastic integrations](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/using-logstash-with-elastic-integrations.md). You can take advantage of the extensive, built-in capabilities of Elastic Agent and Elastic Integrations, and then use {{ls}} for additional data processing before sending the data on to {{es}}.
* **Advanced use cases.** {{ls}} can help with advanced use cases, such as when you need [persistence or buffering](/manage-data/ingest/ingest-reference-architectures/lspq.md), additional [data enrichment](/manage-data/ingest/ingest-reference-architectures/ls-enrich.md), [proxying](/manage-data/ingest/ingest-reference-architectures/ls-networkbridge.md) as a way to bridge network connections, or the ability to route data to [multiple destinations](/manage-data/ingest/ingest-reference-architectures/ls-multi.md).
