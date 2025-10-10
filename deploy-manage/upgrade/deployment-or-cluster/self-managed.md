---
navigation_title: Upgrade Elastic on a self-managed cluster
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
  - id: kibana
---

# Upgrade the {{stack}} on a self-managed cluster

If you've installed the {{stack}} on your own self-managed infrastructure, once you're [prepared to upgrade](/deploy-manage/upgrade/prepare-to-upgrade.md), you'll need to upgrade each of your Elastic components individually.

It's important that you upgrade your components in this order:
* [{{es}}](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md)
* [{{kib}}](/deploy-manage/upgrade/deployment-or-cluster/kibana.md)
* [Elastic APM](/solutions/observability/apm/upgrade.md)
* [Ingest components](/deploy-manage/upgrade/ingest-components.md)

:::{important}
If you're using {{ls}} and the `logstash-filter-elastic_integration` [plugin](logstash-docs-md://lsr/plugins-filters-elastic_integration.md) to extend Elastic integrations, upgrade {{ls}} (or the `logstash-filter-elastic_integration` plugin specifically) *before* you upgrade {{kib}}.

The {{es}} → {{ls}} → {{kib}} installation order for this specific plugin ensures the best experience with {{agent}}-managed pipelines, and embeds functionality from a version of {{es}} Ingest Node that is compatible with the plugin version (`major.minor`).
