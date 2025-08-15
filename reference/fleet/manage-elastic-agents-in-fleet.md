---
navigation_title: Manage {{agents}} in {{fleet}}
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/manage-agents-in-fleet.html
products:
  - id: fleet
  - id: elastic-agent
---

# Centrally manage {{agents}} in {{fleet}} [manage-agents-in-fleet]

The {{fleet}} app in {{kib}} supports both {{agent}} infrastructure management and agent policy management. You can use {{fleet}} to:

- Manage {{agent}} binaries and specify settings installed on the host that determine whether the {{agent}} is enrolled in {{fleet}}, what version of the agent is running, and which agent policy is used.
- Manage agent policies that specify agent configuration settings, which integrations are running, whether agent monitoring is turned on, input settings, and so on.

Advanced users who don’t want to use {{fleet}} for central management can use an external infrastructure management solution and [install {{agent}} in standalone mode](/reference/fleet/install-standalone-elastic-agent.md) instead.

::::{important}
{{fleet}} currently requires a {{kib}} user with `All` privileges on {{fleet}} and {{integrations}}. Since many Integrations assets are shared across spaces, users need the {{kib}} privileges in all spaces. Refer to [Required roles and privileges](/reference/fleet/fleet-roles-privileges.md) to learn how to create a user role with the required privileges to access {{fleet}} and {{integrations}}.
::::

To learn how to add {{agents}} to {{fleet}}, refer to [Install {{fleet}}-managed {{agents}}](/reference/fleet/install-fleet-managed-elastic-agent.md).

To use {{fleet}} go to **Management** → **{{fleet}}** in {{kib}}. The following table describes the main management actions you can perform in {{fleet}}:

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

- [Remote {{es}} output](/reference/fleet/remote-elasticsearch-output.md): {{agents}} can be configured to send data to a remote {{es}} cluster while their check-in payloads are sent to the management cluster. This allows {{fleet}} in the management cluster to maintain a global view of all agents while the ingested data is routed to the agents' respective local clusters.
- [Automatic integrations synchronization](/reference/fleet/automatic-integrations-synchronization.md) {applies_to}`stack: ga 9.1.0`: This feature allows users to install an integration once in the management cluster and to use {{fleet}} to reliably synchronize and update the integration across all remote clusters. With synchronized integrations, services like [OSquery](integration-docs://reference/osquery-intro.md) can be initiated from the management cluster, and responses from dispersed agents can be collected and displayed globally within {{fleet}}'s central management cluster.

:::{image} images/manage-agents-global-fleet.png
:alt: A diagram showing Elastic Agents connected to remote data clusters and to a Fleet management cluster
:::