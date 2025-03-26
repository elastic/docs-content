---
navigation_title: "Set up HTTP TLS"
applies_to:
  deployment:
    self: ga
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-basic-setup-https.html
---


% Scope: HTTP certificates setup / manual configuration / multi or single node cluster
% original title: Set up basic security for the Elastic Stack plus secured HTTPS traffic
# Set up HTTP TLS [security-basic-setup-https]

Enabling TLS on the HTTP layer ensures that all client communications with your cluster are encrypted, adding a critical layer of security.

This document provides guidance on how to:

* [Generate and configure TLS certificates for the HTTP endpoints of your {{es}} nodes](#encrypt-http-communication).
* [Configure {{kib}} to securely connect to {{es}} over HTTPS](#encrypt-kibana-elasticsearch) by trusting the Certificate Authority (CA) used by {{es}}.
* [Generate and configure TLS certificates for the {{kib}} HTTP interface to secure {{kib}} access](#encrypt-kibana-browser).

::::{note}
This guide uses the `elasticsearch-certutil` tool to generate Certificate Authorities (CAs) and TLS certificates. However, using this tool is not required. You can use publicly trusted certificates, your organization's internal certificate management system, or any other method that produces valid certificates.

If you already have certificates available, you can skip the certificate generation steps and proceed directly to the {{es}} and {{kib}} configuration steps.
::::

::::{tip}
When running `elasticsearch-certutil` in `http` mode, the tool prompts you to choose how to generate the TLS certificates. One key question is whether you want to generate a Certificate Signing Request (CSR).

* Answer `n` to skip the CSR and sign your certificates using a Certificate Authority (CA) [you previously created](./set-up-basic-security.md#generate-the-certificate-authority). You’ll be prompted to provide the path to your CA, which the tool will use to generate a `.p12` certificate. The steps in this guide follow this workflow for {{es}} certificates.
* Answer `y` to generate a CSR that can be signed by your organization's internal CA or external certificate provider. This is common in environments where trust is managed centrally. The steps in this guide follow this workflow for {{kib}} certificate.

Both workflows are supported. Choose the one that best fits your infrastructure and trust model.
::::


## Prerequisites [basic-setup-https-prerequisites]

If security feature wasn't already enabled in your cluster, complete all steps in [Manual security setup](./set-up-minimal-security.md).

For multi-node clusters, ensure you have completed the [transport TLS setup](./set-up-basic-security.md). As part of that process, you will have created a Certificate Authority (CA) that this guide reuses to issue HTTP certificates. 

If you prefer to use a separate CA for HTTP, you can generate a new one using the same process. For example:

```bash
elasticsearch-certutil ca --out http-ca.p12
```

Then, use this CA to sign your HTTP certificates in the next section and for {{kib}} HTTP endpoint.

## Generate and configure TLS certificates for {{es}} nodes [encrypt-http-communication]
% Encrypt HTTP client communications for {{es}}

Once TLS is enabled, all client communications with the cluster will be encrypted. Clients must connect using `https` and be configured to trust the Certificate Authority (CA) that signed the {{es}} certificates.

1. On **every** node in your cluster, stop {{es}} and {{kib}} if they are running.
2. On any single node, from the directory where you installed {{es}}, run the {{es}} HTTP certificate tool to generate TLS certificates for your nodes.

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


**Next**: [Encrypt HTTP client communications for {{kib}}](#encrypt-kibana-http)

## Encrypt HTTP client communications for {{kib}} [encrypt-kibana-http]

{{kib}} handles two separate types of HTTP traffic that should be encrypted:
* **Outgoing requests from {{kib}} to {{es}}**: {{kib}} acts as an HTTP client and must be configured to trust the TLS certificate used by {{es}}.
* **Incoming requests from browsers or API clients to {{kib}}**: {{kib}} acts as an HTTP server, and you should configure a TLS certificate for its public-facing endpoint to secure clients traffic.


### Encrypt traffic between {{kib}} and {{es}} [encrypt-kibana-elasticsearch]

:::{include} /deploy-manage/security/_snippets/kibana-client-https-setup.md
:::

**Next**: [Encrypt traffic between your browser and {{kib}}](#encrypt-kibana-browser)


### Encrypt traffic between your browser and {{kib}} [encrypt-kibana-browser]

:::{include} /deploy-manage/security/_snippets/kibana-https-setup.md
:::

**Next**: [Configure {{beats}} security](#configure-beats-security)

% All this should be already in beats repository, including roles, etc
## Configure {{beats}} security [configure-beats-security]

{{beats}} are open source data shippers that you install as agents on your servers to send operational data to {{es}}. Each Beat is a separately installable product. The following steps cover configuring security for {{metricbeat}}. Follow these steps for each [additional Beat](beats://reference/index.md) you want to configure security for.

### Prerequisites [_prerequisites_13]

[Install {{metricbeat}}](beats://reference/metricbeat/metricbeat-installation-configuration.md) using your preferred method.

::::{important}
You cannot connect to the {{stack}} or configure assets for {{metricbeat}} before completing the following steps.
::::



### Create roles for {{metricbeat}} [_create_roles_for_metricbeat]

Typically, you need to create the following separate roles:

* **setup** role for setting up index templates and other dependencies
* **monitoring** role for sending monitoring information
* **writer** role for publishing events collected by {{metricbeat}}
* **reader** role for {{kib}} users who need to view and create visualizations that access {{metricbeat}} data

::::{note}
These instructions assume that you are using the default name for {{metricbeat}} indices. If the indicated index names are not listed, or you are using a custom name, enter it manually when defining roles and modify the privileges to match your index naming pattern.
::::


To create users and roles from Stack Management in {{kib}}, select **Roles** or **Users** from the side navigation.

**Next**: [Create a setup role](#beats-setup-role)


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


**Next**: [Create a monitoring role](#beats-monitoring-role)


##### Create a monitoring role and user [beats-monitoring-role]

To send monitoring data securely, create a monitoring user and grant it the necessary privileges.

You can use the built-in `beats_system` user, if it’s available in your environment. Because the built-in users are not available in {{ecloud}}, these instructions create a user that is explicitly used for monitoring {{metricbeat}}.

1. If you’re using the built-in `beats_system` user, on any node in your cluster, run the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) utility to set the password for that user:

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


**Next**: [Create a writer role](#beats-writer-role)


##### Create a writer role and user [beats-writer-role]

Users who publish events to {{es}} need to create and write to {{metricbeat}} indices. To minimize the privileges required by the writer role, use the setup role to pre-load dependencies. This section assumes that you’ve [created the setup role](#beats-setup-role).

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


**Next**: [Create a reader role](#beats-reader-role)


##### Create a reader role and user [beats-reader-role]

{{kib}} users typically need to view dashboards and visualizations that contain {{metricbeat}} data. These users might also need to create and edit dashboards and visualizations. Create the reader role to assign proper privileges to these users.

1. Create the reader role:
2. Enter **metricbeat_reader** as the role name.
3. On the **metricbeat-\*** indices, choose the **read** privilege.
4. Under **{{kib}}**, click **Add {{kib}} privilege**.

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


**Next**: [Configure {{metricbeat}} to use TLS](#configure-metricbeat-tls)


#### Configure {{metricbeat}} to use TLS [configure-metricbeat-tls]

Before starting {{metricbeat}}, you configure the connections to {{es}} and {{kib}}. You can configure authentication to send data to your secured cluster using basic authentication, API key authentication, or Public Key Infrastructure (PKI) certificates.

The following instructions use the credentials for the `metricbeat_writer` and `metricbeat_setup` users that you created. If you need a greater level of security, we recommend using PKI certificates.

After configuring connections to {{es}} and {{kib}}, you’ll enable the `elasticsearch-xpack` module and configure that module to use HTTPS.

::::{warning}
In production environments, we strongly recommend using a separate cluster (referred to as the monitoring cluster) to store your data. Using a separate monitoring cluster prevents production cluster outages from impacting your ability to access your monitoring data. It also prevents monitoring activities from impacting the performance of your production cluster.
::::


1. On the node where you [generated certificates for the HTTP layer](#encrypt-http-communication), navigate to the `/kibana` directory.
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

    1. Configuring SSL is required when monitoring a node with encrypted traffic. See [Configure SSL for {{metricbeat}}](beats://reference/metricbeat/configuration-ssl.md).`hosts`
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
