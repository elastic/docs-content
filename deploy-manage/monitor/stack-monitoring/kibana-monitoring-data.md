---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/monitoring-data.html
applies_to:
  deployment:
    ess: all
    ece: all
    eck: all
    self: all
products:
  - id: kibana
---


# Access monitoring data in {{kib}} [monitoring-data]


After you collect monitoring data for one or more products in the {{stack}}, you can configure {{kib}} to retrieve that information and display it in on the **Stack Monitoring** page.

At a minimum, you must have monitoring data for the {{es}} production cluster. Once that data exists, {{kib}} can display monitoring data for other products in the cluster.

In {{ece}} and {{ech}}, this configuration is performed automatically. Skip to [View monitoring data in {{kib}}](#view-monitoring-data-in-kibana).

::::{tip}
If you use a separate monitoring cluster to store the monitoring data, it is strongly recommended that you use a separate {{kib}} instance to view it. If you log in to {{kib}} using SAML, Kerberos, PKI, OpenID Connect, or token authentication providers, a dedicated {{kib}} instance is **required**. The security tokens that are used in these contexts are cluster-specific, therefore you cannot use a single {{kib}} instance to connect to both production and monitoring clusters. For more information about the recommended configuration, see [Monitoring overview](../stack-monitoring.md).
::::

## Configure {{kib}} to consume monitoring data
```{applies_to}
deployment:
  eck:
  self:
```

1. Identify where to retrieve monitoring data from.

    If the monitoring data is stored on a dedicated monitoring cluster, it is accessible even when the cluster you’re monitoring is not. If you have at least a gold license, you can send data from multiple clusters to the same monitoring cluster and view them all through the same instance of {{kib}}.

    By default, data is retrieved from the cluster specified in the `elasticsearch.hosts` value in the [`kibana.yml`](/deploy-manage/stack-settings.md) file. If you want to retrieve it from a different cluster, set `monitoring.ui.elasticsearch.hosts`.

    To learn more about typical monitoring architectures, see [How monitoring works](../stack-monitoring.md) and [Monitoring in a production environment](elasticsearch-monitoring-self-managed.md).

2. Verify that `monitoring.ui.enabled` is set to `true`, which is the default value, in the [`kibana.yml`](/deploy-manage/stack-settings.md) file. For more information, see [Monitoring settings](kibana://reference/configuration-reference/monitoring-settings.md).
3. If the Elastic {{security-features}} are enabled on the monitoring cluster, you must provide a user ID and password so {{kib}} can retrieve the data.

    1. Create a user that has the `monitoring_user` [built-in role](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-monitoring-user) on the monitoring cluster.

        ::::{note}
        Make sure the `monitoring_user` role has read privileges on `metrics-*` indices. If it doesn’t, create a new role with `read` and `read_cross_cluster` index privileges on `metrics-*`, then assign the new role (along with `monitoring_user`) to your user.
        ::::

    2. Add the `monitoring.ui.elasticsearch.username` and `monitoring.ui.elasticsearch.password` settings in the [`kibana.yml`](/deploy-manage/stack-settings.md) file. If these settings are omitted, {{kib}} uses the `elasticsearch.username` and `elasticsearch.password` setting values. For more information, see [Configuring security in {{kib}}](../../security.md).

4. (Optional) If you're using a self-managed cluster, then optionally configure {{kib}} to encrypt communications between the {{kib}} server and the monitoring cluster. See [Encrypt TLS communications in {{kib}}](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-http).
5. If the Elastic {{security-features}} are enabled on the {{kib}} server, only users that have the authority to access {{kib}} indices and to read the monitoring indices can use the monitoring dashboards.

    Create users that have the `monitoring_user` and `kibana_admin` [built-in roles](elasticsearch://reference/elasticsearch/roles.md). If you created a new role with read privileges on `metrics-*` indices, also assign that role to the users.

    ::::{note}
    These users must exist on the monitoring cluster. If you are accessing a remote monitoring cluster, you must use credentials that are valid on both the {{kib}} server and the monitoring cluster.
    ::::

## View monitoring data in {{kib}} [view-monitoring-data-in-kibana]

:::::{applies-switch}
::::{applies-item} { eck:, self: }

1. Open the {{kib}} monitoring instance in your web browser.

    By default, if you are running {{kib}} locally, go to `http://localhost:5601/`.

    If the Elastic {{security-features}} are enabled, log in.

2. Go to the **Stack Monitoring** page using the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).

    If data collection is disabled, you are prompted to turn on data collection. If {{es}} {{security-features}} are enabled, you must have `manage` cluster privileges to turn on data collection.

:::{note}
If you are using a separate monitoring cluster, you do not need to turn on data collection. The dashboards appear when there is data in the monitoring cluster.
:::
::::
::::{applies-item} { ess:, ece: }
:::{include} /deploy-manage/monitor/stack-monitoring/_snippets/cloud-monitoring-access.md
:::
::::
:::::


On the **Stack Monitoring** page, you’ll see cluster alerts that require your attention and a summary of the available monitoring metrics for {{es}}, Logstash, {{kib}}, and Beats. To view additional information, click the **Overview**, **Nodes**, **Indices**, or **Instances** links.  For more information about these metrics, refer to [](../monitoring-data/visualizing-monitoring-data.md). For information about configuring alerts for these metrics, refer to [](/deploy-manage/monitor/monitoring-data/configure-stack-monitoring-alerts.md).

:::{image} /deploy-manage/images/kibana-monitoring-dashboard.png
:alt: Monitoring dashboard
:screenshot:
:::

The {{integrations-server}} monitoring component is available only on {{ech}} and {{ece}}.

If you encounter problems, refer to [](/deploy-manage/monitor/monitoring-data/monitor-troubleshooting.md).

:::{tip}
If you're using {{ech}} or {{ece}}, then you can also get a direct link to the relevant **Stack Monitoring** page from the deployment's **Logs and metrics** page. [Learn more](/deploy-manage/monitor/stack-monitoring/ece-ech-stack-monitoring.md#access-kibana-monitoring).
:::