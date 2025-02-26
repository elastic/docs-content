---
navigation_title: "Manage {{agent}}s in {{fleet}}"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/manage-agents-in-fleet.html
---

# Centrally manage {{agent}}s in {{fleet}} [manage-agents-in-fleet]


::::{admonition}
The {{fleet}} app in {{kib}} supports both {{agent}} infrastructure management and agent policy management. You can use {{fleet}} to:

* Manage {{agent}} binaries and specify settings installed on the host that determine whether the {{agent}} is enrolled in {{fleet}}, what version of the agent is running, and which agent policy is used.
* Manage agent policies that specify agent configuration settings, which integrations are running, whether agent monitoring is turned on, input settings, and so on.

Advanced users who don’t want to use {{fleet}} for central management can use an external infrastructure management solution and [install {{agent}} in standalone mode](/reference/ingestion-tools/fleet/install-standalone-elastic-agent.md) instead.

::::


::::{important}
{{fleet}} currently requires a {{kib}} user with `All` privileges on {{fleet}} and {{integrations}}. Since many Integrations assets are shared across spaces, users need the {{kib}} privileges in all spaces. Refer to [Required roles and privileges](/reference/ingestion-tools/fleet/fleet-roles-privileges.md) to learn how to create a user role with the required privileges to access {{fleet}} and {{integrations}}.

::::


To learn how to add {{agent}}s to {{fleet}}, refer to [Install {{fleet}}-managed {{agent}}s](/reference/ingestion-tools/fleet/install-fleet-managed-elastic-agent.md).

To use {{fleet}} go to **Management > {{fleet}}** in {{kib}}. The following table describes the main management actions you can perform in {{fleet}}:

| Component | Management actions |
| --- | --- |
| [{{fleet}} settings](/reference/ingestion-tools/fleet/fleet-settings.md) | Configure global settings available to all {{agent}}s managed by {{fleet}},including {{fleet-server}} hosts and output settings. |
| [{{agent}}s](/reference/ingestion-tools/fleet/manage-agents.md) | Enroll, unenroll, upgrade, add tags, and view {{agent}} status and logs. |
| [Policies](/reference/ingestion-tools/fleet/agent-policy.md) | Create and edit agent policies and add integrations to them. |
| [{{fleet}} enrollment tokens](/reference/ingestion-tools/fleet/fleet-enrollment-tokens.md) | Create and revoke enrollment tokens. |
| [Uninstall tokens](/reference/security/elastic-defend/agent-tamper-protection.md) | ({{elastic-defend}} integration only) Access tokens to allow uninstalling {{agent}} from endpoints with Agent tamper protection enabled. |
| [Data streams](/reference/ingestion-tools/fleet/data-streams.md) | View data streams and navigate to dashboards to analyze your data. |







