---
navigation_title: Remove an OTel Collector
description: Remove an OpenTelemetry Collector from the Fleet Agents list.
type: how-to
applies_to:
  stack: preview 9.5+
  serverless: preview
products:
  - id: fleet
  - id: elastic-agent
---

# Remove an OTel Collector from Fleet

Remove an OpenTelemetry (OTel) Collector from the {{fleet}} **Agents** list when you no longer want {{fleet}} to track it.

## Before you begin

You'll need:

* The **Agents** privilege set to `All`. Refer to [{{fleet}} privileges](/reference/fleet/fleet-roles-privileges.md).
* An active collector in the **Agents** list. The remove action is unavailable for inactive collectors.

## Remove a collector

1. In {{kib}}, enter **Fleet** in the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Fleet / Agents**.
2. To remove a single collector, select **Remove collector** from its **Actions** menu, then confirm.

   To remove several collectors at once, select them in the **Agents** list, then choose **Remove N collectors** from the bulk actions menu, where *N* is the number of selected collectors, and confirm.

Removing a collector removes it from the **Agents** list only. It doesn't stop the collector process, and its enrollment credentials stay valid, so a collector that's still running can reconnect and reappear in the list.

To stop a collector from reporting to {{fleet}}, remove the `opamp` extension from its configuration and restart it.

## Related pages

* [View OTel Collectors in Fleet](/reference/fleet/view-otel-collectors.md)
* [Add an OTel Collector in Fleet](/reference/fleet/add-otel-collector.md)
* [Monitor OpenTelemetry Collectors in Fleet](/reference/fleet/monitor-otel-collectors.md)
