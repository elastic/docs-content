Update the {{es}} configuration on this first node so that other hosts are able to connect to it by editing the settings in [`elasticsearch.yml`](/deploy-manage/deploy/self-managed/configure-elasticsearch.md):

1. Open `elasticsearch.yml` in a text editor.

2. In a multi-node {{es}} cluster, all of the {{es}} instances need to have the same name.

    In the configuration file, uncomment the line `#cluster.name: my-application` and give the {{es}} instance any name that you’d like:

    ```yaml
    cluster.name: elasticsearch-demo
    ```

3. By default, {{es}} runs on `localhost`. For {{es}} instances on other nodes to be able to join the cluster, you need to set up {{es}} to run on a routable, external IP address.

    Uncomment the line `#network.host: 192.168.0.1` and replace the default address with `0.0.0.0`. The `0.0.0.0` setting enables {{es}} to listen for connections on all available network interfaces. In a production environment, you might want to [use a different value](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#common-network-settings), such as a static IP address or a reference to a [network interface of the host](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#network-interface-values).

    ```yaml
    network.host: 0.0.0.0
    ```

4. {{es}} needs to be enabled to listen for connections from other, external hosts.

    Uncomment the line `#transport.host: 0.0.0.0`. The `0.0.0.0` setting enables {{es}} to listen for connections on all available network interfaces. In a production environment you might want to [use a different value](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#common-network-settings), such as a static IP address or a reference to a [network interface of the host](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#network-interface-values).

    ```yaml
    transport.host: 0.0.0.0
    ```

    ::::{tip}
    You can find details about the `network.host` and `transport.host` settings in the {{es}} [networking settings reference](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md).
    ::::

5. Save your changes and close the editor.