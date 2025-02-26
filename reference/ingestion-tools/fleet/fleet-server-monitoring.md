---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/fleet-server-monitoring.html
---

# Monitor a self-managed Fleet Server [fleet-server-monitoring]

For self-managed {{fleet-server}}s, monitoring is key because the operation of the {{fleet-server}} is paramount to the health of the deployed agents and the services they offer. When {{fleet-server}} is not operating correctly, it may lead to delayed check-ins, status information, and updates for the agents it manages. The monitoring data will tell you when to add capacity for {{fleet-server}}, and provide error logs and information to troubleshoot other issues.

For self-managed clusters, monitoring is on by default when you create a new agent policy or use the existing Default {{fleet-server}} agent policy.

To monitor {{fleet-server}}:

1. In {{fleet}}, open the **Agent policies** tab.
2. Click the {{fleet-server}} policy name to edit the policy.
3. Click the **Settings** tab and verify that **Collect agent logs** and **Collect agent metrics** are selected.
4. Next, set the **Default namespace** to something like `fleetserver`.

    Setting the default namespace lets you segregate {{fleet-server}} monitoring data from other collected data. This makes it easier to search and visualize the monitoring data.

    :::{image} images/fleet-server-agent-policy-page.png
    :alt: {{fleet-server}} agent policy
    :class: screenshot
    :::

5. To confirm your change, click **Save changes**.

To see the metrics collected for the agent running {{fleet-server}}, go to **Analytics > Discover**.

In the following example, `fleetserver` was configured as the namespace, and you can see the metrics collected:

:::{image} images/datastream-namespace.png
:alt: Data stream
:class: screenshot
:::

Go to **Analytics > Dashboard** and search for the predefined dashboard called **[Elastic Agent] Agent metrics**. Choose this dashboard, and run a query based on the `fleetserver` namespace.

The following dashboard shows data for the query `data_stream.namespace: "fleetserver"`. In this example, you can observe CPU and memory usage as a metric and then resize the {{fleet-server}}, if necessary.

:::{image} images/dashboard-datastream01.png
:alt: Dashboard Data stream
:class: screenshot
:::

Note that as an alternative to running the query, you can hide all metrics except `fleet_server` in the dashboard.
