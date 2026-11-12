---
navigation_title: Get started with OpenTelemetry profiling
description: Set up OpenTelemetry profiling in Elastic Observability. Check host requirements, deploy the eBPF profiler with Elastic Agent or the OTel Collector, and verify that profiles reach Kibana.
applies_to:
  stack: preview 9.6+
  serverless: preview
products:
  - id: observability
---

# Get started with OpenTelemetry profiling [profiling-otel-get-started]

OpenTelemetry profiling collects whole-system, always-on CPU profiles from your Linux hosts with the [OpenTelemetry eBPF profiler](https://opentelemetry.io/docs/concepts/signals/profiles/). It doesn't require code instrumentation, debug symbols on the host, or service restarts, and it works with native code and most popular runtimes out of the box.

Unlike Universal Profiling, OpenTelemetry profiling needs no setup step in {{kib}}. Install the **OpenTelemetry Profiling** integration on the hosts you want to profile, point it at your deployment, and the data shows up in the **Profiling** app. On {{serverless-full}}, OpenTelemetry profiling is the only supported way to collect profiles.

## How it works [profiling-otel-how-it-works]

The profiler is a receiver that runs inside {{agent}}, or inside any OpenTelemetry Collector that includes it, on each host you profile. It reads stack samples from the kernel through eBPF, which is why it needs elevated privileges, and sends the profiles straight to {{es}} with the `elasticsearch` exporter. There is no separate backend to install or operate: unlike Universal Profiling, which needs its own collector and symbolizer services, OpenTelemetry profiling only needs the profiler on the host and an {{es}} endpoint it can reach. {{es}} stores the profiles in data streams that it creates automatically.

This page shows you how to:

* Check that your deployment and hosts meet the [requirements](#profiling-otel-requirements)
* [Turn on Profiling](#profiling-otel-enable-self-managed) on a self-managed or {{eck}} deployment
* [Deploy the profiler](#profiling-otel-deploy) on your hosts with {{fleet}}, a standalone Collector, or {{k8s}}
* [Verify](#profiling-otel-verify) that profiles are flowing and [find them](#profiling-otel-data-streams) in {{es}}

## Requirements [profiling-otel-requirements]

### Elastic deployment [profiling-otel-requirements-deployment]

* {{stack}} 9.6 or later on {{ech}}, {{ece}}, {{eck}}, or a self-managed deployment, or an {{obs-serverless}} project on the {{observability}} Complete tier. For the serverless tiers, refer to [{{obs-serverless}} feature tiers](/solutions/observability/observability-serverless-feature-tiers.md).
* On {{ech}}, {{ece}}, {{eck}}, and self-managed deployments, a [subscription]({{subscriptions}}) that includes Profiling.
* On self-managed and {{eck}} deployments, the Profiling app must be turned on in {{kib}}, as described in [Turn on Profiling](#profiling-otel-enable-self-managed).
* {{kib}} privileges to add integrations and manage agent policies in {{fleet}} if you deploy the profiler with {{fleet}}. Refer to [Required roles and privileges](/reference/fleet/fleet-roles-privileges.md) for the roles that grant them.

### Hosts to profile [profiling-otel-requirements-hosts]

The profiler runs on each host you want to profile. Every host must meet these requirements:

* Linux with an x86_64 or ARM64 CPU. The profiler doesn't run on other operating systems.
* Linux kernel 5.10 or later with eBPF support.
* Access to the host's `tracefs` or `debugfs` filesystem. If the profiler runs in a container, mount the host's `/sys/kernel/tracing` directory at the same path in the container, read-only.
* Root privileges, or the `CAP_SYS_ADMIN` capability, for the profiler process. If you use {{agent}}, run it as root rather than in [unprivileged mode](/reference/fleet/elastic-agent-unprivileged.md).
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

## Turn on Profiling on self-managed and {{eck}} deployments [profiling-otel-enable-self-managed]
```{applies_to}
deployment:
  self: ga
  eck: ga
```

On {{ech}}, {{ece}}, and {{serverless-short}}, the Profiling app is turned on for you. On self-managed and {{eck}} deployments, the {{kib}} plugin is turned off by default. Add the following setting to [`kibana.yml`](/deploy-manage/stack-settings.md) and restart {{kib}}:

```yaml
xpack.profiling.enabled: true
```

On {{eck}}, add this setting under `spec.config` in the Kibana resource. Refer to [Configure {{kib}} on {{eck}}](/deploy-manage/deploy/cloud-on-k8s/k8s-kibana-advanced-configuration.md#k8s-kibana-configuration). The setting is the same for both profiling approaches, but OpenTelemetry profiling does not require the Universal Profiling ingestion setup.

You don't need to change anything in {{es}}: the profiling plugin and the OpenTelemetry index templates are installed by default.

## Deploy the profiler [profiling-otel-deploy]

Select the deployment option that matches how you run {{agent}}:

* [{{agent}} managed by {{fleet}}](#profiling-otel-deploy-fleet): the recommended option. You configure the profiler once, in an agent policy, and {{fleet}} rolls it out to every enrolled host.
* [Standalone {{agent}} configured as an OTel Collector](#profiling-otel-deploy-standalone): when you manage the Collector configuration yourself.
* [{{k8s}}](#profiling-otel-deploy-kubernetes): when you want to profile every node in a cluster.

These options run the same `profiling` receiver. For details about the integration, refer to [OpenTelemetry Profiling](integration-docs://reference/profiling_otel.md).

Whichever option you select, run exactly one profiler per host. Running it in more than one container on the same host, or as a sidecar next to your application, is not supported.

### Deploy with {{agent}} managed by {{fleet}} [profiling-otel-deploy-fleet]

1. In {{kib}}, find **Profiling** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then click **Add data**. If your deployment has no profiling data yet, the **Add profiling data** page opens directly.
2. On the **Profiling** tab, click **Add OpenTelemetry Profiling integration**. The integration page opens in **{{integrations}}**. You can also find it by searching for **OpenTelemetry Profiling** in **{{integrations}}**.
3. Click **Add OpenTelemetry Profiling** and configure the integration:
    * Optionally, expand the settings for **OpenTelemetry Profiling receiver**, then **Advanced options**, and set `samples_per_second` to change how often the profiler samples each CPU. Lower values reduce overhead and storage at the cost of detail.
    * Select an existing agent policy or create a new one. Every {{agent}} enrolled in this policy runs the profiler, so use a policy for hosts that meet the [host requirements](#profiling-otel-requirements-hosts).
4. Click **Save and continue**. For the full procedure, refer to [Add an integration to a policy](/reference/fleet/add-integration-to-policy.md).
5. [Install a {{fleet}}-managed {{agent}}](/reference/fleet/install-fleet-managed-elastic-agent.md) on each host you want to profile and enroll it in the policy. The agent must run as root.

If you run {{agent}} on {{k8s}} managed by {{fleet}}, give the agent's DaemonSet access to the host's processes and the privileges the eBPF profiler needs. Set `hostPID: true` under `spec.template.spec`, and set the following `securityContext` on the Elastic Agent container under `spec.template.spec.containers`. Then follow [Run {{agent}} on {{k8s}} managed by {{fleet}}](/reference/fleet/running-on-kubernetes-managed-by-fleet.md):

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

Also mount the host's `/sys/kernel/tracing` directory read-only at `/sys/kernel/tracing` in the Agent container. The security context alone does not expose `tracefs`.

### Deploy with a standalone {{agent}} configured as an OTel Collector [profiling-otel-deploy-standalone]

[Download and extract {{agent}}](elastic-agent://reference/edot-collector/download.md) for your Linux architecture. The package includes the `otelcol` executable. Run the following commands from the extracted directory.

If you manage the Collector configuration yourself, add the `profiling` receiver to a `profiles` pipeline and send the profiles to {{es}} with the `elasticsearch` exporter in the `otel` mapping mode.

Save the following configuration as `otel.yml`. Replace `<ELASTICSEARCH_ENDPOINT>` with your {{es}} URL, for example `https://my-deployment.es.us-central1.gcp.cloud.es.io:443`, and `<ELASTICSEARCH_API_KEY>` with an encoded {{es}} API key:

```yaml
receivers:
  profiling:
    samples_per_second: 19

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

Profiles support in the Collector is behind the `service.profilesSupport` feature gate. Start the Collector with the feature gate turned on and with elevated privileges:

```bash
sudo ./otelcol --config otel.yml --feature-gates=service.profilesSupport
```

For the receiver's settings and the `profilingmetrics` connector, which turns profiles into lower-volume metrics, refer to [Configure profiles collection](elastic-agent://reference/edot-collector/config/configure-profiles-collection.md). The Universal Profiling ingestion setup described there applies to {{es}} versions earlier than 9.6. It is not required for this procedure.

### Deploy on {{k8s}} [profiling-otel-deploy-kubernetes]

To profile every node in a cluster, run the Collector as a DaemonSet. The [OpenTelemetry Collector Helm chart](https://github.com/open-telemetry/opentelemetry-helm-charts/tree/main/charts/opentelemetry-collector) has a `profiling` preset that adds the receiver to a `profiles` pipeline and configures the host PID access, security context, and volumes the eBPF profiler needs.

The following example uses the {{agent}} image in Collector mode. Save it as `profiling-values.yml`, replacing `<ELASTIC_AGENT_VERSION>` with the version you deploy and the endpoint and API key placeholders with your {{es}} connection details. Set the image tag explicitly: the chart's default tag is an upstream Collector version, not an {{agent}} version.

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

Install the chart with these values. Use a chart version that includes the `profiling` preset, such as 0.175.0:

```bash
helm upgrade --install profiling opentelemetry-collector \
  --repo https://open-telemetry.github.io/opentelemetry-helm-charts \
  --version 0.175.0 \
  --namespace profiling --create-namespace \
  --values profiling-values.yml
```

## Verify that profiles are flowing [profiling-otel-verify]

A few minutes after the profiler starts, check that data is arriving:

* In {{kib}}, find **Profiling** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then open **Stacktraces**. The **Threads**, **Traces**, and **Hosts** graphs show data, and the schema selector at the top of the page shows **OpenTelemetry**. If your deployment also has Universal Profiling data, make sure **OpenTelemetry** is selected. [Select a profiling schema](universal-profiling.md#profiling-schema-selector) explains how the selector picks a default and which schemas it lists.
* In **{{dev-tools-app}}**, count events in the OpenTelemetry profiling data streams:

    ```console
    GET /profiling-events-all.otel-*/_count
    ```

    A `count` greater than `0` confirms that OpenTelemetry profile events have been indexed. This count includes all retained events; use the time picker in **Stacktraces** to check recent ingestion.

Profiles appear in the same stacktraces, flamegraphs, and functions views as Universal Profiling data. To learn how to read them, refer to [Profiling](universal-profiling.md).

## Where profiles are stored [profiling-otel-data-streams]

OpenTelemetry profiles are stored in data streams that follow the OpenTelemetry semantic conventions:

| Data | Data stream |
| --- | --- |
| Profile events | `profiling-events-*.otel-default` |
| Stack traces | `profiling-stacktraces.otel-default` |
| Stack frames | `profiling-stackframes.otel-default` |
| Executables | `profiling-executables.otel-default` |
| Host metadata | `profiling-hosts.otel-default` |

Retention is managed with the [data stream lifecycle](/manage-data/lifecycle/data-stream.md) rather than {{ilm}}. The Universal Profiling pages about [{{ilm}}](universal-profiling-index-life-cycle-management.md) and the **Storage Explorer** don't apply to these data streams. Data that you collected earlier with Universal Profiling is not migrated.

## Troubleshoot [profiling-otel-troubleshoot]

**The agent is healthy but no profiles arrive.** The profiler can't load its eBPF programs when it lacks privileges or runs on an unsupported kernel, and {{fleet}} doesn't always report this as an error. Check the {{agent}} logs for messages such as:

```txt
failed to load eBPF tracer: failed to read kernel symbols: unable to read kallsyms addresses - check capabilities
```

Run the agent as root, or grant the `CAP_SYS_ADMIN` capability, and confirm that the host meets the [kernel requirements](#profiling-otel-requirements-hosts).

**The receiver reports that neither `debugfs` nor `tracefs` is mounted.** The profiler needs access to scheduler tracepoints. Mount `tracefs` on the Linux host:

```bash
sudo mount -t tracefs tracefs /sys/kernel/tracing
```

For a container deployment, expose that directory at `/sys/kernel/tracing` in the container. The Helm profiling preset configures this container mount for you.

**The receiver fails with `system analysis request was not handled` on a local kind cluster.** kind runs its nodes in containers, so the profiler runs in a nested PID namespace. With {{agent}} 9.6, enable PID namespace translation by adding the following receiver setting to your Helm values:

```yaml
config:
  receivers:
    profiling:
      pid_namespace_translation_mode: auto
```

**Agents cannot create profiling data streams.** {{agent}} logs show an error like this one:

```txt
action [indices:admin/auto_create] is unauthorized for API key id [...] of user [elastic/fleet-server] on indices [profiling-stacktraces.otel-default]
```

If the agent's API key lacks permission to create these data streams, ingestion fails even when the templates are installed. As a user with the `superuser` role, create the missing data streams before the agents start sending data. The event streams include the full stream and downsampled streams from `5pow01` through `5pow11`. Run only the requests for streams that do not already exist:

```console
PUT _data_stream/profiling-events-all.otel-default
PUT _data_stream/profiling-events-5pow01.otel-default
PUT _data_stream/profiling-events-5pow02.otel-default
PUT _data_stream/profiling-events-5pow03.otel-default
PUT _data_stream/profiling-events-5pow04.otel-default
PUT _data_stream/profiling-events-5pow05.otel-default
PUT _data_stream/profiling-events-5pow06.otel-default
PUT _data_stream/profiling-events-5pow07.otel-default
PUT _data_stream/profiling-events-5pow08.otel-default
PUT _data_stream/profiling-events-5pow09.otel-default
PUT _data_stream/profiling-events-5pow10.otel-default
PUT _data_stream/profiling-events-5pow11.otel-default
PUT _data_stream/profiling-stacktraces.otel-default
PUT _data_stream/profiling-stackframes.otel-default
PUT _data_stream/profiling-executables.otel-default
PUT _data_stream/profiling-hosts.otel-default
```

**{{kib}} reports that no profiling data was found.** Check that the schema selector is set to **OpenTelemetry** and widen the time range. Run the event count query in [Verify that profiles are flowing](#profiling-otel-verify). If the count is `0`, check the agent's health and logs in {{fleet}}. The `resources.has_data` field from `GET /_profiling/status` covers both profiling schemas, so `true` does not by itself confirm OpenTelemetry ingestion. In an OpenTelemetry-only deployment, `resource_management.enabled` and `resources.created` can both be `false`: those fields describe Universal Profiling resources.
