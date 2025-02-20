---
mapped_urls:
  - https://www.elastic.co/guide/en/security/current/es-threat-intel-integrations.html
  - https://www.elastic.co/guide/en/serverless/current/security-threat-intelligence.html
---

# Enable threat intelligence integrations [security-enable-threat-intelligence-integrations]

The Threat Intelligence view provides a streamlined way to collect threat intelligence data that you can use for threat detection and matching. Threat intelligence data consists of  [threat indicators](/solutions/security/investigate/indicators-of-compromise.md#ti-indicators) ingested from third-party threat intelligence sources.

Threat indicators describe potential threats, unusual behavior, or malicious activity on a network or in an environment. They are commonly used in indicator match rules to detect and match known threats. When an indicator match rule generates an alert, it includes information about the matched threat indicator.

::::{note}
To learn more about alerts with threat intelligence, visit [View alert details](../detect-and-alert/view-detection-alert-details.md).

::::


You can connect to threat intelligence sources using an [{{agent}} integration](#agent-ti-integration), the [Threat Intel module](#ti-mod-integration), or a [custom integration](#custom-ti-integration).

:::{image} ../../../images/getting-started-threat-intelligence-view.png
:alt: The Threat Intelligence view on the Overview dashboard
:class: screenshot
:::

There are a few scenarios when data won’t display in the Threat Intelligence view:

* If you’ve chosen a time range that doesn’t contain threat indicator event data, you are prompted to choose a different range. Use the date and time picker in the {{security-app}} to select a new range to analyze.
* If the {{agent}} or {{filebeat}} agent hasn’t ingested Threat Intel module data yet, the threat indicator event counts won’t load. You can wait for data to be ingested or reach out to your administrator for help resolving this.


## Add an {{agent}} integration [agent-ti-integration]

1. Install a [{{fleet}}-managed {{agent}}](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/install-fleet-managed-elastic-agent.md) on the hosts you want to monitor.
2. In the Threat Intelligence view, click **Enable sources** to view the Integrations page. Scroll down and select **Elastic Agent only** to filter by {{agent}} integrations.

    ::::{tip}
    If you know the name of {{agent}} integration you want to install, you can search for it directly. Alternatively, choose the **Threat Intelligence** category to display a list of available [threat intelligence integrations](https://docs.elastic.co/en/integrations/threat-intelligence-intro).

    ::::

3. Select an {{agent}} integration, then complete the installation steps.
4. Return to the Threat Intelligence view on the Overview dashboard. If indicator data isn’t displaying, refresh the page or refer to these [troubleshooting steps](../../../troubleshoot/security/indicators-of-compromise.md).


## Add a {{filebeat}} Threat Intel module integration [ti-mod-integration]

% Substeps in step 2 will require inline versioning. Remember to update them when we have more guidance on handling line-level differences.

1. Set up the [{{filebeat}} agent](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-filebeat/filebeat-installation-configuration.md) and enable the Threat Intel module.

    ::::{note}
    For more information about enabling available threat intelligence filesets, refer to [Threat Intel module](asciidocalypse://docs/beats/docs/reference/ingestion-tools/beats-filebeat/filebeat-module-threatintel.md).

    ::::

2. Update the `securitySolution:defaultThreatIndex` [advanced setting](configure-advanced-settings.md#update-threat-intel-indices) by adding the appropriate index pattern name after the default {{fleet}} threat intelligence index pattern (`logs-ti*`):

    * If you’re *only* using {{filebeat}} version 8.x, add the appropriate {{filebeat}} threat intelligence index pattern. For example, `logs-ti*`, `filebeat-8*`. 
    * If you’re using a previous version of Filebeat *and* a current one, differentiate between the threat intelligence indices by using unique index pattern names. For example, if you’re using {{filebeat}} version 7.0.0 and 8.0.0, update the setting to `logs-ti*`,`filebeat-7*`,`filebeat-8*`.

3. Return to the Threat Intelligence view on the Overview dashboard. Refresh the page if indicator data isn’t displaying.


## Add a custom integration [custom-ti-integration]

1. Set up a way to [ingest data](ingest-data-to-elastic-security.md) into your system.
2. Update the `securitySolution:defaultThreatIndex` [advanced setting](configure-advanced-settings.md#update-threat-intel-indices) by adding the appropriate index pattern name after the default {{fleet}} threat intelligence index pattern (`logs-ti*`), for example, `logs-ti*`,`custom-ti-index*`.

    ::::{note}
    Threat intelligence indices aren’t required to be ECS compatible. However, we strongly recommend compatibility if you’d like your alerts to be enriched with relevant threat indicator information. You can find a list of ECS-compliant threat intelligence fields at [Threat Fields](asciidocalypse://docs/ecs/docs/reference/ecs/ecs-threat.md).

    ::::

3. Return to the Threat Intelligence view on the Overview dashboard (**Dashboards** → **Overview**). Refresh the page if indicator data isn’t displaying.

    ::::{note}
    The Threat Intelligence view searches for a `threat.feed.name` field value to define the source name in the **Name** column. If a custom source doesn’t have the `threat.feed.name` field or hasn’t defined a `threat.feed.name` field value, it’s considered unnamed and labeled as **Other**. Dashboards aren’t created for unnamed sources unless the `threat.feed.dashboard_id` field is defined.

    ::::
