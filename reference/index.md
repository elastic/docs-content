---
mapped_pages:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/api-reference.html
products:
  - id: elastic-stack
description: Explore reference documentation for the Elastic Stack including APIs,
  security schemas, configuration settings, query languages, scripting, ECS field
  references, and more.
---

# Reference [api-reference]

Explore the reference documentation for the Elastic Stack. Whether you are configuring security protocols, enhancing search functionalities, or integrating with cloud services, our detailed manuals, API guides, and configuration settings provide the information you need.

## APIs
Explore the reference documentation for [Elastic APIs]({{apis}}).

|     |     |
| --- | --- |
| {{es}} | • [{{es}}]({{es-apis}})<br>• [{{es-serverless}}]({{es-serverless-apis}})<br> |
| {{kib}}<br>({{observability}}, {{elastic-sec}}, {{apm-agent}}, {{fleet}}, and more features) | • [{{kib}}]({{kib-apis}})<br>• [{{kib}} Serverless]({{kib-serverless-apis}})<br> |
| {{ls}} | • [{{ls}}]({{ls-apis}})<br> |
| APM | • [APM Server](/solutions/observability/apm/apm-server/api.md)<br>• [Observability intake Serverless]({{intake-apis}})<br> |
| {{ecloud}} | • [{{ech}}]({{cloud-apis}})<br>• [{{ecloud}} Serverless]({{cloud-serverless-apis}})<br>• [{{ece}}]({{ece-apis}})<br>• [{{eck}}](cloud-on-k8s://reference/api-docs.md)<br>• [{{ecloud}} billing]({{cloud-billing-apis}})<br> |

## Solutions, Platform, Deploy

Find the relevant documentation for Elastic solutions, platform components, and deployment options.


::::{tab-set}

:::{tab-item} Solutions

|     |     |
| --- | --- |
| [**Get started with {{es}}**](/solutions/search/get-started.md) | [Reference docs](elasticsearch://reference/elasticsearch/index.md) |
| [**Get started with Observability**](/solutions/observability/get-started.md) | [Reference docs](observability/index.md) |
| [**Get started with Security**](/solutions/security/get-started.md) | [Reference docs](security/index.md) |

:::

:::{tab-item} Platform

|     |     |
| --- | --- |
| [{{es}}](elasticsearch://reference/elasticsearch/index.md) | The core distributed search and analytics engine at the heart of the Elastic platform. |
| [{{ls}}](logstash://reference/index.md) | A data collection engine with real-time pipelining capabilities. |
| [{{kib}}](kibana://reference/index.md) | Visualize and analyze your data with Kibana, the extensible user interface of the Elastic platform. |
| [Fleet and Elastic Agent](/reference/fleet/index.md) | A unified method to collect logs, metrics, and security data. |
| [Beats](beats://reference/index.md) | Lightweight data shippers that send data to your cluster. |

:::

:::{tab-item} Deploy

|     |     |
| --- | --- |
| [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md) | {{serverless-full}} is a fully managed solution that allows you to deploy and use Elastic for your use cases without managing the underlying infrastructure. |
| [{{ech}}](/deploy-manage/deploy/elastic-cloud/cloud-hosted.md) | {{ech}} is the Elastic Stack, managed through Elastic Cloud deployments. |
| [{{ece}}](/deploy-manage/deploy/cloud-enterprise.md) | Deploy Elastic Cloud on public or private clouds, virtual machines, or your own premises. |
| [{{eck}}](/deploy-manage/deploy/cloud-on-k8s.md) | Deploy Elastic Cloud on Kubernetes. |
| [Self-managed](/deploy-manage/deploy/self-managed.md) | Install, configure, and run Elastic products on your own premises. |

:::

::::

:::{tip}
To learn about RESTful APIs, third-party dependencies, supported regions, and more for ECH, ECE, ECK, and ECCTL deployments, refer to the [Cloud reference documentation](cloud://reference/index.md).
:::

## Browse reference docs

### Ingestion tools

Find the reference docs for various Elastic ingestion tools including:

* [Logstash](logstash://reference/index.md)
* [Beats](beats://reference/index.md)
* [Elastic Distributions of OpenTelemetry](opentelemetry://reference/index.md)
* [Fleet and Elastic Agent](/reference/fleet/index.md)
* [APM](/reference/apm/observability/apm.md)
* [Elastic Serverless Forwarder for AWS](elastic-serverless-forwarder://reference/index.md)
* [Content connectors](elasticsearch://reference/search-connectors/index.md)
* [Elastic integrations](integration-docs://reference/index.md)

**Learn more in [Ingestion tools](ingestion-tools/index.md)**

### Query languages

Find detailed reference documentation for:

* [Query DSL](elasticsearch://reference/query-languages/querydsl.md)
* [{{esql}}](elasticsearch://reference/query-languages/esql.md)
* [SQL](elasticsearch://reference/query-languages/sql.md)
* [EQL](elasticsearch://reference/query-languages/eql.md)
* [Kibana Query Language](elasticsearch://reference/query-languages/kql.md)

### Painless scripting language

Access syntax references, function libraries, and best practices for Painless scripting.

**Learn more in [Painless scripting](elasticsearch://reference/scripting-languages/painless/painless.md)**

### Elastic Common Schema (ECS) reference

Standardize your data with ECS. Access logging libraries, field references, and categorization fields to ensure consistency and compatibility across your data sources.

**Learn more in [ECS](ecs://reference/index.md)**

### Search UI library

Explore reference content on the Search UI library and how you can develop fast, modern, and engaging search experiences on top of {{es}}.

**Learn more in [Search UI](search-ui://reference/index.md)**

### Elastic Distributions of OpenTelemetry (EDOT)

Elastic Distributions of OpenTelemetry (EDOT) is an open-source ecosystem of OpenTelemetry distributions tailored to Elastic. They include a customized OpenTelemetry Collector and several OpenTelemetry Language SDKs.

**Learn more in [Elastic Distributions of OpenTelemetry](opentelemetry://reference/index.md)**

### Elasticsearch plugins

Extend the functionality of your Elastic Stack with a variety of plugins. From analysis and discovery to snapshot/restore and store plugins, customize your setup to fit your requirements.

**Learn more in [Plugins](elasticsearch://reference/elasticsearch-plugins/index.md)**