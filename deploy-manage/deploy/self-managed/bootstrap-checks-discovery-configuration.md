---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-discovery-configuration.html
---

# Discovery configuration check [bootstrap-checks-discovery-configuration]

By default, when Elasticsearch first starts up it will try and discover other nodes running on the same host. If no elected master can be discovered within a few seconds then Elasticsearch will form a cluster that includes any other nodes that were discovered. It is useful to be able to form this cluster without any extra configuration in development mode, but this is unsuitable for production because it’s possible to form multiple clusters and lose data as a result.

This bootstrap check ensures that discovery is not running with the default configuration. It can be satisfied by setting at least one of the following properties:

* `discovery.seed_hosts`
* `discovery.seed_providers`
* `cluster.initial_master_nodes`

Note that you must [remove `cluster.initial_master_nodes` from the configuration of every node](important-settings-configuration.md#initial_master_nodes) after the cluster has started for the first time. Instead, configure `discovery.seed_hosts` or `discovery.seed_providers`. If you do not need any discovery configuration, for instance if running a single-node cluster, set `discovery.seed_hosts: []` to disable discovery and satisfy this bootstrap check.

