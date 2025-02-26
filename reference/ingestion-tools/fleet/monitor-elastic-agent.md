---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/monitor-elastic-agent.html
---

# Monitor Elastic Agents [monitor-elastic-agent]

{{fleet}} provides built-in capabilities for monitoring your fleet of {{agent}}s. In {{fleet}}, you can:

* [View agent status overview](#view-agent-status)
* [View details for an agent](#view-agent-details)
* [View agent activity](#view-agent-activity)
* [View agent logs](#view-agent-logs)
* [Collect {{agent}} diagnostics](#collect-agent-diagnostics)
* [View the {{agent}} metrics dashboard](#view-agent-metrics)
* [Change {{agent}} monitoring settings](#change-agent-monitoring)
* [Send {{agent}} monitoring data to a remote {{es}} cluster](#external-elasticsearch-monitoring)
* [Enable alerts and ML jobs based on {{fleet}} and {{agent}} status](#fleet-alerting)

Agent monitoring is turned on by default in the agent policy unless you turn it off. Want to turn off agent monitoring to stop collecting logs and metrics? See [Change {{agent}} monitoring settings](#change-agent-monitoring).

Want to receive an alert when your {{agent}} health status changes? Refer to [Enable alerts and ML jobs based on {{fleet}} and {{agent}} status](#fleet-alerting) and our [alerting example](#fleet-alerting-example).

For more detail about how agents communicate their status to {{fleet}}, refer to [{{agent}} health status](/reference/ingestion-tools/fleet/agent-health-status.md).


## View agent status overview [view-agent-status]

To view the overall status of your {{fleet}}-managed agents, in {{kib}}, go to **Management → {{fleet}} → Agents**.

:::{image} images/kibana-fleet-agents.png
:alt: Agents tab showing status of each {agent}
:class: screenshot
:::

::::{important}
The **Agents** tab in **{{fleet}}** displays a maximum of 10,000 agents, shown on 500 pages with 20 rows per page. If you have more than 10,000 agents, we recommend using the filtering and sorting options described in this section to narrow the table to fewer than 10,000 rows.
::::


{{agent}}s can have the following statuses:

|     |     |
| --- | --- |
| **Healthy** | {{agent}}s are enrolled and checked in. There are no agent policy updates or automatic agent binary updates in progress, but the agent binary may still be out of date. {{agent}}s continuously check in to the {{fleet-server}} for required updates. |
| **Unhealthy** | {{agent}}s have errors or are running in a degraded state. An agent will be reported as `unhealthy` as a result of a configuration problem on the host system. For example, an {{agent}} may not have the correct permissions required to run an integration that has been added to the {{agent}} policy. In this case, you may need to investigate and address the situation. |
| **Updating** | {{agent}}s are updating the agent policy, updating the binary, or enrolling or unenrolling from {{fleet}}. |
| **Offline** | {{agent}}s have stayed in an unhealthy status for a period of time. Offline agent’s API keys remain valid. You can still see these {{agent}}s in the {{fleet}} UI and investigate them for further diagnosis if required. |
| **Inactive** | {{agent}}s have been offline for longer than the time set in your [inactivity timeout](/reference/ingestion-tools/fleet/set-inactivity-timeout.md). These {{agent}}s are valid, but have been removed from the main {{fleet}} UI. |
| **Unenrolled** | {{agent}}s have been manually unenrolled and their API keys have been removed from the system. You can [unenroll](/reference/ingestion-tools/fleet/unenroll-elastic-agent.md) an offline {{agent}} using {{agent}} actions if you determine it’s offline and no longer valid.<br>These agents need to re-enroll in {{fleet}} to be operational again. |

The following diagram shows the flow of {{agent}} statuses:

:::{image} images/agent-status-diagram.png
:alt: Diagram showing the flow of Fleet Agent statuses
:::

To filter the list of agents by status, click the **Status** dropdown and select one or more statuses.

:::{image} images/agent-status-filter.png
:alt: Agent Status dropdown with multiple statuses selected
:class: screenshot
:::

For advanced filtering, use the search bar to create structured queries using [{{kib}} Query Language](elasticsearch://docs/reference/query-languages/kql.md). For example, enter `local_metadata.os.family : "darwin"` to see only agents running on macOS.

You can also sort the list of agents by host, last activity time, or version, by clicking on the table headings for those fields.

To perform a bulk action on more than 10,000 agents, you can select the **Select everything on all pages** button.


## View details for an agent [view-agent-details]

In {{fleet}}, you can access the detailed status of an individual agent and the integrations that are associated with it through the agent policy.

1. In {{fleet}}, open the **Agents** tab.
2. In the **Host** column, click the agent’s name.

On the **Agent details** tab, the **Overview** pane shows details about the agent and its performance, including its memory and CPU usage, last activity time, and last checkin message. To access metrics visualizations, you can also [View the {{agent}} metrics dashboard](#view-agent-metrics).

:::{image} images/agent-detail-overview.png
:alt: Agent details overview pane with various metrics
:::

The **Integrations** pane shows the status of the integrations that have been added to the agent policy. Expand any integration to view its health status. Any errors or warnings are displayed as alerts.

:::{image} images/agent-detail-integrations-health.png
:alt: Agent details integrations pane with health status
:::

To gather more detail about a particular error or warning, from the **Actions** menu select **View agent JSON**. The JSON contains all of the raw agent data tracked by Fleet.

::::{note}
Currently, the **Integrations** pane shows the health status only for agent inputs. Health status is not yet available for agent outputs.
::::



## View agent activity [view-agent-activity]

You can view a chronological list of all operations performed by your {{agent}}s.

On the **Agents** tab, click **Agent activity**. All agent operations are shown, beginning from the most recent, including any in progress operations.

:::{image} images/agent-activity.png
:alt: Agent activity panel
:class: screenshot
:::


## View agent logs [view-agent-logs]

When {{fleet}} reports an agent status like `Offline` or `Unhealthy`, you might want to view the agent logs to diagnose potential causes. If agent monitoring is configured to collect logs (the default), you can view agent logs in {{fleet}}.

1. In {{fleet}}, open the **Agents** tab.
2. In the **Host** column, click the agent’s name.
3. On the **Agent details** tab, verify that **Monitor logs** is enabled. If it’s not, refer to [Change {{agent}} monitoring settings](#change-agent-monitoring).
4. Click the **Logs** tab.

    :::{image} images/view-agent-logs.png
    :alt: View agent logs under agent details
    :class: screenshot
    :::


On the **Logs** tab you can filter, search, and explore the agent logs:

* Use the search bar to create structured queries using [{{kib}} Query Language](elasticsearch://docs/reference/query-languages/kql.md).
* Choose one or more datasets to show logs for specific programs, such as {{filebeat}} or {{fleet-server}}.

    :::{image} images/kibana-fleet-datasets.png
    :alt: {{fleet}} showing datasets for logging
    :class: screenshot
    :::

* Change the log level to filter the view by log levels. Want to see debugging logs? Refer to [Change the logging level](#change-logging-level).
* Change the time range to view historical logs.
* Click **Open in Logs** to tail agent log files in real time. For more information about logging, refer to [Tail log files](/solutions/observability/logs/logs-stream.md).


## Change the logging level [change-logging-level]

The logging level for monitored agents is set to `info` by default. You can change the agent logging level, for example, to turn on debug logging remotely:

1. After navigating to the **Logs** tab as described in [View agent logs](#view-agent-logs), scroll down to find the **Agent logging level** setting.

    :::{image} images/agent-set-logging-level.png
    :alt: Logs tab showing the agent logging level setting
    :class: screenshot
    :::

2. Select an **Agent logging level**:

    |     |     |
    | --- | --- |
    | `error`<br> | Logs errors and critical errors. |
    | `warning`<br> | Logs warnings, errors, and critical errors. |
    | `info`<br> | Logs informational messages, including the number of events that are published.Also logs any warnings, errors, or critical errors. |
    | `debug`<br> | Logs debug messages, including a detailed printout of all events flushed. Alsologs informational messages, warnings, errors, and critical errors. |

3. Click **Apply changes** to apply the updated logging level to the agent.


## Collect {{agent}} diagnostics [collect-agent-diagnostics]

{{fleet}} provides the ability to remotely generate and gather an {{agent}}'s diagnostics bundle. An agent can gather and upload diagnostics if it is online in a `Healthy` or `Unhealthy` state. To download the diagnostics bundle for local viewing:

1. In {{fleet}}, open the **Agents** tab.
2. In the **Host** column, click the agent’s name.
3. Select the **Diagnostics** tab and click the **Request diagnostics .zip** button.

    :::{image} images/collect-agent-diagnostics1.png
    :alt: Collect agent diagnostics under agent details
    :class: screenshot
    :::

4. In the **Request Diagnostics** pop-up, select **Collect additional CPU metrics** if you’d like detailed CPU data.

    :::{image} images/collect-agent-diagnostics2.png
    :alt: Collect agent diagnostics confirmation pop-up
    :class: screenshot
    :::

5. Click the **Request diagnostics** button.

When available, the new diagnostic bundle will be listed on this page, as well as any in-progress or previously collected bundles for the {{agent}}.

Note that the bundles are stored in {{es}} and are removed automatically after 7 days. You can also delete any previously created bundle by clicking the `trash can` icon.


## View the {{agent}} metrics dashboard [view-agent-metrics]

When agent monitoring is configured to collect metrics (the default), you can use the **[Elastic Agent] Agent metrics** dashboard in {{kib}} to view details about {{agent}} resource usage, event throughput, and errors. This information can help you identify problems and make decisions about scaling your deployment.

To view agent metrics:

1. In {{fleet}}, open the **Agents** tab.
2. In the **Host** column, click the agent’s name.
3. On the **Agent details** tab, verify that **Monitor metrics** is enabled. If it’s not, refer to [Change {{agent}} monitoring settings](#change-agent-monitoring).
4. Click **View more agent metrics** to navigate to the **[Elastic Agent] Agent metrics** dashboard.

    :::{image} images/selected-agent-metrics-dashboard.png
    :alt: Screen capture showing {{agent}} metrics
    :class: screenshot
    :::


The dashboard uses standard {{kib}} visualizations that you can extend to meet your needs.


## Change {{agent}} monitoring settings [change-agent-monitoring]

Agent monitoring is turned on by default in the agent policy. To change agent monitoring settings for all agents enrolled in a specific agent policy:

1. In {{fleet}}, open the **Agent policies** tab.
2. Click the agent policy to edit it, then click **Settings**.
3. Under **Agent monitoring**, deselect (or select) one or both of these settings: **Collect agent logs** and **Collect agent metrics**.
4. Under **Advanced monitoring options** you can configure additional settings including an HTTP monitoring endpoint, diagnostics rate limiting, and diagnostics file upload limits. Refer to [configure agent monitoring](/reference/ingestion-tools/fleet/agent-policy.md#change-policy-enable-agent-monitoring) for details.
5. Save your changes.

To turn off agent monitoring when creating a new agent policy:

1. In the **Create agent policy** flyout, expand **Advanced options**.
2. Under **Agent monitoring**, deselect **Collect agent logs** and **Collect agent metrics**.
3. When you’re done configuring the agent policy, click **Create agent policy**.


## Send {{agent}} monitoring data to a remote {{es}} cluster [external-elasticsearch-monitoring]

You may want to store all of the health and status data about your {{agents}} in a remote {{es}} cluster, so that it’s separate and independent from the deployment where you use {{fleet}} to manage the agents.

To do so, follow the steps in [Remote {{es}} output](/reference/ingestion-tools/fleet/remote-elasticsearch-output.md). After the new output is configured, follow the steps to update the {{agent}} policy and make sure that the **Output for agent monitoring** setting is enabled. {{agent}} monitoring data will use the remote {{es}} output that you configured.


## Enable alerts and ML jobs based on {{fleet}} and {{agent}} status [fleet-alerting]

You can access the health status of {{fleet}}-managed {{agents}} and other {{fleet}} settings through internal {{fleet}} indices. This enables you to leverage various applications within the {{stack}} that can be triggered by the provided information. For instance, you can now create alerts and machine learning (ML) jobs based on these specific fields. Refer to the [Alerting documentation](/explore-analyze/alerts-cases.md) or see the [example](#fleet-alerting-example) on this page to learn how to define rules that can trigger actions when certain conditions are met.

This functionality allows you to effectively track an agent’s status, and identify scenarios where it has gone offline, is experiencing health issues, or is facing challenges related to input or output.

The following datastreams and fields are available.

Datastream
:   `metrics-fleet_server.agent_status-default`

    This data stream publishes the number of {{agents}} in various states.

    **Fields**

    * `@timestamp`
    * `fleet.agents.total` - A count of all agents
    * `fleet.agents.enrolled` - A count of all agents currently enrolled
    * `fleet.agents.unenrolled` - A count of agents currently unenrolled
    * `fleet.agents.healthy` - A count of agents currently healthy
    * `fleet.agents.offline` - A count of agents currently offline
    * `fleet.agents.updating` - A count of agents currently in the process of updating
    * `fleet.agents.unhealthy` - A count of agents currently unhealthy
    * `fleet.agents.inactive` - A count of agents currently inactive

    ::::{note}
    Other fields regarding agent status, based on input and output health, are currently under consideration for future development.
    ::::


Datastream
:   `metrics-fleet_server.agent_versions-default`

    This index publishes a separate document for each version number and a count of enrolled agents only.

    **Fields**

    * `@timestamp`
    * `fleet.agent.version` - A keyword field containing the version number
    * `fleet.agent.count` - A count of agents on the specified version



### Example: Enable an alert for offline {{agent}}s [fleet-alerting-example]

You can set up an alert to notify you when one or more {{agent}}s goes offline:

1. In {{kib}}, navigate to **Management > Stack Management > Rules**.
2. Click **Create rule**.
3. Select **Elasticsearch query** as the rule type.
4. Choose a name for the rule, for example `Elastic Agent status`.
5. Select **KQL or Lucene** as the query type.
6. Select `DATA VIEW metrics-*` as the data view.
7. Define your query, for example: `fleet.agents.offline >= 1`.
8. Set the alert group, threshold, and time window. For example:

    * WHEN: `count()`
    * OVER: `all documents`
    * IS ABOVE: `0`
    * FOR THE LAST `5 minutes`

        This will generate an alert when one or more agents are reported by the `fleet.agents.offline` field over the last five minutes to be offline.

9. Set the number of documents to send, for example:

    * SIZE: 100

10. Set **Check every** to the frequency at which the rule condition should be evaluated. The default setting is one minute.
11. Select an action to occur when the rule conditions are met. For example, to set the alert to send an email when an alert occurs, select the Email connector type and specify:

    * Email connector: `Elastic-Cloud-SMTP`
    * Action frequency: `For each alert` and `On check intervals`
    * Run when: `Query matched`
    * To: <the recipient email address>
    * Subject: <the email subject line>

12. Click **Save**.

The new rule will be enabled and an email will be sent to the specified recipient when the alert conditions are met.

From the **Rules** page you can select the rule you created to enable or disable it, and to view the rule details including a list of active alerts and an alert history.

:::{image} images/elastic-agent-status-rule.png
:alt: A screen capture showing the details for the new Elastic Agent status rule
:::
