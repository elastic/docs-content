::::{note}
To add a node to a cluster running on multiple machines, you must also set [`discovery.seed_hosts`](/deploy-manage/deploy/self-managed/important-settings-configuration.md#unicast.hosts) so that the new node can discover the rest of its cluster.
::::

To enroll new nodes in your cluster, create an enrollment token with the [`elasticsearch-create-enrollment-token`](elasticsearch://reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool on any existing node in your cluster. You can then start a new node with the `--enrollment-token` parameter so that it joins an existing cluster.

1. In a separate terminal from where {{es}} is running, navigate to the directory where you installed {{es}} and run the `elasticsearch-create-enrollment-token` tool to generate an enrollment token for your new nodes.

    ```sh subs=true
    bin{{slash}}elasticsearch-create-enrollment-token -s node
    ```

    Copy the enrollment token, which you’ll use to enroll new nodes with your {{es}} cluster.

    An enrollment token has a lifespan of 30 minutes. You should create a new enrollment token for each new node that you add.

2. From the installation directory of your new node, start {{es}} and pass the enrollment token with the `--enrollment-token` parameter.

    ```sh subs=true
    bin{{slash}}elasticsearch --enrollment-token <enrollment-token>
    ```

    {{es}} automatically generates certificates and keys in the following directory:

    ```sh subs=true
    config{{slash}}certs
    ```

You can repeat these steps for each additional {{es}} node that you would like to add to the cluster.

For more information about discovery and shard allocation, refer to [Discovery and cluster formation](/deploy-manage/distributed-architecture/discovery-cluster-formation.md) and [Cluster-level shard allocation and routing settings](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md).