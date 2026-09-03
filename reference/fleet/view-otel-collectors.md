---
navigation_title: View OTel Collectors
description: View OpenTelemetry Collectors in the Fleet Agents list and inspect an individual collector's health, pipeline, and configuration.
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: fleet
  - id: elastic-agent
---

# View OTel Collectors in Fleet

After you add OpenTelemetry (OTel) Collectors in {{fleet}}, you can view them in the **Agents** list and open an individual collector to inspect its health, pipelines, metadata, and running configuration.

## View OTel Collectors in the Agents list

The **Fleet** → **Agents** page lists OTel Collectors alongside {{agents}}. For each collector, the list shows its status, host name, CPU and memory usage (when internal telemetry is available), last activity timestamp, and version.

Two columns behave differently for collectors than for {{agents}}:

* **Agent policy** shows a dash (`-`), because collectors use managed policies.
* **Version** shows the version the collector reports for itself (the same value as **Service version** on the details page), not an {{stack}} version. An upstream OTel Collector reports its own release number, such as `0.144.0`.

### Filter the list to show only collectors

You can narrow the Agents list to only display OTel Collectors in two ways:

* From the **Tags** filter, select the tag that matches your collectors.
* From the **Agent policies** filter, select **OpAMP**. {{fleet}} creates this managed policy automatically when you add your first collector, and enrolls every collector into it. The policy is hidden from the **Agent policies** tab, but you can still use it to filter the list.

Each collector is automatically tagged with its service name. This is the **Service name** you set when you added the collector, which defaults to a slug of the collector group display name, such as `otel-collector-group`. {{agent}} running in OTel mode reports `elastic-otel-collector`. Any labels you enter in the **Tags** field are added as extra tags.

### Available actions

Collectors support a smaller set of actions than {{agents}}. From the **Actions** menu on the collector's details page, or the actions menu in its row in the **Agents** list, you can select:

* **View agent JSON**: View the collector's stored details as JSON.
* {applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` **Remove collector**: Remove the collector from {{fleet}}. Refer to [Remove an OTel Collector from Fleet](/reference/fleet/remove-otel-collector.md).

## Open the collector details

To open a collector, click its host name in the **Agents** list.

::::{applies-switch}

:::{applies-item} { stack: preview 9.5+, serverless: preview }

The collector's details page shows a **Collector (OpAMP)** badge next to the host name.

The **Collector details** tab contains three sections:

* A [visualization of the collector's pipelines](#visualize-the-collector-pipeline).
* A panel with **Health**, **Info**, and **Config** tabs, covering [health](#check-collector-health), [metadata](#review-collector-metadata), and the [effective configuration](#view-the-effective-configuration).
* An [**Error patterns**](#investigate-error-patterns) table.

:::

:::{applies-item} { stack: preview =9.4 }

The **Agent details** tab has two columns: an **Overview** panel with the collector's [metadata](#review-collector-metadata), and a [**Component health**](#check-collector-health) panel.

:::

::::

A collector also has a **Logs** tab, but it doesn't return data. To review a collector's own logs, make sure [internal telemetry](/reference/fleet/add-otel-collector-internal-telemetry.md) is enabled and [confirm the data is flowing](/reference/fleet/add-otel-collector-internal-telemetry.md#verify-internal-telemetry-is-flowing) in {{kib}}.

{applies_to}`stack: preview =9.4` The **Diagnostics** and **Settings** tabs don't apply to a collector, and are removed in 9.5.

## Visualize the collector pipeline

```{applies_to}
stack: preview 9.5+
serverless: preview
```

The **Collector details** tab shows the collector's pipelines as a graph, so you can see how telemetry flows from receivers through to exporters without reading the YAML.

The graph is built from the collector's effective configuration, so it renders even when the collector is offline.

### Choose which pipelines to display

Use the **Pipeline** selector to choose which pipelines to display:

* **All pipelines** displays every pipeline in the configuration.
* When a signal type has more than one pipeline, an option for that signal appears, labeled with its pipeline count, such as **All metrics (2 pipelines)**.
* Individual pipelines are listed last, by their configuration ID, such as `logs`, `metrics`, or `metrics/host`.

If the configuration defines no pipelines, the graph is replaced by a **No pipelines configured** message.

### Read the graph

Each node is a pipeline component, labeled with its type and its configuration ID, and color-coded by type. The graph draws receivers, processors, exporters, and connectors. Extensions aren't drawn, because they don't participate in a pipeline.

The layout depends on your selection:

* When a single pipeline is displayed, components are laid out left to right in the order data flows through them.
* When several pipelines are displayed, each becomes a labeled container, with its components nested inside. A connector that exports from one pipeline and receives into another is drawn with a dashed line between the two containers.

When health data is available, each node shows a status indicator using the same states described in [Check collector health](#check-collector-health). A pipeline container aggregates the health of the components inside it.

Use the zoom controls to zoom in, zoom out, or fit the graph to the panel. The graph refits automatically when you change the pipeline selection.

Click any node to open the [component detail panel](#inspect-a-pipeline-component). Click it again, or click an empty area of the canvas, to close the panel.

## Check collector health

A collector reports its own health and the health of each component in its pipelines. Where {{fleet}} displays this depends on your version.

::::{applies-switch}

:::{applies-item} { stack: preview 9.5+, serverless: preview }

The **Health** tab of the collector details panel summarizes the collector's overall state:

| Field | Description |
|-------|-------------|
| **Health status** | Overall health reported by the collector. |
| **Start time** | When the collector process started. |
| **Uptime** | How long the collector has been running, shown relative to its start time. |
| **Last health update** | When the collector last reported health data. |
| **Last error** | The most recent error the collector reported. This row appears only when an error has been reported. |

If the collector is offline, inactive, unenrolled, or uninstalled, the tab shows a **Collector is not active** message instead. If the collector is running but hasn't reported health data, the tab shows **No health data available**. Health data is only available while a collector is running.

Under **Component health**, health is broken down per pipeline. A badge next to the heading rolls up the totals across all pipelines, such as `6 healthy` or `4 healthy, 2 unhealthy`, followed by the time of the last update.

Expand a pipeline to see its components, grouped by type: **Receivers**, **Connectors**, **Processors**, and **Exporters**. Each pipeline shows its own component count and health badge. Components reporting an error display the error message beneath them.

Click any component to open the [component detail panel](#inspect-a-pipeline-component).

Each component shows a colored indicator: green for **Healthy**, amber for **Unhealthy**, and grey for **Unknown**. A pipeline indicator is green when every component in it is healthy, red when none are, and amber when some are. **Unhealthy** covers both degraded and warning states.

:::

:::{applies-item} { stack: preview =9.4 }

The **Component health** panel on the **Agent details** tab shows **Collector status** at the top, followed by a section for each configured pipeline and one for extensions.

Within each section, click **Components** to expand the list of individual components, each labeled with its type and configuration ID, such as `Receiver: otlp` or `Exporter: elasticsearch/otel`.

Each component and section displays a colored indicator:

| Indicator | Meaning |
|-----------|---------|
| Green | The component is healthy. |
| Yellow | The component reported a degraded or warning status. |
| Red | The component reported any other unhealthy status. |

Components that aren't healthy display the status the collector reported, such as `StatusPermanentError`, along with any error details.

:::

::::

## Inspect a pipeline component

```{applies_to}
stack: preview 9.5+
serverless: preview
```

Clicking a component in the pipeline graph or in the **Component health** list opens a detail panel titled with the component's type and ID, such as `Receiver: otlp`. Its current health status appears in the panel header.

Depending on the selected component, the panel has up to three tabs.

### Health

This tab shows the component's reported health data.

| Field | Description |
|-------|-------------|
| **Status** | The component's health state: **Healthy**, **Unhealthy**, or **Unknown**. |
| **Reported status** | The status string the collector reported, such as `StatusOK`. |
| **Last updated** | When this component last reported health data. |
| **Last error** | The most recent error for this component. Appears only when an error has been reported. |

### Metrics

This tab is available for receivers, processors, and exporters. It isn't available for connectors, or when you select a whole pipeline.

Metrics come from the collector's own telemetry, so this tab shows **No metrics data available** unless [internal telemetry](/reference/fleet/add-otel-collector-internal-telemetry.md) is enabled on the collector.

Select a time range of **5m**, **15m**, or **1h**. Depending on the component type, up to three groups of charts are shown:

* **Throughput (events/s)**: Rate of telemetry the component accepted or sent
* **Errors (events/s)**: Rate of failed items
* **Queue**: Current queue size and capacity for exporters that queue data

### Config

This tab displays the component's own configuration as YAML, which you can copy. For receivers, processors, exporters, and connectors, a **View component documentation** link opens the upstream OpenTelemetry documentation for that component type.

When you select a whole pipeline, this tab shows the pipeline's wiring instead: its receivers, processors, and exporters.

## Review collector metadata

To view a collector's metadata:

* {applies_to}`serverless: preview` {applies_to}`stack: preview 9.5+` Open the **Info** tab of the collector details panel.
* {applies_to}`stack: preview =9.4` Refer to the **Overview** panel on the **Agent details** tab.

::::{applies-switch}

:::{applies-item} { stack: preview 9.5+, serverless: preview }

| Field | Description |
|-------|-------------|
| **Name** | The per-instance display name reported by the collector. Defaults to the value of **Collector display name** from the **Add collector** flow, which is typically the host name. If no display name is available, shows the collector's agent ID. |
| **Agent ID** | The UUID assigned to this collector instance. Matches the `instance_uid` value in the collector's OpAMP configuration. |
| **Agent status** | Current status of the collector, such as `Healthy`, `Unhealthy`, or `Offline`. |
| **Last activity** | Time of the most recent check-in. |
| **Last checkin message** | Status message from the last check-in, such as `StatusOK`. |
| **Service name** | The collector's `service.name` attribute. Also used as its automatic tag. |
| **Service version** | The version the collector reports for itself. For an upstream collector, this is the collector's own release version. For an {{agent}} run as a collector, it's the {{agent}} version. |
| **Host name** | Name of the host running the collector. |
| **Host ID** | Host identifier. Usually shows a dash (`-`) for collectors. |
| **Host architecture** | CPU architecture of the host, such as `arm64`. |
| **OS** | Operating system type, such as `darwin`, `linux`, or `windows`. |
| **Platform** | Operating system description, such as `macOS 26.6.2`. |
| **Collector group** | The collector group this collector instance belongs to. |
| **Pipelines** | Number of pipelines defined in the collector's configuration. |
| **Enrolled** | When the collector first enrolled in {{fleet}}. |
| **Tags** | Tags assigned to the collector. Refer to [Filter the list to show only collectors](#filter-the-list-to-show-only-collectors) for how these are derived. |
| **Capabilities** | The OpAMP capabilities the collector reports. |

:::

:::{applies-item} { stack: preview =9.4 }

| Field | Description |
|-------|-------------|
| **Status** | Current status of the collector, such as `Healthy`, `Unhealthy`, or `Offline`. |
| **Last activity** | Time of the most recent check-in. |
| **Last checkin message** | Status message from the last check-in, such as `StatusOK`. |
| **Agent ID** | The UUID assigned to this collector instance. Matches the `instance_uid` value in the collector's OpAMP configuration. |
| **Agent version** | The version the collector reports for itself. For an upstream collector, this is the collector's own release version. For an {{agent}} run as a collector, it's the {{agent}} version. |
| **CPU** | Average CPU usage over the last 5 minutes. Requires internal telemetry. |
| **Memory** | Average memory usage over the last 5 minutes. Requires internal telemetry. |
| **Agent policy** | Shows a dash (`-`), because collectors use managed policies. |
| **Host name** | Name of the host running the collector. |
| **Host ID** | Host identifier. Usually shows a dash (`-`) for collectors. |
| **Platform** | The operating system type, such as `darwin`, `linux`, or `windows`. |
| **Tags** | Tags assigned to the collector. Refer to [Filter the list to show only collectors](#filter-the-list-to-show-only-collectors) for how these are derived. |
| **Collector capabilities** | The OpAMP capabilities the collector reports. |

:::

::::

## View the effective configuration

The effective configuration is the configuration the collector is actually running. It can differ from the configuration file you wrote, because the collector resolves environment variables and merges multiple configuration sources.

::::{applies-switch}

:::{applies-item} { stack: preview 9.5+, serverless: preview }

Open the **Config** tab of the collector details panel. The configuration is displayed as YAML, with a badge showing its line count. You can copy it, expand it to full screen, or click **Download** to save it as a YAML file.

:::

:::{applies-item} { stack: preview =9.4 }

On the **Agent details** tab, click **View Collector Configuration**. A flyout opens showing the effective configuration as YAML, which you can copy or save using **Download Configuration**.

:::

::::

## Investigate error patterns

```{applies_to}
stack: preview 9.5+
serverless: preview
```

The **Error patterns** table at the bottom of the **Collector details** tab groups similar error and warning messages from the collector's own logs, so you can spot recurring problems without reading through every log line.

The table stays empty unless [internal telemetry](/reference/fleet/add-otel-collector-internal-telemetry.md) is enabled. When no matching messages exist, the table reports that no error patterns were found in the selected time range. Logs recorded before the collector is added in {{fleet}} aren't included.

Use the controls to change what's shown:

* Select a time range of **Last 5 minutes**, **Last 1 hour** (the default), **Last 1 day**, or **Last 1 week**.
* Switch between **Errors** and **Warnings**. **Errors** covers the `error` and `fatal` log levels, and **Warnings** covers `warn` and `warning`.
* Sort by **Most frequent** or **Most recent**.

A summary next to the heading reports the number of patterns for the selected level, followed by the combined number of matching logs across both levels for the time range.

At most 20 patterns are returned for each level. For each pattern, the table shows its **Level**, the detected **Pattern**, its **Count**, **First seen** and **Last seen** timestamps, an **Example message**, and the **Component** that produced it. Click the icon in the last column to explore the matching logs in **Discover**.

## Related pages

* [Monitor OpenTelemetry Collectors in Fleet](/reference/fleet/monitor-otel-collectors.md)
* [Add an OTel Collector in Fleet](/reference/fleet/add-otel-collector.md)
* [Remove an OTel Collector from Fleet](/reference/fleet/remove-otel-collector.md)
* [Add internal telemetry to an OTel Collector monitored by {{fleet}}](/reference/fleet/add-otel-collector-internal-telemetry.md)
* [Troubleshoot OTel Collectors in Fleet](/troubleshoot/ingest/fleet/common-problems.md#opentelemetry-collectors-in-fleet)
