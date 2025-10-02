---
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/install-standalone-elastic-agent.html
products:
  - id: fleet
  - id: elastic-agent
---

# Install standalone Elastic Agents [install-standalone-elastic-agent]

To run an {{agent}} in standalone mode, install the agent and manually configure the agent locally on the system where it’s installed. You are responsible for managing and upgrading the agents. This approach is recommended for advanced users only.

We recommend using [{{fleet}}-managed {{agent}}s](/reference/fleet/install-fleet-managed-elastic-agent.md), when possible, because it makes the management and upgrade of your agents considerably easier.

::::{important}
Standalone agents are unable to upgrade to new integration package versions automatically. When you upgrade the integration in {{kib}}, you’ll need to update the standalone policy manually.
::::


::::{note}
You can install only a single {{agent}} per host.
::::


{{agent}} can monitor the host where it’s deployed, and it can collect and forward data from remote services and hardware where direct deployment is not possible.

To install and run {{agent}} standalone:

1. On your host, download and extract the installation package.

    :::::::{tab-set}

    ::::::{tab-item} macOS
    ```shell subs=true
    curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-darwin-aarch64.tar.gz
    tar xzvf elastic-agent-{{version.stack}}-darwin-aarch64.tar.gz
    ```
    ::::::

    ::::::{tab-item} Linux
    ```shell subs=true
    curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-linux-x86_64.tar.gz
    tar xzvf elastic-agent-{{version.stack}}-linux-x86_64.tar.gz
    ```
    ::::::

    ::::::{tab-item} Windows
    ```shell subs=true
    # PowerShell 5.0+
    wget https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-windows-x86_64.zip -OutFile elastic-agent-{{version.stack}}-windows-x86_64.zip
    Expand-Archive .\elastic-agent-{{version.stack}}-windows-x86_64.zip
    ```
    Or manually:

    1. Download the {{agent}} Windows zip file from the [download page](https://www.elastic.co/downloads/beats/elastic-agent).

    2. Extract the contents of the zip file.
    ::::::

    ::::::{tab-item} DEB

    :::::{important}
    * To simplify upgrading to future versions of {{agent}}, we recommended that you use the tarball distribution instead of the DEB distribution.
    * You can install {{agent}} in an `unprivileged` mode that does not require `root` privileges. Refer to [Run {{agent}} without administrative privileges](./elastic-agent-unprivileged.md) for details.
    :::::

    ```shell subs=true
    curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-amd64.deb
    sudo dpkg -i elastic-agent-{{version.stack}}-amd64.deb
    ```

    By default the {{agent}} basic flavor is installed. To install the servers flavor add the `ELASTIC_AGENT_FLAVOR=servers` parameter. Refer to [{{agent}} installation flavors](./install-elastic-agents.md#elastic-agent-installation-flavors) for details about the different flavors.

    You can use either of the two command formats to set the `ELASTIC_AGENT_FLAVOR` environment variable:

    ```shell subs=true
    curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-amd64.deb
    sudo ELASTIC_AGENT_FLAVOR=servers dpkg -i elastic-agent-{{version.stack}}-amd64.deb
    ```

    ```shell subs=true
    curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-amd64.deb
    ELASTIC_AGENT_FLAVOR=servers sudo -E dpkg -i elastic-agent-{{version.stack}}-amd64.deb
    ```

    :::::{note}
    If you need to uninstall an {{agent}} package on Debian Linux, note that the `dpkg -r` command to remove a package leaves the flavor file in place. Instead, `dpkg -P` must to be used to purge all package content and reset the flavor.
    :::::

    ::::::

    ::::::{tab-item} RPM

    :::::{important}
    * To simplify upgrading to future versions of {{agent}}, we recommended that you use the tarball distribution instead of the RPM distribution.
    * You can install {{agent}} in an `unprivileged` mode that does not require `root` privileges. Refer to [Run {{agent}} without administrative privileges](./elastic-agent-unprivileged.md) for details.
    :::::

    ```shell subs=true
    curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-x86_64.rpm
    sudo rpm -vi elastic-agent-{{version.stack}}-x86_64.rpm
    ```

    By default the {{agent}} basic flavor is installed. To install the servers flavor add the `ELASTIC_AGENT_FLAVOR=servers` parameter. Refer to [{{agent}} installation flavors](./install-elastic-agents.md#elastic-agent-installation-flavors) for details about the different flavors.

    You can use either of the two command formats to set the `ELASTIC_AGENT_FLAVOR` environment variable:

    ```shell subs=true
    curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-amd64.deb
    sudo ELASTIC_AGENT_FLAVOR=servers rpm -vi elastic-agent-{{version.stack}}-x86_64.rpm
    ```

    ```shell subs=true
    curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-amd64.deb
    ELASTIC_AGENT_FLAVOR=servers sudo -E rpm -vi elastic-agent-{{version.stack}}-x86_64.rpm
    ```

    ::::::

    :::::::

    The commands shown are for either the Intel or ARM platform, but packages for both are available. Refer to the {{agent}} [downloads page](https://www.elastic.co/downloads/elastic-agent) for the full list of available packages.



2. Modify settings in the `elastic-agent.yml` as required.

    To get started quickly and avoid errors, use {{kib}} to create and download a standalone configuration file rather than trying to build it by hand. For more information, refer to [Create a standalone {{agent}} policy](/reference/fleet/create-standalone-agent-policy.md).

    For additional configuration options, refer to [*Configure standalone {{agent}}s*](/reference/fleet/configure-standalone-elastic-agents.md).

3. In the `elastic-agent.yml` policy file, under `outputs`, specify an API key or user credentials for the {{agent}} to access {{es}}. For example:

    ```yaml
    [...]
    outputs:
      default:
        type: elasticsearch
        hosts:
          - 'https://da4e3a6298c14a6683e6064ebfve9ace.us-central1.gcp.cloud.es.io:443'
        api_key: _Nj4oH0aWZVGqM7MGop8:349p_U1ERHyIc4Nm8_AYkw <1>
    [...]
    ```

    1. For more information required privileges and creating API keys, see [Grant standalone {{agent}}s access to {{es}}](/reference/fleet/grant-access-to-elasticsearch.md).

4. Make sure the assets you need, such as dashboards and ingest pipelines, are set up in {{kib}} and {{es}}. If you used {{kib}} to generate the standalone configuration, the assets are set up automatically. Otherwise, you need to install them. For more information, refer to [View integration assets](/reference/fleet/view-integration-assets.md) and [Install integration assets](/reference/fleet/install-uninstall-integration-assets.md#install-integration-assets).
5. From the agent directory, run the following commands to install {{agent}} and start it as a service.

    ::::{note}
    On macOS, Linux (tar package), and Windows, run the `install` command to install {{agent}} as a managed service and start the service. The DEB and RPM packages include a service unit for Linux systems with systemd, so just enable then start the service.
    ::::

    :::::{tab-set}

    ::::{tab-item} macOS

    :::{tip}
    You must run this command as the root user because some integrations require root privileges to collect sensitive data.
    :::

    ```shell
    sudo ./elastic-agent install
    ```

    By default the {{agent}} basic flavor is installed. To install the servers flavor, add the `--ìnstall-servers` parameter. Refer to [{{agent}} installation flavors](./install-elastic-agents.md#elastic-agent-installation-flavors) for details.

    ::::

    ::::{tab-item} Linux

    :::{tip}
    You must run this command as the root user because some integrations require root privileges to collect sensitive data.
    :::

    ```shell
    sudo ./elastic-agent install
    ```

    By default the {{agent}} basic flavor is installed. To install the servers flavor, add the `--ìnstall-servers` parameter. Refer to [{{agent}} installation flavors](./install-elastic-agents.md#elastic-agent-installation-flavors) for details.

    ::::

    ::::{tab-item} Windows

    Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select **Run As Administrator**).

    From the PowerShell prompt, change to the directory where you installed {{agent}}, and run:

    ```shell
    .\elastic-agent.exe install
    ```

    By default the {{agent}} basic flavor is installed. To install the servers flavor, add the `--ìnstall-servers` parameter. Refer to [{{agent}} installation flavors](./install-elastic-agents.md#elastic-agent-installation-flavors) for details.

    ::::

    ::::{tab-item} DEB

    ```shell
    sudo systemctl enable elastic-agent <1>
    sudo systemctl start elastic-agent
    ```

    1. The DEB package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands. If you don’t have systemd, run `sudo service elastic-agent start`.

    ::::

    ::::{tab-item} RPM

    ```shell
    sudo systemctl enable elastic-agent <1>
    sudo systemctl start elastic-agent
    ```

    1. The RPM package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands. If you don’t have systemd, run `sudo service elastic-agent start`.

    ::::

    :::::

Refer to [Installation layout](/reference/fleet/installation-layout.md) for the location of installed {{agent}} files.

Because {{agent}} is installed as an auto-starting service, it will restart automatically if the system is rebooted.

If you run into problems, refer to [](/troubleshoot/ingest/fleet/common-problems.md).
