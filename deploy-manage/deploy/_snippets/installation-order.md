If you're deploying the {{stack}} in a self-managed cluster, then install the {{stack}} products you want to use in the following order:

* [{{es}}](/deploy-manage/deploy/self-managed/installing-elasticsearch.md)
* [{{kib}}](/deploy-manage/deploy/self-managed/install-kibana.md)
* [Logstash](logstash://reference/index.md)
* [{{agent}}](/reference/fleet/index.md) or [Beats](beats://reference/index.md)
* [APM](/solutions/observability/apm/index.md)
* [{{es}} Hadoop](elasticsearch-hadoop://reference/index.md)

Installing in this order ensures that the components each product depends on are in place.

:::{tip}
If you're deploying a production environment and you plan to use [trusted CA-signed certificates](/deploy-manage/security/self-setup.md#manual-configuration) for {{es}}, then you should do so before you deploy {{fleet}} and {{agent}}. If new security certificates are configured, any {{agent}}s need to be reinstalled, so we recommend that you set up {{fleet}} and {{agent}} with the appropriate certificates in place.
:::