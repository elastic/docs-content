---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-inputs-list.html
---

# Elastic Agent inputs [elastic-agent-inputs-list]

When you [configure inputs](/reference/ingestion-tools/fleet/elastic-agent-input-configuration.md) for standalone {{agents}}, the following values are supported for the input `type` parameter.

**Expand any section to view the available inputs:**

::::{dropdown} Audit the activities of users and processes on your systems
:name: elastic-agent-inputs-list-auditbeat

| Input | Description | Learn more |
| --- | --- | --- |
| `audit/auditd` | Receives audit events from the Linux Audit Framework that is a part of the Linux kernel. | [Auditd Module](beats://docs/reference/auditbeat/auditbeat-module-auditd.md) ({{auditbeat}} docs) |
| `audit/file_integrity` | Sends events when a file is changed (created, updated, or deleted) on disk. The events contain file metadata and hashes. | [File Integrity Module](beats://docs/reference/auditbeat/auditbeat-module-file_integrity.md) ({{auditbeat}} docs) |
| `audit/system` | [beta] Collects various security related information about a system. All datasets send both periodic state information (e.g. all currently running processes) and real-time changes (e.g. when a new process starts or stops). | [System Module](beats://docs/reference/auditbeat/auditbeat-module-system.md) ({{auditbeat}} docs) |

::::


::::{dropdown} Collect metrics from operating systems and services running on your servers
:name: elastic-agent-inputs-list-metricbeat

| Input | Description | Learn more |
| --- | --- | --- |
| `activemq/metrics` | Periodically fetches JMX metrics from Apache ActiveMQ. | [ActiveMQ module](beats://docs/reference/metricbeat/metricbeat-module-activemq.md) ({{metricbeat}} docs) |
| `apache/metrics` | Periodically fetches metrics from [Apache HTTPD](https://httpd.apache.org/) servers. | [Apache module](beats://docs/reference/metricbeat/metricbeat-module-apache.md) ({{metricbeat}} docs) |
| `aws/metrics` | Periodically fetches monitoring metrics from AWS CloudWatch using [GetMetricData API](https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_GetMetricData.md) for AWS services. | [AWS module](beats://docs/reference/metricbeat/metricbeat-module-aws.md) ({{metricbeat}} docs) |
| `awsfargate/metrics` | [beta] Retrieves various metadata, network metrics, and Docker stats about tasks and containers. | [AWS Fargate module](beats://docs/reference/metricbeat/metricbeat-module-awsfargate.md) ({{metricbeat}} docs) |
| `azure/metrics` | Collects and aggregates Azure logs and metrics from a variety of sources into a common data platform where it can be used for analysis, visualization, and alerting. | [Azure module](beats://docs/reference/metricbeat/metricbeat-module-azure.md) ({{metricbeat}} docs) |
| `beat/metrics` | Collects metrics about any Beat or other software based on libbeat. | [Beat module](beats://docs/reference/metricbeat/metricbeat-module-beat.md) ({{metricbeat}} docs) |
| `cloudfoundry/metrics` | Connects to Cloud Foundry loggregator to gather container, counter, and value metrics into a common data platform where it can be used for analysis, visualization, and alerting. | [Cloudfoundry module](beats://docs/reference/metricbeat/metricbeat-module-cloudfoundry.md) ({{metricbeat}} docs) |
| `containerd/metrics` | [beta] Collects cpu, memory and blkio statistics about running containers controlled by containerd runtime. | [Containerd module](beats://docs/reference/metricbeat/metricbeat-module-containerd.md) ({{metricbeat}} docs) |
| `docker/metrics` | Fetches metrics from [Docker](https://www.docker.com/) containers. | [Docker module](beats://docs/reference/metricbeat/metricbeat-module-docker.md) ({{metricbeat}} docs) |
| `elasticsearch/metrics` | Collects metrics about {{es}}. | [Elasticsearch module](beats://docs/reference/metricbeat/metricbeat-module-elasticsearch.md) ({{metricbeat}} docs) |
| `etcd/metrics` | This module targets Etcd V2 and V3. When using V2, metrics are collected using [Etcd v2 API](https://coreos.com/etcd/docs/latest/v2/api.md). When using V3, metrics are retrieved from the `/metrics`` endpoint as intended for [Etcd v3](https://coreos.com/etcd/docs/latest/metrics.md). | [Etcd module](beats://docs/reference/metricbeat/metricbeat-module-etcd.md) ({{metricbeat}} docs) |
| `gcp/metrics` | Periodically fetches monitoring metrics from Google Cloud Platform using [Stackdriver Monitoring API](https://cloud.google.com/monitoring/api/metrics_gcp) for Google Cloud Platform services. | [Google Cloud Platform module](beats://docs/reference/metricbeat/metricbeat-module-gcp.md) ({{metricbeat}} docs) |
| `haproxy/metrics` | Collects stats from [HAProxy](http://www.haproxy.org/). It supports collection from TCP sockets, UNIX sockets, or HTTP with or without basic authentication. | [HAProxy module](beats://docs/reference/metricbeat/metricbeat-overview.md) ({{metricbeat}} docs) |
| `http/metrics` | Used to call arbitrary HTTP endpoints for which a dedicated Metricbeat module is not available. | [HTTP module](beats://docs/reference/metricbeat/metricbeat-module-http.md) ({{metricbeat}} docs) |
| `iis/metrics` | Periodically retrieve IIS web server related metrics. | [IIS module](beats://docs/reference/metricbeat/metricbeat-module-iis.md) ({{metricbeat}} docs) |
| `jolokia/metrics` | Collects metrics from [Jolokia agents](https://jolokia.org/reference/html/agents.md) running on a target JMX server or dedicated proxy server. | [Jolokia module](beats://docs/reference/metricbeat/metricbeat-module-jolokia.md) ({{metricbeat}} docs) |
| `kafka/metrics` | Collects metrics from the [Apache Kafka](https://kafka.apache.org/intro) event streaming platform. | [Kafka module](beats://docs/reference/metricbeat/metricbeat-module-kafka.md) ({{metricbeat}} docs) |
| `kibana/metrics` | Collects metrics about {{Kibana}}. | [{{kib}} module](beats://docs/reference/metricbeat/metricbeat-module-kibana.md) ({{metricbeat}} docs) |
| `kubernetes/metrics` | As one of the main pieces provided for Kubernetes monitoring, this module is capable of fetching metrics from several components. | [Kubernetes module](beats://docs/reference/metricbeat/metricbeat-module-kubernetes.md) ({{metricbeat}} docs) |
| `linux/metrics` | [beta] Reports on metrics exclusive to the Linux kernel and GNU/Linux OS. | [Linux module](beats://docs/reference/metricbeat/metricbeat-module-linux.md) ({{metricbeat}} docs) |
| `logstash/metrics` | collects metrics about {{ls}}. | [{{ls}} module](beats://docs/reference/metricbeat/metricbeat-module-logstash.md) ({{metricbeat}} docs) |
| `memcached/metrics` | Collects metrics about the [memcached](https://memcached.org/) memory object caching system. | [Memcached module](beats://docs/reference/metricbeat/metricbeat-module-memcached.md) ({{metricbeat}} docs) |
| `mongodb/metrics` | Periodically fetches metrics from [MongoDB](https://www.mongodb.com/) servers. | [MongoDB module](beats://docs/reference/metricbeat/metricbeat-module-mongodb.md) ({{metricbeat}} docs) |
| `mssql/metrics` | The [Microsoft SQL 2017](https://www.microsoft.com/en-us/sql-server/sql-server-2017) Metricbeat module. It is still under active development to add new Metricsets and introduce enhancements. | [MSSQL module](beats://docs/reference/metricbeat/metricbeat-module-mssql.md) ({{metricbeat}} docs) |
| `mysql/metrics` | Periodically fetches metrics from [MySQL](https://www.mysql.com/) servers. | [MySQL module](beats://docs/reference/metricbeat/metricbeat-module-mysql.md) ({{metricbeat}} docs) |
| `nats/metrics` | Uses the [Nats monitoring server APIs](https://nats.io/documentation/managing_the_server/monitoring/) to collect metrics. | [NATS module](beats://docs/reference/metricbeat/metricbeat-module-nats.md) ({{metricbeat}} docs) |
| `nginx/metrics` | Periodically fetches metrics from [Nginx](https://nginx.org/) servers. | [Nginx module](beats://docs/reference/metricbeat/metricbeat-module-nginx.md) ({{metricbeat}} docs) |
| `oracle/metrics` | The [Oracle](https://www.oracle.com/) module for Metricbeat. It is under active development with feedback from the community. A single Metricset for Tablespace monitoring is added so the community can start gathering metrics from their nodes and contributing to the module. | [Oracle module](beats://docs/reference/metricbeat/metricbeat-module-oracle.md) ({{metricbeat}} docs) |
| `postgresql/metrics` | Periodically fetches metrics from [PostgreSQL](https://www.postgresql.org/) servers. | [PostgresSQL module](beats://docs/reference/metricbeat/metricbeat-module-postgresql.md) ({{metricbeat}} docs) |
| `prometheus/metrics` | Periodically scrapes metrics from [Prometheus exporters](https://prometheus.io/docs/instrumenting/exporters/). | [Prometheus module](beats://docs/reference/metricbeat/metricbeat-module-prometheus.md) ({{metricbeat}} docs) |
| `rabbitmq/metrics` | Uses the [HTTP API](http://www.rabbitmq.com/management.md) created by the management plugin to collect RabbitMQ metrics. | [RabbitMQ module](beats://docs/reference/metricbeat/metricbeat-module-rabbitmq.md) ({{metricbeat}} docs) |
| `redis/metrics` | Periodically fetches metrics from [Redis](http://redis.io/) servers. | [Redis module](beats://docs/reference/metricbeat/metricbeat-module-redis.md) ({{metricbeat}} docs) |
| `sql/metrics` | Allows you to execute custom queries against an SQL database and store the results in {{es}}. | [SQL module](beats://docs/reference/metricbeat/metricbeat-module-sql.md) ({{metricbeat}} docs) |
| `stan/metrics` | Uses [STAN monitoring server APIs](https://github.com/nats-io/nats-streaming-server/blob/master/server/monitor.go) to collect metrics. | [Stan module](beats://docs/reference/metricbeat/metricbeat-module-stan.md) ({{metricbeat}} docs) |
| `statsd/metrics` | Spawns a UDP server and listens for metrics in StatsD compatible format. | [Statsd module](beats://docs/reference/metricbeat/metricbeat-module-statsd.md) ({{metricbeat}} docs) |
| `syncgateway/metrics` | [beta] Monitor a Sync Gateway instance by using its REST API. | [SyncGateway module](beats://docs/reference/metricbeat/metricbeat-module-syncgateway.md) ({{metricbeat}} docs) |
| `system/metrics` | Allows you to monitor your server metrics, including CPU, load, memory, network, processes, sockets, filesystem, fsstat, uptime, and more. | [System module](beats://docs/reference/metricbeat/metricbeat-module-system.md) ({{metricbeat}} docs) |
| `traefik/metrics` | Periodically fetches metrics from a [Traefik](https://traefik.io/) instance. | [Traefik module](beats://docs/reference/metricbeat/metricbeat-module-traefik.md) ({{metricbeat}} docs) |
| `uwsgi/metrics` | By default, collects the uWSGI stats metricset, using [StatsServer](https://uwsgi-docs.readthedocs.io/en/latest/StatsServer.md). | [uWSGI module](beats://docs/reference/metricbeat/metricbeat-module-uwsgi.md) ({{metricbeat}} docs) |
| `vsphere/metrics` | Uses the [Govmomi](https://github.com/vmware/govmomi) library to collect metrics from any Vmware SDK URL (ESXi/VCenter). | [vSphere module](beats://docs/reference/metricbeat/metricbeat-module-vsphere.md) ({{metricbeat}} docs) |
| `windows/metrics` | Collects metrics from Windows systems. | [Windows module](beats://docs/reference/metricbeat/metricbeat-module-windows.md) ({{metricbeat}} docs) |
| `zookeeper/metrics` | Fetches statistics from the ZooKeeper service. | [ZooKeeper module](beats://docs/reference/metricbeat/metricbeat-module-zookeeper.md) ({{metricbeat}} docs) |

::::


::::{dropdown} Forward and centralize log data
:name: elastic-agent-inputs-list-filebeat

| Input | Description | Learn more |
| --- | --- | --- |
| `aws-cloudwatch` | Stores log filesfrom Amazon Elastic Compute Cloud(EC2), AWS CloudTrail, Route53, and other sources. | [AWS CloudWatch input](beats://docs/reference/filebeat/filebeat-input-aws-cloudwatch.md) ({{filebeat}} docs) |
| `aws-s3` | Retrieves logs from S3 objects that are pointed to by S3 notification events read from an SQS queue or directly polling list of S3 objects in an S3 bucket. | [AWS S3 input](beats://docs/reference/filebeat/filebeat-input-aws-s3.md) ({{filebeat}} docs) |
| `azure-blob-storage` | Reads content from files stored in containers which reside on your Azure Cloud. | [Azure Blob Storage](beats://docs/reference/filebeat/filebeat-input-azure-blob-storage.md) ({{filebeat}} docs) |
| `azure-eventhub` | Reads messages from an azure eventhub. | [Azure eventhub input](beats://docs/reference/filebeat/filebeat-input-azure-eventhub.md) ({{filebeat}} docs) |
| `cel` | Reads messages from a file path or HTTP API with a variety of payloads using the [Common Expression Language (CEL)](https://opensource.google.com/projects/cel) and the [mito](https://pkg.go.dev/github.com/elastic/mito/lib) CEL extension libraries. | [Common Expression Language input](beats://docs/reference/filebeat/filebeat-input-cel.md) ({{filebeat}} docs) |
| `cloudfoundry` | Gets HTTP access logs, container logs and error logs from Cloud Foundry. | [Cloud Foundry input](beats://docs/reference/filebeat/filebeat-input-cloudfoundry.md) ({{filebeat}} docs) |
| `cometd` | Streams the real-time events from a Salesforce generic subscription Push Topic. | [CometD input](beats://docs/reference/filebeat/filebeat-input-cometd.md) ({{filebeat}} docs) |
| `container` | Reads containers log files. | [Container input](beats://docs/reference/filebeat/filebeat-input-container.md) ({{filebeat}} docs) |
| `docker` | Alias for `container`. | - |
| `log/docker` | Alias for `container`. | n/a |
| `entity-analytics` | Collects identity assets, such as users, from external identity providers. | [Entity Analytics input](beats://docs/reference/filebeat/filebeat-input-entity-analytics.md) ({{filebeat}} docs) |
| `event/file` | Alias for `log`. | n/a |
| `event/tcp` | Alias for `tcp`. | n/a |
| `filestream` | Reads lines from active log files. Replaces and imporoves on the `log` input. | [filestream input](beats://docs/reference/filebeat/filebeat-input-filestream.md) ({{filebeat}} docs) |
| `gcp-pubsub` | Reads messages from a Google Cloud Pub/Sub topic subscription. | [GCP Pub/Sub input](beats://docs/reference/filebeat/filebeat-input-gcp-pubsub.md) ({{filebeat}} docs) |
| `gcs` | [beta] Reads content from files stored in buckets which reside on your Google Cloud. | [Google Cloud Storage input](beats://docs/reference/filebeat/filebeat-input-gcs.md) ({{filebeat}} docs) |
| `http_endpoint` | [beta] Initializes a listening HTTP server that collects incoming HTTP POST requests containing a JSON body. | [HTTP Endpoint input](beats://docs/reference/filebeat/filebeat-input-http_endpoint.md) ({{filebeat}} docs) |
| `httpjson` | Read messages from an HTTP API with JSON payloads. | [HTTP JSON input](beats://docs/reference/filebeat/filebeat-input-httpjson.md) ({{filebeat}} docs) |
| `journald` | [beta] A system service that collects and stores logging data. | [Journald input](beats://docs/reference/filebeat/filebeat-input-journald.md) ({{filebeat}} docs) |
| `kafka` | Reads from topics in a Kafka cluster. | [Kafka input](beats://docs/reference/filebeat/filebeat-input-kafka.md) ({{filebeat}} docs) |
| `log` | DEPRECATED: Please use the `filestream` input instead. | n/a |
| `logfile` | Alias for `log`. | n/a |
| `log/redis_slowlog` | Alias for `redis`. | n/a |
| `log/syslog` | Alias for `syslog`. | n/a |
| `mqtt` | Reads data transmitted using lightweight messaging protocol for small and mobile devices, optimized for high-latency or unreliable networks. | [MQTT input](beats://docs/reference/filebeat/filebeat-input-mqtt.md) ({{filebeat}} docs) |
| `netflow` | Reads NetFlow and IPFIX exported flows and options records over UDP. | [NetFlow input](beats://docs/reference/filebeat/filebeat-input-netflow.md) ({{filebeat}} docs) |
| `o365audit` | [beta] Retrieves audit messages from Office 365 and Azure AD activity logs. | [Office 365 Management Activity API input](beats://docs/reference/filebeat/filebeat-input-o365audit.md) ({{filebeat}} docs) |
| `osquery` | Collects and decodes the result logs written by [osqueryd](https://osquery.readthedocs.io/en/latest/introduction/using-osqueryd/) in the JSON format. | - |
| `redis` | [beta] Reads entries from Redis slowlogs. | [Redis input](beats://docs/reference/filebeat/filebeat-overview.md) ({{filebeat}} docs) |
| `syslog` | Reads Syslog events as specified by RFC 3164 and RFC 5424, over TCP, UDP, or a Unix stream socket. | [Syslog input](beats://docs/reference/filebeat/filebeat-input-syslog.md) ({{filebeat}} docs) |
| `tcp` | Reads events over TCP. | [TCP input](beats://docs/reference/filebeat/filebeat-input-tcp.md) ({{filebeat}} docs) |
| `udp` | Reads events over UDP. | [UDP input](beats://docs/reference/filebeat/filebeat-input-udp.md) ({{filebeat}} docs) |
| `unix` | [beta] Reads events over a stream-oriented Unix domain socket. | [Unix input](beats://docs/reference/filebeat/filebeat-overview.md) ({{filebeat}} docs) |
| `winlog` | Reads from one or more event logs using Windows APIs, filters the events based on user-configured criteria, then sends the event data to the configured outputs ({{es}} or {{ls}}). | [Winlogbeat Overview](beats://docs/reference/winlogbeat/_winlogbeat_overview.md) ({{winlogbeat}} docs) |

::::


::::{dropdown} Monitor the status of your services
:name: elastic-agent-inputs-list-heartbeat

| Input | Description | Learn more |
| --- | --- | --- |
| `synthetics/http` | Connect via HTTP and optionally verify that the host returns the expected response. | [HTTP options](beats://docs/reference/heartbeat/monitor-http-options.md) ({{heartbeat}} docs) |
| `synthetics/icmp` | Use ICMP (v4 and v6) Echo Requests to check the configured hosts. | [ICMP options](beats://docs/reference/heartbeat/monitor-icmp-options.md) ({{heartbeat}} docs) |
| `synthetics/tcp` | Connect via TCP and optionally verify the endpoint by sending and/or receiving a custom payload. | [TCP options](beats://docs/reference/heartbeat/monitor-tcp-options.md) ({{heartbeat}} docs) |

::::


::::{dropdown} View network traffic between the servers of your network
:name: elastic-agent-inputs-list-packetbeat

| Input | Description | Learn more |
| --- | --- | --- |
| `packet` | Sniffs the traffic between your servers, parses the application-level protocols on the fly, and correlates the messages into transactions. | [Packetbeat overview](beats://docs/reference/packetbeat/packetbeat-overview.md) ({{packetbeat}} docs) |

::::


