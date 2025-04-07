If you're deploying the {{stack}} in a self-managed cluster, then install the {{stack}} products you want to use in the following order:

* [{{es}}](/deploy-manage/deploy/self-managed/installing-elasticsearch.md)
* [{{kib}}](/deploy-manage/deploy/self-managed/install-kibana.md)
* [Logstash](logstash://reference/index.md)
* [{{agent}}](/reference/fleet/index.md) or [Beats](beats://reference/index.md)
* [APM](/solutions/observability/apps/application-performance-monitoring-apm.md)
* [Elasticsearch Hadoop](elasticsearch-hadoop://reference/index.md)

Installing in this order ensures that the components each product depends on are in place.