---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-beat-configuration-examples.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
navigation_title: Configuration examples
---

# Beats configuration examples on {{eck}} [k8s-beat-configuration-examples]

In this section you can find manifests that address a number of common use cases and can be your starting point in exploring Beats deployed with ECK. These manifests are self-contained and work out-of-the-box on any non-secured Kubernetes cluster. They all contain three-node {{es}} cluster and single {{kib}} instance. All Beat configurations set up {{kib}} dashboards if they are available for a given Beat and all required RBAC resources.

::::{warning}
The examples in this section are purely descriptive and should not be considered to be production-ready. Some of these examples use the `node.store.allow_mmap: false` setting which has performance implications and should be tuned for production workloads, as described in [Virtual memory](virtual-memory.md).
::::


## Metricbeat for Kubernetes monitoring [k8s_metricbeat_for_kubernetes_monitoring]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/beats/metricbeat_hosts.yaml
```

Deploys Metricbeat as a DaemonSet that monitors the usage of the following resources:

* Host: CPU, memory, network, filesystem.
* Kubernetes: Nodes, Pods, Containers, Volumes.


## Filebeat with autodiscover [k8s_filebeat_with_autodiscover]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/beats/filebeat_autodiscover.yaml
```

Deploys Filebeat as a DaemonSet with the autodiscover feature enabled. It collects logs from Pods in every namespace and loads them to the connected {{es}} cluster.


## Filebeat with autodiscover for metadata [k8s_filebeat_with_autodiscover_for_metadata]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/beats/filebeat_autodiscover_by_metadata.yaml
```

Deploys Filebeat as a DaemonSet with the autodiscover feature enabled. Logs from Pods that match the following criteria are shipped to the connected {{es}} cluster:

* Pod is in `log-namespace` namespace
* Pod has `log-label: "true"` label


## Filebeat without autodiscover [k8s_filebeat_without_autodiscover]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/beats/filebeat_no_autodiscover.yaml
```

Deploys Filebeat as a DaemonSet with the autodiscover feature disabled. Uses the entire logs directory on the host as the input source. This configuration does not require any RBAC resources as no Kubernetes APIs are used.


## {{es}} and {{kib}} Stack Monitoring [k8s_elasticsearch_and_kibana_stack_monitoring]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/beats/stack_monitoring.yaml
```

Deploys Metricbeat configured for {{es}} and {{kib}} [Stack Monitoring](/deploy-manage/monitor/monitoring-data/visualizing-monitoring-data.md) and Filebeat using autodiscover. Deploys one monitored {{es}} cluster and one monitoring {{es}} cluster. You can access the Stack Monitoring app in the monitoring cluster’s {{kib}}.

::::{note}
In this example, TLS verification is disabled when Metricbeat communicates with the monitored cluster, which is not secure and should not be used in production. To solve this, use custom certificates and configure Metricbeat to verify them.
::::



## Heartbeat monitoring {{es}} and {{kib}} health [k8s_heartbeat_monitoring_elasticsearch_and_kibana_health]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/beats/heartbeat_es_kb_health.yaml
```

Deploys Heartbeat as a single Pod deployment that monitors the health of {{es}} and {{kib}} by TCP probing their Service endpoints. Heartbeat expects that {{es}} and {{kib}} are deployed in the `default` namespace.


## Auditbeat [k8s_auditbeat]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/beats/auditbeat_hosts.yaml
```

Deploys Auditbeat as a DaemonSet that checks file integrity and audits file operations on the host system.


## Packetbeat monitoring DNS and HTTP traffic [k8s_packetbeat_monitoring_dns_and_http_traffic]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/beats/packetbeat_dns_http.yaml
```

Deploys Packetbeat as a DaemonSet that monitors DNS on port `53` and HTTP(S) traffic on ports `80`, `8000`, `8080` and `9200`.


## OpenShift monitoring [k8s_openshift_monitoring]

```sh subs=true
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/{{version.eck | M.M}}/config/recipes/beats/openshift_monitoring.yaml
```

Deploys Metricbeat as a DaemonSet that monitors the host resource usage (CPU, memory, network, filesystem), OpenShift resources (Nodes, Pods, Containers, Volumes), API Server and Filebeat using autodiscover. Deploys an {{es}} cluster and {{kib}} to centralize data collection.
