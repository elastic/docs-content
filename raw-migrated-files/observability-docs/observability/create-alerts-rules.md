# Create and manage rules [create-alerts-rules]

The first step when setting up alerts is to create a rule. To create and manage rules related to {{observability}} apps, go to the {{observability}} **Alerts** page and click **Manage Rules** to navigate to the {{observability}} Rules page. You can also create rules directly from most {{observability}} UIs by clicking **Alerts and rules** and selecting a rule.

To create SLO rules, you must first define a new SLO via the **Create new SLO** button. Once an SLO has been defined, you can create SLO rules tied to this SLO.

:::{image} ../../../images/observability-create-alerts-manage-rules.png
:alt: Elastic {{observability}} Rules page
:class: screenshot
:::

::::{note}
You can also centrally create and manage rules, including rules *not* related to {{observability}}, from the [{{kib}} Management UI](../../../explore-analyze/alerts/kibana/create-manage-rules.md).
::::


From the {{observability}} Rules page, you can manage rules for {{observability}} apps, including:

* Creating a new rule
* Editing or deleting existing rules
* Updating the status of existing rules (Enabled, Disabled, or Snoozed indefinitely)

::::{note}
The {{observability}} Rules page allows you to set a rule to be "Snoozed indefinitely". To snooze a rule for a specific time period, you must use the centralized [{{rules-ui}} page](../../../explore-analyze/alerts/kibana/create-manage-rules.md).

[preview] To temporarily suppress notifications for *all* rules, create a [maintenance window](../../../explore-analyze/alerts/kibana/maintenance-windows.md).

::::


Extend your rules by connecting them to actions that use built-in **connectors** for email, {{ibm-r}}, Index, JIRA, Microsoft Teams, PagerDuty, Server log, {{sn}} ITSM, {{sn}} SecOps, {{sn}} ITOM, Opsgenie, and Slack. Also supported is a powerful webhook output letting you tie into other third-party systems. Connectors allow actions to talk to these services and integrations.

Learn how to create specific types of rules:

* **All of Observability**:

    * [Custom threshold rule](../../../solutions/observability/incident-management/create-custom-threshold-rule.md)
    * [SLO burn rate rule](../../../solutions/observability/incident-management/create-an-slo-burn-rate-rule.md)

* **APM**:

    * [APM Anomaly rule](../../../solutions/observability/incident-management/create-an-apm-anomaly-rule.md)
    * [Error count threshold rule](../../../solutions/observability/incident-management/create-an-error-count-threshold-rule.md)
    * [Failed transaction rate threshold rule](../../../solutions/observability/incident-management/create-an-error-count-threshold-rule.md)
    * [Latency threshold rule](../../../solutions/observability/incident-management/create-latency-threshold-rule.md)

* **Infrastructure**:

    * [Inventory rule](../../../solutions/observability/incident-management/create-an-inventory-rule.md)
    * [Metric threshold rule](../../../solutions/observability/incident-management/create-metric-threshold-rule.md)

* **Logs**:

    * [Log threshold rule](../../../solutions/observability/incident-management/create-log-threshold-rule.md)

* **Synthetics**:

    * [Synthetics monitor status rule](../../../solutions/observability/incident-management/create-monitor-status-rule.md#monitor-status-alert-synthetics)
    * [Synthetics TLS certificate rule](../../../solutions/observability/incident-management/create-tls-certificate-rule.md#tls-rule-synthetics)

* **Uptime** ([8.15.0]):

    * [Uptime monitor status rule](../../../solutions/observability/incident-management/create-monitor-status-rule.md#monitor-status-alert-uptime)
    * [Uptime TLS rule](../../../solutions/observability/incident-management/create-tls-certificate-rule.md#tls-rule-uptime)
    * [Uptime duration anomaly rule](../../../solutions/observability/incident-management/create-an-uptime-duration-anomaly-rule.md)



## View rule details [create-alerts-rules-details]

Click on an individual rule on the Rules page to view details including the rule name, status, definition, execution history, related alerts, and more.

:::{image} ../../../images/observability-create-alerts-rules-details.png
:alt: Elastic {{observability}} detail page for a single rule
:class: screenshot
:::

::::{note}
You can also view rule details by clicking on individual rules in the [{{kib}} Management UI](../../../explore-analyze/alerts/kibana/create-manage-rules.md).
::::



## View and manage alerts [create-alerts-alert]

The **Alerts** page lists all your alerts that have met a condition defined by a rule you created using one of the Observability apps.

Learn more about viewing and managing alerts in [View alerts](../../../solutions/observability/incident-management/view-alerts.md).

:::{image} ../../../images/observability-alerts-page.png
:alt: Elastic {{observability}} Alerts page
:class: screenshot
:::

::::{important}
Not all the predefined rules in {{stack-manage-app}} will generate and list an alert on the {{observability}} Alerts page. Only alerts generated by rules relating to Applications, Logs, Infrastructure, Synthetics, and Uptime can be viewed on the Alerts page.
::::



## Configure alerts [create-alerts-configure]

You may want to disable writing to specific {{observability}} alert indices or disable all alerts and remove the Alerts page altogether. You can do this in {{kib}} settings.

If you are using our [hosted {{ess}}](https://www.elastic.co/cloud/elasticsearch-service) on {{ecloud}}, you’ll edit the {{kib}} user settings:

1. Select your deployment on the home page, and from your deployment menu go to the **Edit** page.
2. In the **{{kib}}** section, click **Edit user settings**, and add the desired settings (detailed below).
3. Click **Back**, and then click **Save**. The changes are automatically appended to the `kibana.yml` configuration file for your instance.

If you have a self-managed {{stack}}, you’ll edit the settings in your `kibana.yml` file.


### Disable writing to specific alert indices [create-alerts-disable-some]

To disable writing to specific {{observability}} alerts-as-data indices while continuing to write to others, use `xpack.ruleRegistry.write.disabledRegistrationContexts`.

You can disable writing to alert indices for:

* Logs (`observability.logs`)
* Infrastructure (`observability.metrics`)
* APM (`observability.apm`)
* Uptime (`observability.uptime`)

::::{note}
Disabling writing to the indices of one of the {{observability}} apps listed above will affect *all* rule types of the corresponding app. For example, disabling writing to uptime alert indices will affect *all* uptime rule types including monitor status and TLS rule types.
::::


For example, to disable writing to Logs alert indices, you would add the following to your {{kib}} settings:

```yaml
xpack.ruleRegistry.write.disabledRegistrationContexts : ['observability.logs']
```

To disable writing to both Logs and Uptime alert indices, you would use:

```yaml
xpack.ruleRegistry.write.disabledRegistrationContexts : ['observability.logs', 'observability.uptime']
```


### Remove the Alerts page [create-alerts-remove-page]

To disable writing to all alert indices and remove the Alerts page from {{kib}} altogether, use the following settings:

```yaml
xpack.ruleRegistry.write.enabled: 'false'
xpack.observability.unsafe.alertingExperience.enabled: 'false'
```













