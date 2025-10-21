---
navigation_title: Manage integrations
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/integrations.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Manage {{agent}} integrations [integrations]

{{agent}} integrations provide a unified way to collect data from apps and services and to protect systems from security threats. 

Integrations are available for a wide array of services and platforms. To browse the full list of available integrations, go to the **Integrations** page in {{kib}}, or visit [Elastic Integrations](integration-docs://reference/index.md).

{{agent}} integrations based on the [Elastic Common Schema](ecs://reference/index.md) (ECS) come prepackaged with assets that support your observability needs:

* Data ingestion, storage, and transformation rules
* Configuration options
* Pre-built, custom dashboards and visualizations
* Documentation

{applies_to}`stack: preview 9.2.0` {{fleet}} also supports installing {{agent}} integration packages for collecting and visualizing OpenTelemetry data. For more information, refer to [Collect OpenTelemetry data with {{agent}} integrations](/reference/fleet/otel-integrations.md).

::::{note}
Some integrations may function differently across different spaces, and some might only work in the default space. For any space-related considerations, review the documentation for the specific integration.
::::

## Integration actions [integration-actions]

The following table shows the main actions you can perform in the **Integrations** app in {{kib}}. You can perform some of these actions from other places in {{kib}}, too.

| User action | Result |
| --- | --- |
| [Add an integration to an {{agent}} policy](/reference/fleet/add-integration-to-policy.md) | Configure an integration for a specific use case and add it to an {{agent}} policy. |
| [View integration policies](/reference/fleet/view-integration-policies.md) | View the integration policies created for a specific integration. |
| [Edit or delete an integration policy](/reference/fleet/edit-delete-integration-policy.md) | Change settings or delete the integration policy. |
| [Install and uninstall integration assets](/reference/fleet/install-uninstall-integration-assets.md) | Install, uninstall, and reinstall integration assets in {{kib}}. |
| [View integration assets](/reference/fleet/view-integration-assets.md) | View the {{kib}} assets installed for a specific integration. |
| [Upgrade an integration](/reference/fleet/upgrade-integration.md) | Upgrade an integration to the latest version. |

::::{note}
The **Integrations** app in {{kib}} needs access to the public {{package-registry}} to discover integrations. If your deployment has network restrictions, you can [deploy your own self-managed {{package-registry}}](/reference/fleet/air-gapped.md#air-gapped-diy-epr).
::::

:::{tip}
Once you've started using integrations to ingest data, you can customize how that data is managed over time. Refer to [Index lifecycle management](/reference/fleet/data-streams.md#data-streams-ilm) to learn more.
:::