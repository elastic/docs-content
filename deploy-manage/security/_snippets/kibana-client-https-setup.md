When you ran the `elasticsearch-certutil` tool with the `http` option, it created a `/kibana` directory containing an `elasticsearch-ca.pem` file. You use this file to configure {{kib}} to trust the {{es}} CA for the HTTP layer.

1. Copy the `elasticsearch-ca.pem` file to the {{kib}} configuration directory, as defined by the `$KBN_PATH_CONF` path.
2. Open `kibana.yml` and add the following line to specify the location of the security certificate for the HTTP layer.

    ```yaml
    elasticsearch.ssl.certificateAuthorities: $KBN_PATH_CONF/elasticsearch-ca.pem
    ```

3. Add the following line to specify the HTTPS URL for your {{es}} cluster.

    ```yaml
    elasticsearch.hosts: https://<your_elasticsearch_host>:9200
    ```

4. Restart {{kib}}.

:::::{admonition} Connect to a secure monitoring cluster
If the Elastic monitoring features are enabled and you configured a separate {{es}} monitoring cluster, you can also configure {{kib}} to connect to the monitoring cluster through HTTPS. The steps are the same, but each setting is prefixed by `monitoring`. For example, `monitoring.ui.elasticsearch.hosts` and `monitoring.ui.elasticsearch.ssl.truststore.path`.

::::{note}
You must create a separate `elasticsearch-ca.pem` security file for the monitoring cluster.
::::

:::::

