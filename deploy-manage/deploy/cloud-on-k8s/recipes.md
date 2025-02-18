---
applies:
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
Compared to other configuration examples that are consistently tested, like [fleet-managed Elastic Agent on ECK](configuration-examples-fleet.md), [standalone Elastic Agent on ECK](configuration-examples-standalone.md), or [Beats on ECK](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-beat-configuration-examples.html), the recipes in this section are not regularly tested by our automation system, and therefore should not be considered to be production-ready.
::::


