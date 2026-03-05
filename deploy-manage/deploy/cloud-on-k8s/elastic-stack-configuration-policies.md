---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-stack-config-policy.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# {{stack}} configuration policies [k8s-stack-config-policy]

{{stack}} configuration policies in {{eck}} (ECK) provide a centralized, declarative way to manage configuration across multiple {{es}} clusters and {{kib}} instances. By defining reusable `StackConfigPolicy` resources in Kubernetes, platform administrators can enforce consistent settings, such as cluster configuration, security settings, snapshot policies, ingest pipelines, or index templates, without configuring each cluster individually.

Once applied, the ECK operator continuously reconciles these policies with the targeted {{es}} and {{kib}} resources to ensure that managed settings remain enforced, enabling configuration-as-code practices and simplifying governance, standardization, and large-scale operations across multiple clusters.

This helps keep deployment manifests simpler by moving reusable configuration into `StackConfigPolicy` resources.

::::{warning}
We have identified an issue with {{es}} 8.15.1 and 8.15.2 that prevents security role mappings configured via Stack configuration policies to work correctly. Avoid these versions and upgrade to 8.16+ to remedy this issue if you are affected.
::::

::::{note}
{{stack}} configuration policies on ECK require a valid Enterprise license or Enterprise trial license. Check [the license documentation](../../license/manage-your-license-in-eck.md) for more details about managing licenses.
::::

::::{note}
Component templates created in configuration policies cannot currently be referenced from index templates created through the {{es}} API or {{kib}} UI.
::::

## How {{stack}} configuration policies work

A policy can be applied to one or more {{es}} clusters or {{kib}} instances in any namespace managed by the ECK operator. Configuration policy settings applied by the ECK operator are immutable through the {{es}} REST API.

With ECK `3.3.0` and later, multiple {{stack}} configuration policies can target the same {{es}} cluster and {{kib}} instance. When multiple policies target the same resource and define the same setting, the value from the policy with the highest `weight` takes precedence. If multiple policies have the same `weight` value, the operator reports a conflict. Refer to [Policy priority and weight](#k8s-stack-config-policy-priority-weight) for more information.

::::{admonition} Scale considerations
While there is no hard limit on how many `StackConfigPolicy` resources can target the same {{es}} cluster or {{kib}} instance, targeting a single resource with more than 100 policies can increase total reconciliation time to several minutes. For optimal performance, combine related settings into fewer policies rather than creating many granular ones.

Additionally, the total size of settings configured through `StackConfigPolicy` resources for a given {{es}} cluster or {{kib}} instance is limited to 1MB due to Kubernetes secret size constraints.
::::

## Define {{stack}} configuration policies [k8s-stack-config-policy-definition]

You can define {{stack}} configuration policies in a `StackConfigPolicy` resource. The following example shows a minimal policy that configures one {{es}} cluster setting.

```yaml
apiVersion: stackconfigpolicy.k8s.elastic.co/v1alpha1
kind: StackConfigPolicy
metadata:
  name: production-settings-all-clusters
  namespace: elastic-system <1>
spec:
  resourceSelector:
    matchLabels:
      env: production <1>
  elasticsearch:
    clusterSettings:
      indices.recovery.max_bytes_per_sec: "100mb"
```
1. Because this policy is created in the operator namespace (`elastic-system`), it applies to all {{es}} clusters managed by the operator that are labeled `env=production`, across all namespaces.

For more advanced, feature-specific configurations, refer to [Examples](#examples).

### Mandatory fields

Each `StackConfigPolicy` must define the following fields under `spec`:

* `name`: A unique name used to identify the policy.

* At least one of `elasticsearch` or `kibana`, each defining at least one attribute.

  ::::{note}
  `spec.elasticsearch` and `spec.kibana` contain the configuration applied to the targeted resources. Each section can include one or more supported configuration fields.

  For the list of supported settings and their corresponding policy fields, refer to:
  - [Elasticsearch features supported by {{stack}} configuration policies](#es-settings)
  - [Kibana features supported by {{stack}} configuration policies](#kib-settings)
  ::::

### Optional fields

The following fields are optional. They control which {{es}} clusters and {{kib}} instances the policy targets.

* {applies_to}`eck: ga 3.3+` `weight`: An integer that determines the priority of this policy when multiple policies target the same resource. Refer to [Policy priority and weight](#k8s-stack-config-policy-priority-weight) for details.

* `namespace`: The namespace of the `StackConfigPolicy` resource, used to identify the {{es}} clusters and {{kib}} instances to which the policy applies. If it equals the operator namespace, the policy applies to all namespaces managed by the operator. Otherwise, the policy applies only to the namespace where the policy is defined.

* `resourceSelector`: A [label selector](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) to identify the {{es}} clusters and {{kib}} instances to which the policy applies in combination with the namespace(s). If `resourceSelector` is not defined, the policy applies to all {{es}} clusters and {{kib}} instances in the namespace(s).


## {{es}} settings [es-settings]

This section describes the different {{es}} settings that can be configured through {{stack}} configuration policies. The syntax of each setting depends on the associated feature and the underlying {{es}} API, when applicable.

The following fields are available under `StackConfigPolicy.spec.elasticsearch`:

| Policy field | Description | Syntax and schema |
|---|---|---|
| `config` | Settings that go into `elasticsearch.yml`. | [Settings map](#syntax-types)<br><br>[{{es}} settings reference](elasticsearch://reference/elasticsearch/configuration-reference/index.md) |
| `clusterSettings` | Dynamic [cluster settings](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#dynamic-cluster-setting) applied through the cluster settings API. | [Settings map](#syntax-types)<br><br>[Cluster settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-settings) |
| `secureSettings` | Secure settings for the {{es}} keystore. | [List of secrets to add](#syntax-types)<br><br>[{{es}} secure settings](/deploy-manage/security/k8s-secure-settings.md) |
| `secretMounts` | Mount Kubernetes secrets into {{es}} pods.<br><br>[Specifics for secret mounts](#k8s-stack-config-policy-specifics-secret-mounts) | [List of secrets to mount](#syntax-types) |
| `snapshotRepositories` | Configure [snapshot repositories](/deploy-manage/tools/snapshot-and-restore/manage-snapshot-repositories.md) for backup and restore.<br><br>[Specifics for snapshot repositories](#k8s-stack-config-policy-specifics-snap-repo) | [Named resources map](#syntax-types)<br><br>[Create snapshot repository API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository) |
| `snapshotLifecyclePolicies` | Configure [snapshot lifecycle policies](/deploy-manage/tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) to automatically take snapshots and control how long they are retained. | [Named resources map](#syntax-types)<br><br>[SLM API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-put-lifecycle) |
| `ingestPipelines` | Configure [ingest pipelines](/manage-data/ingest/transform-enrich/ingest-pipelines.md) to perform common transformations on your data before indexing. | [Named resources map](#syntax-types)<br><br>[Ingest pipeline API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline) |
| `indexLifecyclePolicies` | Configure [{{ilm}} policies](/manage-data/lifecycle/index-lifecycle-management.md), to automatically manage the index lifecycle.  | [Named resources map](#syntax-types)<br><br>[ILM API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle) |
| `indexTemplates.composableIndexTemplates` | Configure [index templates](/manage-data/data-store/templates.md#index-templates) to define settings, mappings, and aliases that can be applied automatically to new indices.<br><br>[Specifics for index and component templates](#templates-specifics) | [Named resources map](#syntax-types)<br><br>[Index template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template) |
| `indexTemplates.componentTemplates` | Configure [component templates](/manage-data/data-store/templates.md#component-templates), reusable building-blocks to define settings, mappings, and aliases for new indices.<br><br>[Specifics for index and component templates](#templates-specifics) | [Named resources map](#syntax-types)<br><br>[Component template API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template) |
| `securityRoleMappings` | Configure [role mappings](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md) to associate roles to users based on rules. | [Named resources map](#syntax-types)<br><br>[Role mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role-mapping) |

### Specifics for secret mounts [k8s-stack-config-policy-specifics-secret-mounts]

The `secretMounts` field allows users to specify a user created secret and a `mountPath` to indicate where this secret should be mounted in the {{es}} Pods that are managed by the {{stack}} configuration policy. This can be used to add additional secrets to the {{es}} Pods that might be needed, for example for sensitive files required to configure [{{es}} authentication realms](/deploy-manage/users-roles/cluster-or-deployment-auth/authentication-realms.md).

The referenced secret should be created by the user in the same namespace as the {{stack}} configuration policy. The operator reads this secret and copies it over to the namespace of {{es}} so that it can be mounted by the {{es}} Pods.

The following is an example of configuring secret mounts in the {{stack}} configuration policy:

```yaml
spec:
  elasticsearch:
    secretMounts:
      - secretName: jwks-secret <1>
        mountPath: "/usr/share/elasticsearch/config/jwks" <2>
```

1. The name of the secret created by the user in the {{stack}} configuration policy namespace.
2. The mount path where the secret must be mounted to inside the {{es}} Pod.

### Specifics for snapshot repositories [k8s-stack-config-policy-specifics-snap-repo]

To avoid a conflict between multiple {{es}} clusters writing their snapshots to the same location, ECK automatically does the following:

* **Azure, GCS, and S3 repositories**: sets the `base_path` to `snapshots/<namespace>-<esName>` when it is not provided
* **FS repositories**: appends `<namespace>-<esName>` to `location`
* **HDFS repositories**: appends `<namespace>-<esName>` to `path`

### Specifics for index and component templates [templates-specifics]

`composableIndexTemplates` and `componentTemplats` must be defined under the `indexTemplates` field:

```yaml
spec:
  elasticsearch:
    indexTemplates:
      composableIndexTemplates:
        my-index-template:
          # ...
      componentTemplates:
        my-component-template:
          # ...
```

## {{kib}} settings [kib-settings]

The following settings can be configured for {{kib}} under `StackConfigPolicy.spec.elasticsearch`:

| Policy field | Description | Syntax and schema |
|---|---|---|
| `config` | Settings that go into `kibana.yml` | [Settings map](#syntax-types)<br><br>[{{kib}} settings reference](kibana://reference/configuration-reference/general-settings.md) |
| `secureSettings` | Secure settings for the {{kib}} keystore | [List of secrets](#syntax-types) to add to the keystore<br><br>[{{kib}} Secure Settings](/deploy-manage/security/k8s-secure-settings.md#k8s-kibana-secure-settings) |

## Examples

The following examples show common `StackConfigPolicy` patterns you can copy and adapt to your deployments.

::::{note}
Multiple `StackConfigPolicy` resources can target the same {{es}} cluster or {{kib}} instance, with `weight` determining which policy takes precedence when applying settings. Refer to [Policy priority and weight](#k8s-stack-config-policy-priority-weight) for more information.
::::

### Configure authentication policies using {{stack}} configuration policy [k8s-stack-config-policy-configuring-authentication-policies]

An {{stack}} configuration policy can be used to configure authentication for {{es}} clusters. Refer to [](../../users-roles/cluster-or-deployment-auth/manage-authentication-for-multiple-clusters.md) for some examples of the various authentication configurations that can be used.

### Configure a snapshot repository, an {{slm-init}} policy and cluster settings

Example of applying a policy that configures snapshot repository, {{slm-init}} Policies, and cluster settings:

```yaml
apiVersion: stackconfigpolicy.k8s.elastic.co/v1alpha1
kind: StackConfigPolicy
metadata:
  name: test-stack-config-policy
  # namespace: elastic-system or test-namespace
spec:
  weight: 0 <1>
  resourceSelector:
    matchLabels:
      env: my-label
  elasticsearch:
    clusterSettings:
      indices.recovery.max_bytes_per_sec: "100mb"
    secureSettings:
    - secretName: "my-secure-settings"
    snapshotRepositories:
      test-repo:
        type: gcs
        settings:
          bucket: my-bucket
    snapshotLifecyclePolicies:
      test-slm:
        schedule: "0 1 2 3 4 ?"
        name: "<production-snap-{now/d}>"
        repository: test-repo
        config:
          indices: ["*"]
          ignore_unavailable: true
          include_global_state: false
        retention:
          expire_after: "7d"
          min_count: 1
          max_count: 20
```
1. {applies_to}`eck: ga 3.3+` Optional: determines priority when multiple policies target the same resource

### Role mappings, ingest pipelines, {{ilm-init}}, and index templates

Another example of configuring role mappings, ingest pipelines, {{ilm-init}}, and index templates:

```yaml
apiVersion: stackconfigpolicy.k8s.elastic.co/v1alpha1
kind: StackConfigPolicy
metadata:
  name: test-stack-config-policy
spec:
  elasticsearch:
    securityRoleMappings:
      everyone-kibana:
        enabled: true
        metadata:
          _foo: something
          uuid: b9a59ba9-6b92-4be2-bb8d-02bb270cb3a7
        roles:
        - kibana_user
        rules:
          field:
            username: '*'
    ingestPipelines:
      test-pipeline:
        description: "optional description"
        processors:
        - set:
            field: my-keyword-field
            value: foo
      test-2-pipeline:
        description: "optional description"
        processors:
        - set:
            field: my-keyword-field
            value: foo
    indexLifecyclePolicies:
      test-ilm:
        phases:
          delete:
            actions:
              delete: {}
            min_age: 30d
          warm:
            actions:
              forcemerge:
                max_num_segments: 1
            min_age: 10d
    indexTemplates:
      componentTemplates:
        test-component-template:
          template:
            mappings:
              properties:
                '@timestamp':
                  type: date
        test-runtime-component-template-test:
          template:
            mappings:
              runtime:
                day_of_week:
                  type: keyword
      composableIndexTemplates:
        test-template:
          composed_of:
          - test-component-template
          - test-runtime-component-template-test
          index_patterns:
          - test*
          - bar*
          priority: 500
          template:
            aliases:
              mydata: {}
            mappings:
              _source:
                enabled: true
              properties:
                created_at:
                  format: EEE MMM dd HH:mm:ss Z yyyy
                  type: date
                host_name:
                  type: keyword
            settings:
              number_of_shards: 1
          version: 1
```

### Configure both {{es}} and {{kib}} through a policy

Example of configuring {{es}} and {{kib}} using an {{stack}} configuration policy. A mixture of `config`, `secureSettings`, and `secretMounts`:

```yaml
apiVersion: stackconfigpolicy.k8s.elastic.co/v1alpha1
kind: StackConfigPolicy
metadata:
  name: test-stack-config-policy
spec:
  resourceSelector:
    matchLabels:
      env: my-label
  elasticsearch:
    secureSettings:
    - secretName: shared-secret
    securityRoleMappings:
      jwt1-elastic-agent:
        roles: [ "remote_monitoring_collector" ]
        rules:
          all:
            - field: { realm.name: "jwt1" }
            - field: { username: "elastic-agent" }
        enabled: true
    config:
       logger.org.elasticsearch.discovery: DEBUG
       xpack.security.authc.realms.jwt.jwt1:
         order: -98
         token_type: id_token
         client_authentication.type: shared_secret
         allowed_issuer: "https://es.credentials.controller.k8s.elastic.co"
         allowed_audiences: [ "elasticsearch" ]
         allowed_subjects: ["elastic-agent"]
         allowed_signature_algorithms: [RS512]
         pkc_jwkset_path: jwks/jwkset.json
         claims.principal: sub
    secretMounts:
    - secretName: "testMountSecret"
      mountPath: "/usr/share/testmount"
    - secretName: jwks-secret
      mountPath: "/usr/share/elasticsearch/config/jwks"
  kibana:
    config:
      "xpack.canvas.enabled": true
    secureSettings:
    - secretName: kibana-shared-secret
```

## Monitor {{stack}} configuration policies [k8s-stack-config-policy-monitoring]

In addition to the logs generated by the operator, a config policy status is maintained in the `StackConfigPolicy` resource. This status gives information in which phase the policy is ("Applying", "Ready", "Error") and it indicates the number of resources for which the policy could be applied.

```sh
kubectl get stackconfigpolicy
```

```sh
NAME                           READY   PHASE   AGE
test-stack-config-policy       1/1     Ready   1m42s
test-err-stack-config-policy   0/1     Error   1m42s
```

When not all resources are ready, you can get more information about the reason by reading the full status:

```sh
kubectl get -n b scp test-err-stack-config-policy -o jsonpath="{.status}" | jq .
```

```json
{
  "errors": 1,
  "observedGeneration": 3,
  "phase": "Error",
  "readyCount": "1/2",
  "resources": 2,
  "details": {
    "elasticsearch": {
      "b/banana-staging": {
        "currentVersion": 1670342369361604600,
        "error": {
          "message": "Error processing slm state change: java.lang.IllegalArgumentException: Error on validating SLM requests\n\tSuppressed: java.lang.IllegalArgumentException: no such repository [es-snapshots]",
          "version": 1670342482739637500
        },
        "expectedVersion": 1670342482739637500,
        "phase": "Error"
      }
    },
    "kibana": {
      "b/banana-kb-staging": {
        "error": {},
        "phase": "Ready"
      }
    }
  }
}
```

Important events are also reported through {{k8s}} events, such as when you don't have the appropriate license:

```sh
17s    Warning   ReconciliationError stackconfigpolicy/config-test   StackConfigPolicy is an enterprise feature. Enterprise features are disabled
```

## Policy priority and weight [k8s-stack-config-policy-priority-weight]
```{applies_to}
deployment:
  eck: ga 3.3+
```

The `weight` field is an integer that determines the priority of a policy when multiple `StackConfigPolicy` resources target the same {{es}} cluster or {{kib}} instance. When multiple policies target the same resource, policies are evaluated in order of their `weight` values (from lowest to highest). Settings from policies with higher `weight` values take precedence and overwrite settings from policies with lower `weight` values. The policy with the highest `weight` value has the highest priority.

The `weight` field is optional and defaults to `0` if not specified. Higher weight values have higher priority.

::::{important} - Conflict resolution

If multiple policies have the same `weight` value and target the same resource, the operator reports a conflict. When a conflict occurs, **no policies are applied to that resource**—this includes not only the conflicting policies but also any other policies that target the same resource. The target resource remains unconfigured by any `StackConfigPolicy` until the conflict is resolved by adjusting the `weight` values of the conflicting policies.
::::

This allows you to create a hierarchy of policies, for example:
* Base policies with lower weights (for example, `weight: 0`) that provide default configurations
* Override policies with higher weights (for example, `weight: 100`) that provide environment-specific or cluster-specific configurations and overwrite the base policy settings

Example of using `weight` to create a policy hierarchy:

```yaml
# Base policy with default settings (lower priority)
apiVersion: stackconfigpolicy.k8s.elastic.co/v1alpha1
kind: StackConfigPolicy
metadata:
  name: base-policy
spec:
  weight: 0  # Lower weight = lower priority
  resourceSelector:
    matchLabels:
      env: production
  elasticsearch:
    clusterSettings:
      indices.recovery.max_bytes_per_sec: "50mb"

---
# Override policy with production-specific settings (higher priority)
apiVersion: stackconfigpolicy.k8s.elastic.co/v1alpha1
kind: StackConfigPolicy
metadata:
  name: production-override-policy
spec:
  weight: 100  # Higher weight = higher priority
  resourceSelector:
    matchLabels:
      env: production
      tier: critical
  elasticsearch:
    clusterSettings:
      indices.recovery.max_bytes_per_sec: "200mb"
```

In this example, clusters labeled with both `env: production` and `tier: critical` have the `production-override-policy` (weight: 100) settings applied, which overwrite the `base-policy` (weight: 0) settings. Other production clusters use only the `base-policy` (weight: 0) settings.

## Syntax types used in configuration policy fields [syntax-types]

Configuration policy fields use one of the following syntax types, depending on the kind of setting being configured.

| Syntax type | Description |
|---|---|
| **Settings map** | A map where keys correspond directly to {{es}} or {{kib}} configuration setting names. The structure matches the settings accepted by the corresponding API or configuration file, expressed in YAML instead of JSON.<br><br>Used in `config` and `clusterSettings` fields. |
| **Named resources map** | A map where each key is a user-defined logical name and the value contains the resource definition. The resource definition structure matches the payload accepted by the corresponding {{es}} API, expressed in YAML instead of JSON.<br><br>Used in fields such as `snapshotRepositories`, `snapshotLifecyclePolicies`, `ingestPipelines`, `indexLifecyclePolicies`, `indexTemplates`, and `securityRoleMappings`. |
| **List of resources** | A list of objects where each item defines a resource entry. Each object follows the schema expected by the corresponding configuration mechanism.<br><br>Used in `secureSettings` and `secretMounts` fields.

### Syntax examples

**Settings map**

```yaml
spec:
  elasticsearch:
    clusterSettings:
      indices.recovery.max_bytes_per_sec: 50mb <1>
```
1. The key corresponds to the name of a valid Elasticsearch cluster setting.

**Named resources map**

```yaml
spec:
  elasticsearch:
    snapshotRepositories:
      my-repo: <1>
        type: fs
        settings:
          location: /snapshots
```
1. The key is a user-defined logical name. The value must match the payload accepted by the corresponding {{es}} API.

```yaml
spec:
  elasticsearch:
    indexTemplates:
      componentTemplates:
        test-component-template: <1>
          template:
            mappings:
              properties:
                '@timestamp':
                  type: date
        test-runtime-component-template-test:
          template:
            mappings:
              runtime:
                day_of_week:
                  type: keyword
      composableIndexTemplates:
        test-template:
          composed_of:
          - test-component-template
          - test-runtime-component-template-test
          index_patterns:
          - test*
          - bar*
          priority: 500
          template:
            aliases:
              mydata: {}
            mappings:
              _source:
                enabled: true
              properties:
                created_at:
                  format: EEE MMM dd HH:mm:ss Z yyyy
                  type: date
                host_name:
                  type: keyword
            settings:
              number_of_shards: 1
          version: 1
```
1. Each top-level key represents a user-defined resource name.

**List of resources**

```yaml
spec:
  elasticsearch:
    secretMounts: <1>
      - name: my-secret
        mountPath: /etc/secrets
      - name: my-certificate
        mountPath: /usr/share/elasticsearch/config/my-certificate
```
1. Each list item defines a secret mount entry and references an existing Kubernetes Secret.
