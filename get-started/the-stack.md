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
description: The {{stack}} are products that work together to securely store, search, analyze, and visualize your data.
---
# The {{stack}}

All Elastic [deployments and projects](deployment-options.md) share the same open source foundation:

- [{{es}}](#stack-components-elasticsearch): The distributed data store and search engine that handles indexing, querying, and analytics.
- [{{kib}}](#stack-components-kibana): The user interface with dashboards, visualizations, and management tools.

Depending on your use case, you might need to install more products that work together with {{es}} and {{kib}} (referred to as the [{{stack}}](https://www.elastic.co/elastic-stack) or ELK). For example:

- [{{agent}}](#stack-components-agent): A lightweight data shipper that collects and forwards data to {{es}}.
- [{{ls}}](#stack-components-logstash): The data ingestion and transformation engine, often used for more complex ETL (extract, transform, load) pipelines.

$$$stack-components$$$
The {{stack}} includes products for [ingesting](#_ingest), [storing](#_store), and [exploring](#_consume) data at scale:

![Components of the {{stack}}](/get-started/images/platform-components-diagram.svg)

Continue reading to learn how these products work together.

## Store, search, and analyze [_store]

All deployments include {{es}}.
{{es}} is the distributed search and analytics engine, scalable data store, and vector database at the heart of all Elastic deployments and solutions.
You can use the {{es}} clients to access data directly by using common programming languages.

### {{es}} [stack-components-elasticsearch]

{{es}} is a data store and [vector database](https://www.elastic.co/elasticsearch/vector-database) that provides near real-time search and analytics for all types of data.
Whether you have structured or unstructured text, time series (timestamped) data, vectors, or geospatial data, {{es}} can efficiently store and index it in a way that supports fast searches.
It also includes multiple query languages, aggregations, and robust features for [querying and filtering](/explore-analyze/query-filter.md) your data.

{{es}} is built to be a resilient and scalable distributed system.
It runs as a cluster of one or more servers, called nodes.
When you add data to an index, it's divided into pieces called shards, which are spread across the various nodes in the cluster.
This architecture allows {{es}} to handle large volumes of data and ensures that your data remains available even if a node fails.
If you use {{serverless-full}}, it has a unique [Search AI Lake cloud-native architecture](https://www.elastic.co/cloud/serverless/search-ai-lake) and automates the nodes, shards, and replicas for you.

{{es}} also includes [AI-powered features](/explore-analyze/ai-features.md) and built-in {{nlp}} (NLP) models that enable you to make predictions, run {{infer}}, and integrate with LLMs faster.

Nearly every aspect of {{es}} can be configured and managed programmatically through its REST APIs.
This allows you to automate repetitive tasks and integrate Elastic management into your existing operational workflows.
For example, you can use the APIs to manage indices, update cluster settings, run complex queries, and configure security.
This API-first approach is fundamental to enabling infrastructure-as-code practices and managing deployments at scale.

Learn more about [the {{es}} data store](/manage-data/data-store.md), its [distributed architecture](/deploy-manage/distributed-architecture.md), and [APIs](elasticsearch://reference/elasticsearch/rest-apis/index.md).

### {{es}} clients [stack-components-elasticsearch-clients]

The clients provide a convenient mechanism to manage API requests and responses to and from {{es}} from popular languages such as Java, Ruby, Go, and Python.
Both official and community contributed clients are available.

[Learn more about the {{es}} clients](/reference/elasticsearch-clients/index.md).

## Explore and visualize [_consume]

Use {{kib}} to explore, manage, and visualize the data that's stored in {{es}} and to manage components of the {{stack}}.

### {{kib}} [stack-components-kibana]

{{kib}} provides the user interface for all Elastic [solutions](/get-started/introduction.md) and {{serverless-short}} projects.
It's a powerful tool for visualizing and analyzing your data and for managing and monitoring the {{stack}}.
Although you can use {{es}} without it, {{kib}} is required for most use cases and is included by default when you deploy {{serverless-full}}.

With {{kib}}, you can:

- Use [Discover](/explore-analyze/discover.md) to interactively search and filter your raw data.
- Build custom [visualizations](/explore-analyze/visualize.md) like charts, graphs, and metrics with tools like **Lens**, which offers a drag-and-drop experience.  
- Assemble your visualizations into interactive [dashboards](/explore-analyze/dashboards.md) to get a comprehensive overview of your information.
- Perform [geospatial analysis](/explore-analyze/geospatial-analysis.md) and add maps to your dashboards.
- Configure notifications for significant data events and track incidents with [alerts and cases](/explore-analyze/alerts-cases.md).
- Manage resources such as processors, pipelines, data streams, trained models, and more.

Each solution or project type provides access to customized features in {{kib}} such as built-in dashboards and [AI assistants](/explore-analyze/ai-features/ai-assistant.md).

{{kib}} also has [query tools](/explore-analyze/query-filter/tools.md) such as **Console**, which provides an interactive way to send requests directly to the {{es}} API and view the responses.
For secure, automated access, you can create and manage API keys to authenticate your scripts and applications.

Learn more in [](/explore-analyze/index.md).

## Ingest [_ingest]

Before you can search it, visualize it, and use it for insights, you must get your data into {{es}}.
There are multiple methods for ingesting data.
The best approach depends on the type of data and your specific use case.
For example, you can collect and ship logs, metrics, and other types of data with {{agent}} or collect detailed performance information with {{product.apm}}.
If you want to transform and enrich data before it's stored, you can use {{es}} ingest pipelines or {{ls}}.

Trying to decide which ingest components to use? Refer to [](/manage-data/ingest.md) and [](/manage-data/ingest/tools.md).

### {{agent}} and {{integrations}}[stack-components-agent]

{{agent}} is a single, unified way to add monitoring for logs, metrics, and other types of data to a host.
It can also protect hosts from security threats, query data from operating systems, and forward data from remote services or hardware.
Each agent has a single policy to which you can add [integrations](integration-docs://reference/index.md) for new data sources, security protections, and more.
You can also use [{{agent}} processors](/reference/fleet/agent-processors.md) to sanitize or enrich your data.

To monitor the state of all your {{agents}}, manage agent policies, and upgrade {{agent}} binaries or integrations, refer to [Central management in {{fleet}}](/reference/fleet/index.md#central-management).

[Learn more about {{agent}}](/reference/fleet/index.md).

### {{product.apm}} [stack-components-apm]

{{product.apm}} is an application performance monitoring system.
It allows you to monitor software services and applications in real-time by collecting detailed performance information on response time for incoming requests, database queries, calls to caches, external HTTP requests, and more.
This makes it easy to pinpoint and fix performance problems quickly.

[Learn more about {{product.apm}}](/solutions/observability/apm/index.md).

### OpenTelemetry Collector [stack-components-otel]

:::{include} /manage-data/_snippets/otel.md
:::

With EDOT, you can use vendor-neutral instrumentation and stream native OTel data such as standardized traces, metrics, and logs without proprietary agents.

### {{beats}} [stack-components-beats]

:::{include} /manage-data/_snippets/beats.md
:::

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