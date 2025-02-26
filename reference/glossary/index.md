---
mapped_pages:
  - https://www.elastic.co/guide/en/elastic-stack-glossary/current/index.html
  - https://www.elastic.co/guide/en/elastic-stack-glossary/current/terms.html
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-glossary.html
  - https://www.elastic.co/guide/en/ecs/current/ecs-glossary.html
---

# Glossary [terms]

$$$glossary-metadata$$$ @metadata
:   A special field for storing content that you don't want to include in output [events](/reference/glossary/index.md#glossary-event). For example, the `@metadata` field is useful for creating transient fields for use in [conditional](/reference/glossary/index.md#glossary-conditional) statements.


## A [a-glos]

$$$glossary-action$$$ action
:   1. The rule-specific response that occurs when an alerting rule fires. A rule can have multiple actions. See [Connectors and actions](kibana://docs/reference/connectors-kibana.md).
2. In {{elastic-sec}}, actions send notifications via other systems when a detection alert is created, such as email, Slack, PagerDuty, and {{webhook}}.


$$$glossary-admin-console$$$ administration console
:   A component of {{ece}} that provides the API server for the [Cloud UI](/reference/glossary/index.md#glossary-cloud-ui). Also syncs cluster and allocator data from ZooKeeper to {{es}}.

$$$glossary-advanced-settings$$$ Advanced Settings
:   Enables you to control the appearance and behavior of {{kib}} by setting the date format, default index, and other attributes. Part of {{kib}} Stack Management. See [Advanced Settings](kibana://docs/reference/advanced-settings.md).

$$$glossary-agent-policy$$$ Agent policy
:   A collection of inputs and settings that defines the data to be collected by {{agent}}. An agent policy can be applied to a single agent or shared by a group of agents; this makes it easier to manage many agents at scale. See [{{agent}} policies](/reference/ingestion-tools/fleet/agent-policy.md).

$$$glossary-alias$$$ alias
:   Secondary name for a group of [data streams](/reference/glossary/index.md#glossary-data-stream) or [indices](/reference/glossary/index.md#glossary-index). Most {{es}} APIs accept an alias in place of a data stream or index. See [Aliases](/manage-data/data-store/aliases.md).

$$$glossary-allocator-affinity$$$ allocator affinity
:   Controls how {{stack}} deployments are distributed across the available set of allocators in your {{ece}} installation.

$$$glossary-allocator-tag$$$ allocator tag
:   In {{ece}}, characterizes hardware resources for {{stack}} deployments. Used by [instance configurations](/reference/glossary/index.md#glossary-instance-configuration) to determine which instances of the {{stack}} should be placed on what hardware.

$$$glossary-allocator$$$ allocator
:   Manages hosts that contain {{es}} and {{kib}} nodes. Controls the lifecycle of these nodes by creating new [containers](/reference/glossary/index.md#glossary-container) and managing the nodes within these containers when requested. Used to scale the capacity of your {{ece}} installation.

$$$glossary-analysis$$$ analysis
:   Process of converting unstructured [text](/reference/glossary/index.md#glossary-text) into a format optimized for search. See [Text analysis](/manage-data/data-store/text-analysis.md).

$$$glossary-annotation$$$ annotation
:   A way to augment a data display with descriptive domain knowledge.

$$$glossary-anomaly-detection-job$$$ {{anomaly-job}}
:   {{anomaly-jobs-cap}} contain the configuration information and metadata necessary to perform an analytics task. See [{{ml-jobs-cap}}](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-create-job).

$$$glossary-api-key$$$ API key
:   Unique identifier for authentication in {{es}}. When [transport layer security (TLS)](/deploy-manage/deploy/self-managed/installing-elasticsearch.md) is enabled, all requests must be authenticated using an API key or a username and password.

$$$glossary-apm-agent$$$ APM agent
:   An open-source library, written in the same language as your service, which [instruments](/reference/glossary/index.md#glossary-instrumentation) your code and collects performance data and errors at runtime.

$$$glossary-apm-server$$$ APM Server
:   An open-source application that receives data from [APM agents](/reference/glossary/index.md#glossary-apm-agent) and sends it to {{es}}.

$$$glossary-app$$$ app
:   A top-level {{kib}} component that is accessed through the side navigation. Apps include core {{kib}} components such as Discover and Dashboard, solutions like {{observability}} and Security, and special-purpose tools like Maps and {{stack-manage-app}}.

$$$glossary-auto-follow-pattern$$$ auto-follow pattern
:   [Index pattern](/reference/glossary/index.md#glossary-index-pattern) that automatically configures new [indices](/reference/glossary/index.md#glossary-index) as [follower indices](/reference/glossary/index.md#glossary-follower-index) for [{{ccr}}](/reference/glossary/index.md#glossary-ccr). See [Manage auto-follow patterns](/deploy-manage/tools/cross-cluster-replication/manage-auto-follow-patterns.md).

$$$glossary-zone$$$ availability zone
:   Contains resources available to an {{ece}} installation that are isolated from other availability zones to safeguard against failure. Could be a rack, a server zone or some other logical constraint that creates a failure boundary. In a highly available cluster, the nodes of a cluster are spread across two or three availability zones to ensure that the cluster can survive the failure of an entire availability zone. Also see [Fault Tolerance (High Availability)](/deploy-manage/deploy/cloud-enterprise/ece-ha.md).


## B [b-glos]

$$$glossary-basemap$$$ basemap
:   The background detail necessary to orient the location of a map.

$$$glossary-beats-runner$$$ beats runner
:   Used to send {{filebeat}} and {{metricbeat}} information to the logging cluster.

$$$glossary-bucket-aggregation$$$ bucket aggregation
:   An aggregation that creates buckets of documents. Each bucket is associated with a criterion (depending on the aggregation type), which determines whether or not a document in the current context falls into the bucket.

$$$glossary-ml-bucket$$$ bucket
:   1. A set of documents in {{kib}} that have certain characteristics in common. For example, matching documents might be bucketed by color, distance, or date range.
2. The {{ml-features}} also use the concept of a bucket to divide the time series into batches for processing. The *bucket span* is part of the configuration information for {{anomaly-jobs}}. It defines the time interval that is used to summarize and model the data. This is typically between 5 minutes to 1 hour and it depends on your data characteristics. When you set the bucket span, take into account the granularity at which you want to analyze, the frequency of the input data, the typical duration of the anomalies, and the frequency at which alerting is required.



## C [c-glos]

$$$glossary-canvas-language$$$ Canvas expression language
:   A pipeline-based expression language for manipulating and visualizing data. Includes dozens of functions and other capabilities, such as table transforms, type casting, and sub-expressions. Supports TinyMath functions for complex math calculations. See [Canvas function reference](/reference/data-analysis/kibana/canvas-functions.md).

$$$glossary-canvas$$$ Canvas
:   Enables you to create presentations and infographics that pull live data directly from {{es}}. See [Canvas](/explore-analyze/visualize/canvas.md).

$$$glossary-certainty$$$ certainty
:   Specifies how many documents must contain a pair of terms before it is considered a useful connection in a graph.

$$$CA$$$CA
:   Certificate authority. An entity that issues digital certificates to verify identities over a network.

$$$glossary-client-forwarder$$$ client forwarder
:   Used for secure internal communications between various components of {{ece}} and ZooKeeper.

$$$glossary-cloud-ui$$$ Cloud UI
:   Provides web-based access to manage your {{ece}} installation, supported by the [administration console](/reference/glossary/index.md#glossary-admin-console).

$$$glossary-cluster$$$ cluster
:   1. A group of one or more connected {{es}} [nodes](/reference/glossary/index.md#glossary-node). See [Clusters, nodes, and shards](/deploy-manage/production-guidance/getting-ready-for-production-elasticsearch.md).
2. A layer type and display option in the **Maps** application. Clusters display a cluster symbol across a grid on the map, one symbol per grid cluster. The cluster location is the weighted centroid for all documents in the grid cell.
3. In {{eck}}, it can refer to either an [Elasticsearch cluster](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md) or a Kubernetes cluster depending on the context.

$$$glossary-codec-plugin$$$ codec plugin
:   A {{ls}} [plugin](/reference/glossary/index.md#glossary-plugin) that changes the data representation of an [event](/reference/glossary/index.md#glossary-event). Codecs are essentially stream filters that can operate as part of an input or output. Codecs enable you to separate the transport of messages from the serialization process. Popular codecs include json, msgpack, and plain (text).

$$$glossary-cold-phase$$$ cold phase
:   Third possible phase in the [index lifecycle](/reference/glossary/index.md#glossary-index-lifecycle). In the cold phase, data is no longer updated and seldom [queried](/reference/glossary/index.md#glossary-query). The data still needs to be searchable, but it's okay if those queries are slower. See [Index lifecycle](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md).

$$$glossary-cold-tier$$$ cold tier
:   [Data tier](/reference/glossary/index.md#glossary-data-tier) that contains [nodes](/reference/glossary/index.md#glossary-node) that hold time series data that is accessed occasionally and not normally updated. See [Data tiers](/manage-data/lifecycle/data-tiers.md).

$$$glossary-component-template$$$ component template
:   Building block for creating [index templates](/reference/glossary/index.md#glossary-index-template). A component template can specify [mappings](/reference/glossary/index.md#glossary-mapping), [index settings](elasticsearch://docs/reference/elasticsearch/index-settings/index.md), and [aliases](/reference/glossary/index.md#glossary-alias). See [index templates](/manage-data/data-store/templates.md).

$$$glossary-condition$$$ condition
:   Specifies the circumstances that must be met to trigger an alerting [rule](/reference/glossary/index.md#glossary-rule).

$$$glossary-conditional$$$ conditional
:   A control flow that executes certain actions based on whether a statement (also called a condition) is true or false. {{ls}} supports `if`, `else if`, and `else` statements. You can use conditional statements to apply filters and send events to a specific output based on conditions that you specify.

$$$glossary-connector$$$ connector
:   A configuration that enables integration with an external system (the destination for an action). See [Connectors and actions](kibana://docs/reference/connectors-kibana.md).

$$$glossary-console$$$ Console
:   In {{kib}}, a tool for interacting with the {{es}} REST API. You can send requests to {{es}}, view responses, view API documentation, and get your request history. See [Console](/explore-analyze/query-filter/tools/console.md).

    In {{ecloud}}, provides web-based access to manage your {{ecloud}} deployments.


$$$glossary-constructor$$$ constructor
:   Directs [allocators](/reference/glossary/index.md#glossary-allocator) to manage containers of {{es}} and {{kib}} nodes and maximizes the utilization of allocators. Monitors plan change requests from the Cloud UI and determines how to transform the existing cluster. In a highly available installation, places cluster nodes within different availability zones to ensure that the cluster can survive the failure of an entire availability zone.

$$$glossary-container$$$ container
:   Includes an instance of {{ece}} software and its dependencies. Used to provision similar environments, to assign a guaranteed share of host resources to nodes, and to simplify operational effort in {{ece}}.

$$$glossary-content-tier$$$ content tier
:   [Data tier](/reference/glossary/index.md#glossary-data-tier) that contains [nodes](/reference/glossary/index.md#glossary-node) that handle the [indexing](/reference/glossary/index.md#glossary-index) and [query](/reference/glossary/index.md#glossary-query) load for content, such as a product catalog. See [Data tiers](/manage-data/lifecycle/data-tiers.md).

$$$glossary-coordinator$$$ coordinator
:   Consists of a logical grouping of some {{ece}} services and acts as a distributed coordination system and resource scheduler.

$$$glossary-ccr$$$ {{ccr}} (CCR)
:   Replicates [data streams](/reference/glossary/index.md#glossary-data-stream) and [indices](/reference/glossary/index.md#glossary-index) from [remote clusters](/reference/glossary/index.md#glossary-remote-cluster) in a [local cluster](/reference/glossary/index.md#glossary-local-cluster). See [{{ccr-cap}}](/deploy-manage/tools/cross-cluster-replication.md).

$$$glossary-ccs$$$ {{ccs}} (CCS)
:   Searches [data streams](/reference/glossary/index.md#glossary-data-stream) and [indices](/reference/glossary/index.md#glossary-index) on [remote clusters](/reference/glossary/index.md#glossary-remote-cluster) from a [local cluster](/reference/glossary/index.md#glossary-local-cluster). See [Search across clusters](/solutions/search/cross-cluster-search.md).

$$$CRD$$$CRD
:   [Custom resource definition](https://kubernetes.io/docs/reference/glossary/?fundamental=true#term-CustomResourceDefinition). {{eck}} extends the Kubernetes API with CRDs to allow users to deploy and manage Elasticsearch, Kibana, APM Server, Enterprise Search, Beats, Elastic Agent, Elastic Maps Server, and Logstash resources just as they would do with built-in Kubernetes resources.

$$$glossary-custom-rule$$$ custom rule
:   A set of conditions and actions that change the behavior of {{anomaly-jobs}}. You can also use filters to further limit the scope of the rules. See [Custom rules](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-rules). {{kib}} refers to custom rules as job rules.


## D [d-glos]

$$$glossary-dashboard$$$ dashboard
:   A collection of [visualizations](/reference/glossary/index.md#glossary-visualization), [saved searches](/reference/glossary/index.md#glossary-saved-search), and [maps](/reference/glossary/index.md#glossary-map) that provide insights into your data from multiple perspectives.

$$$glossary-data-center$$$ data center
:   Check [availability zone](/reference/glossary/index.md#glossary-zone).

$$$glossary-dataframe-job$$$ data frame analytics job
:   Data frame analytics jobs contain the configuration information and metadata necessary to perform {{ml}} analytics tasks on a source index and store the outcome in a destination index. See [{{dfanalytics-cap}} overview](/explore-analyze/machine-learning/data-frame-analytics/ml-dfa-overview.md).

$$$glossary-data-source$$$ data source
:   A file, database, or service that provides the underlying data for a map, Canvas element, or visualization.

$$$glossary-data-stream$$$ data stream
:   A named resource used to manage [time series data](/reference/glossary/index.md#glossary-time-series-data). A data stream stores data across multiple backing [indices](/reference/glossary/index.md#glossary-index). See [Data streams](/manage-data/data-store/data-streams.md).

$$$glossary-data-tier$$$ data tier
:   Collection of [nodes](/reference/glossary/index.md#glossary-node) with the same [data role](elasticsearch://docs/reference/elasticsearch/configuration-reference/node-settings.md) that typically share the same hardware profile. Data tiers include the [content tier](/reference/glossary/index.md#glossary-content-tier), [hot tier](/reference/glossary/index.md#glossary-hot-tier), [warm tier](/reference/glossary/index.md#glossary-warm-tier), [cold tier](/reference/glossary/index.md#glossary-cold-tier), and [frozen tier](/reference/glossary/index.md#glossary-frozen-tier). See [Data tiers](/manage-data/lifecycle/data-tiers.md).

$$$glossary-data-view$$$ data view
:   An object that enables you to select the data that you want to use in {{kib}} and define the properties of the fields. A data view can point to one or more [data streams](/reference/glossary/index.md#glossary-data-stream), [indices](/reference/glossary/index.md#glossary-index), or [aliases](/reference/glossary/index.md#glossary-alias). For example, a data view can point to your log data from yesterday, or all indices that contain your data.

$$$glossary-ml-datafeed$$$ datafeed
:   {{anomaly-jobs-cap}} can analyze either a one-off batch of data or continuously in real time. {{dfeeds-cap}} retrieve data from {{es}} for analysis.

$$$glossary-dataset$$$ dataset
:   A collection of data that has the same structure. The name of a dataset typically signifies its source. See [data stream naming scheme](/reference/ingestion-tools/fleet/data-streams.md).

$$$glossary-delete-phase$$$ delete phase
:   Last possible phase in the [index lifecycle](/reference/glossary/index.md#glossary-index-lifecycle). In the delete phase, an [index](/reference/glossary/index.md#glossary-index) is no longer needed and can safely be deleted. See [Index lifecycle](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md).

$$$glossary-deployment-template$$$ deployment template
:   A reusable configuration of Elastic products and solutions used to create an {{ecloud}} [deployment](/reference/glossary/index.md#glossary-deployment).

$$$glossary-deployment$$$ deployment
:   One or more products from the {{stack}} configured to work together and run on {{ecloud}}.

$$$glossary-detection-alert$$$ detection alert
:   {{elastic-sec}} produced alerts. Detection alerts are never received from external systems. When a rule's conditions are met, {{elastic-sec}} writes a detection alert to an {{es}} alerts index.

$$$glossary-detection-rule$$$ detection rule
:   Background tasks in {{elastic-sec}} that run periodically and produce alerts when suspicious activity is detected.

$$$glossary-ml-detector$$$ detector
:   As part of the configuration information that is associated with {{anomaly-jobs}}, detectors define the type of analysis that needs to be done. They also specify which fields to analyze. You can have more than one detector in a job, which is more efficient than running multiple jobs against the same data.

$$$glossary-director$$$ director
:   Manages the [ZooKeeper](/reference/glossary/index.md#glossary-zookeeper) datastore. This role is often shared with the [coordinator](/reference/glossary/index.md#glossary-coordinator), though in production deployments it can be separated.

$$$glossary-discover$$$ Discover
:   Enables you to search and filter your data to zoom in on the information that you are interested in.

$$$glossary-distributed-tracing$$$ distributed tracing
:   The end-to-end collection of performance data throughout your microservices architecture.

$$$glossary-document$$$ document
:   JSON object containing data stored in {{es}}. See [Documents and indices](/manage-data/data-store/index-basics.md).

$$$glossary-drilldown$$$ drilldown
:   A navigation path that retains context (time range and filters) from the source to the destination, so you can view the data from a new perspective. A dashboard that shows the overall status of multiple data centers might have a drilldown to a dashboard for a single data center. See [Drilldowns](/explore-analyze/dashboards.md).


## E [e-glos]

$$$glossary-edge$$$ edge
:   A connection between nodes in a graph that shows that they are related. The line weight indicates the strength of the relationship.  See [Graph](/explore-analyze/visualize/graph.md).

$$$glossary-elastic-agent$$$ {{agent}}
:   A single, unified way to add monitoring for logs, metrics, and other types of data to a host. It can also protect hosts from security threats, query data from operating systems, forward data from remote services or hardware, and more. See [{{agent}} overview](/reference/ingestion-tools/fleet/index.md).

$$$glossary-ece$$$ {{ece}} (ECE)
:   The official enterprise offering to host and manage the {{stack}} yourself at scale. Can be installed on a public cloud platform, such as AWS, GCP or Microsoft Azure, on your own private cloud, or on bare metal.

$$$glossary-eck$$$ {{eck}} (ECK)
:   Built on the Kubernetes Operator pattern, ECK extends the basic Kubernetes orchestration capabilities to support the setup and management of Elastic products and solutions on Kubernetes.

$$$glossary-ecs$$$ Elastic Common Schema (ECS)
:   A document schema for Elasticsearch, for use cases such as logging and metrics. ECS defines a common set of fields, their datatype, and gives guidance on their correct usage. ECS is used to improve uniformity of event data coming from different sources.

$$$EKS$$$ Elastic Kubernetes Service (EKS)
:   A managed Kubernetes service provided by Amazon Web Services (AWS).

$$$glossary-ems$$$ Elastic Maps Service (EMS)
:   A service that provides basemap tiles, shape files, and other key features that are essential for visualizing geospatial data.

$$$glossary-epr$$$ Elastic Package Registry (EPR)
:   A service hosted by Elastic that stores Elastic package definitions in a central location. See the [EPR GitHub repository](https://github.com/elastic/package-registry).

$$$glossary-elastic-security-indices$$$ {{elastic-sec}} indices
:   Indices containing host and network source events (such as `packetbeat-*`, `log-*`, and `winlogbeat-*`). When you [create a new rule in {{elastic-sec}}](/solutions/security/detect-and-alert/create-detection-rule.md), the default index pattern corresponds to the values defined in the `securitySolution:defaultIndex` advanced setting.

$$$glossary-elastic-stack$$$ {{stack}}
:   Also known as the *ELK Stack*, the {{stack}} is the combination of various Elastic products that integrate for a scalable and flexible way to manage your data.

$$$glossary-elasticsearch-service$$$ Elasticsearch Service
:   The former name of {{ech}}, which is the official hosted {{stack}} offering, from the makers of {{es}}. Available as a software-as-a-service (SaaS) offering on different cloud platforms, such as AWS, GCP, and Microsoft Azure.

$$$glossary-element$$$ element
:   A [Canvas](/reference/glossary/index.md#glossary-canvas) workpad object that displays an image, text, or visualization.

$$$glossary-endpoint-exception$$$ endpoint exception
:   [Exceptions](/reference/glossary/index.md#glossary-exception) added to both rules and Endpoint agents on hosts. Endpoint exceptions can only be added when:

    * Endpoint agents are installed on the hosts.
    * The {{elastic-endpoint}} Security rule is activated.


$$$glossary-eql$$$ Event Query Language (EQL)
:   [Query](/reference/glossary/index.md#glossary-query) language for event-based time series data, such as logs, metrics, and traces. EQL supports matching for event sequences. See [EQL](/explore-analyze/query-filter/languages/eql.md).

$$$glossary-event$$$ event
:   A single unit of information, containing a timestamp plus additional data. An event arrives via an input, and is subsequently parsed, timestamped, and passed through the {{ls}} [pipeline](/reference/glossary/index.md#glossary-pipeline).

$$$glossary-exception$$$ exception
:   In {{elastic-sec}}, exceptions are added to rules to prevent specific source event field values from generating alerts.

$$$glossary-external-alert$$$ external alert
:   Alerts {{elastic-sec}} receives from external systems, such as Suricata.


## F [f-glos]

$$$glossary-feature-controls$$$ Feature Controls
:   Enables administrators to customize which features are available in each [space](/reference/glossary/index.md#glossary-space). See [Feature Controls](/deploy-manage/manage-spaces.md#spaces-control-feature-visibility).

$$$glossary-feature-importance$$$ feature importance
:   In supervised {{ml}} methods such as {{regression}} and {{classification}}, feature importance indicates the degree to which a specific feature affects a prediction. See [{{regression-cap}} feature importance](/explore-analyze/machine-learning/data-frame-analytics/ml-dfa-regression.md#dfa-regression-feature-importance) and [{{classification-cap}} feature importance](/explore-analyze/machine-learning/data-frame-analytics/ml-dfa-classification.md#dfa-classification-feature-importance).

$$$glossary-feature-influence$$$ feature influence
:   In {{oldetection}}, feature influence scores indicate which features of a data point contribute to its outlier behavior. See [Feature influence](/explore-analyze/machine-learning/data-frame-analytics/ml-dfa-finding-outliers.md#dfa-feature-influence).

$$$glossary-feature-state$$$ feature state
:   The indices and data streams used to store configurations, history, and other data for an Elastic feature, such as {{es}} security or {{kib}}. A feature state typically includes one or more [system indices or data streams](/reference/glossary/index.md#glossary-system-index). It may also include regular indices and data streams used by the feature. You can use [snapshots](/reference/glossary/index.md#glossary-snapshot) to back up and restore feature states. See [feature states](/deploy-manage/tools/snapshot-and-restore.md#feature-state).

$$$glossary-field-reference$$$ field reference
:   A reference to an event [field](/reference/glossary/index.md#glossary-field). This reference may appear in an output block or filter block in the {{ls}} config file. Field references are typically wrapped in square (`[]`) brackets, for example `[fieldname]`. If you are referring to a top-level field, you can omit the `[]` and simply use the field name. To refer to a nested field, you specify the full path to that field: `[top-level field][nested field]`.

$$$glossary-field$$$ field
:   1. Key-value pair in a [document](/reference/glossary/index.md#glossary-document). See [Mapping](/manage-data/data-store/mapping.md).
2. In {{ls}}, this term refers to an [event](/reference/glossary/index.md#glossary-event) property. For example, each event in an apache access log has properties, such as a status code (200, 404), request path ("/", "index.html"), HTTP verb (GET, POST), client IP address, and so on. {{ls}} uses the term "fields" to refer to these properties.


$$$glossary-filter-plugin$$$ filter plugin
:   A {{ls}} [plugin](/reference/glossary/index.md#glossary-plugin) that performs intermediary processing on an [event](/reference/glossary/index.md#glossary-event). Typically, filters act upon event data after it has been ingested via inputs, by mutating, enriching, and/or modifying the data according to configuration rules. Filters are often applied conditionally depending on the characteristics of the event. Popular filter plugins include grok, mutate, drop, clone, and geoip. Filter stages are optional.

$$$glossary-filter$$$ filter
:   [Query](/reference/glossary/index.md#glossary-query) that does not score matching documents. See [filter context](/explore-analyze/query-filter/languages/querydsl.md).

$$$glossary-fleet-server$$$ {{fleet-server}}
:   {{fleet-server}} is a component used to centrally manage {{agent}}s. It serves as a control plane for updating agent policies, collecting status information, and coordinating actions across agents.

$$$glossary-fleet$$$ Fleet
:   Fleet provides a way to centrally manage {{agent}}s at scale. There are two parts: The Fleet app in {{kib}} provides a web-based UI to add and remotely manage agents, while the {{fleet-server}} provides the backend service that manages agents. See [{{agent}} overview](/reference/ingestion-tools/fleet/index.md).

$$$glossary-flush$$$ flush
:   Writes data from the [transaction log](elasticsearch://docs/reference/elasticsearch/index-settings/translog.md) to disk for permanent storage.

$$$glossary-follower-index$$$ follower index
:   Target [index](/reference/glossary/index.md#glossary-index) for [{{ccr}}](/reference/glossary/index.md#glossary-ccr). A follower index exists in a [local cluster](/reference/glossary/index.md#glossary-local-cluster) and replicates a [leader index](/reference/glossary/index.md#glossary-leader-index). See [{{ccr-cap}}](/deploy-manage/tools/cross-cluster-replication.md).

$$$glossary-force-merge$$$ force merge
:   Manually triggers a [merge](/reference/glossary/index.md#glossary-merge) to reduce the number of [segments](/reference/glossary/index.md#glossary-segment) in an index's [shards](/reference/glossary/index.md#glossary-shard).

$$$glossary-frozen-phase$$$ frozen phase
:   Fourth possible phase in the [index lifecycle](/reference/glossary/index.md#glossary-index-lifecycle). In the frozen phase, an [index](/reference/glossary/index.md#glossary-index) is no longer updated and [queried](/reference/glossary/index.md#glossary-query) rarely. The information still needs to be searchable, but it's okay if those queries are extremely slow. See [Index lifecycle](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md).

$$$glossary-frozen-tier$$$ frozen tier
:   [Data tier](/reference/glossary/index.md#glossary-data-tier) that contains [nodes](/reference/glossary/index.md#glossary-node) that hold time series data that is accessed rarely and not normally updated. See [Data tiers](/manage-data/lifecycle/data-tiers.md).


## G [g-glos]

$$$GCS$$$GCS
:   Google Cloud Storage. Block storage service provided by Google Cloud Platform (GCP).

$$$GKE$$$GKE
:   [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine/). Managed Kubernetes service provided by Google Cloud Platform (GCP).

$$$glossary-gem$$$ gem
:   A self-contained package of code that's hosted on [RubyGems.org](https://rubygems.org). {{ls}} [plugins](/reference/glossary/index.md#glossary-plugin) are packaged as Ruby Gems. You can use the {{ls}} [plugin manager](/reference/glossary/index.md#glossary-plugin-manager) to manage {{ls}} gems.

$$$glossary-geo-point$$$ geo-point
:   A field type in {{es}}. A geo-point field accepts latitude-longitude pairs for storing point locations. The latitude-longitude format can be from a string, geohash, array, well-known text, or object. See [geo-point](elasticsearch://docs/reference/elasticsearch/mapping-reference/geo-point.md).

$$$glossary-geo-shape$$$ geo-shape
:   A field type in {{es}}. A geo-shape field accepts arbitrary geographic primitives, like polygons, lines, or rectangles (and more). You can populate a geo-shape field from GeoJSON or well-known text. See [geo-shape](elasticsearch://docs/reference/elasticsearch/mapping-reference/geo-shape.md).

$$$glossary-geojson$$$ GeoJSON
:   A format for representing geospatial data. GeoJSON is also a file-type, commonly used in the **Maps** application to upload a file of geospatial data. See [GeoJSON data](/explore-analyze/visualize/maps/indexing-geojson-data-tutorial.md).

$$$glossary-graph$$$ graph
:   A data structure and visualization that shows interconnections between a set of entities. Each entity is represented by a node. Connections between nodes are represented by [edges](/reference/glossary/index.md#glossary-edge). See [Graph](/explore-analyze/visualize/graph.md).

$$$glossary-grok-debugger$$$ Grok Debugger
:   A tool for building and debugging grok patterns. Grok is good for parsing syslog, Apache, and other webserver logs. See [Debugging grok expressions](/explore-analyze/query-filter/tools/grok-debugger.md).


## H [h-glos]

$$$glossary-hardware-profile$$$ hardware profile
:   In {{ecloud}}, a built-in [deployment template](/reference/glossary/index.md#glossary-deployment-template) that supports a specific use case for the {{stack}}, such as a compute optimized deployment that provides high vCPU for search-heavy use cases.

$$$glossary-heat-map$$$ heat map
:   A layer type in the **Maps** application. Heat maps cluster locations to show higher (or lower) densities. Heat maps describe a visualization with color-coded cells or regions to analyze patterns across multiple dimensions. See [Heat map layer](/explore-analyze/visualize/maps/heatmap-layer.md).

$$$glossary-hidden-index$$$ hidden data stream or index
:   [Data stream](/reference/glossary/index.md#glossary-data-stream) or [index](/reference/glossary/index.md#glossary-index) excluded from most [index patterns](/reference/glossary/index.md#glossary-index-pattern) by default. See [Hidden data streams and indices](elasticsearch://docs/reference/elasticsearch/rest-apis/api-conventions.md#multi-hidden).

$$$glossary-host-runner$$$ host runner (runner)
:   In {{ece}}, a local control agent that runs on all hosts, used to deploy local containers based on role definitions. Ensures that containers assigned to the host exist and are able to run, and creates or recreates the containers if necessary.

$$$glossary-hot-phase$$$ hot phase
:   First possible phase in the [index lifecycle](/reference/glossary/index.md#glossary-index-lifecycle). In the hot phase, an [index](/reference/glossary/index.md#glossary-index) is actively updated and queried. See [Index lifecycle](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md).

$$$glossary-hot-thread$$$ hot thread
:   A Java thread that has high CPU usage and executes for a longer than normal period of time.

$$$glossary-hot-tier$$$ hot tier
:   [Data tier](/reference/glossary/index.md#glossary-data-tier) that contains [nodes](/reference/glossary/index.md#glossary-node) that handle the [indexing](/reference/glossary/index.md#glossary-index) load for time series data, such as logs or metrics. This tier holds your most recent, most frequently accessed data. See [Data tiers](/manage-data/lifecycle/data-tiers.md).


## I [i-glos]

$$$glossary-id$$$ ID
:   Identifier for a [document](/reference/glossary/index.md#glossary-document). Document IDs must be unique within an [index](/reference/glossary/index.md#glossary-index). See the [`_id` field](elasticsearch://docs/reference/elasticsearch/mapping-reference/mapping-id-field.md).

$$$glossary-index-lifecycle-policy$$$ index lifecycle policy
:   Specifies how an [index](/reference/glossary/index.md#glossary-index) moves between phases in the [index lifecycle](/reference/glossary/index.md#glossary-index-lifecycle) and what actions to perform during each phase. See [Index lifecycle](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md).

$$$glossary-index-lifecycle$$$ index lifecycle
:   Five phases an [index](/reference/glossary/index.md#glossary-index) can transition through: [hot](/reference/glossary/index.md#glossary-hot-phase), [warm](/reference/glossary/index.md#glossary-warm-phase), [cold](/reference/glossary/index.md#glossary-cold-phase), [frozen](/reference/glossary/index.md#glossary-frozen-phase), and [delete](/reference/glossary/index.md#glossary-delete-phase). See [Index lifecycle](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md).

$$$glossary-index-pattern$$$ index pattern
:   In {{es}}, a string containing a wildcard (`*`) pattern that can match multiple [data streams](/reference/glossary/index.md#glossary-data-stream), [indices](/reference/glossary/index.md#glossary-index), or [aliases](/reference/glossary/index.md#glossary-alias). See [Multi-target syntax](elasticsearch://docs/reference/elasticsearch/rest-apis/api-conventions.md).

$$$glossary-index-template$$$ index template
:   Automatically configures the [mappings](/reference/glossary/index.md#glossary-mapping), [index settings](elasticsearch://docs/reference/elasticsearch/index-settings/index.md), and [aliases](/reference/glossary/index.md#glossary-alias) of new [indices](/reference/glossary/index.md#glossary-index) that match its [index pattern](/reference/glossary/index.md#glossary-index-pattern). You can also use index templates to create [data streams](/reference/glossary/index.md#glossary-data-stream). See [Index templates](/manage-data/data-store/templates.md).

$$$glossary-index$$$ index
:   1. Collection of JSON [documents](/reference/glossary/index.md#glossary-document). See [Documents and indices](/manage-data/data-store/index-basics.md).
2. To add one or more JSON documents to {{es}}. This process is called indexing.


$$$glossary-indexer$$$ indexer
:   A {{ls}} instance that is tasked with interfacing with an {{es}} cluster in order to index [event](/reference/glossary/index.md#glossary-event) data.

$$$glossary-indicator-index$$$ indicator index
:   Indices containing suspect field values in {{elastic-sec}}. [Indicator match rules](/solutions/security/detect-and-alert/create-detection-rule.md#create-indicator-rule) use these indices to compare their field values with source event values contained in [{{elastic-sec}} indices](/reference/glossary/index.md#glossary-elastic-security-indices).

$$$glossary-inference-aggregation$$$ inference aggregation
:   A pipeline aggregation that references a [trained model](/reference/glossary/index.md#glossary-trained-model) in an aggregation to infer on the results field of the parent bucket aggregation. It enables you to use supervised {{ml}} at search time.

$$$glossary-inference-processor$$$ inference processor
:   A processor specified in an ingest pipeline that uses a [trained model](/reference/glossary/index.md#glossary-trained-model) to infer against the data that is being ingested in the pipeline.

$$$glossary-inference$$$ inference
:   A {{ml}} feature that enables you to use supervised learning processes – like {{classification}}, {{regression}}, or [{{nlp}}](/reference/glossary/index.md#glossary-nlp) – in a continuous fashion by using [trained models](/reference/glossary/index.md#glossary-trained-model) against incoming data.

$$$glossary-influencer$$$ influencer
:   Influencers are entities that might have contributed to an anomaly in a specific bucket in an {{anomaly-job}}. For more information, see [Influencers](/explore-analyze/machine-learning/anomaly-detection/ml-ad-run-jobs.md#ml-ad-influencers).

$$$glossary-ingestion$$$ ingestion
:   The process of collecting and sending data from various data sources to {{es}}.

$$$glossary-input-plugin$$$ input plugin
:   A {{ls}} [plugin](/reference/glossary/index.md#glossary-plugin) that reads [event](/reference/glossary/index.md#glossary-event) data from a specific source. Input plugins are the first stage in the {{ls}} event processing [pipeline](/reference/glossary/index.md#glossary-pipeline). Popular input plugins include file, syslog, redis, and beats.

$$$glossary-instance-configuration$$$ instance configuration
:   In {{ecloud}}, enables the instances of the {{stack}} to run on suitable hardware resources by filtering on [allocator tags](/reference/glossary/index.md#glossary-allocator-tag). Used as building blocks for [deployment templates](/reference/glossary/index.md#glossary-deployment-template).

$$$glossary-instance-type$$$ instance type
:   In {{ecloud}}, categories for [instances](/reference/glossary/index.md#glossary-instance) representing an Elastic feature or cluster node types, such as `master`, `ml` or `data`.

$$$glossary-instance$$$ instance
:   A product from the {{stack}} that is running in an {{ecloud}} deployment, such as an {{es}} node or a {{kib}} instance. When you choose more [availability zones](/reference/glossary/index.md#glossary-zone), the system automatically creates more instances for you.

$$$glossary-instrumentation$$$ instrumentation
:   Extending application code to track where your application is spending time. Code is considered instrumented when it collects and reports this performance data to APM.

$$$glossary-integration-policy$$$ integration policy
:   An instance of an [integration](/reference/glossary/index.md#glossary-integration) that is configured for a specific use case, such as collecting logs from a specific file.

$$$glossary-integration$$$ integration
:   An easy way for external systems to connect to the {{stack}}. Whether it's collecting data or protecting systems from security threats, integrations provide out-of-the-box assets to make setup easy—​many with just a single click.


## J [j-glos]

$$$glossary-ml-job$$$$$$glossary-job$$$ job
:   {{ml-cap}} jobs contain the configuration information and metadata necessary to perform an analytics task. There are two types: [{{anomaly-jobs}}](/reference/glossary/index.md#glossary-anomaly-detection-job) and [data frame analytics jobs](/reference/glossary/index.md#glossary-dataframe-job). See also [{{rollup-job}}](/reference/glossary/index.md#glossary-rollup-job).


## K [k-glos]

$$$k8s$$$K8s
:   Shortened form (numeronym) of "Kubernetes" derived from replacing "ubernete" with "8".

$$$glossary-kibana-privilege$$$ {{kib}} privilege
:   Enable administrators to grant users read-only, read-write, or no access to individual features within [spaces](/reference/glossary/index.md#glossary-space) in {{kib}}. See [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

$$$glossary-kql$$$ {{kib}} Query Language (KQL)
:   The default language for querying in {{kib}}. KQL provides support for scripted fields. See [Kibana Query Language](/explore-analyze/query-filter/languages/kql.md).

$$$glossary-kibana$$$ {{kib}}
:   A user interface that lets you visualize your {{es}} data and navigate the {{stack}}.


## L [l-glos]

$$$glossary-labs$$$ labs
:   An in-progress or experimental feature in **Canvas** or **Dashboard** that you can try out and provide feedback. When enabled, you'll see **Labs** in the toolbar.

$$$glossary-leader-index$$$ leader index
:   Source [index](/reference/glossary/index.md#glossary-index) for [{{ccr}}](/reference/glossary/index.md#glossary-ccr). A leader index exists on a [remote cluster](/reference/glossary/index.md#glossary-remote-cluster) and is replicated to [follower indices](/reference/glossary/index.md#glossary-follower-index). See [{{ccr-cap}}](/deploy-manage/tools/cross-cluster-replication.md).

$$$glossary-lens$$$ Lens
:   Enables you to build visualizations by dragging and dropping data fields. Lens makes makes smart visualization suggestions for your data, allowing you to switch between visualization types. See [Lens](/explore-analyze/dashboards.md).

$$$glossary-local-cluster$$$ local cluster
:   [Cluster](/reference/glossary/index.md#glossary-cluster) that pulls data from a [remote cluster](/reference/glossary/index.md#glossary-remote-cluster) in [{{ccs}}](/reference/glossary/index.md#glossary-ccs) or [{{ccr}}](/reference/glossary/index.md#glossary-ccr). See [Remote clusters](/deploy-manage/remote-clusters/remote-clusters-self-managed.md).

$$$glossary-lucene$$$ Lucene query syntax
:   The query syntax for {{kib}}'s legacy query language. The Lucene query syntax is available under the options menu in the query bar and from [Advanced Settings](/reference/glossary/index.md#glossary-advanced-settings).


## M [m-glos]

$$$glossary-ml-nodes$$$ machine learning node
:   A {{ml}} node is a node that has `xpack.ml.enabled` set to `true` and `ml` in `node.roles`. If you want to use {{ml-features}}, there must be at least one {{ml}} node in your cluster. See [Machine learning nodes](elasticsearch://docs/reference/elasticsearch/configuration-reference/node-settings.md#ml-node).

$$$glossary-map$$$ map
:   A representation of geographic data using symbols and labels. See [Maps](/explore-analyze/visualize/maps.md).

$$$glossary-mapping$$$ mapping
:   Defines how a [document](/reference/glossary/index.md#glossary-document), its [fields](/reference/glossary/index.md#glossary-field), and its metadata are stored in {{es}}. Similar to a schema definition. See [Mapping](/manage-data/data-store/mapping.md).

$$$glossary-master-node$$$ master node
:   Handles write requests for the cluster and publishes changes to other nodes in an ordered fashion. Each cluster has a single master node which is chosen automatically by the cluster and is replaced if the current master node fails. Also see [node](/reference/glossary/index.md#glossary-node).

$$$glossary-merge$$$ merge
:   Process of combining a [shard](/reference/glossary/index.md#glossary-shard)'s smaller Lucene [segments](/reference/glossary/index.md#glossary-segment) into a larger one. {{es}} manages merges automatically.

$$$glossary-message-broker$$$ message broker
:   Also referred to as a *message buffer* or *message queue*, a message broker is external software (such as Redis, Kafka, or RabbitMQ) that stores messages from the {{ls}} shipper instance as an intermediate store, waiting to be processed by the {{ls}} indexer instance.

$$$glossary-metric-aggregation$$$ metric aggregation
:   An aggregation that calculates and tracks metrics for a set of documents.

$$$glossary-module$$$ module
:   Out-of-the-box configurations for common data sources to simplify the collection, parsing, and visualization of logs and metrics.

$$$glossary-monitor$$$ monitor
:   A network endpoint which is monitored to track the performance and availability of applications and services.

$$$glossary-multi-field$$$ multi-field
:   A [field](/reference/glossary/index.md#glossary-field) that's [mapped](/reference/glossary/index.md#glossary-mapping) in multiple ways. See the [`fields` mapping parameter](elasticsearch://docs/reference/elasticsearch/mapping-reference/multi-fields.md).

$$$glossary-multifactor$$$ multifactor authentication (MFA)
:   A security process that requires you to provide two or more verification methods to gain access to web-based user interfaces.


## N [n-glos]

$$$glossary-namespace$$$ namespace
:   A user-configurable arbitrary data grouping, such as an environment (`dev`, `prod`, or `qa`), a team, or a strategic business unit.

$$$glossary-nlp$$$ natural language processing (NLP)
:   A {{ml}} feature that enables you to perform operations such as language identification, named entity recognition (NER), text classification, or text embedding. See [NLP overview](/explore-analyze/machine-learning/nlp/ml-nlp-overview.md).

$$$glossary-no-op$$$ no-op
:   In {{ecloud}}, the application of a rolling update on your deployment without actually applying any configuration changes. This type of update can be useful to resolve certain health warnings.

$$$glossary-node$$$ node
:   1. A single {{es}} server. One or more nodes can form a [cluster](/reference/glossary/index.md#glossary-cluster). See [Clusters, nodes, and shards](/deploy-manage/production-guidance/getting-ready-for-production-elasticsearch.md).
2. In {{eck}}, it can refer to either an [Elasticsearch Node](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-node.md) or a [Kubernetes Node](https://kubernetes.io/docs/concepts/architecture/nodes/) depending on the context. ECK maps an Elasticsearch node to a Kubernetes Pod which can get scheduled onto any available Kubernetes node that can satisfy the [resource requirements](/deploy-manage/deploy/cloud-on-k8s/manage-compute-resources.md) and [node constraints](https://kubernetes.io/docs/concepts/configuration/assign-pod-node/) defined in the [pod template](/deploy-manage/deploy/cloud-on-k8s/customize-pods.md).

$$$NodeSet$$$NodeSet
:   A set of Elasticsearch nodes that share the same Elasticsearch configuration and a Kubernetes Pod template. Multiple NodeSets can be defined in the Elasticsearch CRD to achieve a cluster topology consisting of groups of Elasticsearch nodes with different node roles, resource requirements and hardware configurations (Kubernetes node constraints).

## O [o-glos]

$$$glossary-observability$$$ Observability
:   Unifying your logs, metrics, uptime data, and application traces to provide granular insights and context into the behavior of services running in your environments.

$$$OpenShift$$$OpenShift
:   A Kubernetes [platform](https://www.openshift.com/) by RedHat.

$$$Operator$$$operator
:   A design pattern in Kubernetes for [managing custom resources](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/). {{eck}} implements the operator pattern to manage Elasticsearch, Kibana and APM Server resources on Kubernetes.

$$$glossary-output-plugin$$$ output plugin
:   A {{ls}} [plugin](/reference/glossary/index.md#glossary-plugin) that writes [event](/reference/glossary/index.md#glossary-event) data to a specific destination. Outputs are the final stage in the event [pipeline](/reference/glossary/index.md#glossary-pipeline). Popular output plugins include elasticsearch, file, graphite, and statsd.


## P [p-glos]

$$$glossary-painless-lab$$$ Painless Lab
:   An interactive code editor that lets you test and debug Painless scripts in real-time. See [Painless Lab](/explore-analyze/scripting/painless-lab.md).

$$$glossary-panel$$$ panel
:   A [dashboard](/reference/glossary/index.md#glossary-dashboard) component that contains a query element or visualization, such as a chart, table, or list.

$$$PDB$$$PDB
:   A [pod disruption budget](https://kubernetes.io/docs/reference/glossary/?all=true#term-pod-disruption-budget) in {{eck}}.

$$$glossary-pipeline$$$ pipeline
:   A term used to describe the flow of [events](/reference/glossary/index.md#glossary-event) through the {{ls}} workflow. A pipeline typically consists of a series of input, filter, and output stages. [Input](/reference/glossary/index.md#glossary-input-plugin) stages get data from a source and generate events, [filter](/reference/glossary/index.md#glossary-filter-plugin) stages, which are optional, modify the event data, and [output](/reference/glossary/index.md#glossary-output-plugin) stages write the data to a destination. Inputs and outputs support [codecs](/reference/glossary/index.md#glossary-codec-plugin) that enable you to encode or decode the data as it enters or exits the pipeline without having to use a separate filter.

$$$glossary-plan$$$ plan
:   Specifies the configuration and topology of an {{es}} or {{kib}} cluster, such as capacity, availability, and {{es}} version, for example. When changing a plan, the [constructor](/reference/glossary/index.md#glossary-constructor) determines how to transform the existing cluster into the pending plan.

$$$glossary-plugin-manager$$$ plugin manager
:   Accessed via the `bin/logstash-plugin` script, the plugin manager enables you to manage the lifecycle of [plugins](/reference/glossary/index.md#glossary-plugin) in your {{ls}} deployment. You can install, remove, and upgrade plugins by using the plugin manager Command Line Interface (CLI).

$$$glossary-plugin$$$ plugin
:   A self-contained software package that implements one of the stages in the {{ls}} event processing [pipeline](/reference/glossary/index.md#glossary-pipeline). The list of available plugins includes [input plugins](/reference/glossary/index.md#glossary-input-plugin), [output plugins](/reference/glossary/index.md#glossary-output-plugin), [codec plugins](/reference/glossary/index.md#glossary-codec-plugin), and [filter plugins](/reference/glossary/index.md#glossary-filter-plugin). The plugins are implemented as Ruby [gems](/reference/glossary/index.md#glossary-gem) and hosted on [RubyGems.org](https://rubygems.org). You define the stages of an event processing [pipeline](/reference/glossary/index.md#glossary-pipeline) by configuring plugins.

$$$glossary-primary-shard$$$ primary shard
:   Lucene instance containing some or all data for an [index](/reference/glossary/index.md#glossary-index). When you index a [document](/reference/glossary/index.md#glossary-document), {{es}} adds the document to primary shards before [replica shards](/reference/glossary/index.md#glossary-replica-shard). See [Clusters, nodes, and shards](/deploy-manage/production-guidance/getting-ready-for-production-elasticsearch.md).

$$$glossary-proxy$$$ proxy
:   A highly available, TLS-enabled proxy layer that routes user requests, mapping cluster IDs that are passed in request URLs for the container to the cluster nodes handling the user requests.

$$$PVC$$$PVC
:   A [persistent volume claim](https://kubernetes.io/docs/reference/glossary/?all=true#term-persistent-volume-claim) in {{eck}}.

## Q [q-glos]

$$$QoS$$$QoS
:   Quality of service in {{eck}}. When a Kubernetes cluster is under heavy load, the Kubernetes scheduler makes pod eviction decisions based on the [QoS class of individual pods](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/). [*Manage compute resources*](/deploy-manage/deploy/cloud-on-k8s/manage-compute-resources.md) explains how to define QoS classes for Elasticsearch, Kibana and APM Server pods.

$$$glossary-query-profiler$$$ Query Profiler
:   A tool that enables you to inspect and analyze search queries to diagnose and debug poorly performing queries. See [Query Profiler](/explore-analyze/query-filter/tools/search-profiler.md).

$$$glossary-query$$$ query
:   Request for information about your data. You can think of a query as a question, written in a way {{es}} understands. See [Search your data](/solutions/search/querying-for-search.md).


## R [r-glos]

$$$RBAC$$$RBAC
:   Role-based Access Control. In {{eck}}, it is a security mechanism in Kubernetes where access to cluster resources is restricted to principals having the appropriate role. Check [https://kubernetes.io/docs/reference/access-authn-authz/rbac/](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) for more information.

$$$glossary-real-user-monitoring$$$ Real user monitoring (RUM)
:   Performance monitoring, metrics, and error tracking of web applications.

$$$glossary-recovery$$$ recovery
:   Process of syncing a [replica shard](/reference/glossary/index.md#glossary-replica-shard) from a [primary shard](/reference/glossary/index.md#glossary-primary-shard). Upon completion, the replica shard is available for searches.

$$$glossary-reindex$$$ reindex
:   Copies documents from a source to a destination. The source and destination can be a [data stream](/reference/glossary/index.md#glossary-data-stream), [index](/reference/glossary/index.md#glossary-index), or [alias](/reference/glossary/index.md#glossary-alias).

$$$glossary-remote-cluster$$$ remote cluster
:   A separate [cluster](/reference/glossary/index.md#glossary-cluster), often in a different data center or locale, that contains [indices](/reference/glossary/index.md#glossary-index) that can be replicated or searched by the [local cluster](/reference/glossary/index.md#glossary-local-cluster). The connection to a remote cluster is unidirectional. See [Remote clusters](/deploy-manage/remote-clusters/remote-clusters-self-managed.md).

$$$glossary-replica-shard$$$ replica shard
:   Copy of a [primary shard](/reference/glossary/index.md#glossary-primary-shard). Replica shards can improve search performance and resiliency by distributing data across multiple [nodes](/reference/glossary/index.md#glossary-node). See [Clusters, nodes, and shards](/deploy-manage/production-guidance/getting-ready-for-production-elasticsearch.md).

$$$glossary-roles-token$$$ roles token
:   Enables a host to join an existing {{ece}} installation and grants permission to hosts to hold certain roles, such as the [allocator](/reference/glossary/index.md#glossary-allocator) role. Used when installing {{ece}} on additional hosts, a roles token helps secure {{ece}} by making sure that only authorized hosts become part of the installation.

$$$glossary-rollover$$$ rollover
:   Creates a new write index when the current one reaches a certain size, number of docs, or age. A rollover can target a [data stream](/reference/glossary/index.md#glossary-data-stream) or an [alias](/reference/glossary/index.md#glossary-alias) with a write index.

$$$glossary-rollup-index$$$ rollup index
:   Special type of [index](/reference/glossary/index.md#glossary-index) for storing historical data at reduced granularity. Documents are summarized and indexed into a rollup index by a [rollup job](/reference/glossary/index.md#glossary-rollup-job). See [Rolling up historical data](/manage-data/lifecycle/rollup.md).

$$$glossary-rollup-job$$$ {{rollup-job}}
:   Background task that runs continuously to summarize documents in an [index](/reference/glossary/index.md#glossary-index) and index the summaries into a separate rollup index. The job configuration controls what data is rolled up and how often. See [Rolling up historical data](/manage-data/lifecycle/rollup.md).

$$$glossary-rollup$$$ rollup
:   Summarizes high-granularity data into a more compressed format to maintain access to historical data in a cost-effective way. See [Roll up your data](/manage-data/lifecycle/rollup.md).

$$$glossary-routing$$$ routing
:   Process of sending and retrieving data from a specific [primary shard](/reference/glossary/index.md#glossary-primary-shard). {{es}} uses a hashed routing value to choose this shard. You can provide a routing value in [indexing](/reference/glossary/index.md#glossary-index) and search requests to take advantage of caching. See the [`_routing` field](elasticsearch://docs/reference/elasticsearch/mapping-reference/mapping-routing-field.md).

$$$glossary-rule$$$ rule
:   A set of [conditions](/reference/glossary/index.md#glossary-condition), schedules, and [actions](/reference/glossary/index.md#glossary-action) that enable notifications. See [{{rules-ui}}](/reference/glossary/index.md#glossary-rules).

$$$glossary-rules$$$ Rules
:   A comprehensive view of all your alerting rules. Enables you to access and manage rules for all {{kib}} apps from one place. See [{{rules-ui}}](/explore-analyze/alerts-cases.md).

$$$glossary-runner$$$ runner
:   A local control agent that runs on all hosts, used to deploy local containers based on role definitions. Ensures that containers assigned to it exist and are able to run, and creates or recreates the containers if necessary.

$$$glossary-runtime-fields$$$ runtime field
:   [Field](/reference/glossary/index.md#glossary-field) that is evaluated at query time. You access runtime fields from the search API like any other field, and {{es}} sees runtime fields no differently. See [Runtime fields](/manage-data/data-store/mapping/runtime-fields.md).


## S [s-glos]

$$$glossary-saved-object$$$ saved object
:   A representation of a dashboard, visualization, map, data view, or Canvas workpad that can be stored and reloaded.

$$$glossary-saved-search$$$ saved search
:   The query text, filters, and time filter that make up a search, saved for later retrieval and reuse.

$$$glossary-scripted-field$$$ scripted field
:   A field that computes data on the fly from the data in {{es}} indices. Scripted field data is shown in Discover and used in visualizations.

$$$glossary-search-session$$$ search session
:   A group of one or more queries that are executed asynchronously. The results of the session are stored for a period of time, so you can recall the query. Search sessions are user specific.

$$$glossary-search-template$$$ search template
:   A stored search you can run with different variables. See [Search templates](/solutions/search/search-templates.md).

$$$glossary-searchable-snapshot-index$$$ searchable snapshot index
:   [Index](/reference/glossary/index.md#glossary-index) whose data is stored in a [snapshot](/reference/glossary/index.md#glossary-snapshot). Searchable snapshot indices do not need [replica shards](/reference/glossary/index.md#glossary-replica-shard) for resilience, since their data is reliably stored outside the cluster. See [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md).

$$$glossary-searchable-snapshot$$$ searchable snapshot
:   [Snapshot](/reference/glossary/index.md#glossary-snapshot) of an [index](/reference/glossary/index.md#glossary-index) mounted as a [searchable snapshot index](/reference/glossary/index.md#glossary-searchable-snapshot-index). You can search this index like a regular index. See [searchable snapshots](/deploy-manage/tools/snapshot-and-restore/searchable-snapshots.md).

$$$glossary-segment$$$ segment
:   Data file in a [shard](/reference/glossary/index.md#glossary-shard)'s Lucene instance. {{es}} manages Lucene segments automatically.

$$$glossary-services-forwarder$$$ services forwarder
:   Routes data internally in an {{ece}} installation.

$$$glossary-shard$$$ shard
:   Lucene instance containing some or all data for an [index](/reference/glossary/index.md#glossary-index). {{es}} automatically creates and manages these Lucene instances. There are two types of shards: [primary](/reference/glossary/index.md#glossary-primary-shard) and [replica](/reference/glossary/index.md#glossary-replica-shard). See [Clusters, nodes, and shards](/deploy-manage/production-guidance/getting-ready-for-production-elasticsearch.md).

$$$glossary-shareable$$$ shareable
:   A Canvas workpad that can be embedded on any webpage. Shareables enable you to display Canvas visualizations on internal wiki pages or public websites.

$$$glossary-shipper$$$ shipper
:   An instance of {{ls}} that send events to another instance of {{ls}}, or some other application.

$$$glossary-shrink$$$ shrink
:   Reduces the number of [primary shards](/reference/glossary/index.md#glossary-primary-shard) in an index.

$$$glossary-snapshot-lifecycle-policy$$$ snapshot lifecycle policy
:   Specifies how frequently to perform automatic backups of a cluster and how long to retain the resulting [snapshots](/reference/glossary/index.md#glossary-snapshot). See [Automate snapshots with {{slm-init}}](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm).

$$$glossary-snapshot-repository$$$ snapshot repository
:   Location where [snapshots](/reference/glossary/index.md#glossary-snapshot) are stored. A snapshot repository can be a shared filesystem or a remote repository, such as Azure or Google Cloud Storage. See [Snapshot and restore](/deploy-manage/tools/snapshot-and-restore.md).

$$$glossary-snapshot$$$ snapshot
:   Backup taken of a running [cluster](/reference/glossary/index.md#glossary-cluster). You can take snapshots of the entire cluster or only specific [data streams](/reference/glossary/index.md#glossary-data-stream) and [indices](/reference/glossary/index.md#glossary-index). See [Snapshot and restore](/deploy-manage/tools/snapshot-and-restore.md).

$$$glossary-solution$$$ solution
:   In {{ecloud}}, deployments with specialized [templates](/reference/glossary/index.md#glossary-deployment-template) that are pre-configured with sensible defaults and settings for common use cases.

$$$glossary-source_field$$$ source field
:   Original JSON object provided during [indexing](/reference/glossary/index.md#glossary-index). See the [`_source` field](elasticsearch://docs/reference/elasticsearch/mapping-reference/mapping-source-field.md).

$$$glossary-space$$$ space
:   A place for organizing [dashboards](/reference/glossary/index.md#glossary-dashboard), [visualizations](/reference/glossary/index.md#glossary-visualization), and other [saved objects](/reference/glossary/index.md#glossary-saved-object) by category. For example, you might have different spaces for each team, use case, or individual. See [Spaces](/deploy-manage/manage-spaces.md).

$$$glossary-span$$$ span
:   Information about the execution of a specific code path. [Spans](/solutions/observability/apps/spans.md) measure from the start to the end of an activity and can have a parent/child relationship with other spans.

$$$glossary-split$$$ split
:   Adds more [primary shards](/reference/glossary/index.md#glossary-primary-shard) to an [index](/reference/glossary/index.md#glossary-index).

$$$glossary-stack-alert$$$ stack rule
:   The general purpose rule types {{kib}} provides out of the box. Refer to [Stack rules](/explore-analyze/alerts-cases/alerts/rule-types.md#stack-rules).

$$$glossary-standalone$$$ standalone
:   This mode allows manual configuration and management of {{agent}}s locally on the systems where they are installed. See [Install standalone {{agent}}s](/reference/ingestion-tools/fleet/install-standalone-elastic-agent.md).

$$$glossary-stunnel$$$ stunnel
:   Securely tunnels all traffic in an {{ece}} installation.

$$$glossary-system-index$$$ system index
:   [Index](/reference/glossary/index.md#glossary-index) containing configurations and other data used internally by the {{stack}}. System index names start with a dot (`.`), such as `.security`. Do not directly access or change system indices.


## T [t-glos]

$$$glossary-tag$$$ tag
:   A keyword or label that you assign to {{kib}} saved objects, such as dashboards and visualizations, so you can classify them in a way that is meaningful to you. Tags makes it easier for you to manage your content. See [Tags](/explore-analyze/find-and-organize/tags.md).

$$$glossary-term-join$$$ term join
:   A shared key that combines vector features with the results of an {{es}} terms aggregation. Term joins augment vector features with properties for data-driven styling and rich tooltip content in maps.

$$$glossary-term$$$ term
:   See [token](/reference/glossary/index.md#glossary-token).

$$$glossary-text$$$ text
:   Unstructured content, such as a product description or log message. You typically [analyze](/reference/glossary/index.md#glossary-analysis) text for better search. See [Text analysis](/manage-data/data-store/text-analysis.md).

$$$glossary-time-filter$$$ time filter
:   A {{kib}} control that constrains the search results to a particular time period.

$$$glossary-time-series-data-stream$$$ time series data stream
:   A type of [data stream](/reference/glossary/index.md#glossary-data-stream) optimized for indexing metrics [time series data](/reference/glossary/index.md#glossary-time-series-data). A TSDS allows for reduced storage size and for a sequence of metrics data points to be considered efficiently as a whole. See [Time series data stream](/manage-data/data-store/data-streams/time-series-data-stream-tsds.md).

$$$glossary-time-series-data$$$ time series data
:   A series of data points, such as logs, metrics and events, that is indexed in time order. Time series data can be indexed in a [data stream](/reference/glossary/index.md#glossary-data-stream), where it can be accessed as a single named resource with the data stored across multiple backing indices. A [time series data stream](/reference/glossary/index.md#glossary-time-series-data-stream) is optimized for indexing metrics data.

$$$glossary-timelion$$$ Timelion
:   A tool for building a time series visualization that analyzes data in time order. See [Timelion](/explore-analyze/dashboards.md).

$$$glossary-token$$$ token
:   A chunk of unstructured [text](/reference/glossary/index.md#glossary-text) that's been optimized for search. In most cases, tokens are individual words. Tokens are also called terms. See [Text analysis](/manage-data/data-store/text-analysis.md).

$$$glossary-tokenization$$$ tokenization
:   Process of breaking unstructured text down into smaller, searchable chunks called [tokens](/reference/glossary/index.md#glossary-token). See [Tokenization](/manage-data/data-store/text-analysis.md#tokenization).

$$$glossary-trace$$$ trace
:   Defines the amount of time an application spends on a request. Traces are made up of a collection of transactions and spans that have a common root.

$$$glossary-tracks$$$ tracks
:   A layer type in the **Maps** application. This layer converts a series of point locations into a line, often representing a path or route.

$$$glossary-trained-model$$$ trained model
:   A {{ml}} model that is trained and tested against a labeled data set and can be referenced in an ingest pipeline or in a pipeline aggregation to perform {{classification}} or {{reganalysis}} or [{{nlp}}](/reference/glossary/index.md#glossary-nlp) on new data.

$$$glossary-transaction$$$ transaction
:   A special kind of [span](/reference/glossary/index.md#glossary-span) that has additional attributes associated with it. [Transactions](/solutions/observability/apps/transactions.md) describe an event captured by an Elastic [APM agent](/reference/glossary/index.md#glossary-apm-agent) instrumenting a service.

$$$glossary-tsvb$$$ TSVB
:   A time series data visualizer that allows you to combine an infinite number of aggregations to display complex data. See [TSVB](/explore-analyze/dashboards.md).


## U [u-glos]

$$$glossary-upgrade-assistant$$$ Upgrade Assistant
:   A tool that helps you prepare for an upgrade to the next major version of {{es}}. The assistant identifies the deprecated settings in your cluster and indices and guides you through resolving issues, including reindexing. See [Upgrade Assistant](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md).

$$$glossary-uptime$$$ Uptime
:   A metric of system reliability used to monitor the status of network endpoints via HTTP/S, TCP, and ICMP.


## V [v-glos]

$$$glossary-vcpu$$$ vCPU
:   vCPU stands for virtual central processing unit. In {{ecloud}}, vCPUs are virtual compute units assigned to your nodes. The value is dependent on the size and hardware profile of the instance. The instance may be eligible for vCPU boosting depending on the size.

$$$glossary-vector$$$ vector data
:   Points, lines, and polygons used to represent a map.

$$$glossary-vega$$$ Vega
:   A declarative language used to create interactive visualizations. See [Vega](/explore-analyze/dashboards.md).

$$$glossary-visualization$$$ visualization
:   A graphical representation of query results in {{kib}} (e.g., a histogram, line graph, pie chart, or heat map).


## W [w-glos]

$$$glossary-warm-phase$$$ warm phase
:   Second possible phase in the [index lifecycle](/reference/glossary/index.md#glossary-index-lifecycle). In the warm phase, an [index](/reference/glossary/index.md#glossary-index) is generally optimized for search and no longer updated. See [Index lifecycle](/manage-data/lifecycle/index-lifecycle-management/index-lifecycle.md).

$$$glossary-warm-tier$$$ warm tier
:   [Data tier](/reference/glossary/index.md#glossary-data-tier) that contains [nodes](/reference/glossary/index.md#glossary-node) that hold time series data that is accessed less frequently and rarely needs to be updated. See [Data tiers](/manage-data/lifecycle/data-tiers.md).

$$$glossary-watcher$$$ Watcher
:   The original suite of alerting features. See [Watcher](/explore-analyze/alerts-cases/watcher.md).

$$$glossary-wms$$$ Web Map Service (WMS)
:   A layer type in the **Maps** application. Add a WMS source to provide authoritative geographic context to your map. See the [OpenGIS Web Map Service](https://www.ogc.org/standards/wms).

$$$glossary-worker$$$ worker
:   The filter thread model used by {{ls}}, where each worker receives an [event](/reference/glossary/index.md#glossary-event) and applies all filters, in order, before emitting the event to the output queue. This allows scalability across CPUs because many filters are CPU intensive.

$$$glossary-workpad$$$ workpad
:   A workspace where you build presentations of your live data in [Canvas](/reference/glossary/index.md#glossary-canvas). See [Create a workpad](/explore-analyze/visualize/canvas.md).


## X [x-glos]


## Y [y-glos]


## Z [z-glos]

$$$glossary-zookeeper$$$ ZooKeeper
:   A coordination service for distributed systems used by {{ece}} to store the state of the installation. Responsible for discovery of hosts, resource allocation, leader election after failure and high priority notifications.
