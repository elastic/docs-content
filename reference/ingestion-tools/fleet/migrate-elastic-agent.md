---
navigation_title: "Migrate {{agent}}s"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/migrate-elastic-agent.html
---

# Migrate {{fleet}}-managed {{agent}}s from one cluster to another [migrate-elastic-agent]


There are situations where you may need to move your installed {{agent}}s from being managed in one cluster to being managed in another cluster.

For a seamless migration, we advise that you create an identical agent policy in the new cluster that is configured in the same manner as the original cluster. There are a few methods to do this.

This guide takes you through the steps to migrate your {{agent}}s by snapshotting a source cluster and restoring it on a target cluster. These instructions assume that you have an {{ecloud}} deployment, but they can be applied to on-premise clusters as well.


## Take a snapshot of the source cluster [migrate-elastic-agent-take-snapshot]

Refer to the full [Snapshot and restore](/deploy-manage/tools/snapshot-and-restore.md) documentation for full details. In short, to create a new snapshot in an {{ecloud}} deployment:

1. In {{kib}}, open the main menu, then click **Manage this deployment**.
2. In the deployment menu, select **Snapshots**.
3. Click **Take snapshot now**.

    :::{image} images/migrate-agent-take-snapshot.png
    :alt: Deployments Snapshots page
    :class: screenshot
    :::



## Create a new target cluster from the snapshot [migrate-elastic-agent-create-target]

You can create a new cluster based on the snapshot taken in the previous step, and then migrate your {{agent}}s and {{fleet}} to the new cluster. For best results, it’s recommended that the new target cluster be at the same version as the cluster that the agents are migrating from.

1. Open the {{ecloud}} console and select **Create deployment**.
2. Select **Restore snapshot data**.
3. In the **Restore from** field, select your source deployment.
4. Choose your deployment settings, and, optimally, choose the same {{stack}} version as the source cluster.
5. Click **Create deployment**.

    :::{image} images/migrate-agent-new-deployment.png
    :alt: Create a deployment page
    :class: screenshot
    :::



## Update settings in the target cluster [migrate-elastic-agent-target-settings]

when the target cluster is available you’ll need to adjust a few settings. Take some time to examine the {{fleet}} setup in the new cluster.

1. Open the {{kib}} menu and select **Fleet**.
2. On the **Agents** tab, your agents should visible, however they’ll appear as `Offline`. This is because these agents have not yet enrolled in the new, target cluster, and are still enrolled in the original, source cluster.

    :::{image} images/migrate-agent-agents-offline.png
    :alt: Agents tab in Fleet showing offline agents
    :class: screenshot
    :::

3. Open the {{fleet}} **Settings** tab.
4. Examine the configurations captured there for {{fleet}}. Note that these settings are scopied from the snapshot of the source cluster and may not have a meaning in the target cluster, so they need to be modified accordingly.

    In the following example, both the **Fleet Server hosts** and the **Outputs** settings are copied over from the source cluster:

    :::{image} images/migrate-agent-host-output-settings.png
    :alt: Settings tab in Fleet showing source deployment host and output settings
    :class: screenshot
    :::

    The next steps explain how to obtain the relevant {{fleet-server}} host and {{es}} output details applicable to the new target cluster in {{ecloud}}.



### Modify the {{es}} output [migrate-elastic-agent-elasticsearch-output]

1. In the new target cluster on {{ecloud}}, in the **Outputs** section, on the {{fleet}} **Settings** tab, you will find an internal output named `Elastic Cloud internal output`. The host address is in the form:

    `https://<cluster-id-target>.containerhost:9244`

    Record this `<cluster-id-target>` from the target cluster. In the example shown, the ID is `fcccb85b651e452aa28703a59aea9b00`.

2. Also in the **Outputs** section, notice that the default {{es}} output (that was copied over from the source cluster) is also in the form:

    `https://<cluster-id-source>.<cloud endpoint address>:443`.

    Modify the {{es}} output so that the cluster ID is the same as that for `Elastic Cloud internal output`. In this example we also rename the output to `New Elasticsearch`.

    :::{image} images/migrate-agent-elasticsearch-output.png
    :alt: Outputs section showing the new Elasticsearch host setting
    :class: screenshot
    :::

    In this example, the `New Elasticsearch` output and the `Elastic Cloud internal output` now have the same cluster ID, namely `fcccb85b651e452aa28703a59aea9b00`.


You have now created an {{es}} output that agents can use to write data to the new, target cluster. For on-premise environments not using {{ecloud}}, you should similarly be able to use the host address of the new cluster.


### Modify the {{fleet-server}} host [migrate-elastic-agent-fleet-host]

Like the {{es}} host, the {{fleet-server}} host has also changed with the new target cluster. Note that if you’re deploying {{fleet-server}} on premise, the host has probably not changed address and this setting does not need to be modified. We still recommend that you ensure the agents are able to reach the the on-premise {{fleet-server}} host (which they should be able to as they were able to connect to it prior to the migration).

The {{ecloud}} {{fleet-server}} host has a similar format to the {{es}} output:

`https://<deployment-id>.fleet.<domain>.io`

To configure the correct {{ecloud}} {{fleet-server}} host you will need to find the target cluster’s full `deployment-id`, and use it to replace the original `deployment-id` that was copied over from the source cluster.

The easiest way to find the `deployment-id` is from the deployment URL:

1. From the {{kib}} menu select **Manage this deployment**.
2. Copy the deployment ID from the URL in your browser’s address bar.

    :::{image} images/migrate-agent-deployment-id.png
    :alt: Deployment management page
    :class: screenshot
    :::

    In this example, the new deployment ID is `eed4ae8e2b604fae8f8d515479a16b7b`.

    Using that value for `deployment-id`, the new {{fleet-server}} host URL is:

    `https://eed4ae8e2b604fae8f8d515479a16b7b.fleet.us-central1.gcp.cloud.es.io:443`

3. In the target cluster, under **Fleet server hosts**, replace the original host URL with the new value.

    :::{image} images/migrate-agent-fleet-server-host.png
    :alt: Fleet server hosts showing the new host URL
    :class: screenshot
    :::



### Reset the {{ecloud}} policy [migrate-elastic-agent-reset-policy]

On your target cluster, certain settings from the original {{ecloud}} {{agent}} policiy may still be retained, and need to be updated to reference the new cluster. For example, in the APM policy installed to the {{ecloud}} {{agent}} policy, the original and outdated APM URL is preserved. This can be fixed by running the `reset_preconfigured_agent_policies` API request. Note that when you reset the policy, all APM Integration settings are reset, including the secret key or any tail-based sampling.

To reset the {{ecloud}} {{agent}} policy:

1. Choose one of the API requests below and submit it through a terminal window.

    * If you’re using {{kib}} version 8.11 or higher, run:

        ```shell
        curl --request POST \
        --url https://{KIBANA_HOST:PORT}/internal/fleet/reset_preconfigured_agent_policies/policy-elastic-agent-on-cloud \
        -u username:password \
        --header 'Content-Type: application/json' \
        --header 'kbn-xsrf: as' \
        --header 'elastic-api-version: 1'
        ```

    * If you’re using a {{kib}} version below 8.11, run:

        ```shell
        curl --request POST \
        --url https://{KIBANA_HOST:PORT}/internal/fleet/reset_preconfigured_agent_policies/policy-elastic-agent-on-cloud \
        -u username:password \
        --header 'Content-Type: application/json' \
        --header 'kbn-xsrf: as'
        ```

        After running the command, your {{ecloud}} agent policy settings should all be updated appropriately.


::::{note}
After running the command, a warning message may appear in {{fleet}} indicating that {{fleet-server}} is not healthy. As well, the {{agent}} associated with the {{ecloud}} agent policy may disappear from the list of agents. To remedy this, you can restart {{integrations-server}}:

1. From the {{kib}} menu, select **Manage this deployment**.
2. In the deployment menu, select **Integrations Server**.
3. On the **Integrations Server** page, select **Force Restart**.

After the restart, {{integrations-server}} will enroll a new {{agent}} for the {{ecloud}} agent policy and {{fleet-server}} should return to a healthy state.

::::



### Confirm your policy settings [migrate-elastic-agent-confirm-policy]

Now that the {{fleet}} settings are correctly set up, it pays to ensure that the {{agent}} policy is also correctly pointing to the correct entities.

1. In the target cluster, go to **Fleet → Agent policies**.
2. Select a policy to verify.
3. Open the **Settings** tab.
4. Ensure that **Fleet Server**, **Output for integrations**, and **Output for agent monitoring** are all set to the newly created entities.

    :::{image} images/migrate-agent-policy-settings.png
    :alt: An agent policy's settings showing the newly created entities
    :class: screenshot
    :::


::::{note}
If you modified the {{fleet-server}} and the output in place these would have been updated accordingly. However if new entities are created, then ensure that the correct ones are referenced here.
::::



## Agent policies in the new target cluster [migrate-elastic-agent-migrated-policies]

By creating the new target cluster from a snapshot, all of your policies should have been created along with all of the agents. These agents will be offline due to the fact that the actual agents are not checking in with the new, target cluster (yet) and are still communicating with the source cluster.

The agents can now be re-enrolled into these policies and migrated over to the new, target cluster.


## Migrate {{agent}}s to the new target cluster [migrate-elastic-agent-migrated-agents]

In order to ensure that all required API keys are correctly created, the agents in your current cluster need to be re-enrolled into the new, target cluster.

This is best performed one policy at a time. For a given policy, you need to capture the enrollment token and the URL for the agent to connect to. You can find these by running the in-product steps to add a new agent.

1. On the target cluster, open **Fleet** and select **Add agent**.
2. Select your newly created policy.
3. In the section **Install {{agent}} on your host**, find the sample install command. This contains the details you’ll need to enroll the agents, namely the enrollment token and the {{fleet-server}} URL.
4. Copy the portion of the install command containing these values. That is, `–url=<path> –enrollment-token=<token for the new policy>`.

    :::{image} images/migrate-agent-install-command.png
    :alt: Install command from the Add Agent UI
    :class: screenshot
    :::

5. On the host machines where the current agents are installed, enroll the agents again using this copied URL and the enrollment token:

    ```shell
    sudo elastic-agent enroll --url=<fleet server url> --enrollment-token=<token for the new policy>
    ```

    The command output should be like the following:

    :::{image} images/migrate-agent-install-command-output.png
    :alt: Install command output
    :class: screenshot
    :::

6. The agent on each host will now check into the new {{fleet-server}} and appear in the new target cluster. In the source cluster, the agents will go offline as they won’t be sending any check-ins.

    :::{image} images/migrate-agent-newly-enrolled-agents.png
    :alt: Newly enrolled agents in the target cluster
    :class: screenshot
    :::

7. Repeat this procedure for each {{agent}} policy.

If all has gone well, you’ve successfully migrated your {{fleet}}-managed {{agent}}s to a new cluster.

