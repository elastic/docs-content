# An overview of the {{stack}} [stack-components]

What exactly is the "{{stack}}"? It’s a fast and highly scalable set of components — {{es}}, {{kib}}, {{beats}}, {{ls}}, and others — that together enable you to securely take data from any source, in any format, and then search, analyze, and visualize it.

You can deploy the {{stack}} as a Cloud service supported on AWS, Google Cloud, and Azure, or as an on-prem installation on your own hardware.

![Components of the Elastic Stack](../images/stack-components-diagram.svg)

## Ingest [_ingest]

Elastic provides a number of components that ingest data. Collect and ship logs, metrics, and other types of data with {{agent}} or {{beats}}. Manage your {{agents}} with {{fleet}}. Collect detailed performance information with Elastic APM.

If you want to transform or enrich data before it’s stored, you can use {{es}} ingest pipelines or {{ls}}.

Trying to decide which ingest component to use? Refer to [Adding data to {{es}}](https://www.elastic.co/guide/en/cloud/current/ec-cloud-ingest-data.html) to help you decide.

$$$stack-components-agent$$$

{{fleet}} and {{agent}}
:   {{agent}} is a single, unified way to add monitoring for logs, metrics, and other types of data to a host. It can also protect hosts from security threats, query data from operating systems, forward data from remote services or hardware, and more. Each agent has a single policy to which you can add integrations for new data sources, security protections, and more.

    {{fleet}} enables you to centrally manage {{agents}} and their policies. Use {{fleet}} to monitor the state of all your {{agents}}, manage agent policies, and upgrade {{agent}} binaries or integrations.

    [Learn more about {{fleet}} and {{agent}}](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html).


$$$stack-components-apm$$$

APM
:   Elastic APM is an application performance monitoring system built on the {{stack}}. It allows you to monitor software services and applications in real-time, by collecting detailed performance information on response time for incoming requests, database queries, calls to caches, external HTTP requests, and more. This makes it easy to pinpoint and fix performance problems quickly. [Learn more about APM](https://www.elastic.co/guide/en/apm/guide/current/apm-overview.html).

$$$stack-components-beats$$$

{{beats}}
:   {{beats}} are data shippers that you install as agents on your servers to send operational data to {{es}}. {{beats}} are available for many standard observability data scenarios, including audit data, log files and journals, cloud data, availability, metrics, network traffic, and Windows event logs. [Learn more about {{beats}}](https://www.elastic.co/guide/en/beats/libbeat/current/beats-reference.html).

$$$stack-components-ingest-pipelines$$$

{{es}} ingest pipelines
:   Ingest pipelines let you perform common transformations on your data before indexing them into {{es}}. You can configure one or more "processor" tasks to run sequentially, making specific changes to your documents before storing them in {{es}}. [Learn more about ingest pipelines](https://www.elastic.co/guide/en/elasticsearch/reference/current/ingest.html).

$$$stack-components-logstash$$$

{{ls}}
:   {{ls}} is a data collection engine with real-time pipelining capabilities. It can dynamically unify data from disparate sources and normalize the data into destinations of your choice. {{ls}} supports a broad array of input, filter, and output plugins, with many native codecs further simplifying the ingestion process. [Learn more about {{ls}}](https://www.elastic.co/guide/en/logstash/current/introduction.html).


## Store [_store]

$$$stack-components-elasticsearch$$$

{{es}}
:   {{es}} is the distributed search and analytics engine at the heart of the {{stack}}. It provides near real-time search and analytics for all types of data. Whether you have structured or unstructured text, numerical data, or geospatial data, {{es}} can efficiently store and index it in a way that supports fast searches. {{es}} provides a REST API that enables you to store data in {{es}} and retrieve it. The REST API also provides access to {{es}}'s search and analytics capabilities. [Learn more about {{es}}](https://www.elastic.co/guide/en/elasticsearch/reference/current/elasticsearch-intro.html).


## Consume [_consume]

Use {{kib}} to query and visualize the data that’s stored in {{es}}. Or, use the {{es}} clients to access data in {{es}} directly from common programming languages.

$$$stack-components-kibana$$$

{{kib}}
:   {{kib}} is the tool to harness your {{es}} data and to manage the {{stack}}. Use it to analyze and visualize the data that’s stored in {{es}}. {{kib}} is also the home for the Elastic Enterprise Search, Elastic Observability and Elastic Security solutions. [Learn more about {{kib}}](https://www.elastic.co/guide/en/kibana/current/introduction.html).

$$$stack-components-elasticsearch-clients$$$

{{es}} clients
:   The clients provide a convenient mechanism to manage API requests and responses to and from {{es}} from popular languages such as Java, Ruby, Go, Python, and others. Both official and community contributed clients are available. [Learn more about the {{es}} clients](https://www.elastic.co/guide/en/elasticsearch/client/index.html).

