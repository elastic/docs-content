---
mapped_pages:
  - https://www.elastic.co/guide/en/starting-with-the-elasticsearch-platform-and-its-solutions/current/stack-components.html
  - https://www.elastic.co/guide/en/kibana/current/introduction.html
  - https://www.elastic.co/guide/en/kibana/current/index.html
  - https://www.elastic.co/guide/en/elastic-stack/current/installing-elastic-stack.html
  - https://www.elastic.co/guide/en/elastic-stack/current/overview.html
products:
  - id: elastic-stack
---
# {{search-platform}}

Elastic provides a fusion of search technology and artifical intelligence in the [{{search-platform}}](https://www.elastic.co/platform).
It is the foundation for Elastic's two out-of-the-box [solutions](/get-started/introduction.md) and is the platform of choice for developers seeking to build next generation, generative AI powered applications and services.

The {{search-platform}} evolved from the {{stack}} and continues to be open by design.
It's a fast and highly scalable set of components — {{es}}, {{kib}}, {{beats}}, {{ls}}, and others — that together enable you to securely take data from any source, in any format, and then store, search, analyze, and visualize it.

You have many options for deploying the {{search-platform}} to suit your needs, which are summarized in [](/get-started/deployment-options.md).

:::{tip}
To learn how to deploy {{es}}, {{kib}}, and supporting orchestration technologies, refer to [](/deploy-manage/index.md).
To learn how to deploy additional ingest and consume components, refer to the documentation for the component.
:::

Continue reading to learn how these components work together.

% TO-DO: Update SVG
% ![Components of the {{search-platform}}](/get-started/images/stack-components-diagram.svg)

## Ingestion

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

## Storage, search, and AI analysis

{{es}} is the distributed search, storage, and analytics engine at the heart of the {{search-platform}}.
You can use the {{es}} clients to access data directly by using common programming languages.

### {{es}} [components-elasticsearch]

{{es}} provides near real-time search and analytics for all types of data.
Whether you have structured or unstructured text, numerical data, vectors, or geospatial data, {{es}} can efficiently store and index it in a way that supports fast searches.

{{es}} is built to be a resilient and scalable distributed system.
It runs as a cluster of one or more servers, called nodes.
When you add data to an index, it's divided into pieces called shards, which are spread across the various nodes in the cluster.
This architecture allows {{es}} to handle large volumes of data and ensures that your data remains available even if a node fails.

{{es}} provides a REST API that enables you to store data in {{es}} and retrieve it.
The REST API also provides access to search and analytics capabilities.

Learn more about [the {{es}} data store](/manage-data/data-store.md), its [distributed architecture](/deploy-manage/distributed-architecture.md), and [search approaches](/solutions/search/search-approaches.md). 

### {{es}} clients [stack-components-elasticsearch-clients]

The clients provide a convenient mechanism to manage API requests and responses to and from {{es}} from popular languages such as Java, Ruby, Go, Python, and others.
Both official and community contributed clients are available.

[Learn more about the {{es}} clients](/reference/elasticsearch-clients/index.md).

## Exploration and visualization

Use {{kib}} to query and visualize the data that's stored in {{es}}.

### {{kib}} [stack-components-kibana]

{{kib}} is the tool to harness your {{es}} data and to manage the {{search-platform}}.
Use it to analyze and visualize the data that's stored in {{es}}.
{{kib}} is also the home for two out-of-the-box [solutions](/get-started/introduction.md).

[Learn more about {{kib}}](/explore-analyze/index.md).



<!--


### Visualize and query your data [kibana-navigation-search]

While {{es}} stores your data, **Kibana** is the user interface where you can explore, visualize, and manage it. It provides a window into your data, allowing you to quickly gain insights and understand trends.

With Kibana, you can:

* Use **Discover** to interactively search and filter your raw data.  
* Build custom **visualizations** like charts, graphs, and metrics with tools like **Lens**, which offers a drag-and-drop experience.  
* Assemble your visualizations into interactive **dashboards** to get a comprehensive overview of your information.  
* Analyze geospatial data using the powerful **Maps** application.

At the same time, Kibana works as the user interface of all Elastic solutions, like Elastic Security and Elastic Observability, providing ways of configuring Elastic to suit your needs and offering interactive guidance.

A **query** is a question you ask about your data, and Elastic provides several powerful languages to do so. You can query data directly through the API or through the user interface in Kibana.

* **Query DSL** is a full-featured JSON-style query language that enables complex searching, filtering, and aggregations. It is the original and most powerful query language for Elasticsearch today.
* **Elasticsearch Query Language (ES|QL)** is a powerful, modern query language that uses a familiar pipe-based syntax to transform and aggregate your data at search time.  
* **Event Query Language (EQL)** is a specialized language designed to query sequences of events, which is particularly useful for security analytics and threat hunting.
* **Kibana Query Language (KQL)** is the text-based language used in the **Discover** search bar, perfect for interactive filtering and exploration.  

Learn more in [](/explore-analyze/index.md).

### Use the APIs to automate operations and management

Nearly every aspect of Elasticsearch can be configured and managed programmatically through its extensive REST APIs. This allows you to automate repetitive tasks and integrate Elastic management into your existing operational workflows. You can use the APIs to manage indices, update cluster settings, run complex queries, and configure security. 

The **Console** tool in Kibana provides an interactive way to send requests directly to the Elasticsearch API and view the responses. For secure, automated access, you can create and manage **API keys** to authenticate your scripts and applications. This API-first approach is fundamental to enabling infrastructure-as-code practices and managing your deployments at scale.

Learn more in [Elastic APIs](https://www.elastic.co/docs/api).
-->