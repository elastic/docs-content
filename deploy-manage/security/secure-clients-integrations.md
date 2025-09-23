---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-clients-integrations.html
applies_to:
  deployment:
    self: all
    eck: all
    ess: all
    ece: all
products:
  - id: elasticsearch
---

# Secure other {{stack}} components 

The {{es}} {{security-features}} enable you to secure your {{es}} cluster. However, {{es}} itself is only one product within the {{stack}}. Other products in the {{stack}} are connected to the cluster and therefore need to be secured as well, or at least communicate with the cluster in a secured way. Review the guides for other {{es}} products:

* [Apache Hadoop](elasticsearch-hadoop://reference/security.md)
* [Auditbeat](beats://reference/auditbeat/securing-auditbeat.md)
* [Filebeat](beats://reference/filebeat/securing-filebeat.md)
* [{{fleet}} & {{agent}}](/reference/fleet/secure.md)
* [Heartbeat](beats://reference/heartbeat/securing-heartbeat.md)
* [Logstash](logstash://reference/secure-connection.md)
* [Metricbeat](beats://reference/metricbeat/securing-metricbeat.md)
* [Packetbeat](beats://reference/packetbeat/securing-packetbeat.md)
* [Reporting](../../explore-analyze/report-and-share.md)
* [Winlogbeat](beats://reference/winlogbeat/securing-winlogbeat.md)