# Add data to {{es}} [es-ingestion-overview]

There are multiple ways to ingest data into {{es}}. The option that you choose depends on whether you’re working with timestamped data or non-timestamped data, where the data is coming from, its complexity, and more.

::::{tip}
You can load [sample data](../../../manage-data/ingest.md#_add_sample_data) into your {{es}} cluster using {{kib}}, to get started quickly.

::::



## General content [es-ingestion-overview-general-content]

General content is data that does not have a timestamp. This could be data like vector embeddings, website content, product catalogs, and more. For general content, you have the following options for adding data to {{es}} indices:

* [API](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html): Use the {{es}} [Document APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html) to index documents directly, using the Dev Tools [Console](../../../explore-analyze/query-filter/tools/console.md), or cURL.

    If you’re building a website or app, then you can call Elasticsearch APIs using an [{{es}} client](https://www.elastic.co/guide/en/elasticsearch/client/index.html) in the programming language of your choice. If you use the Python client, then check out the `elasticsearch-labs` repo for various [example notebooks](https://github.com/elastic/elasticsearch-labs/tree/main/notebooks/search/python-examples).

* [File upload](../../../manage-data/ingest.md#upload-data-kibana): Use the {{kib}} file uploader to index single files for one-off testing and exploration. The GUI guides you through setting up your index and field mappings.
* [Web crawler](https://github.com/elastic/crawler): Extract and index web page content into {{es}} documents.
* [Connectors](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors.html): Sync data from various third-party data sources to create searchable, read-only replicas in {{es}}.


## Timestamped data [es-ingestion-overview-timestamped]

Timestamped data in {{es}} refers to datasets that include a timestamp field. If you use the [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/{{ecs_version}}/ecs-reference.html), this field is named `@timestamp`. This could be data like logs, metrics, and traces.

For timestamped data, you have the following options for adding data to {{es}} data streams:

* [Elastic Agent and Fleet](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html): The preferred way to index timestamped data. Each Elastic Agent based integration includes default ingestion rules, dashboards, and visualizations to start analyzing your data right away. You can use the Fleet UI in {{kib}} to centrally manage Elastic Agents and their policies.
* [Beats](https://www.elastic.co/guide/en/beats/libbeat/current/beats-reference.html): If your data source isn’t supported by Elastic Agent, use Beats to collect and ship data to Elasticsearch. You install a separate Beat for each type of data to collect.
* [Logstash](https://www.elastic.co/guide/en/logstash/current/introduction.html): Logstash is an open source data collection engine with real-time pipelining capabilities that supports a wide variety of data sources. You might use this option because neither Elastic Agent nor Beats supports your data source. You can also use Logstash to persist incoming data, or if you need to send the data to multiple destinations.
* [Language clients](../../../manage-data/ingest/ingesting-data-from-applications.md): The linked tutorials demonstrate how to use {{es}} programming language clients to ingest data from an application. In these examples, {{es}} is running on Elastic Cloud, but the same principles apply to any {{es}} deployment.

::::{tip}
If you’re interested in data ingestion pipelines for timestamped data, use the decision tree in the [Elastic Cloud docs](../../../manage-data/ingest.md#ec-data-ingest-pipeline) to understand your options.

::::


