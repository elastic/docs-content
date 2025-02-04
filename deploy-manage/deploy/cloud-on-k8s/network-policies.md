---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-network-policies.html
---

# Network policies [k8s-network-policies]

[Network policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) allow you to isolate pods by restricting incoming and outgoing network connections to a trusted set of sources and destinations. This section describes how to use network policies to isolate the ECK operator and the {{stack}} applications to a set of namespaces to implement a form of soft multi-tenancy. Soft multi-tenancy is a term used to describe a scenario where a group of trusted users (different teams within an organization, for example) share a single resource such as a Kubernetes cluster. Note that network policies alone are not sufficient for security. You should complement them with strict RBAC policies, resource quotas, node taints, and other available security mechanisms to ensure that tenants cannot access, modify, or disrupt resources belonging to each other.

::::{note} 
There are several efforts to support multi-tenancy on Kubernetes, including the [official working group for multi-tenancy](https://github.com/kubernetes-sigs/multi-tenancy) and community extensions such as [loft](https://loft.sh) and [kiosk](https://github.com/kiosk-sh/kiosk), that can make configuration and management easier. You might need to employ network policies such the ones described in this section to have fine-grained control over {{stack}} applications deployed by your tenants.
::::


The following sections assume that the operator is installed in the `elastic-system` namespace with the [`namespaces` configuration](configure-eck.md) set to `team-a,team-b`. Each namespace is expected to be labelled as follows:

```sh
kubectl label namespace elastic-system eck.k8s.elastic.co/operator-name=elastic-operator
kubectl label namespace team-a eck.k8s.elastic.co/tenant=team-a
kubectl label namespace team-b eck.k8s.elastic.co/tenant=team-b
```


