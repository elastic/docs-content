---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/kubernetes_leaderelection-provider.html
---

# Kubernetes LeaderElection Provider [kubernetes_leaderelection-provider]

Provides the option to enable leaderelection between a set of {{agent}}s running on Kubernetes. Only one {{agent}} at a time will be the holder of the leader lock and based on this, configurations can be enabled with the condition that the {{agent}} holds the leadership. This is useful in cases where the {{agent}} between a set of {{agent}}s collects cluster wide metrics for the Kubernetes cluster, such as the `kube-state-metrics` endpoint.

Provider needs a `kubeconfig` file to establish a connection to Kubernetes API. It can automatically reach the API if it’s running in an InCluster environment ({{agent}} runs as Pod).

```yaml
providers.kubernetes_leaderelection:
  #enabled: true
  #kube_config: /Users/elastic-agent/.kube/config
  #kube_client_options:
  #  qps: 5
  #  burst: 10
  #leader_lease: agent-k8s-leader-lock
  #leader_retryperiod: 2
  #leader_leaseduration: 15
  #leader_renewdeadline: 10
```

`enabled`
:   (Optional) Defaults to true. To explicitly disable the LeaderElection provider, set `enabled: false`.

`kube_config`
:   (Optional) Use the given config file as configuration for the Kubernetes client. If `kube_config` is not set, `KUBECONFIG` environment variable will be checked and will fall back to InCluster if it’s not present.

`kube_client_options`
:   (Optional) Configure additional options for the Kubernetes client. Supported options are `qps` and `burst`. If not set, the Kubernetes client’s default QPS and burst settings are used.

`leader_lease`
:   (Optional) Specify the name of the leader lease. This is set to `elastic-agent-cluster-leader` by default.

`leader_retryperiod`
:   (Optional) Default value 2 (in sec). How long before {{agent}}s try to get the `leader` role.

`leader_leaseduration`
:   (Optional) Default value 15 (in sec).  How long the leader {{agent}} holds the `leader` state.

`leader_renewdeadline`
:   (Optional) Default value 10 (in sec). How long leaders retry getting the `leader` role.

The available key is:

| Key | Type | Description |
| --- | --- | --- |
| `kubernetes_leaderelection.leader` | `bool` | The value of the leadership flag. This is set to `true` when the {{agent}} is the current leader, and is set to `false` otherwise. |


## Understanding leader timings [_understanding_leader_timings]

As described above, the LeaderElection configuration offers the following parameters: Lease duration (`leader_leaseduration`), Renew deadline (`leader_renewdeadline`), and Retry period (`leader_retryperiod`). Based on the config provided, each agent will trigger {{k8s}} API requests and will try to check the status of the lease.

::::{note}
The number of leader calls to the K8s Control API is proportional to the number of {{agent}}s installed. This means that requests will come from all {{agent}}s per `leader_retryperiod`. Setting `leader_retryperiod` to a greater value than the default (2sec), means that fewer requests will be made towards the {{k8s}} Control API, but will also increase the period where collection of metrics from the leader {{agent}} might be lost.
::::


The library applies [specific checks](https://github.com/kubernetes/client-go/blob/master/tools/leaderelection/leaderelection.go#L76) for the timing parameters and if those are not verified {{agent}} will exit with a `panic` error.

In general: - Leaseduration must be greater than renewdeadline - Renewdeadline must be greater than retryperiod*JitterFactor.

::::{note}
Constant JitterFactor=1.2 is defined in [leaderelection lib](https://pkg.go.dev/gopkg.in/kubernetes/client-go.v11/tools/leaderelection).
::::



## Enabling configurations only when on leadership [_enabling_configurations_only_when_on_leadership]

Use conditions based on the `kubernetes_leaderelection.leader` key to leverage the leaderelection provider and enable specific inputs only when the {{agent}} holds the leadership lock. The below example enables the `state_container` metricset only when the leadership lock is acquired:

```yaml
- data_stream:
    dataset: kubernetes.state_container
    type: metrics
  metricsets:
    - state_container
  add_metadata: true
  hosts:
    - 'kube-state-metrics:8080'
  period: 10s
  condition: ${kubernetes_leaderelection.leader} == true
```

