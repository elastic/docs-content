---
navigation_title: "View monitoring data"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/monitoring-data.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
---

<!-- This doc needs to be moved somewhere else, it's not specific about self-managed, it's about Stack Monitoring in general -->
% hola

# View monitoring data [monitoring-data]


After you collect monitoring data for one or more products in the {{stack}}, you can configure {{kib}} to retrieve that information and display it in on the **Stack Monitoring** page.

At a minimum, you must have monitoring data for the {{es}} production cluster. Once that data exists, {{kib}} can display monitoring data for other products in the cluster.

::::{tip}
If you use a separate monitoring cluster to store the monitoring data, it is strongly recommended that you use a separate {{kib}} instance to view it. If you log in to {{kib}} using SAML, Kerberos, PKI, OpenID Connect, or token authentication providers, a dedicated {{kib}} instance is **required**. The security tokens that are used in these contexts are cluster-specific, therefore you cannot use a single {{kib}} instance to connect to both production and monitoring clusters. For more information about the recommended configuration, see [Monitoring overview](../stack-monitoring.md).
::::


1. Identify where to retrieve monitoring data from.

    If the monitoring data is stored on a dedicated monitoring cluster, it is accessible even when the cluster you’re monitoring is not. If you have at least a gold license, you can send data from multiple clusters to the same monitoring cluster and view them all through the same instance of {{kib}}.

    By default, data is retrieved from the cluster specified in the `elasticsearch.hosts` value in the `kibana.yml` file. If you want to retrieve it from a different cluster, set `monitoring.ui.elasticsearch.hosts`.

    To learn more about typical monitoring architectures, see [How monitoring works](../stack-monitoring.md) and [Monitoring in a production environment](elasticsearch-monitoring-self-managed.md).

2. Verify that `monitoring.ui.enabled` is set to `true`, which is the default value, in the `kibana.yml` file. For more information, see [Monitoring settings](kibana://reference/configuration-reference/monitoring-settings.md).
3. If the Elastic {{security-features}} are enabled on the monitoring cluster, you must provide a user ID and password so {{kib}} can retrieve the data.

    1. Create a user that has the `monitoring_user` [built-in role](../../users-roles/cluster-or-deployment-auth/built-in-roles.md) on the monitoring cluster.

        ::::{note}
        Make sure the `monitoring_user` role has read privileges on `metrics-*` indices. If it doesn’t, create a new role with `read` and `read_cross_cluster` index privileges on `metrics-*`, then assign the new role (along with `monitoring_user`) to your user.
        ::::

    2. Add the `monitoring.ui.elasticsearch.username` and `monitoring.ui.elasticsearch.password` settings in the `kibana.yml` file. If these settings are omitted, {{kib}} uses the `elasticsearch.username` and `elasticsearch.password` setting values. For more information, see [Configuring security in {{kib}}](../../security.md).

4. (Optional) Configure {{kib}} to encrypt communications between the {{kib}} server and the monitoring cluster. See [*Encrypt TLS communications in {{kib}}*](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-http).
5. If the Elastic {{security-features}} are enabled on the {{kib}} server, only users that have the authority to access {{kib}} indices and to read the monitoring indices can use the monitoring dashboards.

    ::::{note}
    These users must exist on the monitoring cluster. If you are accessing a remote monitoring cluster, you must use credentials that are valid on both the {{kib}} server and the monitoring cluster.
    ::::


    1. Create users that have the `monitoring_user` and `kibana_admin` [built-in roles](../../users-roles/cluster-or-deployment-auth/built-in-roles.md). If you created a new role with read privileges on `metrics-*` indices, also assign that role to the users.

6. Open {{kib}} in your web browser.

    By default, if you are running {{kib}} locally, go to `http://localhost:5601/`.

    If the Elastic {{security-features}} are enabled, log in.

7. Go to the **Stack Monitoring** page using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    If data collection is disabled, you are prompted to turn on data collection. If {{es}} {{security-features}} are enabled, you must have `manage` cluster privileges to turn on data collection.

    ::::{note}
    If you are using a separate monitoring cluster, you do not need to turn on data collection. The dashboards appear when there is data in the monitoring cluster.
    ::::


You’ll see cluster alerts that require your attention and a summary of the available monitoring metrics for {{es}}, Logstash, {{kib}}, and Beats. To view additional information, click the Overview, Nodes, Indices, or Instances links.  See [Stack Monitoring](../monitoring-data/visualizing-monitoring-data.md).

:::{image} ../../../images/kibana-monitoring-dashboard.png
:alt: Monitoring dashboard
:class: screenshot
:::

If you encounter problems, see [Troubleshooting monitoring](../monitoring-data/monitor-troubleshooting.md).

