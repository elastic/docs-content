---
navigation_title: Remove agent elevated privileges
applies_to:
  stack: ga 9.3.0+
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Remove elevated privileges from {{agents}} [remove-elevated-privileges]

Elevated privileges (root on Linux/macOS, administrator on Windows) give agents unrestricted access to system resources. If you want to improve security by limiting this access, you can remove the agents' root or administrator privileges centrally using the {{fleet}} UI or the {{fleet}} API.

:::{important}
Restoring elevated privileges to {{agents}} through the {{fleet}} UI or API is not currently supported. To grant an agent root or administrator privileges again, you need to either run the `elastic-agent privileged` command directly on the host or reinstall the agent without the `--unprivileged` flag. Refer to [Changing an {{agent}}'s privilege mode](/reference/fleet/elastic-agent-unprivileged.md#unprivileged-change-mode) for more details.
:::

:::{note}
Running without root privileges is not supported for {{agents}} installed using RPM or DEB packages.
:::

## Requirements [remove-elevated-privileges-requirements]

To be eligible for elevated privilege removal, {{agents}} must meet the following requirements:

* The agent must be running {{agent}} version 9.3.0 or later.
* The agent must not be a {{fleet-server}} agent.
* The agent must not be assigned to an agent policy that contains integrations requiring elevated privileges.

## Remove elevated privileges using the {{fleet}} UI [remove-elevated-privileges-ui]

To remove elevated privileges from one or more {{agents}} using the {{fleet}} UI:

1. In {{kib}}, find **Fleet** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

2. Select one or more agents for which you want to remove the elevated privileges.

3. Select **Actions** > **Security and removal** > **Remove root access for N agents** where N is the number of agents you've selected. A flyout opens.

4. Review the information in the flyout:

   * A warning is displayed if any of the selected agents do not meet the requirements for privilege removal. To view a list of these agents, click **View hosts**.
   * When you proceed, elevated privileges are removed only from the agents that meet all [requirements](#remove-elevated-privileges-requirements). Ineligible agents remain unchanged and continue running with elevated privileges.

5. (Optional) To run the agent as a pre-existing user or as part of a pre-existing group, enter these details:

      - Username
      - User group
      - User password

      If the user details are not specified, {{agent}} uses the default unprivileged user (`elastic-agent-user`) or creates it if it doesn't exist.

      ::::{note}
      For agents running on Windows, the password is required when specifying a custom user account.
      ::::

6. To confirm, select **Remove privilege for N agents** where N is the number of agents eligible for privilege removal.

The eligible agents are switched to unprivileged mode. You can monitor the progress on the **Agents** tab. After the operation completes, the agents run as unprivileged users and their privilege mode is updated in the agent details.

:::{note}
You can also initiate the privilege removal for a single agent on the agent's **Agent details** page. Select **Actions** > **Security and removal** > **Remove root privilege**, then follow steps 4-6.
:::

## Remove elevated privileges using the {{fleet}} API [remove-elevated-privileges-api]

You can also remove elevated privileges using the {{fleet}} API. This is useful for automation or when managing a large number of agents.

:::{note}
You can only use the {{fleet}} API to remove elevated privileges. Restoring elevated privileges through the API is not currently supported.
:::

### Single agent [remove-elevated-privileges-api-single]

To remove elevated privileges from a single agent, use the following API endpoint:

```bash
POST /api/fleet/agent/{agent_id}/privilege_level_change
```

Replace the path parameter `{agent_id}` with the ID of the agent.

For detailed API documentation, including request and response examples, refer to:

- [Change agent privilege level (Kibana Serverless API)](https://www.elastic.co/docs/api/doc/serverless/operation/operation-post-fleet-agents-agentid-privilege-level-change)
- [Change agent privilege level (Kibana API)](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-fleet-agents-agentid-privilege-level-change)

### Multiple agents [remove-elevated-privileges-api-bulk]

To remove elevated privileges from multiple agents at once, use the bulk API endpoint:

```bash
POST /api/fleet/agents/bulk_privilege_level_change
```

Include the agent IDs in the request body. For example:

```yaml
{
  "agents": ["agent-id-1", "agent-id-2", "agent-id-3"]
}
```

For detailed API documentation, including request and response examples, refer to:

- [Bulk change agent privilege level (Kibana Serverless API)](https://www.elastic.co/docs/api/doc/serverless/operation/operation-post-fleet-agents-bulk-privilege-level-change)
- [Bulk change agent privilege level (Kibana API)](https://www.elastic.co/docs/api/doc/kibana/operation/operation-post-fleet-agents-bulk-privilege-level-change)

## What happens when you remove elevated privileges [remove-elevated-privileges-behavior]

When you remove elevated privileges from an {{agent}}:

1. **User creation**: If a pre-existing user is not specified, a dedicated unprivileged user (`elastic-agent-user`) is created on the host (unless it already exists).

2. **Service ownership change**: The {{agent}} service switches to run as the created unprivileged user (`elastic-agent-user`) or a custom pre-existing user (if specified).

3. **File permissions adjustment**: The file permissions are adjusted to allow the unprivileged user to operate the agent.

4. **Data collection continues**: The agent continues to collect data, but it can only access resources that the `elastic-agent-user` or the specified pre-existing user has permission to read.

5. **Integration behavior**: Some integrations or data streams that require root or administrator access may start reporting errors or stop collecting certain data. For more details, refer to [Agent and dashboard behaviors in unprivileged mode](/reference/fleet/elastic-agent-unprivileged.md#unprivileged-command-behaviors).

## Verify the privilege level change [remove-elevated-privileges-verify]

To verify that root or administrator privileges have been removed from an agent:

1. In {{fleet}}, open the **Agents** tab.

2. Select an agent. The **Agent details** page opens.

3. Check the **Privilege mode** field. If the agent is in unprivileged mode, the field shows **Running as non-root**.

You can also view privilege status across all agents enrolled in a policy:

1. In {{fleet}}, open the **Agent policies** tab.

2. Click the agent policy to view its details.

3. Hover over the agent count to see the number of privileged and unprivileged agents enrolled in the policy.

## Troubleshooting [remove-elevated-privileges-troubleshoot]

After removing an agent's elevated privileges, some data sources may become inaccessible. To resolve this:

1. Check the agent logs for permission errors.

2. Grant the `elastic-agent-user` user or `elastic-agent` group read access to the necessary files or directories.

3. Alternatively, add the `elastic-agent-user` to relevant system groups that have the required permissions. Be cautious when granting additional permissions as this might reduce the security benefits of unprivileged mode.

For detailed guidance on resolving specific data collection issues, refer to [Agent and dashboard behaviors in unprivileged mode](/reference/fleet/elastic-agent-unprivileged.md#unprivileged-command-behaviors).
