---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/create-standalone-agent-policy.html
---

# Create a standalone Elastic Agent policy

To get started quickly, use {{kib}} to add integrations to an agent policy, then download the policy to use as a starting point for your standalone {{agent}} policy. This approach saves time, is less error prone, and populates the policy with a lot of details that are tedious to add manually. Also, adding integrations in {{kib}} loads required assets, such as index templates, and ingest pipelines, before you start your {{agent}}s.

::::{tip}
If you’re a {{fleet}} user and already have an agent policy you want to use in standalone mode, go to **{{fleet}} > Agents** and click **Add agent**. Follow the steps under **Run standalone** to download the policy file.
::::


You don’t need {{fleet}} to perform the following steps, but on self-managed clusters, API keys must be enabled in the {{es}} configuration (set `xpack.security.authc.api_key.enabled: true`).

## Create a standalone policy [create-standalone-policy]

1. From the main menu in {{kib}}, click **Add integrations**, and search for the {{agent}} integration you want to use. Read the description to make sure the integration works with {{agent}}.
2. Click the integration to see more details about it, then click **Add <Integration>**.

    :::{image} images/add-integration-standalone.png
    :alt: Add Nginx integration screen with agent policy selected
    :class: screenshot
    :::

    ::::{note}
    If you’re adding your first integration and no {{agent}}s are installed, {{kib}} may display a page that walks you through configuring the integration and installing {{agent}}. If you see this page, click **Install {{agent}}**, then click the **standalone mode** link. Follow the in-product instructions instead of the steps described here.
    ::::

3. Under **Configure integration**, enter a name and description for the integration.
4. Click the down arrow next to enabled streams and make sure the settings are correct for your host.
5. Under **Apply to agent policy**, select an existing policy, or click **Create agent policy** and create a new one.
6. When you’re done, save and continue.

    A popup window gives you the option to add {{agent}} to your hosts.

    :::{image} images/add-agent-to-hosts.png
    :alt: Popup window showing the option to add {{agent}} to your hosts
    :class: screenshot
    :::

7. (Optional) To add more integrations to the agent policy, click **Add {{agent}} later** and go back to the **Integrations** page. Repeat the previous steps for each integration.
8. When you’re done adding integrations, in the popup window, click **Add {{agent}} to your hosts** to open the **Add agent** flyout.
9. Click **Run standalone** and follow the in-product instructions to download {{agent}} (if you haven’t already).
10. Click **Download Policy** to download the policy file.

    :::{image} images/download-agent-policy.png
    :alt: Add data screen with option to download the default agent policy
    :class: screenshot
    :::


The downloaded policy already contains a default {{es}} address and port for your setup. You may need to change them if you use a proxy or load balancer. Modify the policy, as required, making sure that you provide credentials for connecting to {es}

If you need to add integrations to the policy *after* deploying it, you’ll need to run through these steps again and re-deploy the updated policy to the host where {{agent}} is running.

For detailed information about starting the agent, including the permissions needed for the {{es}} user, refer to [Install standalone {{agent}}s](/reference/ingestion-tools/fleet/install-standalone-elastic-agent.md).


## Upgrade standalone agent policies after upgrading an integration [update-standalone-policies]

Because standalone agents are not managed by {{fleet}}, they are unable to upgrade to new integration package versions automatically. When you upgrade an integration in {{kib}} (or it gets upgraded automatically), you’ll need to update the standalone policy to use new features and capabilities.

You’ll also need to update the standalone policy if you want to add new integrations.

To update your standalone policy, use the same steps you used to create and download the original policy file:

1. Follow the steps under [Create a standalone {{agent}} policy](#create-standalone-policy) to create and download a new policy, then compare the new policy file to the old one.
2. Either use the new policy and apply your customizations to it, or update your old policy to include changes, such as field changes, added by the upgrade.

::::{important}
Make sure you update the standalone agent policy in the directory where {{agent}} is running, not the directory where you downloaded the installation package. Refer to [Installation layout](/reference/ingestion-tools/fleet/installation-layout.md) for the location of installed {{agent}} files.
::::
