---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/remote-elasticsearch-output.html
---

# Remote Elasticsearch output [remote-elasticsearch-output]

Remote {{es}} outputs allow you to send {{agent}} data to a remote {{es}} cluster. This is especially useful for data that you want to keep separate and independent from the deployment where you use {{fleet}} to manage the agents.

A remote {{es}} cluster supports the same [output settings](/reference/fleet/es-output-settings.md) as your main {{es}} cluster.

::::{warning}
A bug has been found that causes {{elastic-defend}} response actions to stop working when a remote {{es}} output is configured for an agent. This bug is currently being investigated and is expected to be resolved in an upcoming release.
::::


::::{note}
Using a remote {{es}} output with a target cluster that has [traffic filters](/deploy-manage/security/traffic-filtering.md) enabled is not currently supported.
::::

## Configuration

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
    2. In the remote cluster, open the {{kib}} menu and go to **Management > Dev Tools**.
    3. Run the API request.
    4. Copy the value for the generated token.
    5. Back in your main cluster, paste the value you copied into the output **Service Token** field.

        ::::{note}
        To prevent unauthorized access the {{es}} Service Token is stored as a secret value. While secret storage is recommended, you can choose to override this setting and store the password as plain text in the agent policy definition. Secret storage requires {{fleet-server}} version 8.12 or higher. This setting can also be stored as a secret value or as plain text for preconfigured outputs. See [Preconfiguration settings](kibana://reference/configuration-reference/fleet-settings.md#_preconfiguration_settings_for_advanced_use_cases) in the {{kib}} Guide to learn more.
        ::::

6. Choose whether integrations should automatically be synchronized on the remote {{es}} cluster. Refer to [Automatic integrations synchronization](#automatic-integrations-synchronization) below to configure this feature.
7. Choose whether or not the remote output should be the default for agent integrations or for agent monitoring data. When set, {{agents}} use this output to send data if no other output is set in the [agent policy](/reference/fleet/agent-policy.md).
8. Select which [performance tuning settings](/reference/fleet/es-output-settings.md#es-output-settings-performance-tuning-settings) you’d prefer in order to optimize {{agent}} for throughput, scale, or latency, or leave the default `balanced` setting.
9. Add any [advanced YAML configuration settings](/reference/fleet/es-output-settings.md#es-output-settings-yaml-config) that you’d like for the output.
10. Click **Save and apply settings**.

After the output is created, you can update an {{agent}} policy to use the new output and send data to the remote {{es}} cluster:

1. In {{fleet}}, open the **Agent policies** tab.
2. Click the agent policy to edit it, then click **Settings**.
3. To send integrations data, set the **Output for integrations** option to use the output that you configured in the previous steps.
4. To send {{agent}} monitoring data, set the **Output for agent monitoring** option to use the output that you configured in the previous steps.
5. Click **Save changes**.

The remote {{es}} cluster is now configured.

If you have chosen not to automatically synchronize integrations, you need to make sure that for any integrations that have been [added to your {{agent}} policy](/reference/fleet/add-integration-to-policy.md), the integration assets have been installed on the remote {{es}} cluster. Refer to [Install and uninstall {{agent}} integration assets](/reference/fleet/install-uninstall-integration-assets.md) for the steps.

## Automatic integrations synchronization

```{applies_to}
stack: ga 9.1
```

When enabled, this feature keeps integrations synced between your main {{es}} cluster and remote {{es}} clusters.

### Requirements

This feature requires setting up [{{ccr}}](/deploy-manage/tools/cross-cluster-replication.md), which is available to Platinum and Enterprise [subscriptions](https://www.elastic.co/subscriptions). Remote clusters must be running the same version of {{es}} as the main cluster or a newer version that is compatible with {{ccr}}.

Remote clusters require access to the [{{package-registry}}](/reference/fleet/index.md#package-registry-intro) to install integrations.

### Configuration

1. Configure {{ccr}} on the remote cluster.

    1. In the remote cluster, open the {{kib}} menu and go to **Stack Management > Remote Clusters**.
    2. Refer to [Remote clusters](https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters.html) to add your main cluster (where the remote {{es}} output is configured) as a remote cluster.
    3. Go to **Stack Management > Cross-Cluster Replication**.
    4. Create a follower index named `fleet-synced-integrations-ccr-<output name>` that replicates the `fleet-synced-integrations` leader index on the main cluster.
    5. Resume replication once the follower index is created.

2. In the main cluster, in the **Remote Kibana URL** field, add the Kibana URL of the remote cluster.

3. Create an API key to access Kibana on the remote cluster.

    1. Below the **Remote Kibana API Key** field, copy the API request.
    2. In the remote cluster, open the {{kib}} menu and go to **Management > Dev Tools**.
    3. Run the API request.
    4. Copy the encoded value of the generated API key.
    5. Back in the main cluster, paste the value you copied into the **Remote Kibana API Key** field.

4. Choose whether uninstalled integrations should also be uninstalled on the remote cluster.

### Troubleshooting

When integration syncing is enabled for a remote {{es}} output, the current sync status is reported in **{{fleet}} Settings** in the **Outputs** table. To see a detailed breakdown of the integration syncing status, click on the **Integration syncing** status badge.

You can also use the API to view the list of synced integrations with their sync status:

1. In the main cluster, go to **{{fleet}} Settings** and edit the remote {{es}} output to check.

2. Copy the output ID from the address in your browser.

3. Go to **Management > Dev Tools**.

4. Run the following query using the copied output ID:
    ```sh
    GET kbn:/api/fleet/remote_synced_integrations/<remote_output_id>/remote_status
    ```
    This should return the list of synced integrations with their sync status.

::::{note}
Syncing can take up to five minutes after an integration is installed, updated, or removed on the main cluster.
::::


#### Integration syncing status failure

If integration syncing reports connection errors or fails to report the syncing status, take the following steps to verify your setup.

1. In the remote cluster, check the integration sync status using the API:

    1. Go to **Management > Dev Tools**.
    2. Run the following query:
    ```sh
    GET kbn:/api/fleet/remote_synced_integrations/status
    ```
    This should return the list of synced integrations with their sync status.

2. If the above query returns an error, verify your setup on the remote cluster:

    1. Go to **Stack Management > Remote Clusters**.
    2. Check that the main cluster is connected as a remote cluster.
    4. Go to **Stack Management > Cross-Cluster Replication**.
    3. Check that {{ccr}} using the main cluster as remote is correctly set up and active. In particular, check that the name of the follower index `fleet-synced-integrations-ccr-<output name>` contains the name of the remote {{es}} output on the main cluster.

3. Verify your setup in the main cluster:

    1. In {{fleet}}, open the **Settings** tab.
    1. Check that the remote {{es}} output is healthy. In particular, check that the remote host URL matches one of the {{es}} hosts on the remote cluster.
    2. Edit the remote {{es}} output and check that the remote {{kib}} URL is correct, as well as the validity and privileges of the remote {{kib}} API key. Note that an incorrect value in either of these fields will not cause the output to become unhealthy, but will affect integration syncing.

#### Integrations are not installed on the remote cluster

1. In the main cluster, look for errors in the integration syncing status of the remote {{es}} output in {{fleet}} **Settings** or using the API as described [previously](#troubleshooting).

2. Check the contents of the leader index:

    1. Go to **Management > Dev Tools**.
    2. Run the following query
    ```sh
    GET fleet-synced-integrations/_search
    ```
    The response payload should include the list of integrations with their install status.

3. In the remote cluster, check the contents of the follower index:

    1. Go to **Management > Dev Tools**
    2. Run the following query:
    ```sh
    GET fleet-synced-integrations-ccr-<output name>/_search
    ```
    The response should match the the contents of the leader index on the main cluster.

4. If there is a mismatch between the leader and follower index, wait up to five minutes for the next sync to be completed in each cluster. You can check this by inspecting {{kib}} logs and looking for the line: `[SyncIntegrationsTask] runTask ended: success`.

#### Uninstalled integrations are not uninstalled on the remote cluster

This can happen when the integration cannot be uninstalled on the remote cluster, for instance if it has integration policies assigned to agent policies. To inspect the reason why an integration failed to be uninstalled in the remote cluster, review the integration syncing status of the remote {{es}} output in {{fleet}} **Settings** or using the API as described [above](#troubleshooting).
