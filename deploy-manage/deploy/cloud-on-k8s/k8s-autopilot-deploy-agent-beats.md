---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-autopilot-deploy-agent-beats.html
---

# Deploy a standalone Elastic Agent and/or Beats [k8s-autopilot-deploy-agent-beats]

When running Elastic Agent and Beats within GKE Autopilot there are storage constraints to be considered. No `HostPath` volumes are allowed, which the ECK operator defaults to when unset for both `Deployments` and `Daemonsets`. Instead use [Kubernetes ephemeral volumes](https://kubernetes.io/docs/concepts/storage/ephemeral-volumes).

Refer to [Recipes to deploy Elasticsearch, Kibana, Elastic Fleet Server and Elastic Agent and/or Beats within GKE Autopilot](https://github.com/elastic/cloud-on-k8s/tree/main/config/recipes/autopilot).

