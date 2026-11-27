---
navigation_title: Get started with OpenTelemetry profiling
description: Set up OpenTelemetry profiling in Elastic Observability. Check host requirements, deploy the eBPF profiler with Elastic Agent or the OTel Collector, and verify that profiles reach Kibana.
applies_to:
  stack: preview 9.6+
  serverless: preview
products:
  - id: observability
type: how-to
---

# Get started with OpenTelemetry profiling [profiling-otel-get-started]

OpenTelemetry profiling collects whole-system, always-on CPU profiles from your Linux hosts with the [OpenTelemetry eBPF profiler](https://opentelemetry.io/docs/concepts/signals/profiles/). It doesn't require code instrumentation, debug symbols on the host, or service restarts, and it works with native code and most popular languages, such as Java, Python, and Node.js, out of the box.

To use OpenTelemetry profiling, install the **OpenTelemetry Profiling** integration on the hosts you want to profile, point it at your deployment or project, and the data shows up in the **Profiling** app.

On {{serverless-full}}, OpenTelemetry profiling is the only supported way to collect profiles.

## How it works [profiling-otel-how-it-works]

The profiler is a receiver that runs inside {{agent}}, or inside any OpenTelemetry Collector that includes it, on each host you profile. It reads stack samples from the kernel through eBPF (which is why it needs elevated privileges) and sends the profiles straight to {{es}} with the `elasticsearch` exporter. There is no separate backend to install or operate, as OpenTelemetry profiling only needs the profiler on the host and an {{es}} endpoint it can reach. {{es}} stores the profiles in data streams that it creates automatically.

## Before you begin [profiling-otel-requirements]

### Deployment or project [profiling-otel-requirements-deployment]

* {{stack}} 9.6 or later on {{ech}}, {{ece}}, {{eck}}, or a self-managed deployment, or an {{obs-serverless}} project. For the serverless tiers required, refer to [{{obs-serverless}} feature tiers](/solutions/observability/observability-serverless-feature-tiers.md).
* On {{ech}}, {{ece}}, {{eck}}, and self-managed deployments, a [subscription]({{subscriptions}}) that includes Profiling.
* On self-managed and {{eck}} deployments, the Profiling app must be turned on in {{kib}}, as described in [Turn on Profiling](#profiling-otel-enable-self-managed).
* {{kib}} privileges to add integrations and manage agent policies in {{fleet}} if you deploy the profiler with {{fleet}}. Refer to [Required roles and privileges](/reference/fleet/fleet-roles-privileges.md) for the roles that grant them.

### Hosts to profile [profiling-otel-requirements-hosts]

The profiler runs on each host you want to profile. Every host must meet these requirements:

* Linux with an x86_64 or ARM64 CPU. The profiler doesn't run on other operating systems or CPU architectures.
* Linux kernel 5.10 or later with eBPF support.
* Access to the host's `tracefs` or `debugfs` filesystem. On Linux, `tracefs` is mounted at `/sys/kernel/tracing`. If the profiler runs in a container, mount that host directory read-only at `/sys/kernel/tracing` in the container. Running the container as privileged doesn't expose the directory.
* Root privileges or the `CAP_SYS_ADMIN` capability for the profiler process. {{agent}} in [unprivileged mode](/reference/fleet/elastic-agent-unprivileged.md) is not supported: run it as root.
* {{agent}} 9.4 or later if you deploy the profiler with {{fleet}}.

The profiler captures native code, such as C, C++, Go, and Rust, as well as applications written in these runtimes:

| Runtime | Minimum version |
| --- | --- |
| JVM/JDK | 7 |
| Python | 3.6 |
| V8 (Node.js) | 8.1.0 |
| Perl | 5.28 |
| PHP | 7.3 |
| Ruby | 2.5 |
| .NET | 6 |
| Erlang/OTP | 27.2.4 |

## Turn on Profiling [profiling-otel-enable-self-managed]

On {{ech}}, {{ece}}, and {{serverless-short}}, the Profiling app is turned on by default. However, on self-managed and {{eck}} deployments, the {{kib}} plugin is turned off. To turn it on, add the following setting to [`kibana.yml`](/deploy-manage/stack-settings.md) and restart {{kib}}:

```yaml
xpack.profiling.enabled: true
```

On {{eck}}, add this setting under `spec.config` in the {{kib}} resource. For more information, refer to [Configure {{kib}} on {{eck}}](/deploy-manage/deploy/cloud-on-k8s/k8s-kibana-advanced-configuration.md#k8s-kibana-configuration). This setting is the only {{kib}} configuration OpenTelemetry profiling needs. You don't need to change anything in {{es}}, as the profiling plugin and the OpenTelemetry index templates are installed by default.

## Deploy the profiler [profiling-otel-deploy]

Select the deployment option that matches how you run {{agent}}:

* [{{agent}} managed by {{fleet}}](#profiling-otel-deploy-fleet): Configure the profiler once in an agent policy, and {{fleet}} rolls it out to every enrolled host.
* [Standalone {{agent}} configured as an OTel Collector](#profiling-otel-deploy-standalone): Manage the Collector configuration yourself on each host.
* [{{agent}} configured as an OTel Collector on {{k8s}}](#profiling-otel-deploy-kubernetes): Run the Collector as a DaemonSet with the OpenTelemetry Collector Helm chart to profile every node in a cluster. If {{fleet}} manages your agents on {{k8s}}, use the {{fleet}} option instead.

These options run the same `profiling` receiver. For details about the integration, refer to [OpenTelemetry Profiling](integration-docs://reference/profiling_otel.md).

:::{note}
Whichever option you select, run exactly one profiler per host. Don't run a separate profiler container beside each application.
:::

### Deploy with {{agent}} managed by {{fleet}} [profiling-otel-deploy-fleet]

1. In {{kib}}, find **Infrastructure** in the navigation menu and open **Profiling**, or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Add data**. If your deployment or project has no profiling data yet, the **Add profiling data** page opens directly.
2. On the **Profiling** tab, click **Add OpenTelemetry Profiling integration**. The page opens in **{{integrations}}**. You can also find it by searching for **OpenTelemetry Profiling** in **{{integrations}}**.
3. Click **Add OpenTelemetry Profiling** and configure the integration:
    * Optionally, expand the settings for **OpenTelemetry Profiling receiver**, then **Advanced options**, and set `samples_per_second` to change how often the profiler samples each CPU. Lower values reduce overhead and storage at the cost of detail.
    * Select an existing agent policy or [create a new one](/reference/fleet/agent-policy.md#create-a-policy). Every {{agent}} enrolled in this policy runs the profiler, so use a policy for hosts that meet the [host requirements](#profiling-otel-requirements-hosts).
4. Click **Save and continue**. {{fleet}} installs the integration and adds it to the agent policy you selected. Agents already enrolled in that policy receive it automatically.
5. [Install a {{fleet}}-managed {{agent}}](/reference/fleet/install-fleet-managed-elastic-agent.md) on each host you want to profile and enroll it in the policy. The agent must run as root.

If you run {{agent}} on {{k8s}} managed by {{fleet}}, follow [Run {{agent}} on {{k8s}} managed by {{fleet}}](/reference/fleet/running-on-kubernetes-managed-by-fleet.md) and make these changes in the DaemonSet. The profiler needs access to the host's processes, elevated privileges, and `tracefs`:

1. Set `hostPID: true` under `spec.template.spec`, and set the following `securityContext` on the {{agent}} container under `spec.template.spec.containers`:

    ```yaml
    securityContext:
      readOnlyRootFilesystem: true
      privileged: true
      runAsUser: 0
      runAsGroup: 0
      capabilities:
        add:
          - SYS_ADMIN
    ```

2. Mount the host's `/sys/kernel/tracing` directory read-only at `/sys/kernel/tracing` in the {{agent}} container. The security context alone doesn't expose `tracefs`.

### Deploy with a standalone {{agent}} configured as an OTel Collector [profiling-otel-deploy-standalone]

1. [Download and extract {{agent}}](elastic-agent://reference/edot-collector/download.md) for your Linux architecture. The package includes the `otelcol` executable.
2. In the extracted directory, save the following configuration as `otel.yml`. It adds the `profiling` receiver to a `profiles` pipeline and sends the profiles to {{es}} with the `elasticsearch` exporter in the `otel` mapping mode. Replace `<ELASTICSEARCH_ENDPOINT>` with your {{es}} URL and `<ELASTICSEARCH_API_KEY>` with an encoded {{es}} API key:

    ```yaml
    receivers:
      profiling:
        samples_per_second: 19 # Optional. Defaults to 20.

    exporters:
      elasticsearch:
        endpoint: <ELASTICSEARCH_ENDPOINT>
        api_key: <ELASTICSEARCH_API_KEY>
        mapping:
          mode: otel

    service:
      pipelines:
        profiles:
          receivers: [ profiling ]
          exporters: [ elasticsearch ]
    ```

3. Profiles support in the Collector is behind the `service.profilesSupport` feature gate. From the extracted directory, start the Collector with the feature turned on and with elevated privileges:

    ```bash
    sudo ./otelcol --config otel.yml --feature-gates=service.profilesSupport
    ```

#### Collect metrics using the `profilingmetrics` connector [profiling-otel-profilingmetrics]

Optionally, you can collect metrics instead of raw profiles. The `profilingmetrics` connector turns each stack sample into OpenTelemetry metrics that break down CPU time by frame type, shared library, kernel subsystem, and system call. Those metrics use less ingest and storage than raw profiles, and they power the [Elastic OTel Profiling Metrics](integration-docs://reference/profilingmetrics_otel.md) dashboards. However, as this configuration doesn't send raw profiles, the stacktraces, flamegraphs, and functions views stay empty.

1. Save the following configuration as `otel.yml`. Replace `<ELASTICSEARCH_ENDPOINT>` and `<ELASTICSEARCH_API_KEY>` with your {{es}} URL and API key:

    ```yaml
    receivers:
      profiling:
        samples_per_second: 19 # Optional. Defaults to 20.

    connectors:
      profilingmetrics:

    exporters:
      elasticsearch:
        endpoint: <ELASTICSEARCH_ENDPOINT>
        api_key: <ELASTICSEARCH_API_KEY>
        mapping:
          mode: otel

    service:
      pipelines:
        profiles:
          receivers: [ profiling ]
          exporters: [ profilingmetrics ]
        metrics:
          receivers: [ profilingmetrics ]
          exporters: [ elasticsearch ]
    ```

2. Start the Collector:

    ```bash
    sudo ./otelcol --config otel.yml --feature-gates=service.profilesSupport
    ```

   If it is already running, stop it and start it again with the same command.

### Deploy {{agent}} configured as an OTel Collector on {{k8s}} [profiling-otel-deploy-kubernetes]

To profile every node in a cluster, run the Collector as a DaemonSet. The [OpenTelemetry Collector Helm chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-collector) has a `profiling` preset that adds the receiver to a `profiles` pipeline and configures the host PID access, security context, and volumes the eBPF profiler needs.

1. Save the following example as `profiling-values.yml`. It uses the {{agent}} image, and the `ELASTIC_AGENT_OTEL` environment variable configures {{agent}} as an OTel Collector. Replace `<ELASTIC_AGENT_VERSION>` with the version you deploy, and replace the endpoint and API key placeholders with your {{es}} connection details. Set the image tag explicitly: the chart's default tag is an upstream Collector version, not an {{agent}} version.

    ```yaml
    mode: daemonset

    image:
      repository: docker.elastic.co/elastic-agent/elastic-agent
      tag: "<ELASTIC_AGENT_VERSION>"

    extraEnvs:
      - name: ELASTIC_AGENT_OTEL
        value: "true"

    presets:
      profiling:
        enabled: true

    command:
      extraArgs:
        - --feature-gates=service.profilesSupport

    config:
      exporters:
        elasticsearch:
          endpoint: <ELASTICSEARCH_ENDPOINT>
          api_key: <ELASTICSEARCH_API_KEY>
          mapping:
            mode: otel
      service:
        pipelines:
          profiles:
            exporters: [ elasticsearch ]
    ```

2. Install the chart with these values. The `profiling` preset requires chart version 0.152.1 or later. The command uses the minimum version, and you can replace it with a later one:

    ```bash
    helm upgrade --install profiling opentelemetry-collector \
      --repo https://open-telemetry.github.io/opentelemetry-helm-charts \
      --version 0.152.1 \
      --namespace profiling --create-namespace \
      --values profiling-values.yml
    ```

## Verify that profiles are flowing [profiling-otel-verify]

A few minutes after the profiler starts, check if data is arriving:

* In {{kib}}, find **Infrastructure** in the navigation menu and open **Profiling**, or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then open **Stacktraces**. The **Executables**, **Threads**, **Traces**, and **Hosts** graphs show data. If your deployment also has Universal Profiling data, make sure that the schema selector below the search bar shows **OpenTelemetry**. For more information on how the selector picks a default and which schemas it lists, refer to [Select a profiling schema](profiling.md#profiling-schema-selector).
* In **{{dev-tools-app}}**, count events in the OpenTelemetry profiling data streams:

    ```console
    GET /profiling-events-all.otel-*/_count
    ```

    A `count` greater than `0` confirms that OpenTelemetry profile events have been indexed. This count includes all retained events. You can use the time picker in **Stacktraces** to check recent ingestion.

Profiles appear in stacktraces, flamegraphs, and functions views. To learn how to read them, refer to [Profiling](profiling.md).

If no data arrives, refer to [Troubleshoot OpenTelemetry profiling](/troubleshoot/observability/troubleshoot-opentelemetry-profiling.md) to match the symptom you see in the {{agent}} logs or in {{kib}} with its fix.

## Where profiles are stored [profiling-otel-data-streams]

OpenTelemetry profiles are stored in data streams that follow the OpenTelemetry semantic conventions:

| Data | Data stream |
| --- | --- |
| Profile events | `profiling-events-*.otel-default` |
| Stack traces | `profiling-stacktraces.otel-default` |
| Stack frames | `profiling-stackframes.otel-default` |
| Executables | `profiling-executables.otel-default` |
| Host metadata | `profiling-hosts.otel-default` |

Retention is managed with the [data stream lifecycle](/manage-data/lifecycle/data-stream.md). 

:::{note}
The Universal Profiling pages about [{{ilm}}](universal-profiling-index-life-cycle-management.md) and the **Storage explorer** don't apply to these data streams. Any data that you might have collected with Universal Profiling is not migrated.
:::
