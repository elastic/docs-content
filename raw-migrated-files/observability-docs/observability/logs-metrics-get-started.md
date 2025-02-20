# Get started with system metrics [logs-metrics-get-started]

In this guide you’ll learn how to onboard system metrics data from a machine or server, then observe the data in Elastic Observability. This guide describes how to use a {{fleet}}-managed {{agent}}. To get started quickly with a standalone agent that does not require {{fleet}}, follow the steps described in the [quickstart](../../../solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md).


## Prerequisites [logs-metrics-prereqs]

To follow the steps in this guide, you need an {{stack}} deployment that includes:

* {{es}} for storing and searching data
* {{kib}} for visualizing and managing data
* Kibana user with `All` privileges on {{fleet}} and Integrations. Since many Integrations assets are shared across spaces, users need the Kibana privileges in all spaces.
* Integrations Server (included by default in every {{ess}} deployment)

To get started quickly, spin up a deployment of our hosted {{ess}}. The {{ess}} is available on AWS, GCP, and Azure. [Try it out for free](https://cloud.elastic.co/registration?page=docs&placement=docs-body).


## Step 1: Add the {{agent}} System integration [add-system-integration]

{{agent}} is a single, unified way to add monitoring for logs, metrics, and other types of data to a host. It can also protect hosts from security threats, query data from operating systems, forward data from remote services or hardware, and more. A single agent makes it easier and faster to deploy monitoring across your infrastructure. Each agent has a single policy you can update to add integrations for new data sources, security protections, and more.

In this step, add the System integration to monitor host logs and metrics.

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. In the query bar, search for **System** and select the integration to see more details about it.
3. Click **Add System**.
4. Configure the integration name and optionally add a description. Make sure that **Collect logs from System instances** and **Collect metrics from System instances** are turned on.
5. Expand each configuration section to verify that the settings are correct for your host. For example, if you’re  deploying {{agent}} on macOS hosts, you need to add a new path to the *System syslog logs* section by clicking **Add row** and specifying `/var/log/system.log`.

    :::{image} ../../../images/observability-kibana-agent-add-log-path.png
    :alt: Configuration page for adding log paths to the {{agent}} System integration
    :class: screenshot
    :::

6. Click **Save and continue**. This step takes a minute or two to complete. When it’s done, you’ll have an agent policy that contains a system integration policy for the configuration you just specified.

    :::{image} ../../../images/observability-kibana-system-policy.png
    :alt: Configuration page for adding the {{agent}} System integration
    :class: screenshot
    :::

7. In the popup, click **Add {{agent}} to your hosts** to open the **Add agent** flyout.

    ::::{tip}
    If you accidentally close the popup, go to **{{fleet}} > Agents**, then click **Add agent** to access the flyout.
    ::::



## Step 2: Install and run an {{agent}} on your machine [add-agent-to-fleet]

The **Add agent** flyout has two options: **Enroll in {{fleet}}** and **Run standalone**. The default is to enroll the agents in {{fleet}}, as this reduces the amount of work on the person managing the hosts by providing a centralized management tool in {{kib}}.

1. Skip the **Select enrollment token** step. The enrollment token you need is already selected.

    ::::{note}
    The enrollment token is specific to the {{agent}} policy that you just created. When you run the command to enroll the agent in {{fleet}}, you will pass in the enrollment token.
    ::::

2. Download, install, and enroll the {{agent}} on your host by selecting your host operating system and following the **Install {{agent}} on your host** step.

    :::{image} ../../../images/observability-kibana-agent-flyout.png
    :alt: Add agent flyout in {{kib}}
    :class: screenshot
    :::

    It takes about a minute for {{agent}} to enroll in {{fleet}}, download the configuration specified in the policy you just created, and start collecting data.



## Step 3: Monitor host logs and metrics [view-data]

1. Verify that data is flowing. Wait until agent enrollment is confirmed and incoming data is received, then click **View assets** to access dashboards related to the System integration.

    :::{image} ../../../images/observability-kibana-agent-confirm-data.png
    :alt: Agent confirm data
    :class: screenshot
    :::

2. Choose a dashboard that is related to the operating system of your monitored system. Dashboards are available for Microsoft Windows systems and Unix-like systems (for example, Linux and macOS).

    :::{image} ../../../images/observability-kibana-agent-system-integration-visualizations.png
    :alt: Agent list of visualizations
    :class: screenshot
    :::

3. Open the **[Metrics System] Host overview** dashboard to view performance metrics from your host system.

    :::{image} ../../../images/observability-host-metrics2.png
    :alt: The Host Overview dashboard in {{kib}} with various metrics from your monitored system
    :class: screenshot
    :::


You can hover over any visualization to adjust its settings, or click the **Edit** button to make changes to the dashboard. To learn more, refer to [Dashboard and visualizations](../../../explore-analyze/dashboards.md).


## Step 4: Monitor other sources [add-other-integrations]

Next, add additional integrations to the policy used by your agent.

1. Go back to **Integrations**.
2. In the query bar, search for the source you want to monitor (for example, nginx) and select the integration to see more details about it.
3. Click **Add <Integration>**.
4. Configure the integration name and optionally add a description.
5. Expand each configuration section to verify that the settings are correct for your host.
6. Under **Where to add this integration**, select **Existing hosts**, then select the agent policy you created earlier. That way, you can deploy the change to the agent that’s already running.
7. When you’re done, click **Save and continue**, then **Save and deploy changes**.
8. To see the updated policy, click the agent policy link.

    The newly added integration should appear on the **Integrations** tab in your agent policy.

    :::{image} ../../../images/observability-kibana-fleet-policies-default-with-nginx.png
    :alt: {{fleet}} showing default agent policy with nginx-1 data source
    :class: screenshot
    :::

    Any {{agent}}s assigned to this policy will begin collecting data for the newly configured integrations.

9. To view the data, find **{{fleet}}** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
10. Click the **Data streams** tab.
11. In the **Actions** column, navigate to the dashboards corresponding to the data stream.


## What’s next? [_whats_next_2]

* Monitor the status and response times of applications and services in real time using the {{uptime-app}}. You can monitor the availability of network endpoints via HTTP, TCP, ICMP or Browser monitors. Get started in [Synthetic monitoring](../../../solutions/observability/apps/synthetic-monitoring.md).
* Now that data is streaming into the {{stack}}, take your investigation to a deeper level! Use [Elastic {{observability}}](https://www.elastic.co/observability) to unify your logs, infrastructure metrics, uptime, and application performance data.
* Want to protect your endpoints from security threats? Try [{{elastic-sec}}](https://www.elastic.co/security). Adding endpoint protection is just another integration that you add to the agent policy!
* Are your eyes bleary from staring at a wall of screens? [Create alerts](../../../solutions/observability/incident-management/alerting.md) and find out about problems while sipping your favorite beverage poolside.
* Want Elastic to do the heavy lifting? Use {{ml}} to [detect anomalies](../../../solutions/observability/logs/inspect-log-anomalies.md).
* Got everything working like you want it? Roll out your agent policies to other hosts by deploying {{agent}}s across your infrastructure!
