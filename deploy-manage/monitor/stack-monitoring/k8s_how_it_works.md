---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_how_it_works.html
applies:
  eck: all
---

# How it works [k8s_how_it_works]

In the background, Metricbeat and Filebeat are deployed as sidecar containers in the same Pod as Elasticsearch and Kibana.

Metricbeat is used to collect monitoring metrics and Filebeat to monitor the Elasticsearch log files and collect log events.

The two Beats are configured to ship data directly to the monitoring cluster(s) using HTTPS and dedicated Elastic users managed by ECK.

