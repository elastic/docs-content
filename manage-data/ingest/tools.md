---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-cloud-ingest-data.html
  - https://www.elastic.co/guide/en/fleet/current/beats-agent-comparison.html
  - https://www.elastic.co/guide/en/kibana/current/connect-to-elasticsearch.html
  - https://www.elastic.co/guide/en/serverless/current/project-setting-data.html
  - https://www.elastic.co/customer-success/data-ingestion
  - https://github.com/elastic/ingest-docs/pull/1373
---

# Ingest tools overview

Depending on the type of data you want to ingest, you have a number of methods and tools available for use in your ingestion process. The table below provides more information about the available tools. Refer to our [Ingestion](/manage-data/ingest.md) overview for some guidelines to help you select the optimal tool for your use case.

<br>

| Tools   | Usage           | Links to more information |
| ------- | --------------- | ------------------------- |
| Integrations | Ingest data using a variety of Elastic integrations. | [Elastic Integrations](asciidocalypse://docs/integration-docs/docs/reference/ingestion-tools/index.md) |
| File upload | Upload data from a file and inspect it before importing it into {{es}}. | [Upload data files](/manage-data/ingest/upload-data-files.md) |
| APIs  | Ingest data through code by using the APIs of one of the language clients or the {{es}} HTTP APIs. | [Document APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-document) |
| OpenTelemetry | Collect and send your telemetry data to Elastic Observability | [Elastic Distributions of OpenTelemetry](https://github.com/elastic/opentelemetry?tab=readme-ov-file#elastic-distributions-of-opentelemetry) |
| Fleet and Elastic Agent | Add monitoring for logs, metrics, and other types of data to a host using Elastic Agent, and centrally manage it using Fleet. | [Fleet and {{agent}} overview](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/index.md) <br> [{{fleet}} and {{agent}} restrictions (Serverless)](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/fleet-agent-serverless-restrictions.md) <br> [{{beats}} and {{agent}} capabilities](/manage-data/ingest/tools.md)||
| {{elastic-defend}} | {{elastic-defend}} provides organizations with prevention, detection, and response capabilities with deep visibility for EPP, EDR, SIEM, and Security Analytics use cases across Windows, macOS, and Linux operating systems running on both traditional endpoints and public cloud environments. | [Configure endpoint protection with {{elastic-defend}}](/solutions/security/configure-elastic-defend.md) |
| {{ls}} | Dynamically unify data from a wide variety of data sources and normalize it into destinations of your choice with {{ls}}. | [Logstash (Serverless)](asciidocalypse://docs/logstash/docs/reference/ingestion-tools/logstash/index.md) <br> [Logstash pipelines](/manage-data/ingest/transform-enrich/logstash-pipelines.md) |
| {{beats}} | Use {{beats}} data shippers to send operational data to Elasticsearch directly or through Logstash. | [{{beats}} (Serverless)](asciidocalypse://docs/beats/docs/reference/ingestion-tools/index.md) <br> [What are {{beats}}?](asciidocalypse://docs/beats/docs/reference/ingestion-tools/index.md) <br> [{{beats}} and {{agent}} capabilities](/manage-data/ingest/tools.md)|
| APM | Collect detailed performance information on response time for incoming requests, database queries, calls to caches, external HTTP requests, and more. | [Application performance monitoring (APM)](/solutions/observability/apps/application-performance-monitoring-apm.md) |
| Application logs | Ingest application logs using Filebeat, {{agent}}, or the APM agent, or reformat application logs into Elastic Common Schema (ECS) logs and then ingest them using Filebeat or {{agent}}.  | [Stream application logs](/solutions/observability/logs/stream-application-logs.md) <br> [ECS formatted application logs](/solutions/observability/logs/ecs-formatted-application-logs.md) |
| Elastic Serverless forwarder for AWS | Ship logs from your AWS environment to cloud-hosted, self-managed Elastic environments, or {{ls}}. | [Elastic Serverless Forwarder](asciidocalypse://docs/elastic-serverless-forwarder/docs/reference/ingestion-tools/esf/index.md) |
| Connectors | Use connectors to extract data from an original data source and sync it to an {{es}} index. | [Ingest content with Elastic connectors
](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/search-connectors/index.md) <br> [Connector clients](asciidocalypse://docs/elasticsearch/docs/reference/ingestion-tools/search-connectors/index.md) |
| Web crawler | Discover, extract, and index searchable content from websites and knowledge bases using the web crawler. | [Elastic Open Web Crawler](https://github.com/elastic/crawler#readme) |