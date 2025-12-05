<!--
This snippet is in use in the following locations:
- remote-clusters-api-key.md
- eck-remote-clusters-from-external.md
-->
1. On every node of the local cluster:

    1. Copy the `ca.crt` file generated on the remote cluster earlier into the `config` directory, renaming the file `remote-cluster-ca.crt`.
    2. Add following configuration to [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

        ```yaml
        xpack.security.remote_cluster_client.ssl.enabled: true
        xpack.security.remote_cluster_client.ssl.certificate_authorities: [ "remote-cluster-ca.crt" ]
        ```

        ::::{tip}
        If the remote cluster uses a publicly trusted certificate, don't include the `certificate_authorities` setting. This example assumes the remote is using the private certificates [created earlier](#remote-clusters-security-api-key-remote-action), which require the CA to be added.
        ::::

    3. Add the cross-cluster API key, created on the remote cluster earlier, to the keystore:

        ```sh
        ./bin/elasticsearch-keystore add cluster.remote.ALIAS.credentials
        ```

        Replace `ALIAS` with the same name that you intend to use to create the remote cluster entry later. When prompted, enter the encoded cross-cluster API key created on the remote cluster earlier.

2. Restart the local cluster to load changes to the keystore and settings.

    If you are configuring only the cross-cluster API key, you can use the [Nodes reload secure settings API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-reload-secure-settings) instead of restarting the cluster. Configuring the `remote_cluster_client` settings in `elasticsearch.yml` still requires a restart.
