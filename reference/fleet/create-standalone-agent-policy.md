---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/create-standalone-agent-policy.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Create a standalone Elastic Agent policy

To get started quickly, use {{kib}} to add integrations to an agent policy, then download the policy to use as a starting point for your standalone {{agent}} policy. This approach saves time, is less error prone, and populates the policy with a lot of details that are tedious to add manually. Also, adding integrations in {{kib}} loads required assets, such as index templates, and ingest pipelines, before you start your {{agent}}s.

::::{tip}
If you’re a {{fleet}} user and already have an agent policy you want to use in standalone mode, go to **{{fleet}} → Agents** and select **Add agent**. Follow the steps under **Run standalone** to download the policy file.
::::


You don’t need {{fleet}} to perform the following steps, but on self-managed clusters, API keys must be enabled in the {{es}} configuration (set `xpack.security.authc.api_key.enabled: true`).

## Create a standalone policy [create-standalone-policy]

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for and select the {{agent}} integration you want to use.

    {applies_to}`serverless: ga` {applies_to}`stack: ga 9.6+` If the integration is part of a collection, select the collection tile, then select the integration in the flyout.

3. If the integration's **Overview** page opens, select **Add <integration>**.
4. If the **Ready to add your first integration?** page opens, select **Add integration only (skip agent installation)**. You add {{agent}} after you save the integration.
5. Under **Configure integration**, enter a name and description for the integration.
6. Select the down arrow next to enabled streams and make sure the settings are correct for your host.
7. In the **Where to add this integration?** section, select where to add the integration:

    * To use an existing {{agent}} policy, select the **Existing hosts** tab. In the **Agent policies** field, select the policy.
    * To create a new {{agent}} policy, select the **New hosts** tab and enter a name for the new policy.

8. When you’re done, select **Save and continue**.

    A popup window gives you the option to add {{agent}} to your hosts.

    :::{image} images/add-agent-to-hosts.png
    :alt: Popup window showing the option to add {{agent}} to your hosts
    :screenshot:
    :::

9. (Optional) To add more integrations to the agent policy, select **Add {{agent}} later** and go back to the **Integrations** page. Repeat the previous steps for each integration.
10. When you’re done adding integrations, in the popup window, select **Add {{agent}} to your hosts** to open the **Add agent** flyout.
11. Select **Run standalone** and follow the in-product instructions to download {{agent}} (if you haven’t already).
12. Select **Download Policy** to download the policy file.

    :::{image} images/download-agent-policy.png
    :alt: Add data screen with option to download the default agent policy
    :screenshot:
    :::


The downloaded policy already contains a default {{es}} address and port for your setup. You may need to change them if you use a proxy or load balancer. Modify the policy, as required, making sure that you provide credentials for connecting to {{es}}

If you need to add integrations to the policy *after* deploying it, you’ll need to run through these steps again and re-deploy the updated policy to the host where {{agent}} is running.

For detailed information about starting the agent, including the permissions needed for the {{es}} user, refer to [Install standalone {{agent}}s](/reference/fleet/install-standalone-elastic-agent.md).


## Upgrade standalone agent policies after upgrading an integration [update-standalone-policies]

Because standalone agents are not managed by {{fleet}}, they are unable to upgrade to new integration package versions automatically. When you upgrade an integration in {{kib}} (or it gets upgraded automatically), you’ll need to update the standalone policy to use new features and capabilities.

You’ll also need to update the standalone policy if you want to add new integrations.

To update your standalone policy, use the same steps you used to create and download the original policy file:

1. Follow the steps under [Create a standalone {{agent}} policy](#create-standalone-policy) to create and download a new policy, then compare the new policy file to the old one.
2. Either use the new policy and apply your customizations to it, or update your old policy to include changes, such as field changes, added by the upgrade.

::::{important}
Make sure you update the standalone agent policy in the directory where {{agent}} is running, not the directory where you downloaded the installation package. Refer to [Installation layout](/reference/fleet/installation-layout.md) for the location of installed {{agent}} files.
::::
