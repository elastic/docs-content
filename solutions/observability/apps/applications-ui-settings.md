---
mapped_urls:
  - https://www.elastic.co/guide/en/observability/current/apm-settings-in-kibana.html
  - https://www.elastic.co/guide/en/serverless/current/observability-apm-kibana-settings.html

navigation_title: "Settings"
---

# Applications UI settings [observability-apm-kibana-settings]


::::{note}

The **Editor** role or higher is required to modify settings. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::

You can adjust Application settings to fine-tune your experience in the Applications UI.


## General settings [observability-apm-kibana-settings-general-settings]
```{applies_to}
stack: ga 9.1
```

To change APM settings, select **Settings** from any **Applications** page. The following settings are available.

`observability:apmAgentExplorerView`
:   [beta] Enables the Agent explorer view.

`observability:apmAWSLambdaPriceFactor`
:   Set the price per Gb-second for your AWS Lambda functions.

`observability:apmAWSLambdaRequestCostPerMillion`
:   Set the AWS Lambda cost per million requests.

`observability:apmEnableContinuousRollups`
:   [beta] When continuous rollups are enabled, the UI will select metrics with the appropriate resolution. On larger time ranges, lower resolution metrics will be used, which will improve loading times.

`observability:apmEnableServiceMetrics`
:   [beta] Enables the usage of service transaction metrics, which are low cardinality metrics that can be used by certain views like the service inventory for faster loading times.

`observability:apmLabsButton`
:   Enable or disable the APM Labs button — a quick way to enable and disable technical preview features in APM.

`observability:apmServiceGroupMaxNumberOfServices`
:   Limit the number of services in a given service group.

`observability:apmDefaultServiceEnvironment`
:   Set the default environment for APM. When left empty, data from all environments will be displayed by default.

`observability:apmEnableProfilingIntegration`
:   Enable the Universal Profiling integration in APM.

`observability:enableComparisonByDefault`
:   Enable the comparison feature by default.

`observability:enableInspectEsQueries`
:   When enabled, allows you to inspect Elasticsearch queries in API responses.

## APM Indices [apm-indices-settings]

The Applications UI uses data views to query APM indices. In non-serverless versions, change the default APM indices that the Applications UI queries by opening the Applications UI and select **Settings** → **Indices**. Index settings in the Applications UI take precedence over those set in `kibana.yml`.

APM indices are {{kib}} Spaces-aware; Changes to APM index settings will only apply to the currently enabled space. See [Control access to APM data](../../../solutions/observability/apps/control-access-to-apm-data.md) for more information.


## APM Labs [observability-apm-kibana-settings-apm-labs]

**APM Labs** allows you to easily try out new features that are technical preview.

To enable APM labs, go to **Applications** → **Settings** → **General settings** and toggle **Enable labs button in APM**. Select **Save changes** and refresh the page.

After enabling **APM Labs** select **Labs** in the toolbar to see the technical preview features available to try out.