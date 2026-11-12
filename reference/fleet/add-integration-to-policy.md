---
navigation_title: Add an integration to an {{agent}} policy
description: Add an integration to one or more Elastic Agent policies in Fleet so enrolled agents start collecting data, or deploy it as an Elastic managed integration.
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/add-integration-to-policy.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
type: how-to
---

# Add an integration to an {{agent}} policy [add-integration-to-policy]

Add an integration to one or more [{{agent}} policies](/reference/fleet/agent-policy.md) so that the {{agent}}s enrolled in those policies start collecting the integration's data. When you add an integration, {{fleet}} creates an integration policy that you can share across several {{agent}} policies, which reduces the number of integration policies that you need to manage.

## Before you begin [add-integration-to-policy-prereqs]

To add an integration to an {{agent}} policy, your role needs the `All` privilege for **Fleet** and **Integrations**.

{applies_to}`serverless: ga` {applies_to}`stack: ga 9.1+` If you [customize sub-feature privileges for {{fleet}}](/reference/fleet/fleet-roles-privileges.md#fleet-roles-and-privileges-sub-features), the role needs the `All` privilege for **Agent policies**.

## Add an integration [add-integration-to-policy-steps]

1. In {{kib}}, find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for and select an integration. You can select a category to narrow your search.

    {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` If the integration is part of a collection, select the collection tile, then select the integration in the flyout.

3. Open the **Add <integration>** page:

    * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` Selecting the integration opens the **Add <integration>** page. To learn what data the integration collects and how to configure it, select **View documentation** in the **New to this integration?** panel, if the page shows it. Some integrations open their [**Overview** page](/reference/fleet/open-integration-details.md) instead.
    * {applies_to}`stack: ga 9.0-9.5` Selecting the integration opens its **Overview** page. Select **Add <integration>**.

4. If the **Ready to add your first integration?** page opens, select **Add integration only (skip agent installation)**. You can add an {{agent}} after you add the integration.
5. In the **Configure integration** section, configure the settings specific to the integration.

    If the integration can run as an [{{managed-integration}}](/reference/managed-integrations/index.md), also select a deployment type, either in a separate **Deployment** section or in the **Deployment options** field. Select **Agent-based** to run the integration on {{agent}}s that you manage. The Elastic managed option doesn't use an {{agent}} policy, so if you select it, skip the next step:

    * {applies_to}`serverless: ga` {applies_to}`stack: ga 9.5+` **Elastic Managed Integration**
    * {applies_to}`stack: preview 9.0-9.4` **Agentless**

6. In the **Where to add this integration?** section, select where to add the integration:

    * To create a new {{agent}} policy, select the **New hosts** tab. Enter a name for the new agent policy, and select whether to collect system logs and metrics. Collecting system logs and metrics adds the System integration to the new agent policy.
    * To use existing {{agent}} policies, select the **Existing hosts** tab. In the **Agent policies** field, select one or more agent policies.

      Selecting more than one agent policy, known as **reusable integration policies**, is available only for certain subscription levels. For more information, refer to [Elastic subscriptions](https://www.elastic.co/subscriptions).

    ::::{include} _snippets/version-specific-policy-integration-warning.md
    ::::

7. Select **Save and continue**.

    A notification confirms that the integration was added. If the agent policies have no {{agent}}s enrolled yet, a dialog prompts you to add one. To install an agent now, select **Add {{agent}} to your hosts** and follow the instructions in the **Add agent** flyout. To skip this step, select **Add {{agent}} later**. You can add an agent later from the integration's **Integration policies** tab by selecting **Add agent** in the integration policy's row.

Saving installs the integration if it isn't installed yet. For agent-based deployments, {{fleet}} adds the new integration policy to the {{agent}} policies that you selected and distributes it to all {{agent}}s enrolled in those policies.

If you're monitoring many hosts that run the same service, you don't need to repeat these steps for each host. Refer to [](/reference/fleet/scale-integration-policies.md).

To update the integration policy's settings or the {{agent}} policies that it's added to, refer to [](/reference/fleet/edit-delete-integration-policy.md).

## Related pages [add-integration-to-policy-related-pages]

* [](/reference/fleet/install-fleet-managed-elastic-agent.md)
* [](/reference/fleet/view-integration-policies.md)
* [](/reference/fleet/upgrade-integration.md)
* [Elastic integrations reference](integration-docs://reference/index.md)
