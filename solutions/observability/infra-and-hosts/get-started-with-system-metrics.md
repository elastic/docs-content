---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/logs-metrics-get-started.html
  - https://www.elastic.co/guide/en/serverless/current/observability-get-started-with-metrics.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: observability
  - id: cloud-serverless
  - id: edot-collector
---

# Get started with system metrics [logs-metrics-get-started]

In this guide you can learn how to onboard system metrics data from a machine or server using {{fleet}}-managed {{agent}}.

:::{tip}
To get started quickly without {{fleet}}, follow the steps described in the [quickstarts](/solutions/observability/get-started/quickstarts.md). You can also use the [Elastic Distribution of OpenTelemetry (EDOT) Collector](/solutions/observability/get-started/quickstart-monitor-hosts-with-opentelemetry.md) as an alternative to collect system metrics and logs.
:::

## Prerequisites [logs-metrics-prereqs]

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

To follow the steps in this guide, you need an {{stack}} deployment that includes:

* {{es}} for storing and searching data
* {{kib}} for visualizing and managing data
* Kibana user with `All` privileges on {{fleet}} and Integrations. Because many Integrations assets are shared across spaces, users need the Kibana privileges in all spaces.
* Integrations Server (included by default in every {{ech}} deployment)

To get started quickly, create an {{ech}} deployment and host it on AWS, GCP, or Azure. [Try it out for free](https://cloud.elastic.co/registration?page=docs&placement=docs-body).

:::

:::{tab-item} Serverless
:sync: serverless

The **Admin** role or higher is required to onboard system metrics data. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

:::

::::


## Onboard system metrics data [add-system-integration]

::::{tab-set}
:group: stack-serverless

:::{tab-item} Elastic Stack
:sync: stack

{{agent}} is a single, unified way to add monitoring for logs, metrics, and other types of data to a host. It can also protect hosts from security threats, query data from operating systems, forward data from remote services or hardware, and more. A single agent makes it easier and faster to deploy monitoring across your infrastructure. Each agent has a single policy you can update to add integrations for new data sources, security protections, and more.

In this step, add the System integration to monitor host logs and metrics.

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the query bar, search for **System** and select the integration to see more details about it.
3. Select **Add System**.
4. Configure the integration name and optionally add a description. Make sure that **Collect logs from System instances** and **Collect metrics from System instances** are turned on.
5. Expand each configuration section to verify that the settings are correct for your host. For example, if you're deploying {{agent}} on macOS hosts, you need to add a new path to the *System syslog logs* section by clicking **Add row** and specifying `/var/log/system.log`.

    :::{image} /solutions/images/observability-kibana-agent-add-log-path.png
    :alt: Configuration page for adding log paths to the {{agent}} System integration
    :screenshot:
    :::

6. Select **Save and continue**. This step takes a minute or two to complete. When it's done, the new agent policy contains a system integration policy for the configuration you specified.

    :::{image} /solutions/images/observability-kibana-system-policy.png
    :alt: Configuration page for adding the {{agent}} System integration
    :screenshot:
    :::

7. In the dialog, select **Add {{agent}} to your hosts** to open the **Add agent** flyout.

    ::::{tip}
    If you accidentally close the popup, go to **{{fleet}} > Agents**, then select **Add agent** to access the flyout.
    ::::

:::

:::{tab-item} Serverless
:sync: serverless

1. [Create a new {{obs-serverless}} project](/solutions/observability/get-started.md), or open an existing one.
2. In your {{obs-serverless}} project, go to **Project Settings** → **Integrations**.
3. Enter **System** in the search bar, then select the integration to see more details about it.
4. Select **Add System**.
5. Follow the in-product steps to install the System integration and deploy an {{agent}}. The sequence of steps varies depending on whether you have already installed an integration.

    * When configuring the System integration, make sure that **Collect metrics from System instances** is turned on.
    * Expand each configuration section to verify that the settings are correct for your host. For example, you might want to turn on **System core metrics** to get a complete view of your infrastructure.

## Install and run an {{agent}} on your machine [add-agent-to-fleet]

The **Add agent** flyout has two options: **Enroll in {{fleet}}** and **Run standalone**. The default is to enroll the agents in {{fleet}}, as this reduces the amount of work on the person managing the hosts by providing a centralized management tool in {{kib}}.

1. Skip the **Select enrollment token** step. The enrollment token you need is already selected.

    ::::{note}
    The enrollment token is specific to the {{agent}} policy that you created. When you run the command to enroll the agent in {{fleet}}, you pass in the enrollment token.
    ::::

2. Download, install, and enroll the {{agent}} on your host by selecting your host operating system and following the **Install {{agent}} on your host** step.

    :::{image} /solutions/images/observability-kibana-agent-flyout.png
    :alt: Add agent flyout in {{kib}}
    :screenshot:
    :::

    It takes about a minute for {{agent}} to enroll in {{fleet}}, download the configuration specified in the policy you created, and start collecting data.

Notice that you can also configure the integration to collect logs.

::::{note}
**What if {{agent}} is already running on the host?**

Don't try to deploy a second {{agent}} to the same system. You have a couple options:

* **Use the System integration to collect system logs and metrics.** To do this, uninstall the standalone agent you deployed previously, then follow the in-product steps to install the System integration and deploy an {{agent}}.
* **Configure your existing standalone agent to collect metrics.** To do this, edit the deployed {{agent}}'s YAML file and add metric inputs to the configuration manually. Manual configuration is a time-consuming process. To save time, you can follow the in-product steps that describe how to deploy a standalone {{agent}}, and use the generated configuration as source for the input configurations that you need to add to your standalone config file.

::::


:::

::::


After the agent is installed and successfully streaming metrics data, go to **Infrastructure** → **Infrastructure inventory** or **Hosts** to see a metrics-driven view of your infrastructure. To learn more, refer to [View infrastructure metrics by resource type](/solutions/observability/infra-and-hosts/view-infrastructure-metrics-by-resource-type.md) or [Analyze and compare hosts](/solutions/observability/infra-and-hosts/analyze-compare-hosts.md).


## Next steps [observability-get-started-with-metrics-next-steps]

Now that you have added metrics and explored your data, learn how to onboard other types of data:

* [Get started with system logs](/solutions/observability/logs/get-started-with-system-logs.md)
* [Stream any log file](/solutions/observability/logs/stream-any-log-file.md)
* [Get started with traces and APM](/solutions/observability/apm/get-started.md)