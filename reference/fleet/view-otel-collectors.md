---
navigation_title: View OTel Collectors
description: View OpenTelemetry Collectors and their details in the Fleet Agents list.
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: fleet
  - id: elastic-agent
---

# View OTel Collectors in Fleet

After you add OpenTelemetry (OTel) Collectors in {{fleet}}, you can view them in the **Agents** list and inspect individual collectors for their health, configuration, and operational status.

## View OTel Collectors in the Agents list

The **Fleet** → **Agents** page displays all OTel Collectors alongside {{agents}}. The list shows key health and performance metrics from each collector, including status, CPU and memory usage (when internal telemetry is enabled), host name and tags, version, and last activity timestamp.

:::{note}
Unlike {{agents}}, OTel Collectors don't display an agent policy in the **Agents** list. OTel Collectors use managed policies that can't be modified and aren't displayed in the **Agent policies** tab.
:::

To view detailed information about a specific OTel Collector, click its host name in the list. For more information, refer to [View details about your OTel Collector](#view-details-about-your-otel-collector).

:::{tip}
To display only OTel Collectors in the list of agents:
* From the **Tags** filter, select one or more tags to filter the list. EDOT Collectors are automatically assigned the `elastic-otel-collector` tag. Upstream and community-contributed OTel Collectors are automatically assigned the `otel-contrib` tag.
* From the **Agent policies** filter, select the **OpAMP** option to display all OTel Collectors.
:::

## View details about your OTel Collector

To view detailed information about an OTel Collector, click its host name in the **Agents** list. The **Agent details** page displays the following information:

### Overview

The Overview section provides key information about the OTel Collector's current state and configuration:

| Field | Description |
|-------|-------------|
| **CPU** | Average CPU usage in the last 5 minutes. Available only if internal telemetry is enabled. |
| **Memory** | Average memory usage in the last 5 minutes. Available only if internal telemetry is enabled. |
| **Status** | Current health status of the OTel Collector (for example, `Healthy`, `Unhealthy`, or `Offline`). |
| **Last activity** | Timestamp of the most recent check-in. |
| **Last checkin message** | Status message from the last check-in (for example, `StatusOK`). |
| **Agent ID** | The UUID assigned to the OTel Collector instance. |
| **Agent policy** | Shows a dash (`-`) because OTel Collectors use managed policies. |
| **Agent version** | The version of the upstream and community-contributed OTel Collector or EDOT Collector. |
| **Host name** | The name of the host machine running the OTel Collector. |
| **Host ID** | Shows a dash (`-`) for OTel Collectors. |
| **Platform** | The operating system platform (for example, darwin, linux, windows). |
| **Tags** | Automatically assigned tags based on collector type (`elastic-otel-collector` for EDOT Collector, `otel-contrib` for upstream and community-contributed OTel Collectors). |
| **Collector capabilities** | The OpAMP capabilities reported by the collector: `ReportsAvailableComponents`, `ReportsEffectiveConfig`, `ReportsHealth`, and `ReportsStatus`. |

### Component health

The Component health section displays the operational status of the OTel Collector's pipeline components:

* Collector status: Shows the collector's overall health status
* Pipeline and extension sections: Separate expandable sections for each configured extension and pipeline

Within each section, click **Components** to view the health status of individual pipeline elements:

* Extensions: Service extension components
* Receiver: Input components collecting telemetry data
* Processor: Components transforming, filtering, or enriching data
* Exporter: Output components sending data to destinations

Each component displays a colored indicator showing its health status:

* Green indicator (Healthy): A healthy component operating normally
* Yellow indicator (Degraded): A degraded component with warnings
* Red indicator (Error): An unhealthy component with errors

Components with errors or warnings display the status message and error details.

### Effective configuration

To view the OTel Collector's running configuration, click **View Collector Configuration**. A flyout opens displaying the effective configuration currently applied to the collector. This shows the actual configuration the collector is using, which may differ from your source configuration if the collector merges multiple configuration files.

## Related pages

* [Monitor OpenTelemetry Collectors in Fleet](/reference/fleet/monitor-otel-collectors.md)
* [Troubleshoot OTel Collectors in Fleet](/troubleshoot/ingest/fleet/common-problems.md#opentelemetry-collectors-in-fleet)
