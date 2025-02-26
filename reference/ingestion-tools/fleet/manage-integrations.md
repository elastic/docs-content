---
navigation_title: "Manage integrations"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/integrations.html
---

# Manage {{agent}} integrations [integrations]


::::{admonition}
Integrations are available for a wide array of popular services and platforms. To see the full list of available integrations, go to the **Integrations** page in {{kib}}, or visit [Elastic Integrations](integration-docs://docs/reference/index.md).

{{agent}} integrations provide a simple, unified way to collect data from popular apps and services, and protect systems from security threats.

Each integration comes prepackaged with assets that support all of your observability needs:

* Data ingestion, storage, and transformation rules
* Configuration options
* Pre-built, custom dashboards and visualizations
* Documentation

::::


::::{note}
Please be aware that some integrations may function differently across different spaces. Also, some might only work in the default space. We recommend reviewing the specific integration documentation for any space-related considerations.

::::


The following table shows the main actions you can perform in the **Integrations** app in {{kib}}. You can perform some of these actions from other places in {{kib}}, too.

| User action | Result |
| --- | --- |
| [Add an integration to an {{agent}} policy](/reference/ingestion-tools/fleet/add-integration-to-policy.md) | Configure an integration for a specific use case and add it to an {{agent}} policy. |
| [View integration policies](/reference/ingestion-tools/fleet/view-integration-policies.md) | View the integration policies created for a specific integration. |
| [Edit or delete an integration policy](/reference/ingestion-tools/fleet/edit-delete-integration-policy.md) | Change settings or delete the integration policy. |
| [Install and uninstall integration assets](/reference/ingestion-tools/fleet/install-uninstall-integration-assets.md) | Install, uninstall, and reinstall integration assets in {{kib}}. |
| [View integration assets](/reference/ingestion-tools/fleet/view-integration-assets.md) | View the {{kib}} assets installed for a specific integration. |
| [Upgrade an integration](/reference/ingestion-tools/fleet/upgrade-integration.md) | Upgrade an integration to the latest version. |

::::{note}
The **Integrations** app in {{kib}} needs access to the public {{package-registry}} to discover integrations. If your deployment has network restrictions, you can [deploy your own self-managed {{package-registry}}](/reference/ingestion-tools/fleet/air-gapped.md#air-gapped-diy-epr).

::::













