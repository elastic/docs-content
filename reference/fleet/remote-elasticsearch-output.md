---
navigation_title: Remote Elasticsearch output
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/remote-elasticsearch-output.html
description: Remote ES output allows you to send agent data to a remote cluster, keeping data separate and independent from the deployment where you use Fleet.
applies_to:
  stack: ga
  deployment:
    eck: ga
    ess: ga
    ece: ga
    self: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Remote {{es}} output [remote-elasticsearch-output]

Remote {{es}} outputs allow you to send {{agent}} data to a remote {{es}} cluster. This is especially useful for data that you want to keep separate and independent from the deployment where you use {{fleet}} to manage the {{agent}}s.

A remote {{es}} cluster supports the same [output settings](/reference/fleet/es-output-settings.md) as your main {{es}} cluster.

## Limitations

These limitations apply to remote {{es}} output:

* Using the remote {{es}} output with a remote cluster that has [traffic filters](/deploy-manage/security/traffic-filtering.md) enabled is not currently supported.
* Using {{elastic-defend}} when a remote {{es}} output is configured for an {{agent}} is not currently supported.

## Configuration [remote-output-config]

To configure a remote {{es}} cluster for your {{agent}} data:

1. In your main {{es}} cluster (Cluster A), open {{kib}}, and search for **Fleet settings** in the search bar. Select **Fleet/Settings** in the results.
2. In the **Outputs** section, select **Add output**.
3. In the **Add new output** flyout, provide a name for the output, and select **Remote Elasticsearch** as the output type.
4. In the **Hosts** field, add the URL that {{agent}}s should use to access the remote {{es}} cluster (Cluster B). 

    ::::{dropdown} Find the remote host address of the remote cluster
    :open:
    1. In the remote cluster (Cluster B), open {{kib}}, and search for **Fleet settings** in the search bar. Select **Fleet/Settings** in the results.
    2. In the **Outputs** section, copy the `Hosts` value of the default {{es}} output. If the value is not visible in full, edit the default {{es}} output to display the full value.
    3. In your main cluster (Cluster A), paste the value you copied into the **Hosts** field of the remote output configuration.
    ::::

5. In the **Service Token** field, add a service token to access the remote cluster (Cluster B). 

    ::::{dropdown} Create a service token to access the remote cluster
    :open:
    1. Copy the API request located below the **Service Token** field.
    2. In the remote cluster (Cluster B), open the {{kib}} menu, then go to **Management** → **Dev Tools** in self-managed deployments, or to **Developer tools** in {{ecloud}} deployments.
    3. Paste the API request in the console, then run it.
    4. Copy the value for the generated service token.
    5. In the main cluster (Cluster A), paste the value you copied into the **Service Token** field of the remote output configuration.
    ::::

    ::::{note}
    To prevent unauthorized access, the {{es}} Service Token is stored as a secret value. While secret storage is recommended, you can choose to override this setting, and store the password as plain text in the agent policy definition. Secret storage requires {{fleet-server}} version 8.12 or higher. This setting can also be stored as a secret value or as plain text for preconfigured outputs. To learn more about this option, check [Preconfiguration settings](kibana://reference/configuration-reference/fleet-settings.md#_preconfiguration_settings_for_advanced_use_cases).
    ::::

6. Choose whether integrations should be automatically synchronized on the remote {{es}} cluster (Cluster B). To configure this feature, refer to the [Automatic integrations synchronization](#automatic-integrations-synchronization) section.

    ::::{note}
    This feature is only available with certain subscriptions. For more information, check [Subscriptions](https://www.elastic.co/subscriptions).
    ::::

7. Choose whether the remote output should be the default for agent integrations or for agent monitoring data. When set as the default, {{agents}} use this output to send data if no other output is set in the [agent policy](/reference/fleet/agent-policy.md).
8. Select the [performance tuning settings](/reference/fleet/es-output-settings.md#es-output-settings-performance-tuning-settings) to optimize {{agent}}s for throughput, scale, or latency, or leave the default `balanced` setting.
9. Add any [advanced YAML configuration settings](/reference/fleet/es-output-settings.md#es-output-settings-yaml-config) that you’d like for the remote output.
10. Click **Save and apply settings**.

After the output is created, you can update an {{agent}} policy to use the new output, and send data to the remote {{es}} cluster:

1. In the main cluster (Cluster A), go to **{{fleet}}**, then open the **Agent policies** tab.
2. Click the agent policy you want to update, then click **Settings**.
3. To send integrations data, set the **Output for integrations** option to use the output that you configured in the previous steps.
4. To send {{agent}} monitoring data, set the **Output for agent monitoring** option to use the output that you configured in the previous steps.
5. Click **Save changes**.

The remote {{es}} output is now configured for the remote cluster (Cluster B).

If you choose not to synchronize integrations automatically, you need to make sure that for any integrations that are [added to your {{agent}} policy](/reference/fleet/add-integration-to-policy.md), the integration assets are also installed on the remote {{es}} cluster. For detailed steps on this process, refer to [Install and uninstall {{agent}} integration assets](/reference/fleet/install-uninstall-integration-assets.md).

::::{note}
When you use a remote {{es}} output, {{fleet-server}} performs a test to ensure connectivity to the remote cluster. The result of that connectivity test is used to report whether the remote output is healthy or unhealthy, and is displayed on the **{{fleet}}** → **Settings** → **Outputs** page, in the **Status** column.

In some cases, the remote {{es}} output used for {{agent}} data can be reached by the {{agent}}s but not by {{fleet-server}}. In those cases, you can ignore the resulting unhealthy state of the output and the associated `Unable to connect` error on the UI.
::::

## Automatic integrations synchronization

```{applies_to}
stack: ga 9.1
```

When enabled, this feature keeps integrations and custom assets synchronized between your main {{es}} cluster and one or more remote {{es}} clusters. 

::::{note}
This feature is only available with certain subscriptions. For more information, check [Subscriptions](https://www.elastic.co/subscriptions).
::::

### Requirements

* This feature requires setting up [{{ccr}}](/deploy-manage/tools/cross-cluster-replication.md).
* Remote clusters must be running the same {{es}} version as the main cluster, or a newer version that supports {{ccr}}.
* To install integrations, remote clusters require access to the [{{package-registry}}](/reference/fleet/index.md#package-registry-intro).

### Configure {{ccr}} on the remote cluster

In your remote cluster (Cluster B):

1. Open the {{kib}} menu, and go to **Management** → **Stack Management** → **Remote Clusters**.
2. Select **Add a remote cluster**, then follow the steps to add your main cluster (where the remote {{es}} output is configured) as a remote cluster.

    ::::{note}
    When prompted to add the remote cluster's _remote address_, enter your main cluster's proxy address:
    
    1. In your main cluster (Cluster A), go to **Deployment** → **Manage this deployment** → **Security** (or go to `deployments/<deployment_id>/security`).
    2. Scroll to the **Remote cluster parameters** section, then copy the **Proxy Address**.
    3. In your remote cluster (Cluster B), enter the copied value in the **Remote address** field of the remote cluster setup.
    ::::

    Refer to [Remote clusters](/deploy-manage/remote-clusters.md) for more details on how to add your main cluster (Cluster A) as a remote cluster.

3. After the remote cluster is added, go to **Management** → **Stack Management** → **Cross-Cluster Replication**.
4. In the **Follower indices** tab, create a follower index named `fleet-synced-integrations-ccr-<output_name>` that replicates the `fleet-synced-integrations` leader index on the main cluster. Replace `<output_name>` with the name you provided in the remote output configuration.
5. Resume replication once the follower index is created.

    For more detailed instructions, refer to the [Set up cross-cluster replication](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md) guide.

### Configure the integrations synchronization [integrations-sync-config]

1. In your main {{es}} cluster (Cluster A), open {{kib}}, and search for **Fleet settings** in the search bar. Select **Fleet/Settings** in the results.
2. In the **Outputs** section, edit the remote output for which you want to enable the automatic integrations synchronization.
3. Enable **Synchronize integrations**.
4. Choose whether uninstalled integrations should also be uninstalled on the remote cluster.
5. In the remote output configuration on the main cluster (Cluster A), add the {{kib}} URL of the remote cluster (Cluster B) in the **Remote Kibana URL** field.
6. In the **Remote Kibana API Key** field, add an API key to access Kibana on the remote cluster (Cluster B).

    ::::{dropdown} Create an API Key to access Kibana on the remote cluster
    :open:
    1. Copy the API request located below the **Remote Kibana API Key** field.
    2. In the remote cluster (Cluster B), open the {{kib}} menu, then go to **Management** → **Dev Tools** in self-managed deployments, or to **Developer tools** in {{ecloud}} deployments.
    3. Paste the API request in the console, then run it.
    4. Copy the encoded value of the generated API key.
    5. In the main cluster (Cluster A), paste the value you copied into the **Remote Kibana API Key** field of the remote output configuration.
    ::::

7. Click **Save and apply settings**.

You have now configured the automatic integrations synchronization between your main cluster (Cluster A) and your remote cluster (Cluster B).

### Verify the integrations synchronization [verify-integrations-sync]

When the integration synchronization is enabled for a remote {{es}} output, the current sync status is reported in **{{fleet}}** → **Settings**, in the **Outputs** section. To see a detailed breakdown of the integration syncing status, click the output's status in the **Integration syncing** column. The **Integrations syncing status** flyout opens with a list of the integrations and any custom assets in your main cluster and their current sync status.

You can also use the API to view the list of synced integrations with their sync status:

1. In the main cluster (Cluster A), go to **{{fleet}}** → **Settings**, then open the remote {{es}} output to display its ID.
2. Copy the output ID from the address bar in your browser.
3. Go to **Management** → **Dev Tools** in self-managed deployments, or to **Developer tools** in {{ecloud}} deployments.
4. Run the following query, replacing `<remote_output_id>` with the copied output ID:

    ```sh
    GET kbn:/api/fleet/remote_synced_integrations/<remote_output_id>/remote_status
    ```

    This API call returns the list of synced integrations with their sync status.

::::{note}
Synchronization can take up to five minutes after an integration is installed, updated, or removed on the main cluster.
::::

### View remote cluster data

After the integrations synchronization feature is set up, the following {{ccs}} data views become available for each remote cluster that you configure:

- `<remote_cluster>:logs-*`
- `<remote_cluster>:metrics-*`

To display these data views, open {{kib}} in your main {{es}} cluster, then go to **Management** -> **Stack management** → **Data Views**.

### Troubleshooting

In this section, you can find tips for resolving the following issues:

- [Integration syncing status failure](#integration-syncing-status-failure)
- [Integrations are not installed on the remote cluster](#integrations-are-not-installed-on-the-remote-cluster)
- [Uninstalled integrations are not uninstalled on the remote cluster](#uninstalled-integrations-are-not-uninstalled-on-the-remote-cluster)
- [Integration syncing fails with a retention leases error](#integration-syncing-fails-with-a-retention-leases-error)

#### Integration syncing status failure

If the integration syncing reports connection errors or fails to report the syncing status, follow these steps to verify your setup:

1. In the remote cluster, check the integration sync status using the API:

    1. Go to **Management** → **Dev Tools**, or to **Developer tools** in {{ecloud}} deployments.
    2. Run the following query:

    ```sh
    GET kbn:/api/fleet/remote_synced_integrations/status
    ```

    This API call returns the list of synced integrations with their sync status.

2. If the above query returns an error, verify your setup:

    - ::::{dropdown} Verify your setup in the remote cluster
      :open:
      1. In the remote cluster (Cluster B), go to **Management** → **Stack Management** → **Remote Clusters**.
      2. Check that the main cluster (Cluster A) is connected as a remote cluster.
      3. Go to **Management** → **Stack Management** → **Cross-Cluster Replication**.
      4. Check that {{ccr}} using the main cluster as remote is correctly set up and is active. In particular, check that the name of the follower index `fleet-synced-integrations-ccr-<output_name>` contains the name of the remote {{es}} output configured on the main cluster (Cluster A).
      ::::
    - ::::{dropdown} Verify your setup in the main cluster
      :open:
      1. In the main cluster (Cluster A), go to **{{fleet}}** → **Settings**.
      2. In the **Outputs** section, check that the remote {{es}} output is healthy. In particular, check that the remote {{es}} output's host URL matches the host URL of an {{es}} output on the remote cluster (Cluster B).
      3. Edit the remote {{es}} output, and check if the remote {{kib}} URL is correct, as well as the validity and privileges of the remote {{kib}} API key.
      
          Note that an incorrect value in either of these fields does not cause the output to become unhealthy, but it affects the integration synchronization.
      ::::

#### Integrations are not installed on the remote cluster

1. In the main cluster (Cluster A), look for errors in the integration syncing status of the remote {{es}} output in **{{fleet}}** → **Settings**, or use the API as described in the [Verify the integrations synchronization](#verify-integrations-sync) section.

2. Check the contents of the leader index:

    1. Go to **Management** → **Dev Tools**, or to **Developer tools** in {{ecloud}} deployments.
    2. Run the following query:
    
        ```sh
        GET fleet-synced-integrations/_search
        ```

        The response payload includes the list of integrations with their install status.

3. In the remote cluster (Cluster B), check the contents of the follower index:

    1. Go to **Management** → **Dev Tools**, or to **Developer tools** in {{ecloud}} deployments.
    2. Run the following query, replacing `<output_name>` with the name of the remote {{es}} output configured on the main cluster (Cluster A):

        ```sh
        GET fleet-synced-integrations-ccr-<output_name>/_search
        ```

        The response should match the the contents of the leader index on the main cluster.

4. If there is a mismatch between the leader and follower index, wait up to five minutes for the next sync to be completed in each cluster. To check if the sync is completed, inspect the {{kib}} logs and look for the line `[SyncIntegrationsTask] runTask ended: success`.

#### Uninstalled integrations are not uninstalled on the remote cluster

This can happen if the integration cannot be uninstalled on the remote cluster (Cluster B), for example, if it has integration policies assigned to agent policies. To inspect the reason why an integration failed to be uninstalled in the remote cluster, review the integration syncing status of the remote {{es}} output in **{{fleet}}** → **Settings**, or use the API as described in the [Verify the integrations synchronization](#verify-integrations-sync) section.

#### Integration syncing fails with a retention leases error

The integrations synchronization feature uses {{ccr}} to sync integration states between the main and the remote clusters. If a remote cluster is unreachable for a long time, the replication stops with a retention leases error. This results in the integration syncing failing with an "Operations are no longer available for replicating. Existing retention leases..." error.

To resolve this issue, remove the follower index on the remote cluster (Cluster B), then re-add it manually to restart replication:

1. In the remote cluster (Cluster B), go to **Management** → **Dev Tools**, or to **Developer tools** in {{ecloud}} deployments.
2. Run the following query to find all indices that match `fleet-synced-integrations-ccr-*`:

    ```sh
    GET fleet-synced-integrations-ccr-*
    ```

3. To delete the follower index, run:

    ```sh
    DELETE fleet-synced-integrations-ccr-<output_name>
    ```
    
    Replace `<output_name>` with the name of the remote {{es}} output configured on the main cluster (Cluster A).

4. Go to **Management** → **Stack Management** → **Cross-Cluster Replication**, and re-add a follower index named `fleet-synced-integrations-ccr-<output_name>` that replicates the `fleet-synced-integrations` leader index on the main cluster. Replace `<output_name>` with the name of the remote {{es}} output configured on the main cluster (Cluster A).
5. Click **Resume replication**.