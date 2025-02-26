---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/kubernetes-provider.html
---

# Kubernetes Provider [kubernetes-provider]

Provides inventory information from Kubernetes.


## Provider configuration [_provider_configuration_2]

```yaml
providers.kubernetes:
  node: ${NODE_NAME}
  scope: node
  #kube_config: /Users/elastic-agent/.kube/config
  #sync_period: 600s
  #cleanup_timeout: 60s
  resources:
    pod:
      enabled: true
```

`node`
:   (Optional) Specify the node to scope {{agent}} to in case it cannot be accurately detected by the default discovery approach:

    1. If {{agent}} is deployed in Kubernetes cluster as Pod, use hostname of pod as the pod name to query pod metadata for node name.
    2. If step 1 fails or {{agent}} is deployed outside of the Kubernetes cluster, use machine-id to match against Kubernetes nodes for node name.
    3. If node cannot be discovered with step 1 or 2 fall back to `NODE_NAME` environment variable as default value. In case it is not set return error.


`cleanup_timeout`
:   (Optional) Specify the time of inactivity before stopping the running configuration for a container. This is `60s` by default.

`sync_period`
:   (Optional) Specify the timeout for listing historical resources.

`kube_config`
:   (Optional) Use the given config file as configuration for Kubernetes client. If `kube_config` is not set, the `KUBECONFIG` environment variable will be checked and will fall back to InCluster if not present. InCluster mode means that if {{agent}} runs as a Pod it will try to initialize the client using the token and certificate that are mounted in the Pod by default:

    * `/var/run/secrets/kubernetes.io/serviceaccount/token`
    * `/var/run/secrets/kubernetes.io/serviceaccount/ca.crt`


as well as using the environment variables `KUBERNETES_SERVICE_HOST` and `KUBERNETES_SERVICE_PORT` to reach the API Server. `kube_client_options`:: (Optional) Additional options can be configured for Kubernetes client. Currently client QPS and burst are supported, if not set Kubernetes client’s [default QPS and burst](https://pkg.go.dev/k8s.io/client-go/rest#pkg-constants) will be used. Example:

```yaml
      kube_client_options:
        qps: 5
        burst: 10
```

`scope`
:   (Optional) Specify the level for autodiscover. `scope` can either take `node` or `cluster` as values. `node` scope allows discovery of resources in the specified node. `cluster` scope allows cluster wide discovery. Only `pod` and `node` resources can be discovered at node scope.

`resources`
:   (Optional) Specify the resources that want to start the autodiscovery for. One of `pod`, `node`, `service`. By default `node` and `pod` are being enabled. `service` resource requires the `scope` to be set at `cluster`.

`namespace`
:   (Optional) Select the namespace from which to collect the metadata. If it is not set, the processor collects metadata from all namespaces. It is unset by default.

`include_annotations`
:   (Optional) If added to the provider config, then the list of annotations present in the config are added to the event.

`include_labels`
:   (Optional) If added to the provider config, then the list of labels present in the config will be added to the event.

`exclude_labels`
:   (Optional) If added to the provider config, then the list of labels present in the config will be excluded from the event.

`labels.dedot`
:   (Optional) If set to be `true` in the provider config, then `.` in labels will be replaced with `_`. By default it is `true`.

`annotations.dedot`
:   (Optional) If set to be `true` in the provider config, then `.` in annotations will be replaced with `_`. By default it is `true`.

`add_resource_metadata`
:   (Optional) Specify filters and configration for the extra metadata, that will be added to the event. Configuration parameters:

    * `node` or `namespace`: Specify labels and annotations filters for the extra metadata coming from node and namespace. By default all labels are included while annotations are not. To change the default behaviour `include_labels`, `exclude_labels` and `include_annotations` can be defined. These settings are useful when storing labels and annotations that require special handling to avoid overloading the storage output. The enrichment of `node` or `namespace` metadata can be individually disabled by setting `enabled: false`. Wildcards are supported in these settings by using `use_regex_include: true` in combination with `include_labels`, and respectively by setting `use_regex_exclude: true` in combination with `exclude_labels`.
    * `deployment`: If resource is `pod` and it is created from a `deployment`, by default the deployment name isn’t added, this can be enabled by setting `deployment: true`.
    * `cronjob`: If resource is `pod` and it is created from a `cronjob`, by default the cronjob name isn’t added, this can be enabled by setting `cronjob: true`. Example:


```yaml
      add_resource_metadata:
        namespace:
          #use_regex_include: false
          include_labels: ["namespacelabel1"]
          #use_regex_exclude: false
          #exclude_labels: ["namespacelabel2"]
        node:
          #use_regex_include: false
          include_labels: ["nodelabel2"]
          include_annotations: ["nodeannotation1"]
          #use_regex_exclude: false
          #exclude_labels: ["nodelabel3"]
        #deployment: false
        #cronjob: false
```


## Provider for Pod resources [_provider_for_pod_resources]

The available keys are:

| Key | Type | Description |
| --- | --- | --- |
| `kubernetes.namespace` | `string` | Namespace of the Pod |
| `kubernetes.namespace_uid` | `string` | UID of the Namespace of the Pod |
| `kubernetes.namespace_labels.*` | `object` | Labels of the Namespace of the Pod |
| `kubernetes.namespace_annotations.*` | `object` | Annotations of the Namespace of the Pod |
| `kubernetes.pod.name` | `string` | Name of the Pod |
| `kubernetes.pod.uid` | `string` | UID of the Pod |
| `kubernetes.pod.ip` | `string` | IP of the Pod |
| `kubernetes.labels.*` | `object` | Object of labels of the Pod |
| `kubernetes.annotations.*` | `object` | Object of annotations of the Pod |
| `kubernetes.container.name` | `string` | Name of the container |
| `kubernetes.container.runtime` | `string` | Runtime of the container |
| `kubernetes.container.id` | `string` | ID of the container |
| `kubernetes.container.image` | `string` | Image of the container |
| `kubernetes.container.port` | `string` | Port of the container (if defined) |
| `kubernetes.container.port_name` | `string` | Port’s name for the container (if defined) |
| `kubernetes.node.name` | `string` | Name of the Node |
| `kubernetes.node.uid` | `string` | UID of the Node |
| `kubernetes.node.hostname` | `string` | Hostname of the Node |
| `kubernetes.node.labels.*` | `string` | Labels of the Node |
| `kubernetes.node.annotations.*` | `string` | Annotations of the Node |
| `kubernetes.deployment.name.*` | `string` | Deployment name of the Pod (if exists) |
| `kubernetes.statefulset.name.*` | `string` | StatefulSet name of the Pod (if exists) |
| `kubernetes.replicaset.name.*` | `string` | ReplicaSet name of the Pod (if exists) |

These are the fields available within config templating. The `kubernetes.*` fields will be available on each emitted event.

::::{note}
`kubernetes.labels.*` and `kubernetes.annotations.*` used in config templating are not dedoted and should not be confused with labels and annotations added in the final Elasticsearch document and which are dedoted by default. For examples refer to [Conditions based autodiscover](/reference/ingestion-tools/fleet/conditions-based-autodiscover.md).
::::


Note that not all of these fields are available by default and special configuration options are needed in order to include them.

For example, if the Kubernetes provider provides the following inventory:

```json
[
    {
       "id": "1",
       "mapping:": {"namespace": "kube-system", "pod": {"name": "kube-controllermanger"}},
       "processors": {"add_fields": {"kuberentes.namespace": "kube-system", "kubernetes.pod": {"name": "kube-controllermanger"}}
    {
        "id": "2",
        "mapping:": {"namespace": "kube-system", "pod": {"name": "kube-scheduler"}},
        "processors": {"add_fields": {"kubernetes.namespace": "kube-system", "kubernetes.pod": {"name": "kube-scheduler"}}
    }
]
```

{{agent}} automatically prefixes the result with `kubernetes`:

```json
[
    {"kubernetes": {"id": "1", "namespace": {"name": "kube-system"}, "pod": {"name": "kube-controllermanger"}},
    {"kubernetes": {"id": "2", "namespace": {"name": "kube-system"}, "pod": {"name": "kube-scheduler"}},
]
```

In addition, the Kubernetes metadata are being added to each event by default.


## Provider for Node resources [_provider_for_node_resources]

```yaml
providers.kubernetes:
  node: ${NODE_NAME}
  scope: node
  #kube_config: /Users/elastic-agent/.kube/config
  #sync_period: 600s
  #cleanup_timeout: 60s
  resources:
    node:
      enabled: true
```

This resource is enabled by default but in this example we define it explicitly for clarity.

The available keys are:

| Key | Type | Description |
| --- | --- | --- |
| `kubernetes.labels.*` | `object` | Object of labels of the Node |
| `kubernetes.annotations.*` | `object` | Object of labels of the Node |
| `kubernetes.node.name` | `string` | Name of the Node |
| `kubernetes.node.uid` | `string` | UID of the Node |
| `kubernetes.node.hostname` | `string` | Hostname of the Node |


## Provider for Service resources [_provider_for_service_resources]

```yaml
providers.kubernetes:
  node: ${NODE_NAME}
  scope: cluster
  #kube_config: /Users/elastic-agent/.kube/config
  #sync_period: 600s
  #cleanup_timeout: 60s
  resources:
    service:
      enabled: true
```

Note that this resource is only available with `scope: cluster` setting and `node` cannot be used as scope.

The available keys are:

| Key | Type | Description |
| --- | --- | --- |
| `kubernetes.namespace` | `string` | Namespace of the Service |
| `kubernetes.namespace_uid` | `string` | UID of the Namespace of the Service |
| `kubernetes.namespace_labels.*` | `object` | Labels of the Namespace of the Service |
| `kubernetes.namespace_annotations.*` | `object` | Annotations of the Namespace of the Service |
| `kubernetes.labels.*` | `object` | Object of labels of the Service |
| `kubernetes.annotations.*` | `object` | Object of labels of the Service |
| `kubernetes.service.name` | `string` | Name of the Service |
| `kubernetes.service.uid` | `string` | UID of the Service |
| `kubernetes.selectors.*` | `string` | Kubernetes selectors |

Refer to [kubernetes autodiscovery with Elastic Agent](/reference/ingestion-tools/fleet/elastic-agent-kubernetes-autodiscovery.md) for more information about shaping dynamic inputs for autodiscovery.

