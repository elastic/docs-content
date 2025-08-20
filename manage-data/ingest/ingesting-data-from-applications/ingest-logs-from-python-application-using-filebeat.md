---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-getting-started-search-use-cases-python-logs.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-getting-started-search-use-cases-python-logs.html
applies_to:
  stack: ga
products:
  - id: cloud-hosted
  - id: cloud-enterprise
---

# Ingest logs from a Python application using Filebeat

In this guide, we show you how to ingest logs from a Python application and deliver them securely into an {{ech}} deployment. You’ll set up Filebeat to monitor a JSON-structured log file with fields formatted according to the Elastic Common Schema (ECS). You’ll then view real-time visualizations of the log events in {{kib}} as they occur.

While we use Python for this example, you can apply the same approach to monitoring log output across many client types. Check the list of [available ECS logging plugins](ecs-logging://reference/intro.md). We also use {{ech}} as the target {{stack}} destination for our logs, but with small modifications, you can adapt the steps in this guide to other deployments such as self-managed {{stack}} and {{ece}}.

In this guide, you will:

- [Create a Python script with logging](#ec-python-logs-create-script)
- [Prepare your connection and authentication details](#ec-authentication-details)
- [Set up Filebeat](#ec-python-logs-filebeat)
- [Send Python logs to {{es}}](#ec-python-logs-send-ess)
- [Create log visualizations in {{kib}}](#ec-python-logs-view-kibana)

_Time required: 1 hour_

## Prerequisites [ec_prerequisites_2]

To complete the steps in this guide, you need to have:

- An {{ech}} deployment with the _Elastic for Observability_ solution view and the superuser credentials provided at deployment creation. For more details, see [Create an {{ech}} deployment](../../../deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md).
- A [Python](https://www.python.org/) version installed which is compatible with the ECS logging library for Python. For a list of compatible Python versions, check the library's [README](https://github.com/elastic/ecs-logging-python/blob/main/README.md).
- The [ECS logging library for Python](ecs-logging-python://reference/index.md) installed.

To install the ECS logging library for Python, run:

```sh
python -m pip install ecs-logging
```

::::{note}
Depending on the Python version you're using, you may need to install the library in a [Python virtual environment](https://docs.python.org/3/library/venv.html).
::::


## Create a Python script with logging [ec-python-logs-create-script]

In this step, you’ll create a Python script that generates logs in JSON format using Python’s standard logging module.

1. In a local directory, create a new file named `elvis.py`, and save it with these contents:

    ```python
    #!/usr/bin/python

    import logging
    import ecs_logging
    import time
    from random import randint

    #logger = logging.getLogger(__name__)
    logger = logging.getLogger("app")
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler('elvis.json')
    handler.setFormatter(ecs_logging.StdlibFormatter())
    logger.addHandler(handler)

    print("Generating log entries...")

    messages = [
        "Elvis has left the building.",#
        "Elvis has left the oven on.",
        "Elvis has two left feet.",
        "Elvis was left out in the cold.",
        "Elvis was left holding the baby.",
        "Elvis left the cake out in the rain.",
        "Elvis came out of left field.",
        "Elvis exited stage left.",
        "Elvis took a left turn.",
        "Elvis left no stone unturned.",
        "Elvis picked up where he left off.",
        "Elvis's train has left the station."
        ]

    while True:
        random1 = randint(0,15)
        random2 = randint(1,10)
        if random1 > 11:
            random1 = 0
        if(random1<=4):
            logger.info(messages[random1], extra={"http.request.body.content": messages[random1]})
        elif(random1>=5 and random1<=8):
            logger.warning(messages[random1], extra={"http.request.body.content": messages[random1]})
        elif(random1>=9 and random1<=10):
            logger.error(messages[random1], extra={"http.request.body.content": messages[random1]})
        else:
            logger.critical(messages[random1], extra={"http.request.body.content": messages[random1]})
        time.sleep(random2)
    ```

    This Python script randomly generates one of twelve log messages, continuously, at a random interval of between 1 and 10 seconds. The log messages are written to an `elvis.json` file, each with a timestamp, a log level of _info_, _warning_, _error_, or _critical_, and other data. To add some variance to the log data, the _info_ message _Elvis has left the building_ is set to be the most probable log event.

    For simplicity, there is just one log file (`elvis.json`), and it is written to the local directory where `elvis.py` is located. In a production environment, you may have multiple log files associated with different modules and loggers and likely stored in `/var/log` or similar. To learn more about configuring logging in Python, check [Logging facility for Python](https://docs.python.org/3/library/logging.html).

    Having your logs written in a JSON format with ECS fields allows for easy parsing and analysis, and for standardization with other applications. A standard, easily parsable format becomes increasingly important as the volume and type of data captured in your logs expands over time.

    Together with the standard fields included for each log entry is an extra `http.request.body.content` field. This extra field is there to give you some additional, interesting data to work with, and also to demonstrate how you can add optional fields to your log data. Check the [ECS field reference](ecs://reference/ecs-field-reference.md) for the full list of available fields.

2. Let’s give the Python script a test run. Open a terminal instance in the location where you saved `elvis.py`, and run the following:

    ```sh
    python elvis.py
    ```

    After the script has run for about 15 seconds, enter _CTRL + C_ to stop it. Have a look at the newly generated `elvis.json` file. It should contain one or more entries like this one:

    ```json
    {"@timestamp":"2025-06-16T02:19:34.687Z","log.level":"info","message":"Elvis has left the building.","ecs":{"version":"1.6.0"},"http":{"request":{"body":{"content":"Elvis has left the building."}}},"log":{"logger":"app","origin":{"file":{"line":39,"name":"elvis.py"},"function":"<module>"},"original":"Elvis has left the building."},"process":{"name":"MainProcess","pid":3044,"thread":{"id":4444857792,"name":"MainThread"}}}
    ```

3. After confirming that `elvis.py` runs as expected, you can delete `elvis.json`.


## Prepare your connection and authentication details [ec-authentication-details]

To connect to your {{ech}} deployment, stream data, and issue queries, you have to specify the connection details using your deployment's Cloud ID, and you have to authenticate using either _basic authentication_ or an _API key_.

### Cloud ID

To find the [Cloud ID](/deploy-manage/deploy/elastic-cloud/find-cloud-id.md) of your deployment, go to the {{kib}} main menu, then select **Management** → **Integrations** → **Connection details**. Note that the Cloud ID value is in the format `deployment-name:hash`. Save this value to use it later.

### Basic authentication

To authenticate and send data to {{ech}}, you can use the username and password you saved when you created your deployment. We use this method to set up the Filebeat connection in the [Configure Filebeat to access {{ech}}](#ec-configure-access) section.

### API key

You can also generate an [API key](/deploy-manage/api-keys.md) through the {{ech}} console, and configure Filebeat to use the new key to connect securely to your deployment. API keys are the preferred method for connecting to production environments.

To create an API key for Filebeat:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), and select your deployment.
2. In the main menu, go to **Developer tools**.
3. Enter the following request:

    ```json
    POST /_security/api_key
    {
     "name": "filebeat-api-key",
     "role_descriptors": {
       "logstash_read_write": {
         "cluster": ["manage_index_templates", "monitor"],
         "index": [
           {
             "names": ["filebeat-*"],
             "privileges": ["create_index", "write", "read", "manage"]
           }
         ]
       }
     }
    }
    ```

    This request creates an API key with the cluster `monitor` privilege, which gives read-only access for determining the cluster state, and `manage_index_templates` privilege, which allows all operations on index templates. Additional privileges allow `create_index`, `write`, and `manage` operations for the specified index (`filebeat-*`). The index `manage` privilege is added to enable index refreshes.

4. Click **▶** to run the request. The output should be similar to the following:

    ```json
    {
      "api_key": "tV1dnfF-GHI59ykgv4N0U3",
      "id": "2TBR42gBabmINotmvZjv",
      "name": "filebeat-api-key"
    }
    ```

Learn how to set up the API key in the Filebeat configuration in the [Configure an API key](#ec-configure-api-key) section.


## Set up Filebeat [ec-python-logs-filebeat]

Filebeat offers a straightforward, easy-to-configure way to monitor your Python log files, and port the log data into your deployment.

### Get Filebeat

[Download Filebeat](https://www.elastic.co/downloads/beats/filebeat), then unpack it on the machine where you created the `elvis.py` script.

### Configure Filebeat to access {{ech}} [ec-configure-access]

Go to the directory where you unpacked Filebeat, and open the `filebeat.yml` configuration file. In the **Elastic Cloud** section, make the following modifications to set up basic authentication:

```yml
# =============================== Elastic Cloud ================================

# These settings simplify using Filebeat with the Elastic Cloud (https://cloud.elastic.co/).

# The cloud.id setting overwrites the `output.elasticsearch.hosts` and
# `setup.kibana.host` options.
# You can find the `cloud.id` in the Elastic Cloud web UI.
cloud.id: deployment-name:hash <1>

# The cloud.auth setting overwrites the `output.elasticsearch.username` and
# `output.elasticsearch.password` settings. The format is `<user>:<pass>`.
cloud.auth: username:password <2>
```

1. Uncomment the `cloud.id` line, and add the deployment’s Cloud ID as the key's value. Note that the `cloud.id` value is in the format `deployment-name:hash`. Find your Cloud ID by going to the {{kib}} main menu, and selecting **Management** → **Integrations** → **Connection details**.
2. Uncomment the `cloud.auth` line, and add the username and password for your deployment in the format `username:password`. For example, `cloud.auth: elastic:57ugj782kvkwmSKg8uVe`.

::::{note}
As an alternative to configuring the connection using [`cloud.id` and `cloud.auth`](beats://reference/filebeat/configure-cloud-id.md), you can specify the {{es}} URL and authentication details directly in the [{{es}} output](beats://reference/filebeat/elasticsearch-output.md). This is useful when connecting to a different deployment type, such as a self-managed cluster.
::::

#### Configure an API key [ec-configure-api-key]

To use an _API key_ to authenticate, leave the comment on the `cloud.auth` line as Filebeat will use an API key instead of the deployment credentials to authenticate.

In the `output.elasticsearch` section of `filebeat.yml`, uncomment the `api_key` line, and add the API key you've created for Filebeat. The format of the value is `id:api_key`, where `id` and `api_key` are the values returned by the [Create API key API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-api-key).

Using the example values returned by the `POST` request we used earlier, the configuration for an API key authentication would look like this:

```yml
cloud.id: my-deployment:yTMtd5VzdKEuP2NwPbNsb3VkLtKzLmldJDcyMzUyNjBhZGP7MjQ4OTZiNTIxZTQyOPY2C2NeOGQwJGQ2YWQ4M5FhNjIyYjQ9ODZhYWNjKDdlX2Yz4ELhRYJ7
#cloud.auth:

output.elasticsearch:
  ...
  api_key: "2TBR42gBabmINotmvZjv:tV1dnfF-GHI59ykgv4N0U3"
```

### Configure Filebeat inputs

Filebeat has several ways to collect logs. For this example, you’ll configure log collection manually. In the `filebeat.inputs` section of `filebeat.yml`:

```yml
filebeat.inputs:

# Each - is an input. Most options can be set at the input level, so
# you can use different inputs for various configurations.
# Below are the input-specific configurations.

# filestream is an input for collecting log messages from files.
- type: filestream

  # Unique ID among all inputs, an ID is required.
  id: my-filestream-id

  # Change to true to enable this input configuration.
  enabled: true <1>

  # Paths that should be crawled and fetched. Glob based paths.
  paths:
    - /path/to/log/files/*.json <2>
```

1. Set `enabled: true`.
2. Set `paths` to the location of your log files. For this example, set `paths` to the directory where you saved `elvis.py`.

You can use a wildcard (`*`) character to indicate that all log files in the specified directory should be read. You can also use a wildcard to read logs from multiple directories. For example, `/var/log/*/*.log`.

### Add the JSON input options

Filebeat’s `filestream` input configuration includes several options for decoding logs structured as JSON messages. You can set these options in `parsers.ndjson`. Filebeat processes the logs line by line, so it’s important that they contain one JSON object per line.

For this example, set Filebeat to use the `ndjson` parser with the following decoding options:

```yml
  parsers:
    - ndjson:
        target: ""
        overwrite_keys: true
        expand_keys: true
        add_error_key: true
        message_key: msg
```

To learn more about these settings, check the [`ndjson` parser's configuration options](beats://reference/filebeat/filebeat-input-filestream.md#filebeat-input-filestream-ndjson) and [Decode JSON fields](beats://reference/filebeat/decode-json-fields.md) in the Filebeat reference.

Append `parsers.ndjson` with the set decoding options to the `filebeat.inputs` section of `filebeat.yml`, so that the section now looks like this:

```yml
# ============================== Filebeat inputs ===============================

filebeat.inputs:

# Each - is an input. Most options can be set at the input level, so
# you can use different inputs for various configurations.
# Below are the input-specific configurations.

# filestream is an input for collecting log messages from files.
- type: filestream

  # Unique ID among all inputs, an ID is required.
  id: my-filestream-id

  # Change to true to enable this input configuration.
  enabled: true

  # Paths that should be crawled and fetched. Glob based paths.
  paths:
    - /path/to/log/files/*.json
    #- c:\programdata\elasticsearch\logs\*

  parsers:
    - ndjson:
        target: ""
        overwrite_keys: true
        expand_keys: true
        add_error_key: true
        message_key: msg
```

### Finish setting up Filebeat

Filebeat comes with predefined assets for parsing, indexing, and visualizing your data. To load these assets into {{kib}} on your {{ech}} deployment, run the following from the Filebeat installation directory:

```sh
./filebeat setup -e
```

::::{important}
Depending on variables including the installation location, environment, and local permissions, you might need to [change the ownership](beats://reference/libbeat/config-file-permissions.md) of `filebeat.yml`. You can also try running the command as `root`: `sudo ./filebeat setup -e*`, or you can disable strict permission checks by running the command with the `--strict.perms=false` option.
::::

The setup process takes a couple of minutes. If the setup is successful, you should get a confirmation message:

```txt
Loaded Ingest pipelines
```

The Filebeat data view (formerly _index pattern_) is now available in Elasticsearch. To verify:

::::{note}
Beginning with Elastic Stack version 8.0, Kibana _index patterns_ have been renamed to _data views_. To learn more, check the {{kib}} [What’s new in 8.0](https://www.elastic.co/guide/en/kibana/8.0/whats-new.html#index-pattern-rename) page.
::::

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), and select your deployment.
2. In the main menu, select **Management** → **Stack Management** → **Data Views**.
3. In the search bar, search for _filebeat_. You should see _filebeat-*_ in the search results.

Filebeat is now set to collect log messages and stream them to your deployment.

## Send Python logs to {{es}} [ec-python-logs-send-ess]

It’s time to send some log data into {{es}}.

### Launch Filebeat and `elvis.py`

In a new terminal:

1. Navigate to the directory where you created the `elvis.py` Python script, then run it:

    ```sh
    python elvis.py
    ```

    Let the script run for a few minutes, then make sure that the `elvis.json` file is generated and is populated with several log entries.

2. Launch Filebeat by running the following from the Filebeat installation directory:

    ```sh
    ./filebeat -c filebeat.yml -e
    ```

    In this command:

    * The `-e` flag sends output to the standard error instead of the configured log output.
    * The `-c` flag specifies the path to the Filebeat config file.

    ::::{note}
    In case the command doesn't work as expected, check the [Filebeat quick start](beats://reference/filebeat/filebeat-installation-configuration.md#installation) for the detailed command syntax for your operating system. You can also try running the command as `root`: `sudo ./filebeat -c filebeat.yml -e`.
    ::::

    Filebeat should now be running and monitoring the contents of the `elvis.json` file.

### Verify the log entries

To confirm that the log data has been successfully sent to your deployment:

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), and select your deployment.
2. In the main menu, select **Management** → **Stack Management** → **Data Views**.
3. In the search bar, search for _filebeat_, then select _filebeat-*_.

The filebeat data view shows a list of fields and their details.

## Create log visualizations in {{kib}} [ec-python-logs-view-kibana]

Now you can create visualizations based off of the Python application log data:

1. In the main menu, select **Dashboards** → **Create dashboard**.
2. Select **Create visualization**. The [Lens](../../../explore-analyze/visualize/lens.md) visualization editor opens.
3. In the **Data view** dropdown box, select _filebeat-*_, if it isn’t already selected.
4. In the menu for setting the visualization type, select **Bar** and **Stacked**, if they aren’t already selected.
5. Check that the [time filter](../../../explore-analyze/query-filter/filtering.md) is set to **Last 15 minutes**.
6. From the **Available fields** list, drag and drop the `@timestamp` field onto the visualization builder.
7. Drag and drop the `log.level` field onto the visualization builder.
8. In the chart settings area under **Breakdown**, select **Top values of log.level**.
9. Set the **Number of values** field to _4_ to display all of four levels of severity in the chart legend.
10. Select **Refresh**. A stacked bar chart now shows the relative frequency of each of the four log severity levels over time.

    ![A screen capture of the Kibana "Bar vertical stacked" visualization with several bars. The X axis shows "Count of records" and the Y axis shows "@timestamp per 30 seconds". Each bar is divided into the four log severity levels.](/manage-data/images/cloud-ec-python-logs-levels.png "")

11. Select **Save and return** to add this visualization to your dashboard.

Let’s create a second visualization:

1. Select **Create visualization**.
2. In the menu for setting the visualization type, select **Bar** and **Stacked**, if they aren’t already selected.
3. From the **Available fields** list, drag and drop the `@timestamp` field onto the visualization builder.
4. Drag and drop the `http.request.body.content` field onto the visualization builder.
5. In the chart settings area under **Breakdown**, select **Top values of http.request.body.content**.
6. Set the **Number of values** to _12_ to display all twelve log messages in the chart legend.
7. Select **Refresh**. A stacked bar chart now shows the relative frequency of each of the log messages over time.

    ![A screen capture of the visualization builder](/manage-data/images/cloud-ec-python-logs-content.png "")

8. Select **Save and return** to add this visualization to your dashboard.

Now, create one final visualization:

1. Select **Create visualization**.
2. In the menu for setting the visualization type, select **Pie**.
3. From the **Available fields** list, drag and drop the `log.level` field onto the visualization builder. A pie chart appears.

    ![A screen capture of a pie chart divided into four sections](/manage-data/images/cloud-ec-python-logs-donut.png "")

4. Select **Save and return** to add this visualization to your dashboard.
5. Select **Save** and add a title to save your new dashboard.

You now have a {{kib}} dashboard with three visualizations: a stacked bar chart showing the frequency of each log severity level over time, another stacked bar chart showing the frequency of various message strings over time (from the added `http.request.body.content` parameter), and a pie chart showing the relative frequency of each log severity type.

You can add titles to the visualizations, resize and position them as you like, and then save your changes.

### View log data in real time

1. Select **Refresh** on the {{kib}} dashboard. Because `elvis.py` continues to run and generate log data, your {{kib}} visualizations update with each refresh.

    ![A screen capture of the completed Kibana dashboard](/manage-data/images/cloud-ec-python-logs-final-dashboard.png "")

2. As a final step, remember to stop Filebeat and the Python script. Enter _CTRL + C_ in both your Filebeat terminal and in your `elvis.py` terminal.

You now know how to monitor log files from a Python application, deliver the log event data securely into an {{ech}} deployment, and then visualize the results in {{kib}} in real time. Consult the [Filebeat documentation](beats://reference/filebeat/index.md) to learn more about the Filebeat ingestion and processing options available for your data. You can also explore our [documentation](../../../manage-data/ingest.md) to learn more about ingesting data with other tools.

