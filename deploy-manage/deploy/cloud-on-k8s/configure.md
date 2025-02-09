---
navigation_title: Configure ECK
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-operating-eck.html
---

# Configure ECK [k8s-operating-eck]

By default, the ECK installation includes a **ConfigMap** where you can **add, remove, or update configuration settings**. This ConfigMap is automatically mounted into the operator’s container and provided to it through the `--config` parameter.

To configure ECK **edit the `elastic-operator` ConfigMap** to change the operator configuration. The operator will restart automatically to apply the new changes unless the `--disable-config-watch` flag is set.

Alternatively, you can edit the `elastic-operator` StatefulSet and add flags to the `args` section — which will trigger an automatic restart of the operator pod by the StatefulSet controller.

For a complete description of available **configuration flags and methods**, refer to the [](./configure-eck.md).

## Configuration use cases

The following guides provide detailed instructions on configuring specific features, managing licenses, and performing common operational tasks:

* [*Configure the validating webhook*](configure-validating-webhook.md)
* [*Configure the metrics endpoint*](../../monitor/orchestrators/eck-metrics-configuration.md)
* [*Restrict cross-namespace resource associations*](restrict-cross-namespace-resource-associations.md)
* [*Manage licenses in ECK*](../../license/manage-your-license-in-eck.md)
* [*Install ECK*](install.md)
* [*Upgrade ECK*](../../upgrade/orchestrator/upgrade-cloud-on-k8s.md)
* [*Uninstall ECK*](../../uninstall/uninstall-elastic-cloud-on-kubernetes.md)
* [*Running in air-gapped environments*](air-gapped-install.md)

% suggestion: maybe we should add a comment about most common configuration needs, like CA certificates, namespaces, log-verbosity...