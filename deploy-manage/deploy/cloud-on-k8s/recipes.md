---
applies_to:
  deployment:
    eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-recipes.html
---

# Recipes [k8s-recipes]

This section includes recipes that provide configuration examples for some common use cases.

* [Expose Elasticsearch and Kibana using a Google Cloud Load Balancer (GCLB)](https://github.com/elastic/cloud-on-k8s/tree/main/config/recipes/gclb)
* [Expose Elasticsearch and Kibana using Istio ingress gateway](https://github.com/elastic/cloud-on-k8s/tree/main/config/recipes/istio-gateway)
* [Using Logstash with ECK](https://github.com/elastic/cloud-on-k8s/tree/main/config/recipes/logstash)
* [Expose Elastic Maps Server and Kibana using a Kubernetes Ingress](https://github.com/elastic/cloud-on-k8s/tree/main/config/recipes/maps)
* [Secure your cluster with Pod Security Policies](https://github.com/elastic/cloud-on-k8s/tree/main/config/recipes/psp)
* [Use Traefik to expose Elastic Stack applications](https://github.com/elastic/cloud-on-k8s/tree/main/config/recipes/traefik)
* [Deploy Elasticsearch, Kibana, Elastic Fleet Server and Elastic Agent within GKE Autopilot](https://github.com/elastic/cloud-on-k8s/tree/main/config/recipes/autopilot)

::::{warning}
Compared to other configuration examples that are consistently tested, like [fleet-managed Elastic Agent on ECK](configuration-examples-fleet.md), [standalone Elastic Agent on ECK](configuration-examples-standalone.md), or [Beats on ECK](/deploy-manage/deploy/cloud-on-k8s/configuration-examples-beats.md), the recipes in this section are not regularly tested by our automation system, and therefore should not be considered to be production-ready.
::::

:::{admonition} Support scope for Ingress Controllers
[Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) is a standard Kubernetes concept. While ECK-managed workloads can be publicly exposed using ingress resources, and we provide [example configurations](/deploy-manage/deploy/cloud-on-k8s/recipes.md), setting up an Ingress controller requires in-house Kubernetes expertise. 

If ingress configuration is challenging or unsupported in your environment, consider using standard `LoadBalancer` services as a simpler alternative.
:::



