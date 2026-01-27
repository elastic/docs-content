---
navigation_title: Preferred data tier
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/add-tier.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

% marciw move this page to a new index allocation subsection
% or just move it down in the ToC
% and this page really really needs rewriting

# Add a preferred data tier to a deployment [add-tier]

In an {{es}} deployment, an index and its shards can be allocated to [data tiers](../../manage-data/lifecycle/data-tiers.md) using routing and allocation settings.

To allow indices to be allocated, follow these steps:

1. [Determine which tiers](#determine-target-tier) an index's shards can be allocated to.
1. [Resize your deployment](#resize-your-deployment).


## Determine the target tier [determine-target-tier]

You can run the following step using either [API console](/explore-analyze/query-filter/tools/console.md) or direct [Elasticsearch API](elasticsearch://reference/elasticsearch/rest-apis/index.md) calls.

:::{include} /troubleshoot/elasticsearch/_snippets/determine-data-tier-that-needs-capacity.md
:::

## Resize your deployment [resize-your-deployment]



:::::::{applies-switch}

::::::{applies-item} { ess:, ece: }
To enable a new tier in your {{ech}} deployment, you edit the deployment topology to add a new data tier.

1. In {{kib}}, open your deployment’s navigation menu (placed under the Elastic logo in the upper left corner) and go to **Manage this deployment**.
1. From the right hand side, click to expand the **Manage** dropdown button and select **Edit deployment** from the list of options.
1. On the **Edit** page, click on **+ Add Capacity** for the tier you identified you need to enable in your deployment. Choose the desired size and availability zones for the new tier.
1. Navigate to the bottom of the page and click the **Save** button.
::::::

::::::{applies-item} { self: }

To increase the data node capacity in your cluster, you can [add more nodes](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md) to the cluster and assign the index’s target tier [node role](/manage-data/lifecycle/data-tiers.md#configure-data-tiers-on-premise) to the new nodes, or increase the disk capacity of existing nodes. Disk expansion procedures depend on your operating system and storage infrastructure and are outside the scope of Elastic support. In practice, this is often achieved by [removing a node from the cluster](/deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md) and reinstalling it with a larger disk.
::::::


::::::{applies-item} { eck: }
To increase the disk capacity of data nodes in your {{eck}} cluster, you can either add more data nodes and assign the index's target tier [node role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md#change-node-role) to the new nodes by adjusting the [node configuration](/deploy-manage/deploy/cloud-on-k8s/node-configuration.md) in the `spec` section of your {{es}} resource manifest, or increase the storage size of existing nodes.

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

    ECK automatically creates the new nodes and {{es}} will relocate shards to balance the load. You can monitor the progress using:

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

1. Apply the changes. If the volume driver supports `ExpandInUsePersistentVolumes`, the filesystem will be resized online without restarting {{es}}. Otherwise, you may need to manually delete the Pods after the resize so they can be recreated with the expanded filesystem.

For more information, refer to [](/deploy-manage/deploy/cloud-on-k8s/update-deployments.md) and [](/deploy-manage/deploy/cloud-on-k8s/volume-claim-templates.md). 

::::::

:::::::