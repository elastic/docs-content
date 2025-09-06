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

::::{warning}
We have identified an issue with {{es}} 8.15.1 and 8.15.2 that prevents security role mappings configured via Stack configuration policies to work correctly. Avoid these versions and upgrade to 8.16+ to remedy this issue if you are affected.
::::


::::{note}
This requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../../license/manage-your-license-in-eck.md) for more details about managing licenses.
::::

::::{note}
Component templates created in configuration policies cannot currently be referenced from index templates created through the {{es}} API or {{kib}} UI.
::::

Starting from ECK `2.6.1` and {{es}} `8.6.1`, {{stack}} configuration policies allow you to configure the following settings for {{es}}:

* [Cluster Settings](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#dynamic-cluster-setting)
* [Snapshot Repositories](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-snapshot-create-repository)
* [Snapshot Lifecycle Policies](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-slm-put-lifecycle)
* [Ingest pipelines](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ingest-put-pipeline)
* [Index Lifecycle Policies](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ilm-put-lifecycle)
* [Index templates](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-put-index-template)
* [Components templates](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-put-component-template)
* [Role mappings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role-mapping)
* [{{es}} Configuration](/deploy-manage/deploy/self-managed/configure-elasticsearch.md) (configuration settings for {{es}} that will go into [`elasticsearch.yml`](/deploy-manage/stack-settings.md)) [ECK 2.11.0]
* [{{es}} Secure Settings](../../security/secure-settings.md) [ECK 2.11.0]
* [Secret Mounts](#k8s-stack-config-policy-specifics-secret-mounts) [ECK 2.11.0]

Additionally with ECK `2.11.0` it is possible to configure {{kib}} as well using {{stack}} configuration policies, the following settings can be configured for {{kib}}:

* [{{kib}} Configuration](kibana://reference/configuration-reference/general-settings.md) (configuration settings for {{kib}} that will go into `kibana.yml`)
* [{{kib}} Secure Settings](../../security/k8s-secure-settings.md)

A policy can be applied to one or more {{es}} clusters or {{kib}} instances in any namespace managed by the ECK operator. Configuration policy settings applied by the ECK operator are immutable through the {{es}} REST API. It is currently not allowed to configure an {{es}} cluster or {{kib}} instance with more than one policy.


## Define {{stack}} configuration policies [k8s-stack-config-policy-definition]

{{stack}} configuration policies can be defined in a `StackConfigPolicy` resource. Each `StackConfigPolicy` must have the following field:

* `name` is a unique name used to identify the policy.

At least one of `spec.elasticsearch` or `spec.kibana` needs to be defined with at least one of its attributes.

* `spec.elasticsearch` describes the settings to configure for {{es}}. Each of the following fields except `clusterSettings` is an associative array where keys are arbitrary names and values are definitions:

    * `clusterSettings` are dynamic settings that can be set on a running cluster like with the Cluster Update Settings API.
    * `snapshotRepositories` are snapshot repositories for defining an off-cluster storage location for your snapshots. Check [Specifics for snapshot repositories](#k8s-stack-config-policy-specifics-snap-repo) for more information.
    * `snapshotLifecyclePolicies` are snapshot lifecycle policies, to automatically take snapshots and control how long they are retained.
    * `securityRoleMappings` are role mappings, to define which roles are assigned to each user by identifying them through rules.
    * `ingestPipelines` are ingest pipelines, to perform common transformations on your data before indexing.
    * `indexLifecyclePolicies` are index lifecycle policies, to automatically manage the index lifecycle.
    * `indexTemplates.componentTemplates` are component templates that are building blocks for constructing index templates that specify index mappings, settings, and aliases.
    * `indexTemplates.composableIndexTemplates` are index templates to define settings, mappings, and aliases that can be applied automatically to new indices.
    * `config` are the settings that go into the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file.
    * `secretMounts` are the additional user created secrets that need to be mounted to the {{es}} Pods.
    * `secureSettings` is a list of Secrets containing Secure Settings to inject into the keystore(s) of the {{es}} cluster(s) to which this policy applies, similar to the [{{es}} Secure Settings](../../security/secure-settings.md).

* `spec.kibana` describes the settings to configure for {{kib}}.

    * `config` are the settings that go into the [`kibana.yml`](/deploy-manage/stack-settings.md) file.
    * `secureSettings` is a list of Secrets containing Secure Settings to inject into the keystore(s) of the {{kib}} instance(s) to which this policy applies, similar to the [{{kib}} Secure Settings](../../security/k8s-secure-settings.md).


The following fields are optional:

* `namespace` is the namespace of the `StackConfigPolicy` resource and used to identify the {{es}} clusters to which this policy applies. If it equals to the operator namespace, the policy applies to all namespaces managed by the operator, otherwise the policy only applies to the namespace of the policy.
* `resourceSelector` is a [label selector](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) to identify the {{es}} clusters to which this policy applies in combination with the namespace(s). No `resourceSelector` means all {{es}} clusters in the namespace(s).

Example of applying a policy that configures snapshot repository, SLM Policies, and cluster settings:

```yaml
apiVersion: stackconfigpolicy.k8s.elastic.co/v1alpha1
kind: StackConfigPolicy
metadata:
  name: test-stack-config-policy
  # namespace: elastic-system or test-namespace
spec:
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

Another example of configuring role mappings, ingest pipelines, ILM and index templates:

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

Example of configuring {{es}} and {{kib}} using an {{stack}} configuration policy:

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

Important events are also reported through Kubernetes events, such as when two config policies conflict or you don’t have the appropriate license:

```sh
54s    Warning   Unexpected          stackconfigpolicy/config-test   conflict: resource Elasticsearch ns1/cluster-a already configured by StackConfigpolicy default/config-test-2
```

```sh
17s    Warning   ReconciliationError stackconfigpolicy/config-test   StackConfigPolicy is an enterprise feature. Enterprise features are disabled
```


## Specifics for snapshot repositories [k8s-stack-config-policy-specifics-snap-repo]

In order to avoid a conflict between multiple {{es}} clusters writing their snapshots to the same location, ECK automatically:

* sets the `base_path` to `snapshots/<namespace>-<esName>` when it is not provided, for Azure, GCS and S3 repositories
* appends `<namespace>-<esName>` to `location` for a FS repository
* appends `<namespace>-<esName>` to `path` for an HDFS repository


## Specifics for secret mounts [k8s-stack-config-policy-specifics-secret-mounts]

ECK `2.11.0` introduces `spec.elasticsearch.secretMounts` as a new field. This field allows users to specify a user created secret and a mountPath to indicate where this secret should be mounted in the {{es}} Pods that are managed by the {{stack}} configuration policy. This field can be used to add additional secrets to the {{es}} Pods that may be needed for example for sensitive files required to configure {{es}} security realms. The secret should be created by the user in the same namespace as the {{stack}} configuration policy. The operator reads this secret and copies it over to the namespace of {{es}} so that it can be mounted by the {{es}} Pods. Example of configuring secret mounts in the {{stack}} configuration policy:

```yaml
secretMounts:
  - secretName: jwks-secret <1>
    mountPath: "/usr/share/elasticsearch/config/jwks" <2>
```

1. name of the secret created by the user in the {{stack}} configuration policy namespace.
2. mount path where the secret must be mounted to inside the {{es}} Pod.



## Configuring authentication policies using {{stack}} configuration policy [k8s-stack-config-policy-configuring-authentication-policies]

{{stack}} configuration policy can be used to configure authentication for {{es}} clusters. Check [Managing authentication for multiple stacks using {{stack}} configuration policy](../../users-roles/cluster-or-deployment-auth/manage-authentication-for-multiple-clusters.md) for some examples of the various authentication configurations that can be used.
