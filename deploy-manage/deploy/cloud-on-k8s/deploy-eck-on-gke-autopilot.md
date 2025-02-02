---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autopilot.html
---

# Deploy ECK on GKE Autopilot [k8s-autopilot]

This page shows how to run ECK on GKE Autopilot.

1. It is recommended that each Kubernetes host’s virtual memory kernel settings be modified. Refer to [Virtual memory](virtual-memory.md).
2. It is recommended that Elasticsearch Pods have an `initContainer` that waits for virtual memory settings to be in place. Refer to [Deploy an Elasticsearch instance](k8s-autopilot-deploy-elasticsearch.md).
3. For Elastic Agent/Beats there are storage limitations to be considered. Refer to [Deploy a standalone Elastic Agent and/or Beats](k8s-autopilot-deploy-agent-beats.md)
4. Ensure you are using a node class that is applicable for your workload by adding a `cloud.google.com/compute-class` label in a `nodeSelector`. Refer to [GKE Autopilot documentation.](https://cloud.google.com/kubernetes-engine/docs/concepts/autopilot-compute-classes)

    * [Ensuring virtual memory kernel settings](k8s-autopilot-setting-virtual-memory.md)
    * [Installing the ECK Operator](k8s-autopilot-deploy-operator.md)
    * [Deploy an Elasticsearch instance](k8s-autopilot-deploy-elasticsearch.md)
    * [Deploy a standalone Elastic Agent and/or Beats](k8s-autopilot-deploy-agent-beats.md)






