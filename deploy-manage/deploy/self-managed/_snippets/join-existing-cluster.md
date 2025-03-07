When you install {{es}}, the installation process configures a single-node cluster by default. If you want a node to join an existing cluster instead, generate an enrollment token on an existing node *before* you start the new node for the first time.

1. On any node in your existing cluster, generate a node enrollment token:

    ```sh
    /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node
    ```

2. Copy the enrollment token, which is output to your terminal.
3. On your new {{es}} node, pass the enrollment token as a parameter to the `elasticsearch-reconfigure-node` tool:

    ```sh
    /usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <enrollment-token>
    ```

    {{es}} is now configured to join the existing cluster.

4. [Start your new node using `systemd`](#running-systemd).