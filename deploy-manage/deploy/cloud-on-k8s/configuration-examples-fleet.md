---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-elastic-agent-fleet-configuration-examples.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
navigation_title: Configuration examples
---

# Fleet managed agents configuration examples on {{eck}} [k8s-elastic-agent-fleet-configuration-examples]

This section contains manifests that illustrate common use cases, and can be your starting point in exploring {{agent}} deployed with ECK. These manifests are self-contained and work out-of-the-box on any non-secured {{k8s}} cluster. They all contain a three-node {{es}} cluster, a single {{kib}} instance and a single {{fleet-server}} instance.

::::{warning}
The examples in this section are for illustration purposes only and should not be considered to be production-ready. Some of these examples use the `node.store.allow_mmap: false` setting which has performance implications and should be tuned for production workloads, as described in [Virtual memory](virtual-memory.md).
::::


## System and {{k8s}} {{integrations}} [k8s_system_and_k8s_integrations]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/elastic-agent/fleet-kubernetes-integration.yaml
```

Deploys {{agent}} as a DaemonSet in {{fleet}} mode with System and {{k8s}} {{integrations}} enabled. System integration collects syslog logs, auth logs and system metrics (for CPU, I/O, filesystem, memory, network, process and others). {{k8s}} {{integrations}} collects API server, Container, Event, Node, Pod, Volume and system metrics.


## System and {{k8s}} {{integrations}} running as non-root [k8s_system_and_k8s_integrations_running_as_non_root]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/elastic-agent/fleet-kubernetes-integration-nonroot.yaml
```

The provided example is functionally identical to the previous section but runs the {{agent}} processes (both the {{agent}} running as the {{fleet}} server and the {{agent}} connected to {{fleet}}) as a non-root user by utilizing a DaemonSet to ensure directory and file permissions.

::::{note}
The DaemonSet itself must run as root to set up permissions and ECK >= 2.10.0 is required.
::::



## Custom logs integration with autodiscover [k8s_custom_logs_integration_with_autodiscover]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/elastic-agent/fleet-custom-logs-integration.yaml
```

Deploys {{agent}} as a DaemonSet in {{fleet}} mode with Custom Logs integration enabled. Collects logs from all Pods in the `default` namespace using autodiscover feature.


## APM integration [k8s_apm_integration]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/elastic-agent/fleet-apm-integration.yaml
```

Deploys single instance {{agent}} Deployment in {{fleet}} mode with APM integration enabled.


## Synthetic monitoring [k8s_synthetic_monitoring]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/elastic-agent/synthetic-monitoring.yaml
```

Deploys an {{fleet}}-enrolled {{agent}} that can be used as for [Synthetic monitoring](/solutions/observability/synthetics/index.md). This {{agent}} uses the `elastic-agent-complete` image. The agent policy still needs to be [registered as private location](/solutions/observability/synthetics/monitor-resources-on-private-networks.md#synthetics-private-location-add) in {{kib}}.

## Fleet Server exposed internally and externally [k8s_fleet_server_lb]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/elastic-agent/fleet-ingress-setup.yaml
```

This example shows how to expose the Fleet Server to the outside world using a Kubernetes Ingress resource. The Fleet Server is configured to use custom TLS certificates, and all communications are secured with TLS. The same Fleet Server is also accessible from within the cluster, allowing agents to connect to it regardless of their location. Refer to the comments in the `fleet-ingress-setup.yaml` file for more details on how to set up the Ingress resource and TLS certificates to enable this configuration.