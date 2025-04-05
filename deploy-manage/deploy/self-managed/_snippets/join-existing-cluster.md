% RPM and Debian only

When you install {{es}}, the installation process configures a single-node cluster by default. If you want a node to join an existing cluster instead, generate an enrollment token on an existing node *before* you start the new node for the first time.

1. On any node in your existing cluster, generate a node enrollment token:

    ```sh
    /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node
    ```

    An enrollment token has a lifespan of 30 minutes. You should create a new enrollment token for each new node that you add.

2. Copy the enrollment token, which is output to your terminal.
3. On your new {{es}} node, pass the enrollment token as a parameter to the [`elasticsearch-reconfigure-node`](elasticsearch://reference/elasticsearch/command-line-tools/reconfigure-node.md) tool:

    ```sh
    /usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <enrollment-token>
    ```

   Answer the `Do you want to continue` prompt with `yes` (`y`). The new {{es}} node will be reconfigured.

4. In a terminal, run `ifconfig` and copy the value for the host inet IP address. You’ll need this value later.
5. Open the new Elasticsearch instance's `elasticsearch.yml` file in a text editor.
   
   The `elasticsearch-reconfigure-node` tool has updated several settings. For example:

   * The `transport.host: 0.0.0.0` setting is already uncommented.
   * The `discovery_seed.hosts` setting has the IP address and port of the other {{es}} nodes added the cluster so far. As you add each new {{es}} node to the cluster, the `discovery_seed.hosts` setting will contain an array of the IP addresses and port numbers to connect to each {{es}} node that was previously added to the cluster.

6. In the configuration file, uncomment the line `#cluster.name: my-application` and set it to match the name you specified for the first {{es}} node:
   
   ```yml
   cluster.name: elasticsearch-demo
   ```

7. As with the first {{es}} node, you’ll need to set up {{es}} to run on a routable, external IP address. Uncomment the line `#network.host: 92.168.0.1` and replace the default address with the value that you copied. For example:

    ```yml
    network.host: 10.128.0.132
    ```

8. Save your changes and close the editor.

You can repeat these steps for each additional {{es}} node that you would like to add to the cluster. 