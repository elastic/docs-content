# Tutorial 1: Installing a self-managed {{stack}} [installing-stack-demo-self]

This tutorial demonstrates how to install and configure the {{stack}} in a self-managed environment. Following these steps, you’ll set up a three node {{es}} cluster, with {{kib}}, {{fleet-server}}, and {{agent}}, each on separate hosts. The {{agent}} will be configured with the System integration, enabling it to gather local system logs and metrics and deliver them into the {{es}} cluster. Finally, you’ll learn how to view the system data in {{kib}}.

It should take between one and two hours to complete these steps.

::::{important}
If you’re using these steps to configure a production cluster that uses trusted CA-signed certificates for secure communications, after completing Step 6 to install {{kib}} we recommend jumping directly to [Tutorial 2: Securing a self-managed {{stack}}](../../../deploy-manage/security/secure-your-cluster-deployment.md).

The second tutorial includes steps to configure security across the {{stack}}, and then to set up {{fleet-server}} and {{agent}} with SSL certificates enabled.

::::



## Prerequisites and assumptions [install-stack-self-prereqs]

To get started, you’ll need the following:

* A set of virtual or physical hosts on which to install each stack component.
* On each host, a super user account with `sudo` privileges.

The examples in this guide use RPM packages to install the {{stack}} components on hosts running Red Hat Enterprise Linux 8. The steps for other install methods and operating systems are similar, and can be found in the documentation linked from each section. The packages that you’ll install are:

* [https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-x86_64.rpm](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-x86_64.rpm)
* [https://artifacts.elastic.co/downloads/kibana/kibana-9.0.0-beta1-x86_64.rpm](https://artifacts.elastic.co/downloads/kibana/kibana-9.0.0-beta1-x86_64.rpm)
* [https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-9.0.0-beta1-linux-x86_64.tar.gz](https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-9.0.0-beta1-linux-x86_64.tar.gz)

::::{note}
For {{agent}} and {{fleet-server}} (both of which use the elastic-agent-9.0.0-beta1-linux-x86_64.tar.gz package) we recommend using TAR/ZIP packages over RPM/DEB system packages, since only the former support upgrading using {{fleet}}.
::::


Special considerations such as firewalls and proxy servers are not covered here.

For the basic ports and protocols required for the installation to work, refer to the following overview section.


## {{stack}} overview [install-stack-self-overview]

Before starting, take a moment to familiarize yourself with the {{stack}} components.

:::{image} /raw-migrated-files/images/elastic-stack-stack-install-final-state.png
:alt: Image showing the relationships between stack components
:::

To learn more about the {{stack}} and how each of these components are related, refer to [An overview of the {{stack}}](../../../get-started/the-stack.md).


## Step 1: Set up the first {{es}} node [install-stack-self-elasticsearch-first]

To begin, use RPM to install {{es}} on the first host. This initial {{es}} instance will serve as the master node.

1. Log in to the host where you’d like to set up your first {{es}} node.
2. Create a working directory for the installation package:

    ```shell
    mkdir elastic-install-files
    ```

3. Change into the new directory:

    ```shell
    cd elastic-install-files
    ```

4. Download the {{es}} RPM and checksum file from the {{artifact-registry}}. You can find details about these steps in the section [Download and install the RPM manually](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md#install-rpm).

    ```sh
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-x86_64.rpm
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-x86_64.rpm.sha512
    ```

5. Confirm the validity of the downloaded package by checking the SHA of the downloaded RPM against the published checksum:

    ```sh
    shasum -a 512 -c elasticsearch-9.0.0-beta1-x86_64.rpm.sha512
    ```

    The command should return: `elasticsearch-<version>-x86_64.rpm: OK`.

6. Run the {{es}} install command:

    ```sh
    sudo rpm --install elasticsearch-9.0.0-beta1-x86_64.rpm
    ```

    The {{es}} install process enables certain security features by default, including the following:

    * Authentication and authorization are enabled, including a built-in `elastic` superuser account.
    * Certificates and keys for TLS are generated for the transport and HTTP layer, and TLS is enabled and configured with these keys and certificates.

7. Copy the terminal output from the install command to a local file. In particular, you’ll need the password for the built-in `elastic` superuser account. The output also contains the commands to enable {{es}} to run as a service, which you’ll use in the next step.
8. Run the following two commands to enable {{es}} to run as a service using `systemd`. This enables {{es}} to start automatically when the host system reboots. You can find details about this and the following steps in [Running {{es}} with `systemd`](../../../deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md#start-deb).

    ```sh
    sudo systemctl daemon-reload
    sudo systemctl enable elasticsearch.service
    ```



## Step 2: Configure the first {{es}} node for connectivity [install-stack-self-elasticsearch-config]

Before moving ahead to configure additional {{es}} nodes, you’ll need to update the {{es}} configuration on this first node so that other hosts are able to connect to it. This is done by updating the settings in the `elasticsearch.yml` file. For details about all available settings refer to [Configuring {{es}}](../../../deploy-manage/deploy/self-managed/configure-elasticsearch.md).

1. In a terminal, run the `ifconfig` command and copy the value for the host inet IP address (for example, `10.128.0.84`). You’ll need this value later.
2. Open the {{es}} configuration file in a text editor, such as `vim`:

    ```sh
    sudo vim /etc/elasticsearch/elasticsearch.yml
    ```

3. In a multi-node {{es}} cluster, all of the {{es}} instances need to have the same name.

    In the configuration file, uncomment the line `#cluster.name: my-application` and give the {{es}} instance any name that you’d like:

    ```yaml
    cluster.name: elasticsearch-demo
    ```

4. By default, {{es}} runs on `localhost`. In order for {{es}} instances on other nodes to be able to join the cluster, you’ll need to set up {{es}} to run on a routable, external IP address.

    Uncomment the line `#network.host: 192.168.0.1` and replace the default address with the value that you copied from the `ifconfig` command output. For example:

    ```yaml
    network.host: 10.128.0.84
    ```

5. {{es}} needs to be enabled to listen for connections from other, external hosts.

    Uncomment the line `#transport.host: 0.0.0.0`. The `0.0.0.0` setting enables {{es}} to listen for connections on all available network interfaces. Note that in a production environment you might want to restrict this by setting this value to match the value set for `network.host`.

    ```yaml
    transport.host: 0.0.0.0
    ```

    ::::{tip}
    You can find details about the `network.host` and `transport.host` settings in the {{es}} [Networking](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) documentation.
    ::::

6. Save your changes and close the editor.


## Step 3: Start {{es}} [install-stack-self-elasticsearch-start]

1. Now, it’s time to start the {{es}} service:

    ```sh
    sudo systemctl start elasticsearch.service
    ```

    If you need to, you can stop the service by running `sudo systemctl stop elasticsearch.service`.

2. Make sure that {{es}} is running properly.

    ```sh
    sudo curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
    ```

    In the command, replace `$ELASTIC_PASSWORD` with the `elastic` superuser password that you copied from the install command output.

    If all is well, the command returns a response like this:

    ```js
    {
      "name" : "Cp9oae6",
      "cluster_name" : "elasticsearch",
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

3. Finally, check the status of {{es}}:

    ```shell
    sudo systemctl status elasticsearch
    ```

    As with the previous `curl` command, the output should confirm that {{es}} started successfully. Type `q` to exit from the `status` command results.



## Step 4: Set up a second {{es}} node [install-stack-self-elasticsearch-second]

To set up a second {{es}} node, the initial steps are similar to those that you followed for [Step 1: Set up the first {{es}} node](#install-stack-self-elasticsearch-first).

1. Log in to the host where you’d like to set up your second {{es}} instance.
2. Create a working directory for the installation package:

    ```shell
    mkdir elastic-install-files
    ```

3. Change into the new directory:

    ```shell
    cd elastic-install-files
    ```

4. Download the {{es}} RPM and checksum file:

    ```sh
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-x86_64.rpm
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-x86_64.rpm.sha512
    ```

5. Check the SHA of the downloaded RPM:

    ```sh
    shasum -a 512 -c elasticsearch-9.0.0-beta1-x86_64.rpm.sha512
    ```

6. Run the {{es}} install command:

    ```sh
    sudo rpm --install elasticsearch-9.0.0-beta1-x86_64.rpm
    ```

    Unlike the setup for the first {{es}} node, in this case you don’t need to copy the output of the install command, since these settings will be updated in a later step.

7. Enable {{es}} to run as a service:

    ```sh
    sudo systemctl daemon-reload
    sudo systemctl enable elasticsearch.service
    ```

    ::::{important}
    Don’t start the {{es}} service yet! There are a few more configuration steps to do before restarting.
    ::::

8. To enable this second {{es}} node to connect to the first, you need to configure an enrollment token.

    ::::{important}
    Be sure to run all of these configuration steps before starting the {{es}} service.

    You can find additional details about these steps in [Reconfigure a node to join an existing cluster](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-rpm.md#_reconfigure_a_node_to_join_an_existing_cluster_2) and also in [Enroll nodes in an existing cluster](../../../deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md#_enroll_nodes_in_an_existing_cluster_5).

    ::::


    Return to your terminal shell on the first {{es}} node and generate a node enrollment token:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node
    ```

9. Copy the generated enrollment token from the command output.

    ::::{tip}
    Note the following tips about enrollment tokens:

    1. An enrollment token has a lifespan of 30 minutes. In case the `elasticsearch-reconfigure-node` command returns an `Invalid enrollment token` error, try generating a new token.
    2. Be sure not to confuse an [{{es}} enrollment token](../../../deploy-manage/maintenance/add-and-remove-elasticsearch-nodes.md) (for enrolling {{es}} nodes in an existing cluster) with a [{{kib}} enrollment token](../../../deploy-manage/maintenance/start-stop-services/start-stop-kibana.md#run-kibana-from-command-line) (to enroll your {{kib}} instance with {{es}}, as described in the next section). These two tokens are not interchangeable.

    ::::

10. In the terminal shell for your second {{es}} node, pass the enrollment token as a parameter to the `elasticsearch-reconfigure-node` tool:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <enrollment-token>
    ```

    In the command, replace `<enrollment-token` with the `elastic` generated token that you copied.

11. Answer the `Do you want to continue` prompt with `yes` (`y`). The new {{es}} node will be reconfigured.
12. In a terminal, run `ifconfig` and copy the value for the host inet IP address. You’ll need this value later.
13. Open the second {{es}} instance configuration file in a text editor:

    ```sh
    sudo vim /etc/elasticsearch/elasticsearch.yml
    ```

    Notice that, as a result of having run the `elasticsearch-reconfigure-node` tool, certain settings have been updated. For example:

    * The `transport.host: 0.0.0.0` setting is already uncommented.
    * The `discovery_seed.hosts` setting has the value that you added for `network_host` on the first {{es}} node. As you add each new {{es}} node to the cluster, the `discovery_seed.hosts` setting will contain an array of the IP addresses and port numbers to connect to each {{es}} node that was previously added to the cluster.

14. In the configuration file, uncomment the line `#cluster.name: my-application` and set it to match the name you specified for the first {{es}} node:

    ```yaml
    cluster.name: elasticsearch-demo
    ```

15. As with the first {{es}} node, you’ll need to set up {{es}} to run on a routable, external IP address. Uncomment the line `#network.host: 92.168.0.1` and replace the default address with the value that you copied. For example:

    ```yaml
    network.host: 10.128.0.132
    ```

16. Save your changes and close the editor.
17. Start {{es}} on the second node:

    ```shell
    sudo systemctl start elasticsearch.service
    ```

18. **Optionally**, to view the progress as the second {{es}} node starts up and connects to the first {{es}} node, open a new terminal into the second node and `tail` the {{es}} log file:

    ```shell
    sudo tail -f /var/log/elasticsearch/elasticsearch-demo.log
    ```

    Notice in the log file some helpful diagnostics, such as:

    * `Security is enabled`
    * `Profiling is enabled`
    * `using discovery type [multi-node]`
    * `intialized`
    * `starting...`

        After a minute or so, the log should show a message like:

        ```shell
        [<hostname2>] master node changed {previous [], current [<hostname1>...]}
        ```

        Here, `hostname1` is your first {{es}} instance node, and `hostname2` is your second {{es}} instance node.

        The message indicates that the second {{es}} node has successfully contacted the initial {{es}} node and joined the cluster.

19. As a final check, run the following `curl` request on the new node to confirm that {{es}} is still running properly and viewable at the new node’s `localhost` IP address. Note that you need to replace `$ELASTIC_PASSWORD` with the same `elastic` superuser password that you used on the first {{es}} node.

    ```sh
    sudo curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
    ```

    ```js
    {
      "name" : "Cp9oae6",
      "cluster_name" : "elasticsearch",
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



## Step 5: Set up additional {{es}} nodes [install-stack-self-elasticsearch-third]

To set up your next {{es}} node, follow exactly the same steps as you did previously in [Step 4: Set up a second {{es}} node](#install-stack-self-elasticsearch-second). The process is identical for each additional {{es}} node that you would like to add to the cluster. As a recommended best practice, create a new enrollment token for each new node that you add.


## Step 6: Install {{kib}} [install-stack-self-kibana]

As with {{es}}, you can use RPM to install {{kib}} on another host. You can find details about all of the following steps in the section [Install {{kib}} with RPM](../../../deploy-manage/deploy/self-managed/install-kibana-with-rpm.md#install-rpm).

1. Log in to the host where you’d like to install {{kib}} and create a working directory for the installation package:

    ```shell
    mkdir kibana-install-files
    ```

2. Change into the new directory:

    ```shell
    cd kibana-install-files
    ```

3. Download the {{kib}} RPM and checksum file from the Elastic website.

    ```sh
    wget https://artifacts.elastic.co/downloads/kibana/kibana-9.0.0-beta1-x86_64.rpm
    wget https://artifacts.elastic.co/downloads/kibana/kibana-9.0.0-beta1-x86_64.rpm.sha512
    ```

4. Confirm the validity of the downloaded package by checking the SHA of the downloaded RPM against the published checksum:

    ```sh
    shasum -a 512 -c kibana-9.0.0-beta1-x86_64.rpm.sha512
    ```

    The command should return: `kibana-<version>-x86_64.rpm: OK`.

5. Run the {{kib}} install command:

    ```sh
    sudo rpm --install kibana-9.0.0-beta1-x86_64.rpm
    ```

6. As with each additional {{es}} node that you added, to enable this {{kib}} instance to connect to the first {{es}} node, you need to configure an enrollment token.

    Return to your terminal shell into the first {{es}} node.

7. Run the `elasticsearch-create-enrollment-token` command with the `-s kibana` option to generate a {{kib}} enrollment token:

    ```shell
    sudo /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
    ```

8. Copy the generated enrollment token from the command output.
9. Back on the {{kib}} host, run the following two commands to enable {{kib}} to run as a service using `systemd`, enabling {{kib}} to start automatically when the host system reboots.

    ```sh
    sudo systemctl daemon-reload
    sudo systemctl enable kibana.service
    ```

10. Before starting the {{kib}} service there’s one configuration change to make, to set {{kib}} to run on the {{es}} host IP address. This is done by updating the settings in the `kibana.yml` file. For details about all available settings refer to [Configure {{kib}}](kibana://reference/configuration-reference/general-settings.md).
11. In a terminal, run the `ifconfig` command and copy the value for the host inet IP address.
12. Open the {{kib}} configuration file for editing:

    ```sh
    sudo vim /etc/kibana/kibana.yml
    ```

13. Uncomment the line `#server.host: localhost` and replace the default address with the inet value that you copied from the `ifconfig` command. For example:

    ```yaml
    server.host: 10.128.0.28
    ```

14. Save your changes and close the editor.
15. Start the {{kib}} service:

    ```sh
    sudo systemctl start kibana.service
    ```

    If you need to, you can stop the service by running `sudo systemctl stop kibana.service`.

16. Run the `status` command to get details about the {{kib}} service.

    ```sh
    sudo systemctl status kibana
    ```

17. In the `status` command output, a URL is shown with:

    * A host address to access {{kib}}
    * A six digit verification code

        For example:

        ```sh
        Kibana has not been configured.
        Go to http://10.128.0.28:5601/?code=<code> to get started.
        ```

        Make a note of the verification code.

18. Open a web browser to the external IP address of the {{kib}} host machine, for example: `http://<kibana-host-address>:5601`.

    It can take a minute or two for {{kib}} to start up, so refresh the page if you don’t see a prompt right away.

19. When {{kib}} starts you’re prompted to provide an enrollment token. Paste in the {{kib}} enrollment token that you generated earlier.
20. Click **Configure Elastic**.
21. If you’re prompted to provide a verification code, copy and paste in the six digit code that was returned by the `status` command. Then, wait for the setup to complete.
22. When you see the **Welcome to Elastic** page, provide the `elastic` as the username and provide the password that you copied in Step 1, from the `install` command output when you set up your first {{es}} node.
23. Click **Log in**.

{{kib}} is now fully set up and communicating with your {{es}} cluster!

**IMPORTANT: Stop here if you intend to configure SSL certificates.**

::::{important}
For simplicity, in this tutorial we’re setting up all of the {{stack}} components without configuring security certificates. You can proceed to configure {{fleet}}, {{agent}}, and then confirm that your system data appears in {{kib}}.

However, in a production environment, before going further to install {{fleet-server}} and {{agent}} it’s recommended to update your security settings to use trusted CA-signed certificates as described in [Tutorial 2: Securing a self-managed {{stack}}](../../../deploy-manage/security/secure-your-cluster-deployment.md).

After new security certificates are configured any {{agent}}s would need to be reinstalled. If you’re currently setting up a production environment, we recommend that you jump directly to Tutorial 2, which includes steps to secure the {{stack}} using certificates and then to set up {{fleet}} and {{agent}} with those certificates already in place.

::::



## Step 7: Install {{fleet-server}} [install-stack-self-fleet-server]

Now that {{kib}} is up and running, you can install {{fleet-server}}, which will manage the {{agent}} that you’ll set up in a later step. If you need more detail about these steps, refer to [Deploy on-premises and self-managed](/reference/fleet/add-fleet-server-on-prem.md) in the {{fleet}} and {{agent}} Guide.

1. Log in to the host where you’d like to set up {{fleet-server}}.
2. Create a working directory for the installation package:

    ```shell
    mkdir fleet-install-files
    ```

3. Change into the new directory:

    ```shell
    cd fleet-install-files
    ```

4. In the terminal, run `ifconfig` and copy the value for the host inet IP address (for example, `10.128.0.84`). You’ll need this value later.
5. Back to your web browser, open the {{kib}} menu and go to **Management → Fleet**. {{fleet}} opens with a message that you need to add a {{fleet-server}}.
6. Click **Add Fleet Server**. The **Add a Fleet Server** flyout opens.
7. In the flyout, select the **Quick Start** tab.
8. Specify a name for your {{fleet-server}} host, for example `Fleet Server`.
9. Specify the host URL where {{agents}} will reach {{fleet-server}}, for example: `http://10.128.0.203:8220`. This is the inet value that you copied from the `ifconfig` output.

    Be sure to include the port number. Port `8220` is the default used by {{fleet-server}} in an on-premises environment. Refer to [Default port assignments](/reference/fleet/add-fleet-server-on-prem.md#default-port-assignments-on-prem) in the on-premises {{fleet-server}} install documentation for a list of port assignments.

10. Click **Generate Fleet Server policy**. A policy is created that contains all of the configuration settings for the {{fleet-server}} instance.
11. On the **Install Fleet Server to a centralized host** step, for this example we select the **Linux Tar** tab, but you can instead select the tab appropriate to the host operating system where you’re setting up {{fleet-server}}.

    Note that TAR/ZIP packages are recommended over RPM/DEB system packages, since only the former support upgrading {{fleet-server}} using {{fleet}}.

12. Copy the generated commands and then run them one-by-one in the terminal on your {{fleet-server}} host.

    These commands will, respectively:

    1. Download the {{fleet-server}} package from the {{artifact-registry}}.
    2. Unpack the package archive.
    3. Change into the directory containing the install binaries.
    4. Install {{fleet-server}}.

        If you’d like to learn about the install command options, refer to [`elastic-agent install`](/reference/fleet/agent-command-reference.md#elastic-agent-install-command) in the {{agent}} command reference.

13. At the prompt, enter `Y` to install {{agent}} and run it as a service. Wait for the installation to complete.
14. In the {{kib}} **Add a Fleet Server** flyout, wait for confirmation that {{fleet-server}} has connected.
15. For now, ignore the **Continue enrolling Elastic Agent** option and close the flyout.

{{fleet-server}} is now fully set up!


## Step 8: Install {{agent}} [install-stack-self-elastic-agent]

Next, you’ll install {{agent}} on another host and use the System integration to monitor system logs and metrics.

1. Log in to the host where you’d like to set up {{agent}}.
2. Create a working directory for the installation package:

    ```shell
    mkdir agent-install-files
    ```

3. Change into the new directory:

    ```shell
    cd agent-install-files
    ```

4. Open {{kib}} and go to **Management → Fleet**.
5. On the **Agents** tab, you should see your new {{fleet-server}} policy running with a healthy status.
6. Open the **Settings** tab.
7. Reopen the **Agents** tab and select **Add agent**. The **Add agent** flyout opens.
8. In the flyout, choose a policy name, for example `Demo Agent Policy`.
9. Leave **Collect system logs and metrics** enabled. This will add the [System integration](https://docs.elastic.co/integrations/system) to the {{agent}} policy.
10. Click **Create policy**.
11. For the **Enroll in Fleet?** step, leave **Enroll in Fleet** selected.
12. On the **Install Elastic Agent on your host** step, for this example we select the **Linux Tar** tab, but you can instead select the tab appropriate to the host operating system where you’re setting up {{fleet-server}}.

    As with {{fleet-server}}, note that TAR/ZIP packages are recommended over RPM/DEB system packages, since only the former support upgrading {{agent}} using {{fleet}}.

13. Copy the generated commands.
14. In the `sudo ./elastic-agent install` command, make two changes:

    1. For the `--url` parameter, check that the port number is set to `8220` (used for on-premises {{fleet-server}}).
    2. Append an `--insecure` flag at the end.

        ::::{tip}
        If you want to set up secure communications using SSL certificates, refer to [Tutorial 2: Securing a self-managed {{stack}}](../../../deploy-manage/security/secure-your-cluster-deployment.md).
        ::::


        The result should be like the following:

        ```shell
        sudo ./elastic-agent install --url=https://10.128.0.203:8220 --enrollment-token=VWCobFhKd0JuUnppVYQxX0VKV5E6UmU3BGk0ck9RM2HzbWEmcS4Bc1YUUM==
        ```

15. Run the commands one-by-one in the terminal on your {{agent}} host. The commands will, respectively:

    1. Download the {{agent}} package from the {{artifact-registry}}.
    2. Unpack the package archive.
    3. Change into the directory containing the install binaries.
    4. Install {{agent}}.

16. At the prompt, enter `Y` to install {{agent}} and run it as a service. Wait for the installation to complete.

    If everything goes well, the install will complete successfully:

    ```shell
    Elastic Agent has been successfully installed.
    ```

17. In the {{kib}} **Add agent** flyout, wait for confirmation that {{agent}} has connected.
18. Close the flyout.

Your new {{agent}} is now installed an enrolled with {{fleet-server}}.


## Step 9: View your system data [install-stack-self-view-data]

Now that all of the components have been installed, it’s time to view your system data.

View your system log data:

1. Open the {{kib}} menu and go to **Analytics → Dashboard**.
2. In the query field, search for `Logs System`.
3. Select the `[Logs System] Syslog dashboard` link. The {{kib}} Dashboard opens with visualizations of Syslog events, hostnames and processes, and more.

View your system metrics data:

1. Open the {{kib}} menu and return to **Analytics → Dashboard**.
2. In the query field, search for `Metrics System`.
3. Select the `[Metrics System] Host overview` link. The {{kib}} Dashboard opens with visualizations of host metrics including CPU usage, memory usage, running processes, and others.

    :::{image} /raw-migrated-files/images/elastic-stack-install-stack-metrics-dashboard.png
    :alt: The System metrics host overview showing CPU usage, memory usage, and other visualizations
    :::


Congratulations! You’ve successfully set up a three node {{es}} cluster, with {{kib}}, {{fleet-server}}, and {{agent}}.


## Next steps [install-stack-self-next-steps]

Now that you’ve successfully configured an on-premises {{stack}}, you can learn how to configure the {{stack}} in a production environment using trusted CA-signed certificates. Refer to [Tutorial 2: Securing a self-managed {{stack}}](../../../deploy-manage/security/secure-your-cluster-deployment.md) to learn more.

You can also start using your newly set up {{stack}} right away:

* Do you have data ready to ingest? Learn how to [add data to Elasticsearch](../../../manage-data/ingest.md).
* Use [Elastic {{observability}}](https://www.elastic.co/observability) to unify your logs, infrastructure metrics, uptime, and application performance data.
* Want to protect your endpoints from security threats? Try [{{elastic-sec}}](https://www.elastic.co/security). Adding endpoint protection is just another integration that you add to the agent policy!
