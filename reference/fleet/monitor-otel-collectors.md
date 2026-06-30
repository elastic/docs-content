---
navigation_title: Monitor OTel Collectors
description: Centrally monitor EDOT and OpenTelemetry Collectors in Fleet using OpAMP.
type: overview
applies_to:
  stack: preview 9.4+
  serverless: preview
products:
  - id: fleet
  - id: elastic-agent
---

# Monitor OpenTelemetry Collectors in Fleet

Use {{fleet}} to centrally monitor {{edot}} (EDOT) Collectors and third-party OpenTelemetry (OTel) Collectors running in your infrastructure. {{fleet}} provides visibility into the health, configuration, and telemetry of any OTel Collector with the OpAMP extension, so you can troubleshoot issues, plan capacity, and monitor operations from a single interface.

For monitoring OTel Collectors, {{fleet}} uses the Open Agent Management Protocol (OpAMP). Collectors report their status and configuration to {{fleet-server}}, which acts as an OpAMP server. {{fleet}} doesn't deploy OTel Collectors — you install and run them separately, then configure them with the OpAMP extension to report to {{fleet-server}}.

Supported collectors:

* OpenTelemetry Collector (upstream and community-contributed distributions): version 0.103.0 or later
* EDOT Collector: version 9.2 or later

:::{note}
Unlike {{agents}}, OTel Collectors don't display an agent policy in the **Agents** list. They use managed policies that can't be modified and aren't displayed in the **Agent policies** tab.
:::

Learn more:

* [Add an OTel Collector in Fleet](/reference/fleet/add-otel-collector.md)
* [View OTel Collectors in Fleet](/reference/fleet/view-otel-collectors.md)
* [Add internal telemetry to an OTel Collector monitored by {{fleet}}](/reference/fleet/add-otel-collector-internal-telemetry.md)
