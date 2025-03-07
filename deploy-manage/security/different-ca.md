---
navigation_title: "With a different CA"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/update-node-certs-different.html
---



# Different CA [update-node-certs-different]


If you have to trust a new CA from your organization, or you need to generate a new CA yourself, use this new CA to sign the new node certificates and instruct your nodes to trust the new CA.

## Generate a new certificate for the transport layer [node-certs-different-transport]

Create a new CA certificate, or get the CA certificate of your organization, and add it to your existing CA truststore. After you finish updating your certificates for all nodes, you can remove the old CA certificate from your truststore (but not before!).

::::{note}
The following examples use PKCS#12 files, but the same steps apply to JKS keystores.
::::


1. Open the `ES_PATH_CONF/elasticsearch.yml` file and check the names and locations of the keystores that are currently in use. You’ll use the same names for your new keystores.

    In this example, the keystore and truststore are using different files. Your configuration might use the same file for both the keystore and the truststore.

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

2. On **any** node in your cluster, generate a new CA certificate. You only need to complete this step one time. If you’re using the CA certificate of your organization, then skip this step.

    ```shell
    ./bin/elasticsearch-certutil ca --pem
    ```

    ::::{dropdown} Command parameters
    `--pem`
    :   Generates a directory containing a CA certificate and key in PEM format instead of PKCS#12.

    ::::


    1. Enter a name for the compressed output file that will contain your certificate and key, or accept the default name of `elastic-stack-ca.zip`.
    2. Unzip the output file. The resulting directory contains a CA certificate (`ca.crt`) and a private key (`ca.key`).

        ::::{important}
        Keep these file in a secure location as they contain the private key for your CA.
        ::::

3. On **every** node in your cluster, import the new `ca.crt` certificate into your existing CA truststore. This step ensures that your cluster trusts the new CA certificate. This example uses the Java `keytool` utility to import the certificate into the `elastic-stack-ca.p12` CA truststore.

    ```shell
    keytool -importcert -trustcacerts -noprompt -keystore elastic-stack-ca.p12 \
    -storepass <password>  -alias new-ca -file ca.crt
    ```

    ::::{dropdown} Command parameters
    `-keystore`
    :   Name of the truststore that you are importing the new CA certificate into.

    `-storepass`
    :   Password for the CA truststore.

    `-alias`
    :   Name that you want to assign to the new CA certificate entry in the keystore.

    `-file`
    :   Name of the new CA certificate to import.

    ::::

4. $$$check-ca-truststore$$$ Check that the new CA certificate was added to your truststore.

    ```shell
    keytool -keystore config/elastic-stack-ca.p12 -list
    ```

    When prompted, enter the password for the CA truststore.

    The output should contain both the existing CA certificate and your new certificate. If you previously used the `elasticsearch-certutil` tool to generate your keystore, the alias of the old CA defaults to `ca` and the type of entry is `PrivateKeyEntry`.



### Generate a new certificate for each node in your cluster [node-certs-different-nodes]

Now that your CA truststore is updated, use your new CA certificate to sign a certificate for your nodes.

::::{note}
If your organization has its own CA, you’ll need to [generate Certificate Signing Requests (CSRs)](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md#certutil-csr). CSRs contain information that your CA uses to generate and sign a security certificate.
::::


1. Using the new CA certificate and key, create a new certificate for your nodes.

    ```shell
    ./bin/elasticsearch-certutil cert --ca-cert ca/ca.crt --ca-key ca/ca.key
    ```

    ::::{dropdown} Command parameters
    `--ca-cert`
    :   Specifies the path to your new CA certificate (`ca.crt`) in PEM format. You must also specify the `--ca-key` parameter.

    `--ca-key`
    :   Specifies the path to the private key (`ca.key`) for your CA certificate. You must also specify the `--ca-cert` parameter.

    ::::


    1. Enter a name for the output file or accept the default of `elastic-certificates.p12`.
    2. When prompted, enter a password for your node certificate.

2. $$$start-rolling-restart-newca$$$On the current node in your cluster where you’re updating the keystore, start a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling).

    Stop at the step indicating **Perform any needed changes**, and then proceed to the next step in this procedure.

3. Replace your existing keystore with the new keystore, ensuring that the file names match. For example, `elastic-certificates.p12`.

    ::::{important}
    If your [keystore password is changing](same-ca.md#cert-password-updates), then save the keystore with a new filename so that {{es}} doesn’t attempt to reload the file before you update the password.
    ::::

4. If you needed to save the new keystore with a new filename, update the `ES_PATH_CONF/elasticsearch.yml` file to use the filename of the new keystore. For example:

    ```yaml
    xpack.security.transport.ssl.keystore.path: config/elastic-certificates.p12
    xpack.security.transport.ssl.keystore.type: PKCS12
    xpack.security.transport.ssl.truststore.path: config/elastic-stack-ca.p12
    xpack.security.transport.ssl.truststore.type: PKCS12
    ```

5. Start the node where you updated the keystore.
6. $$$verify-keystore-newca$$$(Optional) Use the [SSL certificate API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ssl-certificates) to verify that {{es}} loaded the new keystore.

    ```console
    GET /_ssl/certificates
    ```
    %  TEST[skip:creates a lot of noise]

7. If you’re only updating certificates for the transport layer (and not the HTTP layer), then complete [step 2](#start-rolling-restart-newca) through [step 6](#verify-keystore-newca) one node at a time until you’ve updated all keystores in your cluster. You can then complete the remaining steps for a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling).

    Otherwise, do not complete a rolling restart. Instead, proceed to the steps for generating a new certificate for the HTTP layer.

8. (Optional) After replacing keystores on each node in your cluster, [list the certificates in your truststore](#check-ca-truststore) and then remove the old CA certificate.

    If you previously used the `elasticsearch-certutil` tool to generate your keystore, the alias of the old CA defaults to `ca` and the type of entry is `PrivateKeyEntry`.

    ```shell
    keytool -delete -noprompt -alias ca  -keystore config/elastic-stack-ca.p12 \
    -storepass <password>
    ```

    ::::{dropdown} Command parameters
    `-alias`
    :   Name of the keystore alias for the old CA certificate that you want to remove from your truststore.

    ::::



### What’s next? [transport-layer-newca-whatsnext]

Well done! You’ve updated the keystore for the transport layer. You can also [update the keystore for the HTTP layer](#node-certs-different-http) if necessary. If you’re not updating the keystore for the HTTP layer, then you’re all set.


## Generate a new certificate for the HTTP layer [node-certs-different-http]

You can generate certificates for the HTTP layer using your new CA certificate and private key. Other components such as {{kib}} or any of the Elastic language clients verify this certificate when they connect to {{es}}.

::::{note}
If your organization has its own CA, you’ll need to [generate Certificate Signing Requests (CSRs)](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md#certutil-csr). CSRs contain information that your CA uses to generate and sign a security certificate instead of using self-signed certificates that the `elasticsearch-certutil` tool generates.
::::


::::{admonition} Update clients to trust the new CA
After generating (but before using) new certificates for the HTTP layer, you need to go to all the clients that connect to {{es}} (such as {{beats}}, {{ls}}, and any language clients) and configure them to also trust the new CA (`ca.crt`) that you generated.

This process is different for each client, so refer to your client’s documentation for trusting certificates. You’ll [update HTTP encryption between {{kib}} and {{es}}](#node-certs-different-kibana) after generating the necessary certificates in this procedure.

::::


1. On any node in your cluster where {{es}} is installed, run the {{es}} HTTP certificate tool.

    ```shell
    ./bin/elasticsearch-certutil http
    ```

    This command generates a `.zip` file that contains certificates and keys to use with {{es}} and {{kib}}. Each folder contains a `README.txt` explaining how to use these files.

    1. When asked if you want to generate a CSR, enter `n`.
    2. When asked if you want to use an existing CA, enter `y`.
    3. Enter the absolute path to your **new** CA certificate, such as the path to the `ca.crt` file.
    4. Enter the absolute path to your new CA certificate private key, such as the path to the `ca.key` file.
    5. Enter an expiration value for your certificate. You can enter the validity period in years, months, or days. For example, enter `1y` for one year.
    6. When asked if you want to generate one certificate per node, enter `y`.

        Each certificate will have its own private key, and will be issued for a specific hostname or IP address.

    7. When prompted, enter the name of the first node in your cluster. Use the same node name as the value for the `node.name` parameter in the `elasticsearch.yml` file.
    8. Enter all hostnames used to connect to your first node. These hostnames will be added as DNS names in the Subject Alternative Name (SAN) field in your certificate.

        List every hostname and variant used to connect to your cluster over HTTPS.

    9. Enter the IP addresses that clients can use to connect to your node.
    10. Repeat these steps for each additional node in your cluster.

2. After generating a certificate for each of your nodes, enter a password for your keystore when prompted.
3. Unzip the generated `elasticsearch-ssl-http.zip` file. This compressed file contains one directory for both {{es}} and {{kib}}. Within the `/elasticsearch` directory is a directory for each node that you specified with its own `http.p12` file. For example:

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

4. If necessary, rename each `http.p12` file to match the name of your existing certificate for HTTP client communications. For example, `node1-http.p12`.
5. $$$start-rolling-restart-http-newca$$$On the current node in your cluster where you’re updating the keystore, start a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling).

    Stop at the step indicating **Perform any needed changes**, and then proceed to the next step in this procedure.

6. Replace your existing keystore with the new keystore, ensuring that the file names match. For example, `node1-http.p12`.

    ::::{important}
    If your [keystore password is changing](same-ca.md#cert-password-updates), then save the keystore with a new filename so that {{es}} doesn’t attempt to reload the file before you update the password.
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

10. $$$verify-keystore-http-newca$$$(Optional) Use the [SSL certificate API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ssl-certificates) to verify that {{es}} loaded the new keystore.

    ```console
    GET /_ssl/certificates
    ```
    %  TEST[skip:creates a lot of noise]

11. One node at a time, complete [step 5](#start-rolling-restart-http-newca) through [step 10](#verify-keystore-http-newca) until you’ve updated all keystores in your cluster.
12. Complete the remaining steps for a [rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling), beginning with the step to **Reenable shard allocation**.


### What’s next? [http-kibana-newca-whatsnext]

Well done! You’ve updated the keystore for the HTTP layer. You can now [update encryption between {{kib}} and {{es}}](#node-certs-different-kibana).


## Update encryption between {{kib}} and {{es}} [node-certs-different-kibana]

When you ran the `elasticsearch-certutil` tool with the `http` option, it created a `/kibana` directory containing an `elasticsearch-ca.pem` file. You use this file to configure {{kib}} to trust the {{es}} CA for the HTTP layer.

1. Copy the `elasticsearch-ca.pem` file to the {{kib}} configuration directory, as defined by the `KBN_PATH_CONF` path.

    ::::{note}
    `KBN_PATH_CONF` contains the path for the {{kib}} configuration files. If you installed {{kib}} using archive distributions (`zip` or `tar.gz`), the path defaults to `KBN_HOME/config`. If you used package distributions (Debian or RPM), the path defaults to `/etc/kibana`.
    ::::

2. If you modified the filename for the `elasticsearch-ca.pem` file, edit `kibana.yml` and update the configuration to specify the location of the security certificate for the HTTP layer.

    ```yaml
    elasticsearch.ssl.certificateAuthorities: KBN_PATH_CONF/elasticsearch-ca.pem
    ```

3. Restart {{kib}}.


