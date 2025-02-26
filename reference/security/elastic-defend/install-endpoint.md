---
navigation_title: "Install {{elastic-defend}}"
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/install-endpoint.html
---

# Install the {{elastic-defend}} integration [install-endpoint]


Like other Elastic integrations, {{elastic-defend}} is integrated into the {{agent}} using [{{fleet}}](/reference/ingestion-tools/fleet/index.md). Upon configuration, the integration allows the {{agent}} to monitor events on your host and send data to the {{security-app}}.

::::{admonition} Requirements
* {{fleet}} is required for {{elastic-defend}}.
* To configure the {{elastic-defend}} integration on the {{agent}}, you must have permission to use {{fleet}} in {{kib}}.
* You must have the **{{elastic-defend}} Policy Management : All** [privilege](/reference/security/elastic-defend/endpoint-management-req.md) to configure an integration policy, and the **Endpoint List** [privilege](/reference/security/elastic-defend/endpoint-management-req.md) to access the **Endpoints** page.

::::



## Before you begin [security-before-you-begin]

If you’re using macOS, some versions may require you to grant Full Disk Access to different kernels, system extensions, or files. Refer to [*{{elastic-defend}} requirements*](/reference/security/elastic-defend/elastic-endpoint-deploy-reqs.md) for more information.

::::{note}
{{elastic-defend}} does not support deployment within an {{agent}} DaemonSet in Kubernetes.
::::



## Add the {{elastic-defend}} integration [add-security-integration]

1. Find **Integrations** in the navigation menu or by using the [global search field](/get-started/the-stack.md#kibana-navigation-search).

    :::{image} ../../../images/security-endpoint-cloud-sec-integrations-page.png
    :alt: Search result for "{{elastic-defend}}" on the Integrations page.
    :class: screenshot
    :::

2. Search for and select **{{elastic-defend}}**, then select **Add {{elastic-defend}}**. The integration configuration page appears.

    ::::{note}
    If this is the first integration you’ve installed and the **Ready to add your first integration?** page appears instead, select **Add integration only (skip agent installation)** to proceed. You can [install {{agent}}](#enroll-agent) after setting up the {{elastic-defend}} integration.
    ::::


    :::{image} ../../../images/security-endpoint-cloud-security-configuration.png
    :alt: Add {{elastic-defend}} integration page
    :class: screenshot
    :::

3. Configure the {{elastic-defend}} integration with an **Integration name** and optional **Description**.
4. Select the type of environment you want to protect, either **Traditional Endpoints** or **Cloud Workloads**.
5. Select a configuration preset. Each preset comes with different default settings for {{agent}} — you can further customize these later by [configuring the {{elastic-defend}} integration policy](/reference/security/elastic-defend/configure-endpoint-integration-policy.md).

    |     |     |
    | --- | --- |
    | **Traditional Endpoint presets** | All traditional endpoint presets *except **Data Collection*** have these preventions enabled by default: malware, ransomware, memory threat, malicious behavior, and credential theft. Each preset collects the following events:<br><br>* **Data Collection:** All events; no preventions<br>* **Next-Generation Antivirus (NGAV):** Process events; all preventions<br>* **Essential EDR (Endpoint Detection & Response):** Process, Network, File events; all preventions<br>* **Complete EDR (Endpoint Detection & Response):** All events; all preventions<br> |
    | **Cloud Workloads presets** | Both cloud workload presets are intended for monitoring cloud-based Linux hosts. Therefore, [session data](/solutions/security/investigate/session-view.md) collection, which enriches process events, is enabled by default. They both have all preventions disabled by default, and collect process, network, and file events.<br><br>* **All events:** Includes data from automated sessions.<br>* **Interactive only:** Filters out data from non-interactive sessions by creating an [event filter](/solutions/security/manage-elastic-defend/event-filters.md).<br> |

6. Enter a name for the agent policy in **New agent policy name**. If other agent policies already exist, you can click the **Existing hosts** tab and select an existing policy instead. For more details on {{agent}} configuration settings, refer to [{{agent}} policies](/reference/ingestion-tools/fleet/agent-policy.md).
7. When you’re ready, click **Save and continue**.
8. To complete the integration, select **Add {{agent}} to your hosts** and continue to the next section to install the {{agent}} on your hosts.


## Configure and enroll the {{agent}} [enroll-security-agent]

To enable the {{elastic-defend}} integration, you must enroll agents in the relevant policy using {{fleet}}.

::::{important}
Before you add an {{agent}}, a {{fleet-server}} must be running. Refer to [Add a {{fleet-server}}](/reference/ingestion-tools/fleet/deployment-models.md).

{{elastic-defend}} cannot be integrated with an {{agent}} in standalone mode.

::::



### Important information about {{fleet-server}} [fleet-server-upgrade]

::::{note}
If you are running an {{stack}} version earlier than 7.13.0, you can skip this section.
::::


If you have upgraded to an {{stack}} version that includes {{fleet-server}} 7.13.0 or newer, you will need to redeploy your agents. Review the following scenarios to ensure you take the appropriate steps.

* If you redeploy the {{agent}} to the same machine through the {{fleet}} application after you upgrade, a new agent will appear.
* If you want to remove the {{agent}} entirely without transitioning to the {{fleet-server}}, then you will need to manually uninstall the {{agent}} on the machine. This will also uninstall the endpoint. Refer to [Uninstall Elastic Agent](/reference/ingestion-tools/fleet/uninstall-elastic-agent.md).
* In the rare event that the {{agent}} fails to uninstall, you might need to manually uninstall the endpoint. Refer to [Uninstall an endpoint](/reference/security/elastic-defend/uninstall-agent.md#uninstall-endpoint) at the end of this topic.


### Add the {{agent}} [enroll-agent]

1. If you’re in the process of installing an {{agent}} integration (such as {{elastic-defend}}), the **Add agent** UI opens automatically. Otherwise, find **{{fleet}}*** in the navigation menu or by using the [global search field](/get-started/the-stack.md#kibana-navigation-search), and select ***Agents** → **Add agent**.

    :::{image} ../../../images/security-endpoint-cloud-sec-add-agent.png
    :alt: Add agent flyout on the Fleet page.
    :class: screenshot
    :::

2. Select an agent policy for the {{agent}}. You can select an existing policy, or select **Create new agent policy** to create a new one. For more details on {{agent}} configuration settings, refer to [{{agent}} policies](/reference/ingestion-tools/fleet/agent-policy.md).

    The selected agent policy should include the integration you want to install on the hosts covered by the agent policy (in this example, {{elastic-defend}}).

    :::{image} ../../../images/security-endpoint-cloud-sec-add-agent-detail.png
    :alt: Add agent flyout with {{elastic-defend}} integration highlighted.
    :class: screenshot
    :::

3. Ensure that the **Enroll in {{fleet}}** option is selected. {{elastic-defend}} cannot be integrated with {{agent}} in standalone mode.
4. Select the appropriate platform or operating system for the host, then copy the provided commands.
5. On the host, open a command-line interface and navigate to the directory where you want to install {{agent}}. Paste and run the commands from {{fleet}} to download, extract, enroll, and start {{agent}}.
6. (Optional) Return to the **Add agent** flyout in {{fleet}}, and observe the **Confirm agent enrollment** and **Confirm incoming data** steps automatically checking the host connection. It may take a few minutes for data to arrive in {{es}}.
7. After you have enrolled the {{agent}} on your host, you can click **View enrolled agents** to access the list of agents enrolled in {{fleet}}. Otherwise, select **Close**.

    The host will now appear on the **Endpoints** page in the {{security-app}}. It may take another minute or two for endpoint data to appear in {{elastic-sec}}.

8. For macOS, continue with [these instructions](/reference/security/elastic-defend/deploy-elastic-endpoint.md) to grant {{elastic-endpoint}} the required permissions.
