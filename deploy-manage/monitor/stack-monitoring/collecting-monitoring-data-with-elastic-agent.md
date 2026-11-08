---
navigation_title: Collecting monitoring data with {{agent}}
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/configuring-elastic-agent.html
applies_to:
  deployment:
    self: all
products:
  - id: elasticsearch
---



# Collecting monitoring data with Elastic Agent [configuring-elastic-agent]

You can use {{agent}} to collect data about {{es}} and ship it to the monitoring cluster.

## Prerequisites [_prerequisites_11]

* (Optional) Create a monitoring cluster as described in [](elasticsearch-monitoring-self-managed.md).
* Create a user on the production cluster that has the `remote_monitoring_collector` [built-in role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-remote-monitoring-collector).


## Add {{es}} monitoring data [_add_es_monitoring_data]

To collect {{es}} monitoring data, add an {{es}} integration to an {{agent}} and deploy it to the host where {{es}} is running.

1. Find **Integrations** in the navigation menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Search for and select **{{es}}**.
3. If the integration's **Overview** page opens, click **Add Elasticsearch**.
4. If the **Ready to add your first integration?** page opens, click **Add integration only (skip agent installation)**.
5. Configure the integration name and optionally add a description. Then update the following settings:

    1. Under **Logs**, modify the log paths to match your {{es}} environment.
    2. Under **Metrics (Stack Monitoring)**, make sure the hosts setting points to your {{es}} host URLs. By default, the integration collects {{es}} monitoring metrics from `localhost:9200`. If that host and port number are not correct, update the `hosts` setting. If you configured {{es}} to use encrypted communications, you must access it via HTTPS. For example, use a `hosts` setting like `https://localhost:9200`.
    3. Expand **Advanced options**. If the Elastic {{security-features}} are enabled, enter the username and password of a user that has the `remote_monitoring_collector` role.
    4. Specify the scope:

        * Specify `cluster` if each entry in the hosts list indicates a single endpoint for a distinct {{es}} cluster (for example, a load-balancing proxy fronting the cluster that directs requests to the master-ineligible nodes in the cluster).
        * Otherwise, accept the default scope, `node`. If this scope is set, you will need to install {{agent}} on each {{es}} node to collect all metrics. {{agent}} will collect most of the metrics from the elected master of the cluster, so you must scale up all your master-eligible nodes to account for this extra load. Do not use this `node` if you have dedicated master nodes.

6. Choose where to add the integration policy. Click **New hosts** to add it to new agent policy or **Existing hosts** to add it to an existing agent policy.
7. Click **Save and continue**. This step takes a minute or two to complete. When it’s done, you’ll have an agent policy that contains an integration for collecting monitoring data from {{es}}.
8. If an {{agent}} is already assigned to the policy and deployed to the host where {{es}} is running, you’re done. Otherwise, you need to deploy an {{agent}}. To deploy an {{agent}}:

    1. Go to **{{fleet}} → Agents**, then click **Add agent**.
    2. Follow the steps in the **Add agent** flyout to download, install, and enroll the {{agent}}. Make sure you choose the agent policy you created earlier.

9. Wait a minute or two until incoming data is confirmed.
10. [View the monitoring data in {{kib}}](kibana-monitoring-data.md).

## Next steps

:::{include} /deploy-manage/monitor/stack-monitoring/_snippets/consumption-next-steps.md
:::
