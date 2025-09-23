---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-kibana.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# {{kib}} configuration [k8s-kibana]

The following sections describe how to customize a {{kib}} deployment to suit your requirements.

* [Connect to an {{es}} cluster](k8s-kibana-es.md)

    * [Connect to an {{es}} cluster managed by ECK](k8s-kibana-es.md#k8s-kibana-eck-managed-es)
    * [Connect to an {{es}} cluster not managed by ECK](k8s-kibana-es.md#k8s-kibana-external-es)

* [Advanced configuration](k8s-kibana-advanced-configuration.md)

    * [Pod Configuration](k8s-kibana-advanced-configuration.md#k8s-kibana-pod-configuration)
    * [{{kib}} Configuration](k8s-kibana-advanced-configuration.md#k8s-kibana-configuration)
    * [Scaling out a {{kib}} deployment](k8s-kibana-advanced-configuration.md#k8s-kibana-scaling)

* [Secure settings](../../security/k8s-secure-settings.md#k8s-kibana-secure-settings)
* [HTTP Configuration](/deploy-manage/security/k8s-https-settings.md#k8s-kibana-http-configuration)

    * [Load balancer settings and TLS SANs](/deploy-manage/security/k8s-https-settings.md#k8s-kibana-http-publish)
    * [Provide your own certificate](/deploy-manage/security/k8s-https-settings.md#k8s-kibana-http-custom-tls)
    * [Disable TLS](/deploy-manage/security/k8s-https-settings.md#k8s-disable-tls)
    * [Install {{kib}} plugins](k8s-kibana-plugins.md)

* [Autoscaling stateless applications](../../autoscaling/autoscaling-in-eck.md#k8s-stateless-autoscaling): Use [Horizontal Pod Autoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/) for {{kib}} or other stateless applications.


