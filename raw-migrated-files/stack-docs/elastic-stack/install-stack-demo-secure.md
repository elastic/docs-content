---
mapped_pages:
  - https://www.elastic.co/guide/en/elastic-stack/current/install-stack-demo-secure.html
applies_to:
  deployment:
    self: ga
products: []
---

# Tutorial: Securing a self-managed {{stack}} [install-stack-demo-secure]

% This doc feels duplicate (it comes from elastic-stack original book), although it includes an end to end guidance and offers different examples for certificates generation
% we have to decide what to do with this at a later stage

This tutorial is a follow-on to [installing a self-managed {{stack}}](/deploy-manage/deploy/self-managed.md) with a multi-node {{es}} cluster, {{kib}}, {{fleet-server}} and {{agent}}. In a production environment, it’s recommended after completing the {{kib}} setup to proceed directly to this tutorial to configure your SSL certificates. These steps guide you through that process, and then describe how to configure {{fleet-server}} and {{agent}} with the certificates in place.

**Securing the {{stack}}**

Since {{stack}} 8.0, security is enabled by default, meaning that traffic between {{es}} nodes and between {{kib}} and {{es}} is SSL-encrypted. While this is suitable for testing non-production viability of the Elastic platform, most production networks have requirements for the use of trusted CA-signed certificates. These steps demonstrate how to update the out-of-the-box self-signed certificates with your own trusted CA-signed certificates.

For traffic to be encrypted between {{es}} cluster nodes and between {{kib}} and {{es}}, SSL certificates must be created for the transport ({{es}} inter-node communication) and HTTP (for the {{es}} REST API) layers. Similarly, when setting up {{fleet-server}} you’ll generate and configure a new certificate bundle, and then {{agent}} uses the generated certificates to communicate with both {{fleet-server}} and {{es}}. The process to set things up is as follows:

* [Prerequisites and assumptions](#install-stack-demo-secure-prereqs)
* [Step 1: Generate a new self-signed CA certificate](#install-stack-demo-secure-ca)
* [Step 2: Generate a new certificate for the transport layer](#install-stack-demo-secure-transport)
* [Step 3: Generate new certificate(s) for the HTTP layer](#install-stack-demo-secure-http)
* [Step 4: Configure security on additional {{es}} nodes](#install-stack-demo-secure-second-node)
* [Step 5: Generate server-side and client-side certificates for {{kib}}](#install-stack-demo-secure-kib-es)
* [Step 6: Install {{fleet}} with SSL certificates configured](#install-stack-demo-secure-fleet)
* [Step 7: Install {{agent}}](#install-stack-demo-secure-agent)
* [Step 8: View your system data](#install-stack-demo-secure-view-data)

It should take between one and two hours to complete these steps.


## Prerequisites and assumptions [install-stack-demo-secure-prereqs]

Before starting, you’ll need to have set up an on-premises {{es}} cluster with {{kib}}, following the steps for [installing a self-managed {{stack}}](/deploy-manage/deploy/self-managed.md).

The examples in this guide use RPM packages to install the {{stack}} components on hosts running Red Hat Enterprise Linux 8. The steps for other install methods and operating systems are similar, and can be found in the documentation linked from each section.

Special considerations such as firewalls and proxy servers are not covered here.


## Step 1: Generate a new self-signed CA certificate [install-stack-demo-secure-ca]

In a production environment you would typically use the CA certificate from your own organization, along with the certificate files generated for the hosts where the {{stack}} is being installed. For demonstration purposes, we’ll use the Elastic certificate utility to configure a self-signed CA certificate.

1. On the first node in your {{es}} cluster, stop the {{es}} service:

    ```shell
    sudo systemctl stop elasticsearch.service
    ```

2. Generate a CA certificate using the provided certificate utility, `elasticsearch-certutil`. Note that the location of the utility depends on the installation method you used to install {{es}}. Refer to [elasticsearch-certutil](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md) for the command details and to [Update security certificates with a different CA](different-ca.md) for details about the procedure as a whole.

    Run the following command. When prompted, specify a unique name for the output file, such as `elastic-stack-ca.zip`:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil ca -pem
    ```

3. Move the output file to the `/etc/elasticsearch/certs` directory. This directory is created automatically when you install {{es}}.

    ```shell
    sudo mv /usr/share/elasticsearch/elastic-stack-ca.zip /etc/elasticsearch/certs/
    ```

4. Unzip the file:

    ```shell
    sudo unzip -d /etc/elasticsearch/certs /etc/elasticsearch/certs/elastic-stack-ca.zip
    ```

5. View the files that were unpacked into a new `ca` directory:

    ```shell
    sudo ls /etc/elasticsearch/certs/ca/
    ```

    `ca.crt`
    :   The generated certificate (or you can substitute this with your own certificate, signed by your organizations’s certificate authority)

    `ca.key`
    :   The certificate authority’s private key

    These steps to generate new self-signed CA certificates need to be done only on the first {{es}} node. The other {{es}} nodes will use the same `ca.crt` and `ca.key` files.

6. From the `/etc/elasticsearch/certs/ca/` directory, import the newly created CA certificate into the {{es}} truststore. This step ensures that your cluster trusts the new CA certificate.

    ::::{note}
    On a new installation a new keystore and truststore are created automatically. If you’re running these steps on an existing {{es}} installation and you know the password to the keystore and the truststore, follow the instructions in [Update security certificates with a different CA](different-ca.md) to import the CA certificate.
    ::::


    Run the `keytool` command as shown, replacing `<password>` with a unique password for the truststore, and store the password securely:

    ```shell
    sudo /usr/share/elasticsearch/jdk/bin/keytool -importcert -trustcacerts -noprompt -keystore /etc/elasticsearch/certs/elastic-stack-ca.p12 -storepass <password> -alias new-ca -file /etc/elasticsearch/certs/ca/ca.crt
    ```

7. Ensure that the new key was added to the keystore:

    ```shell
    sudo /usr/share/elasticsearch/jdk/bin/keytool -keystore /etc/elasticsearch/certs/elastic-stack-ca.p12 -list
    ```

    ::::{note}
    The keytool utility is provided as part of the {{es}} installation and is located at: `/usr/share/elasticsearch/jdk/bin/keytool` on RPM installations.
    ::::


    Enter your password when prompted. The result should show the details for your newly added key:

    ```shell
    Keystore type: jks
    Keystore provider: SUN
    Your keystore contains 1 entry
    new-ca, Jul 12, 2023, trustedCertEntry,
    Certificate fingerprint (SHA-256): F0:86:6B:57:FC...
    ```



## Step 2: Generate a new certificate for the transport layer [install-stack-demo-secure-transport]

This guide assumes the use of self-signed certificates, but the process to import CA-signed certificates is the same. If you’re using a CA provided by your organization, you need to generate Certificate Signing Requests (CSRs) and then use the signed certificates in this step. Once the certificates are generated, whether self-signed or CA-signed, the steps are the same.

1. From the {{es}} installation directory, using the newly-created CA certificate and private key, create a new certificate for your elasticsearch node:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil cert --ca-cert /etc/elasticsearch/certs/ca/ca.crt --ca-key /etc/elasticsearch/certs/ca/ca.key
    ```

    When prompted, choose an output file name (you can use the default `elastic-certificates.p12`) and a password for the certificate.

2. Move the generated file to the `/etc/elasticsearch/certs` directory:

    ```shell
    sudo mv /usr/share/elasticsearch/elastic-certificates.p12 /etc/elasticsearch/certs/
    ```

    ::::{important}
    If you’re running these steps on a production cluster that already contains data:

    * In a cluster with multiple {{es}} nodes, before proceeding you first need to perform a [Rolling restart](../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) beginning with the node where you’re updating the keystore. Stop at the `Perform any needed changes` step, and then proceed to the next step in this guide.
    * In a single node cluster, always stop {{es}} before proceeding.

    ::::

3. Because you’ve created a new truststore and keystore, you need to update the `/etc/elasticsearch/elasticsearch.yml` settings file with the new truststore and keystore filenames.

    Open the {{es}} configuration file in a text editor and adjust the following values to reflect the newly created keystore and truststore filenames and paths:

    ```shell
    xpack.security.transport.ssl:
       ...
       keystore.path: /etc/elasticsearch/certs/elastic-certificates.p12
       truststore.path: /etc/elasticsearch/certs/elastic-stack-ca.p12
    ```



## Update the {{es}} keystore [install-stack-demo-secure-transport-es-keystore]

{{es}} uses a separate keystore to hold the passwords of the keystores and truststores holding the CA and node certificates created in the previous steps. Access to this keystore is through the use of a utility called `elasticsearch-keystore`.

1. From the {{es}} installation directory, list the contents of the existing keystore:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-keystore list
    ```

    The results should be like the following:

    ```yaml
    keystore.seed
    xpack.security.http.ssl.keystore.secure_password
    xpack.security.transport.ssl.keystore.secure_password
    xpack.security.transport.ssl.truststore.secure_password
    ```

    Notice that there are entries for:

    * The `transport.ssl.truststore` that holds the CA certificate
    * The `transport.ssl.keystore` that holds the CA-signed certificates
    * The `http.ssl.keystore` for the HTTP layer

        These entries were created at installation and need to be replaced with the passwords to the newly-created truststore and keystores.

2. Remove the existing keystore values for the default transport keystore and truststore:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-keystore remove xpack.security.transport.ssl.keystore.secure_password

    sudo /usr/share/elasticsearch/bin/elasticsearch-keystore remove xpack.security.transport.ssl.truststore.secure_password
    ```

3. Update the `elasticsearch-keystore` with the passwords for the new keystore and truststore created in the previous steps. This ensures that {{es}} can read the new stores:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password

    sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password
    ```



## Step 3: Generate new certificate(s) for the HTTP layer [install-stack-demo-secure-http]

Now that communication between {{es}} nodes (the transport layer) has been secured with SSL certificates, the same must be done for the communications that use the REST API, including {{kib}}, clients, and any other components on the HTTP layer.

1. Similar to the process for the transport layer, on the first node in your {{es}} cluster use the certificate utility to generate a CA certificate for HTTP communications:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil http
    ```

    Respond to the command prompts as follows:

    * When asked if you want to generate a CSR, enter `n`.
    * When asked if you want to use an existing CA, enter `y`.

        ::::{note}
        If you’re using your organization’s CA certificate, specify that certificate and key in the following two steps.
        ::::

    * Provide the absolute path to your newly created CA certificate: `/etc/elasticsearch/certs/ca/ca.crt`.
    * Provide the absolute path to your newly created CA key: `/etc/elasticsearch/certs/ca/ca.key`.
    * Enter an expiration value for your certificate. You can enter the validity period in years, months, or days. For example, enter `1y` for one year.
    * When asked if you want to generate one certificate per node, enter `y`.

        You’ll be guided through the creation of certificates for each node. Each certificate will have its own private key, and will be issued for a specific hostname or IP address.

        1. Enter the hostname for your first {{es}} node, for example `mynode-es1`.

            ```shell
            mynode-es1
            ```

        2. When prompted, confirm that the settings are correct.
        3. Add the network IP address that clients can use to connect to the first {{es}} node. For example `10.128.0.84`:

            ```shell
            10.128.0.84
            ```

        4. When prompted, confirm that the settings are correct.
        5. When prompted, choose to generate additional certificates, and then repeat the previous steps to add hostname and IP settings for each node in your {{es}} cluster.
        6. Provide a password for the generated `http.p12` keystore file.
        7. The generated files will be included in a zip archive. At the prompt, provide a path and filename for where the archive should be created.

            For this example we use: `/etc/elasticsearch/certs/elasticsearch-ssl-http.zip`:

            ```shell
            What filename should be used for the output zip file? [/usr/share/elasticsearch/elasticsearch-ssl-http.zip] /etc/elasticsearch/certs/elasticsearch-ssl-http.zip
            ```

2. Earlier, when you generated the certificate for the transport layer, the default filename was `elastic-certificates.p12`. Now, when generating a certificate for the HTTP layer, the default filename is `http.p12`. This matches the name of the existing HTTP layer certificate file from when the initial {{es}} cluster was first installed.

    Just to avoid any possible name collisions, rename the existing `http.p12` file to distinguish it from the newly-created keystore:

    ```shell
    sudo mv /etc/elasticsearch/certs/http.p12 /etc/elasticsearch/certs/http-old.p12
    ```

3. Unzip the generated `elasticsearch-ssl-http.zip` archive:

    ```shell
    sudo unzip -d /usr/share/elasticsearch/ /etc/elasticsearch/certs/elasticsearch-ssl-http.zip
    ```

4. When the archive is unpacked, the certificate files are located in separate directories for each {{es}} node and for the {{kib}} node.

    You can run a recursive `ls` command to view the file structure:

    ```shell
    ls -lR /usr/share/elasticsearch/{elasticsearch,kibana}
    ```

    ```shell
    elasticsearch:
    total 0
    drwxr-xr-x. 2 root root 56 Dec 12 19:13 mynode-es1
    drwxr-xr-x. 2 root root 72 Dec 12 19:04 mynode-es2
    drwxr-xr-x. 2 root root 72 Dec 12 19:04 mynode-es3

    elasticsearch/mynode-es1:
    total 8
    -rw-r--r--. 1 root root 1365 Dec 12 19:04 README.txt
    -rw-r--r--. 1 root root  845 Dec 12 19:04 sample-elasticsearch.yml

    elasticsearch/mynode-es2:
    total 12
    -rw-r--r--. 1 root root 3652 Dec 12 19:04 http.p12
    -rw-r--r--. 1 root root 1365 Dec 12 19:04 README.txt
    -rw-r--r--. 1 root root  845 Dec 12 19:04 sample-elasticsearch.yml

    elasticsearch/mynode-es3:
    total 12
    -rw-r--r--. 1 root root 3652 Dec 12 19:04 http.p12
    -rw-r--r--. 1 root root 1365 Dec 12 19:04 README.txt
    -rw-r--r--. 1 root root  845 Dec 12 19:04 sample-elasticsearch.yml

    kibana:
    total 12
    -rw-r--r--. 1 root root 1200 Dec 12 19:04 elasticsearch-ca.pem
    -rw-r--r--. 1 root root 1306 Dec 12 19:04 README.txt
    -rw-r--r--. 1 root root 1052 Dec 12 19:04 sample-kibana.yml
    ```

5. Replace your existing keystore with the new keystore. The location of your certificate directory may be different than what is shown here, depending on the installation method you chose.

    Run the `mv` command, replacing `<es1-hostname>` with the hostname of your initial {{es}} node:

    ```shell
    sudo mv /usr/share/elasticsearch/elasticsearch/<es1-hostname>/http.p12 /etc/elasticsearch/certs/
    ```

6. Because this is a new keystore, the {{es}} configuration file needs to be updated with the path to its location. Open `/etc/elasticsearch/elasticsearch.yml` and update the HTTP SSL settings with the new path:

    ```yaml
    xpack.security.http.ssl:
      enabled: true
      #keystore.path: certs/http.p12
      keystore.path: /etc/elasticsearch/certs/http.p12
    ```

7. Since you also generated a new keystore password, the {{es}} keystore needs to be updated as well. From the {{es}} installation directory, first remove the existing HTTP keystore entry:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-keystore remove xpack.security.http.ssl.keystore.secure_password
    ```

8. Add the updated HTTP keystore password, using the password you generated for this keystore:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
    ```

9. Because we’ve added files to the {{es}} configuration directory during this tutorial, we need to ensure that the permissions and ownership are correct before restarting {{es}}.

    1. Change the files to be owned by `root:elasticsearch`:

        ```shell
        sudo chown -R root:elasticsearch /etc/elasticsearch/certs/
        ```

    2. Set the files in `/etc/elasticsearch/certs` to have read and write permissions by the owner (`root`) and read permission by the `elastic` user:

        ```shell
        sudo chmod 640 /etc/elasticsearch/certs/elastic-certificates.p12
        sudo chmod 640 /etc/elasticsearch/certs/elastic-stack-ca.p12
        sudo chmod 640 /etc/elasticsearch/certs/http_ca.crt
        sudo chmod 640 /etc/elasticsearch/certs/http.p12
        ```

    3. Change the `/etc/elasticsearch/certs` and `/etc/elasticsearch/certs/ca` directories to be executable by the owner:

        ```shell
        sudo chmod 750 /etc/elasticsearch/certs
        sudo chmod 750 /etc/elasticsearch/certs/ca
        ```

10. Restart the {{es}} service:

    ```shell
    sudo systemctl start elasticsearch.service
    ```

11. Run the status command to confirm that {{es}} is running:

    ```shell
    sudo systemctl status elasticsearch.service
    ```

    In the event of any problems, you can also monitor the {{es}} logs for any issues by tailing the {{es}} log file:

    ```shell
    sudo tail -f /var/log/elasticsearch/elasticsearch-demo.log
    ```

    A line in the log file like the following indicates that SSL has been properly configured:

    ```shell
    [2023-07-12T13:11:29,154][INFO ][o.e.x.s.Security         ] [es-ssl-test] Security is enabled
    ```



## Step 4: Configure security on additional {{es}} nodes [install-stack-demo-secure-second-node]

Now that the security is configured for the first {{es}} node, some steps need to be repeated on each additional {{es}} node.

1. To avoid filename collisions, on each additional {{es}} node rename the existing `http.p12` file in the `/etc/elasticsearch/certs/` directory:

    ```shell
    mv http.p12 http-old.p12
    ```

2. Copy the CA and truststore files that you generated on the first {{es}} node so that they can be reused on all other nodes:

    * Copy the `/ca` directory (that contains `ca.crt` and `ca.key`) from `/etc/elasticsearch/certs/` on the first {{es}} node to the same path on all other {{es}} nodes.
    * Copy the `elastic-stack-ca.p12` file from `/etc/elasticsearch/certs/` to the `/etc/elasticsearch/certs/` directory on all other {{es}} nodes.
    * Copy the `http.p12` file from each node directory in `/usr/share/elasticsearch/elasticsearch` (that is, `elasticsearch/mynode-es1`, `elasticsearch/mynode-es2` and `elasticsearch/mynode-es3`) to the `/etc/elasticsearch/certs/` directory on each corresponding cluster node.

3. On each {{es}} node, repeat the steps to generate a new certificate for the transport layer:

    1. Stop the {{es}} service:

        ```shell
        sudo systemctl stop elasticsearch.service
        ```

    2. From the `/etc/elasticsearch/certs` directory, create a new certificate for the {{es}} node:

        ```shell
        sudo /usr/share/elasticsearch/bin/elasticsearch-certutil cert --ca-cert /etc/elasticsearch/certs/ca/ca.crt --ca-key /etc/elasticsearch/certs/ca/ca.key
        ```

        When prompted, choose an output file name and specify a password for the certificate. For this example, we’ll use `/etc/elasticsearch/certs/elastic-certificates.p12`.

    3. Update the `/etc/elasticsearch/elasticsearch.yml` settings file with the new truststore and keystore filename and path:

        ```shell
        xpack.security.transport.ssl:
           ...
           keystore.path: /etc/elasticsearch/certs/elastic-certificates.p12
           truststore.path: /etc/elasticsearch/certs/elastic-stack-ca.p12
        ```

    4. List the content of the {{es}} keystore:

        ```shell
        /usr/share/elasticsearch/bin/elasticsearch-keystore list
        ```

        The results should be like the following:

        ```yaml
        keystore.seed
        xpack.security.http.ssl.keystore.secure_password
        xpack.security.transport.ssl.keystore.secure_password
        xpack.security.transport.ssl.truststore.secure_password
        ```

    5. Remove the existing keystore values for the default transport keystore and truststore:

        ```shell
        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore remove xpack.security.transport.ssl.keystore.secure_password

        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore remove xpack.security.transport.ssl.truststore.secure_password
        ```

    6. Update the `elasticsearch-keystore` with the passwords for the new keystore and truststore:

        ```shell
        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password

        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password
        ```

4. For the HTTP layer, the certificates have been generated already on the first {{es}} node. Each additional {{es}} node just needs to be configured to use the new certificates.

    1. Update the `/etc/elasticsearch/elasticsearch.yml` settings file with the new truststore and keystore filenames:

        ```shell
        xpack.security.http.ssl:
          enabled: true
          #keystore.path: certs/http.p12
          keystore.path: /etc/elasticsearch/certs/http.p12
        ```

    2. Remove the existing HTTP keystore entry:

        ```shell
        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore remove xpack.security.http.ssl.keystore.secure_password
        ```

    3. Add the updated HTTP keystore password:

        ```shell
        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
        ```

    4. Change the certificate files to be owned by the `root:elasticsearch` group:

        ```shell
        sudo chown -R root:elasticsearch /etc/elasticsearch/certs/
        ```

    5. Set the files in `/etc/elasticsearch/certs` to have read and write permissions by the owner (`root`) and read permission by the `elastic` user:

        ```shell
        chmod 640 *
        ```

    6. Change the `/etc/elasticsearch/certs` and `/etc/elasticsearch/certs/ca` directories to be executable by the owner:

        ```shell
        chmod 750 /etc/elasticsearch/certs
        chmod 750 /etc/elasticsearch/certs/ca
        ```

5. Restart the {{es}} service.

    ```shell
    sudo systemctl start elasticsearch.service
    ```

6. Run the status command to confirm that {{es}} is running.

    ```shell
    sudo systemctl status elasticsearch.service
    ```



## Step 5: Generate server-side and client-side certificates for {{kib}} [install-stack-demo-secure-kib-es]

Now that the transport and HTTP layers are configured with encryption using the new certificates, there are two more tasks that must be accomplished for end-to-end connectivity to {{es}}: Set up certificates for encryption between {{kib}} and {{es}}, and between the client browser and {{kib}}. For additional details about any of these steps, refer to [Mutual TLS authentication between {{kib}} and {{es}}](./kibana-es-mutual-tls.md) and [Encrypt traffic between your browser and {{kib}}](set-up-basic-security-plus-https.md#encrypt-kibana-browser).

1. In Step 3, when you generated a new certificate for the HTTP layer, the process created an archive `elasticsearch-ssl-http.zip`.

    From the `kibana` directory in the expanded archive, copy the `elasticsearch-ca.pem` private key file to the {{kib}} host machine.

2. On the {{kib}} host machine, copy `elasticsearch-ca.pem` to the {{kib}} configuration directory (depending on the installation method that you used, the location of the configuration directory may be different from what’s shown):

    ```shell
    mv elasticsearch-ca.pem /etc/kibana
    ```

3. Stop the {{kib}} service:

    ```shell
    sudo systemctl stop kibana.service
    ```

4. Update the `/etc/kibana/kibana.yml` settings file to reflect the location of the `elasticsearch-ca.pem`:

    ```sh
    elasticsearch.ssl.certificateAuthorities: [/etc/kibana/elasticsearch-ca.pem]
    ```

5. Log in to the first {{es}} node and use the certificate utility to generate a certificate bundle for the {{kib}} server. This certificate will be used to encrypt the traffic between {{kib}} and the client’s browser. In the command, replace <DNS name> and <IP address> with the name and IP address of your {{kib}} server host:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil cert --name kibana-server --ca-cert /etc/elasticsearch/certs/ca/ca.crt --ca-key /etc/elasticsearch/certs/ca/ca.key  --dns <DNS name> --ip <IP address> --pem
    ```

    When prompted, specify a unique name for the output file, such as `kibana-cert-bundle.zip`.

6. Copy the generated archive over to your {{kib}} host and unpack it:

    ```shell
    sudo unzip kibana-cert-bundle.zip
    ```

    The unpacked archive will create a directory, `kibana-server`,  containing the new {{kib}} key and certificate:

    ```shell
    ls -l kibana-server/
    total 8
    -rw-r--r--. 1 root root 1208 May  3 16:08 kibana-server.crt
    -rw-r--r--. 1 root root 1675 May  3 16:08 kibana-server.key
    ```

7. Copy the certificate and key into `/etc/kibana`:

    ```shell
    sudo cp kibana-server.crt /etc/kibana/
    sudo cp kibana-server.key /etc/kibana/
    ```

8. Update the permissions on the certificate files to ensure that they’re readable. From inside the `/etc/kibana` directory, run:

    ```shell
    sudo chmod 640 *.crt
    sudo chmod 640 *.key
    ```

9. Open `/etc/kibana/kibana.yml` and make the following changes:

    ```sh
    server.ssl.certificate: /etc/kibana/kibana-server.crt
    server.ssl.key: /etc/kibana/kibana-server.key
    server.ssl.enabled: true
    ```

    Keep the file open for the next step.

10. To ensure that {{kib}} sessions are not invalidated, set up an encryption key by assigning any string of 32 characters or longer to the `xpack.security.encryptionKey` setting (this string will be configured in `kibana.yml` and does not need to be remembered). To generate a random string, you can use the following bash commands:

    ```shell
    cat /dev/urandom | tr -dc 'a-z0-9' | fold -w 32 | head -n 1
    ```

    Using your own string or the output of the above command sequence, add the encryption key setting to `/etc/kibana/kibana.yml`:

    ```sh
    xpack.security.encryptionKey: previously_create_string
    ```

    Save and close the file.

11. Restart the {{kib}} service:

    ```shell
    sudo systemctl start kibana.service
    ```

12. Confirm that {{kib}} is running:

    ```shell
    sudo systemctl status kibana.service
    ```

    If everything is configured correctly, connection to {{es}} will be established and {{kib}} will start normally.

13. You can also view the {{kib}} log file to gather more detail:

    ```shell
    tail -f /var/log/kibana/kibana.log
    ```

    In the log file you should find a `{{kib}} is now available` message.

14. You should now have an end-to-end ecnrypted deployment with {{es}} and {{kib}} that provides encryption between both the cluster nodes and {{kib}}, and HTTPS access to {{kib}}.

    Open a web browser to the external IP address of the {{kib}} host machine: `https://<kibana-host-address>:5601`. Note that the URL should use the `https` and not the `http` protocol.

15. Log in using the `elastic` user and password that you configured when [installing your self-managed {{stack}}](/deploy-manage/deploy/self-managed.md).

Congratulations! You’ve successfully updated the SSL certificates between {{es}} and {{kib}}.


## Step 6: Install {{fleet}} with SSL certificates configured [install-stack-demo-secure-fleet]

Now that {{kib}} is up and running, you can proceed to install {{fleet-server}}, which will manage the {{agent}} that we’ll set up in a later step.

If you’d like to learn more about these steps, refer to [Deploy on-premises and self-managed](/reference/fleet/add-fleet-server-on-prem.md) in the {{fleet}} and {{agent}} Guide. You can find detailed steps to generate and configure certificates in [Configure SSL/TLS for self-managed Fleet Servers](/reference/fleet/secure-connections.md).

1. Log in to the first {{es}} node and use the certificate utility to generate a certificate bundle for {{fleet-server}}. In the command, replace `<DNS name>` and `IP address` with the name and IP address of your {{fleet-server}} host:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil cert --name fleet-server --ca-cert /etc/elasticsearch/certs/ca/ca.crt --ca-key /etc/elasticsearch/certs/ca/ca.key  --dns <DNS name> --ip <IP address> --pem
    ```

    When prompted, specify a unique name for the output file, such as `fleet-cert-bundle.zip`.

2. On your {{fleet-server}} host, create a directory for the certificate files:

    ```shell
    sudo mkdir /etc/fleet
    ```

3. Copy the generated archive over to your {{fleet-server}} host and unpack it into `/etc/fleet/`:

    * `/etc/fleet/fleet-server.crt`
    * `/etc/fleet/fleet-server.key``

4. From the first {{es}} node, copy the `ca.crt` file, and paste it into the `/etc/fleet/` directory on the {{fleet-server}} host. Just to help identify the file we’ll also rename it to `es-ca.crt`:

    * `/etc/fleet/es-ca.crt`

5. Update the permissions on the certificate files to ensure that they’re readable. From inside the `/etc/fleet` directory, run:

    ```shell
    sudo chmod 640 *.crt
    sudo chmod 640 *.key
    ```

6. Now that the certificate files are in place, on the {{fleet-server}} host create a working directory for the installation package:

    ```shell
    mkdir fleet-install-files
    ```

7. Change into the new directory:

    ```shell
    cd fleet-install-files
    ```

8. In the terminal, run the `ifconfig` command and copy the value for the host inet IP address (for example, `10.128.0.84`). You’ll need this value later.
9. Back in your web browser, open the {{kib}} menu and go to **Management → Fleet**. {{fleet}} opens with a message that you need to add a {{fleet-server}}.
10. Click **Add Fleet Server**. The **Add a Fleet Server** flyout opens.
11. In the flyout, select the **Advanced** tab.
12. On the **Create a policy for Fleet Server** step, keep the default {{fleet-server}} policy name and all advanced options at their defaults.

    Leave the option to collect system logs and metrics selected. Click **Create policy**. The policy takes a minute or so to create.

13. On the **Choose a deployment mode for security** step, select the **Production** option. This enables you to provide your own certificates.
14. On the **Add your Fleet Server host** step:

    1. Specify a name for your {{fleet-server}} host, for example `Fleet Server`.
    2. Specify the host URL and where {{agents}} will reach {{fleet-server}}, including the default port `8220`. For example, `https://10.128.0.203:8220`.

        The URL is the inet value that you copied from the `ifconfig` output.

        For details about default port assignments, refer to [Default port assignments](/reference/fleet/add-fleet-server-on-prem.md#default-port-assignments-on-prem) in the on-premises {{fleet-server}} install documentation.

    3. Click **Add host**.

15. On the **Generate a service token** step, generate the token and save the output. The token will also be propagated automatically to the command to install {{fleet-server}}.
16. On the **Install Fleet Server to a centralized host** step, for this example we select the **Linux Tar** tab, but you can instead select the tab appropriate to the host operating system where you’re setting up {{fleet-server}}.

    Note that TAR/ZIP packages are recommended over RPM/DEB system packages, since only the former support upgrading {{fleet-server}} using {{fleet}}.

17. Run the first three commands one-by-one in the terminal on your {{fleet-server}} host.

    These commands will, respectively:

    1. Download the {{fleet-server}} package from the {{artifact-registry}}.
    2. Unpack the package archive.
    3. Change into the directory containing the install binaries.

18. Before running the provided `elastic-agent install` command, you’ll need to make a few changes:

    1. Update the paths to the correct file locations:

        * The {{es}} CA file (`es-ca.crt`)
        * The {{fleet-server}} certificate (`fleet-server.crt`)
        * The {{fleet-server}} key (`fleet-server.key`)

    2. The `fleet-server-es-ca-trusted-fingerprint` also needs to be updated. On any of your {{es}} hosts, run the following command to get the correct fingerprint to use:

        ```shell
        grep -v ^- /etc/elasticsearch/certs/ca/ca.crt | base64 -d | sha256sum
        ```

        Save the fingerprint value. You’ll need it in a later step.

        Replace the `fleet-server-es-ca-trusted-fingerprint` setting with the returned value. Your updated command should be similar to the following:

        ```shell
        sudo ./elastic-agent install -url=https://10.128.0.208:8220 \
          --fleet-server-es=https://10.128.0.84:9200 \
          --fleet-server-service-token=AAEAAWVsYXN0aWMvZmxlZXQtc2VydmPyL6Rva2VuLTE5OTg4NzAxOTM4NDU6X1I0Q1RrRHZTSWlyNHhkSXQwNEJoQQ \
          --fleet-server-policy=fleet-server-policy \
          --fleet-server-es-ca-trusted-fingerprint=92b51cf91e7fa311f8c84849224d448ca44824eb \
          --certificate-authorities=/etc/fleet/es-ca.crt \
          --fleet-server-cert=/etc/fleet/fleet-server.crt \
          --fleet-server-cert-key=/etc/fleet/fleet-server.key \
          --fleet-server-port=8220
        ```

        For details about all of the install command options, refer to [`elastic-agent install`](/reference/fleet/agent-command-reference.md#elastic-agent-install-command) in the {{agent}} command reference.

19. After you’ve made the required updates, run the `elastic-agent install` command to install {{fleet-server}}.

    When prompted, confirm that {{agent}} should run as a service. If everything goes well, the install will complete successfully:

    ```shell
    Elastic Agent has been successfully installed.
    ```

    ::::{tip}
    Wondering why the command refers to {{agent}} rather than {{fleet-server}}? {{fleet-server}} is actually a subprocess that runs inside {{agent}} with a special {{fleet-server}} policy. Refer to [What is {{fleet-server}}](/reference/fleet/fleet-server.md) to learn more.
    ::::

20. Return to the {{kib}} **Add a Fleet Server** flyout and wait for confirmation that {{fleet-server}} has connected.
21. Once the connection is confirmed, ignore the **Continue enrolling Elastic Agent** option and close the flyout.

{{fleet-server}} is now fully set up!

Before proceeding to install {{agent}}, there are a few steps needed to update the `kibana.yml` settings file with the {{es}} CA fingerprint:

1. On your {{kib}} host, stop the {{kib}} service:

    ```shell
    sudo systemctl stop kibana.service
    ```

2. Open `/etc/kibana/kibana.yml` for editing.
3. Find the `xpack.fleet.outputs` setting.
4. Update `ca_trusted_fingerprint` to the value you captured earlier, when you ran the `grep` command on the {{es}} `ca.crt` file.

    The updated entry in `kibana.yml` should be like the following:

    ```yaml
    xpack.fleet.outputs: [{id: fleet-default-output, name: default, is_default: true, is_default_monitoring: true, type: elasticsearch, hosts: [`https://10.128.0.84:9200`], ca_trusted_fingerprint: 92b51cf91e7fa311f8c84849224d448ca44824eb}]
    ```

5. Save your changes.
6. Restart {{kib}}:

    ```shell
    sudo systemctl start kibana.service
    ```

    {{kib}} is now configured with the correct fingerprint for {{agent}} to access {{es}}. You’re now ready to set up {{agent}}!



## Step 7: Install {{agent}} [install-stack-demo-secure-agent]

Next, we’ll install {{agent}} on another host and use the System integration to monitor system logs and metrics. You can find additional details about these steps in [Configure SSL/TLS for self-managed Fleet Servers](/reference/fleet/secure-connections.md).

1. Log in to the host where you’d like to set up {{agent}}.
2. Create a directory for the {{es}} certificate file:

    ```shell
    sudo mkdir /etc/agent
    ```

3. From the first {{es}} node, copy the `ca.crt` file, and paste it into the `/etc/agent/` directory on the {{fleet-server}} host. Just to help identify the file we’ll also rename it to `es-ca.crt`:

    * `/etc/fleet/es-ca.crt`

4. Create a working directory for the installation package:

    ```shell
    mkdir agent-install-files
    ```

5. Change into the new directory:

    ```shell
    cd agent-install-files
    ```

6. Open {{kib}} and go to **Management → Fleet**.
7. On the **Agents** tab, you should see your new {{fleet-server}} policy running with a healthy status.
8. Click **Add agent**. The **Add agent** flyout opens.
9. In the flyout, choose an agent policy name, for example `Demo Agent Policy`.
10. Leave **Collect system logs and metrics** enabled. This will add the [System integration](https://docs.elastic.co/integrations/system) to the {{agent}} policy.
11. Click **Create policy**.
12. For the **Enroll in Fleet?** step, leave **Enroll in Fleet** selected.
13. On the **Install Elastic Agent on your host** step, for this example we select the **Linux Tar** tab, but you can instead select the tab appropriate to the host operating system where you’re setting up {{fleet-server}}.

    As with {{fleet-server}}, note that TAR/ZIP packages are recommended over RPM/DEB system packages, since only the former support upgrading {{agent}} using {{fleet}}.

14. Run the first three commands one-by-one in the terminal on your {{agent}} host.

    These commands will, respectively:

    1. Download the {{agent}} package from the {{artifact-registry}}.
    2. Unpack the package archive.
    3. Change into the directory containing the install binaries.

15. Before running the provided `elastic-agent install` command, you’ll need to make a few changes:

    1. For the `--url` parameter, confirm that the port number is `8220` (this is the default port for on-premises {{fleet-server}}).
    2. Add a `--certificate-authorities` parameter with the full path of your CA certificate file. For example, `--certificate-authorities=/etc/agent/es-ca.crt`.

        The result should be like the following:

        ```shell
        sudo ./elastic-agent install \
        --url=https://10.128.0.203:8220 \
        --enrollment-token=VWCobFhKd0JuUnppVYQxX0VKV5E6UmU3BGk0ck9RM2HzbWEmcS4Bc1YUUM== \
        --certificate-authorities=/etc/agent/es-ca.crt
        ```

16. Run the `elastic-agent install` command.

    At the prompt, enter `Y` to install {{agent}} and run it as a service. wait for the installation to complete.

    If everything goes well, the install will complete successfully:

    ```shell
    Elastic Agent has been successfully installed.
    ```

17. In the {{kib}} **Add agent** flyout, wait for confirmation that {{agent}} has connected.
18. Wait for the **Confirm incoming data** step to complete. This may take a couple of minutes.
19. Once data is confirmed to be flowing, close the flyout.

Your new {{agent}} is now installed an enrolled with {{fleet-server}}.


## Step 8: View your system data [install-stack-demo-secure-view-data]

Now that all of the components have been installed, it’s time to view your system data.

View your system log data:

1. Open the {{kib}} menu and go to **Analytics → Dashboard**.
2. In the query field, search for `Logs System`.
3. Select the `[Logs System] Syslog dashboard` link. The {{kib}} Dashboard opens with visualizations of Syslog events, hostnames and processes, and more.

View your system metrics data:

1. Open the {{kib}} menu and return to **Analytics → Dashboard**.
2. In the query field, search for `Metrics System`.
3. Select the `[Metrics System] Host overview` link. The {{kib}} Dashboard opens with visualizations of host metrics including CPU usage, memory usage, running processes, and more.

    :::{image} /deploy-manage/images/elastic-stack-install-stack-metrics-dashboard.png
    :alt: The System metrics host overview showing CPU usage, memory usage, and other visualizations
    :::


Congratulations! You’ve successfully configured security for {{es}}, {{kib}}, {{fleet}}, and {{agent}} using your own trusted CA-signed certificates.


## What’s next? [_whats_next]

* Do you have data ready to ingest into your newly set up {{stack}}? Learn how to [add data to {{es}}](../../manage-data/ingest.md).
* Use [Elastic {{observability}}](https://www.elastic.co/observability) to unify your logs, infrastructure metrics, uptime, and application performance data.
* Want to protect your endpoints from security threats? Try [{{elastic-sec}}](https://www.elastic.co/security). Adding endpoint protection is just another integration that you add to the agent policy!
