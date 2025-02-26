---
navigation_title: "Set up basic security plus HTTPS"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html
---



# Set up basic security plus HTTPS [security-basic-setup-https]


When you enable TLS on the HTTP layer it provides an additional layer of security to ensure that all communications to and from your cluster are encrypted.

When you run the `elasticsearch-certutil` tool in `http` mode, the tool asks several questions about how you want to generate certificates. While there are numerous options, the following choices result in certificates that should work for most environments.

::::{admonition} Signing certificates
:name: signing-certificates

The first question that the `elasticsearch-certutil` tool prompts you with is whether you want to generate a Certificate Signing Request (CSR). Answer `n` if you want to sign your own certificates, or `y` if you want to sign certificates with a central CA.


#### Sign your own certificates [_sign_your_own_certificates]

If you want to use the CA that you created when [Generating the certificate authority](secure-cluster-communications.md#generate-certificates) answer `n` when asked if you want to generate a CSR. You then specify the location of your CA, which the tool uses to sign and generate a `.p12` certificate. The steps in this procedure follow this workflow.


#### Sign certificates with a central CA [_sign_certificates_with_a_central_ca]

If you work in an environment with a central security team, they can likely generate a certificate for you. Infrastructure within your organization might already be configured to trust an existing CA, so it may be easier for clients to connect to {{es}} if you use a CSR and send that request to the team that controls your CA. To use a central CA, answer `y` to the first question.

::::


## Prerequisites [basic-setup-https-prerequisites]

Complete all steps in [Set up basic security for the Elastic Stack](secure-cluster-communications.md).


## Encrypt HTTP client communications for {{es}} [encrypt-http-communication]

1. On **every** node in your cluster, stop {{es}} and {{kib}} if they are running.
2. On any single node, from the directory where you installed {{es}}, run the {{es}} HTTP certificate tool to generate a Certificate Signing Request (CSR).

    ```shell
    ./bin/elasticsearch-certutil http
    ```

    This command generates a `.zip` file that contains certificates and keys to use with {{es}} and {{kib}}. Each folder contains a `README.txt` explaining how to use these files.

    1. When asked if you want to generate a CSR, enter `n`.
    2. When asked if you want to use an existing CA, enter `y`.
    3. Enter the path to your CA. This is the absolute path to the `elastic-stack-ca.p12` file that you generated for your cluster.
    4. Enter the password for your CA.
    5. Enter an expiration value for your certificate. You can enter the validity period in years, months, or days. For example, enter `90D` for 90 days.
    6. When asked if you want to generate one certificate per node, enter `y`.

        Each certificate will have its own private key, and will be issued for a specific hostname or IP address.

    7. When prompted, enter the name of the first node in your cluster. Use the same node name that you used when [generating node certificates](secure-cluster-communications.md#generate-certificates).
    8. Enter all hostnames used to connect to your first node. These hostnames will be added as DNS names in the Subject Alternative Name (SAN) field in your certificate.

        List every hostname and variant used to connect to your cluster over HTTPS.

    9. Enter the IP addresses that clients can use to connect to your node.
    10. Repeat these steps for each additional node in your cluster.

3. After generating a certificate for each of your nodes, enter a password for your private key when prompted.
4. Unzip the generated `elasticsearch-ssl-http.zip` file. This compressed file contains one directory for both {{es}} and {{kib}}.

    ```txt
    /elasticsearch
    |_ README.txt
    |_ http.p12
    |_ sample-elasticsearch.yml
    ```

    ```txt
    /kibana
    |_ README.txt
    |_ elasticsearch-ca.pem
    |_ sample-kibana.yml
    ```

5. On **every** node in your cluster, complete the following steps:

    1. Copy the relevant `http.p12` certificate to the `$ES_PATH_CONF` directory.
    2. Edit the `elasticsearch.yml` file to enable HTTPS security and specify the location of the `http.p12` security certificate.

        ```yaml
        xpack.security.http.ssl.enabled: true
        xpack.security.http.ssl.keystore.path: http.p12
        ```

    3. Add the password for your private key to the secure settings in {{es}}.

        ```shell
        ./bin/elasticsearch-keystore add xpack.security.http.ssl.keystore.secure_password
        ```

    4. Start {{es}}.


**Next**: [Encrypt HTTP client communications for {{kib}}](secure-http-communications.md#encrypt-kibana-http)


## Encrypt HTTP client communications for {{kib}} [encrypt-kibana-http]

Browsers send traffic to {{kib}} and {{kib}} sends traffic to {{es}}. These communication channels are configured separately to use TLS. You encrypt traffic between {{kib}} and {{es}}, and then encrypt traffic between your browser and {{kib}}.

### Encrypt traffic between {{kib}} and {{es}} [encrypt-kibana-elasticsearch]

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
If the Elastic monitoring features are enabled and you configured a separate {{es}} monitoring cluster, you can also configure {{kib}} to connect to the monitoring cluster via HTTPS. The steps are the same, but each setting is prefixed by `monitoring`. For example, `monitoring.ui.elasticsearch.hosts` and `monitoring.ui.elasticsearch.ssl.truststore.path`.

::::{note}
You must create a separate `elasticsearch-ca.pem` security file for the monitoring cluster.
::::


:::::


**Next**: [Encrypt traffic between your browser and {{kib}}](secure-http-communications.md#encrypt-kibana-browser)


### Encrypt traffic between your browser and {{kib}} [encrypt-kibana-browser]

You create a server certificate and private key for {{kib}}. {{kib}} uses this server certificate and corresponding private key when receiving connections from web browsers.

When you obtain a server certificate, you must set its subject alternative name (SAN) correctly to ensure that browsers will trust it. You can set one or more SANs to the {{kib}} server’s fully-qualified domain name (FQDN), hostname, or IP address. When choosing the SAN, pick whichever attribute you’ll use to connect to {{kib}} in your browser, which is likely the FQDN.

The following instructions create a Certificate Signing Request (CSR) for {{kib}}. A CSR contains information that a CA uses to generate and sign a security certificate. The certificate can be trusted (signed by a public, trusted CA) or untrusted (signed by an internal CA). A self-signed or internally-signed certificate is acceptable for development environments and building a proof of concept, but should not be used in a production environment.

::::{warning}
Before going to production, use a trusted CA such as [Let’s Encrypt](https://letsencrypt.org/) or your organization’s internal CA to sign the certificate. Using a signed certificate establishes browser trust for connections to {{kib}} for internal access or on the public internet.
::::


1. Generate a server certificate and private key for {{kib}}.

    ```shell
    ./bin/elasticsearch-certutil csr -name kibana-server -dns example.com,www.example.com
    ```

    The CSR has a common name (CN) of `kibana-server`, a SAN of `example.com`, and another SAN of `www.example.com`.

    This command generates a `csr-bundle.zip` file by default with the following contents:

    ```txt
    /kibana-server
    |_ kibana-server.csr
    |_ kibana-server.key
    ```

2. Unzip the `csr-bundle.zip` file to obtain the `kibana-server.csr` unsigned security certificate and the `kibana-server.key` unencrypted private key.
3. Send the `kibana-server.csr` certificate signing request to your internal CA or trusted CA for signing to obtain a signed certificate. The signed file can be in different formats, such as a `.crt` file like `kibana-server.crt`.
4. Open `kibana.yml` and add the following lines to configure {{kib}} to access the server certificate and unencrypted private key.

    ```yaml
    server.ssl.certificate: $KBN_PATH_CONF/kibana-server.crt
    server.ssl.key: $KBN_PATH_CONF/kibana-server.key
    ```

    ::::{note}
    `$KBN_PATH_CONF` contains the path for the {{kib}} configuration files. If you installed {{kib}} using archive distributions (`zip` or `tar.gz`), the path defaults to `$KBN_HOME/config`. If you used package distributions (Debian or RPM), the path defaults to `/etc/kibana`.
    ::::

5. Add the following line to `kibana.yml` to enable TLS for inbound connections.

    ```yaml
    server.ssl.enabled: true
    ```

6. Start {{kib}}.

::::{note}
After making these changes, you must always access {{kib}} via HTTPS. For example, `https://<your_kibana_host>.com`.
::::


**Next**: [Configure {{beats}} security](secure-http-communications.md#configure-beats-security)



## Configure {{beats}} security [configure-beats-security]

{{beats}} are open source data shippers that you install as agents on your servers to send operational data to {{es}}. Each Beat is a separately installable product. The following steps cover configuring security for {{metricbeat}}. Follow these steps for each [additional Beat](asciidocalypse://docs/beats/docs/reference/index.md) you want to configure security for.

### Prerequisites [_prerequisites_13]

[Install {{metricbeat}}](asciidocalypse://docs/beats/docs/reference/metricbeat/metricbeat-installation-configuration.md) using your preferred method.

::::{important}
You cannot connect to the {{stack}} or configure assets for {{metricbeat}} before completing the following steps.
::::



### Create roles for {{metricbeat}} [_create_roles_for_metricbeat]

Typically, you need to create the following separate roles:

* **setup** role for setting up index templates and other dependencies
* **monitoring** role for sending monitoring information
* **writer** role for publishing events collected by {{metricbeat}}
* **reader** role for Kibana users who need to view and create visualizations that access {{metricbeat}} data

::::{note}
These instructions assume that you are using the default name for {{metricbeat}} indices. If the indicated index names are not listed, or you are using a custom name, enter it manually when defining roles and modify the privileges to match your index naming pattern.
::::


To create users and roles from Stack Management in {{kib}}, select **Roles** or **Users** from the side navigation.

**Next**: [Create a setup role](secure-http-communications.md#beats-setup-role)


##### Create a setup role and user [beats-setup-role]

Administrators who set up {{metricbeat}} typically need to load mappings, dashboards, and other objects used to index data into {{es}} and visualize it in {{kib}}.

::::{warning}
Setting up {{metricbeat}} is an admin-level task that requires extra privileges. As a best practice, grant the setup role to administrators only, and use a more restrictive role for event publishing.
::::


1. Create the setup role:
2. Enter **metricbeat_setup** as the role name.
3. Choose the **monitor** and **manage_ilm** cluster privileges.
4. On the **metricbeat-\** indices, choose the ***manage** and **write** privileges.

    If the **metricbeat-\*** indices aren’t listed, enter that pattern into the list of indices.

5. Create the setup user:
6. Enter **metricbeat_setup** as the user name.
7. Enter the username, password, and other user details.
8. Assign the following roles to the **metricbeat_setup** user:

    | Role | Purpose |
    | --- | --- |
    | `metricbeat_setup` | Set up {{metricbeat}}. |
    | `kibana_admin` | Load dependencies, such as example dashboards, if available, into {{kib}} |
    | `ingest_admin` | Set up index templates and, if available, ingest pipelines |


**Next**: [Create a monitoring role](secure-http-communications.md#beats-monitoring-role)


##### Create a monitoring role and user [beats-monitoring-role]

To send monitoring data securely, create a monitoring user and grant it the necessary privileges.

You can use the built-in `beats_system` user, if it’s available in your environment. Because the built-in users are not available in {{ecloud}}, these instructions create a user that is explicitly used for monitoring {{metricbeat}}.

1. If you’re using the built-in `beats_system` user, on any node in your cluster, run the [`elasticsearch-reset-password`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/reset-password.md) utility to set the password for that user:

    This command resets the password for the `beats_system` user to an auto-generated value.

    ```shell
    ./bin/elasticsearch-reset-password -u beats_system
    ```

    If you want to set the password to a specific value, run the command with the interactive (`-i`) parameter.

    ```shell
    ./bin/elasticsearch-reset-password -i -u beats_system
    ```

2. Create the monitoring role:
3. Enter **metricbeat_monitoring** as the role name.
4. Choose the **monitor** cluster privilege.
5. On the **.monitoring-beats-\** indices, choose the ***create_index** and **create_doc** privileges.
6. Create the monitoring user:
7. Enter **metricbeat_monitoring** as the user name.
8. Enter the username, password, and other user details.
9. Assign the following roles to the **metricbeat_monitoring** user:

    | Role | Purpose |
    | --- | --- |
    | `metricbeat_monitoring` | Monitor {{metricbeat}}. |
    | `kibana_admin` | Use {{kib}} |
    | `monitoring_user` | Use Stack Monitoring in {{kib}} to monitor {{metricbeat}} |


**Next**: [Create a writer role](secure-http-communications.md#beats-writer-role)


##### Create a writer role and user [beats-writer-role]

Users who publish events to {{es}} need to create and write to {{metricbeat}} indices. To minimize the privileges required by the writer role, use the setup role to pre-load dependencies. This section assumes that you’ve [created the setup role](secure-http-communications.md#beats-setup-role).

1. Create the writer role:
2. Enter **metricbeat_writer** as the role name.
3. Choose the **monitor** and **read_ilm** cluster privileges.
4. On the **metricbeat-\** indices, choose the ***create_doc***, ***create_index**, and **view_index_metadata** privileges.
5. Create the writer user:
6. Enter **metricbeat_writer** as the user name.
7. Enter the username, password, and other user details.
8. Assign the following roles to the **metricbeat_writer** user:

    | Role | Purpose |
    | --- | --- |
    | `metricbeat_writer` | Monitor {{metricbeat}} |
    | `remote_monitoring_collector` | Collect monitoring metrics from {{metricbeat}} |
    | `remote_monitoring_agent` | Send monitoring data to the monitoring cluster |


**Next**: [Create a reader role](secure-http-communications.md#beats-reader-role)


##### Create a reader role and user [beats-reader-role]

{{kib}} users typically need to view dashboards and visualizations that contain {{metricbeat}} data. These users might also need to create and edit dashboards and visualizations. Create the reader role to assign proper privileges to these users.

1. Create the reader role:
2. Enter **metricbeat_reader** as the role name.
3. On the **metricbeat-\*** indices, choose the **read** privilege.
4. Under **Kibana**, click **Add Kibana privilege**.

    * Under **Spaces**, choose **Default**.
    * Choose **Read** or **All** for Discover, Visualize, Dashboard, and Metrics.

5. Create the reader user:
6. Enter **metricbeat_reader** as the user name.
7. Enter the username, password, and other user details.
8. Assign the following roles to the **metricbeat_reader** user:

    | Role | Purpose |
    | --- | --- |
    | `metricbeat_reader` | Read {{metricbeat}} data. |
    | `monitoring_user` | Allow users to monitor the health of {{metricbeat}}itself. Only assign this role to users who manage {{metricbeat}} |
    | `beats_admin` | Create and manage configurations in {{beats}} centralmanagement. Only assign this role to users who need to use {{beats}} centralmanagement. |


**Next**: [Configure {{metricbeat}} to use TLS](secure-http-communications.md#configure-metricbeat-tls)


#### Configure {{metricbeat}} to use TLS [configure-metricbeat-tls]

Before starting {{metricbeat}}, you configure the connections to {{es}} and {{kib}}. You can configure authentication to send data to your secured cluster using basic authentication, API key authentication, or Public Key Infrastructure (PKI) certificates.

The following instructions use the credentials for the `metricbeat_writer` and `metricbeat_setup` users that you created. If you need a greater level of security, we recommend using PKI certificates.

After configuring connections to {{es}} and {{kib}}, you’ll enable the `elasticsearch-xpack` module and configure that module to use HTTPS.

::::{warning}
In production environments, we strongly recommend using a separate cluster (referred to as the monitoring cluster) to store your data. Using a separate monitoring cluster prevents production cluster outages from impacting your ability to access your monitoring data. It also prevents monitoring activities from impacting the performance of your production cluster.
::::


1. On the node where you [generated certificates for the HTTP layer](secure-http-communications.md#encrypt-http-communication), navigate to the `/kibana` directory.
2. Copy the `elasticsearch-ca.pem` certificate to the directory where you installed {{metricbeat}}.
3. Open the `metricbeat.yml` configuration file and configure the connection to {{es}}.

    Under `output.elasticsearch`, specify the following fields:

    ```yaml
    output.elasticsearch:
     hosts: ["<your_elasticsearch_host>:9200"]
     protocol: "https"
     username: "metricbeat_writer"
     password: "<password>"
     ssl:
       certificate_authorities: ["elasticsearch-ca.pem"]
       verification_mode: "certificate"
    ```

    `hosts`
    :   Specifies the host where your {{es}} cluster is running.

    `protocol`
    :   Indicates the protocol to use when connecting to {{es}}. This value must be `https`.

    `username`
    :   Name of the user with privileges required to publish events to {{es}}. The `metricbeat_writer` user that you created has these privileges.

    `password`
    :   Password for the indicated `username`.

    `certificate_authorities`
    :   Indicates the path to the local `.pem` file that contains your CA’s certificate.

4. Configure the connection to {{kib}}.

    Under `setup.kibana`, specify the following fields:

    ```yaml
    setup.kibana
     host: "https://<your_elasticsearch_host>:5601"
     ssl.enabled: true
     username: "metricbeat_setup"
     password: "p@ssw0rd"
    ```

    `hosts`
    :   The URLs of the {{es}} instances to use for all your queries. Ensure that you include `https` in the URL.

    `username`
    :   Name of the user with privileges required to set up dashboards in {{kib}}. The `metricbeat_setup` user that you created has these privileges.

    `password`
    :   Password for the indicated `username`.

5. Enable the `elasticsearch-xpack` module.

    ```shell
    ./metricbeat modules enable elasticsearch-xpack
    ```

6. Modify the `elasticsearch-xpack` module to use HTTPS. This module collects metrics about {{es}}.

    Open `/modules.d/elasticsearch-xpack.yml` and specify the following fields:

    ```yaml
    - module: elasticsearch
     xpack.enabled: true
     period: 10s
     hosts: ["https://<your_elasticsearch_host>:9200"]
     username: "remote_monitoring_user"
     password: "<password>"
     ssl:     <1>
       enabled: true
       certificate_authorities: ["elasticsearch-ca.pem"]
       verification_mode: "certificate"
    ```

    1. Configuring SSL is required when monitoring a node with encrypted traffic. See [Configure SSL for {{metricbeat}}](asciidocalypse://docs/beats/docs/reference/metricbeat/configuration-ssl.md).`hosts`
    :   Specifies the host where your {{es}} cluster is running. Ensure that you include `https` in the URL.

    `username`
    :   Name of the user with privileges to collect metric data. The built-in `monitoring_user` user has these privileges. Alternatively, you can create a user and assign it the `monitoring_user` role.

    `password`
    :   Password for the indicated `username`.

    `certificate_authorities`
    :   Indicates the path to the local `.pem` file that contains your CA’s certificate.

7. If you want to use the predefined assets for parsing, indexing, and visualizing your data, run the following command to load these assets:

    ```shell
    ./metricbeat setup -e
    ```

8. Start {{es}}, and then start {{metricbeat}}.

    ```shell
    ./metricbeat -e
    ```

    `-e` is optional and sends output to standard error instead of the configured log output.

9. Log in to {{kib}}, open the main menu, and click **Stack Monitoring**.

    You’ll see cluster alerts that require your attention and a summary of the available monitoring metrics for {{es}}. Click any of the header links on the available cards to view additional information.
