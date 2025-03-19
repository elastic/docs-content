# ECS formatted application logs [observability-ecs-application-logs]

Logs formatted in Elastic Common Schema (ECS) don’t require manual parsing, and the configuration can be reused across applications. ECS-formatted logs, when paired with an {{apm-agent}}, allow you to correlate logs to easily view logs that belong to a particular trace.

You can format your logs in ECS format the following ways:

* [**ECS loggers:**](../../../solutions/observability/logs/ecs-formatted-application-logs.md#observability-ecs-application-logs-ecs-loggers) plugins for your logging libraries that reformat your logs into ECS format.
* [**{{apm-agent}} ECS reformatting:**](../../../solutions/observability/logs/ecs-formatted-application-logs.md#reformatting-logs) Java, Ruby, and Python {{apm-agent}}s automatically reformat application logs to ECS format without a logger.


## ECS loggers [observability-ecs-application-logs-ecs-loggers]

ECS loggers reformat your application logs into ECS-compatible JSON, removing the need for manual parsing. ECS loggers require {{filebeat}} or {{agent}} configured to monitor and capture application logs. In addition, pairing ECS loggers with your framework’s {{apm-agent}} allows you to correlate logs to easily view logs that belong to a particular trace.


### Get started [observability-ecs-application-logs-get-started]

For more information on adding an ECS logger to your application, refer to the guide for your framework:

* [.NET](ecs-dotnet://reference/setup.md)
* Go: [zap](ecs-logging-go-zap://reference/setup.md)
* [Java](ecs-logging-java://reference/setup.md)
* Node.js: [morgan](ecs-logging-nodejs://reference/winston.md)
* [PHP](ecs-logging-php://reference/setup.md)
* [Python](ecs-logging-python://reference/installation.md)
* [Ruby](ecs-logging-ruby://reference/setup.md)


## APM agent ECS reformatting [reformatting-logs]

Java, Ruby, and Python {{apm-agent}}s can automatically reformat application logs to ECS format without an ECS logger or the need to modify your application. The {{apm-agent}} also allows for log correlation so you can easily view logs that belong to a particular trace.

To set up log ECS reformatting:

1. [Enable {{apm-agent}} reformatting](../../../solutions/observability/logs/ecs-formatted-application-logs.md#observability-ecs-application-logs-enable-log-ecs-reformatting)
2. [Ingest logs with {{filebeat}} or {{agent}}.](../../../solutions/observability/logs/ecs-formatted-application-logs.md#observability-ecs-application-logs-ingest-logs)
3. [View logs in Logs Explorer](../../../solutions/observability/logs/ecs-formatted-application-logs.md#observability-ecs-application-logs-view-logs)


### Enable log ECS reformatting [observability-ecs-application-logs-enable-log-ecs-reformatting]

Log ECS reformatting is controlled by the `log_ecs_reformatting` configuration option, and is disabled by default. Refer to the guide for your framework for information on enabling:

* [Java](apm-agent-java://reference/config-logging.md#config-log-ecs-reformatting)
* [Ruby](apm-agent-ruby://reference/configuration.md#config-log-ecs-formatting)
* [Python](apm-agent-python://reference/configuration.md#config-log_ecs_reformatting)


### Ingest logs [observability-ecs-application-logs-ingest-logs]

After enabling log ECS reformatting, send your application logs to your project using one of the following shipping tools:

* [**{{filebeat}}:**](../../../solutions/observability/logs/ecs-formatted-application-logs.md#observability-ecs-application-logs-ingest-logs-with-filebeat) A lightweight data shipper that sends log data to your project.
* [**{{agent}}:**](../../../solutions/observability/logs/ecs-formatted-application-logs.md#observability-ecs-application-logs-ingest-logs-with-agent) A single agent for logs, metrics, security data, and threat prevention. With Fleet, you can centrally manage {{agent}} policies and lifecycles directly from your project.


### Ingest logs with {{filebeat}} [observability-ecs-application-logs-ingest-logs-with-filebeat]

::::{important}
Use {{filebeat}} version 8.11+ for the best experience when ingesting logs with {{filebeat}}.

::::


Follow these steps to ingest application logs with {{filebeat}}.


#### Step 1: Install {{filebeat}} [observability-ecs-application-logs-step-1-install-filebeat]

Install {{filebeat}} on the server you want to monitor by running the commands that align with your system:

:::::::{tab-set}

::::::{tab-item} macOS
```sh
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.16.1-darwin-x86_64.tar.gz
tar xzvf filebeat-8.16.1-darwin-x86_64.tar.gz
```
::::::

::::::{tab-item} Linux
```sh
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.16.1-linux-x86_64.tar.gz
tar xzvf filebeat-8.16.1-linux-x86_64.tar.gz
```
::::::

::::::{tab-item} Windows
1. Download the {{filebeat}} Windows zip file: [https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.16.1-windows-x86_64.zip](https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.16.1-windows-x86_64.zip)
2. Extract the contents of the zip file into `C:\Program Files`.
3. Rename the `filebeat-((version))-windows-x86_64` directory to `((filebeat))`.
4. Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select **Run As Administrator**).
5. From the PowerShell prompt, run the following commands to install {{filebeat}} as a Windows service:

    ```powershell
    PS > cd 'C:\Program Files{filebeat}'
    PS C:\Program Files{filebeat}> .\install-service-filebeat.ps1
    ```


If script execution is disabled on your system, you need to set the execution policy for the current session to allow the script to run. For example: `PowerShell.exe -ExecutionPolicy UnRestricted -File .\install-service-filebeat.ps1`.
::::::

::::::{tab-item} DEB
```sh
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.16.1-amd64.deb
sudo dpkg -i filebeat-8.16.1-amd64.deb
```
::::::

::::::{tab-item} RPM
```sh
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.16.1-x86_64.rpm
sudo rpm -vi filebeat-8.16.1-x86_64.rpm
```
::::::

:::::::

#### Step 2: Connect to your project [observability-ecs-application-logs-step-2-connect-to-your-project]

Connect to your project using an API key to set up {{filebeat}}. Set the following information in the `filebeat.yml` file:

```yaml
output.elasticsearch:
  hosts: ["your-projects-elasticsearch-endpoint"]
  api_key: "id:api_key"
```

1. Set the `hosts` to your project’s {{es}} endpoint. Locate your project’s endpoint by clicking the help icon (![Help icon](../../../images/serverless-help.svg "")) and selecting **Endpoints**. Add the **{{es}} endpoint** to your configuration.
2. From **Developer tools**, run the following command to create an API key that grants `manage` permissions for the `cluster` and the `filebeat-*` indices using:

    ```shell
    POST /_security/api_key
    {
      "name": "filebeat_host001",
      "role_descriptors": {
        "filebeat_writer": {
          "cluster": ["manage"],
          "index": [
            {
              "names": ["filebeat-*"],
              "privileges": ["manage"]
            }
          ]
        }
      }
    }
    ```

    Refer to [Grant access using API keys](beats://reference/filebeat/beats-api-keys.md) for more information.



#### Step 3: Configure {{filebeat}} [observability-ecs-application-logs-step-3-configure-filebeat]

Add the following configuration to your `filebeat.yaml` file to start collecting log data.

:::::::{tab-set}

::::::{tab-item} Log file
1. Add the following configuration to your `filebeat.yaml` file to start collecting log data.

```yaml
filebeat.inputs:
- type: filestream   <1>
  paths: /path/to/logs.json
  parsers:
    - ndjson:
        overwrite_keys: true   <2>
        add_error_key: true   <3>
        expand_keys: true   <4>
  fields:
    service.name: your_service_name   <5>
    service.version: your_service_version   <5>
    service.environment: your_service_environment   <5>

processors:   <6>
  - add_host_metadata: ~
  - add_cloud_metadata: ~
  - add_docker_metadata: ~
  - add_kubernetes_metadata: ~
```

1. Use the filestream input to read lines from active log files.
2. Values from the decoded JSON object overwrite the fields that {{filebeat}} normally adds (type, source, offset, etc.) in case of conflicts.
3. {{filebeat}} adds an "error.message" and "error.type: json" key in case of JSON unmarshalling errors.
4. {{filebeat}} will recursively de-dot keys in the decoded JSON, and expand them into a hierarchical object structure.
5. The `service.name` (required), `service.version` (optional) and `service.environment` (optional) of the service you’re collecting logs from, used for [Log correlation](../../../solutions/observability/logs/stream-application-logs.md#observability-correlate-application-logs-log-correlation).
6. Processors enhance your data. See [processors](beats://reference/filebeat/filtering-enhancing-data.md) to learn more.
::::::

::::::{tab-item} Kubernetes
1. Make sure your application logs to stdout/stderr.
2. Follow the [Run {{filebeat}} on Kubernetes](beats://reference/filebeat/running-on-kubernetes.md) guide.
3. Enable [hints-based autodiscover](beats://reference/filebeat/configuration-autodiscover-hints.md) (uncomment the corresponding section in `filebeat-kubernetes.yaml`).
4. Add these annotations to your pods that log using ECS-compatible JSON. This will make sure the logs are parsed appropriately.

    ```yaml
    annotations:
    co.elastic.logs/json.overwrite_keys: true   <1>
    co.elastic.logs/json.add_error_key: true   <2>
    co.elastic.logs/json.expand_keys: true   <3>
    ```

    1. Values from the decoded JSON object overwrite the fields that {{filebeat}} normally adds (type, source, offset, etc.) in case of conflicts.
    2. {{filebeat}} adds an "error.message" and "error.type: json" key in case of JSON unmarshalling errors.
    3. {{filebeat}} will recursively de-dot keys in the decoded JSON, and expand them into a hierarchical object structure.
::::::

::::::{tab-item} Docker
1. Make sure your application logs to stdout/stderr.
2. Follow the [Run {{filebeat}} on Docker](beats://reference/filebeat/running-on-docker.md) guide.
3. Enable [hints-based autodiscover](beats://reference/filebeat/configuration-autodiscover-hints.md).
4. Add these labels to your containers that log using ECS-compatible JSON. This will make sure the logs are parsed appropriately. In `docker-compose.yml`:

```yaml
labels:
  co.elastic.logs/json.overwrite_keys: true   <1>
  co.elastic.logs/json.add_error_key: true   <2>
  co.elastic.logs/json.expand_keys: true   <3>
```

1. Values from the decoded JSON object overwrite the fields that {{filebeat}} normally adds (type, source, offset, etc.) in case of conflicts.
2. {{filebeat}} adds an "error.message" and "error.type: json" key in case of JSON unmarshalling errors.
3. {{filebeat}} will recursively de-dot keys in the decoded JSON, and expand them into a hierarchical object structure.
::::::

:::::::

#### Step 4: Set up and start {{filebeat}} [observability-ecs-application-logs-step-4-set-up-and-start-filebeat]

From the {{filebeat}} installation directory, set the [index template](../../../manage-data/data-store/templates.md) by running the command that aligns with your system:

:::::::{tab-set}

::::::{tab-item} macOS
```shell
./filebeat setup --index-management
```
::::::

::::::{tab-item} Linux
```shell
./filebeat setup --index-management
```
::::::

::::::{tab-item} Windows
```powershell
PS > .\filebeat.exe setup --index-management
```
::::::

::::::{tab-item} DEB
```shell
filebeat setup --index-management
```
::::::

::::::{tab-item} RPM
```sh
filebeat setup --index-management
```
::::::

:::::::
From the {{filebeat}} installation directory, start filebeat by running the command that aligns with your system:

:::::::{tab-set}

::::::{tab-item} macOS
```shell
sudo chown root filebeat.yml
sudo ./filebeat -e
```

::::{note}
You’ll be running {{filebeat}} as root, so you need to change ownership of the configuration file and any configurations enabled in the `modules.d` directory, or run {{filebeat}} with `--strict.perms=false` specified. Refer to [Config file ownership and permissions](beats://reference/libbeat/config-file-permissions.md).

::::
::::::

::::::{tab-item} Linux
```shell
sudo chown root filebeat.yml
sudo ./filebeat -e
```

::::{note}
You’ll be running {{filebeat}} as root, so you need to change ownership of the configuration file and any configurations enabled in the `modules.d` directory, or run {{filebeat}} with `--strict.perms=false` specified. Refer to [Config file ownership and permissions](beats://reference/libbeat/config-file-permissions.md).

::::
::::::

::::::{tab-item} Windows
```powershell
PS C:\Program Files\filebeat> Start-Service filebeat
```

By default, Windows log files are stored in `C:\ProgramData\filebeat\Logs`.
::::::

::::::{tab-item} DEB
```shell
sudo service filebeat start
```

::::{note}
If you use an init.d script to start {{filebeat}}, you can’t specify command line flags (refer to [Command reference](beats://reference/filebeat/command-line-options.md)). To specify flags, start {{filebeat}} in the foreground.

::::


Also, refer to [{{filebeat}} and systemd](beats://reference/filebeat/running-with-systemd.md).
::::::

::::::{tab-item} RPM
```shell
sudo service filebeat start
```

::::{note}
If you use an init.d script to start {{filebeat}}, you can’t specify command line flags (refer to [Command reference](beats://reference/filebeat/command-line-options.md)). To specify flags, start {{filebeat}} in the foreground.

::::


Also, refer to [{{filebeat}} and systemd](beats://reference/filebeat/running-with-systemd.md).
::::::

:::::::

### Ingest logs with {{agent}} [observability-ecs-application-logs-ingest-logs-with-agent]

Add the custom logs integration to ingest and centrally manage your logs using {{agent}} and {{fleet}}:


#### Step 1: Add the custom logs integration to your project [observability-ecs-application-logs-step-1-add-the-custom-logs-integration-to-your-project]

To add the custom logs integration to your project:

1. In your {{obs-serverless}} project, go to **Project Settings** → **Integrations**.
2. Type `custom` in the search bar and select **Custom Logs**.
3. Click **Install {{agent}}** at the bottom of the page, and follow the instructions for your system to install the {{agent}}. If you’ve already installed an {{agent}}, you’ll be taken directly to configuring your integration.
4. After installing the {{agent}}, click **Save and continue** to configure the integration from the **Add Custom Logs integration** page.
5. Give your integration a meaningful name and description.
6. Add the **Log file path**. For example, `/var/log/your-logs.log`.
7. Under **Custom log file**, click **Advanced options**.

    ![Screenshot of advanced options location](../../../images/serverless-custom-logs-advanced-options.png "")

8. In the **Processors** text box, add the following YAML configuration to add processors that enhance your data. See [processors](beats://reference/filebeat/filtering-enhancing-data.md) to learn more.

    ```yaml
    processors:
      - add_host_metadata: ~
      - add_cloud_metadata: ~
      - add_docker_metadata: ~
      - add_kubernetes_metadata: ~
    ```

9. Under **Custom configurations**, add the following YAML configuration to collect data.

    ```yaml
    json:
      overwrite_keys: true  <1>
      add_error_key: true  <2>
      expand_keys: true  <3>
      keys_under_root: true  <4>
    fields_under_root: true  <5>
    fields:
      service.name: your_service_name  <6>
      service.version: your_service_version  <6>
      service.environment: your_service_environment  <6>
    ```

    1. Values from the decoded JSON object overwrite the fields that {{agent}} normally adds (type, source, offset, etc.) in case of conflicts.
    2. {{agent}} adds an "error.message" and "error.type: json" key in case of JSON unmarshalling errors.
    3. {{agent}} will recursively de-dot keys in the decoded JSON, and expand them into a hierarchical object structure.
    4. By default, the decoded JSON is placed under a "json" key in the output document. When set to `true`, the keys are copied top level in the output document.
    5. When set to `true`, custom fields are stored as top-level fields in the output document instead of being grouped under a fields sub-dictionary.
    6. The `service.name` (required), `service.version` (optional), and `service.environment` (optional) of the service you’re collecting logs from, used for [Log correlation](../../../solutions/observability/logs/stream-application-logs.md#observability-correlate-application-logs-log-correlation).

10. An agent policy is created that defines the data your {{agent}} collects. If you’ve previously installed an {{agent}} on the host you’re collecting logs from, you can select the **Existing hosts** tab and use an existing agent policy.
11. Click **Save and continue**.


## View logs [observability-ecs-application-logs-view-logs]

Use [Logs Explorer](../../../solutions/observability/logs/logs-explorer.md) to search, filter, and visualize your logs. Refer to the [filter and aggregate logs](../../../solutions/observability/logs/filter-aggregate-logs.md) documentation for more information.
