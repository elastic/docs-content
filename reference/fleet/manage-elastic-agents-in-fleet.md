---
navigation_title: Manage {{agents}} in {{fleet}}
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/manage-agents-in-fleet.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Centrally manage {{agents}} in {{fleet}} [manage-agents-in-fleet]

The {{fleet}} app in {{kib}} supports both {{agent}} infrastructure management and agent policy management. You can use {{fleet}} to:

- Manage {{agent}} binaries and specify settings installed on the host that determine whether the agent is enrolled in {{fleet}}, what version of the agent is running, and which agent policy is used.
- Manage agent policies that specify agent configuration settings, which integrations are running, whether agent monitoring is turned on, input settings, and more.

Advanced users who don’t want to use {{fleet}} for central management can use an external infrastructure management solution and [install {{agent}} in standalone mode](/reference/fleet/install-standalone-elastic-agent.md) instead.

::::{important}
{{fleet}} currently requires a {{kib}} user with `All` privileges on {{fleet}} and {{integrations}}. Since many Integrations assets are shared across spaces, users need the {{kib}} privileges in all spaces. Refer to [Required roles and privileges](/reference/fleet/fleet-roles-privileges.md) to learn how to create a user role with the required privileges to access {{fleet}} and {{integrations}}.
::::

To learn how to add {{agents}} to {{fleet}}, refer to [Install {{fleet}}-managed {{agents}}](/reference/fleet/install-fleet-managed-elastic-agent.md).

Find **{{fleet}}** in the {{kib}} navigation menu, or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). The following table describes the main management actions you can perform in {{fleet}}:

| Component | Management actions |
| --- | --- |
| [{{fleet}} settings](/reference/fleet/fleet-settings.md) | Configure global settings available to all {{agents}} managed by {{fleet}}, including {{fleet-server}} hosts and output settings. |
| [{{agents}}](/reference/fleet/manage-agents.md) | Enroll, unenroll, upgrade, add tags, and view {{agent}} status and logs. |
| [Policies](/reference/fleet/agent-policy.md) | Create and edit agent policies and add integrations to them. |
| [{{fleet}} enrollment tokens](/reference/fleet/fleet-enrollment-tokens.md) | Create and revoke enrollment tokens. |
| [Uninstall tokens](/solutions/security/configure-elastic-defend/prevent-elastic-agent-uninstallation.md) | ({{elastic-defend}} integration only) Access tokens to allow uninstalling {{agent}} from endpoints with Agent tamper protection enabled. |
| [Data streams](/reference/fleet/data-streams.md) | View data streams and navigate to dashboards to analyze your data. |

## Global {{fleet}} management

In {{fleet}} deployments where {{agents}} are installed in diverse locations and where data must be stored in local clusters, operators need a unified view of all agents and a central management interface for tasks like upgrades, policy organization, and metrics collection. {{fleet}} offers features to facilitate this deployment model:

- [Remote {{es}} output](/reference/fleet/remote-elasticsearch-output.md): Configure {{agents}} to send data to remote {{es}} clusters while still sending their check-in payloads to the management cluster. This allows {{fleet}} on the management cluster to maintain a global view of all agents while the ingested data is routed to the agents' respective local clusters.
- {applies_to}`stack: ga 9.1.0` [Automatic integrations synchronization](/reference/fleet/automatic-integrations-synchronization.md): Install an integration once in the management cluster and use {{fleet}} to synchronize and update the integration across all remote clusters. This enables you to initiate services like [OSquery](integration-docs://reference/osquery-intro.md) from the management cluster, and to collect and display responses from dispersed agents in {{fleet}} on the central management cluster.

:::{image} images/manage-agents-global-fleet.png
:alt: A diagram showing Elastic Agents connected to remote data clusters and to a Fleet management cluster
:::
