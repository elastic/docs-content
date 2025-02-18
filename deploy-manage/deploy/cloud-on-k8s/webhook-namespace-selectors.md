---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-webhook-namespace-selectors.html
---

# Webhook namespace selectors [k8s-webhook-namespace-selectors]

If you install ECK through the Helm chart, you can now set `namespaceSelector` and `objectSelector` on the webhook. The webhook name is generated as `<operator-name>.<operator-namespace>.k8s.elastic.co` so that multiple operators can be installed side-by-side in the same cluster.

This can be useful in large and busy clusters, where you might want to divide the set of namespaces across several operators to speed up reconciliation times and reduce the amount of resources required per operator.

Webhook resources are cluster-scoped, therefore `createClusterScopedResources` must be set to true when installing the chart. This means that each operator gets a ClusterRole that applies to the whole cluster and not just the set of namespaces it is configured to manage. This approach is suitable only if you want to do load-splitting in a trusted cluster.

::::{warning} 
It is not recommended to deploy webhook resources in environments where operators are run by untrusted users and need to be locked down tightly.
::::

For more information, check [Configure the validating webhook](configure-validating-webhook.md) and [Dynamic Admission Control](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/).

