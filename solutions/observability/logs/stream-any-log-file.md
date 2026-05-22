---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/logs-stream.html
  - https://www.elastic.co/guide/en/serverless/current/observability-stream-log-files.html
applies_to:
  stack: all
  serverless: all
products:
  - id: observability
  - id: cloud-serverless
---

# Send any log file using {{agent}} [logs-stream]

This guide shows you how to manually configure a standalone {{agent}} to send your log data to {{es}} using the `elastic-agent.yml` file. For an {{edot}} (EDOT) Collector equivalent, refer to [Send any log file using OTel Collector](/solutions/observability/logs/stream-any-log-file-using-edot-collector.md).

To get started quickly without manually configuring the {{agent}}, you can use the **Monitor hosts with {{agent}}** quickstart. Refer to the [quickstart documentation](/solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md) for more information.

Continue with this guide for instructions on manual configuration.

## Prerequisites [logs-stream-prereq]

::::{applies-switch}

:::{applies-item} stack:

To follow the steps in this guide, you need an {{stack}} deployment that includes:

* {{es}} for storing and searching data
* {{kib}} for visualizing and managing data
* Kibana user with `All` privileges on {{fleet}} and Integrations. Since many Integrations assets are shared across spaces, users need the Kibana privileges in all spaces.
* Integrations Server (included by default in every {{ech}} deployment)

To get started quickly, create an {{ech}} deployment and host it on AWS, GCP, or Azure. [Try it out for free](https://cloud.elastic.co/registration?page=docs&placement=docs-body).


:::

:::{applies-item} serverless:

The **Admin** role or higher is required to onboard log data. To learn more, refer to [Assign user roles and privileges](/deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

:::

::::

## Install and configure the standalone {{agent}} [logs-stream-install-config-agent]

Complete these steps to install and configure the standalone {{agent}} and send your log data to {{es}}:

1. [Download and extract the {{agent}} installation package.](/solutions/observability/logs/stream-any-log-file.md#logs-stream-extract-agent)
2. [Install and start the {{agent}}.](/solutions/observability/logs/stream-any-log-file.md#logs-stream-install-agent)
3. [Configure the {{agent}}.](/solutions/observability/logs/stream-any-log-file.md#logs-stream-agent-config)

### Step 1: Download and extract the {{agent}} installation package [logs-stream-extract-agent]

On your host, download and extract the installation package that corresponds with your system:

:::::{tab-set}

::::{tab-item} macOS

```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-darwin-x86_64.tar.gz
tar xzvf elastic-agent-{{version.stack}}-darwin-x86_64.tar.gz
```
::::

::::{tab-item} Linux

```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-linux-x86_64.tar.gz
tar xzvf elastic-agent-{{version.stack}}-linux-x86_64.tar.gz
```

::::

::::{tab-item} Windows

```powershell subs=true
# PowerShell 5.0+
wget https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-windows-x86_64.zip -OutFile elastic-agent-{{version.stack}}-windows-x86_64.zip
Expand-Archive .\elastic-agent-{{version.stack}}-windows-x86_64.zip

```

::::

::::{tab-item} DEB

:::{tip}
To simplify upgrading to future versions of Elastic Agent, use the tarball distribution instead of the RPM distribution.
You can install Elastic Agent in an unprivileged mode that does not require root privileges.
:::

```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-amd64.deb
sudo dpkg -i elastic-agent-{{version.stack}}-amd64.deb
```
::::

::::{tab-item} RPM

:::{tip}
To simplify upgrading to future versions of Elastic Agent, use the tarball distribution instead of the RPM distribution.
You can install Elastic Agent in an unprivileged mode that does not require root privileges.
:::

```shell subs=true
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-{{version.stack}}-x86_64.rpm
sudo rpm -vi elastic-agent-{{version.stack}}-x86_64.rpm
```
::::

:::::

### Step 2: Install and start the {{agent}} [logs-stream-install-agent]

After downloading and extracting the installation package, you're ready to install the {{agent}}. From the agent directory, run the install command that corresponds with your system:

:::{note}
On macOS, Linux (tar package), and Windows, run the `install` command to install and start {{agent}} as a managed service and start the service. The DEB and RPM packages include a service unit for Linux systems with systemd. For these systems, you must enable and start the service.
:::


:::::{tab-set}

::::{tab-item} macOS
:::{tip}
You must run this command as the root user because some integrations require root privileges to collect sensitive data.
:::


```shell
sudo ./elastic-agent install
```
::::

::::{tab-item} Linux
:::{tip}
You must run this command as the root user because some integrations require root privileges to collect sensitive data.
:::


```shell
sudo ./elastic-agent install
```
::::

::::{tab-item} Windows
Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select **Run As Administrator**).

From the PowerShell prompt, change to the directory where you installed {{agent}}, and run:

```shell
.\elastic-agent.exe install
```
::::

::::{tab-item} DEB
:::{tip}
You must run this command as the root user because some integrations require root privileges to collect sensitive data.
:::


```shell
sudo systemctl enable elastic-agent <1>
sudo systemctl start elastic-agent
```

1. The DEB package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands. If you don't have systemd, run `sudo service elastic-agent start`.
::::

::::{tab-item} RPM
:::{tip}
You must run this command as the root user because some integrations require root privileges to collect sensitive data.
:::


```shell
sudo systemctl enable elastic-agent <1>
sudo systemctl start elastic-agent
```

1. The RPM package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands. If you don't have systemd, run `sudo service elastic-agent start`.
::::

:::::

During installation, you're prompted with some questions:

1. When asked if you want to install the agent as a service, enter `Y`.
2. When asked if you want to enroll the agent in Fleet, enter `n`.


### Step 3: Configure the {{agent}} [logs-stream-agent-config]

With your agent installed, configure it by updating the `elastic-agent.yml` file.


#### Locate your configuration file [logs-stream-yml-location]

After installing the agent, you'll find the `elastic-agent.yml` in one of the following locations according to your system:

::::{tab-set}

:::{tab-item} macOS
Main {{agent}} configuration file location:

`/Library/Elastic/Agent/elastic-agent.yml`
:::

:::{tab-item} Linux
Main {{agent}} configuration file location:

`/opt/Elastic/Agent/elastic-agent.yml`
:::

:::{tab-item} Windows
Main {{agent}} configuration file location:

`C:\Program Files\Elastic\Agent\elastic-agent.yml`
:::

:::{tab-item} DEB
Main {{agent}} configuration file location:

`/etc/elastic-agent/elastic-agent.yml`
:::

:::{tab-item} RPM
Main {{agent}} configuration file location:

`/etc/elastic-agent/elastic-agent.yml`
:::

::::

#### Update your configuration file [logs-stream-example-config]

The following is an example of a standalone {{agent}} configuration. To configure your {{agent}}, replace the contents of the `elastic-agent.yml` file with this configuration:

```yaml
outputs:
  default:
    type: elasticsearch
    hosts: '<your-elasticsearch-endpoint>:<port>'
    api_key: 'your-api-key'
inputs:
  - id: your-log-id
    type: filestream
    streams:
      - id: your-log-stream-id
        data_stream:
          dataset: example
        paths:
          - /var/log/your-logs.log
```

Next, set the values for these fields:

* `hosts`: Copy the {{es}} endpoint from **Help menu (![help icon](/solutions/images/observability-help-icon.svg "")) → Connection details**. For example, `https://my-deployment.es.us-central1.gcp.cloud.es.io:443`.
* `api-key`: Use an API key to grant the agent access to {{es}}. To create an API key for your agent, refer to the [Create API keys for standalone agents](/reference/fleet/grant-access-to-elasticsearch.md#create-api-key-standalone-agent) documentation.

    :::{note}
    The API key format should be `<id>:<key>`. Make sure you selected **Beats** when you created your API key. Base64 encoded API keys are not currently supported in this configuration.
    :::

* `inputs.id`: A unique identifier for your input.
* `type`: The type of input. For collecting logs, set this to `filestream`.
* `streams.id`: A unique identifier for your stream of log data.
* `data_stream.dataset`: The name for your dataset data stream. Name this data stream anything that signifies the source of the data. In this configuration, the dataset is set to `example`. The default value is `generic`.
* `paths`: The path to your log files. You can also use a pattern like `/var/log/your-logs.log*`.


#### Restart the {{agent}} [logs-stream-restart-agent]

After updating your configuration file, you need to restart the {{agent}}:

First, stop the {{agent}} and its related executables using the command that works with your system:

:::::{tab-set}

::::{tab-item} macOS
```shell
sudo launchctl unload /Library/LaunchDaemons/co.elastic.elastic-agent.plist
```

:::{note}
{{agent}} will restart automatically if the system is rebooted.
:::
::::

::::{tab-item} Linux
```shell
sudo service elastic-agent stop
```

:::{note}
{{agent}} will restart automatically if the system is rebooted.
:::
::::

::::{tab-item} Windows
```shell
Stop-Service Elastic Agent
```

If necessary, use Task Manager on Windows to stop {{agent}}. This will kill the `elastic-agent` process and any sub-processes it created (such as {{beats}}).

:::{note}
{{agent}} will restart automatically if the system is rebooted.
:::
::::

::::{tab-item} DEB
The DEB package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to stop the agent:

```shell
sudo systemctl stop elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent stop
```

:::{note}
{{agent}} will restart automatically if the system is rebooted.
:::
::::

::::{tab-item} RPM
The RPM package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to stop the agent:

```shell
sudo systemctl stop elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent stop
```

:::{note}
{{agent}} will restart automatically if the system is rebooted.
:::
::::
:::::

Next, restart the {{agent}} using the command that works with your system:

::::{tab-set}

:::{tab-item} macOS
```shell
sudo launchctl load /Library/LaunchDaemons/co.elastic.elastic-agent.plist
```
:::

:::{tab-item} Linux
```shell
sudo service elastic-agent start
```
:::

:::{tab-item} Windows
```shell
Start-Service Elastic Agent
```
:::

:::{tab-item} DEB
The DEB package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to start the agent:

```shell
sudo systemctl start elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent start
```
:::

:::{tab-item} RPM
The RPM package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to start the agent:

```shell
sudo systemctl start elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent start
```
:::

::::

## Troubleshoot your {{agent}} configuration [logs-stream-troubleshooting]

If you're not seeing your log files in the UI, verify the following in the `elastic-agent.yml` file:

* The path to your logs file under `paths` is correct.
* Your API key is in `<id>:<key>` format. If not, your API key may be in an unsupported format, and you'll need to create an API key in **Beats** format.

If you're still running into issues, see [](/troubleshoot/ingest/fleet/common-problems.md) and [Configure standalone Elastic Agents](/reference/fleet/configure-standalone-elastic-agents.md).


## Next steps [logs-stream-next-steps]

After you have your agent configured and are streaming log data to {{es}}:

* Refer to the [Explore log data](/solutions/observability/logs/discover-logs.md) documentation for information on exploring your log data in the UI, including searching and filtering your log data, getting information about the structure of log fields, and displaying your findings in a visualization.
* Refer to the [Parse and organize logs](/solutions/observability/logs/parse-route-logs.md) documentation for information on extracting structured fields from your log data, rerouting your logs to different data streams, and filtering and aggregating your log data.
* Refer to the [Filter and aggregate logs](/solutions/observability/logs/filter-aggregate-logs.md) documentation for information on filtering and aggregating your log data to find specific information, gain insight, and monitor your systems more efficiently.