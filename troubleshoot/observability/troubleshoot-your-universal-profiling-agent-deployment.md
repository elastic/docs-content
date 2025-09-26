---
navigation_title: Universal Profiling
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/profiling-troubleshooting.html
applies_to:
  stack: all
products:
  - id: observability
---



# Troubleshoot your Universal Profiling agent deployment [profiling-troubleshooting]


You can use the Universal Profiling Agent logs to find errors.

The following is an example of a *healthy* Universal Profiling Agent output:

```txt
time="..." level=info msg="Starting Prodfiler Host Agent v2.4.0 (revision develop-5cce978a, build timestamp 12345678910)"
time="..." level=info msg="Interpreter tracers: perl,php,python,hotspot,ruby,v8"
time="..." level=info msg="Automatically determining environment and machine ID ..."
time="..." level=warning msg="Environment tester (gcp) failed: failed to get GCP metadata: Get \"http://169.254.169.254/computeMetadata/v1/instance/id\": dial tcp 169.254.169.254:80: i/o timeout"
time="..." level=warning msg="Environment tester (azure) failed: failed to get azure metadata: Get \"http://169.254.169.254/metadata/instance/compute?api-version=2020-09-01&format=json\": context deadline exceeded (Client.Timeout exceeded while awaiting headers)"
time="..." level=warning msg="Environment tester (aws) failed: failed to get aws metadata: EC2MetadataRequestError: failed to get EC2 instance identity document\ncaused by: RequestError: send request failed\ncaused by: Get \"http://169.254.169.254/latest/dynamic/instance-identity/document\": context deadline exceeded (Client.Timeout exceeded while awaiting headers)"
time="..." level=info msg="Environment: hardware, machine ID: 0xdeadbeefdeadbeef"
time="..." level=info msg="Assigned ProjectID: 5"
time="..." level=info msg="Start CPU metrics"
time="..." level=info msg="Start I/O metrics"
time="..." level=info msg="Found tpbase offset: 9320 (via x86_fsbase_write_task)"
time="..." level=info msg="Environment variable KUBERNETES_SERVICE_HOST not set"
time="..." level=info msg="Supports eBPF map batch operations"
time="..." level=info msg="eBPF tracer loaded"
time="..." level=info msg="Attached tracer program"
time="..." level=info msg="Attached sched monitor"
```

A Universal Profiling Agent deployment is working if the output of the following command is empty:

```txt
head host-agent.log -n 15 | grep "level=error"
```

If running this command outputs error-level logs, the following are possible causes:

* The Universal Profiling Agent is running on an unsupported version of the Linux kernel, or its missing kernel features.

    If the Universal Profiling Agent is running on an unsupported kernel version, the following is logged:

    ```txt
    Universal Profiling Agent requires kernel version 4.19 or newer but got 3.10.0
    ```

    If eBPF features are not available in the kernel, the Universal Profiling Agent fails to start, and one of the following is logged:

    ```txt
    Failed to probe eBPF syscall
    ```

    or

    ```txt
    Failed to probe tracepoint
    ```

* The Universal Profiling Agent is not able to connect to {{ecloud}}. In this case, a similar message to the following is logged:

    ```txt
    Failed to setup gRPC connection (retrying...): context deadline exceeded
    ```

    Verify the `collection-agent` configuration value is set and is equal to what was printed  in Kibana, when clicking to **Add Data**.

* The secret token is not valid, or it has been changed. In this case, the Universal Profiling Agent gent shuts down, and logs a similar message to the following:

    ```txt
    rpc error: code = Unauthenticated desc = authentication failed
    ```

* The Universal Profiling Agent is unable to send data to your deployment. In this case, a similar message to the following is logged:

    ```txt
    Failed to report hostinfo (retrying...): rpc error: code = Unimplemented desc = unknown service collectionagent.CollectionAgent"
    ```

    This typically means that your {{ecloud}} cluster has not been configured for Universal Profiling. To configure your {{ecloud}} cluster, follow the steps in [configure data ingestion](../../solutions/observability/infra-and-hosts/get-started-with-universal-profiling.md#profiling-configure-data-ingestion).

* The collector (part of the backend in {{ecloud}} that receives data from the Universal Profiling Agent) ran out of memory. In this case, a similar message to the following is logged:

    ```txt
    Error: failed to invoke XXX(): Unavailable rpc error: code = Unavailable desc = unexpected HTTP status code received from server: 502 (Bad Gateway); transport: received unexpected content-type "application/json; charset=UTF-8"
    ```

    Verify that the collector is running by navigating to **{{ecloud}} → Deployments → `<Deployment Name>` → Integrations Server** in [Elastic Cloud](https://cloud.elastic.co/home). If the **Copy endpoint** link next to **Profiling** is grayed out, you need to restart the collector by clicking **Force Restart** under **Integrations Server Management**.

    For non-demo workloads, verify that the Integrations Server has at least the recommended 4GB of RAM. You can check this on the Integrations Server page under **Instances**.

* The Universal Profiling Agent is incompatible with the {{stack}} version. In this case, the following message is logged:

    ```txt
    rpc error: code = FailedPrecondition desc= HostAgent version is unsupported, please upgrade to the latest version
    ```

    Follow the Universal Profiling Agent deployment instructions shown in Kibana which will always be correct for the {{stack}} version that you are using.

* You are using a Universal Profling Agent from a newer {{stack}} version, configured to connect to an older {{stack}} version cluster. In this case, the following message is logged:

    ```txt
    rpc error: code = FailedPrecondition desc= Backend is incompatible with HostAgent, please check your configuration
    ```

    Follow the Universal Profiling Agent deployment instructions shown in Kibana which will always be correct for the {{stack}} version that you are using.


If you’re unable to find a solution to the Universal Profiling Agent failure, you can raise a support request indicating `Universal Profiling` and `Universal Profiling Agent` as the source of the problem.


## Enable verbose logging in Universal Profiling Agent [profiling-enable-verbose-logging]

During the support process, you may be asked to provide debug logs from one of the Universal Profiling Agent installations from your deployment.

To enable debug logs, add the `-verbose` command-line flag or the `verbose true` setting in the configuration file.

::::{note}
We recommend only enabling debug logs on a single instance of Universal Profiling Agent rather than an entire deployment to limit the amount of logs produced.
::::



## Improve load times [profiling-improve-load-time]

The amount of data loaded for the flamegraph, topN functions, and traces view can lead to latency when using a slow connection (e.g. DSL or mobile).

Setting the Kibana cluster option `server.compression.brotli.enabled: true` reduces the amount of data transferred and should reduce load time.


## Troubleshoot Universal Profiling Agent {{k8s}} deployments [profiling-troubleshoot-kubernetes]

When the Helm chart installation finishes, the output has instructions on how to check the Universal Profiling Agent pod status and read logs. The following sections provide potential scenarios when Universal Profiling Agent installation **is not healthy**.


### Taints [profiling-taints]

{{k8s}} clusters often include [taints and tolerations](https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/) in their setup. In these cases, a Universal Profiling Agent installation may show no pods or very few pods running, even for a large cluster.

This is because a taint precludes the execution of pods on a node unless the workload has been tolerated. The Helm chart `tolerations` key in the `values.yaml` sets the toleration of taints using the official {{k8s}} scheduling API format.

The following examples provide a `tolerations` config that you can add to the Helm chart `values.yaml`:

* To deploy the Universal Profiling Agent on all nodes with taint `workload=python:NoExecute`, add the following to the `values.yaml`:

    ```yaml
    tolerations:
    - key: "workload"
      value: "python"
      effect: "NoExecute"
    ```

* To deploy the Universal Profiling Agent on all nodes tainted with *key* `production` and effect `NoSchedule` (no value provided), add the following to the `values.yaml`:

    ```yaml
    tolerations:
      - key: "production"
        effect: "NoSchedule"
        operator: Exists
    ```

* To deploy the Universal Profiling Agent on all nodes, tolerating all taints, add the following to the `values.yaml`:

    ```yaml
    tolerations:
      - effect: NoSchedule
        operator: Exists
      - effect: NoExecute
        operator: Exists
    ```



### Security policy enforcement [profiling-security-policy-enforcement]

Some {{k8s}} clusters are configured with hardened security add-ons to limit the blast radius of exploited application vulnerabilities. Different hardening methodologies can impair Universal Profiling Agent operations and may, for example, result in pods continuously restarting after displaying a `CrashLoopBackoff` status.


#### {{k8s}} PodSecurityPolicy [profiling-kubernetes-podsecuritypolicy]
```{applies_to}
stack: deprecated
```

This {{k8s}} API [has been deprecated](https://kubernetes.io/blog/2021/04/06/podsecuritypolicy-deprecation-past-present-and-future/), but some still use it. A PodSecurityPolicy (PSP) may explicitly prevent the execution of `privileged` containers across the entire cluster.

Since Universal Profiling Agent *needs* privileges in most kernels/CRI, you need to build a PSP to allow the Universal Profiling Agent DaemonSet to run.


#### {{k8s}} policy engines [profiling-policy-engines]

Read more about {{k8s}} policy engines in the [SIG-Security documentation](https://github.com/kubernetes/sig-security/blob/main/sig-security-docs/papers/policy/kubernetes-policy-management.md).

The following tools *may* prevent the execution of Universal Profiling Agent pods as the Helm chart builds a cluster role and binds it into the Universal Profiling Agent service account (we use it for container metadata):

* Open Policy Agent Gatekeeper
* Kyverno
* Fairwinds Polaris

If you have a policy engine in place, configure it to allow the Universal Profiling Agent execution and RBAC configs.


#### Network configurations [profiling-network-config]

In some instances, your Universal Profiling Agent pods may be running fine, but they will not connect to the remote data collector gRPC interface and stay in the startup phase, while trying to connect periodically.

The following are potential causes:

* {{k8s}} [`NetworkPolicies`](https://kubernetes.io/docs/concepts/services-networking/network-policies/) define connectivity rules that prevent all outgoing traffic unless explicitly allow-listed.
* Cloud or datacenter provider network rules are restricting egress traffic to allowed destinations only (ACLs).


#### OS-level security [profiling-os-level-security]

These settings *are not part of {{k8s}}* and may have been included in the node setup. They can prevent the Universal Profiling Agent from working properly, as they intercept syscalls from the Universal Profiling Agent to the kernel and modify or block them.

If you have implemented security hardening (some providers listed below), you should know the privileges the Universal Profiling Agent needs.

* gVisor on GKE
* seccomp filters
* AppArmor LSM


## Submit a support request [profiling-submit-support]

You can submit a support request from the [support request page](https://cloud.elastic.co/support) in the {{ecloud}} console.

In the support request, specify if your issue deals with the Universal Profiling Agent or the Kibana app.


## Send feedback [profiling-send-feedback]

If troubleshooting and support are not fixing your issues, or you have any other feedback that you want to share about the product, send the Universal Profiling team an email at `profiling-feedback@elastic.co`.
