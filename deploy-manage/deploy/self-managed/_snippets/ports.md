This table shows the ports that must be accessible in order to operate an {{es}} cluster. The {{es}} REST and {{kib}} interfaces must be open to external users in order for the cluster to be usable. The transport API must be accessible between {{es}} nodes in the cluster, and to any external clients using the transport API. 

By default, {{es}} will try to listen to the first port in the specified range. If the port is taken, it will try the next one.

These settings can be overridden in the relevant configuration file.

| Port | Access type | Purpose | Setting |
| --- | --- | --- | --- |
| 9200 and onwards | HTTP (REST) | REST API for Elasticsearch. This is the primary interface used for access to the cluster from external sources, including {{kib}} and {{ls}}. | Elasticsearch [`http.port`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#common-network-settings) |
| 9300 and onwards | TCP |	Transport API. Used for intra-cluster communications and client access via the transport API (Java client). | Elasticsearch [`transport.port`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#common-network-settings) |
| 5601 | HTTP |	{{kib}} default access port. | Kibana [`server.port`](kibana://reference/configuration-reference/general-settings.md#server-port) |

Additional ports might be required for [optional {{stack}} components](/get-started/the-stack.md). Refer to the installation guide for the component that you want to install.