# Plaintext application logs [observability-plaintext-application-logs]

Ingest and parse plaintext logs, including existing logs, from any programming language or framework without modifying your application or its configuration.

Plaintext logs require some additional setup that structured logs do not require:

* To search, filter, and aggregate effectively, you need to parse plaintext logs using an ingest pipeline to extract structured fields. Parsing is based on log format, so you might have to maintain different settings for different applications.
* To [correlate plaintext logs](../../../solutions/observability/logs/plaintext-application-logs.md#observability-plaintext-application-logs-correlate-logs), you need to inject IDs into log messages and parse them using an ingest pipeline.

To ingest, parse, and correlate plaintext logs:

1. Ingest plaintext logs with [{{filebeat}}](../../../solutions/observability/logs/plaintext-application-logs.md#observability-plaintext-application-logs-ingest-logs-with-filebeat) or [{{agent}}](../../../solutions/observability/logs/plaintext-application-logs.md#observability-plaintext-application-logs-ingest-logs-with-agent) and parse them before indexing with an ingest pipeline.
2. [Correlate plaintext logs with an {{apm-agent}}.](../../../solutions/observability/logs/plaintext-application-logs.md#observability-plaintext-application-logs-correlate-logs)
3. [View logs in Logs Explorer](../../../solutions/observability/logs/plaintext-application-logs.md#observability-plaintext-application-logs-view-logs)


## Ingest logs [observability-plaintext-application-logs-ingest-logs]

Send application logs to your project using one of the following shipping tools:

* [**{{filebeat}}:**](../../../solutions/observability/logs/plaintext-application-logs.md#observability-plaintext-application-logs-ingest-logs-with-filebeat) A lightweight data shipper that sends log data to your project.
* [**{{agent}}:**](../../../solutions/observability/logs/plaintext-application-logs.md#observability-plaintext-application-logs-ingest-logs-with-agent) A single agent for logs, metrics, security data, and threat prevention. With Fleet, you can centrally manage {{agent}} policies and lifecycles directly from your project.


### Ingest logs with {{filebeat}} [observability-plaintext-application-logs-ingest-logs-with-filebeat]

::::{important}
Use {{filebeat}} version 8.11+ for the best experience when ingesting logs with {{filebeat}}.

::::


Follow these steps to ingest application logs with {{filebeat}}.


#### Step 1: Install {{filebeat}} [observability-plaintext-application-logs-step-1-install-filebeat]

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

#### Step 2: Connect to your project [observability-plaintext-application-logs-step-2-connect-to-your-project]

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
      "name": "your_api_key",
      "role_descriptors": {
        "filebeat_writer": {
          "cluster": ["manage"],
          "index": [
            {
              "names": ["filebeat-*"],
              "privileges": ["manage", "create_doc"]
            }
          ]
        }
      }
    }
    ```

    Refer to [Grant access using API keys](asciidocalypse://docs/beats/docs/reference/filebeat/beats-api-keys.md) for more information.



#### Step 3: Configure {{filebeat}} [observability-plaintext-application-logs-step-3-configure-filebeat]

Add the following configuration to the `filebeat.yaml` file to start collecting log data.

```yaml
filebeat.inputs:
- type: filestream   <1>
  enabled: true
  paths: /path/to/logs.log   <2>
```

1. Reads lines from an active log file.
2. Paths that you want {{filebeat}} to crawl and fetch logs from.


You can add additional settings to the `filebeat.yml` file to meet the needs of your specific set up. For example, the following settings would add a parser to manage messages that span multiple lines and add service fields:

```yaml
  parsers:
  - multiline:
      type: pattern
      pattern: '^[0-9]{4}-[0-9]{2}-[0-9]{2}'
      negate: true
      match: after
  fields_under_root: true
  fields:
    service.name: your_service_name
    service.environment: your_service_environment
    event.dataset: your_event_dataset
```


#### Step 4: Set up and start {{filebeat}} [observability-plaintext-application-logs-step-4-set-up-and-start-filebeat]

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
from the {{filebeat}} installation directory, start filebeat by running the command that aligns with your system:

:::::::{tab-set}

::::::{tab-item} macOS
```shell
sudo chown root filebeat.yml
sudo ./filebeat -e
```

::::{note}
You’ll be running {{filebeat}} as root, so you need to change ownership of the configuration file and any configurations enabled in the `modules.d` directory, or run {{filebeat}} with `--strict.perms=false` specified. Refer to [Config file ownership and permissions](asciidocalypse://docs/beats/docs/reference/libbeat/config-file-permissions.md).

::::
::::::

::::::{tab-item} Linux
```shell
sudo chown root filebeat.yml
sudo ./filebeat -e
```

::::{note}
You’ll be running {{filebeat}} as root, so you need to change ownership of the configuration file and any configurations enabled in the `modules.d` directory, or run {{filebeat}} with `--strict.perms=false` specified. Refer to [Config file ownership and permissions](asciidocalypse://docs/beats/docs/reference/libbeat/config-file-permissions.md).

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
If you use an init.d script to start {{filebeat}}, you can’t specify command line flags (refer to [Command reference](asciidocalypse://docs/beats/docs/reference/filebeat/command-line-options.md)). To specify flags, start {{filebeat}} in the foreground.

::::


Also, refer to [{{filebeat}} and systemd](asciidocalypse://docs/beats/docs/reference/filebeat/running-with-systemd.md).
::::::

::::::{tab-item} RPM
```shell
sudo service filebeat start
```

::::{note}
If you use an init.d script to start {{filebeat}}, you can’t specify command line flags (refer to [Command reference](asciidocalypse://docs/beats/docs/reference/filebeat/command-line-options.md)). To specify flags, start {{filebeat}} in the foreground.

::::


Also, refer to [{{filebeat}} and systemd](asciidocalypse://docs/beats/docs/reference/filebeat/running-with-systemd.md).
::::::

:::::::

#### Step 5: Parse logs with an ingest pipeline [observability-plaintext-application-logs-step-5-parse-logs-with-an-ingest-pipeline]

Use an ingest pipeline to parse the contents of your logs into structured, [Elastic Common Schema (ECS)](asciidocalypse://docs/ecs/docs/reference/index.md)-compatible fields.

Create an ingest pipeline with a [dissect processor](elasticsearch://reference/ingestion-tools/enrich-processor/dissect-processor.md) to extract structured ECS fields from your log messages. In your project, go to **Developer Tools** and use a command similar to the following example:

```shell
PUT _ingest/pipeline/filebeat*  <1>
{
  "description": "Extracts the timestamp log level and host ip",
  "processors": [
    {
      "dissect": {  <2>
        "field": "message",  <3>
        "pattern": "%{@timestamp} %{log.level} %{host.ip} %{message}"  <4>
      }
    }
  ]
}
```

1. `_ingest/pipeline/filebeat*`: The name of the pipeline. Update the pipeline name to match the name of your data stream. For more information, refer to [Data stream naming scheme](/reference/ingestion-tools/fleet/data-streams.md#data-streams-naming-scheme).
2. `processors.dissect`: Adds a [dissect processor](elasticsearch://reference/ingestion-tools/enrich-processor/dissect-processor.md) to extract structured fields from your log message.
3. `field`: The field you’re extracting data from, `message` in this case.
4. `pattern`: The pattern of the elements in your log data. The pattern varies depending on your log format. `%{@timestamp}`, `%{log.level}`, `%{host.ip}`, and `%{{message}}` are common [ECS](asciidocalypse://docs/ecs/docs/reference/index.md) fields. This pattern would match a log file in this format: `2023-11-07T09:39:01.012Z ERROR 192.168.1.110 Server hardware failure detected.`


Refer to [Extract structured fields](../../../solutions/observability/logs/parse-route-logs.md#observability-parse-log-data-extract-structured-fields) for more on using ingest pipelines to parse your log data.

After creating your pipeline, specify the pipeline for filebeat in the `filebeat.yml` file:

```yaml
output.elasticsearch:
  hosts: ["your-projects-elasticsearch-endpoint"]
  api_key: "id:api_key"
  pipeline: "your-pipeline"  <1>
```

1. Add the pipeline output and the name of your pipeline to the output.



### Ingest logs with {{agent}} [observability-plaintext-application-logs-ingest-logs-with-agent]

Follow these steps to ingest and centrally manage your logs using {{agent}} and {{fleet}}.


#### Step 1: Add the custom logs integration to your project [observability-plaintext-application-logs-step-1-add-the-custom-logs-integration-to-your-project]

To add the custom logs integration to your project:

1. In your {{obs-serverless}} project, go to **Project Settings** → **Integrations**.
2. Type `custom` in the search bar and select **Custom Logs**.
3. Click **Add Custom Logs**.
4. Click **Install {{agent}}** at the bottom of the page, and follow the instructions for your system to install the {{agent}}.
5. After installing the {{agent}}, configure the integration from the **Add Custom Logs integration** page.
6. Give your integration a meaningful name and description.
7. Add the **Log file path**. For example, `/var/log/your-logs.log`.
8. An agent policy is created that defines the data your {{agent}} collects. If you’ve previously installed an {{agent}} on the host you’re collecting logs from, you can select the **Existing hosts** tab and use an existing agent policy.
9. Click **Save and continue**.

You can add additional settings to the integration under **Custom log file** by clicking **Advanced options** and adding YAML configurations to the **Custom configurations**. For example, the following settings would add a parser to manage messages that span multiple lines and add service fields. Service fields are used for [Log correlation](../../../solutions/observability/logs/stream-application-logs.md#observability-correlate-application-logs-log-correlation).

```yaml
  parsers:
  - multiline:
      type: pattern
      pattern: '^[0-9]{4}-[0-9]{2}-[0-9]{2}'
      negate: true
      match: after
  fields_under_root: true
  fields:
    service.name: your_service_name  <1>
    service.version: your_service_version  <1>
    service.environment: your_service_environment  <1>
```

1. for [Log correlation](../../../solutions/observability/logs/stream-application-logs.md#observability-correlate-application-logs-log-correlation), add the `service.name` (required), `service.version` (optional), and `service.environment` (optional) of the service you’re collecting logs from.



#### Step 2: Add an ingest pipeline to your integration [observability-plaintext-application-logs-step-2-add-an-ingest-pipeline-to-your-integration]

To aggregate or search for information in plaintext logs, use an ingest pipeline with your integration to parse the contents of your logs into structured, [Elastic Common Schema (ECS)](asciidocalypse://docs/ecs/docs/reference/index.md)-compatible fields.

1. From the custom logs integration, select **Integration policies** tab.
2. Select the integration policy you created in the previous section.
3. Click **Change defaults** → **Advanced options**.
4. Under **Ingest pipelines**, click **Add custom pipeline**.
5. Create an ingest pipeline with a [dissect processor](elasticsearch://reference/ingestion-tools/enrich-processor/dissect-processor.md) to extract structured fields from your log messages.

    Click **Import processors** and add a similar JSON to the following example:

    ```JSON
    {
      "description": "Extracts the timestamp log level and host ip",
      "processors": [
        {
          "dissect": {  <1>
            "field": "message",  <2>
            "pattern": "%{@timestamp} %{log.level} %{host.ip} %{message}"  <3>
          }
        }
      ]
    }
    ```

    1. `processors.dissect`: Adds a [dissect processor](elasticsearch://reference/ingestion-tools/enrich-processor/dissect-processor.md) to extract structured fields from your log message.
    2. `field`: The field you’re extracting data from, `message` in this case.
    3. `pattern`: The pattern of the elements in your log data. The pattern varies depending on your log format. `%{@timestamp}`, `%{log.level}`, `%{host.ip}`, and `%{{message}}` are common [ECS](asciidocalypse://docs/ecs/docs/reference/index.md) fields. This pattern would match a log file in this format: `2023-11-07T09:39:01.012Z ERROR 192.168.1.110 Server hardware failure detected.`

6. Click **Create pipeline**.
7. Save and deploy your integration.


## Correlate logs [observability-plaintext-application-logs-correlate-logs]

Correlate your application logs with trace events to:

* view the context of a log and the parameters provided by a user
* view all logs belonging to a particular trace
* easily move between logs and traces when debugging application issues

Log correlation works on two levels:

* at service level: annotation with `service.name`, `service.version`, and `service.environment` allow you to link logs with APM services
* at trace level: annotation with `trace.id` and `transaction.id` allow you to link logs with traces

Learn about correlating plaintext logs in the agent-specific ingestion guides:

* [Go](apm-agent-go://reference/logs.md)
* [Java](asciidocalypse://docs/apm-agent-java/docs/reference/logs.md#log-correlation-ids)
* [.NET](apm-agent-dotnet://reference/logs.md)
* [Node.js](asciidocalypse://docs/apm-agent-nodejs/docs/reference/logs.md)
* [Python](asciidocalypse://docs/apm-agent-python/docs/reference/logs.md#log-correlation-ids)
* [Ruby](asciidocalypse://docs/apm-agent-ruby/docs/reference/logs.md)


## View logs [observability-plaintext-application-logs-view-logs]

To view logs ingested by {{filebeat}}, go to **Discover**. Create a data view based on the `filebeat-*` index pattern. Refer to [Create a data view](../../../explore-analyze/find-and-organize/data-views.md) for more information.

To view logs ingested by {{agent}}, go to **Discover** and select the [**Logs Explorer**](../../../solutions/observability/logs/logs-explorer.md) tab. Refer to the [Filter and aggregate logs](../../../solutions/observability/logs/filter-aggregate-logs.md) documentation for more on viewing and filtering your log data.
