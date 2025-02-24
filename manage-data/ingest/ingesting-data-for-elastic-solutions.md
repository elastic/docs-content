---
mapped_pages:
  - https://www.elastic.co/guide/en/ingest-overview/current/ingest-for-solutions.html
applies_to:
  stack: ga
  serverless: ga
---

# Ingesting data for Elastic solutions [ingest-for-solutions]

Elastic solutions—​Security, Observability, and Search—​are loaded with features and functionality to help you get value and insights from your data. [Elastic Agent](https://www.elastic.co/guide/en/fleet/current) and [Elastic integrations](integration-docs://docs/reference/ingestion-tools/integrations/index.md) can help, and are the best place to start.

When you use integrations with solutions, you have an integrated experience that offers easier implementation and decreases the time it takes to get insights and value from your data.

::::{admonition} High-level overview
To use [Elastic Agent](https://www.elastic.co/guide/en/fleet/current) and [Elastic integrations](integration-docs://docs/reference/ingestion-tools/integrations/index.md) with Elastic solutions:

1. Create an [{{ecloud}}](https://www.elastic.co/cloud) deployment for your solution. If you don’t have an {{ecloud}} account, you can sign up for a [free trial](https://cloud.elastic.co/registration) to get started.
2. Add the [Elastic integration](integration-docs://docs/reference/ingestion-tools/integrations/index.md) for your data source to the deployment.
3. [Install {{agent}}](docs-content://docs/reference/ingestion-tools/fleet/install-elastic-agents.md) on the systems whose data you want to collect.

::::


::::{note}
[Elastic serverless](/deploy-manage/deploy/elastic-cloud/serverless.md) makes using solutions even easier. Sign up for a [free trial](/deploy-manage/deploy/elastic-cloud/create-an-organization.md), and check it out.
::::



## Ingesting data for Search [ingest-for-search]

{{es}} is the magic behind Search and our other solutions. The solution gives you more pre-built components to get you up and running quickly for common use cases.

**Resources**

* [Install {{agent}}](docs-content://docs/reference/ingestion-tools/fleet/install-elastic-agents.md)
* [Elastic Search for integrations](https://www.elastic.co/integrations/data-integrations?solution=search)
* [{{es}} Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current)

    * [{{es}} document APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-document)
    * [{{es}} language clients](https://www.elastic.co/guide/en/elasticsearch/client/index.html)
    * [Elastic web crawler](https://www.elastic.co/web-crawler)
    * [Elastic connectors](elasticsearch://docs/reference/ingestion-tools/search-connectors/index.md)



## Ingesting data for Observability [ingest-for-obs]

With [Elastic Observability](https://www.elastic.co/observability), you can monitor and gain insights into logs, metrics, and application traces. The guides and resources in this section illustrate how to ingest data and use it with the Observability solution.

**Guides for popular Observability use cases**

* [Monitor applications and systems with Elastic Observability](/solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md)
* [Get started with logs and metrics](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md)

    * [Step 1: Add the {{agent}} System integration](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md#add-system-integration)
    * [Step 2: Install and run {{agent}}](/solutions/observability/infra-and-hosts/get-started-with-system-metrics.md#add-agent-to-fleet)

* [Observability](/solutions/observability.md) on [{{serverless-full}}](/deploy-manage/deploy/elastic-cloud/serverless.md):

    * [Monitor hosts with {{agent}} ({{serverless-short}})](/solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md)
    * [Monitor your K8s cluster with {{agent}} ({{serverless-short}})](/solutions/observability/get-started/quickstart-monitor-kubernetes-cluster-with-elastic-agent.md)

* [Use OpenTelemetry with APM](../../solutions/observability/apps/use-opentelemetry-with-apm.md)


**Resources**

* [Install {{agent}}](docs-content://docs/reference/ingestion-tools/fleet/install-elastic-agents.md)
* [Elastic Observability integrations](https://www.elastic.co/integrations/data-integrations?solution=observability)


## Ingesting data for Security [ingest-for-security]

You can detect and respond to threats when you use [Elastic Security](https://www.elastic.co/security) to analyze and take action on your data. The guides and resources in this section illustrate how to ingest data and use it with the Security solution.

**Guides for popular Security use cases**

* [Use Elastic Security for SIEM](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-siem-security.html)
* [Protect hosts with endpoint threat intelligence from Elastic Security](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-endpoint-security.html)

**Resources**

* [Install {{agent}}](docs-content://docs/reference/ingestion-tools/fleet/install-elastic-agents.md)
* [Elastic Security integrations](https://www.elastic.co/integrations/data-integrations?solution=search)
* [Elastic Security documentation](/solutions/security.md)


## Ingesting data for your own custom search solution [ingest-for-custom]

Elastic solutions can give you a head start for common use cases, but you are not at all limited. You can still do your own thing with a custom solution designed by *you*.

Bring your ideas and use {{es}} and the {{stack}} to store, search, and visualize your data.

**Resources**

* [Install {{agent}}](docs-content://docs/reference/ingestion-tools/fleet/install-elastic-agents.md)
* [{{es}} Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current)

    * [{{es}} document APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-document)
    * [{{es}} language clients](https://www.elastic.co/guide/en/elasticsearch/client/index.html)
    * [Elastic web crawler](https://www.elastic.co/web-crawler)
    * [Elastic connectors](elasticsearch://docs/reference/ingestion-tools/search-connectors/index.md)

* [Tutorial: Get started with vector search and generative AI](https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/getting-started-general-purpose.html)
