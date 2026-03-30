---
mapped_pages:
  - https://www.elastic.co/guide/en/elastic-stack/current/installing-stack-demo-self.html
navigation_title: Install a self-managed {{stack}}
applies_to:
  deployment:
    self:
products:
  - id: elastic-stack
  - id: elasticsearch
  - id: kibana
  - id: elastic-agent
  - id: fleet
---
# Tutorial 1: Install a self-managed {{stack}} [installing-stack-demo-self]

This tutorial demonstrates how to install and configure the latest {{version.stack}} version of the {{stack}} in a self-managed environment. Following these steps sets up a three node {{es}} cluster, with {{kib}}, {{fleet-server}}, and {{agent}}, each on separate hosts. The {{agent}} is configured with the System integration, enabling it to gather local system logs and metrics and deliver them into the {{es}} cluster. Finally, the tutorial shows how to view the system data in {{kib}}.

::::{note}
This installation flow relies on the {{es}} [automatic security setup](/deploy-manage/security/self-auto-setup.md), which secures {{es}} by default during the initial installation.

If you plan to use custom certificates (for example, corporate-provided or publicly trusted certificates), or if you need to configure HTTPS for browser-to-{{kib}} communication, you can follow this tutorial in combination with [Tutorial 2: Customize certificates for a self-managed {{stack}}](tutorial-self-managed-secure.md) at the appropriate stage of the installation.

For more details, refer to [Security overview](#security-overview).
::::

It should take between one and two hours to complete these steps.

* [Prerequisites and assumptions](#install-stack-self-prereqs)
* [{{stack}} overview](#install-stack-self-overview)
* [Security overview](#security-overview)
* [Step 1: Set up the first {{es}} node](#install-stack-self-elasticsearch-first)
* [Step 2: Configure the first {{es}} node for connectivity](#install-stack-self-elasticsearch-config)
* [Step 3: Start {{es}}](#install-stack-self-elasticsearch-start)
* [Step 4: Set up a second {{es}} node](#install-stack-self-elasticsearch-second)
* [Step 5: Set up additional {{es}} nodes](#install-stack-self-elasticsearch-third)
* [Step 6: Consolidate {{es}} configuration](#install-stack-self-elasticsearch-consolidate)
* [Step 7: Install {{kib}}](#install-stack-self-kibana)
* [Step 8: Install {{fleet-server}}](#install-stack-self-fleet-server)
* [Step 9: Install {{agent}}](#install-stack-self-elastic-agent)
* [Step 10: View your system data](#install-stack-self-view-data)
* [Next steps](#install-stack-self-next-steps)

## Prerequisites and assumptions [install-stack-self-prereqs]

To get started, you need the following:

* A set of virtual or physical hosts on which to install each stack component.
* On each host, a user account with `sudo` privileges, and `curl` installed.

The examples in this guide use RPM Package Manager (RPM) packages to install the {{stack}} {{version.stack}} components on hosts running Red Hat Enterprise Linux or a compatible distribution such as Rocky Linux.

For the full list of supported operating systems and platforms, refer to the [Elastic Support Matrix](https://www.elastic.co/support/matrix).

The packages needed by this tutorial are:

* [elasticsearch-{{version.stack}}-x86_64.rpm](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{version.stack}}-x86_64.rpm)
* [kibana-{{version.stack}}-x86_64.rpm](https://artifacts.elastic.co/downloads/kibana/kibana-{{version.stack}}-x86_64.rpm)
* [https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-linux-x86_64.tar.gz](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-linux-x86_64.tar.gz)

:::{note}
For {{agent}} and {{fleet-server}} (both of which use the elastic-agent-{{version.stack}}-linux-x86_64.tar.gz package) we recommend using TAR/ZIP packages over RPM/DEB system packages, since only the former support upgrading using {{fleet}}.
:::

Special considerations such as firewalls and proxy servers are not covered here.

For the basic ports and protocols required for the installation to work, refer to the following overview section.

## {{stack}} overview [install-stack-self-overview]

Before starting, take a moment to familiarize yourself with the {{stack}} components.

![Overview of the Elastic Stack components](/deploy-manage/images/stack-install-final-state.png)

To learn more about the {{stack}} and how each of these components are related, refer to [An overview of the {{stack}}](/get-started/the-stack.md).

## Security overview [security-overview]

This tutorial results in a secure-by-default environment, but not every connection uses the same certificate model. Before you begin, it helps to understand the security layout produced by these steps:

* {{es}} uses the [automatic security setup](/deploy-manage/security/self-auto-setup.md) during the initial installation flow. This process generates certificates and enables TLS for both the transport and HTTP layers.
* {{kib}} connects to {{es}} using the enrollment flow from the initial {{es}} setup.
* HTTPS for browser-to-{{kib}} communication is **not configured** in this tutorial, although it is strongly recommended for production environments. {{kib}} HTTPS is covered in [Tutorial 2: Customize certificates for a self-managed {{stack}}](tutorial-self-managed-secure.md).
* {{fleet-server}} is installed using the Quick Start flow, which uses a self-signed certificate for its HTTPS endpoint.
* {{agent}} enrolls using that Quick Start flow, which requires the install command to include the `--insecure` flag.

If you plan to use certificates signed by your organization's certificate authority or by a public CA, complete this tutorial until {{kib}} is installed (Step 7), and then continue with [Tutorial 2: Customize certificates for a self-managed {{stack}}](tutorial-self-managed-secure.md) before installing {{fleet-server}} and {{agent}}.

## Step 1: Set up the first {{es}} node [install-stack-self-elasticsearch-first]

To begin, use RPM to install {{es}} on the first host. This initial {{es}} instance bootstraps a new cluster. You can find details about all of the following steps in the document [Install {{es}} with RPM](/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md).

::::{note}
For installation steps for other supported methods, refer to [Install {{es}}](/deploy-manage/deploy/self-managed/installing-elasticsearch.md#installation-methods).
::::

1. Log in to the host where you'd like to set up your first {{es}} node.

1. Create a working directory for the installation package:

   ```shell
   mkdir elastic-install-files
   ```

1. Navigate to the new directory:

   ```shell
   cd elastic-install-files
   ```

1. Download the {{es}} RPM and checksum file from the {{artifact-registry}}.

   ```shell subs=true
   curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{version.stack}}-x86_64.rpm
   curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{version.stack}}-x86_64.rpm.sha512
   ```

1. (Optional) Confirm the validity of the downloaded package by checking the SHA of the downloaded RPM against the published checksum:

   ```shell subs=true
   sha512sum -c elasticsearch-{{version.stack}}-x86_64.rpm.sha512
   ```

   The command should return:
   
   ```shell subs=true
   elasticsearch-{{version.stack}}-x86_64.rpm: OK.
   ```

1. (Optional) Import the {{es}} GPG key used to verify the RPM package signature:

    ```shell
    sudo rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
    ```

1. Run the {{es}} install command:

   ```shell subs=true
   sudo rpm --install elasticsearch-{{version.stack}}-x86_64.rpm
   ```

   The {{es}} install process enables [certain security features](/deploy-manage/security/self-auto-setup.md) by default, including the following:

   * Authentication and authorization, including the built-in `elastic` superuser account.
   * TLS certificates and keys for the transport and HTTP layers, stored in `/etc/elasticsearch/certs` and configured automatically for use by {{es}}.
   * The transport interface is bound to the loopback interface (`localhost`), preventing other nodes from joining the cluster, while the HTTP interface listens on all network interfaces (`http.host: 0.0.0.0`).

1. Copy the terminal output from the install command to a local file. In particular, you need the password for the built-in `elastic` superuser account. The output also contains the commands to enable {{es}} to run as a service, which you use in the next step.

1. Run the following two commands to enable {{es}} to run as a service using `systemd`. This enables {{es}} to start automatically when the host system reboots. For more details, refer to [Running {{es}} with `systemd`](/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md#running-systemd).

   ```shell
   sudo systemctl daemon-reload
   sudo systemctl enable elasticsearch.service
   ```

## Step 2: Configure the first {{es}} node for connectivity [install-stack-self-elasticsearch-config]

Before moving ahead to configure additional {{es}} nodes, you need to update the {{es}} configuration on this first node so that other hosts are able to connect to it. This is done by updating the settings in the `elasticsearch.yml` file. For more details about {{es}} configuration and the most common settings, refer to [Configure {{es}}](/deploy-manage/deploy/self-managed/configure-elasticsearch.md) and [important settings configuration](/deploy-manage/deploy/self-managed/important-settings-configuration.md).

1. Obtain your host IP address (for example, by running `ifconfig`). You need this value later.

1. Open the {{es}} configuration file in a text editor, such as `vim`:

   ```shell
   sudo vim /etc/elasticsearch/elasticsearch.yml
   ```

1. In a multi-node {{es}} cluster, all of the {{es}} instances must have the same cluster name.

   In the configuration file, uncomment the line `#cluster.name: my-application` and give the {{es}} cluster any name that you'd like:

   ```yaml
   cluster.name: elasticsearch-demo
   ```

1. (Optional) Set a node name for this instance. If you don't set one, {{es}} uses its host name by default.

   In the configuration file, uncomment the line `#node.name: node-1` and give the {{es}} instance any name that you'd like:

   ```yaml
   node.name: instance-1
   ```

1. Configure networking settings.

   1. Uncomment the line `#transport.host: 0.0.0.0` to accept connections on all available network interfaces.

      By default, {{es}} listens for transport traffic on `localhost`, which prevents other {{es}} instances from joining the cluster. To allow communication between nodes, you need to bind the transport interface to a non-loopback address.

      ```yaml
      transport.host: 0.0.0.0 <1>
      ```
      1. If you want {{es}} to listen only on a specific interface, set this to the host IP address instead.

   1. Make sure `http.host` is configured.

      {{es}} should already be configured to listen on all network interfaces for HTTP traffic as part of the automatic setup.

      Verify that this setting is present in your configuration file. If it is not, add it:

      ```yaml
      http.host: 0.0.0.0 <1>
      ```
      1. If you want {{es}} to listen only on a specific interface, set this to the host IP address instead.

      :::{tip}
      As an alternative to setting `transport.host` and `http.host` separately, you can use `network.host` to configure both interfaces at once. For details, refer to the [{{es}} networking settings](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) documentation.
      :::

1. Save your changes and close the editor.

   :::{important}
   After you configure {{es}} to use non-loopback addresses, it enforces [bootstrap checks](/deploy-manage/deploy/self-managed/bootstrap-checks.md). If {{es}} does not start successfully in the next step, review the [Important system configuration](/deploy-manage/deploy/self-managed/important-system-configuration.md) documentation.
   :::

## Step 3: Start {{es}} and bootstrap the cluster [install-stack-self-elasticsearch-start]

1. Now, it's time to start the {{es}} service on the first node:

   ```shell
   sudo systemctl start elasticsearch.service
   ```

   If you need to, you can stop the service by running `sudo systemctl stop elasticsearch.service`.

   :::{tip}
   If {{es}} does not start successfully, check the {{es}} log file at `/var/log/elasticsearch/<cluster-name>.log` to learn more. For example, if your cluster name is `elasticsearch-demo`, the log file is `/var/log/elasticsearch/elasticsearch-demo.log`.
   :::

1. Make sure that {{es}} is running properly.

   ```shell
   sudo curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
   ```

   In the command, replace `$ELASTIC_PASSWORD` with the `elastic` superuser password that you copied from the install command output.

   If all is well, the command returns a response like this:

   ```json
   {
     "name" : "Cp9oae6",
     "cluster_name" : "elasticsearch-demo",
     "cluster_uuid" : "AT69_C_DTp-1qgIJlatQqA",
     "version" : {
       "number" : "{version_qualified}",
       "build_type" : "{build_type}",
       "build_hash" : "f27399d",
       "build_flavor" : "default",
       "build_date" : "2016-03-30T09:51:41.449Z",
       "build_snapshot" : false,
       "lucene_version" : "{lucene_version}",
       "minimum_wire_compatibility_version" : "1.2.3",
       "minimum_index_compatibility_version" : "1.2.3"
     },
     "tagline" : "You Know, for Search"
   }
   ```

1. Finally, check the status of {{es}}:

   ```shell
   sudo systemctl status elasticsearch
   ```

   As with the previous `curl` command, the output should confirm that {{es}} started successfully. Type `q` to exit from the `status` command results.

## Step 4: Set up a second {{es}} node [install-stack-self-elasticsearch-second]

To set up a second {{es}} node, you start by installing the {{es}} RPM package, but then follow a different configuration flow so that the node joins the existing cluster instead of creating a new one. You can find additional details in [Reconfigure a node to join an existing cluster](/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md#existing-cluster).

1. Log in to the host where you'd like to set up your second {{es}} instance.

1. Create a working directory for the installation package:

   ```shell
   mkdir elastic-install-files
   ```

1. Change into the new directory:

   ```shell
   cd elastic-install-files
   ```

1. Download the {{es}} RPM and checksum file:

   ```shell subs=true
   curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{version.stack}}-x86_64.rpm
   curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{version.stack}}-x86_64.rpm.sha512
   ```

1. Check the SHA of the downloaded RPM:

   ```shell subs=true
   sha512sum -c elasticsearch-{{version.stack}}-x86_64.rpm.sha512
   ```

1. (Optional) Import the {{es}} GPG key used to verify the RPM package signature:

   ```shell
   sudo rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
   ```

1. Run the {{es}} install command:

   ```shell subs=true
   sudo rpm --install elasticsearch-{{version.stack}}-x86_64.rpm
   ```

   Unlike the setup for the first {{es}} node, in this case you don't need to copy the output of the install command. By default, the installation prepares the node as a single-node cluster, but in a later step the `elasticsearch-reconfigure-node` tool updates that configuration so the node can join your existing cluster.

1. Enable {{es}} to run as a service:

   ```shell
   sudo systemctl daemon-reload
   sudo systemctl enable elasticsearch.service
   ```

   :::{important}
   Don't start the {{es}} service yet. Complete the remaining configuration steps first.
   :::

1. To enable the new {{es}} node to connect to the cluster, create an enrollment token from any node that is already part of the cluster.

   Return to your terminal shell on the first {{es}} node and generate a node enrollment token:

   ```shell
   sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node
   ```

1. Copy the generated enrollment token from the command output.

   :::{tip} 
   An enrollment token has a lifespan of 30 minutes. In case the `elasticsearch-reconfigure-node` command returns an `Invalid enrollment token` error, try generating a new token.
   
   Be sure not to confuse an [{{es}} enrollment token](/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md#existing-cluster) (for enrolling {{es}} nodes in an existing cluster) with a [{{kib}} enrollment token](/deploy-manage/maintenance/start-stop-services/start-stop-kibana.md#run-kibana-from-command-line) (to enroll your {{kib}} instance with {{es}}, as described in the next section). These two tokens are not interchangeable.
   :::

1. In the terminal shell for your second {{es}} node, pass the enrollment token as a parameter to the `elasticsearch-reconfigure-node` tool:

   ```shell
   sudo /usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <enrollment-token> <1>
   ```
   1. Replace `<enrollment-token>` with the token that you copied in the previous step.

   ::::{note}
   If `elasticsearch-reconfigure-node` fails and indicates that the node has already been started or initialized, refer to [Cases when security auto-configuration is skipped](/deploy-manage/security/self-auto-setup.md#stack-skip-auto-configuration) for a list of possible causes.

   This can happen, for example, if {{es}} was started previously, which creates the `data` directory and prevents the auto-configuration process from running again.
   ::::

1. Answer the `Do you want to continue with the reconfiguration process` prompt with `yes` (`y`). The new {{es}} node is reconfigured.

1. Obtain your host IP address (for example, by running `ifconfig`). You need this value later.

1. Open the new {{es}} instance configuration file in a text editor:

   ```shell
   sudo vim /etc/elasticsearch/elasticsearch.yml
   ```

   Because of running the `elasticsearch-reconfigure-node` tool, certain settings have been updated. For example:

   * The `transport.host: 0.0.0.0` and `http.host: 0.0.0.0` settings are already uncommented.
   * The `discovery_seed.hosts` setting has the host IP address of the first {{es}} node. As you add each new {{es}} node to the cluster, the `discovery_seed.hosts` setting contains an array of the IP addresses and port numbers to connect to each {{es}} node that was previously added to the cluster.

1. In the configuration file, uncomment the line `#cluster.name: my-application` and set it to match the name you specified on the first {{es}} node:

   ```yaml
   cluster.name: elasticsearch-demo
   ```

1. (Optional) Set a node name for this instance. If you don't set one, {{es}} uses its host name by default.

   In the configuration file, uncomment the line `#node.name: node-1` and give the {{es}} instance any name that you'd like:

   ```yaml
   node.name: instance-2
   ```

1. (Optional) Review networking settings.

   After running `elasticsearch-reconfigure-node`, {{es}} is already configured to use non-loopback addresses for transport and HTTP traffic, so no changes are usually required. You can verify this in your configuration file:

   ```yaml
   transport.host: 0.0.0.0
   http.host: 0.0.0.0
   ```

   ::::{note}
   If you make changes to the networking settings, ensure that the networking configuration is consistent across all nodes. For example, use the same approach to binding (specific IP addresses or `0.0.0.0`) and the same settings (`transport.host`, `http.host`, or `network.host`) across all nodes. For details, refer to the [{{es}} networking settings](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) documentation.
   ::::

1. Save your changes and close the editor.

1. Start {{es}} on the second node:

   ```shell
   sudo systemctl start elasticsearch.service
   ```

   :::{tip}
   If {{es}} does not start successfully, check the {{es}} log file at `/var/log/elasticsearch/<cluster-name>.log` to learn more. For example, if your cluster name is `elasticsearch-demo`, the log file is `/var/log/elasticsearch/elasticsearch-demo.log`.
   :::

1. (Optional) To monitor the second {{es}} node as it starts up and joins the cluster, open a new terminal into the second node and `tail` the {{es}} log file:

    ```shell
    sudo tail -f /var/log/elasticsearch/elasticsearch-demo.log <1>
    ```
    1. If needed, replace `elasticsearch-demo` with your cluster name.

    Notice in the log file some helpful diagnostics, such as:
     - `Security is enabled`
     - `Profiling is enabled`
     - `using discovery type [multi-node]`
     - `initialized`
     - `starting...`

    After a minute or so, the log should show a message like:

    ```text
    [<hostname2>] master node changed {previous [], current [<hostname1>...]}
    ```

    where `hostname1` is your first {{es}} instance node, and `hostname2` is your second {{es}} instance node.
    
    The message indicates that the second {{es}} node has successfully contacted the initial {{es}} node and joined the cluster.

1. As a final check, verify that the new node is reachable and responding, and that it appears in the cluster. In the following commands, replace `$ELASTIC_PASSWORD` with the same `elastic` superuser password that you used on the first {{es}} node.

    To confirm that {{es}} is running properly on the new node, run:

    ```shell
    sudo curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200 <1>
    ```
    1. For a more complete check, replace `localhost` with the IP address of the new node to verify that it is reachable over the network.
    
    Response example:

    ```json
    {
      "name" : "Cp9oae6",
      "cluster_name" : "elasticsearch-demo",
      "cluster_uuid" : "AT69_C_DTp-1qgIJlatQqA",
      "version" : {
        "number" : "{version_qualified}",
        "build_type" : "{build_type}",
        "build_hash" : "f27399d",
        "build_flavor" : "default",
        "build_date" : "2016-03-30T09:51:41.449Z",
        "build_snapshot" : false,
        "lucene_version" : "{lucene_version}",
        "minimum_wire_compatibility_version" : "1.2.3",
        "minimum_index_compatibility_version" : "1.2.3"
      },
      "tagline" : "You Know, for Search"
    }
    ```

    To confirm that the node has joined the cluster, run the following command on any {{es}} node:

    ```shell
    sudo curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200/_cat/nodes?v <1>
    ```
    1. You can replace `localhost` with the IP address of any of the nodes.

    The output should include the new node together with the existing node or nodes in the cluster, for example:

    ```shell
    203.0.113.25 46 97 18 0.21 0.23 0.10 cdfhilmrstw - instance-2
    203.0.113.21 31 96  1 0.04 0.03 0.01 cdfhilmrstw * instance-1
    ```

## Step 5: Set up additional {{es}} nodes [install-stack-self-elasticsearch-third]

To set up additional {{es}} nodes, repeat the process from [Step 4: Set up a second {{es}} node](#install-stack-self-elasticsearch-second) for each new node that you add to the cluster.

As a recommended best practice, create a new enrollment token for each new node that you add.

## Step 6: Consolidate {{es}} configuration [install-stack-self-elasticsearch-consolidate]

Once you have added all your {{es}} nodes to the cluster, you need to consolidate the `elasticsearch.yml` configuration on all nodes so that they can restart and rejoin the cluster cleanly in the future.

1. On each {{es}} node, open `/etc/elasticsearch/elasticsearch.yml` in a text editor.
1. Comment out or remove the `cluster.initial_master_nodes` setting, if it is still present. This setting is only needed while bootstrapping a new cluster.
1. Update `discovery.seed_hosts` so it includes the IP address and transport port of each master-eligible {{es}} node in the cluster.

   On the first node in the cluster, you need to add the `discovery.seed_hosts` setting manually. For example, if your cluster has three nodes:

   ```yaml
   discovery.seed_hosts:
     - 203.0.113.84:9300
     - 203.0.113.132:9300
     - 203.0.113.156:9300
   ```

   ::::{note}
   If you are not configuring [node roles](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md), then all your {{es}} nodes should appear in the `discovery.seed_hosts` list of all the nodes.
   ::::

1. Save your changes on each node.
1. Optionally, restart the {{es}} service on each node to validate the updated configuration.

If you do not perform these steps, one or more nodes can fail the [discovery configuration bootstrap check](/deploy-manage/deploy/self-managed/bootstrap-checks.md#bootstrap-checks-discovery-configuration) when restarted.

For more information, refer to [Update the config files](/deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md#update-config-files) and [Discovery and cluster formation](/deploy-manage/distributed-architecture/discovery-cluster-formation.md).


## Step 7: Install {{kib}} [install-stack-self-kibana]

As with {{es}}, you can use RPM to install {{kib}} on another host. You can find details about all of the following steps in the document [Install {{kib}} with RPM](/deploy-manage/deploy/self-managed/install-kibana-with-rpm.md).

::::{note}
For installation steps using other supported methods, refer to [Install {{kib}}](/deploy-manage/deploy/self-managed/install-kibana.md).
::::

### Install {{kib}} package

1. Log in to the host where you'd like to install {{kib}} and create a working directory for the installation package:

   ```shell
   mkdir kibana-install-files
   ```

1. Change into the new directory:

   ```shell
   cd kibana-install-files
   ```

1. Download the {{kib}} RPM and checksum file from the Elastic website.

   ```shell subs=true
   curl -L -O https://artifacts.elastic.co/downloads/kibana/kibana-{{version.stack}}-x86_64.rpm
   curl -L -O https://artifacts.elastic.co/downloads/kibana/kibana-{{version.stack}}-x86_64.rpm.sha512
   ```

1. Confirm the validity of the downloaded package by checking the SHA of the downloaded RPM against the published checksum:

   ```shell subs=true
   sha512sum -c kibana-{{version.stack}}-x86_64.rpm.sha512
   ```

   The command should return: 
   
   ```shell subs=true
   kibana-{{version.stack}}-x86_64.rpm: OK
   ```

1. (Optional) Import the {{es}} GPG key used to verify the RPM package signature:

   ```shell
   sudo rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch <1>
   ```
   1. The GPG key used to sign {{kib}} and {{es}} RPM packages is the same.

1. Run the {{kib}} install command:

   ```shell subs=true
   sudo rpm --install kibana-{{version.stack}}-x86_64.rpm
   ```

1. Run the following two commands to enable {{kib}} to run as a service using `systemd`, enabling {{kib}} to start automatically when the host system reboots.

   ```shell
   sudo systemctl daemon-reload
   sudo systemctl enable kibana.service
   ```

### Configure {{kib}}

Before starting the {{kib}} service, update `kibana.yml` with the following settings:

* The network binding address so that {{kib}} listens on its host IP address.
* A saved objects encryption key required for features such as {{fleet}}.

For more details about {{kib}} configuration, refer to the [{{kib}} configuration](/deploy-manage/deploy/self-managed/configure-kibana.md).

1. Obtain the host IP address for your {{kib}} host (for example, by running `ifconfig`) and make note of it.

1. Generate a [saved objects encryption key](/deploy-manage/security/secure-saved-objects.md) on the {{kib}} host:

   ```shell
   sudo /usr/share/kibana/bin/kibana-encryption-keys generate
   ```

   The command output includes several encryption-related settings. For this tutorial, copy only the value of `xpack.encryptedSavedObjects.encryptionKey`, which is required for {{fleet}} features. You can ignore the other generated keys for now.

1. Open the {{kib}} configuration file for editing:

   ```shell
   sudo vim /etc/kibana/kibana.yml
   ```

1. Uncomment the line `#server.host: localhost` and replace the default address with the host IP address that you copied. For example:

   ```yaml
   server.host: 203.0.113.28 <1>
   ```
   1. If you want {{kib}} to listen on all available network interfaces, you can use `0.0.0.0` instead.

1. Add the `xpack.encryptedSavedObjects.encryptionKey` setting with the value returned by the `kibana-encryption-keys generate` command:

   ```yaml
   xpack.encryptedSavedObjects.encryptionKey: "min-32-byte-long-strong-encryption-key" <1>
   ```
   1. Replace the value with the actual key.

   :::{important}
   In production environments, consider storing this setting in the {{kib}} keystore instead of `kibana.yml`. For guidance, refer to [{{kib}} secure settings](/deploy-manage/security/secure-settings.md).

   Rotate encryption keys only as part of a planned process. This helps ensure existing encrypted saved objects remain readable. For guidance on rotation, refer to [Encryption key rotation](/deploy-manage/security/secure-saved-objects.md#encryption-key-rotation).
   :::

1. Save your changes and close the editor.

{{kib}} is now ready to start and enroll with the {{es}} cluster.

### Start and enroll {{kib}}

In this section, you start {{kib}} for the first time and complete enrollment with your {{es}} cluster. This initial startup provides the verification code and enrollment prompt, and it finalizes {{kib}} setup by automatically applying the required connection settings.

1. Start the {{kib}} service:

    ```shell
    sudo systemctl start kibana.service
    ```

    If you need to, you can stop the service by running `sudo systemctl stop kibana.service`.

1. Run the `status` command to get details about the {{kib}} service.

    ```shell
    sudo systemctl status kibana
    ```

1. In the `status` command output, a URL is shown with: 
    - a host address to access {{kib}}
    - a six digit verification code
    
    For example:
    ```text
    Kibana has not been configured.
    Go to http://203.0.113.28:5601/?code=<code> to get started. <1>
    ```
    1. If the URL shows `0.0.0.0`, use the host IP address when connecting to {{kib}} in the next step.

    Make note of the verification code.

1. Open a web browser to the external IP address of the {{kib}} host machine, for example: `http://<kibana-host-address>:5601`.

    It can take a minute or two for {{kib}} to start up, so refresh the page if you don't see a prompt right away.

1. When {{kib}} starts, you're prompted for an enrollment token. You must generate this token in {{es}}:

   1. Return to the terminal session on the first {{es}} node.

   1. Run the `elasticsearch-create-enrollment-token` command with the `-s kibana` option to generate a {{kib}} enrollment token:

      ```shell
      sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
      ```

   1. Copy the generated enrollment token from the command output and paste it into the enrollment prompt in the browser.

1. Click **Configure Elastic**.

1. If you're prompted to provide a verification code, copy and paste in the six digit code that was returned by the `status` command. Then, wait for the setup to complete.

1. When the **Welcome to Elastic** page appears, sign in with the `elastic` superuser account and the password that was generated when you installed the first {{es}} node.

1. Click **Log in**.

{{kib}} is now fully set up and communicating with your {{es}} cluster.

:::{warning} - Stop here if you plan to use your own TLS/SSL certificates
This tutorial already uses the {{es}} [automatic security setup](/deploy-manage/security/self-auto-setup.md), which configures security for {{es}} by default, including TLS for both the transport and HTTP layers.

If you plan to use certificates signed by your organization's certificate authority or by a public CA instead, stop here after installing {{kib}} and continue with [Tutorial 2: Customize certificates for a self-managed {{stack}}](tutorial-self-managed-secure.md). That tutorial is the right place to replace or adjust the default certificate configuration before installing {{fleet-server}} and {{agent}}.

Following that path avoids installing {{fleet-server}} and {{agent}} with the certificate setup from this tutorial and then needing to reinstall the components after changing the security configuration.

Note also that the automatic setup used here does not configure HTTPS for browser access to {{kib}}, which is highly recommended for production environments.
:::

## Step 8: Install {{fleet-server}} [install-stack-self-fleet-server]

Now that {{kib}} is up and running, you can install {{fleet-server}}. {{fleet-server}} connects {{agent}} instances to {{fleet}} and serves as a control plane for updating agent policies and collecting agent status information.

::::{note}
This tutorial uses the **Quick Start** installation flow, which generates a self-signed certificate for the {{fleet-server}} by default. For more details about **Quick Start** and **Advanced** setup options, refer to [Deploy on-premises and self-managed {{fleet-server}}](/reference/fleet/add-fleet-server-on-prem.md).

If you want to use custom SSL/TLS certificates, follow [Tutorial 2: Customize certificates for a self-managed {{stack}}](tutorial-self-managed-secure.md) instead of continuing with these steps.
::::

Before proceeding, confirm the following prerequisites:

* If you're not using the built-in `elastic` superuser, ensure your {{kib}} user has **All** privileges for **{{fleet}}** and **{{integrations}}**.
* {{agent}} hosts have direct network connectivity to both the {{fleet-server}} and the {{es}} cluster.
* The {{kib}} host can connect to `https://epr.elastic.co` on port `443` to download integration packages.

1. Log in to the host where you'd like to set up {{fleet-server}}.

1. Create a working directory for the installation package:

   ```shell
   mkdir fleet-install-files
   ```

1. Change into the new directory:

   ```shell
   cd fleet-install-files
   ```

1. Obtain the host IP address for your {{fleet-server}} host (for example, by running `ifconfig`). You need this value later.

1. Return to your web browser. Open the {{kib}} menu and go to **Management -> Fleet**. {{fleet}} opens with a message that you need to add a {{fleet-server}}.

1. Click **Add Fleet Server**. The **Add a Fleet Server** flyout shows up.

1. In the flyout, select the **Quick Start** tab.

1. Specify a name for your {{fleet-server}} host, for example `Fleet Server`.

1. Specify the host URL that {{agent}}s need to use to reach the {{fleet-server}}, for example: `https://203.0.113.203:8220`. This is the {{fleet-server}} host IP address that you copied earlier.

   Be sure to include the port number. Port `8220` is the default used by {{fleet-server}} in an on-premises environment. Refer to [Default port assignments](/reference/fleet/add-fleet-server-on-prem.md#default-port-assignments-on-prem) in the on-premises {{fleet-server}} install documentation for a list of port assignments.

1. Click **Generate Fleet Server policy**. A policy is created that contains all of the configuration settings for the {{fleet-server}} instance.

1. On the **Install Fleet Server to a centralized host** step, for this example we select the **Linux** tab. Be sure to select the tab that matches both your operating system and architecture (for example, `aarch64` or `x64`). TAR/ZIP packages are recommended over RPM/DEB system packages, since only the former support upgrading {{fleet-server}} using {{fleet}}.

1. Copy the generated commands and then run them one-by-one in the terminal on your {{fleet-server}} host. These commands do the following:
    - Download the {{fleet-server}} package from the {{artifact-registry}}
    - Unpack the package archive
    - Change into the directory containing the install binaries
    - Install {{fleet-server}}
    
    If you'd like to learn about the install command options, refer to [`elastic-agent install`](/reference/fleet/agent-command-reference.md#elastic-agent-install-command) in the {{agent}} command reference.

1. When prompted, enter `Y` to install {{agent}} and run it as a service. Wait for the installation to complete.

1. In the {{kib}} **Add a Fleet Server** flyout, wait for confirmation that {{fleet-server}} has connected.

1. For now, ignore the **Continue enrolling Elastic Agent** option and close the flyout.

{{fleet-server}} is now fully set up.

## Step 9: Install {{agent}} [install-stack-self-elastic-agent]

Next, install {{agent}} on another host and use the System integration to monitor system logs and metrics.

:::{note}
You can install only one {{agent}} per host.
:::

1. Log in to the host where you'd like to set up {{agent}}.

1. Create a working directory for the installation package:

   ```shell
   mkdir agent-install-files
   ```

1. Change into the new directory:

   ```shell
   cd agent-install-files
   ```

1. Open {{kib}} and go to **Management -> Fleet**.

1. On the **Agents** tab, you should see your new {{fleet-server}} policy running with a healthy status.

1. Open the **Settings** tab and review the **Fleet Server hosts** and **Outputs** URLs. Ensure the URLs and IP addresses are valid for reaching {{fleet-server}} and the {{es}} cluster, and that they use the HTTPS protocol.

1. Reopen the **Agents** tab and select **Add agent**. The **Add agent** flyout shows up.

1. In the flyout, choose a policy name, for example `Demo Agent Policy`.

1. Leave **Collect system logs and metrics** enabled. This adds the [System integration](https://docs.elastic.co/integrations/system) to the {{agent}} policy.

1. Click **Create policy**.

1. For the **Enroll in Fleet?** step, leave **Enroll in Fleet** selected.

1. On the **Install Elastic Agent on your host** step, for this example we select the **Linux** tab. Be sure to select the tab that matches both your operating system and architecture (for example, `aarch64` or `x64`).

    As with {{fleet-server}}, note that TAR/ZIP packages are recommended over RPM/DEB system packages, since only the former support upgrading {{agent}} using {{fleet}}.

1. Copy the generated commands to a text editor. Do not run them yet, because you need to modify one of the commands in the next step.

1. In the `sudo ./elastic-agent install` command, make two changes:
    - For the `--url` parameter, check that the port number is set to `8220` (used for on-premises {{fleet-server}}).
    - Append an `--insecure` flag at the end.

    The `--insecure` flag is required in this tutorial to allow connections to a {{fleet-server}} endpoint that uses a self-signed certificate. For related guidance, refer to [Install Fleet-managed Elastic Agents](/reference/fleet/install-fleet-managed-elastic-agent.md).

    :::{tip}
    If you want to set up secure communications using custom SSL certificates, refer to [Tutorial 2: Customize certificates for a self-managed {{stack}}](tutorial-self-managed-secure.md).
    :::

    The result should look like the following:

    ```shell
    sudo ./elastic-agent install --url=https://203.0.113.203:8220 --enrollment-token=VWCobFhKd0JuUnppVYQxX0VKV5E6UmU3BGk0ck9RM2HzbWEmcS4Bc1YUUM== --insecure
    ```

1. Run the commands one-by-one in the terminal on your {{agent}} host. The commands do the following:
    - Download the {{agent}} package from the {{artifact-registry}}.
    - Unpack the package archive.
    - Change into the directory containing the install binaries.
    - Install {{agent}}.

1. When prompted, enter `Y` to install {{agent}} and run it as a service. Wait for the installation to complete:

    ```text
    Elastic Agent has been successfully installed.
    ```

1. In the {{kib}} **Add agent** flyout, wait for confirmation that {{agent}} has connected.

1. Close the flyout.

Your new {{agent}} is now installed and enrolled with {{fleet-server}}.

## Step 10: View your system data [install-stack-self-view-data]

Now that all components are installed, you can view your data in multiple ways. [Elastic {{observability}}](/solutions/observability.md) provides solution views for exploring host activity, and each integration can also provide dedicated dashboards and visualizations. In this tutorial, you'll first check the host view in {{observability}}, then open example logs and metrics dashboards from the [System integration](https://docs.elastic.co/integrations/system).

The System integration assets (including dashboards) are installed automatically when you add the System integration to the {{agent}} policy.

**View your host data in {{observability}}:**

1. Open the {{kib}} menu and go to **Observability -> Infrastructure -> Hosts**.
2. Confirm that your host appears and is reporting data.

**View your system log data:**

1. Open the {{kib}} menu and go to **Analytics -> Dashboard**.
2. In the query field, search for `Logs System`.
3. Select the `[Logs System] Syslog dashboard` link. The {{kib}} Dashboard opens with visualizations of Syslog events, hostnames and processes, and more.

**View your system metrics data:**

1. Open the {{kib}} menu and return to **Analytics -> Dashboard**.
2. In the query field, search for `Metrics System`.
3. Select the `[Metrics System] Host overview` link. The {{kib}} Dashboard opens with visualizations of host metrics including CPU usage, memory usage, running processes, and others.

![Sample Kibana dashboard](/deploy-manage/images/install-stack-metrics-dashboard.png)

You've successfully set up a three-node {{es}} cluster, with {{kib}}, {{fleet-server}}, and {{agent}}.

## Next steps [install-stack-self-next-steps]

Now that you've successfully configured an on-premises {{stack}}, you can learn how to customize the certificate configuration for the {{stack}} in a production environment using trusted CA-signed certificates. Refer to [Tutorial 2: Customize certificates for a self-managed {{stack}}](tutorial-self-managed-secure.md) to learn more.

You can also start using your newly set up {{stack}} right away:

* Do you have data ready to ingest? Learn how to [bring your data to Elastic](/manage-data/ingest.md).
* Use [Elastic {{observability}}](/solutions/observability.md) to unify your logs, infrastructure metrics, uptime, and application performance data.
* Want to protect your endpoints from security threats? Try [{{elastic-sec}}](/solutions/security.md). Adding endpoint protection is just another integration that you add to the agent policy!
