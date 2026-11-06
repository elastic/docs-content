---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-restrict-cross-namespace-associations.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Restrict cross-namespace resource associations [k8s-restrict-cross-namespace-associations]

This section describes how to restrict associations that can be created between resources managed by ECK.

When using the `elasticsearchRef` field to establish a connection to {{es}} from {{kib}}, APM Server, or Beats resources, by default the association is allowed as long as both resources are deployed to namespaces managed by that particular ECK instance. The association will succeed even if the user creating the association does not have access to one of the namespaces or the {{es}} resource.

The enforcement of access control rules for cross-namespace associations is disabled by default. Once enabled, it only enforces access control for resources deployed across two different namespaces. Associations between resources deployed in the same namespace are not affected.

When RBAC checks are enabled, ECK checks whether the associated resource's `ServiceAccount` has `get` permission for the referenced Kubernetes resource. The selected enforcement mode determines whether ECK unbinds the association or only emits a Warning event when access is denied.

::::{important}
ECK automatically removes associations that lack the correct access rights, scoped to whichever reference types the selected enforcement mode checks. If you have existing associations, do not enable this feature without creating the required `Roles` and `RoleBindings` as described in the following sections.
::::


## Enforcement modes [k8s-restrict-cross-namespace-enforcement-modes]

To enforce RBAC checks for cross-namespace associations, start the operator with the `--enforce-rbac-on-refs` flag. It accepts these values:

| Value | Behavior                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|---|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `false` | {applies_to}`eck: ga 3.0+` The operator performs no RBAC checks. If you omit the flag, the operator uses this value by default.                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `true` | {applies_to}`eck: ga 3.6+` The operator performs RBAC checks on all cross-namespace references. If the `ServiceAccount` cannot access a referenced resource, the operator removes associations that use direct or transitive {{es}} references. For other reference types, it only emits an event of type `Warning`.<br><br>{applies_to}`eck: ga 3.0-3.5` The operator performs RBAC checks only on direct and transitive {{es}} references. If the `ServiceAccount` cannot access the referenced resource, the operator removes the association. It does not check other reference types. |
| `"legacy"` | {applies_to}`eck: ga 3.6` Deprecated alias for `true`. Will be removed in a future release.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `"all"` | {applies_to}`eck: ga 3.6+` The operator performs RBAC checks on all cross-namespace references. If the `ServiceAccount` cannot access the referenced resource, the operator removes the association.                                                                                                                                                                                                                                                                                                                                                                                       |

::::{note}
Specifying `--enforce-rbac-on-refs` without an explicit value is equivalent to setting it to `true`.

In a future release, `true` will become an alias for `"all"`. The operator will then remove any cross-namespace association for which the `ServiceAccount` cannot access the referenced resource, not only associations that use {{es}} references. Before this behavior changes, review events of type `Warning` for non-{{es}} references and update your RBAC rules as needed.
::::

## Set up RBAC for cross-namespace associations [k8s-restrict-cross-namespace-rbac-setup]

Follow these steps to set up RBAC for an {{es}} association.

1. Create a `ClusterRole` to allow HTTP `GET` requests to be run against {{es}} objects:

    ```yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: ClusterRole
    metadata:
      name: elasticsearch-association
    rules:
      - apiGroups:
          - elasticsearch.k8s.elastic.co
        resources:
          - elasticsearches
        verbs:
          - get
    ```

2. Create a `ServiceAccount` and a `RoleBinding` in the {{es}} namespace to allow any resource using the `ServiceAccount` to associate with the {{es}} cluster:

    ```sh
    > kubectl create serviceaccount associated-resource-sa
    ```

    ```yaml
    apiVersion: rbac.authorization.k8s.io/v1
    kind: RoleBinding
    metadata:
      name: allow-associated-resource-from-remote-namespace
      namespace: elasticsearch-ns
    roleRef:
      apiGroup: rbac.authorization.k8s.io
      kind: ClusterRole
      name: elasticsearch-association
    subjects:
      - kind: ServiceAccount
        name: associated-resource-sa
        namespace: associated-resource-ns
    ```

3. Set the `serviceAccountName` field in the associated resource to specify which `ServiceAccount` is used to create the association:

    ```yaml
    apiVersion: kibana.k8s.elastic.co/v1
    kind: Kibana
    metadata:
      name: associated-resource
      namespace: associated-resource-ns
    spec:
     ...
      elasticsearchRef:
        name: "elasticsearch-sample"
        namespace: "elasticsearch-ns"
      # Service account used by this resource to get access to an Elasticsearch cluster
      serviceAccountName: associated-resource-sa
    ```


In this example, `associated-resource` can be of any `Kind` that requires an association to be created, for example `Kibana` or `ApmServer`. You can find [a complete example in the ECK GitHub repository](https://github.com/elastic/cloud-on-k8s/blob/{{version.eck | M.M}}/config/recipes/associations-rbac/apm_es_kibana_rbac.yaml).

::::{note}
If the `serviceAccountName` is not set, ECK uses the default service account assigned to the pod by the [Service Account Admission Controller](https://kubernetes.io/docs/reference/access-authn-authz/service-accounts-admin/#service-account-admission-controller).
::::


The associated resource `associated-resource` is now allowed to create an association with any {{es}} cluster in the namespace `elasticsearch-ns`.

