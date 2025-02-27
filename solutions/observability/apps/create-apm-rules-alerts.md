---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-alerts.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-alerts.html

navigation_title: "Create rules and alerts"
---

# Create APM rules and alerts [apm-alerts]


The Applications UI allows you to define **rules** to detect complex conditions within your APM data and trigger built-in **actions** when those conditions are met.


## APM rules [apm_rules]

The following APM rules are supported:

|     |     |
| --- | --- |
| **APM Anomaly** | Alert when either the latency, throughput, or failed transaction rate of a service is anomalous.Anomaly rules can be set at the environment level, service level, and/or transaction type level. Read more in [APM Anomaly rule →](../../../solutions/observability/incident-management/create-an-apm-anomaly-rule.md) |
| **Error count threshold** | Alert when the number of errors in a service exceeds a defined threshold. Error count rules can be set at theenvironment level, service level, and error group level. Read more in [Error count threshold rule →](../../../solutions/observability/incident-management/create-an-error-count-threshold-rule.md) |
| **Failed transaction rate threshold** | Alert when the rate of transaction errors in a service exceeds a defined threshold. Read more in [Failed transaction rate threshold rule →](../../../solutions/observability/incident-management/create-failed-transaction-rate-threshold-rule.md) |
| **Latency threshold** | Alert when the latency or failed transaction rate is abnormal.Threshold rules can be as broad or as granular as you’d like, enabling you to define exactly when you want to be alerted—​whether that’s at the environment level, service name level, transaction type level, and/or transaction name level. Read more in [Latency threshold rule →](../../../solutions/observability/incident-management/create-latency-threshold-rule.md) |

::::{tip}
For a complete walkthrough of the **Create rule** flyout panel, including detailed information on each configurable property, see Kibana’s [Create and manage rules](../../../explore-analyze/alerts-cases/alerts/create-manage-rules.md).

::::

## Rules and alerts in the Applications UI [_rules_and_alerts_in_the_applications_ui]
```{applies_to}
stack: all
```

View and manage rules and alerts in the Applications UI.


### View active alerts [apm-alert-view-active]

Active alerts are displayed and grouped in multiple ways in the Applications UI.


#### View alerts by service group [apm-alert-view-group]

If you’re using the [service groups](../../../solutions/observability/apps/services.md#service-groups) feature, you can view alerts by service group. From the service group overview page, click the red alert indicator to open the **Alerts** tab with a predefined filter that matches the filter used when creating the service group.

:::{image} ../../../images/observability-apm-service-group.png
:alt: Example view of service group in the Applications UI in Kibana
:class: screenshot
:::


#### View alerts by service [apm-alert-view-service]

Alerts can be viewed within the context of any service. After selecting a service, go to the **Alerts** tab to view any alerts that are active for the selected service.

:::{image} ../../../images/observability-active-alert-service.png
:alt: View active alerts by service
:class: screenshot
:::


### Manage alerts and rules [apm-alert-manage]

From the Applications UI, select **Alerts and rules** → **Manage rules** to be taken to the {{kib}} **{{rules-ui}}** page. From this page, you can disable, mute, and delete APM alerts.


### More information [apm-alert-more-info]

See [Alerting](../../../explore-analyze/alerts-cases.md) for more information.

::::{note}
If you are using an **on-premise** Elastic Stack deployment with security, communication between Elasticsearch and Kibana must have TLS configured. More information is in the alerting [prerequisites](../../../explore-analyze/alerts-cases/alerts/alerting-setup.md#alerting-prerequisites).
::::