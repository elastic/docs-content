---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/configure-uptime-settings.html
applies_to:
  stack: all
---

# Configure settings [configure-uptime-settings]

The **Settings** page enables you to change which {{heartbeat}} indices are displayed by the {{uptime-app}}, configure rule connectors, and set expiration/age thresholds for TLS certificates.

Uptime settings apply to the current space only. To segment different uptime use cases and domains, use different settings in other spaces.

1. To access this page, go to **{{observability}} > Uptime**.
2. At the top of the page, click **Settings**.

    ::::{important}
    To modify items on this page, you must have the [`all`](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) Uptime privilege granted to your role.

    ::::



## Configure indices [configure-uptime-indices]

Specify a comma-separated list of index patterns to match indices in {{es}} that contain {{heartbeat}} data.

::::{note}
The pattern set here only restricts what the {{uptime-app}} displays. You can still query {{es}} for data outside of this pattern.

::::


:::{image} ../../../images/observability-heartbeat-indices.png
:alt: {{heartbeat}} indices
:class: screenshot
:::


## Configure connectors [configure-uptime-alert-connectors]

**Alerts** work by running checks on a schedule to detect conditions defined by a rule. When a condition is met, the rule tracks it as an **alert** and responds by triggering one or more **actions**. Actions typically involve interaction with {{kib}} services or third party integrations. **Connectors** allow actions to talk to these services and integrations.

Click **Create connector** and follow the prompts to select a connector type and configure its properties. After you create a connector, it’s available to you anytime you set up a rule action in the current space.

For more information about each connector, see [action types and connectors](../../../deploy-manage/manage-connectors.md).

:::{image} ../../../images/observability-alert-connector.png
:alt: Rule connector
:class: screenshot
:::


## Configure certificate thresholds [configure-cert-thresholds]

You can modify certificate thresholds to control how Uptime displays your TLS values in the [TLS Certificates](uptime-monitoring-deprecated.md#view-certificate-status) page. These settings also determine which certificates are selected by any TLS rule you create.

|     |     |
| --- | --- |
| **Expiration threshold** | The `expiration` threshold specifies when you are notifiedabout certificates that are approaching expiration dates. When the value of a certificate’s remaining valid days fallsbelow the `Expiration threshold`, it’s considered a warning state. When you define a[TLS rule](../incident-management/create-tls-certificate-rule.md), you receive a notification about the certificate. |
| **Age limit** | The `age` threshold specifies when you are notified about certificatesthat have been valid for too long. |

A standard security requirement is to make sure that your TLS certificates have not been valid for longer than a year. To help you keep track of which certificates you may want to refresh, modify the **Age limit** value to `365` days.

:::{image} ../../../images/observability-cert-expiry-settings.png
:alt: Certificate expiry settings
:class: screenshot
:::

