---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elastic-agent-configuration-examples.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
navigation_title: Configuration examples
---

# Standalone Elastic Agent configuration examples on {{eck}} [k8s-elastic-agent-configuration-examples]

This section contains manifests that illustrate common use cases, and can be your starting point in exploring Elastic Agent deployed with ECK. These manifests are self-contained and work out-of-the-box on any non-secured Kubernetes cluster. They all contain a three-node {{es}} cluster and a single {{kib}} instance. Add the corresponding integration package to {{kib}} to install the dashboards, visualizations and other assets for each of these examples as described in [the Elastic Agent documentation](/reference/fleet/install-elastic-agents.md).

::::{warning}
The examples in this section are for illustration purposes only and should not be considered to be production-ready. Some of these examples use the `node.store.allow_mmap: false` setting which has performance implications and should be tuned for production workloads, as described in [Virtual memory](virtual-memory.md).
::::


## System integration [k8s_system_integration]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/elastic-agent/system-integration.yaml
```

Deploys Elastic Agent as a DaemonSet in standalone mode with system integration enabled. Collects syslog logs, auth logs and system metrics (for CPU, I/O, filesystem, memory, network, process and others).


## Kubernetes integration [k8s_kubernetes_integration]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/elastic-agent/kubernetes-integration.yaml
```

Deploys Elastic Agent as a DaemonSet in standalone mode with Kubernetes integration enabled. Collects API server, Container, Event, Node, Pod, Volume and system metrics.


## Multiple {{es}} clusters output [k8s_multiple_elasticsearch_clusters_output]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/elastic-agent/multi-output.yaml
```

Deploys two {{es}} clusters and two {{kib}} instances together with single Elastic Agent DaemonSet in standalone mode with System integration enabled. System metrics are sent to the `elasticsearch` cluster. Elastic Agent monitoring data is sent to `elasticsearch-mon` cluster.


## Storing local state in host path volume [k8s_storing_local_state_in_host_path_volume]

::::{include} _snippets/storing-local-state-host-path-volume.md