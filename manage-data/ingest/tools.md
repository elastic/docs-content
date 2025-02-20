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

% What needs to be done: Finish draft

% GitHub issue: docs-projects#327

% Scope notes: Read more about the scope in the tracking issue

% Use migrated content from existing pages that map to this page:

% - [x] ./raw-migrated-files/cloud/cloud/ec-cloud-ingest-data.md
%      Notes: These are resources to pull from, but this new "Ingest tools overiew" page will not be a replacement for any of these old AsciiDoc pages.  File upload: https://www.elastic.co/guide/en/kibana/current/connect-to-elasticsearch.html#upload-data-kibana https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-file-upload.html API: https://www.elastic.co/guide/en/kibana/current/connect-to-elasticsearch.html#_add_data_with_programming_languages https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-api.html OpenTelemetry: https://github.com/elastic/opentelemetry Fleet and Agent: https://www.elastic.co/guide/en/fleet/current/fleet-overview.html https://www.elastic.co/guide/en/serverless/current/fleet-and-elastic-agent.html Logstash: https://www.elastic.co/guide/en/logstash/current/introduction.html https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-logstash.html https://www.elastic.co/guide/en/serverless/current/logstash-pipelines.html Beats: https://www.elastic.co/guide/en/beats/libbeat/current/beats-reference.html https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-beats.html APM: /solutions/observability/apps/application-performance-monitoring-apm.md Application logging: https://www.elastic.co/guide/en/observability/current/application-logs.html ECS logging: https://www.elastic.co/guide/en/observability/current/logs-ecs-application.html Elastic serverless forwarder for AWS: https://www.elastic.co/guide/en/esf/current/aws-elastic-serverless-forwarder.html Integrations: https://www.elastic.co/guide/en/integrations/current/introduction.html Search connectors: https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors.html https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-integrations-connector-client.html Web crawler: https://github.com/elastic/crawler/tree/main/docs
% - [This comparison page is being moved to the reference section, so I'm linking to that from the current page - Wajiha] ./raw-migrated-files/ingest-docs/fleet/beats-agent-comparison.md
% - [x] ./raw-migrated-files/kibana/kibana/connect-to-elasticsearch.md
% - [x] https://www.elastic.co/customer-success/data-ingestion
% - [x] https://github.com/elastic/ingest-docs/pull/1373

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc): 
% These IDs are from content that I'm not including on this current page. I've resolved them by changing the internal links to anchor links where needed. - Wajiha

$$$supported-outputs-beats-and-agent$$$

$$$additional-capabilities-beats-and-agent$$$

Depending on the type of data you want to ingest, you have a number of methods and tools available for use in your ingestion process. The table below provides more information about the available tools. Refer to our [Ingestion](/manage-data/ingest.md) overview for some guidelines to help you select the optimal tool for your use case.

<br>

| Tools   | Usage           | Links to more information |
| ------- | --------------- | ------------------------- |
| Integrations | Ingest data using a variety of Elastic integrations. | [Elastic Integrations](https://www.elastic.co/guide/en/integrations/current/index.html) |
| File upload | Upload data from a file and inspect it before importing it into {{es}}. | [Upload data files](/manage-data/ingest/upload-data-files.md) |
| APIs  | Ingest data through code by using the APIs of one of the language clients or the {{es}} HTTP APIs. | [Document APIs](https://www.elastic.co/guide/en/elasticsearch/reference/current/docs.html) |
| OpenTelemetry | Collect and send your telemetry data to Elastic Observability | [Elastic Distributions of OpenTelemetry](https://github.com/elastic/opentelemetry?tab=readme-ov-file#elastic-distributions-of-opentelemetry) |
| Fleet and Elastic Agent | Add monitoring for logs, metrics, and other types of data to a host using Elastic Agent, and centrally manage it using Fleet. | [Fleet and {{agent}} overview](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html) <br> [{{fleet}} and {{agent}} restrictions (Serverless)](https://www.elastic.co/guide/en/fleet/current/fleet-agent-serverless-restrictions.html) <br> [{{beats}} and {{agent}} capabilities](https://www.elastic.co/guide/en/fleet/current/beats-agent-comparison.html)||
| {{elastic-defend}} | {{elastic-defend}} provides organizations with prevention, detection, and response capabilities with deep visibility for EPP, EDR, SIEM, and Security Analytics use cases across Windows, macOS, and Linux operating systems running on both traditional endpoints and public cloud environments. | [Configure endpoint protection with {{elastic-defend}}](/solutions/security/configure-elastic-defend.md) |
| {{ls}} | Dynamically unify data from a wide variety of data sources and normalize it into destinations of your choice with {{ls}}. | [Logstash (Serverless)](https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-logstash.html) <br> [Logstash pipelines](/manage-data/ingest/transform-enrich/logstash-pipelines.md) |
| {{beats}} | Use {{beats}} data shippers to send operational data to Elasticsearch directly or through Logstash. | [{{beats}} (Serverless)](https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-beats.html) <br> [What are {{beats}}?](https://www.elastic.co/guide/en/beats/libbeat/current/beats-reference.html) <br> [{{beats}} and {{agent}} capabilities](https://www.elastic.co/guide/en/fleet/current/beats-agent-comparison.html)|
| APM | Collect detailed performance information on response time for incoming requests, database queries, calls to caches, external HTTP requests, and more. | [Application performance monitoring (APM)](/solutions/observability/apps/application-performance-monitoring-apm.md) |
| Application logs | Ingest application logs using Filebeat, {{agent}}, or the APM agent, or reformat application logs into Elastic Common Schema (ECS) logs and then ingest them using Filebeat or {{agent}}.  | [Stream application logs](/solutions/observability/logs/stream-application-logs.md) <br> [ECS formatted application logs](/solutions/observability/logs/ecs-formatted-application-logs.md) |
| Elastic Serverless forwarder for AWS | Ship logs from your AWS environment to cloud-hosted, self-managed Elastic environments, or {{ls}}. | [Elastic Serverless Forwarder](https://www.elastic.co/guide/en/esf/current/aws-elastic-serverless-forwarder.html) |
| Connectors | Use connectors to extract data from an original data source and sync it to an {{es}} index. | [Ingest content with Elastic connectors
](https://www.elastic.co/guide/en/elasticsearch/reference/current/es-connectors.html) <br> [Connector clients](https://www.elastic.co/guide/en/serverless/current/elasticsearch-ingest-data-through-integrations-connector-client.html) |
| Web crawler | Discover, extract, and index searchable content from websites and knowledge bases using the web crawler. | [Elastic Open Web Crawler](https://github.com/elastic/crawler#readme) |