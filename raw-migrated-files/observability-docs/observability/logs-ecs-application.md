# ECS formatted application logs [logs-ecs-application]

Logs formatted in Elastic Common Schema (ECS) don’t require manual parsing, and the configuration can be reused across applications. ECS-formatted logs, when paired with an {{apm-agent}}, allow you to correlate logs to easily view logs that belong to a particular trace.

You can format your logs in ECS format the following ways:

* [ECS loggers](../../../solutions/observability/logs/ecs-formatted-application-logs.md#ecs-loggers): plugins for your logging libraries that reformat your logs into ECS format.
* [APM agent ECS reformatting](../../../solutions/observability/logs/ecs-formatted-application-logs.md#apm-agent-ecs-reformatting): Java, Ruby, and Python {{apm-agent}}s automatically reformat application logs to ECS format without a logger.


## ECS loggers [ecs-loggers]

ECS loggers reformat your application logs into ECS-compatible JSON, removing the need for manual parsing. ECS loggers require {{filebeat}} or {{agent}} configured to monitor and capture application logs. In addition, pairing ECS loggers with your framework’s {{apm-agent}} allows you to correlate logs to easily view logs that belong to a particular trace.


### Get started with ECS loggers [get-started-ecs-logging]

For more information on adding an ECS logger to your application, refer to the guide for your framework:

* [.NET](https://www.elastic.co/guide/en/ecs-logging/dotnet/{{ecs-logging-dotnet}}/setup.html)
* Go: [zap](https://www.elastic.co/guide/en/ecs-logging/go-zap/{{ecs-logging-go-zap}}/setup.html), [logrus](https://www.elastic.co/guide/en/ecs-logging/go-logrus/{{ecs-logging-go-logrus}}/setup.html)
* [Java](https://www.elastic.co/guide/en/ecs-logging/java/{{ecs-logging-java}}/setup.html)
* Node.js: [morgan](https://www.elastic.co/guide/en/ecs-logging/nodejs/{{ecs-logging-nodejs}}/morgan.html), [pino](https://www.elastic.co/guide/en/ecs-logging/nodejs/{{ecs-logging-nodejs}}/pino.html), [winston](https://www.elastic.co/guide/en/ecs-logging/nodejs/{{ecs-logging-nodejs}}/winston.html)
* [PHP](https://www.elastic.co/guide/en/ecs-logging/php/{{ecs-logging-php}}/setup.html)
* [Python](https://www.elastic.co/guide/en/ecs-logging/python/{{ecs-logging-python}}/installation.html)
* [Ruby](https://www.elastic.co/guide/en/ecs-logging/ruby/{{ecs-logging-ruby}}/setup.html)


## APM agent ECS reformatting [apm-agent-ecs-reformatting]

Java, Ruby, and Python {{apm-agent}}s can automatically reformat application logs to ECS format without an ECS logger or the need to modify your application. The {{apm-agent}} also allows for log correlation so you can easily view logs that belong to a particular trace.

To set up log ECS reformatting:

1. [Enable {{apm-agent}} reformatting](../../../solutions/observability/logs/ecs-formatted-application-logs.md#enable-log-ecs-reformatting)
2. [Ingest logs with {{filebeat}} or {{agent}}](../../../solutions/observability/logs/ecs-formatted-application-logs.md#ingest-ecs-logs)
3. [View logs in Logs Explorer](../../../solutions/observability/logs/ecs-formatted-application-logs.md#view-ecs-logs)


### Enable log ECS reformatting [enable-log-ecs-reformatting]

Log ECS reformatting is controlled by the `log_ecs_reformatting` configuration option, and is disabled by default. Refer to the guide for your framework for information on enabling:

* [Java](https://www.elastic.co/guide/en/apm/agent/java/current/config-logging.html#config-log-ecs-reformatting)
* [Ruby](https://www.elastic.co/guide/en/apm/agent/ruby/current/configuration.html#config-log-ecs-formatting)
* [Python](https://www.elastic.co/guide/en/apm/agent/python/current/configuration.html#config-log_ecs_reformatting)


### Ingest logs [ingest-ecs-logs]

After enabling log ECS reformatting, send your application logs to your project using one of the following shipping tools:

* [{{filebeat}}](../../../solutions/observability/logs/ecs-formatted-application-logs.md#ingest-ecs-logs-with-filebeat): A lightweight data shipper that sends log data to your project.
* [{{agent}}](../../../solutions/observability/logs/ecs-formatted-application-logs.md#ingest-ecs-logs-with-agent): A single agent for logs, metrics, security data, and threat prevention. With Fleet, you can centrally manage {{agent}} policies and lifecycles directly from your project.


#### Ingest logs with {{filebeat}} [ingest-ecs-logs-with-filebeat]

Follow these steps to ingest application logs with {{filebeat}}.


#### Step 1: Install {{filebeat}} [step-1-ecs-install-filebeat]

Install {{filebeat}} on the server you want to monitor by running the commands that align with your system:

:::::::{tab-set}

::::::{tab-item} DEB
```sh
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-9.0.0-beta1-darwin-x86_64.tar.gz
tar xzvf filebeat-9.0.0-beta1-darwin-x86_64.tar.gz
```
::::::

::::::{tab-item} RPM
```sh
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-9.0.0-beta1-linux-x86_64.tar.gz
tar xzvf filebeat-9.0.0-beta1-linux-x86_64.tar.gz
```
::::::

::::::{tab-item} macOS
1. Download the {{filebeat}} Windows zip file: https\://artifacts.elastic.co/downloads/beats/filebeat/filebeat-9.0.0-beta1-windows-x86_64.zip[https\://artifacts.elastic.co/downloads/beats/filebeat/filebeat-9.0.0-beta1-windows-x86_64.zip]
2. Extract the contents of the zip file into `C:\Program Files`.
3. Rename the `filebeat-{{version}}-windows-x86_64` directory to `{{filebeat}}`.
4. Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select **Run As Administrator**).
5. From the PowerShell prompt, run the following commands to install {{filebeat}} as a Windows service:

    ```powershell
    PS > cd 'C:\Program Files\{filebeat}'
    PS C:\Program Files\{filebeat}> .\install-service-filebeat.ps1
    ```


If script execution is disabled on your system, you need to set the execution policy for the current session to allow the script to run. For example: `PowerShell.exe -ExecutionPolicy UnRestricted -File .\install-service-filebeat.ps1`.
::::::

::::::{tab-item} Linux
```sh
curl -L -O https\://artifacts.elastic.co/downloads/beats/filebeat/filebeat-9.0.0-beta1-amd64.deb
sudo dpkg -i filebeat-9.0.0-beta1-amd64.deb
```
::::::

::::::{tab-item} Windows
```sh
curl -L -O https\://artifacts.elastic.co/downloads/beats/filebeat/filebeat-9.0.0-beta1-x86_64.rpm
sudo rpm -vi filebeat-9.0.0-beta1-x86_64.rpm
```
::::::

:::::::

#### Step 2: Connect to your project [step-2-ecs-connect-to-your-project]

Connect to your project using an API key to set up {{filebeat}}. Set the following information in the `filebeat.yml` file:

```yaml
output.elasticsearch:
  hosts: ["your-projects-elasticsearch-endpoint"]
  api_key: "id:api_key"
```

1. Set the `hosts` to your deployment’s {{es}} endpoint. Copy the {{es}} endpoint from **Help menu (![help icon](../../../images/observability-help-icon.png "")) → Connection details**. For example, `https://my-deployment.es.us-central1.gcp.cloud.es.io:443`.
2. From **Developer tools**, run the following command to create an API key that grants `manage` permissions for the `cluster` and the `filebeat-*` indices using:

    ```console
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

    Refer to [Grant access using API keys](https://www.elastic.co/guide/en/beats/filebeat/current/beats-api-keys.html) for more information.



#### Step 3: Configure {{filebeat}} [step-3-ecs-configure-filebeat]

Add the following configuration to your `filebeat.yaml` file to start collecting log data.

```yaml
filebeat.inputs:
- type: filestream  <1>
  enabled: true
  paths: /path/to/logs.log  <2>
```

1. Reads lines from an active log file.
2. Paths that you want {{filebeat}} to crawl and fetch logs from.



#### Step 4: Set up and start {{filebeat}} [step-4-ecs-set-up-and-start-filebeat]

From the {{filebeat}} installation directory, set the [index template](../../../manage-data/data-store/templates.md) by running the command that aligns with your system:

:::::::{tab-set}

::::::{tab-item} DEB
```sh
./filebeat setup -e
```
::::::

::::::{tab-item} RPM
```sh
./filebeat setup -e
```
::::::

::::::{tab-item} MacOS
```sh
PS > .\filebeat.exe setup -e
```
::::::

::::::{tab-item} Linux
```sh
filebeat setup -e
```
::::::

::::::{tab-item} Windows
```sh
filebeat setup -e
```
::::::

:::::::
From the {{filebeat}} installation directory, start filebeat by running the command that aligns with your system:

:::::::{tab-set}

::::::{tab-item} DEB
```sh
sudo service filebeat start
```

::::{note}
If you use an `init.d` script to start Filebeat, you can’t specify command line flags (see [Command reference](https://www.elastic.co/guide/en/beats/filebeat/master/command-line-options.html)). To specify flags, start Filebeat in the foreground.
::::


Also see [Filebeat and systemd](https://www.elastic.co/guide/en/beats/filebeat/master/running-with-systemd.html).
::::::

::::::{tab-item} RPM
```sh
sudo service filebeat start
```

::::{note}
If you use an `init.d` script to start Filebeat, you can’t specify command line flags (see [Command reference](https://www.elastic.co/guide/en/beats/filebeat/master/command-line-options.html)). To specify flags, start Filebeat in the foreground.
::::


Also see [Filebeat and systemd](https://www.elastic.co/guide/en/beats/filebeat/master/running-with-systemd.html).
::::::

::::::{tab-item} MacOS
```sh
./filebeat -e
```
::::::

::::::{tab-item} Linux
```sh
./filebeat -e
```
::::::

::::::{tab-item} Windows
```sh
PS C:\Program Files\filebeat> Start-Service filebeat
```

By default, Windows log files are stored in `C:\ProgramData\filebeat\Logs`.
::::::

:::::::

#### Ingest logs with {{agent}} [ingest-ecs-logs-with-agent]

Add the custom logs integration to ingest and centrally manage your logs using {{agent}} and {{fleet}}:


#### Add the custom logs integration to your project [step-1-add-the-custom-logs-integration-to-your-project-ecs]

To add the custom logs integration to your project:

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Type `custom` in the search bar and select **Custom Logs**.
3. Click **Install {{agent}}** at the bottom of the page, and follow the instructions for your system to install the {{agent}}.
4. After installing the {{agent}}, click **Save and continue** to configure the integration from the **Add Custom Logs integration** page.
5. Give your integration a meaningful name and description.
6. Add the **Log file path**. For example, `/var/log/your-logs.log`.
7. Click **Advanced options**.
8. In the **Processors** text box, add the following YAML configuration to add processors that enhance your data. Refer to [processors](https://www.elastic.co/guide/en/beats/filebeat/current/filtering-and-enhancing-data.html) to learn more.

    ```yaml
    processors:
      - add_host_metadata: \~
      - add_cloud_metadata: \~
      - add_docker_metadata: \~
      - add_kubernetes_metadata: \~
    ```

9. Under **Custom configurations**, add the following YAML configuration to collect data.

    ```yaml
      json:
        overwrite_keys: true <1>
        add_error_key: true <2>
        expand_keys: true <3>
        keys_under_root: true <4>
      fields_under_root: true <5>
      fields:
        service.name: your_service_name <6>
        service.version: your_service_version <6>
        service.environment: your_service_environment <6>
    ```

    1. Values from the decoded JSON object overwrite the fields that {{agent}} normally adds (type, source, offset, etc.) in case of conflicts.
    2. {{agent}} adds an "error.message" and "error.type: json" key in case of JSON unmarshalling errors.
    3. {{agent}} will recursively de-dot keys in the decoded JSON, and expand them into a hierarchical object structure.
    4. By default, the decoded JSON is placed under a "json" key in the output document. When set to `true`, the keys are copied top level in the output document.
    5. When set to `true`, custom fields are stored as top-level fields in the output document instead of being grouped under a fields sub-dictionary.
    6. The `service.name` (required), `service.version` (optional), and `service.environment` (optional) of the service you’re collecting logs from, used for log correlation.

10. Give your agent policy a name. The agent policy defines the data your {{agent}} collects.
11. Save your integration to add it to your deployment.


## View logs [view-ecs-logs]

Refer to the [Filter and aggregate logs](../../../solutions/observability/logs/filter-aggregate-logs.md) documentation for more information on viewing and filtering your logs in {{kib}}.
