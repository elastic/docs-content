# Upgrade Elastic on self-managed infrastructure

If you've installed the {{stack}} on your own self-managed infrastructure, once you're [prepare to upgrade](/deploy-manage/upgrade/deployment-or-cluster.md#prepare-to-upgrade), you'll need to upgrade each of your Elastic components individually. 

It's important that you upgrade your components in this order: 
* [{{es}}](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md)
* [{{kib}}](/deploy-manage/upgrade/deployment-or-cluster/kibana.md)
* [Elastic APM](../../../solutions/observability/apps/upgrade.md)
* [Ingest components](/deploy-manage/upgrade/ingest-components.md)

:::{important}
If you are using {{ls}} and the `logstash-filter-elastic_integration plugin` to extend Elastic integrations, upgrade Logstash (or the `logstash-filter-elastic_integration` plugin specifically) *before* you upgrade Kibana.

The Elasticsearch-Logstash-Kibana installation order for this specific plugin ensures the best experience with Elastic Agent-managed pipelines, and embeds functionality from a version of {{es}} Ingest Node that is compatible with the plugin version (`major.minor`).
