---
navigation_title: Remote Elasticsearch output
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/remote-elasticsearch-output.html
description: Remote ES output allows you to send agent data to a remote cluster, keeping data separate and independent from the deployment where you use Fleet.
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: fleet
  - id: elastic-agent
---

# Remote {{es}} output [remote-elasticsearch-output]

Remote {{es}} outputs allow you to send {{agent}} data to a remote {{es}} cluster. This is especially useful for data that you want to keep separate and independent from the deployment where you use {{fleet}} to manage the {{agent}}s.

A remote {{es}} cluster supports the same [output settings](/reference/fleet/es-output-settings.md) as your management {{es}} cluster.

## Limitations [remote-output-limitations]

These limitations apply to remote {{es}} output:

* {{fleet-server}} must be able to reach the remote {{es}} cluster with a service token to generate API keys for the {{agents}} that use the remote output for data ingestion.
* Using a remote {{es}} output with a target cluster that has [network security](/deploy-manage/security/network-security.md) enabled is not currently supported.
* Using {{elastic-defend}} when a remote {{es}} output is configured for an {{agent}} is not currently supported.

## Configure the remote output [remote-output-config]

To configure a remote {{es}} cluster for your {{agent}} data:

::::::{stepper}

:::::{step} Create a new remote output

1. In your management {{es}} cluster, open {{kib}}, and search for **Fleet settings** in the search bar. Select **Fleet/Settings** in the results.
2. In the **Outputs** section, select **Add output**.
3. In the **Add new output** flyout, provide a name for the output.
4. Select **Remote Elasticsearch** as the output type.
:::::

:::::{step} Add remote cluster host URL

In the **Hosts** field, add the URL that {{agents}} should use to access the remote {{es}} cluster.

:::{dropdown} Find the remote host address of the remote cluster
:open:
1. In the remote cluster, open {{kib}}, and search for **Fleet settings** in the search bar. Select **Fleet/Settings** in the results.
2. In the **Outputs** section, copy the `Hosts` value of the default {{es}} output. If the value is not visible in full, edit the default  {{es}} output to display the full value.
3. In your management cluster, paste the value you copied into the **Hosts** field of the remote output configuration.
:::
:::::

:::::{step} Configure service token authentication

In the **Service Token** field, add a service token to access the remote cluster.

:::{dropdown} Create a service token to access the remote cluster
:open:
1. Copy the API request located below the **Service Token** field.
2. In the remote cluster, open the {{kib}} menu, then go to **Management** → **Dev Tools** in self-managed deployments, or to **Developer tools** in {{ecloud}} deployments.
3. Paste the API request in the console, then run it.
4. Copy the value for the generated service token.
5. In the management cluster, paste the value you copied into the **Service Token** field of the remote output configuration.
:::

:::{note}
To prevent unauthorized access, the {{es}} service token is stored as a secret value. While secret storage is recommended, you can choose to override this setting, and store the password as plain text in the agent policy definition. Secret storage requires {{fleet-server}} version 8.12 or higher. This setting can also be stored as a secret value or as plain text for preconfigured outputs. To learn more about this option, check [Preconfiguration settings](kibana://reference/configuration-reference/fleet-settings.md#_preconfiguration_settings_for_advanced_use_cases).
:::
:::::

:::::{step} Configure SSL certificate authorities (optional)

Configure SSL certificate authorities if the remote {{es}} cluster uses certificates that are not publicly trusted.

::::{applies-switch}

:::{applies-item} stack: ga 9.1

Expand the **Authentication** section to configure the SSL settings:

- **Server SSL certificate authorities**: Add the certificate authority (CA) used to sign the remote {{es}} cluster's SSL certificate. This allows {{fleet-server}} to validate the remote cluster's certificate.
- **Client SSL certificate** (optional): Add a client certificate if the remote {{es}} cluster requires mutual TLS (mTLS) authentication.
- **Client SSL certificate key** (optional): Add the private key for the client certificate.

:::

:::{applies-item} stack: ga =9.0

Add SSL settings in the **Advanced YAML configuration** section. For example:

```yaml
ssl:
  certificate_authorities:
  - |
    -----BEGIN CERTIFICATE-----
    MIIDSjCCAjKgAwIBAgIQRK+wgNajJ7qJMDmGLvhAazANBgkqhkiG9w0BAQUFADA/
    ...
    -----END CERTIFICATE-----
```

:::

::::

For more information about TLS configuration options, refer to [One-way and mutual TLS certifications flow > Output SSL options](/reference/fleet/tls-overview.md#output-ssl-options).
:::::

:::::{step} Configure output preferences

1. {applies_to}`stack: ga 9.1` Choose whether integrations should be automatically synchronized on the remote {{es}} cluster. To configure this feature, refer to [Automatic integrations synchronization](/reference/fleet/automatic-integrations-synchronization.md).

   :::{note}
   Automatic integrations synchronization is available only for certain subscription levels. For more information, check **Fleet Multi-Cluster support** on the [Elastic subscriptions](https://www.elastic.co/subscriptions) page.
   :::

2. Choose whether the remote output should be the default for agent integrations or for agent monitoring data. When set as the default, {{agents}} use this output to send data if no other output is set in the [agent policy](/reference/fleet/agent-policy.md).

3. Select the [performance tuning settings](/reference/fleet/es-output-settings.md#es-output-settings-performance-tuning-settings) to optimize {{agent}}s for throughput, scale, or latency, or leave the default `balanced` setting.

4. {applies_to}`stack: preview 9.2` Choose whether {{agents}} using this output should send data to [wired streams](/solutions/observability/streams/streams.md#streams-wired-streams). Using this feature requires additional steps. For more details, refer to [Ship data to streams > {{fleet}}](/solutions/observability/streams/wired-streams.md#streams-wired-streams-ship).
:::::

:::::{step} Configure advanced settings (optional)

Add any [advanced YAML configuration settings](/reference/fleet/es-output-settings.md#es-output-settings-yaml-config) that you'd like for the remote output.
:::::

:::::{step} Save the output configuration

Click **Save and apply settings**.
:::::

::::::

## Use the remote {{es}} output [remote-output-usage]

After creating the output, update an {{agent}} policy to use it and send data to the remote {{es}} cluster:

1. In the management cluster, go to **{{fleet}}**, then open the **Agent policies** tab.
2. Click the agent policy you want to update, then click **Settings**.
3. To send integrations data, set the **Output for integrations** option to use the output that you configured in the previous steps.
4. To send {{agent}} monitoring data, set the **Output for agent monitoring** option to use the output that you configured in the previous steps.
5. Click **Save changes**.

The remote {{es}} output is now configured for the remote cluster.

If you choose not to synchronize integrations automatically, you need to make sure that for any integrations that are [added to your {{agent}} policy](/reference/fleet/add-integration-to-policy.md), the integration assets are also installed on the remote {{es}} cluster. For detailed steps on this process, refer to [Install and uninstall {{agent}} integration assets](/reference/fleet/install-uninstall-integration-assets.md).

## Remote output health status [remote-output-health-status]

{{fleet-server}} requires connectivity to the remote cluster to generate API keys for {{agents}}. When you use a remote {{es}} output, {{fleet-server}} tests whether it can reach the remote cluster. The result determines whether the remote output is reported as healthy or unhealthy in the **Status** column for the output on the **{{fleet}}** → **Settings** page.

:::{note}
If you have multiple {{fleet-server}} instances, each {{fleet-server}} will attempt to test connectivity to all remote {{es}} outputs. If the {{fleet-server}} instances have different network scopes, it's expected that some of them might not be able to reach a certain remote output. In this case, the remote output will show as unhealthy in the UI with an `Unable to connect` error. You can ignore this status as long as the {{fleet-server}} instance that manages the {{agents}} using that remote output has connectivity to the remote cluster.
:::
