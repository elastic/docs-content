# Stream any log file [observability-stream-log-files]

::::{admonition} Required role
:class: note

The **Admin** role or higher is required to onboard log data. To learn more, refer to [Assign user roles and privileges](../../../deploy-manage/users-roles/cloud-organization/user-roles.md#general-assign-user-roles).

::::


<div style="display:none">
:::{image} ../../../images/serverless-logs-stream-logs-api-key-beats.png
:alt: logs stream logs api key beats
:class: screenshot
:::

:::{image} ../../../images/serverless-log-copy-es-endpoint.png
:alt: Copy a project's Elasticsearch endpoint
:class: screenshot
:::

</div>
This guide shows you how to send a log file to your Observability project using a standalone {{agent}} and configure the {{agent}} and your data streams using the `elastic-agent.yml` file, and query your logs using the data streams you’ve set up.

The quickest way to get started is using the **Monitor hosts with {{agent}}** quickstart. Refer to the [quickstart documentation](../../../solutions/observability/get-started/quickstart-monitor-hosts-with-elastic-agent.md) for more information.

To install and configure the {{agent}} manually, refer to [Manually install and configure the standalone {{agent}}](../../../solutions/observability/logs/stream-any-log-file.md).


## Manually install and configure the standalone {{agent}} [manually-install-agent-logs]

If you’re not using the guided instructions, follow these steps to manually install and configure your the {{agent}}.


### Step 1: Download and extract the {{agent}} installation package [observability-stream-log-files-step-1-download-and-extract-the-agent-installation-package]

On your host, download and extract the installation package that corresponds with your system:

:::::::{tab-set}

::::::{tab-item} macOS
```sh
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.16.1-darwin-x86_64.tar.gz
tar xzvf elastic-agent-8.16.1-darwin-x86_64.tar.gz
```
::::::

::::::{tab-item} Linux
```sh
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.16.1-linux-x86_64.tar.gz
tar xzvf elastic-agent-8.16.1-linux-x86_64.tar.gz
```
::::::

::::::{tab-item} Windows
```powershell
# PowerShell 5.0+
wget https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.16.1-windows-x86_64.zip -OutFile elastic-agent-8.16.1-windows-x86_64.zip
Expand-Archive .\elastic-agent-8.16.1-windows-x86_64.zip
```

Or manually:

1. Download the {{agent}} Windows zip file from the [download page](https://www.elastic.co/downloads/beats/elastic-agent).
2. Extract the contents of the zip file.
::::::

::::::{tab-item} DEB
::::{important}
To simplify upgrading to future versions of {{agent}}, we recommended that you use the tarball distribution instead of the DEB distribution.

::::


```sh
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.16.1-amd64.deb
sudo dpkg -i elastic-agent-8.16.1-amd64.deb
```
::::::

::::::{tab-item} RPM
::::{important}
To simplify upgrading to future versions of {{agent}}, we recommended that you use the tarball distribution instead of the RPM distribution.

::::


```sh
curl -L -O https://artifacts.elastic.co/downloads/beats/elastic-agent/elastic-agent-8.16.1-x86_64.rpm
sudo rpm -vi elastic-agent-8.16.1-x86_64.rpm
```
::::::

:::::::

### Step 2: Install and start the {{agent}} [observability-stream-log-files-step-2-install-and-start-the-agent]

After downloading and extracting the installation package, you’re ready to install the {{agent}}. From the agent directory, run the install command that corresponds with your system:

::::{note}
On macOS, Linux (tar package), and Windows, run the `install` command to install and start {{agent}} as a managed service and start the service. The DEB and RPM packages include a service unit for Linux systems with systemd, For these systems, you must enable and start the service.

::::


:::::::{tab-set}

::::::{tab-item} macOS
::::{tip}
You must run this command as the root user because some integrations require root privileges to collect sensitive data.

::::


```shell
sudo ./elastic-agent install
```
::::::

::::::{tab-item} Linux
::::{tip}
You must run this command as the root user because some integrations require root privileges to collect sensitive data.

::::


```shell
sudo ./elastic-agent install
```
::::::

::::::{tab-item} Windows
Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select **Run As Administrator**).

From the PowerShell prompt, change to the directory where you installed {{agent}}, and run:

```shell
.\elastic-agent.exe install
```
::::::

::::::{tab-item} DEB
::::{tip}
You must run this command as the root user because some integrations require root privileges to collect sensitive data.

::::


```shell
sudo systemctl enable elastic-agent   <1>
sudo systemctl start elastic-agent
```

1. The DEB package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands. If you don’t have systemd, run `sudo service elastic-agent start`.
::::::

::::::{tab-item} RPM
::::{tip}
You must run this command as the root user because some integrations require root privileges to collect sensitive data.

::::


```shell
sudo systemctl enable elastic-agent   <1>
sudo systemctl start elastic-agent
```

1. The RPM package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands. If you don’t have systemd, run `sudo service elastic-agent start`.
::::::

:::::::
During installation, you’ll be prompted with some questions:

1. When asked if you want to install the agent as a service, enter `Y`.
2. When asked if you want to enroll the agent in Fleet, enter `n`.


### Step 3: Configure the {{agent}} [observability-stream-log-files-step-3-configure-the-agent]

After your agent is installed, configure it by updating the `elastic-agent.yml` file.


#### Locate your configuration file [observability-stream-log-files-locate-your-configuration-file]

You’ll find the `elastic-agent.yml` in one of the following locations according to your system:

:::::::{tab-set}

::::::{tab-item} macOS
Main {{agent}} configuration file location:

`/Library/Elastic/Agent/elastic-agent.yml`
::::::

::::::{tab-item} Linux
Main {{agent}} configuration file location:

`/opt/Elastic/Agent/elastic-agent.yml`
::::::

::::::{tab-item} Windows
Main {{agent}} configuration file location:

`C:\Program Files\Elastic\Agent\elastic-agent.yml`
::::::

::::::{tab-item} DEB
Main {{agent}} configuration file location:

`/etc/elastic-agent/elastic-agent.yml`
::::::

::::::{tab-item} RPM
Main {{agent}} configuration file location:

`/etc/elastic-agent/elastic-agent.yml`
::::::

:::::::

#### Update your configuration file [observability-stream-log-files-update-your-configuration-file]

Update the default configuration in the `elastic-agent.yml` file manually. It should look something like this:

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

You need to set the values for the following fields:

`hosts`
:   Copy the {{es}} endpoint from your project’s page and add the port (the default port is `443`). For example, `https://my-deployment.es.us-central1.gcp.cloud.es.io:443`.

    If you’re following the guided instructions in your project, the {{es}} endpoint will be prepopulated in the configuration file.

    :::::{tip}
    If you need to find your project’s {{es}} endpoint outside the guided instructions:

    1. Go to the **Projects** page that lists all your projects.
    2. Click **Manage** next to the project you want to connect to.
    3. Click **View** next to *Endpoints*.
    4. Copy the *Elasticsearch endpoint*.

    :::{image} ../../../images/serverless-log-copy-es-endpoint.png
    :alt: Copy a project's Elasticsearch endpoint
    :class: screenshot
    :::

    :::::


`api-key`
:   Use an API key to grant the agent access to your project. The API key format should be `<id>:<key>`.

    If you’re following the guided instructions in your project, an API key will be autogenerated and will be prepopulated in the downloadable configuration file.

    If configuring the {{agent}} manually, create an API key:

    1. Navigate to **Project settings** → **Management*** → ***API keys** and click **Create API key**.
    2. Select **Restrict privileges** and add the following JSON to give privileges for ingesting logs.

        ```json
        {
          "standalone_agent": {
            "cluster": [
              "monitor"
            ],
            "indices": [
              {
                "names": [
                  "logs-*-*"
                ],
                "privileges": [
                  "auto_configure", "create_doc"
                ]
              }
            ]
          }
        }
        ```

    3. You *must* set the API key to configure {{beats}}. Immediately after the API key is generated and while it is still being displayed, click the **Encoded** button next to the API key and select **Beats** from the list in the tooltip. Base64 encoded API keys are not currently supported in this configuration.

        :::{image} ../../../images/serverless-logs-stream-logs-api-key-beats.png
        :alt: logs stream logs api key beats
        :class: screenshot
        :::


`inputs.id`
:   A unique identifier for your input.

`type`
:   The type of input. For collecting logs, set this to `filestream`.

`streams.id`
:   A unique identifier for your stream of log data.

`data_stream.dataset`
:   The name for your dataset data stream. Name this data stream anything that signifies the source of the data. In this configuration, the dataset is set to `example`. The default value is `generic`.

`paths`
:   The path to your log files. You can also use a pattern like `/var/log/your-logs.log*`.


#### Restart the {{agent}} [observability-stream-log-files-restart-the-agent]

After updating your configuration file, you need to restart the {{agent}}.

First, stop the {{agent}} and its related executables using the command that works with your system:

:::::::{tab-set}

::::::{tab-item} macOS
```shell
sudo launchctl unload /Library/LaunchDaemons/co.elastic.elastic-agent.plist
```

::::{note}
{{agent}} will restart automatically if the system is rebooted.

::::
::::::

::::::{tab-item} Linux
```shell
sudo service elastic-agent stop
```

::::{note}
{{agent}} will restart automatically if the system is rebooted.

::::
::::::

::::::{tab-item} Windows
```shell
Stop-Service Elastic Agent
```

If necessary, use Task Manager on Windows to stop {{agent}}. This will kill the `elastic-agent` process and any sub-processes it created (such as {{beats}}).

::::{note}
{{agent}} will restart automatically if the system is rebooted.

::::
::::::

::::::{tab-item} DEB
The DEB package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to stop the agent:

```shell
sudo systemctl stop elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent stop
```

::::{note}
{{agent}} will restart automatically if the system is rebooted.

::::
::::::

::::::{tab-item} RPM
The RPM package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to stop the agent:

```shell
sudo systemctl stop elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent stop
```

::::{note}
{{agent}} will restart automatically if the system is rebooted.

::::
::::::

:::::::
Next, restart the {{agent}} using the command that works with your system:

:::::::{tab-set}

::::::{tab-item} macOS
```shell
sudo launchctl load /Library/LaunchDaemons/co.elastic.elastic-agent.plist
```
::::::

::::::{tab-item} Linux
```shell
sudo service elastic-agent start
```
::::::

::::::{tab-item} Windows
```shell
Start-Service Elastic Agent
```
::::::

::::::{tab-item} DEB
The DEB package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to start the agent:

```shell
sudo systemctl start elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent start
```
::::::

::::::{tab-item} RPM
The RPM package includes a service unit for Linux systems with systemd. On these systems, you can manage {{agent}} by using the usual systemd commands.

Use `systemctl` to start the agent:

```shell
sudo systemctl start elastic-agent
```

Otherwise, use:

```shell
sudo service elastic-agent start
```
::::::

:::::::

## Troubleshoot your {{agent}} configuration [observability-stream-log-files-troubleshoot-your-agent-configuration]

If you’re not seeing your log files in your project, verify the following in the `elastic-agent.yml` file:

* The path to your logs file under `paths` is correct.
* Your API key is in `<id>:<key>` format. If not, your API key may be in an unsupported format, and you’ll need to create an API key in **Beats** format.

If you’re still running into issues, refer to [{{agent}} troubleshooting](../../../troubleshoot/ingest/fleet/common-problems.md) and [Configure standalone Elastic Agents](asciidocalypse://docs/docs-content/docs/reference/ingestion-tools/fleet/configure-standalone-elastic-agents.md).


## Next steps [observability-stream-log-files-next-steps]

After you have your agent configured and are streaming log data to your project:

* Refer to the [Parse and organize logs](../../../solutions/observability/logs/parse-route-logs.md) documentation for information on extracting structured fields from your log data, rerouting your logs to different data streams, and filtering and aggregating your log data.
* Refer to the [Filter and aggregate logs](../../../solutions/observability/logs/filter-aggregate-logs.md) documentation for information on filtering and aggregating your log data to find specific information, gain insight, and monitor your systems more efficiently.
