# Bootstrap Checks [bootstrap-checks]

Collectively, we have a lot of experience with users suffering unexpected issues because they have not configured [important settings](../../../deploy-manage/deploy/self-managed/important-settings-configuration.md). In previous versions of Elasticsearch, misconfiguration of some of these settings were logged as warnings. Understandably, users sometimes miss these log messages. To ensure that these settings receive the attention that they deserve, Elasticsearch has bootstrap checks upon startup.

These bootstrap checks inspect a variety of Elasticsearch and system settings and compare them to values that are safe for the operation of Elasticsearch. If Elasticsearch is in development mode, any bootstrap checks that fail appear as warnings in the Elasticsearch log. If Elasticsearch is in production mode, any bootstrap checks that fail will cause Elasticsearch to refuse to start.

There are some bootstrap checks that are always enforced to prevent Elasticsearch from running with incompatible settings. These checks are documented individually.


## Development vs. production mode [dev-vs-prod-mode] 

By default, {{es}} binds to loopback addresses for [HTTP and transport (internal) communication](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-network.html). This is fine for downloading and playing with {{es}} as well as everyday development, but it’s useless for production systems. To join a cluster, an {{es}} node must be reachable via transport communication. To join a cluster via a non-loopback address, a node must bind transport to a non-loopback address and not be using [single-node discovery](../../../deploy-manage/deploy/self-managed/bootstrap-checks.md#single-node-discovery). Thus, we consider an Elasticsearch node to be in development mode if it can not form a cluster with another machine via a non-loopback address, and is otherwise in production mode if it can join a cluster via non-loopback addresses.

Note that HTTP and transport can be configured independently via [`http.host`](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-network.html#http-settings) and [`transport.host`](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-network.html#transport-settings); this can be useful for configuring a single node to be reachable via HTTP for testing purposes without triggering production mode.


## Single-node discovery [single-node-discovery] 

We recognize that some users need to bind the transport to an external interface for testing a remote-cluster configuration. For this situation, we provide the discovery type `single-node` (configure it by setting `discovery.type` to `single-node`); in this situation, a node will elect itself master and will not join a cluster with any other node.


## Forcing the bootstrap checks [_forcing_the_bootstrap_checks] 

If you are running a single node in production, it is possible to evade the bootstrap checks (either by not binding transport to an external interface, or by binding transport to an external interface and setting the discovery type to `single-node`). For this situation, you can force execution of the bootstrap checks by setting the system property `es.enforce.bootstrap.checks` to `true` in the [JVM options](https://www.elastic.co/guide/en/elasticsearch/reference/current/advanced-configuration.html#set-jvm-options). We strongly encourage you to do this if you are in this specific situation. This system property can be used to force execution of the bootstrap checks independent of the node configuration.















