---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/monitoring-overview.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/how-monitoring-works.html
  - https://www.elastic.co/guide/en/cloud/current/ec-monitoring.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---

# Stack monitoring

% What needs to be done: Refine

% GitHub issue: https://github.com/elastic/docs-projects/issues/350

% Scope notes: Merge both docs into 1 as an overview. Ensure its valid for all deployment types. Consider bringing part of the info from the elastic cloud monitoring introduction.

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/monitoring-overview.md
% - [ ] ./raw-migrated-files/elasticsearch/elasticsearch-reference/how-monitoring-works.md
% - [ ] ./raw-migrated-files/cloud/cloud/ec-monitoring.md


https://www.elastic.co/guide/en/cloud/current/ec-monitoring-setup.html


% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$ec-es-cluster-health$$$

$$$ec-es-cluster-performance$$$

$$$ec-es-health-dedicated$$$

$$$ec-es-health-preconfigured$$$

$$$ec-es-health-warnings$$$

$$$ec-health-best-practices$$$

**This page is a work in progress.** The documentation team is working to combine content pulled from the following pages:

* [/raw-migrated-files/elasticsearch/elasticsearch-reference/monitoring-overview.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/monitoring-overview.md)
* [/raw-migrated-files/elasticsearch/elasticsearch-reference/how-monitoring-works.md](/raw-migrated-files/elasticsearch/elasticsearch-reference/how-monitoring-works.md)
* [/raw-migrated-files/cloud/cloud/ec-monitoring.md](/raw-migrated-files/cloud/cloud/ec-monitoring.md)

* [Configuring monitoring in {{kib}}](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-legacy.md)
* [Configuring monitoring for Logstash nodes](logstash://reference/monitoring-logstash-legacy.md)


1. Configure your production cluster to collect data and send it to the monitoring cluster:

    * [{{agent}} collection methods](../../../deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-elastic-agent.md)
    * [{{metricbeat}} collection methods](../../../deploy-manage/monitor/stack-monitoring/collecting-monitoring-data-with-metricbeat.md)
    * [Legacy collection methods](../../../deploy-manage/monitor/stack-monitoring/es-legacy-collection-methods.md)

3. (Optional) [Configure {{ls}} to collect data and send it to the monitoring cluster](logstash://reference/monitoring-logstash-legacy.md).
4. (Optional) Configure the {{beats}} to collect data and send it to the monitoring cluster. Skip this step for {{beats}} that are managed by {{agent}}.

    * [Auditbeat](asciidocalypse://docs/beats/docs/reference/auditbeat/monitoring.md)
    * [Filebeat](asciidocalypse://docs/beats/docs/reference/filebeat/monitoring.md)
    * [Heartbeat](asciidocalypse://docs/beats/docs/reference/heartbeat/monitoring.md)
    * [Metricbeat](asciidocalypse://docs/beats/docs/reference/metricbeat/monitoring.md)
    * [Packetbeat](asciidocalypse://docs/beats/docs/reference/packetbeat/monitoring.md)
    * [Winlogbeat](asciidocalypse://docs/beats/docs/reference/winlogbeat/monitoring.md)

5. (Optional) [Configure APM Server monitoring](/solutions/observability/apps/monitor-apm-server.md)
6. (Optional) Configure {{kib}} to collect data and send it to the monitoring cluster:

    * [{{agent}} collection methods](../../../deploy-manage/monitor/stack-monitoring/kibana-monitoring-elastic-agent.md)
    * [{{metricbeat}} collection methods](../../../deploy-manage/monitor/stack-monitoring/kibana-monitoring-metricbeat.md)
    * [Legacy collection methods](../../../deploy-manage/monitor/stack-monitoring/kibana-monitoring-legacy.md)