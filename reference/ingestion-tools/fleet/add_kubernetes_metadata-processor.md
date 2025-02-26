---
navigation_title: "add_kubernetes_metadata"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add_kubernetes_metadata-processor.html
---

# Add Kubernetes metadata [add_kubernetes_metadata-processor]


::::{tip}
Inputs that collect logs and metrics use this processor by default, so you do not need to configure it explicitly.
::::


The `add_kubernetes_metadata` processor annotates each event with relevant metadata based on which Kubernetes Pod the event originated from. At startup it detects an `in_cluster` environment and caches the Kubernetes-related metadata.

For events to be annotated with Kubernetes-related metadata, the Kubernetes configuration must be valid.

Each event is annotated with:

* Pod Name
* Pod UID
* Namespace
* Labels

In addition, the node and namespace metadata are added to the Pod metadata.

The `add_kubernetes_metadata` processor has two basic building blocks:

* Indexers
* Matchers

Indexers use Pod metadata to create unique identifiers for each one of the Pods. These identifiers help to correlate the metadata of the observed Pods with actual events. For example, the `ip_port` indexer can take a Kubernetes Pod and create identifiers for it based on all its `pod_ip:container_port` combinations.

Matchers use information in events to construct lookup keys that match the identifiers created by the indexers. For example, when the `fields` matcher takes `["metricset.host"]` as a lookup field, it constructs a lookup key with the value of the field `metricset.host`. When one of these lookup keys matches with one of the identifiers, the event is enriched with the metadata of the identified Pod.

For more information about available indexers and matchers, plus some examples, refer to [Indexers and matchers](#kubernetes-indexers-and-matchers).


## Examples [_examples_3]

This configuration enables the processor when {{agent}} is run as a Pod in Kubernetes.

```yaml
  - add_kubernetes_metadata:
      # Defining indexers and matchers manually is required for {beatname_lc}, for instance:
      #indexers:
      #  - ip_port:
      #matchers:
      #  - fields:
      #      lookup_fields: ["metricset.host"]
      #labels.dedot: true
      #annotations.dedot: true
```

This configuration enables the processor on an {{agent}} running as a process on the Kubernetes node:

```yaml
  - add_kubernetes_metadata:
      host: <hostname>
      # If kube_config is not set, KUBECONFIG environment variable will be checked
      # and if not present it will fall back to InCluster
      kube_config: ${fleet} and {agent} Guide/.kube/config
      # Defining indexers and matchers manually is required for {beatname_lc}, for instance:
      #indexers:
      #  - ip_port:
      #matchers:
      #  - fields:
      #      lookup_fields: ["metricset.host"]
      #labels.dedot: true
      #annotations.dedot: true
```

This configuration disables the default indexers and matchers, and then enables different indexers and matchers:

```yaml
  - add_kubernetes_metadata:
      host: <hostname>
      # If kube_config is not set, KUBECONFIG environment variable will be checked
      # and if not present it will fall back to InCluster
      kube_config: ~/.kube/config
      default_indexers.enabled: false
      default_matchers.enabled: false
      indexers:
        - ip_port:
      matchers:
        - fields:
            lookup_fields: ["metricset.host"]
      #labels.dedot: true
      #annotations.dedot: true
```


## Configuration settings [_configuration_settings_7]

::::{note}
{{agent}} processors execute *before* ingest pipelines, which means that they process the raw event data rather than the final event sent to {{es}}. For related limitations, refer to [What are some limitations of using processors?](/reference/ingestion-tools/fleet/agent-processors.md#limitations)
::::


| Name | Required | Default | Description |
| --- | --- | --- | --- |
| `host` | No |  | Node to scope {{agent}} to in case it cannot be accurately detected, as when running {{agent}} in host network mode. |
| `scope` | No | `node` | Whether the processor should have visibility at the node level (`node`) or at the entire cluster level (`cluster`). |
| `namespace` | No |  | Namespace to collect the metadata from. If no namespaces is specified, collects metadata from all namespaces. |
| `add_resource_metadata` | No |  | Filters and configuration for adding extra metadata to the event. This setting accepts the following settings:<br><br>* `node` or `namespace`: Labels and annotations filters for the extra metadata coming from node and namespace. By default all labels are included, but annotations are not. To change the default behavior, you can set `include_labels`, `exclude_labels`, and `include_annotations`. These settings are useful when storing labels and annotations that require special handling to avoid overloading the storage output. Wildcards are supported in these settings by using `use_regex_include: true` in combination with `include_labels`, and respectively by setting `use_regex_exclude: true` in combination with `exclude_labels`. To turn off enrichment of `node` or `namespace` metadata individually, set `enabled: false`.<br>* `deployment`: If the resource is `pod` and it is created from a `deployment`, the deployment name is not added by default. To enable this behavior, set `deployment: true`.<br>* `cronjob`: If the resource is `pod` and it is created from a `cronjob`, the cronjob name is not added by default. To enable this behavior, set `cronjob: true`.<br><br>::::{dropdown} Expand this to see an example<br>```yaml<br>      add_resource_metadata:<br>        namespace:<br>          include_labels: ["namespacelabel1"]<br>          # use_regex_include: false<br>          # use_regex_exclude: false<br>          # exclude_labels: ["namespacelabel2"]<br>          #labels.dedot: true<br>          #annotations.dedot: true<br>        node:<br>          # use_regex_include: false<br>          include_labels: ["nodelabel2"]<br>          include_annotations: ["nodeannotation1"]<br>          # use_regex_exclude: false<br>          # exclude_annotations: ["nodeannotation2"]<br>          #labels.dedot: true<br>          #annotations.dedot: true<br>        deployment: true<br>        cronjob: true<br>```<br><br>::::<br><br> |
| `kube_config` | No | `KUBECONFIG` environment variable, if present | Config file to use as the configuration for the Kubernetes client. |
| `kube_client_options` | No |  | Additional configuration options for the Kubernetes client. Currently client QPS and burst are supported. If this setting is not configured, the Kubernetes client’s [default QPS and burst](https://pkg.go.dev/k8s.io/client-go/rest#pkg-constants) is used.<br><br>::::{dropdown} Expand this to see an example<br>```yaml<br>      kube_client_options:<br>        qps: 5<br>        burst: 10<br>```<br><br>::::<br><br> |
| `cleanup_timeout` | No | `60s` | Time of inactivity before stopping the running configuration for a container. |
| `sync_period` | No |  | Timeout for listing historical resources. |
| `labels.dedot` | No | `true` | Whether to replace dots (`.`) in labels with underscores (`_`).<br>`annotations.dedot` |


## Indexers and matchers [kubernetes-indexers-and-matchers]

The `add_kubernetes_metadata` processor has two basic building blocks:

* Indexers
* Matchers


### Indexers [_indexers]

Indexers use Pod metadata to create unique identifiers for each one of the Pods.

Available indexers are:

`container`
:   Identifies the Pod metadata using the IDs of its containers.

`ip_port`
:   Identifies the Pod metadata using combinations of its IP and its exposed ports. When using this indexer, metadata is identified using the combination of `ip:port` for each of the ports exposed by all containers of the pod. The `ip` is the IP of the pod.

`pod_name`
:   Identifies the Pod metadata using its namespace and its name as `namespace/pod_name`.

`pod_uid`
:   Identifies the Pod metadata using the UID of the Pod.


### Matchers [_matchers]

Matchers are used to construct the lookup keys that match with the identifiers created by indexes.

Available matchers are:

`field_format`
:   Looks up Pod metadata using a key created with a string format that can include event fields.

    This matcher has an option `format` to define the string format. This string format can contain placeholders for any field in the event.

    For example, the following configuration uses the `ip_port` indexer to identify the Pod metadata by combinations of the Pod IP and its exposed ports, and uses the destination IP and port in events as match keys:

    ```yaml
    - add_kubernetes_metadata:
        ...
        default_indexers.enabled: false
        default_matchers.enabled: false
        indexers:
          - ip_port:
        matchers:
          - field_format:
              format: '%{[destination.ip]}:%{[destination.port]}'
    ```


`fields`
:   Looks up Pod metadata using as key the value of some specific fields. When multiple fields are defined, the first one included in the event is used.

    This matcher has an option `lookup_fields` to define the files whose value will be used for lookup.

    For example, the following configuration uses the `ip_port` indexer to identify Pods, and defines a matcher that uses the destination IP or the server IP for the lookup, the first it finds in the event:

    ```yaml
    - add_kubernetes_metadata:
        ...
        default_indexers.enabled: false
        default_matchers.enabled: false
        indexers:
          - ip_port:
        matchers:
          - fields:
              lookup_fields: ['destination.ip', 'server.ip']
    ```


`logs_path`
:   Looks up Pod metadata using identifiers extracted from the log path stored in the `log.file.path` field.

    This matcher has the following configuration settings:

    `logs_path`
    :   (Optional) Base path of container logs. If not specified, it uses the default logs path of the platform where Agent is running: for Linux - `/var/lib/docker/containers/`, Windows - `C:\\ProgramData\\Docker\\containers`. To change the default value: container ID must follow right after the `logs_path` - `<log_path>/<container_id>`, where `container_id` is a 64-character-long hexadecimal string.

    `resource_type`
    :   (Optional) Type of the resource to obtain the ID of. Valid `resource_type`:

        * `pod`: to make the lookup based on the Pod UID. When `resource_type` is set to `pod`, `logs_path` must be set as well, supported path in this case:

            * `/var/lib/kubelet/pods/` used to read logs from mounted into the Pod volumes, those logs end up under `/var/lib/kubelet/pods/<pod UID>/volumes/<volume name>/...` To use `/var/lib/kubelet/pods/` as a `log_path`, `/var/lib/kubelet/pods` must be mounted into the filebeat Pods.
            * `/var/log/pods/` Note: when using `resource_type: 'pod'` logs will be enriched only with Pod metadata: Pod id, Pod name, etc., not container metadata.

        * `container`: to make the lookup based on the container ID, `logs_path` must be set to `/var/log/containers/`. It defaults to `container`.


    To be able to use `logs_path` matcher agent’s input path must be a subdirectory of directory defined in `logs_path` configuration setting.

    The default configuration is able to lookup the metadata using the container ID when the logs are collected from the default docker logs path (`/var/lib/docker/containers/<container ID>/...` on Linux).

    For example the following configuration would use the Pod UID when the logs are collected from `/var/lib/kubelet/pods/<pod UID>/...`.

    ```yaml
    - add_kubernetes_metadata:
        ...
        default_indexers.enabled: false
        default_matchers.enabled: false
        indexers:
          - pod_uid:
        matchers:
          - logs_path:
              logs_path: '/var/lib/kubelet/pods'
              resource_type: 'pod'
    ```


