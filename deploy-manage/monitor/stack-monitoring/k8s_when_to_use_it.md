---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s_when_to_use_it.html
applies:
  eck: all
---

# When to use it [k8s_when_to_use_it]

This feature is a good solution if you need to monitor your Elastic applications in restricted Kubernetes environments where you cannot grant advanced permissions:

* to Metricbeat to allow queriying the k8s API
* to Filebeat to deploy a privileged DaemonSet

However, for maximum efficiency and minimising resource consumption, or advanced use cases that require specific Beats configurations, you can deploy a standalone Metricbeat Deployment and a Filebeat Daemonset. Check the [Beats configuration Examples](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-beat-configuration-examples.html) for more information.

