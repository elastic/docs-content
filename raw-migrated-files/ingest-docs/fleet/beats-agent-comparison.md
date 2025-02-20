# {{beats}} and {{agent}} capabilities [beats-agent-comparison]

Elastic provides two main ways to send data to {{es}}:

* **{{beats}}** are lightweight data shippers that send operational data to {{es}}. Elastic provides separate {{beats}} for different types of data, such as logs, metrics, and uptime. Depending on what data you want to collect, you may need to install multiple shippers on a single host.
* **{{agent}}** is a single agent for logs, metrics, security data, and threat prevention. The {{agent}} can be deployed in two different modes:

    * **Managed by {{fleet}}** — The {{agent}} policies and lifecycle are centrally managed by the {{fleet}} app in {{kib}}. The Integrations app also lets you centrally add integrations with other popular services and systems. This is the recommended option for most users.
    * **Standalone mode** — All policies are applied to the {{agent}} manually as a YAML file. This is intended for more advanced users. See [Install standalone {{agent}}s](https://www.elastic.co/guide/en/fleet/current/install-standalone-elastic-agent.html) for more information.


The method you use depends on your use case, which features you need, and whether you want to centrally manage your agents.

{{beats}} and {{agent}} can both send data directly to {{es}} or via {{ls}}, where you can further process and enhance the data, before visualizing it in {{kib}}.

This article summarizes the features and functionality you need to be aware of before adding new {{agent}}s or replacing your current {{beats}} with {{agent}}s. Starting in version 7.14.0, {{agent}} is generally available (GA).


## Choosing between {{agent}} and {{beats}} [choosing-between-agent-and-beats]

{{agent}} is a single binary designed to provide the same functionality that the various {{beats}} provide today. However, some functionality gaps are being addressed as we strive to reach feature parity.

The following steps will help you determine if {{agent}} can support your use case:

1. Determine if the integrations you need are supported and Generally Available (GA) on {{agent}}. To find out if an integration is GA, see the [{{integrations}} quick reference table](https://docs.elastic.co/en/integrations/all_integrations).
2. If the integration is available, check [Supported outputs](#supported-outputs-beats-and-agent) to see whether the required output is also supported.
3. Review [Capabilities comparison](#additional-capabilities-beats-and-agent) to determine if any features required by your deployment are supported. {{agent}} should support most of the features available on {{beats}} and is updated for each release.

If you are satisfied with all three steps, then {{agent}} is suitable for your deployment. However, if any steps fail your assessment, you should continue using {{beats}}, and review future updates or contact us in the [discuss forum](https://discuss.elastic.co/).


## Supported inputs [supported-inputs-beats-and-agent]

For {{agent}}s that are centrally managed by {{fleet}}, data collection is further simplified and defined by integrations. In this model, the decision on the inputs is driven by the integration you want to collect data from. The complexity of configuration details of various inputs is driven centrally by {{fleet}} and specifically by the integrations.

To find out if an integration is GA, see the [{{integrations}} quick reference table](https://docs.elastic.co/en/integrations/all_integrations).


## Supported outputs [supported-outputs-beats-and-agent]

The following table shows the outputs supported by the {{agent}} in 9.0.0-beta1:

::::{note}
{{elastic-defend}} and APM Server have a different output matrix.
::::


| Output | {{beats}} | {{fleet}}-managed {{agent}} | Standalone {{agent}} |
| --- | --- | --- | --- |
| {{es}} Service | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") |
| {{es}} | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") |
| {{ls}} | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") |
| Kafka | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") |
| Remote {{es}} | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") |
| Redis | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") | ![no](../../../images/fleet-red-x.svg "") |
| File | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") | ![no](../../../images/fleet-red-x.svg "") |
| Console | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") | ![no](../../../images/fleet-red-x.svg "") |


## Supported configurations [supported-configurations]

| {{beats}} configuration | {{agent}} support |
| --- | --- |
| [Modules](https://www.elastic.co/guide/en/beats/filebeat/current/configuration-filebeat-modules.html) | Supported via integrations. |
| [Input setting overrides](https://www.elastic.co/guide/en/beats/filebeat/current/advanced-settings.html) | Not configurable. Set to default values. |
| [General settings](https://www.elastic.co/guide/en/beats/filebeat/current/configuration-general-options.html) | Many of these global settings are now internal to the agent and for properoperations should not be modified. |
| [Project paths](https://www.elastic.co/guide/en/beats/filebeat/current/configuration-path.html) | {{agent}} configures these paths to provide a simpler and more streamlinedconfiguration experience. |
| [External configuration file loading](https://www.elastic.co/guide/en/beats/filebeat/current/filebeat-configuration-reloading.html) | Config is distributed via policy. |
| [Live reloading](https://www.elastic.co/guide/en/beats/filebeat/current/_live_reloading.html) | Related to the config file reload. |
| [Outputs](https://www.elastic.co/guide/en/beats/filebeat/current/configuring-output.html) | Configured through {{fleet}}. See [Supported outputs](#supported-outputs-beats-and-agent). |
| [SSL](https://www.elastic.co/guide/en/beats/filebeat/current/configuration-ssl.html) | Supported |
| [{{ilm-cap}}](https://www.elastic.co/guide/en/beats/filebeat/current/ilm.html) | Enabled by default although the Agent uses [data streams](https://www.elastic.co/guide/en/fleet/current/data-streams.html). |
| [{{es}} index template loading](https://www.elastic.co/guide/en/beats/filebeat/current/configuration-template.html) | No longer applicable |
| [{{kib}} endpoint](https://www.elastic.co/guide/en/beats/filebeat/current/setup-kibana-endpoint.html) | New {{agent}} workflow doesn’t need this. |
| [{{kib}} dashboard loading](https://www.elastic.co/guide/en/beats/filebeat/current/configuration-dashboards.html) | New {{agent}} workflow doesn’t need this. |
| [Processors](https://www.elastic.co/guide/en/beats/filebeat/current/defining-processors.html) | Processors can be defined at the integration level. Global processors, configured at the policy level, are currently under consideration. |
| [Autodiscover](https://www.elastic.co/guide/en/beats/filebeat/current/configuration-autodiscover.html) | Autodiscover is facilitated through [dynamic inputs](https://www.elastic.co/guide/en/fleet/current/dynamic-input-configuration.html). {{agent}} does not support hints-based autodiscovery. |
| [Internal queues](https://www.elastic.co/guide/en/beats/filebeat/current/configuring-internal-queue.html) | {{fleet}}-managed {{agent}} and Standalone {{agent}} both support configuration of the internal memoryqueues by an end user. Neither support configuration of the internal disk queues by an end user. |
| [Load balance output hosts](https://www.elastic.co/guide/en/beats/filebeat/current/elasticsearch-output.html#_loadbalance) | Within the {{fleet}} UI, you can add YAML settings to configure multiple hostsper output type, which enables load balancing. |
| [Logging](https://www.elastic.co/guide/en/beats/filebeat/current/configuration-logging.html) | Supported |
| [HTTP Endpoint](https://www.elastic.co/guide/en/beats/filebeat/current/http-endpoint.html) | Supported |
| [Regular expressions](https://www.elastic.co/guide/en/beats/filebeat/current/regexp-support.html) | Supported |


## Capabilities comparison [additional-capabilities-beats-and-agent]

The following table shows a comparison of capabilities supported by {{beats}} and the {{agent}} in 9.0.0-beta1:

| Item | {{beats}} | {{fleet}}-managed {{agent}} | Standalone {{agent}} | Description |
| --- | --- | --- | --- | --- |
| Single agent for all use cases | ![no](../../../images/fleet-red-x.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | {{agent}} provides logs, metrics, and more. You’d need to install multiple {{beats}} for these use cases. |
| Install integrations from web UI or API | ![no](../../../images/fleet-red-x.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | {{agent}} integrations are installed with a convenient web UI or API, but {{beats}} modules are installed with a CLI. This installs {{es}} assets such as index templates and ingest pipelines, and {{kib}} assets such as dashboards. |
| Configure from web UI or API | ![no](../../../images/fleet-red-x.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") (optional) | {{fleet}}-managed {{agent}} integrations can be configured in the web UI or API. Standalone {{agent}} can use the web UI, API, or YAML. {{beats}} can only be configured via YAML files. |
| Central, remote agent policy management | ![no](../../../images/fleet-red-x.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") | {{agent}} policies can be centrally managed through {{fleet}}. You have to manage {{beats}} configuration yourself or with a third-party solution. |
| Central, remote agent binary upgrades | ![no](../../../images/fleet-red-x.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") | {{agent}}s can be remotely upgraded through {{fleet}}. You have to upgrade {{beats}} yourself or with a third-party solution. |
| Add {{kib}} and {{es}} assets for a single integration or module | ![no](../../../images/fleet-red-x.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | {{agent}} integrations allow you to add {{kib}} and {{es}} assets for a single integration at a time. {{beats}} installs hundreds of assets for all modules at once. |
| Auto-generated {{es}} API keys | ![no](../../../images/fleet-red-x.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") | {{fleet}} can automatically generate API keys with limited permissions for each {{agent}}, which can be individually revoked. Standalone {{agent}} and {{beats}} require you to create and manage credentials, and users often share them across hosts. |
| Auto-generate minimal {{es}} permissions | ![no](../../../images/fleet-red-x.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") | {{fleet}} can automatically give {{agent}}s minimal output permissions based on the inputs running. With standalone {{agent}} and {{beats}}, users often give overly broad permissions because it’s more convenient. |
| Data streams support | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | Both {{beats}} (default as of version 8.0) and {{agent}}s use [data streams](https://www.elastic.co/guide/en/fleet/current/data-streams.html) with easier index life cycle management and the [data stream naming scheme](https://www.elastic.co/blog/an-introduction-to-the-elastic-data-stream-naming-scheme). |
| Variables and input conditions | ![no](../../../images/fleet-red-x.svg "") | ![yes](../../../images/fleet-green-check.svg "") (limited) | ![yes](../../../images/fleet-green-check.svg "") | {{agent}} offers [variables and input conditions](https://www.elastic.co/guide/en/fleet/current/dynamic-input-configuration.html) to dynamically adjust based on the local host environment. Users can configure these directly in YAML for standalone {{agent}} or using the {{fleet}} API for {{fleet}}-managed {{agent}}. The Integrations app allows users to enter variables, and we are considering a [UI to edit conditions](https://github.com/elastic/kibana/issues/108525). {{beats}} only offers static configuration. |
| Allow non-superusers to manage assets and agents | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") (it’s optional) | Starting with version 8.1.0, a superuser role is no longer required to use the {{fleet}} and Integrations apps and corresponding APIs. These apps are optional for standalone {{agent}}. {{beats}} offers [finer grained](https://www.elastic.co/guide/en/beats/filebeat/current/feature-roles.html) roles. |
| Air-gapped network support | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") (with Limits) | ![yes](../../../images/fleet-green-check.svg "") | The {{integrations}} and {{fleet}} apps can be deployed in an air-gapped environment [self-managed deployment of the {{package-registry}}](https://www.elastic.co/guide/en/fleet/current/air-gapped.html#air-gapped-diy-epr). {{fleet}}-managed {{agent}}s require a connection to our artifact repository for agent binary upgrades. However the policy can be modified to have agents point to a local server in order to fetch the agent binary. |
| Run without root on host | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | {{fleet}}-managed {{agent}}s, Standalone {{agent}}s, and {{beats}} require root permission only if they’re configured to capture data that requires that level of permission. |
| Multiple outputs | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | The policy for a single {{fleet}}-managed {{agent}} can specify multiple outputs. |
| Separate monitoring cluster | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | ![yes](../../../images/fleet-green-check.svg "") | {{fleet}}-managed {{agent}}s, Standalone {{agent}} and {{beats}} can send to a remote monitoring cluster. |
| Secret management | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") | ![no](../../../images/fleet-red-x.svg "") | {{agent}} stores credentials in the agent policy. We are considering adding [keystore support](https://github.com/elastic/integrations/issues/244). {{beats}} allows users to access credentials in a local [keystore](https://www.elastic.co/guide/en/beats/filebeat/current/keystore.html). |
| Progressive or canary deployments | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") | ![yes](../../../images/fleet-green-check.svg "") | {{fleet}} does not have a feature to deploy an {{agent}} policy update progressively but we are considering [improved support](https://github.com/elastic/kibana/issues/108267). With standalone {{agent}} and {{beats}} you can deploy configuration files progressively using third party solutions. |
| Multiple configurations per host | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") (uses input conditions instead) | ![no](../../../images/fleet-red-x.svg "") (uses input conditions instead) | {{agent}} uses a single {{agent}} policy for configuration, and uses [variables and input conditions](https://www.elastic.co/guide/en/fleet/current/dynamic-input-configuration.html) to adapt on a per-host basis. {{beats}} supports multiple configuration files per host, enabling third party solutions to deploy files hierarchically or in multiple groups, and enabling finer-grained access control to those files. |
| Compatible with version control and infrastructure as code solutions | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") (only via API) | ![yes](../../../images/fleet-green-check.svg "") | {{fleet}} stores the agent policy in {{es}}. It does not integrate with external version control or infrastructure as code solutions, but we are considering [improved support](https://github.com/elastic/kibana/issues/108524). However, {{beats}} and {{agent}} in standalone mode use a YAML file that is compatible with these solutions. |
| Spooling data to local disk | ![yes](../../../images/fleet-green-check.svg "") | ![no](../../../images/fleet-red-x.svg "") | ![no](../../../images/fleet-red-x.svg "") | This feature is currently being [considered for development](https://github.com/elastic/elastic-agent/issues/3490). |


## {{agent}} monitoring support [agent-monitoring-support]

You configure the collection of agent metrics in the agent policy. If metrics collection is selected (the default), all {{agent}}s enrolled in the policy will send metrics data to {{es}} (the output is configured globally).

The following image shows the **Agent monitoring** settings for the default agent policy:

:::{image} ../../../images/fleet-agent-monitoring-settings.png
:alt: Screen capture of agent monitoring settings in the default agent policy
:class: screenshot
:::

There are also pre-built dashboards for agent metrics that you can access under **Assets** in the {{agent}} integration:

:::{image} ../../../images/fleet-agent-monitoring-assets.png
:alt: Screen capture of {{agent}} monitoring assets
:class: screenshot
:::

The **[{{agent}}] Agent metrics** dashboard shows an aggregated view of agent metrics:

:::{image} ../../../images/fleet-agent-metrics-dashboard.png
:alt: Screen capture showing {{agent}} metrics
:class: screenshot
:::

For more information, refer to [Monitor {{agent}}s](https://www.elastic.co/guide/en/fleet/current/monitor-elastic-agent.html).

