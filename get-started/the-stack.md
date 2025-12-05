---
mapped_pages:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/stack-components.html
  - https://www.elastic.co/guide/en/kibana/current/introduction.html
  - https://www.elastic.co/guide/en/kibana/current/index.html
  - https://www.elastic.co/guide/en/elastic-stack/current/installing-elastic-stack.html
  - https://www.elastic.co/guide/en/elastic-stack/current/overview.html
products:
  - id: elastic-stack
  - id: kibana
applies_to:
  stack:
---

# The {{stack}}

This section provides an overview of the {{stack}} and its components.

$$$kibana-navigation-search$$$

## An overview of the {{stack}} [stack-components]

What is the {{stack}}? It’s a fast and highly scalable set of components — {{es}}, {{kib}}, {{beats}}, {{ls}}, and others — that together enable you to securely take data from any source, in any format, and then search, analyze, and visualize it.

The products in the {{es}} are designed to be used together and releases are synchronized to simplify the installation and upgrade process.

You have many options for deploying the {{stack}} to suit your needs. You can deploy it on your own hardware, in the cloud, or use a managed service on {{ecloud}}.

:::{tip}
To learn how to deploy {{es}}, {{kib}}, and supporting orchestration technologies, refer to [](/deploy-manage/index.md). To learn how to deploy additional ingest and consume components, refer to the documentation for the component.
:::

![Components of the Elastic Stack](/get-started/images/stack-components-diagram.svg)

### Ingest [_ingest]

Elastic provides a number of components that ingest data. Collect and ship logs, metrics, and other types of data with {{agent}} or {{beats}}. Manage your {{agents}} with {{fleet}}. Collect detailed performance information with Elastic APM.

If you want to transform or enrich data before it’s stored, you can use {{es}} ingest pipelines or {{ls}}.

Trying to decide which ingest component to use? Refer to [Adding data to {{es}}](/manage-data/ingest.md) to help you decide.

#### {{fleet}} and {{agent}} [stack-components-agent]

{{agent}} is a single, unified way to add monitoring for logs, metrics, and other types of data to a host. It can also protect hosts from security threats, query data from operating systems, forward data from remote services or hardware, and more. Each agent has a single policy to which you can add integrations for new data sources, security protections, and more.

{{fleet}} enables you to centrally manage {{agents}} and their policies. Use {{fleet}} to monitor the state of all your {{agents}}, manage agent policies, and upgrade {{agent}} binaries or integrations.

[Learn more about {{fleet}} and {{agent}}](/reference/fleet/index.md).

#### APM [stack-components-apm]

Elastic APM is an application performance monitoring system built on the {{stack}}. It allows you to monitor software services and applications in real-time, by collecting detailed performance information on response time for incoming requests, database queries, calls to caches, external HTTP requests, and more. This makes it easy to pinpoint and fix performance problems quickly. [Learn more about APM](/solutions/observability/apm/index.md).

#### {{beats}} [stack-components-beats]

{{beats}} are data shippers that you install as agents on your servers to send operational data to {{es}}. {{beats}} are available for many standard observability data scenarios, including audit data, log files and journals, cloud data, availability, metrics, network traffic, and Windows event logs. [Learn more about {{beats}}](beats://reference/index.md).

#### {{es}} ingest pipelines [stack-components-ingest-pipelines]

Ingest pipelines let you perform common transformations on your data before indexing them into {{es}}. You can configure one or more "processor" tasks to run sequentially, making specific changes to your documents before storing them in {{es}}. [Learn more about ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md).

#### {{ls}} [stack-components-logstash]

{{ls}} is a data collection engine with real-time pipelining capabilities. It can dynamically unify data from disparate sources and normalize the data into destinations of your choice. {{ls}} supports a broad array of input, filter, and output plugins, with many native codecs further simplifying the ingestion process. [Learn more about {{ls}}](logstash://reference/index.md).


### Store [_store]

#### {{es}} [stack-components-elasticsearch]

{{es}} is the distributed search and analytics engine at the heart of the {{stack}}. It provides near real-time search and analytics for all types of data. Whether you have structured or unstructured text, numerical data, or geospatial data, {{es}} can efficiently store and index it in a way that supports fast searches. {{es}} provides a REST API that enables you to store data in {{es}} and retrieve it. The REST API also provides access to {{es}}'s search and analytics capabilities. [Learn more about {{es}}](/get-started/index.md).


### Consume [_consume]

Use {{kib}} to query and visualize the data that’s stored in {{es}}. Or, use the {{es}} clients to access data in {{es}} directly from common programming languages.

#### {{kib}} [stack-components-kibana]

{{kib}} is the tool to harness your {{es}} data and to manage the {{stack}}. Use it to analyze and visualize the data that’s stored in {{es}}. {{kib}} is also the home for the Search, Observability and Security solutions. [Learn more about {{kib}}](/explore-analyze/index.md).

#### {{es}} clients [stack-components-elasticsearch-clients]

The clients provide a convenient mechanism to manage API requests and responses to and from {{es}} from popular languages such as Java, Ruby, Go, Python, and others. Both official and community contributed clients are available. [Learn more about the {{es}} clients](/reference/elasticsearch-clients/index.md).

Whitelist

## Version compatibility
```{applies_to}
deployment:
  self:
```

:::{include} /deploy-manage/deploy/_snippets/stack-version-compatibility.md
:::

## Installation order
```{applies_to}
deployment:
  self:
```

:::{include} /deploy-manage/deploy/_snippets/installation-order.md
:::
