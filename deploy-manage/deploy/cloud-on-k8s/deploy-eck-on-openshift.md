---
applies_to:
  deployment:
    eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-openshift.html
---

# Deploy ECK on Openshift [k8s-openshift]

This section shows how to run ECK on OpenShift.

* [Before you begin](#k8s-openshift-before-you-begin)
* [Deploy the operator](k8s-openshift-deploy-operator.md)
* [Deploy an {{es}} instance with a route](k8s-openshift-deploy-elasticsearch.md)
* [Deploy a {{kib}} instance with a route](k8s-openshift-deploy-kibana.md)
* [Deploy Docker images with `anyuid` SCC](k8s-openshift-anyuid-workaround.md)
* [Grant privileged permissions to Beats](k8s-openshift-beats.md)
* [Grant host access permission to Elastic Agent](k8s-openshift-agent.md)

## Before you begin [k8s-openshift-before-you-begin] 

1. To run the instructions on this page, you must be a `system:admin` user or a user with the privileges to create Projects, CRDs, and RBAC resources at the cluster level.
2. Set virtual memory settings on the Kubernetes nodes.

    Before deploying an {{es}} cluster with ECK, make sure that the Kubernetes nodes in your cluster have the correct `vm.max_map_count` sysctl setting applied. By default, Pods created by ECK are likely to run with the `restricted` [Security Context Constraint](https://docs.openshift.com/container-platform/4.12/authentication/managing-security-context-constraints.html) (SCC) which restricts privileged access required to change this setting in the underlying Kubernetes nodes.

    Alternatively, you can opt for setting `node.store.allow_mmap: false` at the [{{es}} node configuration](node-configuration.md) level. This has performance implications and is not recommended for production workloads.

    For more information, check [Virtual memory](virtual-memory.md).








