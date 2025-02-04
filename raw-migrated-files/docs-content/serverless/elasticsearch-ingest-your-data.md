# Ingest your data [elasticsearch-ingest-your-data]

The best ingest option(s) for your use case depends on whether you are indexing general content or time series (timestamped) data.


## Ingest data using APIs [es-ingestion-overview-apis] 

You can use the [{{es}} REST APIs](../../../deploy-manage/deploy/elastic-cloud/tools-apis.md) to add data to your {{es}} indices, using any HTTP client, including the [{{es}} client libraries](../../../solutions/search/site-or-app/clients.md).

While the {{es}} APIs can be used for any data type, Elastic provides specialized tools that optimize ingestion for specific use cases.


## Ingest general content [es-ingestion-overview-general-content] 

General content is typically text-heavy data that does not have a timestamp. This could be data like knowledge bases, website content, product catalogs, and more.

You can use these specialized tools to add general content to {{es}} indices:

* [Connector clients](https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-integrations-connector-client.html)
* [Elastic Open Web Crawler](https://github.com/elastic/crawler)
* [File Uploader](../../../manage-data/ingest/tools/upload-data-files.md)


## Ingest time series data [elasticsearch-ingest-time-series-data] 

Time series, or timestamped data, describes data that changes frequently and "flows" over time, such as stock quotes, system metrics, and network traffic data.

::::{note} 
Time series data refers to any document in standard indices or data streams that includes the `@timestamp` field.

::::


You can use these specialized tools to add timestamped data to {{es}} data streams:

* [{{beats}}](https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-beats.html)
* [{{ls}}](https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-logstash.html)






