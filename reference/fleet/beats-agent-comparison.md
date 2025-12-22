---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/beats-agent-comparison.html
applies_to:
  stack: ga
  serverless: ga
products:
  - id: beats
  - id: fleet
  - id: elastic-agent
---

# {{beats}} and {{agent}} capabilities

Elastic provides two main ways to send data to {{es}}:

* **{{beats}}** are lightweight data shippers that send operational data to {{es}}. Elastic provides separate {{beats}} for different types of data, such as logs, metrics, and uptime. Depending on what data you want to collect, you may need to install multiple shippers on a single host.
* **{{agent}}** is a single agent for logs, metrics, security data, and threat prevention. The {{agent}} can be deployed in two different modes:

    * **Managed by {{fleet}}** — The {{agent}} policies and lifecycle are centrally managed by the {{fleet}} app in {{kib}}. The Integrations app also lets you centrally add integrations with other popular services and systems. This is the recommended option for most users.
    * **Standalone mode** — All policies are applied to the {{agent}} manually as a YAML file. This is intended for more advanced users. See [Install standalone {{agent}}s](install-standalone-elastic-agent.md) for more information.


The method you use depends on your use case, which features you need, and whether you want to centrally manage your agents.

{{beats}} and {{agent}} can both send data directly to {{es}} or through {{ls}}, where you can further process and enhance the data, before visualizing it in {{kib}}.

This article summarizes the features and functionality you need to be aware of before adding new {{agent}}s or replacing your current {{beats}} with {{agent}}s. Starting in version 7.14.0, {{agent}} is generally available (GA).


## Choosing between {{agent}} and {{beats}} [choosing-between-agent-and-beats]

{{agent}} is a single binary designed to provide the same functionality that the various {{beats}} provide today. However, some functionality gaps are being addressed as we strive to reach feature parity.

The following steps will help you determine if {{agent}} can support your use case:

1. Determine if the integrations you need are supported and Generally Available (GA) on {{agent}}. To find out if an integration is GA, see the [{{integrations}} quick reference table](integration-docs://reference/all_integrations.md).
2. If the integration is available, check [Supported outputs](#supported-outputs-beats-and-agent) to see whether the required output is also supported.
3. Review [Capabilities comparison](#additional-capabilities-beats-and-agent) to determine if any features required by your deployment are supported. {{agent}} should support most of the features available on {{beats}} and is updated for each release.

If you are satisfied with all three steps, then {{agent}} is suitable for your deployment. However, if any steps fail your assessment, you should continue using {{beats}}, and review future updates or contact us in the [discuss forum](https://discuss.elastic.co/).


## Supported inputs [supported-inputs-beats-and-agent]

For {{agent}}s that are centrally managed by {{fleet}}, data collection is further simplified and defined by integrations. In this model, the decision on the inputs is driven by the integration you want to collect data from. The complexity of configuration details of various inputs is driven centrally by {{fleet}} and specifically by the integrations.

To find out if an integration is GA, see the [{{integrations}} quick reference table](integration-docs://reference/all_integrations.md).


## Supported outputs [supported-outputs-beats-and-agent]

The following table shows the outputs supported by the {{agent}} in 9.0.0-beta1:

::::{note}
{{elastic-defend}} and APM Server have a different output matrix.
::::


| Output | {{beats}} | {{fleet}}-managed {{agent}} | Standalone {{agent}} |
| --- |:---:|:---:|:---:|
| {{es}} Service | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") |
| {{es}} | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") |
| {{ls}} | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") |
| Kafka | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") |
| Remote {{es}} | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") |
| Redis | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") |
| File | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") |
| Console | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") |


## Supported configurations [supported-configurations]

| {{beats}} configuration | {{agent}} support |
| --- | --- |
| [Modules](beats://reference/filebeat/configuration-filebeat-modules.md) | Supported through integrations. |
| [Input setting overrides](beats://reference/filebeat/advanced-settings.md) | Not configurable. Set to default values. |
| [General settings](beats://reference/filebeat/configuration-general-options.md) | Many of these global settings are now internal to the agent and should not be modified. |
| [Project paths](beats://reference/filebeat/configuration-path.md) | {{agent}} configures these paths to provide a simpler and more streamlined configuration experience. |
| [External configuration file loading](beats://reference/filebeat/filebeat-configuration-reloading.md) | Config is distributed through policy. |
| [Live reloading](beats://reference/filebeat/_live_reloading.md) | Related to the config file reload. |
| [Outputs](beats://reference/filebeat/configuring-output.md) | Configured through {{fleet}}. See [Supported outputs](#supported-outputs-beats-and-agent). |
| [SSL](beats://reference/filebeat/configuration-ssl.md) | Supported |
| [{{ilm-cap}}](beats://reference/filebeat/ilm.md) | Enabled by default although the Agent uses [data streams](data-streams.md). |
| [{{es}} index template loading](beats://reference/filebeat/configuration-template.md) | No longer applicable |
| [{{kib}} endpoint](beats://reference/filebeat/setup-kibana-endpoint.md) | New {{agent}} workflow doesn’t need this. |
| [{{kib}} dashboard loading](beats://reference/filebeat/configuration-dashboards.md) | New {{agent}} workflow doesn’t need this. |
| [Processors](beats://reference/filebeat/defining-processors.md) | Processors can be defined at the integration level. Global processors, configured at the policy level, are currently under consideration. |
| [Autodiscover](beats://reference/filebeat/configuration-autodiscover.md) | Autodiscover is facilitated through [dynamic inputs](dynamic-input-configuration.md). {{agent}} does not support hints-based autodiscovery. |
| [Internal queues](beats://reference/filebeat/configuring-internal-queue.md) | {{fleet}}-managed {{agent}} and Standalone {{agent}} both support configuration of the internal memory queues by an end user. Neither support configuration of the internal disk queues by an end user. |
| [Load balance output hosts](beats://reference/filebeat/elasticsearch-output.md#_loadbalance) | Within the {{fleet}} UI, you can add YAML settings to configure multiple hosts per output type, which enables load balancing. |
| [Logging](beats://reference/filebeat/configuration-logging.md) | Supported |
| [HTTP endpoint](beats://reference/filebeat/http-endpoint.md) | Supported |
| [Regular expressions](beats://reference/filebeat/regexp-support.md) | Supported |


## Capabilities comparison [additional-capabilities-beats-and-agent]

The following table shows a comparison of capabilities supported by {{beats}} and the {{agent}} in 9.0.0-beta1:

| Item | {{beats}} | {{fleet}}-managed {{agent}} | Standalone {{agent}} | Description |
| --- |:---:|:---:|:---:| --- |
| Single agent for all use cases | ![no](images/red-x.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | {{agent}} provides logs, metrics, and more. You’d need to install multiple {{beats}} for these use cases. |
| Install integrations from web UI or API | ![no](images/red-x.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | {{agent}} integrations are installed with a convenient web UI or API, but {{beats}} modules are installed with a CLI. This installs {{es}} assets such as index templates and ingest pipelines, and {{kib}} assets such as dashboards. |
| Configure from web UI or API | ![no](images/red-x.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "")<br>(optional) | {{fleet}}-managed {{agent}} integrations can be configured in the web UI or API. Standalone {{agent}} can use the web UI, API, or YAML. {{beats}} can only be configured through YAML files. |
| Central, remote agent policy management | ![no](images/red-x.svg "") | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") | {{agent}} policies can be centrally managed through {{fleet}}. You have to manage {{beats}} configuration yourself or with a third-party solution. |
| Central, remote agent binary upgrades | ![no](images/red-x.svg "") | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") | {{agent}}s can be remotely upgraded through {{fleet}}. You have to upgrade {{beats}} yourself or with a third-party solution. |
| Add {{kib}} and {{es}} assets for a single integration or module | ![no](images/red-x.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | {{agent}} integrations allow you to add {{kib}} and {{es}} assets for a single integration at a time. {{beats}} installs hundreds of assets for all modules at once. |
| Auto-generated {{es}} API keys | ![no](images/red-x.svg "") | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") | {{fleet}} can automatically generate API keys with limited permissions for each {{agent}}, which can be individually revoked. Standalone {{agent}} and {{beats}} require you to create and manage credentials, and users often share them across hosts. |
| Auto-generate minimal {{es}} permissions | ![no](images/red-x.svg "") | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") | {{fleet}} can automatically give {{agent}}s minimal output permissions based on the inputs running. With standalone {{agent}} and {{beats}}, users often give overly broad permissions because it’s more convenient. |
| Data streams support | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | Both {{beats}} (default as of version 8.0) and {{agent}}s use [data streams](data-streams.md) with easier index life cycle management and the [data stream naming scheme](https://www.elastic.co/blog/an-introduction-to-the-elastic-data-stream-naming-scheme). |
| Variables and input conditions | ![no](images/red-x.svg "") | ![yes](images/green-check.svg "")<br>(limited) | ![yes](images/green-check.svg "") | {{agent}} offers [variables and input conditions](dynamic-input-configuration.md) to dynamically adjust based on the local host environment. Users can configure these directly in YAML for standalone {{agent}} or using the {{fleet}} API for {{fleet}}-managed {{agent}}. The Integrations app allows users to enter variables, and we are considering a [UI to edit conditions](https://github.com/elastic/kibana/issues/108525). {{beats}} only offers static configuration. |
| Allow non-superusers to manage assets and agents | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") (optional) | Starting with version 8.1.0, a superuser role is no longer required to use the {{fleet}} and Integrations apps and corresponding APIs. These apps are optional for standalone {{agent}}. {{beats}} offers [finer grained](beats://reference/filebeat/feature-roles.md) roles. |
| Air-gapped network support | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "")<br>(limited) | ![yes](images/green-check.svg "") | The {{integrations}} and {{fleet}} apps can be deployed in an air-gapped environment [self-managed deployment of the {{package-registry}}](air-gapped.md#air-gapped-diy-epr). {{fleet}}-managed {{agent}}s require a connection to our artifact repository for agent binary upgrades. However the policy can be modified to have agents point to a local server in order to fetch the agent binary. |
| Run without root on host | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | {{fleet}}-managed {{agent}}s, Standalone {{agent}}s, and {{beats}} require root permission only if they’re configured to capture data that requires that level of permission. |
| Multiple outputs | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | The policy for a single {{fleet}}-managed {{agent}} can specify multiple outputs. |
| Separate monitoring cluster | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "") | {{fleet}}-managed {{agent}}s, Standalone {{agent}} and {{beats}} can send to a remote monitoring cluster. |
| Secret management | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") | {{agent}} stores credentials in the agent policy. {{beats}} allows users to access credentials in a local [keystore](beats://reference/filebeat/keystore.md). |
| Progressive or canary deployments | ![yes](images/green-check.svg "") | ![yes](images/green-check.svg "")<br>{applies_to}`stack: ga 9.1.0` | ![yes](images/green-check.svg "") | To upgrade {{fleet}}-managed {{agents}} progressively, you can [configure an automatic upgrade](upgrade-elastic-agent.md#auto-upgrade-agents) in the {{agent}} policy. {applies_to}`stack: ga 9.1.0`<br><br>With standalone {{agent}} and {{beats}} you can deploy configuration files progressively using third party solutions. |
| Multiple configurations per host | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "")<br>(uses input conditions instead) | ![no](images/red-x.svg "")<br>(uses input conditions instead) | {{agent}} uses a single {{agent}} policy for configuration, and uses [variables and input conditions](dynamic-input-configuration.md) to adapt on a per-host basis. {{beats}} supports multiple configuration files per host, enabling third party solutions to deploy files hierarchically or in multiple groups, and enabling finer-grained access control to those files. |
| Compatible with version control and infrastructure as code solutions | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "")<br>(only using API) | ![yes](images/green-check.svg "") | Agent policies created in the {{fleet}} UI can't be managed with external version control or infrastructure as code solutions. However, you could develop a solution that [uses the {{fleet}} API or adds a preconfigured policy to Kibana](/reference/fleet/create-policy-no-ui.md). {{beats}} and {{agent}} in standalone mode use a YAML file that is compatible with these solutions. |
| Spooling data to local disk | ![yes](images/green-check.svg "") | ![no](images/red-x.svg "") | ![no](images/red-x.svg "") | This feature is currently being [considered for development](https://github.com/elastic/elastic-agent/issues/3490). |


## {{agent}} monitoring support [agent-monitoring-support]

You configure the collection of agent metrics in the agent policy. If metrics collection is selected (the default), all {{agent}}s enrolled in the policy will send metrics data to {{es}} (the output is configured globally).

The following image shows the **Agent monitoring** settings for the default agent policy:

:::{image} images/agent-monitoring-settings.png
:alt: Screen capture of agent monitoring settings in the default agent policy
:screenshot:
:::

There are also pre-built dashboards for agent metrics that you can access under **Assets** in the {{agent}} integration:

:::{image} images/agent-monitoring-assets.png
:alt: Screen capture of {{agent}} monitoring assets
:screenshot:
:::

The **[{{agent}}] Agent metrics** dashboard shows an aggregated view of agent metrics:

:::{image} images/agent-metrics-dashboard.png
:alt: Screen capture showing {{agent}} metrics
:screenshot:
:::

For more information, refer to [Monitor {{agent}}s](monitor-elastic-agent.md).
