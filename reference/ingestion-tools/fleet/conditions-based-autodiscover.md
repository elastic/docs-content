---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/conditions-based-autodiscover.html
---

# Conditions based autodiscover [conditions-based-autodiscover]

You can define autodiscover conditions in each input to allow {{agent}} to automatically identify Pods and start monitoring them using predefined integrations. Refer to [Inputs](/reference/ingestion-tools/fleet/elastic-agent-input-configuration.md) to get an idea.

::::{important}
Condition definition is supported both in **{{agent}} managed by {{fleet}}** and in **standalone** scenarios.
::::


For more information about variables and conditions in input configurations, refer to [Variables and conditions in input configurations](/reference/ingestion-tools/fleet/dynamic-input-configuration.md). You can find available variables of autodiscovery in [Kubernetes Provider](/reference/ingestion-tools/fleet/kubernetes-provider.md).

## Example: Target Pods by label [_example_target_pods_by_label]

To automatically identify a Redis Pod and monitor it with the Redis integration, uncomment the following input configuration inside the [{{agent}} Standalone manifest](https://github.com/elastic/elastic-agent/blob/main/deploy/kubernetes/elastic-agent-standalone-kubernetes.yaml):

```yaml
- name: redis
  type: redis/metrics
  use_output: default
  meta:
    package:
      name: redis
      version: 0.3.6
  data_stream:
    namespace: default
  streams:
    - data_stream:
        dataset: redis.info
        type: metrics
      metricsets:
        - info
      hosts:
        - '${kubernetes.pod.ip}:6379'
      idle_timeout: 20s
      maxconn: 10
      network: tcp
      period: 10s
      condition: ${kubernetes.labels.app} == 'redis'
```

The condition `${kubernetes.labels.app} == 'redis'` will make the {{agent}} look for a Pod with the  label `app:redis` within the scope defined in its manifest.

For a list of provider fields that you can use in conditions, refer to [Kubernetes Provider](/reference/ingestion-tools/fleet/kubernetes-provider.md). Some examples of conditions usage are:

1. For a pod with label `app.kubernetes.io/name=ingress-nginx` the condition should be `condition: ${kubernetes.labels.app.kubernetes.io/name} == "ingress-nginx"`.
2. For a pod with annotation `prometheus.io/scrape: "true"` the condition should be `${kubernetes.annotations.prometheus.io/scrape} == "true"`.
3. For a pod with name `kube-scheduler-kind-control-plane` the condition should be `${kubernetes.pod.name} == "kube-scheduler-kind-control-plane"`.

The `redis` input defined in the {{agent}} manifest only specifies the`info` metricset. To learn about other available metricsets and their configuration settings, refer to the [Redis module page](beats://docs/reference/metricbeat/metricbeat-module-redis.md).

To deploy Redis, you can apply the following example manifest:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: redis
  labels:
    k8s-app: redis
    app: redis
spec:
  containers:
  - image: redis
    imagePullPolicy: IfNotPresent
    name: redis
    ports:
    - name: redis
      containerPort: 6379
      protocol: TCP
```

You should now be able to see Redis data flowing in on index `metrics-redis.info-default`. Make sure the port in your Redis manifest file matches the port used in the Redis input.

::::{note}
All assets (dashboards, ingest pipelines, and so on) related to the Redis integration are not installed. You need to explicitly [install them through {{kib}}](/reference/ingestion-tools/fleet/install-uninstall-integration-assets.md).
::::


Conditions can also be used in inputs configuration in order to set the target host dynamically for a targeted Pod based on its labels. This is useful for datasets that target specific pods like `kube-scheduler` or `kube-controller-manager`. The following configuration will enable `kubernetes.scheduler` dataset only for pods which have the label `component=kube-scheduler` defined.

```yaml
- data_stream:
    dataset: kubernetes.scheduler
    type: metrics
  metricsets:
    - scheduler
  bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
  hosts:
    - 'https://${kubernetes.pod.ip}:10259'
  period: 10s
  ssl.verification_mode: none
  condition: ${kubernetes.labels.component} == 'kube-scheduler'
```

::::{note}
Pods' labels and annotations can be used in autodiscover conditions. In the case of labels or annotations that include dots(`.`), they can be used in conditions exactly as they are defined in the pods. For example `condition: ${kubernetes.labels.app.kubernetes.io/name} == 'ingress-nginx'`. This should not be confused with the dedoted (by default) labels and annotations stored into Elasticsearch([Kubernetes Provider](/reference/ingestion-tools/fleet/kubernetes-provider.md)).
::::


::::{warning}
Before the 8.6 release, labels used in autodiscover conditions were dedoted in case the `labels.dedot` parameter was set to `true` in Kubernetes Provider configuration (by default `true`). The same did not apply for annotations. This was fixed in 8.6 release. Refer to the Release Notes section of the version 8.6.0 documentation.
::::


::::{warning}
In some "As a Service" Kubernetes implementations, like GKE, the control plane nodes or even the Pods running on them won’t be visible. In these cases, it won’t be possible to use scheduler metricsets, necessary for this example. Refer [scheduler and controller manager](beats://docs/reference/metricbeat/metricbeat-module-kubernetes.md#_scheduler_and_controllermanager) to find more information.
::::


Following the Redis example, if you deploy another Redis Pod with a different port, it should be detected. To check this, go, for example, to the field `service.address` under `metrics-redis.info-default`. It should be displaying two different services.

To obtain the policy generated by this configuration, connect to {{agent}} container:

```sh
kubectl exec -n kube-system --stdin --tty elastic-agent-standalone-id -- /bin/bash
```

Do not forget to change the `elastic-agent-standalone-id` to your {{agent}} Pod’s name. Moreover, make sure that your Pod is inside `kube-system`. If not, change `-n kube-system` to the correct namespace.

Inside the container [inspect the output](/reference/ingestion-tools/fleet/agent-command-reference.md) of the configuration file you used for the {{agent}}:

```sh
elastic-agent inspect --variables --variables-wait 1s -c /etc/elastic-agent/agent.yml
```

::::{dropdown} You should now be able to see the generated policy. If you look for the `scheduler`, it will look similar to this.
```yaml
- bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
  hosts:
    - https://172.19.0.2:10259
  index: metrics-kubernetes.scheduler-default
  meta:
    package:
      name: kubernetes
      version: 1.9.0
  metricsets:
    - scheduler
  module: kubernetes
  name: kubernetes-node-metrics
  period: 10s
  processors:
    - add_fields:
        fields:
          labels:
            component: kube-scheduler
            tier: control-plane
          namespace: kube-system
          namespace_labels:
            kubernetes_io/metadata_name: kube-system
          namespace_uid: 03d6fd2f-7279-4db4-9a98-51e50bbe5c62
          node:
            hostname: kind-control-plane
            labels:
              beta_kubernetes_io/arch: amd64
              beta_kubernetes_io/os: linux
              kubernetes_io/arch: amd64
              kubernetes_io/hostname: kind-control-plane
              kubernetes_io/os: linux
              node-role_kubernetes_io/control-plane: ""
              node_kubernetes_io/exclude-from-external-load-balancers: ""
            name: kind-control-plane
            uid: b8d65d6b-61ed-49ef-9770-3b4f40a15a8a
          pod:
            ip: 172.19.0.2
            name: kube-scheduler-kind-control-plane
            uid: f028ad77-c82a-4f29-ba7e-2504d9b0beef
        target: kubernetes
    - add_fields:
        fields:
          cluster:
            name: kind
            url: kind-control-plane:6443
        target: orchestrator
    - add_fields:
        fields:
          dataset: kubernetes.scheduler
          namespace: default
          type: metrics
        target: data_stream
    - add_fields:
        fields:
          dataset: kubernetes.scheduler
          target: event
    - add_fields:
        fields:
          id: ""
          snapshot: false
          version: 8.3.0
        target: elastic_agent
    - add_fields:
        fields:
          id: ""
        target: agent
  ssl.verification_mode: none
```

::::



## Example: Dynamic logs path [_example_dynamic_logs_path]

To set the log path of Pods dynamically in the configuration, use a variable in the {{agent}} policy to return path information from the provider:

```yaml
- name: container-log
  id: container-log-${kubernetes.pod.name}-${kubernetes.container.id}
  type: filestream
  use_output: default
  meta:
    package:
      name: kubernetes
      version: 1.9.0
  data_stream:
    namespace: default
  streams:
    - data_stream:
      dataset: kubernetes.container_logs
      type: logs
      prospector.scanner.symlinks: true
      parsers:
        - container: ~
      paths:
        - /var/log/containers/*${kubernetes.container.id}.log
```

::::{dropdown} The policy generated by this configuration will look similar to this for every Pod inside the scope defined in the manifest.
```yaml
- id: container-log-etcd-kind-control-plane-af311067a62fa5e4d6e5cb4d31e64c1c35d82fe399eb9429cd948d5495496819
  index: logs-kubernetes.container_logs-default
  meta:
    package:
      name: kubernetes
      version: 1.9.0
  name: container-log
  parsers:
    - container: null
  paths:
    - /var/log/containers/*af311067a62fa5e4d6e5cb4d31e64c1c35d82fe399eb9429cd948d5495496819.log
  processors:
    - add_fields:
        fields:
          id: af311067a62fa5e4d6e5cb4d31e64c1c35d82fe399eb9429cd948d5495496819
          image:
            name: registry.k8s.io/etcd:3.5.4-0
          runtime: containerd
        target: container
    - add_fields:
        fields:
          container:
            name: etcd
        labels:
          component: etcd
          tier: control-plane
        namespace: kube-system
        namespace_labels:
          kubernetes_io/metadata_name: kube-system
        namespace_uid: 03d6fd2f-7279-4db4-9a98-51e50bbe5c62
        node:
          hostname: kind-control-plane
          labels:
            beta_kubernetes_io/arch: amd64
            beta_kubernetes_io/os: linux
            kubernetes_io/arch: amd64
            kubernetes_io/hostname: kind-control-plane
            kubernetes_io/os: linux
            node-role_kubernetes_io/control-plane: ""
            node_kubernetes_io/exclude-from-external-load-balancers: ""
          name: kind-control-plane
          uid: b8d65d6b-61ed-49ef-9770-3b4f40a15a8a
        pod:
          ip: 172.19.0.2
          name: etcd-kind-control-plane
          uid: 08970fcf-bb93-487e-b856-02399d81fb29
      target: kubernetes
    - add_fields:
        fields:
          cluster:
            name: kind
            url: kind-control-plane:6443
        target: orchestrator
    - add_fields:
        fields:
          dataset: kubernetes.container_logs
          namespace: default
          type: logs
        target: data_stream
    - add_fields:
        fields:
          dataset: kubernetes.container_logs
        target: event
    - add_fields:
        fields:
          id: ""
          snapshot: false
          version: 8.3.0
        target: elastic_agent
    - add_fields:
        fields:
          id: ""
        target: agent
  prospector.scanner.symlinks: true
  type: filestream
```

::::



