---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-clients-integrations.html
---

# Secure clients and integrations [security-clients-integrations]

You will need to update the configuration for several [clients](httprest-clients-security.md) to work with a secured {{es}} cluster.

The {{es}} {security-features} enable you to secure your {{es}} cluster. But {{es}} itself is only one product within the {{stack}}. It is often the case that other products in the {{stack}} are connected to the cluster and therefore need to be secured as well, or at least communicate with the cluster in a secured way:

* [Apache Hadoop](https://www.elastic.co/guide/en/elasticsearch/reference/current/hadoop.html)
* [Auditbeat](https://www.elastic.co/guide/en/beats/auditbeat/current/securing-auditbeat.html)
* [Filebeat](https://www.elastic.co/guide/en/beats/filebeat/current/securing-filebeat.html)
* [{{fleet}} & {{agent}}](https://www.elastic.co/guide/en/fleet/current/secure.html)
* [Heartbeat](https://www.elastic.co/guide/en/beats/heartbeat/current/securing-heartbeat.html)
* [{{kib}}](../security.md)
* [Logstash](https://www.elastic.co/guide/en/logstash/current/ls-security.html)
* [Metricbeat](https://www.elastic.co/guide/en/beats/metricbeat/current/securing-metricbeat.html)
* [Monitoring and security](../monitor.md)
* [Packetbeat](https://www.elastic.co/guide/en/beats/packetbeat/current/securing-packetbeat.html)
* [Reporting](../../explore-analyze/report-and-share.md)
* [Winlogbeat](https://www.elastic.co/guide/en/beats/winlogbeat/current/securing-winlogbeat.html)




