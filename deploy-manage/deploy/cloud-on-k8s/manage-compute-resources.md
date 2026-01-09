---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-managing-compute-resources.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Manage compute resources [k8s-managing-compute-resources]

To help the Kubernetes scheduler correctly place Pods in available Kubernetes nodes and ensure quality of service (QoS), it is recommended to specify the CPU and memory requirements for objects managed by the operator ({{eck_resources_list}}). In Kubernetes, `requests` defines the minimum amount of resources that must be available for a Pod to be scheduled; `limits` defines the maximum amount of resources that a Pod is allowed to consume. For more information about how Kubernetes uses these concepts, check [Managing Compute Resources for Containers](https://kubernetes.io/docs/concepts/configuration/manage-compute-resources-container/).

::::{note}
The operator applies default requests and limits for memory and CPU. They may be suitable for experimenting with the {{stack}}, however it is recommended to reevaluate these values for production use cases.
::::


Consider that Kubernetes throttles containers exceeding the CPU limit defined in the `limits` section. Do not set this value too low, or it would affect the performance of your workloads, even if you have enough resources available in the Kubernetes cluster.

Also, to minimize disruption caused by Pod evictions due to resource contention, you can run Pods at the "Guaranteed" QoS level by setting both `requests` and `limits` to the same value.


## Set compute resources [k8s-compute-resources]

You can set compute resource constraints in the `podTemplate` of objects managed by the operator.


### Set compute resources for {{es}} [k8s-compute-resources-elasticsearch]

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 1
    podTemplate:
      spec:
        containers:
        - name: elasticsearch
          resources:
            requests:
              memory: 4Gi
              cpu: 8
            limits:
              memory: 4Gi
```


#### Memory limit and JVM Heap settings [k8s-elasticsearch-memory]

Starting with {{es}} 7.11, the heap size of the JVM is automatically calculated based on the node roles and the available memory. The available memory is defined by the value of `resources.limits.memory` set on the `elasticsearch` container in the Pod template, or the available memory on the Kubernetes node if no limit is set.

For {{es}} before 7.11, or if you want to override the default calculated heap size on newer versions, set the `ES_JAVA_OPTS` environment variable in the `podTemplate` to an appropriate value:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 1
    podTemplate:
      spec:
        containers:
        - name: elasticsearch
          env:
          - name: ES_JAVA_OPTS
            value: -Xms2g -Xmx2g
          resources:
            requests:
              memory: 4Gi
              cpu: 8
            limits:
              memory: 4Gi
```


#### CPU resources [k8s-elasticsearch-cpu]

The value set for CPU limits or requests directly impacts the {{es}} `node.processors` setting. By default {{es}} automatically detects the number of processors and sets the thread pool settings based on it. The following table gives the default value for `node.processors` given the CPU limits and requests set on the `elasticsearch` container:

|  | No CPU limit | With CPU limit |
| --- | --- | --- |
| No CPU request | `All the available cores on the K8S node` | `Value of the CPU limit` |
| CPU request set to 1 | `All the available cores on the K8S node` | `Value of the CPU limit` |
| Other CPU requests | `Value of the CPU request` | `Value of the CPU limit` |

You can also set your own value for `node.processors` in the {{es}} config.

::::{note}
A [known Kubernetes issue](https://github.com/kubernetes/kubernetes/issues/51135) may lead to over-aggressive CPU limits throttling. If the host Linux Kernel does not include [this CFS quota fix](https://github.com/kubernetes/kubernetes/issues/67577), you may want to:

* not set any CPU limit in the {{es}} resource (Burstable QoS)
* [reduce the CFS quota period](https://github.com/kubernetes/kubernetes/pull/63437) in kubelet configuration
* [disable CFS quotas](https://github.com/kubernetes/kubernetes/issues/51135#issuecomment-386319185) in kubelet configuration

::::



### Set compute resources for {{kib}}, Elastic Maps Server, APM Server and Logstash [k8s-compute-resources-kibana-and-apm]

```yaml subs=true
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  podTemplate:
    spec:
      containers:
      - name: kibana
        env:
          - name: NODE_OPTIONS
            value: "--max-old-space-size=2048"
        resources:
          requests:
            memory: 1Gi
            cpu: 0.5
          limits:
            memory: 2.5Gi
            cpu: 2
```

```yaml subs=true
apiVersion: maps.k8s.elastic.co/v1alpha1
kind: ElasticMapsServer
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  podTemplate:
    spec:
      containers:
      - name: maps
        env:
          - name: NODE_OPTIONS
            value: "--max-old-space-size=980"
        resources:
          requests:
            memory: 1Gi
            cpu: 1
          limits:
            memory: 1Gi
            cpu: 1
```

```yaml subs=true
apiVersion: apm.k8s.elastic.co/v1
kind: ApmServer
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  podTemplate:
    spec:
      containers:
      - name: apm-server
        resources:
          requests:
            memory: 1Gi
            cpu: 0.5
          limits:
            memory: 2Gi
            cpu: 2
```

% enterprise search not available in 9.0+ so this uses a hardcoded version

```yaml
apiVersion: enterprisesearch.k8s.elastic.co/v1
kind: EnterpriseSearch
metadata:
  name: enterprise-search-quickstart
spec:
  version: 8.19.1
  podTemplate:
    spec:
      containers:
      - name: enterprise-search
        resources:
          requests:
            memory: 4Gi
            cpu: 1
          limits:
            memory: 4Gi
            cpu: 2
        env:
        - name: JAVA_OPTS
          value: -Xms3500m -Xmx3500m
```

```yaml subs=true
apiVersion: logstash.k8s.elastic.co/v1
kind: logstash
metadata:
  name: logstash-quickstart
spec:
  version: {{version.stack}}
  podTemplate:
    spec:
      containers:
      - name: logstash
        resources:
          requests:
            memory: 4Gi
            cpu: 1
          limits:
            memory: 4Gi
            cpu: 2
        env:
        - name: LS_JAVA_OPTS
          value: -Xms2000m -Xmx2000m
```

For the container name, use `apm-server`, `maps`,  `kibana` or `enterprise-search`, respectively.


### Set compute resources for Beats and Elastic Agent [k8s-compute-resources-beats-agent]

For Beats or Elastic Agent objects, the `podTemplate` can be configured as follows, depending on the chosen deployment model.

When deploying as a Kubernetes Deployment:

```yaml subs=true
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: quickstart
spec:
  type: filebeat
  version: {{version.stack}}
  deployment:
    podTemplate:
      spec:
        containers:
        - name: filebeat
          resources:
            requests:
              memory: 300Mi
              cpu: 0.5
            limits:
              memory: 500Mi
              cpu: 0.5
```

When deploying as a Kubernetes DaemonSet:

```yaml subs=true
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: elastic-agent
spec:
  version: {{version.stack}}
  daemonSet:
    podTemplate:
      spec:
        containers:
        - name: agent
          resources:
            requests:
              memory: 300Mi
              cpu: 0.5
            limits:
              memory: 300Mi
              cpu: 0.5
```

For the container name, use the name of the Beat in lower case. For example `filebeat`, `metricbeat`, or `heartbeat`. In case of Elastic Agent, use `agent`.


## Default behavior [k8s-default-behavior]

If `resources` is not defined in the specification of an object, then the operator applies a default memory limit to ensure that Pods have enough resources to start correctly. This memory limit will also be applied to any user-defined init containers that do not have explict resource requirements set. As the operator cannot make assumptions about the available CPU resources in the cluster, no CPU limits will be set — resulting in the Pods having the "Burstable" QoS class. Check if this is acceptable for your use case and follow the instructions in [Set compute resources](#k8s-compute-resources) to configure appropriate limits.

| Type | Requests | Limits |
| --- | --- | --- |
| APM Server | `512Mi` | `512Mi` |
| {{es}} | `2Gi` | `2Gi` |
| {{kib}} | `1Gi` | `1Gi` |
| Beat | `300Mi` | `300Mi` |
| Elastic Agent | `400Mi` | `400Mi` |
| Elastic Maps Server | `200Mi` | `200Mi` |
| Logstash | `2Gi` | `2Gi` |
| Elastic Package Registry | `1Gi` | `1Gi` |
| AutoOps Agent | `400Mi` | `400Mi` |

If the Kubernetes cluster is configured with [LimitRanges](https://kubernetes.io/docs/tasks/administer-cluster/manage-resources/memory-default-namespace/) that enforce a minimum memory constraint, they could interfere with the operator defaults and cause object creation to fail.

For example, you might have a `LimitRange` that enforces a default and minimum memory limit on containers as follows:

```yaml
apiVersion: v1
kind: LimitRange
metadata:
  name: default-mem-per-container
spec:
  limits:
  - min:
      memory: "3Gi"
    defaultRequest:
      memory: "3Gi"
    type: Container
```

With this limit range in place, if you create an {{es}} object without defining the `resources` section, you will get the following error:

```
Cannot create pod elasticsearch-sample-es-ldbgj48c7r: pods "elasticsearch-sample-es-ldbgj48c7r" is forbidden: minimum memory usage per Container is 3Gi, but request is 2Gi
```
To avoid this, explicitly define the requests and limits mandated by your environment in the resource specification. It will prevent the operator from applying the built-in defaults.


## Monitor compute resources [k8s-monitor-compute-resources]


#### Using Beats [k8s-monitor-compute-resources-beats]

[Metricbeat](beats.md) can collect the percentage of both the CPU and the memory limits used by each Pod (or total node allocatable if resource is not limited). The two relevant metrics are `kubernetes.pod.cpu.usage.limit.pct` for CPU, and `kubernetes.pod.memory.usage.node.pct` for memory.

:::{image} /deploy-manage/images/cloud-on-k8s-metrics-explorer-cpu.png
:alt: cgroup CPU perforamce chart
:screenshot:
:::


#### Monitoring {{es}} CPU using Stack Monitoring [k8s-monitor-compute-resources-stack-monitoring]

If [Stack Monitoring](../../monitor/stack-monitoring/eck-stack-monitoring.md) is enabled, the pressure applied by the CPU cgroup controller to an {{es}} node can be evaluated from the **Stack Monitoring** page in {{kib}}.

1. On the **Stack Monitoring** page select the {{es}} node you want to monitor.
2. Select the **Advanced** tab.

In the following example, an {{es}} container is limited to 2 cores.

```yaml
nodeSets:
- name: default
  count: 3
  podTemplate:
    spec:
      containers:
        - name: elasticsearch
          resources:
            limits:
              cpu: 2
```

The **Cgroup usage** curve shows that the CPU usage of this container has been steadily increasing up to 2 cores. Then, while the container was still requesting more CPU, the **Cgroup Throttling** curve shows how much the {{es}} container has been throttled:

:::{image} /deploy-manage/images/cloud-on-k8s-cgroups-cfs-stats.png
:alt: cgroup CPU perforamce chart
:screenshot:
:::

