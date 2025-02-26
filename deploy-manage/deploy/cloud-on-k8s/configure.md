---
navigation_title: Configure
applies_to:
  deployment:
    eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-operating-eck.html
---

# Configure ECK [k8s-operating-eck]

This section covers ECK configuration mechanisms and use cases, starting with the basic setup of the operator using the provided `ConfigMap` and extending to more advanced configuration scenarios that require detailed procedures.

::::{tip}
This content focuses on ECK operator configuration. For details on available features and how to configure your {{es}} and {{kib}} deployments, refer to [](./configure-deployments.md).
::::

The following guides cover common ECK configuration tasks:

* [](./configure-eck.md): Apply configuration changes, such the CA certificate validity period, the namespaces where the operator is allowed to work, or the log verbosity level for ECK.

* [Configure the validating webhook](configure-validating-webhook.md): Enable or disable the webhook, and configure multiple SSL certificate generation options.

* [Restrict cross-namespace resource associations](restrict-cross-namespace-resource-associations.md): Configure access control rules for cross-namespace associations. This functionality is disabled by default.

* [Create custom images](./create-custom-images.md): Use your own images with {{es}} plugins already installed rather than installing them through init containers.

* [Service meshes](./service-meshes.md): Connect ECK and managed Elastic Stack applications to some of the most popular [service mesh](https://www.cncf.io/blog/2017/04/26/service-mesh-critical-component-cloud-native-stack/) implementations in the Kubernetes ecosystem.

* [Network policies](./network-policies.md): Use [Kubernetes network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) to isolate pods by restricting incoming and outgoing network connections to a trusted set of sources and destinations.

* [](./webhook-namespace-selectors.md): Restrict the namespaces that the validation webhook applies to, allowing multiple operators to coexist efficiently in the same cluster.

Other sections of the Elastic documentation cover additional topics related to ECK configuration:

* **Monitoring**
  * [Configure the metrics endpoint](/deploy-manage/monitor/orchestrators/eck-metrics-configuration.md)  (monitor an orchestrator)

* **Licensing**
  * [Manage licenses in ECK](../../license/manage-your-license-in-eck.md)

* **Maintenance**
  * [Upgrade ECK](../../upgrade/orchestrator/upgrade-cloud-on-k8s.md)
  * [Uninstall ECK](../../uninstall/uninstall-elastic-cloud-on-kubernetes.md)