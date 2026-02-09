
:::::::{applies-switch}

::::::{applies-item} { ess:, ece: }

:::{warning}
:applies_to: ece:
In ECE, resizing is limited by your [allocator capacity](/deploy-manage/deploy/cloud-enterprise/ece-manage-capacity.md).
:::

To resize your deployment and increase its capacity by expanding a data tier or adding a new one, use the following options:

**Option 1: Configure Autoscaling**

1. Log in to the [{{ecloud}} console](https://cloud.elastic.co?page=docs&placement=docs-body) or ECE Cloud UI.
1. On the home page, find your deployment and select **Manage**.
1. Go to **Actions** > **Edit deployment** and check that autoscaling is enabled. Adjust the **Enable Autoscaling for** dropdown menu as needed and select **Save**.
1. If autoscaling is successful, the cluster returns to a `healthy` status.
If the cluster is still out of disk, check if autoscaling has reached its set limits and [update your autoscaling settings](/deploy-manage/autoscaling/autoscaling-in-ece-and-ech.md#ec-autoscaling-update).

**Option 2: Configure deployment size and tiers**

You can increase the deployment capacity by editing the deployment and adjusting the size of the existing data tiers or adding new ones.

1. In {{kib}}, open your deployment’s navigation menu (placed under the Elastic logo in the upper left corner) and go to **Manage this deployment**.
1. From the right hand side, click to expand the **Manage** dropdown button and select **Edit deployment** from the list of options.
1. On the **Edit** page, increase capacity for the data tier you identified earlier by either adding a new tier with **+ Add capacity** or adjusting the size of an existing one. Choose the desired size and availability zones for that tier.
1. Navigate to the bottom of the page and click the **Save** button.

**Option 3: Change the hardware profiles/deployment templates**

You can change the [hardware profile](/deploy-manage/deploy/elastic-cloud/ec-change-hardware-profile.md) for {{ech}} deployments or [deployment template](/deploy-manage/deploy/cloud-enterprise/deployment-templates.md) of the {{ece}} cluster to one with a higher disk-to-memory ratio.

**Option 4: {applies_to}`ece: ga ` Override disk quota**

{{ece}} administrators can temporarily override the disk quota of {{es}} nodes in real time as explained in [](/deploy-manage/deploy/cloud-enterprise/resource-overrides.md). We strongly recommend making this change only under the guidance of Elastic Support, and only as a temporary measure or for troubleshooting purposes.



::::::

::::::{applies-item} { self: }
To increase the data node capacity in your cluster, you can [add more nodes](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md) to the cluster and assign the index’s target tier [node role](/manage-data/lifecycle/data-tiers.md#configure-data-tiers-on-premise) to the new nodes, or increase the disk capacity of existing nodes. Disk expansion procedures depend on your operating system and storage infrastructure and are outside the scope of Elastic support. In practice, this is often achieved by [removing a node from the cluster](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md) and reinstalling it with a larger disk.

::::::

::::::{applies-item} { eck: }
To increase the capacity of the data nodes in your {{eck}} cluster, you can either add more data nodes to the desired tier, or increase the storage size of existing nodes.

**Option 1: Add more data nodes**

1. Update the `count` field in your data node `nodeSets` to add more nodes:

    ```yaml subs=true
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: quickstart
    spec:
      version: {{version.stack}}
      nodeSets:
      - name: data-nodes
        count: 5  # Increase from previous count
        config:
          node.roles: ["data"]
        volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes:
            - ReadWriteOnce
            resources:
              requests:
                storage: 100Gi
    ```

1. Apply the changes:

    ```sh
    kubectl apply -f your-elasticsearch-manifest.yaml
    ```

    ECK automatically creates the new nodes with a `data` [node role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md) and {{es}} will relocate shards to balance the load. 
    
    You can monitor the progress using:

    ```console
    GET /_cat/shards?v&h=state,node&s=state
    ```

**Option 2: Increase storage size of existing nodes**

1. If your storage class supports [volume expansion](https://kubernetes.io/docs/concepts/storage/persistent-volumes/#expanding-persistent-volumes-claims), you can increase the storage size in the `volumeClaimTemplates`:

    ```yaml subs=true
    apiVersion: elasticsearch.k8s.elastic.co/v1
    kind: Elasticsearch
    metadata:
      name: quickstart
    spec:
      version: {{version.stack}}
      nodeSets:
      - name: data-nodes
        count: 3
        config:
          node.roles: ["data"]
        volumeClaimTemplates:
        - metadata:
            name: elasticsearch-data
          spec:
            accessModes:
            - ReadWriteOnce
            resources:
              requests:
                storage: 200Gi  # Increased from previous size
    ```

1. Apply the changes. If the volume driver supports `ExpandInUsePersistentVolumes`, the filesystem will be resized online without restarting {{es}}. Otherwise, you might need to manually delete the Pods after the resize so they can be recreated with the expanded filesystem.

For more information, refer to [](/deploy-manage/deploy/cloud-on-k8s/update-deployments.md) and [](/deploy-manage/deploy/cloud-on-k8s/volume-claim-templates.md#k8s-volume-claim-templates-update).
::::::


:::::::