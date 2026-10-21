---
navigation_title: Restart agents
description: Remotely restart Fleet-managed Elastic Agents from Kibana or the Fleet API, individually or in bulk, and track the restart progress in the agent activity log.
type: how-to
applies_to:
  serverless: preview
  stack: preview 9.6+
products:
  - id: fleet
  - id: elastic-agent
---

# Restart {{fleet}}-managed {{agent}}s [restart-elastic-agent]

Restart the {{agent}} process on one or more hosts directly from {{fleet}}, without logging in to each host. A restart can resolve common problems, for example when an agent stops sending data.

You can also restart agents programmatically, using the `POST /api/fleet/agents/{agentId}/restart` endpoint for a single agent or the `POST /api/fleet/agents/bulk_restart` endpoint for multiple agents. For the endpoint specifications, refer to the [Kibana API docs]({{kib-apis}}). For {{serverless-full}} projects, use the [Kibana Serverless API docs]({{kib-serverless-apis}}).

To restart the {{agent}} service locally on the host instead, refer to [Start and stop {{agent}}s on edge hosts](/reference/fleet/start-stop-elastic-agent.md).

## Before you begin [restart-elastic-agent-before-you-begin]

* You need `All` access for **Agents** in {{fleet}}. Refer to [{{fleet}} roles and privileges](/reference/fleet/fleet-roles-privileges.md).
* The agents must be on version 9.6.0 or later. For agents on earlier versions, the restart action is unavailable.
* The agents must be enrolled in {{fleet}}. You can't restart unenrolled or inactive agents.
* You can't restart agents that are enrolled in a [hosted agent policy](/reference/fleet/agent-policy.md#agent-policy-types), because these agents are managed by an external orchestration solution, such as {{ecloud}} or Kubernetes. To restart them, use your orchestration solution.

## Restart a single agent [restart-elastic-agent-single]

To restart the {{agent}} running on a specific host:

1. In {{kib}}, find **Fleet** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Agents**.
2. From the **Actions** menu next to the agent, select **Restart agent**. The action is also available in the **Actions** menu on the agent details page.
3. In the confirmation window, click **Restart agent**.

{{fleet}} sends the restart action to the agent, and the {{agent}} process on the host restarts. To verify the result, [track the restart progress](#restart-elastic-agent-track).

## Restart multiple agents [restart-elastic-agent-bulk]

To restart a group of agents in a single action:

1. In {{kib}}, find **Fleet** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md), then select **Agents**.
2. Select the agents you want to restart.
3. Select **Actions** → **Restart _x_ agents**.
4. In the confirmation window, click **Restart agents**.

{{fleet}} restarts all eligible agents in your selection. Agents that can't be restarted, for example because they're on a version earlier than 9.6.0, are excluded from the action and receive individual error results. To verify the results, [track the restart progress](#restart-elastic-agent-track).

## Track the restart progress [restart-elastic-agent-track]

To follow the progress of the restart, click **Agent activity** on the **Agents** tab. For more information, refer to [View agent activity](/reference/fleet/monitor-elastic-agent.md#view-agent-activity). The activity log shows the restart action, when it completed, and any agents that couldn't be restarted. If any agents failed to restart, select **Show errors** to view the error message for each agent.

If an agent is offline when you issue the restart, it receives the action the next time it checks in with {{fleet}}.

## Related pages [restart-elastic-agent-related]

* [{{agent}}s](/reference/fleet/manage-agents.md)
* [Start and stop {{agent}}s on edge hosts](/reference/fleet/start-stop-elastic-agent.md)
* [{{agent}} health status](/reference/fleet/agent-health-status.md)
* [{{fleet}} roles and privileges](/reference/fleet/fleet-roles-privileges.md)
