# Plaintext application logs [logs-plaintext]

Ingest and parse plaintext logs, including existing logs, from any programming language or framework without modifying your application or its configuration.

Plaintext logs require some additional setup that structured logs do not require:

* To search, filter, and aggregate effectively, you need to parse plaintext logs using an ingest pipeline to extract structured fields. Parsing is based on log format, so you might have to maintain different settings for different applications.
* To [correlate plaintext logs](../../../solutions/observability/logs/plaintext-application-logs.md#correlate-plaintext-logs), you need to inject IDs into log messages and parse them using an ingest pipeline.

To ingest, parse, and correlate plaintext logs:

1. Ingest plaintext logs with [{{filebeat}}](../../../solutions/observability/logs/plaintext-application-logs.md#ingest-plaintext-logs-with-filebeat) or [{{agent}}](../../../solutions/observability/logs/plaintext-application-logs.md#ingest-plaintext-logs-with-the-agent) and parse them before indexing with an ingest pipeline.
2. [Correlate plaintext logs with an {{apm-agent}}.](../../../solutions/observability/logs/plaintext-application-logs.md#correlate-plaintext-logs)
3. [View logs in Logs Explorer](../../../solutions/observability/logs/plaintext-application-logs.md#view-plaintext-logs)


## Ingest logs [ingest-plaintext-logs]

Send application logs to {{es}} using one of the following shipping tools:

* [{{filebeat}}](../../../solutions/observability/logs/plaintext-application-logs.md#ingest-plaintext-logs-with-filebeat) A lightweight data shipper that sends log data to {{es}}.
* [{{agent}}](../../../solutions/observability/logs/plaintext-application-logs.md#ingest-plaintext-logs-with-the-agent) A single agent for logs, metrics, security data, and threat prevention. Combined with Fleet, you can centrally manage {{agent}} policies and lifecycles directly from {{kib}}.


### Ingest logs with {{filebeat}} [ingest-plaintext-logs-with-filebeat]

Follow these steps to ingest application logs with {{filebeat}}.


#### Step 1: Install {{filebeat}} [step-1-plaintext-install-filebeat]

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

#### Step 2: Connect to {{es}} [step-2-plaintext-connect-to-your-project]

Connect to {{es}} using an API key to set up {{filebeat}}. Set the following information in the `filebeat.yml` file:

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
              "privileges": ["manage", "create_doc"]
            }
          ]
        }
      }
    }
    ```

    Refer to [Grant access using API keys](https://www.elastic.co/guide/en/beats/filebeat/current/beats-api-keys.html) for more information.



#### Step 3: Configure {{filebeat}} [step-3-plaintext-configure-filebeat]

Add the following configuration to your `filebeat.yaml` file to start collecting log data.

```yaml
filebeat.inputs:
- type: filestream  <1>
  enabled: true
  paths: /path/to/logs.log  <2>
```

1. Reads lines from an active log file.
2. Paths that you want {{filebeat}} to crawl and fetch logs from.



#### Step 4: Set up and start {{filebeat}} [step-4-plaintext-set-up-and-start-filebeat]

{{filebeat}} comes with predefined assets for parsing, indexing, and visualizing your data. To load these assets:

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

#### Step 5: Parse logs with an ingest pipeline [step-5-plaintext-parse-logs-with-an-ingest-pipeline]

Use an ingest pipeline to parse the contents of your logs into structured, [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/{{ecs_version}}/ecs-reference.html)-compatible fields.

Create an ingest pipeline that defines a [dissect processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/dissect-processor.html) to extract structured ECS fields from your log messages. In your project, navigate to **Developer Tools** and using a command similar to the following example:

```console
PUT _ingest/pipeline/filebeat* <1>
{
  "description": "Extracts the timestamp log level and host ip",
  "processors": [
    {
      "dissect": { <2>
        "field": "message", <3>
        "pattern": "%{@timestamp} %{log.level} %{host.ip} %{message}" <4>
      }
    }
  ]
}
```

1. `_ingest/pipeline/filebeat*`: The name of the pipeline. Update the pipeline name to match the name of your data stream. For more information, refer to [Data stream naming scheme](https://www.elastic.co/guide/en/fleet/current/data-streams.html#data-streams-naming-scheme).
2. `processors.dissect`: Adds a [dissect processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/dissect-processor.html) to extract structured fields from your log message.
3. `field`: The field you’re extracting data from, `message` in this case.
4. `pattern`: The pattern of the elements in your log data. The pattern varies depending on your log format. `%{@timestamp}` is required. `%{log.level}`, `%{host.ip}`, and `%{{message}}` are common [ECS](https://www.elastic.co/guide/en/ecs/{{ecs_version}}/ecs-reference.html) fields. This pattern would match a log file in this format: `2023-11-07T09:39:01.012Z ERROR 192.168.1.110 Server hardware failure detected.`


Refer to [Extract structured fields](../../../solutions/observability/logs/parse-route-logs.md#logs-stream-parse) for more on using ingest pipelines to parse your log data.

After creating your pipeline, specify the pipeline for filebeat in the `filebeat.yml` file:

```yaml
output.elasticsearch:
  hosts: ["your-projects-elasticsearch-endpoint"]
  api_key: "id:api_key"
  pipeline: "your-pipeline" <1>
```

1. Add the `pipeline` output and the name of your pipeline to the output.



### Ingest logs with the {{agent}} [ingest-plaintext-logs-with-the-agent]

Follow these steps to ingest and centrally manage your logs using {{agent}} and {{fleet}}.


#### Step 1: Add the custom logs integration to your project [step-1-plaintext-add-the-custom-logs-integration-to-your-project]

To add the custom logs integration to your project:

1. Find **Integrations** in the main menu or use the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md).
2. Type `custom` in the search bar and select **Custom Logs**.
3. Click **Add Custom Logs**.
4. Click **Install {{agent}}** at the bottom of the page, and follow the instructions for your system to install the {{agent}}.
5. After installing the {{agent}}, configure the integration from the **Add Custom Logs integration** page.
6. Give your integration a meaningful name and description.
7. Add the **Log file path**. For example, `/var/log/your-logs.log`.
8. Give your agent policy a name. The agent policy defines the data your {{agent}} collects.
9. Save your integration to add it to your deployment.


#### Step 2: Add an ingest pipeline to your integration [step-2-plaintext-add-an-ingest-pipeline-to-your-integration]

To aggregate or search for information in plaintext logs, use an ingest pipeline with your integration to parse the contents of your logs into structured, [Elastic Common Schema (ECS)](https://www.elastic.co/guide/en/ecs/{{ecs_version}}/ecs-reference.html)-compatible fields.

1. From the custom logs integration, select **Integration policies** tab.
2. Select the integration policy you created in the previous section.
3. Click **Change defaults → Advanced options**.
4. Under **Ingest pipelines**, click **Add custom pipeline**.
5. Create an ingest pipeline with a [dissect processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/dissect-processor.html) to extract structured fields from your log messages.

    Click **Import processors** and add a similar JSON to the following example:

    ```JSON
    {
      "description": "Extracts the timestamp log level and host ip",
      "processors": [
        {
          "dissect": { <1>
            "field": "message", <2>
            "pattern": "%{@timestamp} %{log.level} %{host.ip} %{message}" <3>
          }
        }
      ]
    }
    ```

    1. `processors.dissect`: Adds a [dissect processor](https://www.elastic.co/guide/en/elasticsearch/reference/current/dissect-processor.html) to extract structured fields from your log message.
    2. `field`: The field you’re extracting data from, `message` in this case.
    3. `pattern`: The pattern of the elements in your log data. The pattern varies depending on your log format. `%{@timestamp}`, `%{log.level}`, `%{host.ip}`, and `%{{message}}` are common [ECS](https://www.elastic.co/guide/en/ecs/{{ecs_version}}/ecs-reference.html) fields. This pattern would match a log file in this format: `2023-11-07T09:39:01.012Z ERROR 192.168.1.110 Server hardware failure detected.`

6. Click **Create pipeline**.
7. Save and deploy your integration.


## Correlate logs [correlate-plaintext-logs]

Correlate your application logs with trace events to:

* view the context of a log and the parameters provided by a user
* view all logs belonging to a particular trace
* easily move between logs and traces when debugging application issues

Log correlation works on two levels:

* at service level: annotation with `service.name`, `service.version`, and `service.environment` allow you to link logs with APM services
* at trace level: annotation with `trace.id` and `transaction.id` allow you to link logs with traces

Learn about correlating plaintext logs in the agent-specific ingestion guides:

* [Go](https://www.elastic.co/guide/en/apm/agent/go/current/logs.html)
* [Java](https://www.elastic.co/guide/en/apm/agent/java/current/logs.html#log-correlation-ids)
* [.NET](https://www.elastic.co/guide/en/apm/agent/dotnet/current/logs.html)
* [Node.js](https://www.elastic.co/guide/en/apm/agent/nodejs/current/log-correlation.html)
* [Python](https://www.elastic.co/guide/en/apm/agent/python/current/logs.html#log-correlation-ids)
* [Ruby](https://www.elastic.co/guide/en/apm/agent/ruby/current/log-correlation.html)


## View logs [view-plaintext-logs]

To view logs ingested by {{filebeat}}, go to **Discover** from the main menu and create a data view based on the `filebeat-*` index pattern. Refer to [Create a data view](../../../explore-analyze/find-and-organize/data-views.md) for more information.

To view logs ingested by {{agent}}, go to Logs Explorer by clicking **Explorer** under **Logs** from the {{observability}} main menu. Refer to the [Filter and aggregate logs](../../../solutions/observability/logs/filter-aggregate-logs.md) documentation for more information on viewing and filtering your logs in {{kib}}.
