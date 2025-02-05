---
navigation_title: "Collect monitoring data with {{agent}}"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/monitoring-elastic-agent.html
applies:
  stack: all
---



# Collect monitoring data with Elastic Agent [monitoring-elastic-agent]


In 8.5 and later, you can use {{agent}} to collect data about {{kib}} and ship it to the monitoring cluster, rather than [using {{metricbeat}}](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-metricbeat.md) or routing data through the production cluster as described in [Legacy collection methods](/deploy-manage/monitor/stack-monitoring/kibana-monitoring-legacy.md).

To learn about monitoring in general, see [Monitor a cluster](../../monitor.md).


## Prerequisites [_prerequisites]

* Set up {{es}} monitoring and optionally create a monitoring cluster as described in the [{{es}} monitoring documentation](elasticsearch-monitoring-self-managed.md).
* Create a user on the production cluster that has the `remote_monitoring_collector` [built-in role](../../users-roles/cluster-or-deployment-auth/built-in-roles.md).


## Add {{kib}} monitoring data [_add_kib_monitoring_data]

To collect {{kib}} monitoring data, add a {{kib}} integration to an {{agent}} and deploy it to the host where {{kib}} is running.

1. Go to the **Integrations** page.

    ::::{note}
    If you’re using a monitoring cluster, use the {{kib}} instance connected to the monitoring cluster.
    ::::

2. In the query bar, search for and select the **Kibana** integration for {{agent}}.
3. Read the overview to make sure you understand integration requirements and other considerations.
4. Click **Add Kibana**.

    ::::{tip}
    If you’re installing an integration for the first time, you may be prompted to install {{agent}}. Click **Add integration only (skip agent installation)**.
    ::::

5. Configure the integration name and optionally add a description. Make sure you configure all required settings:

    * Under **Collect Kibana logs**, modify the log paths to match your {{kib}} environment.
    * Under **Collect Kibana metrics**, make sure the hosts setting points to your Kibana host URLs. By default, the integration collects {{kib}} monitoring metrics from `localhost:5601`. If that host and port number are not correct, update the `hosts` setting. If you configured {{kib}} to use encrypted communications, you must access it via HTTPS. For example, use a `hosts` setting like `https://localhost:5601`.
    * If the Elastic {{security-features}} are enabled, expand **Advanced options** under the Hosts setting and enter the username and password of a user that has the `remote_monitoring_collector` role.

6. Choose where to add the integration policy. Click **New hosts*** to add it to new agent policy or ***Existing hosts** to add it to an existing agent policy.
7. Click **Save and continue**. This step takes a minute or two to complete. When it’s done, you’ll have an agent policy that contains an integration for collecting monitoring data from {{kib}}.
8. If an {{agent}} is already assigned to the policy and deployed to the host where {{kib}} is running, you’re done. Otherwise, you need to deploy an {{agent}}. To deploy an {{agent}}:

    1. Go to **{{fleet}} → Agents***, then click ***Add agent**.
    2. Follow the steps in the **Add agent** flyout to download, install, and enroll the {{agent}}. Make sure you choose the agent policy you created earlier.

9. Wait a minute or two until incoming data is confirmed.
10. [View the monitoring data in {{kib}}](/deploy-manage/monitor/monitoring-data.md).
