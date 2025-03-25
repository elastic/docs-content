---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-clients-integrations.html
---

# Secure clients and integrations [security-clients-integrations]

:::{warning}
**This page is a work in progress.**
:::


You will need to update the configuration for several [clients](httprest-clients-security.md) to work with a secured {{es}} cluster.

The {{es}} {{security-features}} enable you to secure your {{es}} cluster. But {{es}} itself is only one product within the {{stack}}. It is often the case that other products in the {{stack}} are connected to the cluster and therefore need to be secured as well, or at least communicate with the cluster in a secured way:

* [Apache Hadoop](elasticsearch-hadoop://reference/security.md)
* [Auditbeat](beats://reference/auditbeat/securing-auditbeat.md)
* [Filebeat](beats://reference/filebeat/securing-filebeat.md)
* [{{fleet}} & {{agent}}](/reference/fleet/secure.md)
* [Heartbeat](beats://reference/heartbeat/securing-heartbeat.md)
* [{{kib}}](../security.md)
* [Logstash](logstash://reference/secure-connection.md)
* [Metricbeat](beats://reference/metricbeat/securing-metricbeat.md)
* [Monitoring and security](../monitor.md)
* [Packetbeat](beats://reference/packetbeat/securing-packetbeat.md)
* [Reporting](../../explore-analyze/report-and-share.md)
* [Winlogbeat](beats://reference/winlogbeat/securing-winlogbeat.md)




