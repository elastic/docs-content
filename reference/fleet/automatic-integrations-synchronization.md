---
navigation_title: Automatic integrations synchronization
description: The automatic integrations sync feature keeps integrations and custom assets synced between your management Elasticsearch cluster and one or more remote clusters.
applies_to:
  stack: ga 9.1
  deployment:
    ess: ga
    ece: ga
    self: ga
products:
  - id: fleet
  - id: elastic-agent
---

# Automatic integrations synchronization

When enabled, this feature keeps integrations and custom assets synchronized between your main {{es}} cluster and one or more remote {{es}} clusters. 

::::{note}
This feature is available only for certain subscription levels. For more information, check **Fleet Multi-Cluster support** on the [Elastic subscriptions](https://www.elastic.co/subscriptions) page.
::::

## Requirements

* To use this feature, you need a configured [remote {{es}} output](/reference/fleet/remote-elasticsearch-output.md) and a set up [{{ccr}}](/deploy-manage/tools/cross-cluster-replication.md).
* Remote clusters must be running the same {{es}} version as the management cluster, or a newer version that supports {{ccr}}.
* To install integrations, remote clusters require access to the [{{package-registry}}](/reference/fleet/index.md#package-registry-intro).

## Limitations

These limitations apply when using the automatic integrations synchronization feature:

- [Index lifecycle management](/manage-data/lifecycle/index-lifecycle-management.md) (ILM) policies and enrich policies referenced in custom component templates are not automatically synchronized. Synchronizing custom assets that include references to ILM or enrich policies may cause custom component templates to break.
- Integrations installed on the management cluster are synchronized to the remote cluster regardless of the space they are installed in. On the remote cluster, the synchronized integrations are always installed in the default space.

## Configure {{ccr}} on the remote cluster

In your remote cluster:

1. Open the {{kib}} menu, and go to **Management** → **Stack Management** → **Remote Clusters**.
2. Select **Add a remote cluster**, then follow the steps to add your management cluster (where the remote {{es}} output is configured) as a remote cluster.

    ::::{note}
    When prompted to add the remote cluster's _remote address_, enter your management cluster's proxy address:
    
    1. In your management cluster, go to **Deployment** → **Manage this deployment** → **Security** (or go to `deployments/<deployment_id>/security`).
    2. Scroll to the **Remote cluster parameters** section, then copy the **Proxy Address**.
    3. In your remote cluster, enter the copied value in the **Remote address** field of the remote cluster setup.
    ::::

    Refer to [Remote clusters](/deploy-manage/remote-clusters.md) for more details on how to add your management cluster as a remote cluster.

3. After the remote cluster is added, go to **Management** → **Stack Management** → **Cross-Cluster Replication**.
4. In the **Follower indices** tab, create a follower index named `fleet-synced-integrations-ccr-<output_name>` that replicates the `fleet-synced-integrations` leader index on the management cluster. Replace `<output_name>` with the name you provided in the remote output configuration.
5. Resume replication once the follower index is created.

    For more detailed instructions, refer to the [Set up cross-cluster replication](/deploy-manage/tools/cross-cluster-replication/set-up-cross-cluster-replication.md) guide.

## Configure the integrations synchronization [integrations-sync-config]

1. In your management {{es}} cluster, open {{kib}}, and search for **Fleet settings** in the search bar. Select **Fleet/Settings** in the results.
2. In the **Outputs** section, edit the remote output for which you want to enable the automatic integrations synchronization.
3. Enable **Synchronize integrations**.
4. Choose whether uninstalled integrations should also be uninstalled on the remote cluster.
5. In the remote output configuration on the management cluster, add the {{kib}} URL of the remote cluster in the **Remote Kibana URL** field.
6. In the **Remote Kibana API Key** field, add an API key to access Kibana on the remote cluster.

    ::::{dropdown} Create an API key to access Kibana on the remote cluster
    :open:
    1. Copy the API request located below the **Remote Kibana API Key** field.
    2. In the remote cluster, open the {{kib}} menu, then go to **Management** → **Dev Tools** in self-managed deployments, or to **Developer tools** in {{ecloud}} deployments.
    3. Paste the API request in the console, then run it.
    4. Copy the encoded value of the generated API key.
    5. In the management cluster, paste the value you copied into the **Remote Kibana API Key** field of the remote output configuration.
    ::::

7. Click **Save and apply settings**.

You have now configured the automatic integrations synchronization between your management cluster and your remote cluster.

## Verify the integrations synchronization [verify-integrations-sync]

When the integration synchronization is enabled for a remote {{es}} output, the current sync status is reported in **{{fleet}}** → **Settings**, in the **Outputs** section. To see a detailed breakdown of the integration syncing status, click the output's status in the **Integration syncing** column. The **Integrations syncing status** flyout opens with a list of the integrations and any custom assets in your management cluster and their current sync status.

You can also use the API to view the list of synced integrations with their sync status:

1. In the management cluster, go to **{{fleet}}** → **Settings**, then open the remote {{es}} output to display its ID.
2. Copy the output ID from the address bar in your browser.
3. Go to **Management** → **Dev Tools** in self-managed deployments, or to **Developer tools** in {{ecloud}} deployments.
4. Run the following query, replacing `<remote_output_id>` with the copied output ID:

    ```sh
    GET kbn:/api/fleet/remote_synced_integrations/<remote_output_id>/remote_status
    ```

    This API call returns the list of synced integrations with their sync status.

::::{note}
Synchronization can take up to five minutes after an integration is installed, updated, or removed on the management cluster.
::::

## View remote cluster data

After the integrations synchronization feature is set up, the following {{ccs}} data views become available for each remote cluster that you configure:

- `<remote_cluster>:logs-*`
- `<remote_cluster>:metrics-*`

To display these data views, open {{kib}} in your management {{es}} cluster, then go to **Management** → **Stack management** → **Data Views**.

## Troubleshooting

In this section, you can find tips for resolving the following issues:

- [Integration syncing status failure](#integration-syncing-status-failure)
- [Integrations are not installed on the remote cluster](#integrations-are-not-installed-on-the-remote-cluster)
- [Uninstalled integrations are not uninstalled on the remote cluster](#uninstalled-integrations-are-not-uninstalled-on-the-remote-cluster)
- [Integration syncing fails with a retention leases error](#integration-syncing-fails-with-a-retention-leases-error)

### Integration syncing status failure

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
      1. In the remote cluster, go to **Management** → **Stack Management** → **Remote Clusters**.
      2. Check that the management cluster is connected as a remote cluster.
      3. Go to **Management** → **Stack Management** → **Cross-Cluster Replication**.
      4. Check that {{ccr}} using the management cluster as remote is correctly set up and is active. In particular, check that the name of the follower index `fleet-synced-integrations-ccr-<output_name>` contains the name of the remote {{es}} output configured on the management cluster.
      ::::
    - ::::{dropdown} Verify your setup in the management cluster
      :open:
      1. In the management cluster, go to **{{fleet}}** → **Settings**.
      2. In the **Outputs** section, check that the remote {{es}} output is healthy. In particular, check that the remote {{es}} output's host URL matches the host URL of an {{es}} output on the remote cluster.
      3. Edit the remote {{es}} output, and check if the remote {{kib}} URL is correct, as well as the validity and privileges of the remote {{kib}} API key.
      
          Note that an incorrect value in either of these fields does not cause the output to become unhealthy, but it affects the integration synchronization.
      ::::

### Integrations are not installed on the remote cluster

1. In the management cluster, look for errors in the integration syncing status of the remote {{es}} output in **{{fleet}}** → **Settings**, or use the API as described in the [Verify the integrations synchronization](#verify-integrations-sync) section.

2. Check the contents of the leader index:

    1. Go to **Management** → **Dev Tools**, or to **Developer tools** in {{ecloud}} deployments.
    2. Run the following query:
    
        ```sh
        GET fleet-synced-integrations/_search
        ```

        The response payload includes the list of integrations with their install status.

3. In the remote cluster, check the contents of the follower index:

    1. Go to **Management** → **Dev Tools**, or to **Developer tools** in {{ecloud}} deployments.
    2. Run the following query, replacing `<output_name>` with the name of the remote {{es}} output configured on the management cluster:

        ```sh
        GET fleet-synced-integrations-ccr-<output_name>/_search
        ```

        The response should match the contents of the leader index on the management cluster.

4. If there is a mismatch between the leader and follower index, wait up to five minutes for the next sync to be completed in each cluster. To check if the sync is completed, inspect the {{kib}} logs and look for the line `[SyncIntegrationsTask] runTask ended: success`.

### Uninstalled integrations are not uninstalled on the remote cluster

This can happen if the integration cannot be uninstalled on the remote cluster, for example, if it has integration policies assigned to agent policies. To inspect the reason why an integration failed to be uninstalled in the remote cluster, review the integration syncing status of the remote {{es}} output in **{{fleet}}** → **Settings**, or use the API as described in the [Verify the integrations synchronization](#verify-integrations-sync) section.

### Integration syncing fails with a retention leases error

The integrations synchronization feature uses {{ccr}} to sync integration states between the management and the remote clusters. If a remote cluster is unreachable for a long time, the replication stops with a retention leases error. This results in the integration syncing failing with an "Operations are no longer available for replicating. Existing retention leases..." error.

To resolve this issue, remove the follower index on the remote cluster, then re-add it manually to restart replication:

1. In the remote cluster, go to **Management** → **Dev Tools**, or to **Developer tools** in {{ecloud}} deployments.
2. Run the following query to find all indices that match `fleet-synced-integrations-ccr-*`:

    ```sh
    GET fleet-synced-integrations-ccr-*
    ```

3. To delete the follower index, run:

    ```sh
    DELETE fleet-synced-integrations-ccr-<output_name>
    ```
    
    Replace `<output_name>` with the name of the remote {{es}} output configured on the management cluster.

4. Go to **Management** → **Stack Management** → **Cross-Cluster Replication**, and re-add a follower index named `fleet-synced-integrations-ccr-<output_name>` that replicates the `fleet-synced-integrations` leader index on the management cluster. Replace `<output_name>` with the name of the remote {{es}} output configured on the management cluster.
5. Click **Resume replication**.