1. Enable the remote cluster server on every node of the remote cluster. In [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

    1. Set [`remote_cluster_server.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote-cluster-network-settings) to `true`.
    2. Configure the bind and publish address for remote cluster server traffic, for example using [`remote_cluster.host`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote-cluster-network-settings). Without configuring the address, remote cluster traffic may be bound to the local interface, and remote clusters running on other machines can't connect.
    3. Optionally, configure the remote server port using [`remote_cluster.port`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote_cluster.port) (defaults to `9443`).

2. Next, generate a certificate authority (CA) and a server certificate/key pair. On one of the nodes of the remote cluster, from the directory where {{es}} has been installed:

    1. Create a CA, if you don't have a CA already:

        ```sh
        ./bin/elasticsearch-certutil ca --pem --out=cross-cluster-ca.zip --pass CA_PASSWORD
        ```

        Replace `CA_PASSWORD` with the password you want to use for the CA. You can remove the `--pass` option and its argument if you are not deploying to a production environment.

    2. Unzip the generated `cross-cluster-ca.zip` file. This compressed file contains the following content:

        ```txt
        /ca
        |_ ca.crt
        |_ ca.key
        ```

    3. Generate a certificate and private key pair for the nodes in the remote cluster:

        ```sh
        ./bin/elasticsearch-certutil cert --out=cross-cluster.p12 --pass=CERT_PASSWORD --ca-cert=ca/ca.crt --ca-key=ca/ca.key --ca-pass=CA_PASSWORD --dns=<CLUSTER_FQDN> --ip=192.0.2.1
        ```

        * Replace `CA_PASSWORD` with the CA password from the previous step.
        * Replace `CERT_PASSWORD` with the password you want to use for the generated private key.
        * Use the `--dns` option to specify the relevant DNS name for the certificate. You can specify it multiple times for multiple DNS.
        * Use the `--ip` option to specify the relevant IP address for the certificate. You can specify it multiple times for multiple IP addresses.

    4. If the remote cluster has multiple nodes, you can either:

        * create a single wildcard certificate for all nodes;
        * or, create separate certificates for each node either manually or in batch with the [silent mode](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md#certutil-silent).

3. On every node of the remote cluster:

    1. Copy the `cross-cluster.p12` file from the earlier step to the `config` directory. If you didn't create a wildcard certificate, make sure you copy the correct node-specific p12 file.
    2. Add following configuration to [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

        ```yaml
        xpack.security.remote_cluster_server.ssl.enabled: true
        xpack.security.remote_cluster_server.ssl.keystore.path: cross-cluster.p12
        ```

    3. Add the SSL keystore password to the {{es}} keystore:

        ```sh
        ./bin/elasticsearch-keystore add xpack.security.remote_cluster_server.ssl.keystore.secure_password
        ```

        When prompted, enter the `CERT_PASSWORD` from the earlier step.

4. Restart the remote cluster.

