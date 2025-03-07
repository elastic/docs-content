---
navigation_title: "With the same CA"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/update-node-certs-same.html
---



# Same CA [update-node-certs-same]


This procedure assumes that the you have access to the CA certificate and key that was originally generated (or otherwise held by your organization) and used to sign the node certificates currently in use. It also assumes that the clients connecting to {{es}} on the HTTP layer are configured to trust the CA certificate.

If you have access to the CA used to sign your existing certificates, you only need to replace the certificates and keys for each node in your cluster. If you replace your existing certificates and keys on each node and use the same filenames, {{es}} reloads the files starts using the new certificates and keys.

You don’t have to restart each node, but doing so forces new TLS connections and is [a recommended practice](updating-certificates.md#use-rolling-restarts) when updating certificates. Therefore, the following steps include a node restart after updating each certificate.

The following steps provide instructions for generating new node certificates and keys for both the transport layer and the HTTP layer. You might only need to replace one of these layer’s certificates depending on which of your certificates are expiring.

::::{important}
:name: cert-password-updates

If your keystore is password protected, the password is stored in the {{es}} secure settings, *and* the password needs to change, then you must perform a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) on your cluster. You must also use a different file name for the keystore so that {{es}} doesn’t reload the file before the node is restarted.
::::


::::{tip}
If your CA has changed, complete the steps in [update security certificates with a different CA](different-ca.md).
::::


## Generate a new certificate for the transport layer [node-certs-same-transport]

The following examples use PKCS#12 files, but the same steps apply to JKS keystores.

1. Open the `ES_PATH_CONF/elasticsearch.yml` file and check the names and locations of the keystores that are currently in use. You’ll use the same names for your new certificate.

    In this example, the keystore and truststore are pointing to different files. Your configuration might use the same file that contains the certificate and CA. In this case, include the path to that file for both the keystore and truststore.

    ::::{note}
    These instructions assume that the provided certificate is signed by a trusted CA and the verification mode is set to `certificate`. This setting ensures that nodes to not attempt to perform hostname verification.

    ::::


    ```yaml
    xpack.security.transport.ssl.keystore.path: config/elastic-certificates.p12
    xpack.security.transport.ssl.keystore.type: PKCS12
    xpack.security.transport.ssl.truststore.path: config/elastic-stack-ca.p12
    xpack.security.transport.ssl.truststore.type: PKCS12
    xpack.security.transport.ssl.verification_mode: certificate
    ```

2. Using your existing CA, generate a keystore for your nodes. You must use the CA that was used to sign the certificate currently in use.

    ```shell
    ./bin/elasticsearch-certutil cert --ca elastic-stack-ca.p12
    ```

    ::::{dropdown} Command parameters
    `--ca <ca_file>`
    :   Name of the CA keystore used to sign your certificates. If you used the `elasticsearch-certutil` tool to generate your existing CA, the keystore name defaults to `elastic-stack-ca.p12`.

    ::::


    1. Enter a name for the output file or accept the default of `elastic-certificates.p12`.
    2. When prompted, enter a password for the node keystore.

3. If you entered a password when creating the node keystore that is different from the current keystore password, run the following command to store the password in the {{es}} keystore:

    ```shell
    ./bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password
    ```

4. $$$start-rolling-restart$$$On the current node in your cluster where you’re updating the keystore, start a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling).

    Stop at the step indicating **Perform any needed changes**, and then proceed to the next step in this procedure.

5. $$$replace-keystores$$$Replace your existing keystore with the new keystore, ensuring that the file names match. For example, `elastic-certificates.p12`.

    ::::{important}
    If your [keystore password is changing](#cert-password-updates), then save the keystore with a new filename so that {{es}} doesn’t attempt to reload the file before you update the password.
    ::::

6. If you needed to save the new keystore with a new filename, update the `ES_PATH_CONF/elasticsearch.yml` file to use the filename of the new keystore. For example:

    ```yaml
    xpack.security.transport.ssl.keystore.path: config/elastic-certificates.p12
    xpack.security.transport.ssl.keystore.type: PKCS12
    xpack.security.transport.ssl.truststore.path: config/elastic-stack-ca.p12
    xpack.security.transport.ssl.truststore.type: PKCS12
    ```

7. Start the node where you updated the keystore.
8. $$$verify-keystore$$$(Optional) Use the [SSL certificate API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ssl-certificates) to verify that {{es}} loaded the new keystore.

    ```console
    GET /_ssl/certificates
    ```
    %  TEST[skip:creates a lot of noise]

9. If you’re only updating certificates for the transport layer (and not the HTTP layer), then complete [step 4](#start-rolling-restart) through [step 8](#verify-keystore) one node at a time until you’ve updated all keystores in your cluster. You can then complete the remaining steps for a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling).

    Otherwise, do not complete a rolling restart. Instead, proceed to the steps for generating a new certificate for the HTTP layer.



### What’s next? [transport-layer-sameca-whatsnext]

Well done! You’ve updated the keystore for the transport layer. You can also [update the keystore for the HTTP layer](#node-certs-same-http) if necessary. If you’re not updating the keystore for the HTTP layer, then you’re all set.


## Generate a new certificate for the HTTP layer [node-certs-same-http]

Other components such as {{kib}} or any of the Elastic language clients verify this certificate when they connect to {{es}}.

::::{note}
If your organization has its own CA, you’ll need to [generate Certificate Signing Requests (CSRs)](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md#certutil-csr). CSRs contain information that your CA uses to generate and sign a certificate.
::::


1. On any node in your cluster where {{es}} is installed, run the {{es}} HTTP certificate tool.

    ```shell
    ./bin/elasticsearch-certutil http
    ```

    This command generates a `.zip` file that contains certificates and keys to use with {{es}} and {{kib}}. Each folder contains a `README.txt` explaining how to use these files.

    1. When asked if you want to generate a CSR, enter `n`.
    2. When asked if you want to use an existing CA, enter `y`.
    3. Enter the absolute path to your CA, such as the path to the `elastic-stack-ca.p12` file.
    4. Enter the password for your CA.
    5. Enter an expiration value for your certificate. You can enter the validity period in years, months, or days. For example, enter `1y` for one year.
    6. When asked if you want to generate one certificate per node, enter `y`.

        Each certificate will have its own private key, and will be issued for a specific hostname or IP address.

    7. When prompted, enter the name of the first node in your cluster. It’s helpful to use the same node name as the value for the `node.name` parameter in the `elasticsearch.yml` file.
    8. Enter all hostnames used to connect to your first node. These hostnames will be added as DNS names in the Subject Alternative Name (SAN) field in your certificate.

        List every hostname and variant used to connect to your cluster over HTTPS.

    9. Enter the IP addresses that clients can use to connect to your node.
    10. Repeat these steps for each additional node in your cluster.

2. After generating a certificate for each of your nodes, enter a password for your private key when prompted.
3. Unzip the generated `elasticsearch-ssl-http.zip` file. This compressed file contains two directories; one each for {{es}} and {{kib}}. Within the `/elasticsearch` directory is a directory for each node that you specified with its own `http.p12` file. For example:

    ```txt
    /node1
    |_ README.txt
    |_ http.p12
    |_ sample-elasticsearch.yml
    ```

    ```txt
    /node2
    |_ README.txt
    |_ http.p12
    |_ sample-elasticsearch.yml
    ```

    ```txt
    /node3
    |_ README.txt
    |_ http.p12
    |_ sample-elasticsearch.yml
    ```

4. If necessary, rename the `http.p12` file to match the name of your existing certificate for HTTP client communications. For example, `node1-http.p12`.
5. $$$start-rolling-restart-http$$$On the current node in your cluster where you’re updating the keystore, start a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling).

    Stop at the step indicating **Perform any needed changes**, and then proceed to the next step in this procedure.

6. Replace your existing keystore with the new keystore, ensuring that the file names match. For example, `node1-http.p12`.

    ::::{important}
    If your [keystore password is changing](#cert-password-updates), then save the keystore with a new filename so that {{es}} doesn’t attempt to reload the file before you update the password.
    ::::

7. If you needed to save the new keystore with a new filename, update the `ES_PATH_CONF/elasticsearch.yml` file to use the filename of the new keystore. For example:

    ```yaml
    xpack.security.http.ssl.enabled: true
    xpack.security.http.ssl.keystore.path: node1-http.p12
    ```

8. If your keystore password is changing, add the password for your private key to the secure settings in {{es}}.

    ```shell
    ./bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
    ```

9. Start the node where you updated the keystore.

    Use the [cat nodes API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) to confirm that the node joined the cluster:

    ```console
    GET _cat/nodes
    ```

10. $$$verify-keystore-http$$$(Optional) Use the [SSL certificate API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ssl-certificates) to verify that {{es}} loaded the new keystore.

    ```console
    GET /_ssl/certificates
    ```
    %  TEST[skip:creates a lot of noise]

11. One node at a time, complete [step 5](#start-rolling-restart-http) through [step 10](#verify-keystore-http) until you’ve updated all keystores in your cluster.
12. Complete the remaining steps for a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling), beginning with the step to **Reenable shard allocation**.


