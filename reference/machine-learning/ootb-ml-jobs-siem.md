---
mapped_pages:
  - https://www.elastic.co/guide/en/security/current/prebuilt-ml-jobs.html
  - https://www.elastic.co/guide/en/serverless/current/security-prebuilt-ml-jobs.html
  - https://www.elastic.co/guide/en/machine-learning/current/ootb-ml-jobs-siem.html
applies_to:
  stack: all
  serverless:
    security: all
products:
  - id: security
  - id: cloud-serverless
  - id: machine-learning
---

# Security {{anomaly-detect}} configurations

These {{anomaly-jobs}} automatically detect file system and network anomalies on your hosts. They appear in the **Anomaly Detection** interface of the {{security-app}} in {{kib}} when you have data that matches their configuration. For more information, refer to [Anomaly detection with machine learning](/solutions/security/advanced-entity-analytics/anomaly-detection.md).

::::{note}
:applies_to: {stack: ga 9.4+, serverless: ga}

In {{stack}} 9.4, [Entity Analytics](/solutions/security/advanced-entity-analytics.md) introduces fields for entity resolution. The {{ml-jobs}} created in this version and later are designed to leverage these fields.

* The affected {{ml-jobs}} include an `_ea` suffix in their names, as described in each module below.
* Previously installed {{ml-jobs}} and detection rules continue to run, allowing time to transition to the Entity Analytics fields.
* We recommend that you install the `_ea` {{ml-jobs}} and verify they are collecting data and generating anomalies before upgrading to the latest detection rules included in 9.4.
::::

## Security: Authentication [security-authentication]

Detect anomalous activity in your ECS-compatible authentication logs.

In the {{ml-app}} app, these configurations are available only when data exists that matches the query specified in the [manifest file](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/manifest.json). In the {{security-app}}, it looks in the {{data-source}} specified in the [`securitySolution:defaultIndex` advanced setting](kibana://reference/advanced-settings.md#securitysolution-defaultindex) for data that matches the query.

By default, when you create these jobs in the {{security-app}}, the job wizard uses a {{data-source}} that applies to multiple indices. If you use {{ml-app}} instead, create a similar [{{data-source}}](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/manifest.json#L7) and select it in the job wizard so the results match.

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`auth_high_count_logon_events_ea`
:   Looks for an unusually large spike in successful authentication events. This can be due to password spraying, user enumeration, or brute force activity.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_high_count_logon_events_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_high_count_logon_events_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`auth_high_count_logon_events`
:   Looks for an unusually large spike in successful authentication events. This can be due to password spraying, user enumeration, or brute force activity.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_high_count_logon_events.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_high_count_logon_events.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`auth_high_count_logon_events_for_a_source_ip_ea`
:   Looks for an unusually large spike in successful authentication events from a particular source IP address. This can be due to password spraying, user enumeration or brute force activity.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_high_count_logon_events_for_a_source_ip_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_high_count_logon_events_for_a_source_ip_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`auth_high_count_logon_events_for_a_source_ip`
:   Looks for an unusually large spike in successful authentication events from a particular source IP address. This can be due to password spraying, user enumeration or brute force activity.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_high_count_logon_events_for_a_source_ip.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_high_count_logon_events_for_a_source_ip.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`auth_high_count_logon_fails_ea`
:   Looks for an unusually large spike in authentication failure events. This can be due to password spraying, user enumeration, or brute force activity and may be a precursor to account takeover or credentialed access.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_high_count_logon_fails_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_high_count_logon_fails_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`auth_high_count_logon_fails`
:   Looks for an unusually large spike in authentication failure events. This can be due to password spraying, user enumeration, or brute force activity and may be a precursor to account takeover or credentialed access.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_high_count_logon_fails.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_high_count_logon_fails.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`auth_rare_hour_for_a_user_ea`
:   Looks for a user logging in at a time of day that is unusual for the user. This can be due to credentialed access through a compromised account when the user and the threat actor are in different time zones. In addition, unauthorized user activity often takes place during non-business hours.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_rare_hour_for_a_user_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_rare_hour_for_a_user_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`auth_rare_hour_for_a_user`
:   Looks for a user logging in at a time of day that is unusual for the user. This can be due to credentialed access through a compromised account when the user and the threat actor are in different time zones. In addition, unauthorized user activity often takes place during non-business hours.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_rare_hour_for_a_user.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_rare_hour_for_a_user.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`auth_rare_source_ip_for_a_user_ea`
:   Looks for a user logging in from an IP address that is unusual for the user. This can be due to credentialed access through a compromised account when the user and the threat actor are in different locations. An unusual source IP address for a username could also be due to lateral movement when a compromised account is used to pivot between hosts.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_rare_source_ip_for_a_user_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_rare_source_ip_for_a_user_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`auth_rare_source_ip_for_a_user`
:   Looks for a user logging in from an IP address that is unusual for the user. This can be due to credentialed access through a compromised account when the user and the threat actor are in different locations. An unusual source IP address for a username could also be due to lateral movement when a compromised account is used to pivot between hosts.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_rare_source_ip_for_a_user.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_rare_source_ip_for_a_user.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`auth_rare_user_ea`
:   Looks for an unusual user name in the authentication logs. An unusual user name is one way of detecting credentialed access by means of a new or dormant user account. A user account that is normally inactive, because the user has left the organization, which becomes active, may be due to credentialed access using a compromised account password. Threat actors will sometimes also create new users as a means of persisting in a compromised web application.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_rare_user_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_rare_user_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`auth_rare_user`
:   Looks for an unusual user name in the authentication logs. An unusual user name is one way of detecting credentialed access by means of a new or dormant user account. A user account that is normally inactive, because the user has left the organization, which becomes active, may be due to credentialed access using a compromised account password. Threat actors will sometimes also create new users as a means of persisting in a compromised web application.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/auth_rare_user.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_auth_rare_user.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`suspicious_login_activity_ea`
:   Detect unusually high number of authentication attempts.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/suspicious_login_activity_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_suspicious_login_activity_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`suspicious_login_activity`
:   Detect unusually high number of authentication attempts.

    **Supported integrations:** [System](integration-docs://reference/system/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/suspicious_login_activity.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_auth/ml/datafeed_suspicious_login_activity.json)

:::

::::


## Security: Azure Activity Logs [security-azure-activitylogs]

```yaml {applies_to}
stack: ga 9.3
serverless: ga
```

Detect suspicious activity recorded in your Azure Activity Logs.

In the {{ml-app}} app, these configurations are available only when data exists that matches the query specified in the [manifest file](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/manifest.json). In the {{security-app}}, it looks in the {{data-source}} specified in the [`securitySolution:defaultIndex` advanced setting](kibana://reference/advanced-settings.md#securitysolution-defaultindex) for data that matches the query.

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`azure_activitylogs_high_distinct_count_event_action_fail_ea`
:   Looks for a spike in the rate of an error message, which might indicate an impending service failure or potentially be byproducts of attempted or successful persistence, privilege escalation, defense evasion, discovery, lateral movement, or collection activity by a threat actor.

    **Supported integrations:** [Azure Activity Logs](integration-docs://reference/azure/activitylogs.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/azure_activitylogs_high_distinct_count_event_action_fail_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/datafeed_azure_activitylogs_high_distinct_count_event_action_fail_ea.json)

:::

:::{applies-item} {stack: ga =9.3}

`azure_activitylogs_high_distinct_count_event_action_on_failure`
:   Looks for a spike in the rate of an error message, which might indicate an impending service failure or potentially be byproducts of attempted or successful persistence, privilege escalation, defense evasion, discovery, lateral movement, or collection activity by a threat actor.

    **Supported integrations:** [Azure Activity Logs](integration-docs://reference/azure/activitylogs.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/azure_activitylogs_high_distinct_count_event_action_on_failure.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/datafeed_azure_activitylogs_high_distinct_count_event_action_on_failure.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`azure_activitylogs_rare_event_action_on_failure_ea`
:   Looks for unusual Azure activity event actions on failure. Rare and unusual errors might simply indicate an impending service failure but they can also be byproducts of attempted or successful persistence, privilege escalation, defense evasion, discovery, lateral movement, or collection activity by a threat actor.

    **Supported integrations:** [Azure Activity Logs](integration-docs://reference/azure/activitylogs.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/azure_activitylogs_rare_event_action_on_failure_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/datafeed_azure_activitylogs_rare_event_action_on_failure_ea.json)

:::

:::{applies-item} {stack: ga =9.3}

`azure_activitylogs_rare_event_action_on_failure`
:   Looks for unusual Azure activity event actions on failure. Rare and unusual errors might simply indicate an impending service failure but they can also be byproducts of attempted or successful persistence, privilege escalation, defense evasion, discovery, lateral movement, or collection activity by a threat actor.

    **Supported integrations:** [Azure Activity Logs](integration-docs://reference/azure/activitylogs.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/azure_activitylogs_rare_event_action_on_failure.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/datafeed_azure_activitylogs_rare_event_action_on_failure.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`azure_activitylogs_rare_event_action_for_a_city_ea`
:   Looks for Azure activity event actions that, while not inherently suspicious or atypical, are sourcing from a geolocation (city) that is unexpected. This can be the result of compromised credentials or keys.

    **Supported integrations:** [Azure Activity Logs](integration-docs://reference/azure/activitylogs.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/azure_activitylogs_rare_event_action_for_a_city_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/datafeed_azure_activitylogs_rare_event_action_for_a_city_ea.json)

:::

:::{applies-item} {stack: ga =9.3}

`azure_activitylogs_rare_event_action_for_a_city`
:   Looks for Azure activity event actions that, while not inherently suspicious or atypical, are sourcing from a geolocation (city) that is unexpected. This can be the result of compromised credentials or keys.

    **Supported integrations:** [Azure Activity Logs](integration-docs://reference/azure/activitylogs.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/azure_activitylogs_rare_event_action_for_a_city.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/datafeed_azure_activitylogs_rare_event_action_for_a_city.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`azure_activitylogs_rare_event_action_for_a_country_ea`
:   Looks for Azure activity event actions that, while not inherently suspicious or atypical, are sourcing from a geolocation (country) that is unexpected. This can be the result of compromised credentials or keys.

    **Supported integrations:** [Azure Activity Logs](integration-docs://reference/azure/activitylogs.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/azure_activitylogs_rare_event_action_for_a_country_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/datafeed_azure_activitylogs_rare_event_action_for_a_country_ea.json)

:::

:::{applies-item} {stack: ga =9.3}

`azure_activitylogs_rare_event_action_for_a_country`
:   Looks for Azure activity event actions that, while not inherently suspicious or atypical, are sourcing from a geolocation (country) that is unexpected. This can be the result of compromised credentials or keys.

    **Supported integrations:** [Azure Activity Logs](integration-docs://reference/azure/activitylogs.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/azure_activitylogs_rare_event_action_for_a_country.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/datafeed_azure_activitylogs_rare_event_action_for_a_country.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`azure_activitylogs_rare_event_action_for_a_user_email_ea`
:   Looks for Azure activity event actions that, while not inherently suspicious or atypical, are sourcing from a unique user identifier context that does not normally call the method. This can be the result of compromised credentials or keys as someone uses a valid account to persist, move laterally, or exfil data.

    **Supported integrations:** [Azure Activity Logs](integration-docs://reference/azure/activitylogs.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/azure_activitylogs_rare_event_action_for_a_user_email_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/datafeed_azure_activitylogs_rare_event_action_for_a_user_email_ea.json)

:::

:::{applies-item} {stack: ga =9.3}

`azure_activitylogs_rare_event_action_for_a_username`
:   Looks for Azure activity event actions that, while not inherently suspicious or atypical, are sourcing from a user context that does not normally call the method. This can be the result of compromised credentials or keys as someone uses a valid account to persist, move laterally, or exfil data.

    **Supported integrations:** [Azure Activity Logs](integration-docs://reference/azure/activitylogs.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/azure_activitylogs_rare_event_action_for_a_username.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_azure_activitylogs/ml/datafeed_azure_activitylogs_rare_event_action_for_a_username.json)

:::

::::


## Security: CloudTrail [security-cloudtrail-jobs]

Detect suspicious activity recorded in your CloudTrail logs.

In the {{ml-app}} app, these configurations are available only when data exists that matches the query specified in the [manifest file](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/manifest.json). In the {{security-app}}, it looks in the {{data-source}} specified in the [`securitySolution:defaultIndex` advanced setting](kibana://reference/advanced-settings.md#securitysolution-defaultindex) for data that matches the query.


`high_distinct_count_error_message`
:   Looks for a spike in the rate of an error message which may simply indicate an impending service failure but these can also be byproducts of attempted or successful persistence, privilege escalation, defense evasion, discovery, lateral movement, or collection activity by a threat actor.

    **Supported integrations:** [AWS](integration-docs://reference/aws/cloudtrail.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/high_distinct_count_error_message.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/datafeed_high_distinct_count_error_message.json)

`rare_error_code`
:   Looks for unusual errors. Rare and unusual errors may simply indicate an impending service failure but they can also be byproducts of attempted or successful persistence, privilege escalation, defense evasion, discovery, lateral movement, or collection activity by a threat actor.

    **Supported integrations:** [AWS](integration-docs://reference/aws/cloudtrail.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/rare_error_code.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/datafeed_rare_error_code.json)

`rare_method_for_a_city`
:   Looks for AWS API calls that, while not inherently suspicious or abnormal, are sourcing from a geolocation (city) that is unusual. This can be the result of compromised credentials or keys.

    **Supported integrations:** [AWS](integration-docs://reference/aws/cloudtrail.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/rare_method_for_a_city.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/datafeed_rare_method_for_a_city.json)

`rare_method_for_a_country`
:   Looks for AWS API calls that, while not inherently suspicious or abnormal, are sourcing from a geolocation (country) that is unusual. This can be the result of compromised credentials or keys.

    **Supported integrations:** [AWS](integration-docs://reference/aws/cloudtrail.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/rare_method_for_a_country.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/datafeed_rare_method_for_a_country.json)

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`rare_method_for_a_user_id_ea`
:   Looks for AWS API calls that, while not inherently suspicious or atypical, are sourcing from a user context that does not normally call the method. This can be the result of compromised credentials or keys as someone uses a valid account to persist, move laterally, or exfil data.

    **Supported integrations:** [AWS](integration-docs://reference/aws/cloudtrail.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/rare_method_for_a_user_id_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/datafeed_rare_method_for_a_user_id_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`rare_method_for_a_username`
:   Looks for AWS API calls that, while not inherently suspicious or atypical, are sourcing from a user context that does not normally call the method. This can be the result of compromised credentials or keys as someone uses a valid account to persist, move laterally, or exfil data.

    **Supported integrations:** [AWS](integration-docs://reference/aws/cloudtrail.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/rare_method_for_a_username.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_cloudtrail/ml/datafeed_rare_method_for_a_username.json)

:::

::::


## Security: GCP Audit logs [security-gcp-audit]

```yaml {applies_to}
stack: ga 9.3+
serverless: ga
```

Detect suspicious activity recorded in your GCP Audit logs.

In the {{ml-app}} app, these configurations are available only when data exists that matches the query specified in the [manifest file](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/manifest.json). In the {{security-app}}, it looks in the {{data-source}} specified in the [`securitySolution:defaultIndex` advanced setting](kibana://reference/advanced-settings.md#securitysolution-defaultindex) for data that matches the query.

:::{note}
:applies_to: {stack: ga 9.4+, serverless: ga}

Entity Analytics {{ml-jobs}} require GCP Audit integration version `2.47.2` or later.
:::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`gcp_audit_high_distinct_count_error_message_ea`
:   Looks for a spike in the rate of an action where the event outcome is a failure. Spikes might indicate an impending service failure but could also be byproducts of attempted or successful persistence, privilege escalation, defense evasion, discovery, lateral movement, or collection activity by a threat actor.

    **Supported integrations:** [GCP Audit](integration-docs://reference/gcp/audit.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/gcp_audit_high_distinct_count_error_message_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/datafeed_gcp_audit_high_distinct_count_error_message_ea.json)

:::

:::{applies-item} {stack: ga =9.3}

`gcp_audit_high_distinct_count_error_message`
:   Looks for a spike in the rate of an action where the event outcome is a failure. Spikes might indicate an impending service failure but could also be byproducts of attempted or successful persistence, privilege escalation, defense evasion, discovery, lateral movement, or collection activity by a threat actor.

    **Supported integrations:** [GCP Audit](integration-docs://reference/gcp/audit.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/gcp_audit_high_distinct_count_error_message.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/datafeed_gcp_audit_high_distinct_count_error_message.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`gcp_audit_rare_error_code_ea`
:   Looks for unusual errors. Rare and unusual errors might indicate an impending service failure but they can also be byproducts of attempted or successful persistence, privilege escalation, defense evasion, discovery, lateral movement, or collection activity by a threat actor.

    **Supported integrations:** [GCP Audit](integration-docs://reference/gcp/audit.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/gcp_audit_rare_error_code_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/datafeed_gcp_audit_rare_error_code_ea.json)

:::

:::{applies-item} {stack: ga =9.3}

`gcp_audit_rare_error_code`
:   Looks for unusual errors. Rare and unusual errors might indicate an impending service failure but they can also be byproducts of attempted or successful persistence, privilege escalation, defense evasion, discovery, lateral movement, or collection activity by a threat actor.

    **Supported integrations:** [GCP Audit](integration-docs://reference/gcp/audit.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/gcp_audit_rare_error_code.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/datafeed_gcp_audit_rare_error_code.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`gcp_audit_rare_method_for_a_city_ea`
:   Looks for GCP actions that, while not inherently suspicious or atypical, are sourcing from a geolocation (city) that is unexpected. This can be the result of compromised credentials or keys.

    **Supported integrations:** [GCP Audit](integration-docs://reference/gcp/audit.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/gcp_audit_rare_method_for_a_city_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/datafeed_gcp_audit_rare_method_for_a_city_ea.json)

:::

:::{applies-item} {stack: ga =9.3}

`gcp_audit_rare_method_for_a_city`
:   Looks for GCP actions that, while not inherently suspicious or atypical, are sourcing from a geolocation (city) that is unexpected. This can be the result of compromised credentials or keys.

    **Supported integrations:** [GCP Audit](integration-docs://reference/gcp/audit.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/gcp_audit_rare_method_for_a_city.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/datafeed_gcp_audit_rare_method_for_a_city.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`gcp_audit_rare_method_for_a_country_ea`
:   Looks for GCP actions calls that, while not inherently suspicious or atypical, are sourcing from a geolocation (country) that is unexpected. This can be the result of compromised credentials or keys.

    **Supported integrations:** [GCP Audit](integration-docs://reference/gcp/audit.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/gcp_audit_rare_method_for_a_country_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/datafeed_gcp_audit_rare_method_for_a_country_ea.json)

:::

:::{applies-item} {stack: ga =9.3}

`gcp_audit_rare_method_for_a_country`
:   Looks for GCP actions calls that, while not inherently suspicious or atypical, are sourcing from a geolocation (country) that is unexpected. This can be the result of compromised credentials or keys.

    **Supported integrations:** [GCP Audit](integration-docs://reference/gcp/audit.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/gcp_audit_rare_method_for_a_country.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/datafeed_gcp_audit_rare_method_for_a_country.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`gcp_audit_rare_method_for_a_user_email_ea`
:   Looks for GCP actions that, while not inherently suspicious or atypical, are sourcing from a user context that does not normally call the method. This can be the result of compromised credentials or keys as someone uses a valid account to persist, move laterally, or exfil data.

    **Supported integrations:** [GCP Audit](integration-docs://reference/gcp/audit.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/gcp_audit_rare_method_for_a_user_email_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/datafeed_gcp_audit_rare_method_for_a_user_email_ea.json)

:::

:::{applies-item} {stack: ga =9.3}

`gcp_audit_rare_method_for_a_client_user_email`
:   Looks for GCP actions that, while not inherently suspicious or atypical, are sourcing from a user context that does not normally call the method. This can be the result of compromised credentials or keys as someone uses a valid account to persist, move laterally, or exfil data.

    **Supported integrations:** [GCP Audit](integration-docs://reference/gcp/audit.md)

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/gcp_audit_rare_method_for_a_client_user_email.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_gcp_audit/ml/datafeed_gcp_audit_rare_method_for_a_client_user_email.json)

:::

::::


## Security: Host [security-host-jobs]

Anomaly detection jobs for host-based threat hunting and detection.

In the {{ml-app}} app, these configurations are available only when data exists that matches the query specified in the [manifest file](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_host/manifest.json). In the {{security-app}}, it looks in the {{data-source}} specified in the [`securitySolution:defaultIndex` advanced setting](kibana://reference/advanced-settings.md#securitysolution-defaultindex) for data that matches the query.

To access the host traffic anomalies dashboard in Kibana, go to: `Security -> Dashboards -> Host Traffic Anomalies`.

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`high_count_events_for_a_host_name_ea`
:   Detects sudden spikes in traffic associated with a host. This can be due to a range of security issues, such as a compromised system, DDoS attacks, malware infections, privilege escalation, or data exfiltration.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [System](integration-docs://reference/system/index.md)

    **Supported OS:** windows, linux, macOS

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_host/ml/high_count_events_for_a_host_name_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_host/ml/datafeed_high_count_events_for_a_host_name_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`high_count_events_for_a_host_name`
:   Looks for a sudden spike in host based traffic. This can be due to a range of security issues, such as a compromised system, DDoS attacks, malware infections, privilege escalation, or data exfiltration.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [System](integration-docs://reference/system/index.md)

    **Supported OS:** windows, linux, macOS

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_host/ml/high_count_events_for_a_host_name.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_host/ml/datafeed_high_count_events_for_a_host_name.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`low_count_events_for_a_host_name_ea`
:   Detects sudden drops in traffic associated with a host. This can be due to a range of security issues, such as a compromised system, a failed service, or a network misconfiguration.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [System](integration-docs://reference/system/index.md)

    **Supported OS:** windows, linux, macOS

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_host/ml/low_count_events_for_a_host_name_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_host/ml/datafeed_low_count_events_for_a_host_name_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`low_count_events_for_a_host_name`
:   Looks for a sudden drop in host based traffic. This can be due to a range of security issues, such as a compromised system, a failed service, or a network misconfiguration.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [System](integration-docs://reference/system/index.md)

    **Supported OS:** windows, linux, macOS

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_host/ml/low_count_events_for_a_host_name.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_host/ml/datafeed_low_count_events_for_a_host_name.json)

:::

::::


## Security: Linux [security-linux-jobs]

Anomaly detection jobs for Linux host-based threat hunting and detection.

In the {{ml-app}} app, these configurations are available only when data exists that matches the query specified in the [manifest file](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/manifest.json). In the {{security-app}}, it looks in the {{data-source}} specified in the [`securitySolution:defaultIndex` advanced setting](kibana://reference/advanced-settings.md#securitysolution-defaultindex) for data that matches the query.

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_anomalous_network_activity_ea`
:   Looks for unusual processes using the network which could indicate command-and-control, lateral movement, persistence, or data exfiltration activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_anomalous_network_activity_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_anomalous_network_activity_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_anomalous_network_activity`
:   Looks for unusual processes using the network which could indicate command-and-control, lateral movement, persistence, or data exfiltration activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_anomalous_network_activity.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_anomalous_network_activity.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_anomalous_network_port_activity_ea`
:   Looks for unusual destination port activity that could indicate command-and-control, persistence mechanism, or data exfiltration activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_anomalous_network_port_activity_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_anomalous_network_port_activity_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_anomalous_network_port_activity`
:   Looks for unusual destination port activity that could indicate command-and-control, persistence mechanism, or data exfiltration activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_anomalous_network_port_activity.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_anomalous_network_port_activity.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_anomalous_process_all_hosts_ea`
:   Looks for processes that are unusual to all Linux hosts. Such unusual processes may indicate unauthorized software, malware, or persistence mechanisms.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_anomalous_process_all_hosts_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_anomalous_process_all_hosts_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_anomalous_process_all_hosts`
:   Looks for processes that are unusual to all Linux hosts. Such unusual processes may indicate unauthorized software, malware, or persistence mechanisms.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_anomalous_process_all_hosts.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_anomalous_process_all_hosts.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_anomalous_user_name_ea`
:   Rare and unusual users that are not normally active may indicate unauthorized changes or activity by an unauthorized user which may be credentialed access or lateral movement.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_anomalous_user_name_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_anomalous_user_name_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_anomalous_user_name`
:   Rare and unusual users that are not normally active may indicate unauthorized changes or activity by an unauthorized user which may be credentialed access or lateral movement.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_anomalous_user_name.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_anomalous_user_name.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_network_configuration_discovery_ea`
:   Looks for commands related to system network configuration discovery from an unusual user context. This can be due to uncommon troubleshooting activity or due to a compromised account. A compromised account may be used by a threat actor to engage in system network configuration discovery to increase their understanding of connected networks and hosts. This information may be used to shape follow-up behaviors such as lateral movement or additional discovery.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_network_configuration_discovery_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_network_configuration_discovery_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_network_configuration_discovery`
:   Looks for commands related to system network configuration discovery from an unusual user context. This can be due to uncommon troubleshooting activity or due to a compromised account. A compromised account may be used by a threat actor to engage in system network configuration discovery to increase their understanding of connected networks and hosts. This information may be used to shape follow-up behaviors such as lateral movement or additional discovery.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_network_configuration_discovery.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_network_configuration_discovery.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_network_connection_discovery_ea`
:   Looks for commands related to system network connection discovery from an unusual user context. This can be due to uncommon troubleshooting activity or due to a compromised account. A compromised account may be used by a threat actor to engage in system network connection discovery to increase their understanding of connected services and systems. This information may be used to shape follow-up behaviors such as lateral movement or additional discovery.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_network_connection_discovery_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_network_connection_discovery_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_network_connection_discovery`
:   Looks for commands related to system network connection discovery from an unusual user context. This can be due to uncommon troubleshooting activity or due to a compromised account. A compromised account may be used by a threat actor to engage in system network connection discovery to increase their understanding of connected services and systems. This information may be used to shape follow-up behaviors such as lateral movement or additional discovery.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_network_connection_discovery.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_network_connection_discovery.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_rare_metadata_process_ea`
:   Looks for anomalous access to the metadata service by an unusual process. The metadata service may be targeted in order to harvest credentials or user data scripts containing secrets.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_rare_metadata_process_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_rare_metadata_process_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_rare_metadata_process`
:   Looks for anomalous access to the metadata service by an unusual process. The metadata service may be targeted in order to harvest credentials or user data scripts containing secrets.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_rare_metadata_process.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_rare_metadata_process.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_rare_metadata_user_ea`
:   Looks for anomalous access to the metadata service by an unusual user. The metadata service may be targeted in order to harvest credentials or user data scripts containing secrets.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_rare_metadata_user_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_rare_metadata_user_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_rare_metadata_user`
:   Looks for anomalous access to the metadata service by an unusual user. The metadata service may be targeted in order to harvest credentials or user data scripts containing secrets.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_rare_metadata_user.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_rare_metadata_user.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_rare_sudo_user_ea`
:   Looks for sudo activity from an unusual user context. Unusual user context changes can be due to privilege escalation.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_rare_sudo_user_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_rare_sudo_user_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_rare_sudo_user`
:   Looks for sudo activity from an unusual user context. Unusual user context changes can be due to privilege escalation.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_rare_sudo_user.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_rare_sudo_user.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_rare_user_compiler_ea`
:   Looks for compiler activity by a user context which does not normally run compilers. This can be ad-hoc software changes or unauthorized software deployment. This can also be due to local privilege elevation through locally run exploits or malware activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_rare_user_compiler_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_rare_user_compiler_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_rare_user_compiler`
:   Looks for compiler activity by a user context which does not normally run compilers. This can be ad-hoc software changes or unauthorized software deployment. This can also be due to local privilege elevation through locally run exploits or malware activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_rare_user_compiler.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_rare_user_compiler.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_system_information_discovery_ea`
:   Looks for commands related to system information discovery from an unusual user context. This can be due to uncommon troubleshooting activity or due to a compromised account. A compromised account may be used to engage in system information discovery to gather detailed information about system configuration and software versions. This may be a precursor to the selection of a persistence mechanism or a method of privilege elevation.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_system_information_discovery_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_system_information_discovery_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_system_information_discovery`
:   Looks for commands related to system information discovery from an unusual user context. This can be due to uncommon troubleshooting activity or due to a compromised account. A compromised account may be used to engage in system information discovery to gather detailed information about system configuration and software versions. This may be a precursor to the selection of a persistence mechanism or a method of privilege elevation.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_system_information_discovery.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_system_information_discovery.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_system_process_discovery_ea`
:   Looks for commands related to system process discovery from an unusual user context. This can be due to uncommon troubleshooting activity or due to a compromised account. A compromised account may be used to engage in system process discovery to increase their understanding of software applications running on a target host or network. This may be a precursor to the selection of a persistence mechanism or a method of privilege elevation.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_system_process_discovery_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_system_process_discovery_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_system_process_discovery`
:   Looks for commands related to system process discovery from an unusual user context. This can be due to uncommon troubleshooting activity or due to a compromised account. A compromised account may be used to engage in system process discovery to increase their understanding of software applications running on a target host or network. This may be a precursor to the selection of a persistence mechanism or a method of privilege elevation.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_system_process_discovery.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_system_process_discovery.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_linux_system_user_discovery_ea`
:   Looks for commands related to system user or owner discovery from an unusual user context. This can be due to uncommon troubleshooting activity or due to a compromised account. A compromised account may be used to engage in system owner or user discovery to identify currently active or primary users of a system. This may be a precursor to additional discovery, credential dumping, or privilege elevation activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_system_user_discovery_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_system_user_discovery_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_linux_system_user_discovery`
:   Looks for commands related to system user or owner discovery from an unusual user context. This can be due to uncommon troubleshooting activity or due to a compromised account. A compromised account may be used to engage in system owner or user discovery to identify currently active or primary users of a system. This may be a precursor to additional discovery, credential dumping, or privilege elevation activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_linux_system_user_discovery.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_linux_system_user_discovery.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_rare_process_by_host_linux_ea`
:   Looks for processes that are unusual to a particular Linux host. Such unusual processes may indicate unauthorized software, malware, or persistence mechanisms.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_rare_process_by_host_linux_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_rare_process_by_host_linux_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_rare_process_by_host_linux`
:   Looks for processes that are unusual to a particular Linux host. Such unusual processes may indicate unauthorized software, malware, or persistence mechanisms.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Auditd Manager](integration-docs://reference/auditd_manager/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/v3_rare_process_by_host_linux.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_linux/ml/datafeed_v3_rare_process_by_host_linux.json)

:::

::::


## Security: Network [security-network-jobs]

Detect anomalous network activity in your ECS-compatible network logs.

In the {{ml-app}} app, these configurations are available only when data exists that matches the query specified in the [manifest file](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_network/manifest.json). In the {{security-app}}, it looks in the {{data-source}} specified in the [`securitySolution:defaultIndex` advanced setting](kibana://reference/advanced-settings.md#securitysolution-defaultindex) for data that matches the query.

By default, when you create these jobs in the {{security-app}}, the job wizard uses a {{data-source}} that applies to multiple indices. If you use {{ml-app}} instead, create a similar [{{data-source}}](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_network/manifest.json#L7) and select it in the job wizard so the results match.

`high_count_by_destination_country`
:   Looks for an unusually large spike in network activity to one destination country in the network logs. This could be due to unusually large amounts of reconnaissance or enumeration traffic. Data exfiltration activity may also produce such a surge in traffic to a destination country which does not normally appear in network traffic or business work-flows. Malware instances and persistence mechanisms may communicate with command-and-control (C2) infrastructure in their country of origin, which may be an unusual destination country for the source network.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux, macOS

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_network/ml/high_count_by_destination_country.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_network/ml/datafeed_high_count_by_destination_country.json)

`high_count_network_denies`
:   Looks for an unusually large spike in network traffic that was denied by network ACLs or firewall rules. Such a burst of denied traffic is usually either 1) a misconfigured application or firewall or 2) suspicious or malicious activity. Unsuccessful attempts at network transit, in order to connect to command-and-control (C2), or engage in data exfiltration, may produce a burst of failed connections. This could also be due to unusually large amounts of reconnaissance or enumeration traffic.  Denial-of-service attacks or traffic floods may also produce such a surge in traffic.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux, macOS

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_network/ml/high_count_network_denies.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_network/ml/datafeed_high_count_network_denies.json)

`high_count_network_events`
:   Looks for an unusually large spike in network traffic. Such a burst of traffic, if not caused by a surge in business activity, can be due to suspicious or malicious activity. Large-scale data exfiltration may produce a burst of network traffic; this could also be due to unusually large amounts of reconnaissance or enumeration traffic.  Denial-of-service attacks or traffic floods may also produce such a surge in traffic.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux, macOS

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_network/ml/high_count_network_events.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_network/ml/datafeed_high_count_network_events.json)

`rare_destination_country`
:   Looks for an unusual destination country name in the network logs. This can be due to initial access, persistence, command-and-control, or exfiltration activity. For example, when a user clicks on a link in a phishing email or opens a malicious document, a request may be sent to download and run a payload from a server in a country which does not normally appear in network traffic or business work-flows. Malware instances and persistence mechanisms may communicate with command-and-control (C2) infrastructure in their country of origin, which may be an unusual destination country for the source network.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux, macOS

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_network/ml/rare_destination_country.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_network/ml/datafeed_rare_destination_country.json)


## Security: {{packetbeat}} [security-packetbeat-jobs]

Detect suspicious network activity in {{packetbeat}} data.

In the {{ml-app}} app, these configurations are available only when data exists that matches the query specified in the [manifest file](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/manifest.json). In the {{security-app}}, it looks in the {{data-source}} specified in the [`securitySolution:defaultIndex` advanced setting](kibana://reference/advanced-settings.md#securitysolution-defaultindex) for data that matches the query.

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`packetbeat_dns_tunneling_ea`
:   Looks for unusual DNS activity that could indicate command-and-control or data exfiltration activity.

    **Supported integrations:** [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/packetbeat_dns_tunneling_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/datafeed_packetbeat_dns_tunneling_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`packetbeat_dns_tunneling`
:   Looks for unusual DNS activity that could indicate command-and-control or data exfiltration activity.

    **Supported integrations:** [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/packetbeat_dns_tunneling.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/datafeed_packetbeat_dns_tunneling.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`packetbeat_rare_dns_question_ea`
:   Looks for unusual DNS activity that could indicate command-and-control activity.

    **Supported integrations:** [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/packetbeat_rare_dns_question_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/datafeed_packetbeat_rare_dns_question_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`packetbeat_rare_dns_question`
:   Looks for unusual DNS activity that could indicate command-and-control activity.

    **Supported integrations:** [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/packetbeat_rare_dns_question.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/datafeed_packetbeat_rare_dns_question.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`packetbeat_rare_server_domain_ea`
:   Looks for unusual HTTP or TLS destination domain activity that could indicate execution, persistence, command-and-control or data exfiltration activity.

    **Supported integrations:** [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/packetbeat_rare_server_domain_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/datafeed_packetbeat_rare_server_domain_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`packetbeat_rare_server_domain`
:   Looks for unusual HTTP or TLS destination domain activity that could indicate execution, persistence, command-and-control or data exfiltration activity.

    **Supported integrations:** [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/packetbeat_rare_server_domain.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/datafeed_packetbeat_rare_server_domain.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`packetbeat_rare_urls_ea`
:   Looks for unusual web browsing URL activity that could indicate execution, persistence, command-and-control or data exfiltration activity.

    **Supported integrations:** [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/packetbeat_rare_urls_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/datafeed_packetbeat_rare_urls_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`packetbeat_rare_urls`
:   Looks for unusual web browsing URL activity that could indicate execution, persistence, command-and-control or data exfiltration activity.

    **Supported integrations:** [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/packetbeat_rare_urls.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/datafeed_packetbeat_rare_urls.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`packetbeat_rare_user_agent_ea`
:   Looks for unusual HTTP user agent activity that could indicate execution, persistence, command-and-control or data exfiltration activity.

    **Supported integrations:** [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/packetbeat_rare_user_agent_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/datafeed_packetbeat_rare_user_agent_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`packetbeat_rare_user_agent`
:   Looks for unusual HTTP user agent activity that could indicate execution, persistence, command-and-control or data exfiltration activity.

    **Supported integrations:** [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/packetbeat_rare_user_agent.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_packetbeat/ml/datafeed_packetbeat_rare_user_agent.json)

:::

::::


## Security: Windows [security-windows-jobs]

Anomaly detection jobs for Windows host-based threat hunting and detection.

In the {{ml-app}} app, these configurations are available only when data exists that matches the query specified in the [manifest file](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/manifest.json). In the {{security-app}}, it looks in the {{data-source}} specified in the [`securitySolution:defaultIndex` advanced setting](kibana://reference/advanced-settings.md#securitysolution-defaultindex) for data that matches the query.

If there are additional requirements such as installing the Windows System Monitor (Sysmon) or auditing process creation in the Windows security event log, they are listed for each job.

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_rare_process_by_host_windows_ea`
:   Looks for processes that are unusual to a particular Windows host. Such unusual processes may indicate unauthorized software, malware, or persistence mechanisms.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_rare_process_by_host_windows_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_rare_process_by_host_windows_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_rare_process_by_host_windows`
:   Looks for processes that are unusual to a particular Windows host. Such unusual processes may indicate unauthorized software, malware, or persistence mechanisms.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_rare_process_by_host_windows.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_rare_process_by_host_windows.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_anomalous_network_activity_ea`
:   Looks for unusual processes using the network which could indicate command-and-control, lateral movement, persistence, or data exfiltration activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_network_activity_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_network_activity_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_anomalous_network_activity`
:   Looks for unusual processes using the network which could indicate command-and-control, lateral movement, persistence, or data exfiltration activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_network_activity.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_network_activity.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_anomalous_path_activity_ea`
:   Looks for activity in unusual paths that may indicate execution of malware or persistence mechanisms. Windows payloads often execute from user profile paths.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_path_activity_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_path_activity_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_anomalous_path_activity`
:   Looks for activity in unusual paths that may indicate execution of malware or persistence mechanisms. Windows payloads often execute from user profile paths.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_path_activity.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_path_activity.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_anomalous_process_all_hosts_ea`
:   Looks for processes that are unusual to all Windows hosts. Such unusual processes may indicate execution of unauthorized software, malware, or persistence mechanisms.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_process_all_hosts_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_process_all_hosts_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_anomalous_process_all_hosts`
:   Looks for processes that are unusual to all Windows hosts. Such unusual processes may indicate execution of unauthorized software, malware, or persistence mechanisms.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_process_all_hosts.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_process_all_hosts.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_anomalous_process_creation_ea`
:   Looks for unusual process relationships which may indicate execution of malware or persistence mechanisms.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_process_creation_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_process_creation_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_anomalous_process_creation`
:   Looks for unusual process relationships which may indicate execution of malware or persistence mechanisms.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_process_creation.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_process_creation.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_anomalous_script_ea`
:   Looks for unusual powershell scripts that may indicate execution of malware, or persistence mechanisms.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_script_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_script_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_anomalous_script`
:   Looks for unusual powershell scripts that may indicate execution of malware, or persistence mechanisms.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_script.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_script.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_anomalous_service_ea`
:   Looks for rare and unusual Windows service names which may indicate execution of unauthorized services, malware, or persistence mechanisms.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_service_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_service_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_anomalous_service`
:   Looks for rare and unusual Windows service names which may indicate execution of unauthorized services, malware, or persistence mechanisms.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_service.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_service.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_anomalous_user_name_ea`
:   Rare and unusual users that are not normally active may indicate unauthorized changes or activity by an unauthorized user which may be credentialed access or lateral movement.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_user_name_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_user_name_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_anomalous_user_name`
:   Rare and unusual users that are not normally active may indicate unauthorized changes or activity by an unauthorized user which may be credentialed access or lateral movement.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_anomalous_user_name.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_anomalous_user_name.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_rare_metadata_process_ea`
:   Looks for anomalous access to the metadata service by an unusual process. The metadata service may be targeted in order to harvest credentials or user data scripts containing secrets.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_rare_metadata_process_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_rare_metadata_process_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_rare_metadata_process`
:   Looks for anomalous access to the metadata service by an unusual process. The metadata service may be targeted in order to harvest credentials or user data scripts containing secrets.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_rare_metadata_process.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_rare_metadata_process.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_rare_metadata_user_ea`
:   Looks for anomalous access to the metadata service by an unusual user. The metadata service may be targeted in order to harvest credentials or user data scripts containing secrets.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_rare_metadata_user_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_rare_metadata_user_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_rare_metadata_user`
:   Looks for anomalous access to the metadata service by an unusual user. The metadata service may be targeted in order to harvest credentials or user data scripts containing secrets.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_rare_metadata_user.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_rare_metadata_user.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_rare_user_runas_event_ea`
:   Unusual user context switches can be due to privilege escalation.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_rare_user_runas_event_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_rare_user_runas_event_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_rare_user_runas_event`
:   Unusual user context switches can be due to privilege escalation.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_rare_user_runas_event.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_rare_user_runas_event.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_rare_user_type10_remote_login_ea`
:   Unusual RDP (remote desktop protocol) user logins can indicate account takeover or credentialed access.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_rare_user_type10_remote_login_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_rare_user_type10_remote_login_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_rare_user_type10_remote_login`
:   Unusual RDP (remote desktop protocol) user logins can indicate account takeover or credentialed access.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_rare_user_type10_remote_login.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_rare_user_type10_remote_login.json)

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`v3_windows_rare_script_ea`
:   Looks for rare powershell scripts that may indicate execution of malware, or persistence mechanisms using hash.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_rare_script_ea.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_rare_script_ea.json)

:::

:::{applies-item} {stack: ga 9.0-9.3}

`v3_windows_rare_script`
:   Looks for rare powershell scripts that may indicate execution of malware, or persistence mechanisms using hash.

    **Supported integrations:** [Windows](integration-docs://reference/windows/index.md), [Winlogbeat](beats://reference/winlogbeat/index.md)

    **Supported OS:** windows

    **Job (JSON):** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/v3_windows_rare_script.json)

    **Datafeed:** [code](https://github.com/elastic/kibana/blob/main/x-pack/platform/plugins/shared/ml/server/models/data_recognizer/modules/security_windows/ml/datafeed_v3_windows_rare_script.json)

:::

::::


## Security: Elastic Integrations [security-integrations-jobs]

[Elastic Integrations](integration-docs://reference/index.md) are a streamlined way to add Elastic assets to your environment, such as data ingestion, transforms, and in this case, {{ml}} capabilities for Security.

The following Integrations use {{ml}} to analyze patterns of user and entity behavior, and help detect and alert when there is related suspicious activity in your environment.

* [Data Exfiltration Detection](integration-docs://reference/ded/index.md)
* [Domain Generation Algorithm Detection](integration-docs://reference/dga/index.md)
* [Lateral Movement Detection](integration-docs://reference/lmd/index.md)
* [Living off the Land Attack Detection](integration-docs://reference/problemchild/index.md)
* {applies_to}`stack: ga 9.4+` {applies_to}`serverless: ga` [Privileged Access Detection](integration-docs://reference/pad.md)

### Data Exfiltration Detection (DED)

{{ml-cap}} package to detect data exfiltration in your network and file data. Refer to the [subscription page](https://www.elastic.co/subscriptions) to learn more about the required subscription.

To download, refer to the [documentation](integration-docs://reference/ded/index.md).

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`ded_high_sent_bytes_destination_geo_country_iso_code_ea`
:   Detects data exfiltration to an unusual geo-location (by country iso code).

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

:::

:::{applies-item} {stack: ga 9.0-9.3}

`ded_high_sent_bytes_destination_geo_country_iso_code`
:   Detects data exfiltration to an unusual geo-location (by country iso code).

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`ded_high_sent_bytes_destination_ip_ea`
:   Detects data exfiltration to an unusual geo-location (by IP address).

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

:::

:::{applies-item} {stack: ga 9.0-9.3}

`ded_high_sent_bytes_destination_ip`
:   Detects data exfiltration to an unusual geo-location (by IP address).

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`ded_high_sent_bytes_destination_port_ea`
:   Detects data exfiltration to an unusual destination port.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

:::

:::{applies-item} {stack: ga 9.0-9.3}

`ded_high_sent_bytes_destination_port`
:   Detects data exfiltration to an unusual destination port.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`ded_high_sent_bytes_destination_region_name_ea`
:   Detects data exfiltration to an unusual geo-location (by region name).

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

:::

:::{applies-item} {stack: ga 9.0-9.3}

`ded_high_sent_bytes_destination_region_name`
:   Detects data exfiltration to an unusual geo-location (by region name).

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`ded_high_bytes_written_to_external_device_ea`
:   Detects data exfiltration activity by identifying high bytes written to an external device.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`ded_high_bytes_written_to_external_device`
:   Detects data exfiltration activity by identifying high bytes written to an external device.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`ded_rare_process_writing_to_external_device_ea`
:   Detects data exfiltration activity by identifying a file write started by a rare process to an external device.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`ded_rare_process_writing_to_external_device`
:   Detects data exfiltration activity by identifying a file write started by a rare process to an external device.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`ded_high_bytes_written_to_external_device_airdrop_ea`
:   Detects data exfiltration activity by identifying high bytes written to an external device using Airdrop.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** macOS

:::

:::{applies-item} {stack: ga 9.0-9.3}

`ded_high_bytes_written_to_external_device_airdrop`
:   Detects data exfiltration activity by identifying high bytes written to an external device using Airdrop.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** macOS

:::

::::


The job configurations and datafeeds can be found [here](https://github.com/elastic/integrations/blob/main/packages/ded/kibana/ml_module/ded-ml.json).

### Domain Generation Algorithm (DGA) Detection

{{ml-cap}} solution package to detect domain generation algorithm (DGA) activity in your network data. Refer to the [subscription page](https://www.elastic.co/subscriptions) to learn more about the required subscription.

To download, refer to the [documentation](integration-docs://reference/dga/index.md).

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`dga_high_sum_probability_ea`
:   Detect domain generation algorithm (DGA) activity in your network data.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

:::

:::{applies-item} {stack: ga 9.0-9.3}

`dga_high_sum_probability`
:   Detect domain generation algorithm (DGA) activity in your network data.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Network Packet Capture](integration-docs://reference/network_traffic/index.md), [Packetbeat](beats://reference/packetbeat/index.md)

    **Supported OS:** windows, linux

:::

::::


The job configurations and datafeeds can be found [here](https://github.com/elastic/integrations/blob/main/packages/dga/kibana/ml_module/dga-ml.json).

### Lateral Movement Detection (LMD)

{{ml-cap}} package to detect lateral movement based on file transfer activity and Windows RDP events. Refer to the [subscription page](https://www.elastic.co/subscriptions) to learn more about the required subscription.

To download, refer to the [documentation](integration-docs://reference/lmd/index.md).

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`lmd_high_count_remote_file_transfer_ea`
:   Detects unusually high file transfers to a remote host in the network.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows, linux

:::

:::{applies-item} {stack: ga 9.0-9.3}

`lmd_high_count_remote_file_transfer`
:   Detects unusually high file transfers to a remote host in the network.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows, linux

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`lmd_high_file_size_remote_file_transfer_ea`
:   Detects unusually high size of files shared with a remote host in the network.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows, linux

:::

:::{applies-item} {stack: ga 9.0-9.3}

`lmd_high_file_size_remote_file_transfer`
:   Detects unusually high size of files shared with a remote host in the network.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows, linux

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`lmd_rare_file_extension_remote_transfer_ea`
:   Detects data exfiltration to an unusual destination port.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows, linux

:::

:::{applies-item} {stack: ga 9.0-9.3}

`lmd_rare_file_extension_remote_transfer`
:   Detects data exfiltration to an unusual destination port.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows, linux

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`lmd_rare_file_path_remote_transfer_ea`
:   Detects unusual folders and directories on which a file is transferred.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows, linux

:::

:::{applies-item} {stack: ga 9.0-9.3}

`lmd_rare_file_path_remote_transfer`
:   Detects unusual folders and directories on which a file is transferred.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows, linux

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`lmd_high_mean_rdp_session_duration_ea`
:   Detects unusually high mean of RDP session duration.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`lmd_high_mean_rdp_session_duration`
:   Detects unusually high mean of RDP session duration.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`lmd_high_var_rdp_session_duration_ea`
:   Detects unusually high variance in RDP session duration.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`lmd_high_var_rdp_session_duration`
:   Detects unusually high variance in RDP session duration.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`lmd_high_sum_rdp_number_of_processes_ea`
:   Detects unusually high number of processes started in a single RDP session.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`lmd_high_sum_rdp_number_of_processes`
:   Detects unusually high number of processes started in a single RDP session.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`lmd_unusual_time_weekday_rdp_session_start_ea`
:   Detects an RDP session started at an unusual time or weekday.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`lmd_unusual_time_weekday_rdp_session_start`
:   Detects an RDP session started at an unusual time or weekday.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`lmd_high_rdp_distinct_count_source_ip_for_destination_ea`
:   Detects a high count of source IPs making an RDP connection with a single destination IP.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`lmd_high_rdp_distinct_count_source_ip_for_destination`
:   Detects a high count of source IPs making an RDP connection with a single destination IP.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`lmd_high_rdp_distinct_count_destination_ip_for_source_ea`
:   Detects a high count of destination IPs establishing an RDP connection with a single source IP.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`lmd_high_rdp_distinct_count_destination_ip_for_source`
:   Detects a high count of destination IPs establishing an RDP connection with a single source IP.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`lmd_high_mean_rdp_process_args_ea`
:   Detects unusually high number of process arguments in an RDP session.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`lmd_high_mean_rdp_process_args`
:   Detects unusually high number of process arguments in an RDP session.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

:::

::::


The job configurations and datafeeds can be found [here](https://github.com/elastic/integrations/blob/main/packages/lmd/kibana/ml_module/lmd-ml.json).

### Living off the Land Attack (LotL) Detection

{{ml-cap}} solution package to detect Living off the Land (LotL) attacks in your environment. Refer to the [subscription page](https://www.elastic.co/subscriptions) to learn more about the required subscription. (Also known as ProblemChild).

To download, refer to the [documentation](integration-docs://reference/problemchild/index.md).

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`problem_child_rare_process_by_host_ea`
:   Looks for a process that has been classified as malicious on a host that does not commonly manifest malicious process activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`problem_child_rare_process_by_host`
:   Looks for a process that has been classified as malicious on a host that does not commonly manifest malicious process activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`problem_child_high_sum_by_host_ea`
:   Looks for a set of one or more malicious child processes on a single host.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`problem_child_high_sum_by_host`
:   Looks for a set of one or more malicious child processes on a single host.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`problem_child_rare_process_by_user_ea`
:   Looks for a process that has been classified as malicious where the user context is unusual and does not commonly manifest malicious process activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`problem_child_rare_process_by_user`
:   Looks for a process that has been classified as malicious where the user context is unusual and does not commonly manifest malicious process activity.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`problem_child_rare_process_by_parent_ea`
:   Looks for rare malicious child processes spawned by a parent process.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`problem_child_rare_process_by_parent`
:   Looks for rare malicious child processes spawned by a parent process.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`problem_child_high_sum_by_user_ea`
:   Looks for a set of one or more malicious processes, started by the same user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`problem_child_high_sum_by_user`
:   Looks for a set of one or more malicious processes, started by the same user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

::::

::::{applies-switch}

:::{applies-item} {stack: ga 9.4+, serverless: ga}

`problem_child_high_sum_by_parent_ea`
:   Looks for a set of one or more malicious child processes spawned by the same parent process.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

:::{applies-item} {stack: ga 9.0-9.3}

`problem_child_high_sum_by_parent`
:   Looks for a set of one or more malicious child processes spawned by the same parent process.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md), [Windows](integration-docs://reference/windows/index.md)

    **Supported OS:** windows

:::

::::


The job configurations and datafeeds can be found [here](https://github.com/elastic/integrations/blob/main/packages/problemchild/kibana/ml_module/problemchild-ml.json).

### Privileged Access Detection (PAD)

```yaml {applies_to}
stack: ga 9.4+
serverless: ga
```

{{ml-cap}} package to detect anomalous privileged access activity in Windows, Linux and Okta logs. Refer to the [subscription page](https://www.elastic.co/subscriptions) to learn more about the required subscription.

To download, refer to the [documentation](integration-docs://reference/pad.md).

`pad_windows_high_count_special_logon_events_ea`
:   Detects unusually high special logon events initiated by a user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

`pad_windows_high_count_special_privilege_use_events_ea`
:   Detects unusually high special privilege use events initiated by a user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

`pad_windows_high_count_group_management_events_ea`
:   Detects unusually high security group management events initiated by a user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

`pad_windows_high_count_user_account_management_events_ea`
:   Detects unusually high security user account management events initiated by a user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

`pad_windows_rare_privilege_assigned_to_user_ea`
:   Detects an unusual privilege type assigned to a user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

`pad_windows_rare_group_name_by_user_ea`
:   Detects an unusual group name accessed by a user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

`pad_windows_rare_device_by_user_ea`
:   Detects an unusual device accessed by a user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

`pad_windows_rare_source_ip_by_user_ea`
:   Detects an unusual source IP address accessed by a user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

`pad_windows_rare_region_name_by_user_ea`
:   Detects an unusual region name for a user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** windows

`pad_linux_high_count_privileged_process_events_by_user_ea`
:   Detects a spike in privileged commands executed by a user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** linux

`pad_linux_rare_process_executed_by_user_ea`
:   Detects a rare process executed by a user.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** linux

`pad_linux_high_median_process_command_line_entropy_by_user_ea`
:   Detects process command lines executed by a user with an abnormally high median entropy value.

    **Supported integrations:** [{{elastic-defend}}](integration-docs://reference/endpoint/index.md)

    **Supported OS:** linux

`pad_okta_spike_in_group_membership_changes_ea`
:   Detects spike in group membership change events by a user.

    **Supported integrations:** [Okta](integration-docs://reference/okta/index.md)

`pad_okta_spike_in_user_lifecycle_management_changes_ea`
:   Detects spike in user lifecycle management change events by a user.

    **Supported integrations:** [Okta](integration-docs://reference/okta/index.md)

`pad_okta_spike_in_group_privilege_changes_ea`
:   Detects spike in group privilege change events by a user.

    **Supported integrations:** [Okta](integration-docs://reference/okta/index.md)

`pad_okta_spike_in_group_application_assignment_change_ea`
:   Detects spike in group application assignment change events by a user.

    **Supported integrations:** [Okta](integration-docs://reference/okta/index.md)

`pad_okta_spike_in_group_lifecycle_changes_ea`
:   Detects spike in group lifecycle change events by a user.

    **Supported integrations:** [Okta](integration-docs://reference/okta/index.md)

`pad_okta_high_sum_concurrent_sessions_by_user_ea`
:   Detects an unusual sum of active sessions started by a user.

    **Supported integrations:** [Okta](integration-docs://reference/okta/index.md)

`pad_okta_rare_source_ip_by_user_ea`
:   Detects an unusual source IP address accessed by a user.

    **Supported integrations:** [Okta](integration-docs://reference/okta/index.md)

`pad_okta_rare_region_name_by_user_ea`
:   Detects an unusual region name for a user.

    **Supported integrations:** [Okta](integration-docs://reference/okta/index.md)

`pad_okta_rare_host_name_by_user_ea`
:   Detects an unusual host name for a user.

    **Supported integrations:** [Okta](integration-docs://reference/okta/index.md)


The job configurations and datafeeds can be found [here](https://github.com/elastic/integrations/blob/main/packages/pad/kibana/ml_module/pad-ml.json).
