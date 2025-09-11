---
mapped_pages:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/stack-components.html
  - https://www.elastic.co/guide/en/kibana/current/introduction.html
  - https://www.elastic.co/guide/en/kibana/current/index.html
  - https://www.elastic.co/guide/en/elastic-stack/current/installing-elastic-stack.html
  - https://www.elastic.co/guide/en/elastic-stack/current/overview.html
products:
  - id: elastic-stack
applies_to:
  serverless:
  stack:
---
# {{search-platform}}

Elastic provides a fusion of search technology and artifical intelligence in the [{{search-platform}}](https://www.elastic.co/platform).
It is the foundation for Elastic's [solutions](/get-started/introduction.md) and for developers seeking to build next generation, generative AI powered applications and services.

The {{search-platform}} is a fast and highly scalable set of components — {{es}}, {{kib}}, {{beats}}, {{ls}}, and others — that together enable you to securely take data from any source, in any format, and then store, search, analyze, and visualize it.

$$$stack-components$$$
![Components of the {{search-platform}}](/get-started/images/platform-components-diagram.svg)

:::{tip}
The components that share the same versioning scheme are often referred to as the _{{stack}}_. Learn more in [](/get-started/versioning-availability.md).
:::

You have many options for deploying the {{search-platform}}, which are summarized in [](/get-started/deployment-options.md).
All deployments include [{{es}}](#stack-components-elasticsearch).
Although [{{kib}}](#stack-components-kibana) is not required to use {{es}}, it is included by default when you use deployment methods such as {{serverless-full}}.

Continue reading to learn how these components work together.

## Ingest [_ingest]

Elastic provides a number of components that ingest data.
Collect and ship logs, metrics, and other types of data with {{agent}} or {{beats}}.
Manage your {{agents}} with {{fleet}}.
Collect detailed performance information with Elastic APM.

If you want to transform or enrich data before it's stored, you can use {{es}} ingest pipelines or {{ls}}.

Trying to decide which ingest component to use? Refer to [](/manage-data/ingest.md) to help you decide.

### {{fleet}} and {{agent}} [stack-components-agent]

{{agent}} is a single, unified way to add monitoring for logs, metrics, and other types of data to a host.
It can also protect hosts from security threats, query data from operating systems, forward data from remote services or hardware, and more.
Each agent has a single policy to which you can add integrations for new data sources, security protections, and more.

{{fleet}} enables you to centrally manage {{agents}} and their policies.
Use {{fleet}} to monitor the state of all your {{agents}}, manage agent policies, and upgrade {{agent}} binaries or integrations.

[Learn more about {{fleet}} and {{agent}}](/reference/fleet/index.md).

### APM [stack-components-apm]

Elastic APM is an application performance monitoring system.
It allows you to monitor software services and applications in real-time, by collecting detailed performance information on response time for incoming requests, database queries, calls to caches, external HTTP requests, and more.
This makes it easy to pinpoint and fix performance problems quickly.

[Learn more about APM](/solutions/observability/apm/index.md).

### {{beats}} [stack-components-beats]

{{beats}} are data shippers that you install as agents on your servers to send operational data to {{es}}.
{{beats}} are available for many standard observability data scenarios, including audit data, log files and journals, cloud data, availability, metrics, network traffic, and Windows event logs.

[Learn more about {{beats}}](beats://reference/index.md).

### {{es}} ingest pipelines [stack-components-ingest-pipelines]

Ingest pipelines let you perform common transformations on your data before indexing them into {{es}}.
You can configure one or more "processor" tasks to run sequentially, making specific changes to your documents before storing them in {{es}}.

[Learn more about ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md).

### {{ls}} [stack-components-logstash]

{{ls}} is a data collection engine with real-time pipelining capabilities.
It can dynamically unify data from disparate sources and normalize the data into destinations of your choice.
{{ls}} supports a broad array of input, filter, and output plugins, with many native codecs further simplifying the ingestion process.

[Learn more about {{ls}}](logstash://reference/index.md).

## Store, search, and analyze [_store]

{{es}} is the distributed search, storage, and analytics engine at the heart of the {{search-platform}}.

### {{es}} [stack-components-elasticsearch]

{{es}} provides near real-time search and analytics for all types of data.
Whether you have structured or unstructured text, numerical data, vectors, or geospatial data, {{es}} can efficiently store and index it in a way that supports fast searches.

{{es}} is built to be a resilient and scalable distributed system.
It runs as a cluster of one or more servers, called nodes.
When you add data to an index, it's divided into pieces called shards, which are spread across the various nodes in the cluster.
This architecture allows {{es}} to handle large volumes of data and ensures that your data remains available even if a node fails.

Nearly every aspect of {{es}} can be configured and managed programmatically through its REST APIs.
This allows you to automate repetitive tasks and integrate Elastic management into your existing operational workflows.
For example, you can use the APIs to manage indices, update cluster settings, run complex queries, and configure security.
This API-first approach is fundamental to enabling infrastructure-as-code practices and managing deployments at scale.

Learn more about [the {{es}} data store](/manage-data/data-store.md), its [distributed architecture](/deploy-manage/distributed-architecture.md), and [APIs](elasticsearch://reference/elasticsearch/rest-apis/index.md).

## Explore [_consume]

Use {{kib}} to explore and visualize the data that's stored in {{es}} and to manage the {{search-platform}}.
You can use the {{es}} clients to access data directly by using common programming languages.

### {{kib}} [stack-components-kibana]

With {{kib}}, you can:

* Use **Discover** to interactively search and filter your raw data.  
* Build custom visualizations like charts, graphs, and metrics with tools like **Lens**, which offers a drag-and-drop experience.  
* Assemble your visualizations into interactive dashboards to get a comprehensive overview of your information.  
* Analyze geospatial data using the powerful **Maps** application.

It also has [query tools](/explore-analyze/query-filter/tools.md) such as **Console**, which provides an interactive way to send requests directly to the {{es}} API and view the responses.
For secure, automated access, you can create and manage API keys to authenticate your scripts and applications.

[Learn more about {{kib}}](/explore-analyze/index.md).

### {{es}} clients [stack-components-elasticsearch-clients]

The clients provide a convenient mechanism to manage API requests and responses to and from {{es}} from popular languages such as Java, Ruby, Go, Python, and others.
Both official and community contributed clients are available.

[Learn more about the {{es}} clients](/reference/elasticsearch-clients/index.md).