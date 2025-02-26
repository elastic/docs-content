---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/remote-elasticsearch-output.html
---

# Remote Elasticsearch output [remote-elasticsearch-output]

Beginning in version 8.12.0, you can send {{agent}} data to a remote {{es}} cluster. This is especially useful for data that you want to keep separate and independent from the deployment where you use {{fleet}} to manage the agents.

A remote {{es}} cluster supports the same [output settings](/reference/ingestion-tools/fleet/es-output-settings.md) as your main {{es}} cluster.

::::{warning}
A bug has been found that causes {{elastic-defend}} response actions to stop working when a remote {{es}} output is configured for an agent. This bug is currently being investigated and is expected to be resolved in an upcoming release.
::::


::::{note}
Using a remote {{es}} output with a target cluster that has [traffic filters](/deploy-manage/security/traffic-filtering.md) enabled is not currently supported.
::::


To configure a remote {{es}} cluster for your {{agent}} data:

1. In {{fleet}}, open the **Settings** tab.
2. In the **Outputs** section, select **Add output**.
3. In the **Add new output** flyout, provide a name for the output and select **Remote Elasticsearch** as the output type.
4. In the **Hosts** field, add the URL that agents should use to access the remote {{es}} cluster.

    1. To find the remote host address, in the remote cluster open {{kib}} and go to **Management → {{fleet}} → Settings**.
    2. Copy the **Hosts** value for the default output.
    3. Back in your main cluster, paste the value you copied into the output **Hosts** field.

5. Create a service token to access the remote cluster.

    1. Below the **Service Token** field, copy the API request.
    2. In the remote cluster, open the {{kib}} menu and go to **Management → Dev Tools**.
    3. Run the API request.
    4. Copy the value for the generated token.
    5. Back in your main cluster, paste the value you copied into the output **Service Token** field.

        ::::{note}
        To prevent unauthorized access the {{es}} Service Token is stored as a secret value. While secret storage is recommended, you can choose to override this setting and store the password as plain text in the agent policy definition. Secret storage requires {{fleet-server}} version 8.12 or higher. This setting can also be stored as a secret value or as plain text for preconfigured outputs. See [Preconfiguration settings](kibana://docs/reference/configuration-reference/fleet-settings.md#_preconfiguration_settings_for_advanced_use_cases) in the {{kib}} Guide to learn more.
        ::::

6. Choose whether or not the remote output should be the default for agent integrations or for agent monitoring data. When set, {{agent}}s use this output to send data if no other output is set in the [agent policy](/reference/ingestion-tools/fleet/agent-policy.md).
7. Select which [performance tuning settings](/reference/ingestion-tools/fleet/es-output-settings.md#es-output-settings-performance-tuning-settings) you’d prefer in order to optimize {{agent}} for throughput, scale, or latency, or leave the default `balanced` setting.
8. Add any [advanced YAML configuration settings](/reference/ingestion-tools/fleet/es-output-settings.md#es-output-settings-yaml-config) that you’d like for the output.
9. Click **Save and apply settings**.

After the output is created, you can update an {{agent}} policy to use the new remote {{es}} cluster:

1. In {{fleet}}, open the **Agent policies** tab.
2. Click the agent policy to edit it, then click **Settings**.
3. To send integrations data, set the **Output for integrations** option to use the output that you configured in the previous steps.
4. To send {{agent}} monitoring data, set the **Output for agent monitoring** option to use the output that you configured in the previous steps.
5. Click **Save changes**.

The remote {{es}} cluster is now configured.

As a final step before using the remote {{es}} output, you need to make sure that for any integrations that have been [added to your {{agent}} policy](/reference/ingestion-tools/fleet/add-integration-to-policy.md), the integration assets have been installed on the remote {{es}} cluster. Refer to [Install and uninstall {{agent}} integration assets](/reference/ingestion-tools/fleet/install-uninstall-integration-assets.md) for the steps.
