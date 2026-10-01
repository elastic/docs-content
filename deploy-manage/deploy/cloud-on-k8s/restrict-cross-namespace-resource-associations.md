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

ECK allows an association only if the `ServiceAccount` of the associated resource can send HTTP `GET` requests to the referenced resource object.

::::{important}
ECK automatically removes any associations that do not have the correct access rights. If you have existing associations, do not enable this feature without creating the required `Roles` and `RoleBindings` as described in the following sections.
::::


## Enforcement modes [k8s-restrict-cross-namespace-enforcement-modes]

To enable the restriction of cross-namespace associations, start the operator with the `--enforce-rbac-on-refs` flag. It accepts these values:

| Value | Behavior |
|---|---|
| `false` | {applies_to}`eck: ga 3.0` Disabled (default). The operator performs no RBAC checks. |
| `true` | {applies_to}`eck: ga 3.6` The operator checks RBAC for all cross-namespace references. It unbinds direct or transitive {{es}} references when the service account is denied access. For all other cross-namespace references, it emits a Warning event only.<br><br>{applies_to}`eck: ga 3.0-3.5` The operator checks and unbinds direct or transitive {{es}} references when the service account is denied access. Non-Elasticsearch references are not checked. |
| `"legacy"` | {applies_to}`eck: ga 3.6` Deprecated alias for `true`. Will be removed in a future release. |
| `"all"` | {applies_to}`eck: ga 3.6` The operator checks RBAC for all cross-namespace references and unbinds any where the service account is denied access. |

::::{note}
* The bare flag without a value (`--enforce-rbac-on-refs`) is equivalent to `--enforce-rbac-on-refs=true`.

* In a future release, `true` will become an alias for `"all"`, and the operator will unbind all cross-namespace references where the service account is denied access, not just Elasticsearch ones. Review the Warning events emitted for non-Elasticsearch references and update your RBAC rules so your setup is ready before that change lands.
::::

## Set up RBAC for cross-namespace associations [k8s-restrict-cross-namespace-rbac-setup]

These steps set up RBAC for an {{es}} association.

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

