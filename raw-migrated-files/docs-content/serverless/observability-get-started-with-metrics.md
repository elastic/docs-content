# Get started with system metrics [observability-get-started-with-metrics]

::::{admonition} Required role
:class: note

The **Admin** role or higher is required to onboard system metrics data. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


In this guide you’ll learn how to onboard system metrics data from a machine or server, then observe the data in {{obs-serverless}}.

To onboard system metrics data:

1. [Create a new {{obs-serverless}} project](../../../solutions/observability/get-started/create-an-observability-project.md), or open an existing one.
2. In your {{obs-serverless}} project, go to **Project Settings** → **Integrations**.
3. Type **System** in the search bar, then select the integration to see more details about it.
4. Click **Add System**.
5. Follow the in-product steps to install the System integration and deploy an {{agent}}. The sequence of steps varies depending on whether you have already installed an integration.

    * When configuring the System integration, make sure that **Collect metrics from System instances** is turned on.
    * Expand each configuration section to verify that the settings are correct for your host. For example, you may want to turn on **System core metrics** to get a complete view of your infrastructure.


Notice that you can also configure the integration to collect logs.

::::{admonition} What if {{agent}} is already running on my host?
:class: note

Do not try to deploy a second {{agent}} to the same system. You have a couple options:

* **Use the System integration to collect system logs and metrics.** To do this, uninstall the standalone agent you deployed previously, then follow the in-product steps to install the System integration and deploy an {{agent}}.
* **Configure your existing standalone agent to collect metrics.** To do this, edit the deployed {{agent}}'s YAML file and add metric inputs to the configuration manually. Manual configuration is a time-consuming process. To save time, you can follow the in-product steps that describe how to deploy a standalone {{agent}}, and use the generated configuration as source for the input configurations that you need to add to your standalone config file.

::::


After the agent is installed and successfully streaming metrics data, go to **Infrastructure** → **Infrastructure inventory** or **Hosts** to see a metrics-driven view of your infrastructure. To learn more, refer to [View infrastructure metrics by resource type](../../../solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md) or [Analyze and compare hosts](../../../solutions/observability/infra-and-hosts/analyze-compare-hosts.md).


## Next steps [observability-get-started-with-metrics-next-steps]

Now that you’ve added metrics and explored your data, learn how to onboard other types of data:

* [Get started with system logs](../../../solutions/observability/logs/get-started-with-system-logs.md)
* [Stream any log file](../../../solutions/observability/logs/stream-any-log-file.md)
* [Get started with traces and APM](../../../solutions/observability/apps/get-started-with-apm.md)
