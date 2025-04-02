When {{es}} starts for the first time, the security auto-configuration process binds the HTTP layer to `0.0.0.0`, but only binds the transport layer to localhost. This intended behavior ensures that you can start a single-node cluster with security enabled by default without any additional configuration.

Before enrolling a new node, additional actions such as binding to an address other than `localhost` or satisfying bootstrap checks are typically necessary in production clusters. During that time, an auto-generated enrollment token could expire, which is why enrollment tokens aren’t generated automatically.

Additionally, only nodes on the same host can join the cluster without additional configuration. If you want nodes from another host to join your cluster, you need to set `transport.host` to a [supported value](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#network-interface-values) (such as uncommenting the suggested value of `0.0.0.0`), or an IP address that’s bound to an interface where other hosts can reach it. Refer to [transport settings](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#transport-settings) for more information.

To enroll new nodes in your cluster, create an enrollment token with the `elasticsearch-create-enrollment-token` tool on any existing node in your cluster. You can then start a new node with the `--enrollment-token` parameter so that it joins an existing cluster.

1. In a separate terminal from where {{es}} is running, navigate to the directory where you installed {{es}} and run the [`elasticsearch-create-enrollment-token`](elasticsearch://reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool to generate an enrollment token for your new nodes.

    ```sh subs=true
    bin{{slash}}elasticsearch-create-enrollment-token -s node
    ```

    Copy the enrollment token, which you’ll use to enroll new nodes with your {{es}} cluster.

2. From the installation directory of your new node, start {{es}} and pass the enrollment token with the `--enrollment-token` parameter.

    ```sh subs=true
    bin{{slash}}elasticsearch --enrollment-token <enrollment-token>
    ```

    {{es}} automatically generates certificates and keys in the following directory:

    ```sh subs=true
    config{{slash}}certs
    ```

3. Repeat the previous step for any new nodes that you want to enroll.

For more information about discovery and shard allocation, refer to [Discovery and cluster formation](/deploy-manage/distributed-architecture/discovery-cluster-formation.md) and [Cluster-level shard allocation and routing settings](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md).