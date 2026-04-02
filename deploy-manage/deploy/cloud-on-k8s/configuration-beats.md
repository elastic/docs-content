---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-beat-configuration.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
navigation_title: Configuration
---

# Configuration for Beats on {{eck}} [k8s-beat-configuration]

## Upgrade the Beat specification [k8s-beat-upgrade-specification]

You can upgrade the Beat version or change settings by editing the YAML specification. ECK applies the changes by performing a rolling restart of the Beat Pods. Depending on the specification settings that you used, ECK will set the [output](configuration-beats.md#k8s-beat-set-beat-output) part of the config, perform {{kib}} dashboard [setup](configuration-beats.md#k8s-beat-set-up-kibana-dashboards), restart Beats on certificates rollover and set up the Beats [keystore](configuration-beats.md#k8s-beat-secrets-keystore-for-secure-settings).


## Customize Beat configuration [k8s-beat-custom-configuration]

The Beat configuration is defined in the `config` element:

```yaml subs=true
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: quickstart
spec:
  type: heartbeat
  version: {{version.stack}}
  elasticsearchRef:
    name: quickstart
  config:
    heartbeat.monitors:
    - type: tcp
      schedule: '@every 5s'
      hosts: ["quickstart-es-http.default.svc:9200"]
  deployment:
    podTemplate:
      spec:
        dnsPolicy: ClusterFirstWithHostNet
        securityContext:
          runAsUser: 0
```

Alternatively, it can be provided through a Secret specified in the `configRef` element:

```yaml subs=true
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: heartbeat-quickstart
spec:
  type: heartbeat
  version: {{version.stack}}
  elasticsearchRef:
    name: quickstart
  configRef:
    secretName: heartbeat-config
  deployment:
    podTemplate:
      spec:
        dnsPolicy: ClusterFirstWithHostNet
        securityContext:
          runAsUser: 0
---
apiVersion: v1
kind: Secret
metadata:
  name: heartbeat-config
stringData:
  beat.yml: |-
    heartbeat.monitors:
    - type: tcp
      schedule: '@every 5s'
      hosts: ["quickstart-es-http.default.svc:9200"]
```

For more details, check the [Beats configuration](beats://reference/libbeat/config-file-format.md) section.


## Customize the connection to an {{es}} cluster [k8s-beat-connect-es]

The `elasticsearchRef` element allows ECK to automatically configure Beats to establish a secured connection to a managed {{es}} cluster. By default it targets all nodes in your cluster. If you want to direct traffic to specific nodes of your {{es}} cluster, refer to [*Traffic Splitting*](requests-routing-to-elasticsearch-nodes.md) for more information and examples.


## Deploy a Beat [k8s-beat-deploy-elastic-beat]

ECK supports the deployment of the following Beats:

* [Filebeat](https://www.elastic.co/beats/filebeat)
* [Metricbeat](https://www.elastic.co/beats/metricbeat)
* [Heartbeat](https://www.elastic.co/beats/heartbeat)
* [Auditbeat](https://www.elastic.co/beats/auditbeat)
* [Packetbeat](https://www.elastic.co/beats/packetbeat)
* [Journalbeat](https://www.elastic.co/guide/en/beats/journalbeat/current/index.html)

For each Beat you want to deploy, you can specify the `type` and `version` elements. ECK creates a new user in {{es}} with a minimal set of appropriate roles and permissions to enable the use of all Beats features.


## Deploy a Community Beat [k8s-beat-deploy-community-beat]

ECK supports the deployment of any Community Beat.

1. Specify the `type` and `version` elements.
2. Set the `image` element to point to the image to be deployed.
3. Make sure the following roles exist in {{es}}:

    * If `elasticsearchRef` is provided, create the role `eck_beat_es_$type_role`, where `$type` is the Beat type. For example, when deploying `kafkabeat`, the role name is `eck_beat_es_kafkabeat_role`. This role must have the permissions required by the Beat. Check the [{{es}} documentation](/deploy-manage/users-roles/cluster-or-deployment-auth/defining-roles.md) for more details.
    * If `kibanaRef` is provided, create the role `eck_beat_kibana_$type_role` with the permissions required to setup {{kib}} dashboards.


Alternatively, create a user in {{es}} and include the credentials in the Beats `config` for {{es}} output, {{kib}} setup or both. If `elasticsearchRef` and `kibanaRef` are also defined, ECK will use the provided user credentials when setting up the connections.


## Set up {{kib}} dashboards [k8s-beat-set-up-kibana-dashboards]

ECK can instruct Beats to set up example dashboards packaged with the Beat. To enable this, set the `kibanaRef` element in the specification to point to ECK-managed {{kib}} deployment:

```yaml
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: quickstart
spec:
  kibanaRef:
    name: quickstart
...
```

ECK will create a new user in {{es}} with a minimal set of appropriate roles and permissions that is needed for dashboard setup.


## Secrets keystore for secure settings [k8s-beat-secrets-keystore-for-secure-settings]

Beats offer a keystore for sensitive settings like passwords. This avoids storing them in plaintext in the configuration.

ECK exposes that mechanism with the `secureSettings` element in the specification. [Similar to Elasticsearch](../../security/secure-settings.md), you can use Kubernetes Secrets to provide the settings securely:

```yaml
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: quickstart
spec:
  secureSettings:
  - secretName: agent-name-secret
  config:
    name: ${AGENT_NAME_VAR}
...
---
apiVersion: v1
kind: Secret
metadata:
  name: agent-name-secret
stringData:
  AGENT_NAME_VAR: id_007
```

Check [Beats documentation](beats://reference/filebeat/keystore.md) for more details.


## Set Beat output [k8s-beat-set-beat-output]

If the `elasticsearchRef` element is specified, ECK populates the output section of the Beat config. ECK creates a user with appropriate roles and permissions and uses its credentials. If required, it also mounts the CA certificate in all Beat Pods, and recreates Pods when this certificate changes. Moreover, `elasticsearchRef` element can refer to an ECK-managed {{es}} cluster by filling the `name`, `namespace`, `serviceName` fields accordingly, as well as to a Kubernetes secret that contains the connection information to an {{es}} cluster not managed by it. In the latter case, for authenticating against the {{es}} cluster the secret must contain the fields of `url` and either the `username` with `password` or the `api-key`.

Output can be set to any value that is supported by a given Beat. To use it, remove the `elasticsearchRef` element from the specification and include an appropriate output configuration in the `config` or `configRef` elements.

```yaml
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: quickstart
spec:
  config:
    output.kafka:
      hosts: ["kafka1.default.svc:9092", "kafka2.default.svc:9092"]
      topic: '%{[fields.log_topic]}'
      partition.round_robin:
        reachable_only: false
      required_acks: 1
...
```


## Choose the deployment model [k8s-beat-chose-the-deployment-model]

Depending on the use case, Beats may need to be deployed as a [Deployment](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) or a [DaemonSet](https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/). Provide a `podTemplate` element under either the `deployment` or the `daemonSet` element in the specification to choose how a given Beat should be deployed. When choosing the `deployment` option you can additionally specify the [strategy](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#strategy) used to replace old Pods with new ones.

```yaml
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: quickstart
spec:
  deployment:
    strategy:
      type: Recreate
    podTemplate:
      spec:
        securityContext:
          runAsUser: 0
```

Consider picking the `Recreate` strategy if you are using a `hostPath` volume as the Beats data directory to avoid two Pods competing for the same directory.


## Role Based Access Control for Beats [k8s-beat-role-based-access-control-for-beats]

Some Beats features (such as [autodiscover](beats://reference/filebeat/configuration-autodiscover.md) or Kubernetes module [metricsets](beats://reference/metricbeat/metricbeat-metricset-kubernetes-apiserver.md)) require that Beat Pods interact with Kubernetes APIs. Specific permissions are needed to allow this functionality. Standard Kubernetes [RBAC](https://kubernetes.io/docs/reference/access-authn-authz/rbac/) rules apply. For example, to allow for autodiscover:

```yaml
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: quickstart
spec:
  config:
    filebeat:
      autodiscover:
        providers:
        - node: ${NODE_NAME}
          type: kubernetes
          hints:
            enabled: true
            default_config:
              type: container
              paths:
              - /var/log/containers/*${data.kubernetes.container.id}.log
  daemonSet:
    podTemplate:
      spec:
        serviceAccount: elastic-beat-filebeat-quickstart
        automountServiceAccountToken: true
        containers:
        - name: filebeat
          env:
          - name: NODE_NAME
            valueFrom:
              fieldRef:
                fieldPath: spec.nodeName
...
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: elastic-beat-filebeat-quickstart
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: elastic-beat-autodiscover-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: elastic-beat-autodiscover
subjects:
- kind: ServiceAccount
  name: elastic-beat-filebeat-quickstart
  namespace: default
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: elastic-beat-autodiscover
rules:
- apiGroups:
  - ""
  resources:
  - nodes
  - namespaces
  - events
  - pods
  verbs:
  - get
  - list
  - watch
- apiGroups: ["apps"]
  resources:
  - replicasets
  verbs:
  - get
  - list
  - watch
- apiGroups: ["batch"]
  resources:
  - jobs
  verbs:
  - get
  - list
  - watch
```


## Deploying Beats in secured clusters [k8s-beat-deploying-beats-in-secured-clusters]

To deploy Beats in clusters with the Pod Security Policy admission controller enabled, or [in OpenShift clusters](k8s-openshift-beats.md), you must grant additional permissions to the Service Account used by the Beat Pods. Those Service Accounts must be bound to a Role or ClusterRole that has `use` permission for the required Pod Security Policy or Security Context Constraints. Different Beats and their features might require different settings set in their PSP/[SCC](k8s-openshift-beats.md).


