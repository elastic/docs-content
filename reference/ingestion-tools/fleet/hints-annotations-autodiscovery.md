---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/hints-annotations-autodiscovery.html
---

# Hints annotations based autodiscover [hints-annotations-autodiscovery]

::::{warning}
This functionality is in beta and is subject to change. The design and code is less mature than official GA features and is being provided as-is with no warranties. Beta features are not subject to the support SLA of official GA features.
::::


::::{note}
Make sure you are using {{agent}} 8.5+.
::::


::::{note}
Hints autodiscovery only works with {{agent}} Standalone.
::::


Standalone {{agent}} supports autodiscover based on hints from the [provider](/reference/ingestion-tools/fleet/kubernetes-provider.md). The hints mechanism looks for hints in Kubernetes Pod annotations that have the prefix `co.elastic.hints`. As soon as the container starts, {{agent}} checks it for hints and launches the proper configuration for the container. Hints tell {{agent}} how to monitor the container by using the proper integration. This is the full list of supported hints:


## Required hints: [_required_hints]


### `co.elastic.hints/package` [_co_elastic_hintspackage]

The package to use for monitoring.


## Optional hints available: [_optional_hints_available]


### `co.elastic.hints/host` [_co_elastic_hintshost]

The host to use for metrics retrieval. If not defined, the host will be set as the default one: `<pod-ip>:<container-port>`.


### `co.elastic.hints/data_stream` [_co_elastic_hintsdata_stream]

The list of data streams to enable. If not specified, the integration’s default data streams are used. To find the defaults, refer to the [Elastic integrations documentation](integration-docs://docs/reference/index.md).

If data streams are specified, additional hints can be defined per data stream. For example, `co.elastic.hints/info.period: 5m` if the data stream specified is `info` for the [Redis module](beats://docs/reference/metricbeat/metricbeat-module-redis.md).

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: redis
  annotations:
    co.elastic.hints/package: redis
    co.elastic.hints/data_streams: info
    co.elastic.hints/info.period: 5m
```

If data stream hints are not specified, the top level hints will be used in its configuration.


### `co.elastic.hints/metrics_path` [_co_elastic_hintsmetrics_path]

The path to retrieve the metrics from.


### `co.elastic.hints/period` [_co_elastic_hintsperiod]

The time interval for metrics retrieval, for example, 10s.


### `co.elastic.hints/timeout` [_co_elastic_hintstimeout]

Metrics retrieval timeout, for example, 3s.


### `co.elastic.hints/username` [_co_elastic_hintsusername]

The username to use for authentication.


### `co.elastic.hints/password` [_co_elastic_hintspassword]

The password to use for authentication. It is recommended to retrieve this sensitive information from an ENV variable and avoid placing passwords in plain text.


### `co.elastic.hints/stream` [_co_elastic_hintsstream]

The stream to use for logs collection, for example, stdout/stderr.

If the specified package has no logs support, a generic container’s logs input will be used as a fallback. See the `Hints autodiscovery for kubernetes log collection` example below.


### `co.elastic.hints/processors` [_co_elastic_hintsprocessors]

Define a processor to be added to the  input configuration. See [*Define processors*](/reference/ingestion-tools/fleet/agent-processors.md) for the list of supported processors.

If the processors configuration uses list data structure, object fields must be enumerated. For example, hints for the rename processor configuration below

```yaml
processors:
  - rename:
      fields:
        - from: "a.g"
          to: "e.d"
      fail_on_error: true
```

will look like:

```yaml
co.elastic.hints/processors.rename.fields.0.from: "a.g"
co.elastic.hints/processors.rename.fields.1.to: "e.d"
co.elastic.hints/processors.rename.fail_on_error: 'true'
```

If the processors configuration uses map data structure, enumeration is not needed. For example, the equivalent to the `add_fields` configuration below

```yaml
processors:
  - add_fields:
      target: project
      fields:
        name: myproject
```

is

```yaml
co.elastic.hints/processors.1.add_fields.target: "project"
co.elastic.hints/processors.1.add_fields.fields.name: "myproject"
```

In order to provide ordering of the processor definition, numbers can be provided. If not, the hints builder will do arbitrary ordering:

```yaml
co.elastic.hints/processors.1.dissect.tokenizer: "%{key1} %{key2}"
co.elastic.hints/processors.dissect.tokenizer: "%{key2} %{key1}"
```

In the above sample the processor definition tagged with `1` would be executed first.

::::{important}
Processor configuration is not supported on the datastream level, so annotations like `co.elastic.hints/<datastream>.processors` are ignored.
::::



## Multiple containers [_multiple_containers]

When a pod has multiple containers, the settings are shared unless you put the container name in the hint. For example, these hints configure `processors.decode_json_fields` for all containers in the pod, but set a specific `stream` hint for the container called sidecar.

```yaml
annotations:
  co.elastic.hints/processors.decode_json_fields.fields: "message"
	co.elastic.hints/processors.decode_json_fields.add_error_key: true
	co.elastic.hints/processors.decode_json_fields.overwrite_keys: true
	co.elastic.hints/processors.decode_json_fields.target: "team"
	co.elastic.hints.sidecar/stream: "stderr"
```


## Available packages that support hints autodiscovery [_available_packages_that_support_hints_autodiscovery]

The available packages that are supported through hints can be found [here](https://github.com/elastic/elastic-agent/tree/main/deploy/kubernetes/elastic-agent-standalone/templates.d).


## Configure hints autodiscovery [_configure_hints_autodiscovery]

To enable hints autodiscovery, you must add `hints.enabled: true` to the provider’s configuration:

```yaml
providers:
  kubernetes:
    hints.enabled: true
```

Then ensure that an init container is specified by uncommenting the respective sections in the {{agent}} manifest. An init container is required to download the hints templates.

```yaml
initContainers:
- name: k8s-templates-downloader
  image: docker.elastic.co/elastic-agent/elastic-agent:master
  command: ['bash']
  args:
    - -c
    - >-
      mkdir -p /usr/share/elastic-agent/state/inputs.d &&
      curl -sL https://github.com/elastic/elastic-agent/archive/master.tar.gz | tar xz -C /usr/share/elastic-agent/state/inputs.d --strip=5 "elastic-agent-master/deploy/kubernetes/elastic-agent-standalone/templates.d"
  securityContext:
    runAsUser: 0
  volumeMounts:
    - name: elastic-agent-state
      mountPath: /usr/share/elastic-agent/state
```

::::{note}
The {{agent}} can load multiple configuration files from `{path.config}/inputs.d`  and finally produce a unified one (refer to [*Configure standalone {{agent}}s*](/reference/ingestion-tools/fleet/configure-standalone-elastic-agents.md)). Users have the ability to manually mount their own templates under `/usr/share/elastic-agent/state/inputs.d` **if they want to skip enabling initContainers section**.
::::



## Examples: [_examples]


### Hints autodiscovery for redis [_hints_autodiscovery_for_redis]

Enabling hints allows users deploying Pods on the cluster to automatically turn on Elastic monitoring at Pod deployment time. For example, to deploy a Redis Pod on the cluster and automatically enable Elastic monitoring, add the proper hints as annotations on the Pod manifest file:

```yaml
...
apiVersion: v1
kind: Pod
metadata:
  name: redis
  annotations:
    co.elastic.hints/package: redis
    co.elastic.hints/data_streams: info
    co.elastic.hints/host: '${kubernetes.pod.ip}:6379'
    co.elastic.hints/info.period: 5s
  labels:
    k8s-app: redis
    app: redis
...
```

After deploying this Pod, the data will start flowing in automatically. You can find it on the index `metrics-redis.info-default`.

::::{note}
All assets (dashboards, ingest pipelines, and so on) related to the Redis integration are not installed. You need to explicitly [install them through {{kib}}](/reference/ingestion-tools/fleet/install-uninstall-integration-assets.md).
::::



### Hints autodiscovery for kubernetes log collection [_hints_autodiscovery_for_kubernetes_log_collection]

The log collection for Kubernetes autodiscovered pods can be supported by using  [container_logs.yml template](https://github.com/elastic/elastic-agent/tree/main/deploy/kubernetes/elastic-agent-standalone/templates.d/container_logs.yml). Elastic Agent needs to emit a container_logs mapping so as to start collecting logs for all the discovered containers **even if no annotations are present in the containers**.

1. Follow steps described above to enable Hints Autodiscover
2. Make sure that relevant `container_logs.yml` template will be mounted under /usr/share/elastic-agent/state/inputs.d/ folder of Elastic Agent
3. Deploy Elastic Agent Manifest
4. Elastic Agent should be able to discover all containers inside kuernetes cluster and to collect available logs.

The previous default behaviour can be disabled with `hints.default_container_logs: false`. So this will disable the automatic logs collection from all discovered pods. Users need specifically to annotate their pod with following annotations:

```yaml
annotations:
  co.elastic.hints/package: "container_logs"
```

```yaml
providers.kubernetes:
  node: ${NODE_NAME}
  scope: node
  hints:
    enabled: true
    default_container_logs: false
...
```

In the following sample nginx manifest, we will additionally provide specific stream annotation, in order to configure the filestream input to read only stderr stream:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    app: nginx
  name: nginx
  namespace: default
spec:
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
      annotations:
        co.elastic.hints/package: "container_logs"
        co.elastic.hints/stream: "stderr"
    spec:
      containers:
      - image: nginx
        name: nginx
...
```

Users can monitor the final rendered Elastic Agent configuration:

```bash
kubectl exec -ti -n kube-system elastic-agent-7fkzm -- bash


/usr/share/elastic-agent# /elastic-agent inspect -v --variables --variables-wait 2s

inputs:
- data_stream.namespace: default
  id: hints-container-logs-3f69573a1af05c475857c1d0f98fc55aa01b5650f146d61e9653a966cd50bd9c-kubernetes-1780aca0-3741-4c8c-aced-b9776ba3fa81.nginx
  name: filestream-generic
  original_id: hints-container-logs-3f69573a1af05c475857c1d0f98fc55aa01b5650f146d61e9653a966cd50bd9c
  [output truncated ....]
  streams:
  - data_stream:
      dataset: kubernetes.container_logs
      type: logs
    exclude_files: []
    exclude_lines: []
    parsers:
    - container:
        format: auto
        stream: stderr
    paths:
    - /var/log/containers/*3f69573a1af05c475857c1d0f98fc55aa01b5650f146d61e9653a966cd50bd9c.log
    prospector:
      scanner:
        symlinks: true
    tags: []
  type: filestream
  use_output: default
outputs:
  default:
    hosts:
    - https://elasticsearch:9200
    password: changeme
    type: elasticsearch
    username: elastic
providers:
  kubernetes:
    hints:
      default_container_logs: false
      enabled: true
    node: control-plane
    scope: node
```


### Hints autodiscovery for kubernetes logs with JSON decoding [_hints_autodiscovery_for_kubernetes_logs_with_json_decoding]

Based on the previous example, users might want to perform extra processing on specific logs, for example to decode specific fields containing JSON strings. Use of [decode_json_fields](/reference/ingestion-tools/fleet/decode-json-fields.md) is advisable as follows:

You need to have enabled hints autodiscovery, as described in the previous `Hints autodiscovery for Kubernetes log collection` example.

The pod that will produce JSON logs needs to be annotated with:

```yaml
 annotations:
        co.elastic.hints/package: "container_logs"
        co.elastic.hints/processors.decode_json_fields.fields: "message"
        co.elastic.hints/processors.decode_json_fields.add_error_key: 'true'
        co.elastic.hints/processors.decode_json_fields.overwrite_keys: 'true'
        co.elastic.hints/processors.decode_json_fields.target: "team"
```

:::{note}
These parameters for the decode_json_fields processor are just an example.
:::

The following log entry:

```json
{"myteam": "ole"}
```

Will produce both fields: the original `message` field and also the target field `team`.

```json
"team": {
      "myteam": "ole"
    },

"message": "{\"myteam\": \"ole\"}",
```


## Troubleshooting [_troubleshooting]

When things do not work as expected, you may need to troubleshoot your setup. Here we provide some directions to speed up your investigation:

1. Exec inside an Agent’s Pod and run the `inspect` command to verify how inputs are constructed dynamically:

    ```sh
    ./elastic-agent inspect --variables --variables-wait 1s -c /etc/elastic-agent/agent.yml
    ```

    Specifically, examine how the inputs are being populated.

2. View the {{agent}} logs:

    ```sh
    tail -f /etc/elastic-agent/data/logs/elastic-agent-*.ndjson
    ```

    Verify that the hints feature is enabled in the config and look for hints-related logs like: "Generated hints mappings are …​" In these logs, you can find the mappings that are extracted out of the annotations and determine if the values can populate a specific input.

3. View the {{metricbeat}} logs:

    ```sh
    tail -f /etc/elastic-agent/data/logs/default/metricbeat-*.ndjson
    ```

4. View the {{filebeat}} logs:

    ```sh
    tail -f /etc/elastic-agent/data/logs/default/filebeat-*.ndjson
    ```

5. View the target input template. For the Redis example:

    ```sh
    cat f /usr/share/elastic-agent/state/inputs.d/redis.yml
    ```


