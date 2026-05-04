---
navigation_title: Version-specific agent policies
description: Fleet generates version-specific policies to ensure agents get a compatible configuration when integrations require a minimum agent version.
applies_to:
  stack: ga 9.4+
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Version-specific agent policies [version-specific-agent-policies]

{{agent}} integrations can require a minimum {{agent}} version, or use newer {{agent}} capabilities only when they're available.

Integrations can specify two kinds of agent version requirements:

* **Package-level requirement**: The integration requires a minimum {{agent}} version. Agents below that version receive a version-specific policy that doesn't include a configuration for this integration.
* **Input template-level requirement**: Individual configuration blocks are conditionally included based on the agent's version. Agents that meet the requirement receive the newer configuration. Agents on earlier versions receive a fallback configuration.

For specific examples of how integration authors declare version requirements, refer to [Agent version conditions](integrations://extend/agent-version-conditions.md).

When a policy contains an integration that declares an agent version requirement, {{fleet}} automatically generates version-specific policies to ensure all agents receive compatible configurations. This prevents configuration errors and allows you to use newer integration features while supporting agents on earlier versions.

{{fleet}} groups these policies under the primary policy in the UI so you continue to manage one logical policy: edit the primary policy to change the configuration that its version-specific policies inherit. You can't create, edit, delete, or reassign version-specific policies directly.

## How version-specific policies work [how-version-specific-policies-work]

1. When you add or update the integration, {{fleet}} compiles a set of version-specific policies for common {{agent}} minor versions (for example, `9.4`, `9.3`, and `8.19`) and stores them alongside the primary agent policy. Each version-specific policy is identified internally as `<primary_policy_id>#<minor_version>`.
2. About once a minute, a scheduled {{fleet}} task identifies agents that need a version-specific policy. This includes newly enrolled agents, recently upgraded agents, and agents whose current version-specific policy is out of date. {{fleet}} then reassigns each agent to the matching version-specific policy. You can configure the interval in the {{kib}} configuration using the `xpack.fleet.versionSpecificPolicyAssignment.taskInterval` setting (the default is `1m`).
3. Each agent receives a rendered configuration valid for its version. {{fleet}} omits any inputs that the agent's version doesn't support. The rest of the policy still applies.

## Version-specific policies in the {{fleet}} UI [version-specific-policies-fleet-ui]

### When you add an integration to a policy [version-specific-policies-add-integration]

When you add or edit an integration that declares a minimum agent version requirement, the **Add integration** form checks the requirement against the agents enrolled in the target agent policy.

If some or all agents enrolled in the policy don't meet the integration's requirement, a warning indicates that these agents aren't compatible with the integration.

You can still add the integration to the policy. If you later upgrade your agents or enroll new agents that meet the minimum version requirement, they receive the integration configuration automatically.

The same warning appears when you upgrade an integration to a version with a stricter requirement, so you can decide whether to upgrade the integration now or upgrade your agents first.

For detailed steps, refer to [Add an integration to an agent policy](/reference/fleet/add-integration-to-policy.md) and [Upgrade an integration](/reference/fleet/upgrade-integration.md).

### When you enroll an agent [version-specific-policies-enroll-agent]

In the **Add agent** flyout, when you select a policy that has an integration with a minimum required {{agent}} version, the flyout shows the recommended agent version and warns you to install an agent at or above that version.

The agent still enrolls even if its version is below the minimum required, but it skips any integration whose minimum version requirement it doesn't meet. A warning badge appears next to the agent on the **Agents** list.

For details on agent enrollment, refer to [Install {{fleet}}-managed {{agents}}](/reference/fleet/install-fleet-managed-elastic-agent.md).

### On the Agents and Agent details pages [version-specific-policies-agent-list]

On the **Agents** and **Agent details** pages, you can identify agents enrolled in a version-specific policy by the branch icon preceding the name of their agent policy. Agents whose version is below the minimum required by the integrations in their primary policy are marked with a warning badge next to the policy revision.

The agent count on the primary policy's details page includes all agents on its version-specific policies. Select the count to open the **Agents** list filtered to show every agent on the primary policy and on each of its version-specific policies.

:::{note}
Reassignments to and from version-specific policies are performed internally by {{fleet}} and are hidden from the **Agent activity** page.
:::

For more information about the **Agents** list and **Agent details** views, refer to [Monitor {{agents}}](/reference/fleet/monitor-elastic-agent.md).

## View an agent's rendered configuration [view-agent-rendered-configuration]

The configuration that {{fleet}} delivers to an agent on a version-specific policy reflects what that agent's version supports, so older agents skip inputs they can't run. To verify what an agent runs, [view the configuration delivered to the agent](/reference/fleet/monitor-elastic-agent.md#view-agent-configuration) using the **View agent policy** action.
