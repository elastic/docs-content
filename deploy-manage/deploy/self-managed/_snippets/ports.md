This table shows the ports that must be accessible in order to operate an {{es}} cluster. The {{es}} REST and {{kib}} interfaces must be open to external users in order for the cluster to be usable. The transport API must be accessible between {{es}} nodes in the cluster, and to any external clients using the transport API. 

These settings can be overridden in the relevant configuration file.

| Port | Access type | Purpose | Setting |
| --- | --- | --- | --- |
| 9200-9300	| HTTP (REST) | REST API for Elasticsearch. This is the primary interface used for access to the cluster from external sources, including {{kib}} and {{ls}}. | Elasticsearch [`http.port`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#common-network-settings) |
| 9300-9400	| TCP |	Transport API. Used for intra-cluster communications and client access via the transport API (Java client). | Elasticsearch [`transport.port`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#common-network-settings) |
| 5601 | HTTP |	{{kib}} default access port. | Kibana [`server.port`](kibana:///reference/elasticsearch/configuration-reference/general-settings.md#server-port) |