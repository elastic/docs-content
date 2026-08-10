---
mapped_pages:
  - https://www.elastic.co/guide/en/elastic-stack/current/install-stack-demo-secure.html
navigation_title: Customize TLS certificates for a self-managed {{stack}}
applies_to:
  deployment:
    self:
products:
  - id: elastic-stack
  - id: elasticsearch
  - id: kibana
---
# Customize TLS certificates for a self-managed {{stack}} [install-stack-demo-secure]

This tutorial demonstrates how to replace the default certificates and keys from [Install a self-managed {{stack}}](tutorial-self-managed-install.md) with certificates and keys you create and install yourself. You start with {{es}}: TLS for node-to-node transport and for the HTTP API, and you align {{kib}} so it trusts the cluster’s HTTP certificate authority. After that, you turn on HTTPS for browsers that open {{kib}}, and you configure TLS for {{fleet-server}} and for {{agent}} hosts that enroll through it.

:::{tip}
To review the baseline security and TLS configuration established by [Install a self-managed {{stack}}](tutorial-self-managed-install.md), including {{es}} [automatic security setup](/deploy-manage/security/self-auto-setup.md) and the self-signed {{fleet-server}} certificate from the Quick Start flow, refer to [Security overview](tutorial-self-managed-install.md#security-overview).
:::

The tutorial is organized into the following phases:

- [Configure TLS certificates for the {{es}} transport layer](#install-stack-demo-secure-transport-tls)
  - Generate a new certificate authority (CA) for transport
  - Generate transport certificates for all nodes
  - Apply configuration changes and restart the nodes

- [Configure TLS certificates for the {{es}} HTTP layer](#ssl-http)
  - Generate a shared HTTP CA for the {{stack}}
  - Generate HTTP certificates for {{es}} nodes
  - Apply configuration changes and restart the cluster
  - Configure {{kib}} client to trust {{es}} HTTP CA

- [Configure HTTPS for {{kib}}](#install-stack-demo-secure-kib-https)
  - Generate server-side TLS certificates for {{kib}}
  - Apply configuration changes and restart {{kib}}

- [Configure {{fleet-server}} and {{agent}} with custom certificates](#install-stack-demo-secure-fleet-agent-tls)
  - Install {{fleet-server}} with custom TLS certificates
  - Install {{agent}}
  - View your system data

Each section is independent unless otherwise noted, so you can follow only the parts relevant to your setup. Estimated completion time is 90 minutes.

:::{note}
This tutorial does not cover mutual TLS authentication (mTLS) for HTTP client connections to {{es}}. If you require client certificate authentication, refer to the following documentation:

- [Mutual TLS authentication between {{kib}} and {{es}}](/deploy-manage/security/kibana-es-mutual-tls.md)
- [{{fleet}} and {{agent}} deployment models with mutual TLS](/reference/fleet/mutual-tls.md)
- [{{fleet}} TLS flow (one-way and mutual TLS), including output SSL options](/reference/fleet/tls-overview.md#output-ssl-options)
:::

## Before you begin 

Before starting, you must have an on-premises {{es}} cluster with {{kib}} already set up, following the steps in the tutorial [Install a self-managed {{stack}}](tutorial-self-managed-install.md).

### Verify existing configuration

As a result of the cluster installation, all your {{es}} nodes should contain the following files under `/etc/elasticsearch/certs`:

```sh
sudo ls -l /etc/elasticsearch/certs
-rw-rw----. 1 root elasticsearch  1935 ... http_ca.crt <1>
-rw-rw----. 1 root elasticsearch 10077 ... http.p12 <2>
-rw-rw----. 1 root elasticsearch  5838 ... transport.p12 <3>
```
1. HTTP CA, in PEM format
2. HTTP keystore for the node, in PKCS#12 format, including the server certificate and key, and the HTTP CA
3. Transport keystore for the node, in PKCS#12 format, including the server certificate, the key, and the transport CA

The existing `elasticsearch.yml` configuration in all nodes should include settings like the following:

```yaml subs=true
# Enable encryption for HTTP API client connections, such as {{kib}}, {{ls}}, and Agents
xpack.security.http.ssl:
  enabled: true
  keystore.path: certs/http.p12

# Enable encryption and mutual authentication between cluster nodes
xpack.security.transport.ssl:
  enabled: true
  verification_mode: certificate
  keystore.path: certs/transport.p12
  truststore.path: certs/transport.p12
```

And the {{es}} keystore in each node should include the following secure settings:

```sh
sudo /usr/share/elasticsearch/bin/elasticsearch-keystore list
xpack.security.http.ssl.keystore.secure_password
xpack.security.transport.ssl.keystore.secure_password
xpack.security.transport.ssl.truststore.secure_password
```

:::{note}
If your setup uses different certificate files or paths, or does not have TLS configured, you might need to adapt some of the steps in this tutorial accordingly.
:::

### Prepare the PKI host [preparations]

In this tutorial, `/usr/share/elasticsearch/pki` is used as a central working directory for generating and storing certificates before distributing them to the corresponding nodes.

This directory is referred to as the **PKI directory**, and the host where these steps are performed is referred to as the **PKI host**.

::::{note}
All CA and certificate generation steps in this tutorial use [`elasticsearch-certutil`](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md).

For simplicity, the examples use the first {{es}} node as the PKI host. In production environments, use a separate and secured host for PKI operations, keep CA private keys there, and distribute only the required certificate artifacts to each node.

You can run `elasticsearch-certutil` on any Linux host with access to the {{es}} distribution, for example from the extracted [`.tar.gz` archive](/deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos.md#install-linux).
::::

On the PKI host, run the following commands:

1. Create the PKI directory to store all generated certificates:

    ```sh
    sudo mkdir -p /usr/share/elasticsearch/pki
    ```

1. Install `unzip` tool, if not installed already:

    ```sh
    sudo yum install -y unzip
    ```

## Configure TLS certificates for the {{es}} transport layer [install-stack-demo-secure-transport-tls]

In this section, you create a self-signed certificate authority (CA) used to issue transport certificates for all {{es}} nodes in the cluster. These certificates can replace the existing ones, or can be used to enable transport TLS on clusters where it is not yet configured.

::::{important}
We strongly recommend using a dedicated CA per cluster for {{es}} transport security, not a CA used to sign certificates for other systems or purposes. Never use a public CA for the {{es}} transport layer. Refer to [Using an external certificate authority to secure node-to-node connections](/deploy-manage/security/external-ca-transport.md) for transport TLS certificate requirements. 
::::

### Step 1: Generate a new CA for the {{es}} transport layer [create-transport-ca]

On the host where you generate the certificates (the [PKI host](#preparations)), run the following commands:

1. Create a CA. When prompted, specify a unique name for the output file, such as `transport-ca.zip`:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil ca -pem
    ```

1. Move the output file to the `/usr/share/elasticsearch/pki/transport` directory.

    ```shell
    sudo mkdir -p /usr/share/elasticsearch/pki/transport
    sudo mv /usr/share/elasticsearch/transport-ca.zip /usr/share/elasticsearch/pki/transport/
    ```

1. Unzip the file:

    ```shell
    sudo unzip -d /usr/share/elasticsearch/pki/transport/ /usr/share/elasticsearch/pki/transport/transport-ca.zip
    ```

1. When the archive is unpacked, it creates a `ca` directory with the following files:

    ```text
    /usr/share/elasticsearch/pki/transport/
    └── ca/
        ├── ca.crt
        └── ca.key
    ```

    * `ca.crt`: The generated CA certificate.
    * `ca.key`: The certificate authority's private key.

    In the remaining steps, use this CA to generate transport certificates for all {{es}} nodes in the cluster. Keep the `ca.key` file in a secure location and do not distribute it to the nodes.

### Step 2: Generate transport certificates for all nodes [install-stack-demo-secure-transport]

In this section, you generate transport certificates for all cluster nodes using the CA created in the previous step.

::::{note}
Do not use publicly trusted certificates for the {{es}} transport layer. If you want to use a private or corporate CA, refer to [Using an external certificate authority to secure node-to-node connections](/deploy-manage/security/external-ca-transport.md) for transport certificate requirements and best practices.
::::

1. On the host where you generate the certificates (the [PKI host](#preparations)), and using the newly-created CA certificate and key, create certificates for all your {{es}} nodes:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil cert \
    --ca-cert /usr/share/elasticsearch/pki/transport/ca/ca.crt \
    --ca-key /usr/share/elasticsearch/pki/transport/ca/ca.key \
    --multiple <1>
    ```
    1. Use the [`--multiple`](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md#certutil-cert) option to generate certificates for multiple {{es}} nodes in a single command. In `elasticsearch-certutil` prompts, each node is entered as an instance name. Alternatively, run the command once per {{es}} node and specify a different output filename each time.

    When prompted:
    * Set an instance name for each node.
    * Optionally set the `IP address` and `FQDN names` for each node, for additional security.
    * Choose an output file name (you can use the default `certificate-bundle.zip`) and a password for each certificate.
    * Optionally, use the **same password** for all certificates to simplify keystore configuration in the next step.

    The following is an example of the command interactions:

    ```sh
    Enter instance name: es-node1
    Enter name for directories and files of es-node1 [es-node1]:
    Enter IP Addresses for instance (comma-separated if more than one) []:
    Enter DNS names for instance (comma-separated if more than one) []:
    Would you like to specify another instance? Press 'y' to continue entering instance information: y
    Enter instance name: es-node2
    Enter name for directories and files of es-node2 [es-node2]:
    Enter IP Addresses for instance (comma-separated if more than one) []:
    Enter DNS names for instance (comma-separated if more than one) []:
    Would you like to specify another instance? Press 'y' to continue entering instance information: y
    Enter instance name: es-node3
    Enter name for directories and files of es-node3 [es-node3]:
    Enter IP Addresses for instance (comma-separated if more than one) []:
    Enter DNS names for instance (comma-separated if more than one) []:
    Would you like to specify another instance? Press 'y' to continue entering instance information: n
    Please enter the desired output file [certificate-bundle.zip]:
    Enter password for es-node2/es-node2.p12 :
    Enter password for es-node1/es-node1.p12 :
    Enter password for es-node3/es-node3.p12 :

    Certificates written to /usr/share/elasticsearch/certificate-bundle.zip
    ```

1. Move the output file to the `/usr/share/elasticsearch/pki/transport` directory.

    ```shell
    sudo mkdir -p /usr/share/elasticsearch/pki/transport
    sudo mv /usr/share/elasticsearch/certificate-bundle.zip /usr/share/elasticsearch/pki/transport/
    ```

1. Unzip the file:

    ```shell
    sudo unzip -d /usr/share/elasticsearch/pki/transport/ /usr/share/elasticsearch/pki/transport/certificate-bundle.zip
    ```

    After extraction, `/usr/share/elasticsearch/pki/transport/` matches the structure below. The `ca/` directory holds the transport CA you created in [Step 1: Generate a new CA for the {{es}} transport layer](#create-transport-ca).

    ```text
    /usr/share/elasticsearch/pki/transport/
    ├── ca/
    │   ├── ca.crt
    │   └── ca.key
    ├── es-node1/
    │   └── es-node1.p12
    ├── es-node2/
    │   └── es-node2.p12
    └── es-node3/
        └── es-node3.p12
    ```

1. List the unpacked files for a node directory:

    ```shell
    sudo ls /usr/share/elasticsearch/pki/transport/<es-node-name>
    ```

    * `<es-node-name>.p12`: The generated certificate in PKCS#12 format, protected with the password you entered during certificate creation.

### Step 3: Distribute certificates

In this step, you copy the transport CA and node certificates to the {{es}} nodes. Each node receives only its own certificate and the shared CA.

:::{note}
This tutorial uses `scp` to copy files to a regular user's home directory and then `mv` to the {{es}} configuration directory. If your environment supports a more direct transfer method to the final destination, use that instead.
:::

After completing this step, the following files should be present on each {{es}} node:

- `/etc/elasticsearch/certs/transport_ca_new.pem`, containing the CA certificate in PEM format.
- `/etc/elasticsearch/certs/transport_cert_new.p12`, containing the node’s transport keystore in PKCS#12 format.

1. From the host used to generate all certificates (the [PKI host](#preparations)), copy the transport CA certificate and the node certificate together to each corresponding {{es}} node:

    ```sh
    sudo scp /usr/share/elasticsearch/pki/transport/ca/ca.crt \
      /usr/share/elasticsearch/pki/transport/<es-node-name>/<es-node-name>.p12 \
      <user>@<node-host>:/home/user/
    ```

    Repeat this command for each node, replacing `<es-node-hostname>` and `<es-node-host>` with the corresponding values.

1. On each {{es}} node, move the copied certificate files from that directory to the configuration directory:

    ```sh
    sudo mv /home/user/ca.crt /etc/elasticsearch/certs/transport_ca_new.pem
    sudo mv /home/user/<es-node-name>.p12 /etc/elasticsearch/certs/transport_cert_new.p12 <1>
    ```
    1. For consistency and operational simplicity, the same filename is used for the final certificate file on all {{es}} nodes. If you'd like to keep the original filenames (`<es-node-name>.p12`), make sure you update the configuration accordingly when you reach the [next step](#configure-es-tls).

1. Ensure the certificate files have the correct ownership and permissions on each {{es}} node:

   ```shell
   sudo chown -R root:elasticsearch /etc/elasticsearch/certs/
   sudo sh -c 'chmod 640 /etc/elasticsearch/certs/*'
   sudo chmod 750 /etc/elasticsearch/certs
   ```

### Step 4: Configure transport TLS on the nodes and apply changes [configure-es-tls]

There are two ways to apply the changes, depending on whether you can tolerate a short disruption of the service, or if you prefer to avoid any downtime:

- **Full cluster restart**: Simpler and faster, recommended for small clusters where a short downtime is acceptable. Update the configuration in all nodes, then stop and start all nodes.
- **Rolling restart (no downtime)**: Update the truststores to temporarily include both the existing and the new CA certificates, allowing nodes to trust old and new certificates during the transition. Then update the configuration and restart each node one at a time until all nodes use the new certificates.

Choose the approach that best fits your operational requirements.

:::{note}
In [Full cluster and rolling restart procedures](/deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md), you apply changes after you shut down all nodes (full-cluster restart), or after you shut down the current node (rolling restart).

In this tutorial, those changes are made before the stop and restart steps to reduce downtime. This order is acceptable when the changes do not affect the running node and only take effect after the service restart.
:::

#### Preparations for a rolling restart update [apply-rolling-preparations]

When replacing the transport CA, nodes using certificates signed by a new CA are not trusted by default, so a full cluster restart is typically required unless additional steps are taken.

:::{note}
These steps are only needed if you want to apply the changes one node at a time, without service disruption. If you can accommodate a full cluster restart, skip directly to [Nodes configuration](#configure-es-tls-nodes).
:::

To prepare the cluster to trust both existing and new certificates, perform the following steps on all {{es}} nodes:

1. Extract the original transport CA from the existing PKCS#12 truststore. The original CA will be needed in a later step.

    ```sh
    sudo openssl pkcs12 -in /etc/elasticsearch/certs/transport.p12 \ <1>
      -cacerts -nokeys \
      -out /etc/elasticsearch/certs/transport_ca_old.pem
    ```
    1. `transport.p12` is the name of the transport TLS truststore being used (`xpack.security.transport.ssl.truststore.path`).

    When prompted, enter the truststore password. The command creates the `/etc/elasticsearch/certs/transport_ca_old.pem` file, containing the original CA in PEM format.

    ::::{tip}
    If you don't know the password of your original truststore, you can obtain it from the {{es}} secure settings with:

    ```sh
    sudo /usr/share/elasticsearch/bin/elasticsearch-keystore show xpack.security.transport.ssl.truststore.secure_password
    ```
    ::::

1. Import the newly-created CA certificate into the existing {{es}} truststore. This step ensures that your running cluster will trust nodes presenting the new certificates:

    ```shell
    sudo /usr/share/elasticsearch/jdk/bin/keytool -importcert -trustcacerts -noprompt \
      -keystore /etc/elasticsearch/certs/transport.p12 \ <1>
      -storepass <password> -alias new-transport-ca \
      -file /etc/elasticsearch/certs/transport_ca_new.pem <2>
    ```
    1. `transport.p12` is the name of the transport TLS truststore being used (`xpack.security.transport.ssl.truststore.path`).
    2. `transport_ca_new.pem` is the newly-created transport CA, in PEM format.

    To verify that the CA was added to the truststore, run:

    ```shell
    sudo /usr/share/elasticsearch/jdk/bin/keytool \
      -keystore /etc/elasticsearch/certs/transport.p12 -list
    ```

    In the output, confirm that the `new-transport-ca` alias is present.

1. Import the original CA into the new `transport_cert_new.p12` PKCS#12 file. This step ensures that reconfigured nodes can join and communicate with existing nodes that still use the original CA.

    ```shell
    sudo /usr/share/elasticsearch/jdk/bin/keytool -importcert -trustcacerts -noprompt \
      -keystore /etc/elasticsearch/certs/transport_cert_new.p12 \ <1>
      -storepass <password> -alias old-transport-ca \ <2>
      -file /etc/elasticsearch/certs/transport_ca_old.pem <3>
    ```
    1. `transport_cert_new.p12` is the name of the new transport TLS certificate.
    2. Use the same password you used in [Step 2: Generate transport certificates](#install-stack-demo-secure-transport).
    3. `transport_ca_old.pem` is the current transport CA being used, in PEM format.

    To verify that the CA was added to the truststore, run:

    ```shell
    sudo /usr/share/elasticsearch/jdk/bin/keytool \
      -keystore /etc/elasticsearch/certs/transport_cert_new.p12 -list
    ```

    In the output, confirm that the `old-transport-ca` alias is present.


#### Nodes configuration [configure-es-tls-nodes]

On the first {{es}} node, complete the following actions to configure it to use the new certificate. The final step in this section indicates how and when to repeat the same procedure on the remaining nodes, based on the restart approach you selected.

1. Open the configuration file (`/etc/elasticsearch/elasticsearch.yml`) in a text editor and adjust the following values to reflect the newly created certificates:

    ```yaml
    # Enable encryption and mutual authentication between cluster nodes
    xpack.security.transport.ssl:
      enabled: true
      verification_mode: certificate <1>
      keystore.path: certs/transport_cert_new.p12 <2>
      truststore.path: certs/transport_cert_new.p12 <3>
    ```
    1. If you generated individual certificates for each node that include the corresponding DNS names or IP addresses, you can set the verification mode to `full`. Refer to `xpack.security.transport.ssl.verification_mode` parameter in [TLS settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#transport-tls-ssl-settings).
    2. If you created the certificates with different names, set them accordingly in every node.
    3. The truststore uses the same file name because the generated PKCS#12 file includes also the CA certificate.

1. Configure the passwords of the PKCS#12 files as [secure settings](/deploy-manage/security/secure-settings.md), using the [`elasticsearch-keystore`](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-keystore.md) utility.

    1. From the {{es}} installation directory, list the configured secure settings:

        ```shell
        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore list
        ```

        Check for the existence of the following settings in the output:

        ```yaml
        xpack.security.transport.ssl.keystore.secure_password
        xpack.security.transport.ssl.truststore.secure_password
        ```

        These secure settings contain the passwords that protect the existing PKCS#12 certificates created during the installation, and need to be replaced with the passwords of the newly-created certificates.

    1. Remove the existing settings for the default transport keystore and truststore:

        ```shell
        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore remove xpack.security.transport.ssl.keystore.secure_password
        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore remove xpack.security.transport.ssl.truststore.secure_password
        ```

    1. Add the secure settings with the password associated to the newly-created certificates. This ensures that {{es}} can read the new PKCS#12 files:

        ```shell
        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.keystore.secure_password
        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.transport.ssl.truststore.secure_password <1>
        ```
        1. Use the same password in both secure settings, as both `keystore` and `truststore` {{es}} YAML settings are pointing to the same file.

1. To apply the changes, complete the actions that match the selected approach:

    - **For a rolling restart**: Restart the node, ensure it rejoins the cluster with the new certificates, and then repeat this procedure on the next node.

      To restart a running node:
      ```sh
      sudo systemctl restart elasticsearch
      ```

      Confirm that {{es}} is running:
      ```shell
      sudo systemctl status elasticsearch.service
      ```

      If needed, monitor {{es}} logs for startup or TLS-related errors:
      ```shell
      sudo tail -f /var/log/elasticsearch/elasticsearch-demo.log
      ```

      Refer to [Rolling restart](/deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) for operational guidance and additional verification steps.

    - **For a full-cluster restart**: Repeat the previous steps on all nodes, and once all nodes are configured, stop and start the entire cluster:

      To stop the cluster, run this on all nodes:

      ```sh
      systemctl stop elasticsearch
      ```

      To start the cluster, run this on all nodes:

      ```sh
      systemctl start elasticsearch
      ```

      Refer to [Full-cluster restart](/deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-full) for operational guidance and additional verification steps.

1. After all {{es}} nodes are running with the new certificates, if you followed the rolling restart approach and [prepared the nodes for a rolling restart](#apply-rolling-preparations), remove the original CA (`old-transport-ca`) from the new truststore in all nodes:

    ```sh
    sudo /usr/share/elasticsearch/jdk/bin/keytool -delete \
      -keystore /etc/elasticsearch/certs/transport_cert_new.p12 \
      -storepass <password> \
      -alias old-transport-ca
    ```
   
## Configure TLS certificates for the {{es}} HTTP layer [ssl-http]

This section covers TLS configuration for {{es}} HTTP connections. It includes creating a shared HTTP CA that can be reused across the {{stack}}.

::::{note}
Unlike the transport layer, where using a CA dedicated exclusively to the cluster is recommended for security reasons, there are multiple valid approaches for HTTP certificates. For example, you can use certificates signed by a publicly trusted CA, or certificates signed by your organization's CA.

You can also use a single shared HTTP CA across the stack (for example, for {{es}}, {{kib}}, and {{fleet-server}} certificates), or use different CAs and certificate profiles per component to separate trust domains. Refer to [Same CA](/deploy-manage/security/same-ca.md) and [Different CA](/deploy-manage/security/different-ca.md) for more details about these trust models.
::::

### Step 1: Generate a new CA for the {{stack}} [install-stack-demo-secure-ca]

This section covers TLS configuration for HTTP connections across the {{stack}} by creating a shared HTTP CA used to sign certificates for {{es}}, {{kib}}, and {{fleet-server}}.

On the host where you generate the certificates (the [PKI host](#preparations)), run the following commands:

1. Create a new self-signed CA:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil ca -pem
    ```

    When prompted, specify a unique name for the output file, such as `elastic-stack-http-ca.zip`.

1. Move the output file to the `/usr/share/elasticsearch/pki/http` directory.

    ```shell
    sudo mkdir -p /usr/share/elasticsearch/pki/http
    sudo mv /usr/share/elasticsearch/elastic-stack-http-ca.zip /usr/share/elasticsearch/pki/http/
    ```

1. Unzip the file:

    ```shell
    sudo unzip -d /usr/share/elasticsearch/pki/http/ /usr/share/elasticsearch/pki/http/elastic-stack-http-ca.zip
    ```

1. When the archive is unpacked, it creates a `ca` directory with the following files:

    ```text
    /usr/share/elasticsearch/pki/http/
    └── ca/
        ├── ca.crt
        └── ca.key
    ```

1. Rename the files using descriptive names:

    ```shell
    sudo mv /usr/share/elasticsearch/pki/http/ca/ca.crt /usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.crt
    sudo mv /usr/share/elasticsearch/pki/http/ca/ca.key /usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.key
    ```

    The resulting structure is:

    ```text
    /usr/share/elasticsearch/pki/http/
    ├── elastic-stack-http-ca.zip
    └── ca/
        ├── elastic-stack-http-ca.crt
        └── elastic-stack-http-ca.key
    ```

    * `elastic-stack-http-ca.crt`: The generated CA certificate.
    * `elastic-stack-http-ca.key`: The certificate authority's private key.

In the rest of this tutorial, you use this CA to generate HTTP certificates across the stack, including {{es}} nodes and other components such as {{kib}} and {{fleet-server}}. Keep the CA key file in a secure location and do not distribute it to nodes.

### Step 2: Generate new HTTP certificates for {{es}} [install-stack-demo-secure-http]

In this step, you generate certificates for the {{es}} nodes using the previously-created CA for HTTP.

:::{note}
If you already obtained HTTP certificates from your security team or certificate authority, skip this step and go directly to [Step 3: Apply configuration changes and restart nodes](#configure-es-http).
:::

1. On the host where you generate the certificates (the [PKI host](#preparations)), use the [`elasticsearch-certutil`](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md) utility to create HTTP certificates for {{es}} nodes:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil http
    ```

    Respond to the command prompts as follows:

    * When asked if you want to generate a CSR, enter `n`.

      ::::{note}
      If you want to generate CSRs to be signed by an external CA, answer `y` to the CSR prompt instead.
      ::::

    * When asked if you want to use an existing CA, enter `y` and provide the CA certificate and key generated in [Step 1: Generate a shared HTTP CA for the {{stack}}](#install-stack-demo-secure-ca):
      * `/usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.crt`
      * `/usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.key`

    * Enter an expiration value for your certificate. You can enter the validity period in years, months, or days. For example, enter `1y` for one year.

    * When asked if you want to generate one certificate per node, enter `y`.

      You'll be guided through creating certificates for each node. Each certificate has its own private key and is issued for the provided hostnames and IP addresses.

      ::::{note}
      If you prefer to create a single certificate for all cluster nodes, answer `n` when prompted to generate one certificate per node, and make sure to include the IP address(es) and FQDN(s) that clients use to access the cluster.
      ::::

    * **For each certificate you create, complete the following actions:**
      1. Enter a descriptive name for the node, for example `es-node1`.
      1. Enter the list of hostnames to be added as `DNS` names in the `Subject Alternative Name` (SAN) field in your certificate.

          :::{note}
          If there's a common FQDN that you want all nodes to accept, include it in all certificates. This is useful when you access the cluster through an external load balancer or reverse proxy.
          :::
      1. When prompted, confirm that the settings are correct.
      1. Add the network IP addresses that clients can use to connect to the node. At a minimum, include the IP address of the node the certificate is intended for, for example `203.0.113.21`.

          :::{note}
          If there's a common IP address used to access the cluster, include it in all certificates. This is useful when you access the cluster through an external load balancer or reverse proxy and want to allow access by its IP address.
          :::

      1. When prompted, confirm that the settings are correct.
      1. When prompted, choose to generate additional certificates, and then repeat the previous steps for each node in your {{es}} cluster.

    * Provide a password for the generated `http.p12` keystore files.

      :::{note}
      All generated PKCS#12 certificates are protected with the same password
      :::

    * Provide a name for the output file, or accept the default `/usr/share/elasticsearch/elasticsearch-ssl-http.zip`.

    The tool generates all certificates in `/usr/share/elasticsearch/elasticsearch-ssl-http.zip`.

1. Move the output file to the `/usr/share/elasticsearch/pki/http` directory:

   ```shell
   sudo mkdir -p /usr/share/elasticsearch/pki/http
   sudo mv /usr/share/elasticsearch/elasticsearch-ssl-http.zip /usr/share/elasticsearch/pki/http/
   ```

1. Unzip the generated `elasticsearch-ssl-http.zip` archive:

   ```shell
   sudo unzip -d /usr/share/elasticsearch/pki/http/ /usr/share/elasticsearch/pki/http/elasticsearch-ssl-http.zip
   ```

1. When the archive is unpacked, the certificate files are placed in separate directories for each {{es}} node. A `ca` directory is also created for the HTTP CA, and a `kibana` directory is created so you can configure {{kib}} to trust that CA.

    ```text
    /usr/share/elasticsearch/pki/http/
    ├── elasticsearch-ssl-http.zip
    ├── elasticsearch/
    │   ├── es-node1/
    │   │   └── http.p12
    │   └── es-node2/
    │       └── http.p12
    │   └── ...
    └── kibana/
        └── elasticsearch-ca.pem
    ```

    * `http.p12`: PKCS#12 keystore for each {{es}} node, containing the node certificate and private key.
    * `elasticsearch-ca.pem`: CA certificate in PEM format, used by {{kib}} and other clients to trust {{es}} HTTP certificates. This is the same CA as `elastic-stack-http-ca.crt`.

### Step 3: Distribute HTTP certificates to {{es}} nodes

In this step, you copy the generated PKCS#12 certificates and the CA to the corresponding {{es}} nodes. The new keystore is stored as `http_new.p12`, while the existing `http.p12` remains in use until you switch over in the next step.

:::{note}
This tutorial uses `scp` to copy files to a regular user's home directory and then `mv` to the {{es}} configuration directory. If your environment supports a more direct transfer method to the final destination, use that instead.
:::

After completing this step, the following files should be present on each Elasticsearch node in `/etc/elasticsearch/certs`:

- `http.p12`, containing the currently active HTTP certificate.
- `http_new.p12`, containing the new HTTP certificate for that node.
- `elastic-stack-http-ca.crt`, containing the HTTP CA certificate in PEM format.

1. From the host where you generate the certificates (the [PKI host](#preparations)), copy each generated `http.p12` certificate and the shared HTTP CA certificate to its corresponding node:

   ```shell
   sudo scp /usr/share/elasticsearch/pki/http/elasticsearch/<es-node-hostname>/http.p12 \
     /usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.crt \
     <user>@<es-node-host>:/home/user/
   ```

   Repeat this command for each node, replacing `<es-node-hostname>` and `<es-node-host>` with the corresponding values.

1. On each {{es}} node, move the received files to the configuration directory and rename `http.p12` to `http_new.p12`:

   ```shell
   sudo mv /home/user/http.p12 /etc/elasticsearch/certs/http_new.p12
   sudo mv /home/user/elastic-stack-http-ca.crt /etc/elasticsearch/certs/elastic-stack-http-ca.crt
   ```

1. Ensure the certificate files have the correct ownership and permissions configured on each {{es}} node:

   ```shell
   sudo chown -R root:elasticsearch /etc/elasticsearch/certs/
   sudo chmod 640 /etc/elasticsearch/certs/*
   sudo chmod 750 /etc/elasticsearch/certs
   ```

### Step 4: Apply configuration changes and restart nodes [configure-es-http]

Updating HTTP certificates in {{es}} clusters can be done one node at a time, following a [rolling restart](/deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling) procedure.

:::{important}
Using new HTTP certificates signed by a different CA can affect client HTTP connections to the cluster, such as {{kib}}, {{fleet-server}}, and {{agent}} hosts. Clients that do not trust the new CA will fail to connect to {{es}}. For production environments, add the new HTTP CA to all client trust stores before applying the changes.
:::

Complete this procedure for each node in the cluster:

1. Open the configuration file (`/etc/elasticsearch/elasticsearch.yml`) in a text editor and update the HTTP SSL settings to point to the new certificate keystore:

   ```yaml
   xpack.security.http.ssl:
     enabled: true
     keystore.path: certs/http_new.p12 <1>
   ```
   1. Ensure this path matches the location of the new HTTP certificate deployed on each node.

1. Update the HTTP keystore password configured as a [secure setting](/deploy-manage/security/secure-settings.md), using the [`elasticsearch-keystore`](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-keystore.md) utility:

    1. First remove the existing entry:

        ```shell
        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore remove xpack.security.http.ssl.keystore.secure_password
        ```

    1. Add the secure setting again, using the password of the new HTTP certificate:

        ```shell
        sudo /usr/share/elasticsearch/bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
        ```

1. Restart the {{es}} service for the changes to take effect:

    ```shell
    sudo systemctl restart elasticsearch.service
    ```

1. Verify that the restarted node rejoins the cluster by following the checks in the [rolling restart procedure](/deploy-manage/maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-rolling).

    In the event of any problems, you can also monitor the {{es}} logs for any issues by tailing the {{es}} log file:

    ```shell
    sudo tail -f /var/log/elasticsearch/elasticsearch-demo.log
    ```

1. Verify that the node responds to HTTP requests with the new CA:

      ```sh
      curl -u elastic --cacert /etc/elasticsearch/certs/elastic-stack-http-ca.crt "https://<NODE_IP>:9200/_cat/nodes?v" <1>
      ```
      1. Use the node IP, hostname, or FQDN according to the SAN entries you included when generating the HTTP certificates.

1. Continue with the next node.

#### Configure {{kib}} to trust {{es}} [es-ca-kibana-trust]

When the {{es}} HTTP CA changes, {{kib}} must trust the new CA certificate to continue establishing HTTPS connections to {{es}}.

1. From the host where you generate the certificates (the [PKI host](#preparations)), copy the {{es}} CA (`elastic-stack-http-ca.crt`) from the PKI directory to the {{kib}} host machine:

   ```sh
   sudo scp /usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.crt <user>@<kibana-host>:/home/user/elastic-stack-http-ca.crt
   ```

1. On the {{kib}} host machine, move the file to the {{kib}} configuration directory:

   ```shell
   sudo mv /home/user/elastic-stack-http-ca.crt /etc/kibana
   ```

1. Update the `/etc/kibana/kibana.yml` settings file to reflect the location of the `elastic-stack-http-ca.crt`:

   ```yaml
   elasticsearch.ssl.certificateAuthorities: [ "/etc/kibana/elastic-stack-http-ca.crt" ]
   ```

1. Restart the {{kib}} service:

   ```shell
   sudo systemctl restart kibana.service
   ```

## Configure HTTPS for {{kib}} [install-stack-demo-secure-kib-https]

This section covers server-side HTTPS configuration for {{kib}}, so browser-to-{{kib}} traffic is encrypted.

::::{important}
Server-side SSL/TLS certificates for {{kib}} are strongly recommended. They are not configured automatically by default.
::::

In this tutorial, you generate a new TLS certificate for {{kib}} using the Certificate Authority (CA) created in [Generate a new HTTP CA for the {{stack}}](#install-stack-demo-secure-ca), but there are other valid options:

* If you obtain the certificates from a publicly trusted CA or from your organization's CA, copy them to your {{kib}} host, and skip directly to [Configure {{kib}} SSL server and restart](#kib-ssl-configure).
* If you prefer to create a new CA for {{kib}} HTTP, repeat the steps in [Generate a new HTTP CA for the {{stack}}](#install-stack-demo-secure-ca) and provide different file names.
* If you want to create a CSR and submit it to your organization, you can follow the example provided in [Encrypt traffic between your browser and {{kib}}](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-browser).

For additional guidance on {{kib}} security and HTTPS configuration, refer to [Configure security in {{kib}}](/deploy-manage/security/using-kibana-with-security.md) and [Set up HTTPS](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-http).

### Step 1: Generate new certificate for {{kib}} HTTP [install-stack-demo-secure-kib-es]

To create a new certificate for {{kib}} using an existing HTTP CA, complete the following actions:

1. On the host where you generate the certificates (the [PKI host](#preparations)), use the certificate utility to generate a certificate bundle for the {{kib}} server.

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil cert --name kibana-server \
      --ca-cert /usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.crt \
      --ca-key /usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.key \
      --dns <DNS name> --ip <IP address> --pem <1>
    ```
    1. Replace `<DNS name>` and `<IP address>` with the name and IP address of your {{kib}} server host.

    :::{tip}
    You can include multiple `--dns` entries if you want your certificate to serve other FQDNs.
    :::

    When prompted, specify a unique name for the output file, such as `kibana-cert-bundle.zip`.

1. Move the output archive to the PKI directory:

   ```shell
   sudo mkdir -p /usr/share/elasticsearch/pki/kibana
   sudo mv /usr/share/elasticsearch/kibana-cert-bundle.zip /usr/share/elasticsearch/pki/kibana/
   ```

1. Unzip the generated `kibana-cert-bundle.zip` archive:

   ```shell
   sudo unzip -d /usr/share/elasticsearch/pki/kibana/ /usr/share/elasticsearch/pki/kibana/kibana-cert-bundle.zip
   ```

1. The resulting bundle structure is similar to the following:

   ```text
   /usr/share/elasticsearch/pki/kibana/
   ├── kibana-cert-bundle.zip
   └── kibana-server/
       ├── kibana-server.crt
       └── kibana-server.key
   ```

   :::{note}
   The CA certificate associated with this new certificate is the shared HTTP CA created earlier (`/usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.crt`).
   :::

### Step 2: Distribute certificate files to {{kib}}

1. From the host where you generate the certificates (the [PKI host](#preparations)), copy the {{kib}} certificate and key to your {{kib}} host:

   ```shell
   sudo scp /usr/share/elasticsearch/pki/kibana/kibana-server/kibana-server.crt \
     /usr/share/elasticsearch/pki/kibana/kibana-server/kibana-server.key \
     <user>@<kibana-host>:/home/user/
   ```

   Replace `<kibana-host>` with the hostname or IP address of your {{kib}} server.

1. From the same host, copy the CA certificate associated with the {{kib}} server certificate to your {{kib}} host. In this tutorial, that CA is the shared HTTP CA generated earlier:

   ```shell
   sudo scp /usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.crt <user>@<kibana-host>:/home/user/elastic-stack-http-ca.crt
   ```

   :::{note}
   If you used a different CA to generate the {{kib}} server certificate, copy that CA certificate instead.
   :::

1. On the {{kib}} host, move the certificate files into `/etc/kibana`:

   ```shell
   sudo mv /home/user/kibana-server.crt /etc/kibana/
   sudo mv /home/user/kibana-server.key /etc/kibana/
   sudo mv /home/user/elastic-stack-http-ca.crt /etc/kibana/
   ```

1. Update the ownership and permissions on the certificate files. From inside the `/etc/kibana` directory, run:

   ```shell
   sudo chown root:kibana /etc/kibana/kibana-server.crt /etc/kibana/kibana-server.key /etc/kibana/elastic-stack-http-ca.crt
   sudo chmod 640 /etc/kibana/kibana-server.crt /etc/kibana/kibana-server.key /etc/kibana/elastic-stack-http-ca.crt
   ```

### Step 3: Configure {{kib}} SSL server and restart [kib-ssl-configure]

1. Open `/etc/kibana/kibana.yml` and make the following changes:

   ```yaml
   server.ssl.certificate: /etc/kibana/kibana-server.crt
   server.ssl.key: /etc/kibana/kibana-server.key
   server.ssl.enabled: true
   ```

1. Restart the {{kib}} service:

    ```shell
    sudo systemctl restart kibana.service
    ```

1. Confirm that {{kib}} is running:

    ```shell
    sudo systemctl status kibana.service
    ```

    If everything is configured correctly, connection to {{es}} will be established and {{kib}} will start normally.

1. You can also view the {{kib}} log file to gather more detail:

    ```shell
    tail -f /var/log/kibana/kibana.log
    ```

    Verify that the log file contains a **{{kib}} is now available** message.

1. Access {{kib}} from your browser using HTTPS (`https://<KIBANA-IP>:5601`). Log in using the `elastic` user and the password generated when you installed the first {{es}} node.

    :::{note}
    To avoid browser security warnings and ensure secure TLS validation, client browsers must trust the CA that signed the {{kib}} server certificate (`elastic-stack-http-ca.crt`), or a certificate chain that includes it.
    :::

## Configure {{fleet-server}} and {{agent}} with custom certificates [install-stack-demo-secure-fleet-agent-tls]

### Step 1: Install {{fleet-server}} with custom TLS certificates [install-stack-demo-secure-fleet]

Now that {{kib}} is up and running, you can proceed to install {{fleet-server}}, which will manage the {{agent}} that we'll set up in a later step.

Refer to [Deploy on-premises and self-managed {{fleet-server}}](/reference/fleet/add-fleet-server-on-prem.md) and [Configure SSL/TLS for self-managed {{fleet-server}}](/reference/fleet/secure-connections.md) for more detail.

1. Log in to the host where the HTTP CA was generated (the [PKI host](#preparations)) and use the certificate utility to generate a certificate bundle for {{fleet-server}}. In the command, replace `<DNS name>` and `<IP address>` with the name and IP address of your {{fleet-server}} host:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-certutil cert --name fleet-server \
      --ca-cert /usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.crt \
      --ca-key /usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.key \
      --dns <DNS name> --ip <IP address> --pem
    ```

    :::{note}
    In this tutorial, {{fleet-server}} uses the same CA as {{kib}} and {{es}} for HTTP. If you prefer to create a new CA for {{fleet-server}} certificates, repeat the steps in [Generate a new HTTP CA for the {{stack}}](#install-stack-demo-secure-ca) and provide different file names.
    :::

    When prompted, specify a unique name for the output file, such as `fleet-cert-bundle.zip`.

1. On your {{fleet-server}} host, create a directory for the certificate files:

   ```shell
   sudo mkdir /etc/fleet
   ```

1. Copy the generated archive over to your {{fleet-server}} host and unpack it into `/etc/fleet/`:
   - `/etc/fleet/fleet-server.crt`
   - `/etc/fleet/fleet-server.key`

1. Copy the {{es}} CA certificate (`/usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.crt`) into the `/etc/fleet/` directory on the {{fleet-server}} host and rename it to `es-ca.crt`:
   - `/etc/fleet/es-ca.crt`

    :::{note}
    In this tutorial, the CA used for {{es}} HTTP is also used to generate the {{fleet-server}} certificate. In other environments, these can be different CAs.
    :::

1. Update the permissions on the certificate files to ensure that they’re readable. From inside the `/etc/fleet` directory, run:

   ```shell
   sudo chmod 640 *.crt
   sudo chmod 640 *.key
   ```

1. Now that the certificate files are in place, on the {{fleet-server}} host create a working directory for the installation package:

   ```shell
   mkdir fleet-install-files
   ```

1. Change into the new directory:

   ```shell
   cd fleet-install-files
   ```

1. Obtain the host IP address for your {{fleet-server}} host (for example, by running `ifconfig`). You'll need this value later.

1. In your web browser, open {{kib}} **Management -> {{fleet}}**, click **Add {{fleet-server}}**, and select the **Advanced** tab.

1. On the **Create a policy for {{fleet-server}}** step, keep the default {{fleet-server}} policy name. Leave the option to collect system logs and metrics selected. Click **Create policy**. The policy takes a minute or so to create.

1. On the **Choose a deployment mode for security** step, select **Production**. This enables you to provide your own certificates.

1. On the **Add your {{fleet-server}} host** step:
    1. Specify a name for your {{fleet-server}} host.
    1. Specify the host URL where {{agent}}s will reach {{fleet-server}} (for example, `https://203.0.113.41:8220`). You can use the host IP address from the previous step, or a resolvable FQDN. Refer to [Default port assignments](/reference/fleet/add-fleet-server-on-prem.md#default-port-assignments-on-prem) for reference.
    1. Click **Add host**.

1. On the **Generate a service token** step, generate the token and save the output. The token will also be propagated automatically to the command to install {{fleet-server}}.

1. On the **Install {{fleet-server}} to a centralized host** step, select the **Linux Tar** tab (or the tab for your host OS). TAR/ZIP packages are recommended over RPM/DEB system packages, since only the former support upgrading {{fleet-server}} using {{fleet}}.

1. In the command block shown in {{kib}}, run the first three preparation commands. These commands do the following:

    1. Download the {{fleet-server}} package from the {{artifact-registry}}.
    1. Unpack the package archive.
    1. Change into the directory containing the install binaries.

1. Before running the `elastic-agent install` command: 
    1. Update the paths to the correct file locations:
        - The {{es}} CA file (`es-ca.crt`)
        - The {{fleet-server}} certificate (`fleet-server.crt`)
        - The {{fleet-server}} key (`fleet-server.key`)

    1. Update the `fleet-server-es-ca-trusted-fingerprint`. Run the following command to get the correct fingerprint from `es-ca.crt`:

        ```shell
        grep -v ^- /etc/fleet/es-ca.crt | base64 -d | sha256sum
        ```

        Alternatively, you can use:

        ```shell
        openssl x509 -outform der -in /etc/fleet/es-ca.crt | sha256sum
        ```
        
        Save the fingerprint value. You’ll need it in a later step.

        Replace the `fleet-server-es-ca-trusted-fingerprint setting` with the returned value. Your updated command should be similar to the following:

        ```shell
        sudo ./elastic-agent install --url=https://203.0.113.41:8220 \ <1>
          --fleet-server-es=https://203.0.113.21:9200 \ <2>
          --fleet-server-service-token=<token> \
          --fleet-server-policy=fleet-server-policy \
          --fleet-server-es-ca-trusted-fingerprint=<fingerprint> \
          --certificate-authorities=/etc/fleet/es-ca.crt \
          --fleet-server-cert=/etc/fleet/fleet-server.crt \
          --fleet-server-cert-key=/etc/fleet/fleet-server.key \
          --fleet-server-port=8220
        ```
        1. Set this to the HTTPS endpoint where {{agent}}s will connect to {{fleet-server}} (the host and port configured in the **Add your {{fleet-server}} host** step, typically port `8220`).
        2. Set this to the HTTPS endpoint of your {{es}} cluster.

        Refer to [`elastic-agent install`](/reference/fleet/agent-command-reference.md#elastic-agent-install-command) for all options.

1. Run the `elastic-agent install` command to install {{fleet-server}}.

    When prompted, confirm that {{agent}} should run as a service. The following message displays when the installation completes successfully:

    ```shell subs=true
    {{agent}} has been successfully installed.
    ```
    :::{tip}
    Wondering why the command refers to {{agent}} rather than {{fleet-server}}? {{fleet-server}} is actually a subprocess that runs inside {{agent}} with a special
    {{fleet-server}} policy. Refer to [{{fleet-server}}](/reference/fleet/index.md#fleet-server-intro) to learn more.
    :::

1. In the {{kib}} **Add a {{fleet-server}}** flyout, wait for confirmation that {{fleet-server}} has connected, then close the flyout.

    {{fleet-server}} is now fully set up.

1. Before installing {{agent}}, complete the following steps to update the `kibana.yml` settings file with the {{es}} CA fingerprint:

    :::{note}
    You can also configure this in the {{fleet}} UI by going to **Settings** -> **Outputs**, editing the default output, and setting the CA trusted fingerprint there.
    :::

    1. On your {{kib}} host, stop the {{kib}} service:
       ```shell
       sudo systemctl stop kibana.service
       ```

    1. Open `/etc/kibana/kibana.yml` for editing.
    1. Find the `xpack.fleet.outputs` setting.
    1. Update `ca_trusted_fingerprint` to the value you captured earlier, when you ran the `grep` command on the {{es}} `es-ca.crt` file.

       The updated entry in `kibana.yml` should be like the following:
       ```shell
       xpack.fleet.outputs: [{id: fleet-default-output, name: default, is_default: true, is_default_monitoring: true, type: elasticsearch, hosts: [`https://203.0.113.21:9200`], ca_trusted_fingerprint: 92b51cf91e7fa311f8c84849224d448ca44824eb}]
       ```
    1. Save your changes.
    1. Start {{kib}}:
       ```shell
       sudo systemctl start kibana.service
       ```
       {{kib}} is now configured with the correct fingerprint for {{agent}} to access {{es}}. You’re now ready to set up {{agent}}!

### Step 2: Install {{agent}} [install-stack-demo-secure-agent]

Next, we'll install {{agent}} on another host and use the System integration to monitor system logs and metrics. See [Configure SSL/TLS for self-managed {{fleet-server}}](/reference/fleet/secure-connections.md) for more detail.

1. Log in to the host where you'd like to set up {{agent}}.

1. Create a directory for the {{fleet-server}} CA certificate file:

   ```shell
   sudo mkdir /etc/agent
   ```

1. From the host where you generate the certificates (the [PKI host](#preparations)), copy the CA certificate used to generate the {{fleet-server}} certificate into `/etc/agent/` on the agent host and rename it to `fleet-server-ca.crt`:
   - `/etc/agent/fleet-server-ca.crt`

    :::{note}
    {{agent}} needs to trust the CA that issued the {{fleet-server}} certificate. In this tutorial, that CA is the same as the {{es}} HTTP CA (`/usr/share/elasticsearch/pki/http/ca/elastic-stack-http-ca.crt`), but these can be different in other environments.

    {{agent}} also needs to trust {{es}}, but that trust is delivered after enrollment through {{fleet}} policies and the configured {{es}} outputs, including the CA fingerprint configured earlier.
    :::

1. Create a working directory for the installation package:
   ```shell
   mkdir agent-install-files
   ```

1. Change into the new directory:
   ```shell
   cd agent-install-files
   ```

1. In {{kib}}, go to **Management -> {{fleet}}**. On the **Agents** tab, you should see your new {{fleet-server}} policy running with a healthy status.

1. Click **Add agent**, choose a policy name (e.g. `Demo Agent Policy`), and leave **Collect system logs and metrics** enabled (this adds the [System integration](https://docs.elastic.co/integrations/system)). Click **Create policy**.

1. For the **Enroll in {{fleet}}?** step, leave **Enroll in {{fleet}}** selected.

1. On the **Install {{agent}} on your host** step, select the **Linux Tar** tab, or use the tab matching your operating system where you're setting up {{fleet-server}}.

    As with {{fleet-server}}, note that TAR/ZIP packages are recommended over RPM/DEB system packages, since only the former support upgrading {{agent}} using {{fleet}}.

1. In the command block shown in {{kib}}, run the first three preparation commands in the terminal on your {{agent}} host. These commands do the following:

    1. Download the {{agent}} package from the {{artifact-registry}}.
    1. Unpack the package archive.
    1. Change into the directory containing the install binaries.

1. Before running the `elastic-agent install` command, make the following changes:

    1. For the `--url` parameter, confirm that the port number is `8220` (this is the default port for on-premises {{fleet-server}}).
    1. Add a `--certificate-authorities` parameter with the full path of your CA certificate file. For example, `--certificate-authorities=/etc/agent/fleet-server-ca.crt`.

    The result should be like the following:

    ```shell
    sudo ./elastic-agent install \
    --url=https://203.0.113.41:8220 \ <1>
    --enrollment-token=<token> \
    --certificate-authorities=/etc/agent/fleet-server-ca.crt
    ```
    1. Ensure the value matches the {{fleet-server}} URL you configured earlier.

1. Run the `elastic-agent install` command. Enter `Y` when prompted. Wait for the **Add agent** flyout to show the agent as connected and for **Confirm incoming data** to complete, then close the flyout.

Your new {{agent}} is now installed and enrolled with {{fleet-server}}.

### Step 3: View your system data [install-stack-demo-secure-view-data]

Use the following validation steps to view your system data.

**View your system log data:**

1. Open the {{kib}} menu and go to **Analytics -> Dashboard**.
1. In the query field, search for `Logs System`.
1. Select the `[Logs System] Syslog dashboard` link. The {{kib}} Dashboard opens with visualizations of Syslog events, hostnames and processes, and more.

**View your system metrics data:**

1. Open the {{kib}} menu and return to **Analytics -> Dashboard**.
1. In the query field, search for `Metrics System`.
1. Select the `[Metrics System] Host overview` link. The {{kib}} Dashboard opens with visualizations of host metrics including CPU usage, memory usage, running processes, and others.

![Sample {{kib}} dashboard](/deploy-manage/images/install-stack-metrics-dashboard.png)

Congratulations! You've successfully configured security for {{es}}, {{kib}}, {{fleet}}, and {{agent}} using your own trusted CA-signed certificates.

## Next steps [install-stack-demo-secure-next-steps]

Now that you’ve successfully installed and secured an on-premises {{stack}}, learn how to bring in data and start exploring:

* Do you have data ready to ingest? Learn how to [bring your data to Elastic](/manage-data/ingest.md).
* Use [Elastic {{observability}}](https://www.elastic.co/observability) to unify your logs, infrastructure metrics, uptime, and application performance data.
* Want to protect your endpoints from security threats? Try [{{elastic-sec}}](https://www.elastic.co/security). Adding endpoint protection is just another integration that you add to the agent policy!
