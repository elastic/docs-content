# Advanced settings [security-advanced-settings]

The advanced settings determine:

* Which indices {{elastic-sec}} uses to retrieve data
* {{ml-cap}} anomaly score display threshold
* The navigation menu style used throughout the {security-app}
* Whether the news feed is displayed on the [Overview dashboard](../../../solutions/security/dashboards/overview-dashboard.md)
* The default time interval used to filter {{elastic-sec}} pages
* The default {{elastic-sec}} pages refresh time
* Which IP reputation links appear on [IP detail](../../../solutions/security/explore/network-page.md) pages
* Whether cross-cluster search (CCS) privilege warnings are displayed
* Whether related integrations are displayed on the Rules page tables
* The options provided in the alert tag menu

To change these settings, you need either the appropriate [predefined Security user role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles) or a [custom role](../../../deploy-manage/users-roles/cloud-organization/user-roles.md) with `All` privileges for the **Advanced Settings** feature.

::::{warning}
Modifying advanced settings can affect performance and cause problems that are difficult to diagnose. Setting a property value to a blank field reverts to the default behavior, which might not be compatible with other configuration settings. Deleting a custom setting removes it permanently.

::::



## Access advanced settings [security-advanced-settings-access-advanced-settings]

To access advanced settings, go to **Project Settings** → **Management*** → ***Advanced Settings**, then scroll down to **Security Solution** settings.

::::{tip}
For more information on non-Security settings, refer to [Advanced Settings](https://www.elastic.co/guide/en/kibana/current/advanced-options.html). Some settings might not be available in serverless projects.

::::


:::{image} ../../../images/serverless--getting-started-solution-advanced-settings.png
:alt:  getting started solution advanced settings
:class: screenshot
:::


## Update default Elastic Security indices [update-sec-indices]

The `securitySolution:defaultIndex` field defines which {{es}} indices the {{security-app}} uses to collect data. By default, index patterns are used to match sets of {{es}} indices:

* `apm-*-transaction*`
* `auditbeat-*`
* `endgame-*`
* `filebeat-*`
* `logs-*`
* `packetbeat-*`
* `winlogbeat-*`

::::{note}
Index patterns use wildcards to specify a set of indices. For example, the `filebeat-*` index pattern means all indices starting with `filebeat-` are available in the {{security-app}}.

::::


All of the default index patterns match [{{beats}}](https://www.elastic.co/guide/en/beats/libbeat/current/beats-reference.html) and [{{agent}}](https://www.elastic.co/guide/en/fleet/current/fleet-overview.html) indices. This means all data shipped via {{beats}} and the {{agent}} is automatically added to the {{security-app}}.

You can add or remove any indices and index patterns as required, with a maximum of 50 items in the comma-delimited list. For background information on {{es}} indices, refer to [Data in: documents and indices](../../../manage-data/data-store/index-basics.md).

::::{note}
If you leave the `-*elastic-cloud-logs-*` index pattern selected, all Elastic cloud logs are excluded from all queries in the {{security-app}} by default. This is to avoid adding data from cloud monitoring to the app.

::::


::::{important}
{{elastic-sec}} requires [ECS-compliant data](https://www.elastic.co/guide/en/ecs/{{ecs_version}}). If you use third-party data collectors to ship data to {{es}}, the data must be mapped to ECS. [{{elastic-sec}} ECS field reference](https://www.elastic.co/guide/en/serverless/current/security-siem-field-reference.html) lists ECS fields used in {{elastic-sec}}.

::::



## Update default Elastic Security threat intelligence indices [update-threat-intel-indices]

The `securitySolution:defaultThreatIndex` advanced setting specifies threat intelligence indices that {{elastic-sec}} features query for ingested threat indicators. This setting affects features that query threat intelligence indices, such as the Threat Intelligence view on the Overview page, indicator match rules, and the alert enrichment query.

You can specify a maximum of 10 threat intelligence indices; multiple indices must be separated by commas. By default, only the `logs-ti*` index pattern is specified. Do not remove or overwrite this index pattern, as it is used by {{agent}} integrations.

::::{important}
Threat intelligence indices aren’t required to be ECS-compatible for use in indicator match rules. However, we strongly recommend compatibility if you want your alerts to be enriched with relevant threat indicator information. When searching for threat indicator data, indicator match rules use the threat indicator path specified in the **Indicator prefix override** advanced setting. Visit [Configure advanced rule settings](../../../solutions/security/detect-and-alert/create-detection-rule.md#rule-ui-advanced-params) for more information.

::::



## Telemetry settings [telemetry-settings]

Elastic transmits certain information about Elastic Security when users interact with the {{security-app}}, detailed below. Elastic redacts or obfuscates personal data (IP addresses, host names, usernames, etc.) before transmitting messages. Security-specific telemetry events include:

* **Detection rule security alerts:** Information about Elastic-authored prebuilt detection rules using the detection engine. Examples of alert data include machine learning job influencers, process names, and cloud audit events.
* **{{elastic-endpoint}} Security alerts:** Information about malicious activity detected using {{elastic-endpoint}} detection engines. Examples of alert data include malicious process names, digital signatures, and file names written by the malicious software. Examples of alert metadata include the time of the alert, the {{elastic-endpoint}} version and related detection engine versions.
* **Configuration data for {{elastic-endpoint}}:** Information about the configuration of {{elastic-endpoint}} deployments. Examples of configuration data include the Endpoint versions, operating system versions, and performance counters for Endpoint.
* **Exception list entries for Elastic rules:** Information about exceptions added for Elastic rules. Examples include trusted applications, detection exceptions, and rule exceptions.
* **Security alert activity records:** Information about actions taken on alerts generated in the {{security-app}}, such as acknowledged or closed.

To learn more, refer to our [Privacy Statement](https://www.elastic.co/legal/privacy-statement).


## Set machine learning score threshold [security-advanced-settings-set-machine-learning-score-threshold]

When security [{{ml}} jobs](../../../solutions/security/advanced-entity-analytics/anomaly-detection.md) are enabled, this setting determines the threshold above which anomaly scores appear in {{elastic-sec}}:

* `securitySolution:defaultAnomalyScore`


## Modify news feed settings [security-advanced-settings-modify-news-feed-settings]

You can change these settings, which affect the news feed displayed on the {{elastic-sec}} **Overview** page:

* `securitySolution:enableNewsFeed`: Enables the security news feed on the Security **Overview** page.
* `securitySolution:newsFeedUrl`: The URL from which the security news feed content is retrieved.


## Set the maximum notes limit for alerts and events [max-notes-alerts-events]

The `securitySolution:maxUnassociatedNotes` field determines the maximum number of [notes](../../../solutions/security/investigate/notes.md) that you can attach to alerts and events. The maximum limit and default value is 1000.


## Access the event analyzer and session view from the event or alert details flyout [visualizations-in-flyout]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


The `securitySolution:enableVisualizationsInFlyout` setting allows you to access the event analyzer and Session View in the **Visualize** [tab](../../../solutions/security/detect-and-alert/view-detection-alert-details.md#expanded-visualizations-view) on the alert or event details flyout. This setting is turned off by default.


## Change the default search interval and data refresh time [security-advanced-settings-change-the-default-search-interval-and-data-refresh-time]

These settings determine the default time interval and refresh rate {{elastic-sec}} pages use to display data when you open the app:

* `securitySolution:timeDefaults`: Default time interval
* `securitySolution:refreshIntervalDefaults`: Default refresh rate

::::{note}
Refer to [Date Math](https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html) for information about the syntax. The UI [time filter](../../../explore-analyze/query-filter/filtering.md) overrides the default values.

::::



## Display reputation links on IP detail pages [ip-reputation-links]

On IP details pages (**Network** → ****IP address**), links to external sites for verifying the IP address’s reputation are displayed. By default, links to these sites are listed: [TALOS](https://talosintelligence.com/) and [VIRUSTOTAL](https://www.virustotal.com/).

The `securitySolution:ipReputationLinks` field determines which IP reputation sites are listed. To modify the listed sites, edit the field’s JSON array. These fields must be defined in each array element:

* `name`: The link’s UI display name.
* `url_template`: The link’s URL. It can include `{{ip}}`, which is placeholder for the IP address you are viewing on the **IP detail** page.

**Example**

Adds a link to [https://www.dnschecker.org](https://www.dnschecker.org) on **IP detail** pages:

```json
[
  { "name": "virustotal.com", "url_template": "https://www.virustotal.com/gui/search/{{ip}}" },
  { "name": "dnschecker.org", "url_template": "https://www.dnschecker.org/ip-location.php?ip={{ip}}" },
  { "name": "talosIntelligence.com", "url_template": "https://talosintelligence.com/reputation_center/lookup?search={{ip}}" }
]
```


## Show/hide related integrations in Rules page tables [show-related-integrations]

By default, Elastic prebuilt rules in the **Rules** and **Rule Monitoring** tables include a badge showing how many related integrations have been installed. Turn off `securitySolution:showRelatedIntegrations` to hide this in the rules tables (related integrations will still appear on rule details pages).


## Manage alert tag options [manage-alert-tags]

The `securitySolution:alertTags` field determines which options display in the alert tag menu. The default alert tag options are `Duplicate`, `False Positive`, and `Further investigation required`. You can update the alert tag menu by editing these options or adding more. To learn more about using alert tags, refer to [Apply and filter alert tags](../../../solutions/security/detect-and-alert/manage-detection-alerts.md#apply-alert-tags).
