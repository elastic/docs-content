---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest/current/use-case-arch.html
---

# Ingest architectures [use-case-arch]

We offer a variety of ingest architectures to serve a wide range of use cases and network configurations.

To ingest data into {{es}}, use the *simplest option that meets your needs* and satisfies your use case. For many users and use cases, the simplest approach is ingesting data with {{agent}} and sending it to {{es}}. {{agent}} and [{{agent}} integrations](https://www.elastic.co/integrations/) are available for many popular platforms and services, and are a good place to start.

::::{tip}
You can host {{es}} on your own hardware or send your data to {{es}} on {{ecloud}}. For most users, {{agent}} writing directly to {{es}} on {{ecloud}} provides the easiest and fastest time to value. {ess-leadin-short}
::::


**Decision tree**

[Data ingestion](../../ingest.md)

| **Ingest architecture** | **Use when** |
| --- | --- |
| [*{{agent}} to Elasticsearch*](agent-to-es.md)<br><br>![Image showing {{agent}} collecting data and sending to {{es}}](../../../images/ingest-ea-es.png "") | An [{{agent}} integration](https://docs.elastic.co/en/integrations) is available for your data source:<br><br>* Software components with [{{agent}} installed](agent-installed.md)<br>* Software components using [APIs for data collection](agent-apis.md)<br> |
| [*{{agent}} to {{ls}} to Elasticsearch*](agent-ls.md)<br><br>![Image showing {{agent}} to {{ls}} to {{es}}](../../../images/ingest-ea-ls-es.png "") | You need additional capabilities offered by {{ls}}:<br><br>* [**enrichment**](ls-enrich.md) between {{agent}} and {{es}}<br>* [**persistent queue (PQ) buffering**](lspq.md) to accommodate network issues and downstream unavailability<br>* [**proxying**](ls-networkbridge.md) in cases where {{agent}}s have network restrictions for connecting outside of the {{agent}} network<br>* data needs to be [**routed to multiple**](ls-multi.md) {{es}} clusters and other destinations depending on the content<br> |
| [*{{agent}} to proxy to Elasticsearch*](agent-proxy.md)<br><br>![Image showing connections between {{agent}} and {{es}} using a proxy](../../../images/ingest-ea-proxy-es.png "") | Agents have [network restrictions](agent-proxy.md) that prevent connecting outside of the {{agent}} network Note that [{{ls}} as proxy](ls-networkbridge.md) is one option.<br> |
| [*{{agent}} to {{es}} with Kafka as middleware message queue*](agent-kafka-es.md)<br><br>![Image showing {{agent}} collecting data and using Kafka as a message queue enroute to {{es}}](../../../images/ingest-ea-kafka.png "") | Kafka is your [middleware message queue](agent-kafka-es.md):<br><br>* [Kafka ES sink connector](agent-kafka-essink.md) to write from Kafka to {{es}}<br>* [{{ls}} to read from Kafka and route to {{es}}](agent-kafka-ls.md)<br> |
| [*{{ls}} to Elasticsearch*](ls-for-input.md)<br><br>![Image showing {{ls}} collecting data and sending to {{es}}](../../../images/ingest-ls-es.png "") | You need to collect data from a source that {{agent}} can’t read (such as databases, AWS Kinesis). Check out the [{{ls}} input plugins](https://www.elastic.co/guide/en/logstash/current/input-plugins.html).<br> |
| [*Elastic air-gapped architectures*](airgapped-env.md)<br><br>![Image showing {{stack}} in an air-gapped environment](../../../images/ingest-ea-airgapped.png "") | You want to deploy {{agent}} and {{stack}} in an air-gapped environment (no access to outside networks)<br> |
