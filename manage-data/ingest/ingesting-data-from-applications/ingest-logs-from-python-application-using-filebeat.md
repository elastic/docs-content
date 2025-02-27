---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-getting-started-search-use-cases-python-logs.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-getting-started-search-use-cases-python-logs.html
---

# Ingest logs from a Python application using Filebeat

% What needs to be done: Refine

% Scope notes: Merge ESS and ECE versions (should be pretty much identical)

% Use migrated content from existing pages that map to this page:

% - [ ] ./raw-migrated-files/cloud/cloud/ec-getting-started-search-use-cases-python-logs.md
% - [ ] ./raw-migrated-files/cloud/cloud-enterprise/ece-getting-started-search-use-cases-python-logs.md

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$ec-python-logs-create-script$$$

$$$ec-python-logs-filebeat$$$

$$$ec-python-logs-send-ess$$$

$$$ec-python-logs-view-kibana$$$

$$$ece-python-logs-create-script$$$

$$$ece-python-logs-filebeat$$$

$$$ece-python-logs-send-ess$$$

$$$ece-python-logs-view-kibana$$$

This guide demonstrates how to ingest logs from a Python application and deliver them securely into an {{ech}} deployment. You’ll set up Filebeat to monitor a JSON-structured log file that has standard Elastic Common Schema (ECS) formatted fields, and you’ll then view real-time visualizations of the log events in {{kib}} as they occur. While Python is used for this example, this approach to monitoring log output is applicable across many client types. Check the list of [available ECS logging plugins](asciidocalypse://docs/ecs-logging/docs/reference/intro.md).

*Time required: 1 hour*

## Prerequisites [ec_prerequisites_2]

To complete these steps you need to have [Python](https://www.python.org/) installed on your system as well as the [Elastic Common Schema (ECS) logger](asciidocalypse://docs/ecs-logging-python/docs/reference/installation.md) for the Python logging library.

To install *ecs-logging-python*, run:

```sh
python -m pip install ecs-logging
```


## Create a deployment [ec_get_elasticsearch_service_3]

::::{tab-set}

:::{tab-item} Elastic Cloud Hosted
1. [Get a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
2. Log into [Elastic Cloud](https://cloud.elastic.co?page=docs&placement=docs-body).
3. Select **Create deployment**.
4. Give your deployment a name. You can leave all other settings at their default values.
5. Select **Create deployment** and save your Elastic deployment credentials. You need these credentials later on.
6. When the deployment is ready, click **Continue** and a page of **Setup guides** is displayed. To continue to the deployment homepage click **I’d like to do something else**.

Prefer not to subscribe to yet another service? You can also get {{ech}} through [AWS, Azure, and GCP marketplaces](../../../deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md).
:::

:::{tab-item} Elastic Cloud Enterprise
1. Log into the Elastic Cloud Enterprise admin console.
2. Select **Create deployment**.
3. Give your deployment a name. You can leave all other settings at their default values.
4. Select **Create deployment** and save your Elastic deployment credentials. You need these credentials later on.
5. When the deployment is ready, click **Continue** and a page of **Setup guides** is displayed. To continue to the deployment homepage click **I’d like to do something else**.
:::

::::

## Connect securely [ec_connect_securely_2]

When connecting to {{ech}} or {{ece}}, you can use a Cloud ID to specify the connection details. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.

To connect to, stream data to, and issue queries, you need to think about authentication. Two authentication mechanisms are supported, *API key* and *basic authentication*. Here, to get you started quickly, we’ll show you how to use basic authentication, but you can also generate API keys as shown later on. API keys are safer and preferred for production environments.


## Create a Python script with logging [ec-python-logs-create-script]

In this step, you’ll create a Python script that generates logs in JSON format, using Python’s standard logging module.

1. In a local directory, create a new file *elvis.py* and save it with these contents:

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

    This Python script randomly generates one of twelve log messages, continuously, at a random interval of between 1 and 10 seconds. The log messages are written to file `elvis.json`, each with a timestamp, a log level of *info*, *warning*, *error*, or *critical*, and other data. Just to add some variance to the log data, the *info* message *Elvis has left the building* is set to be the most probable log event.

    For simplicity, there is just one log file and it is written to the local directory where `elvis.py` is located. In a production environment you may have multiple log files, associated with different modules and loggers, and likely stored in `/var/log` or similar. To learn more about configuring logging in Python, check [Logging facility for Python](https://docs.python.org/3/library/logging.md).

    Having your logs written in a JSON format with ECS fields allows for easy parsing and analysis, and for standardization with other applications. A standard, easily parsible format becomes increasingly important as the volume and type of data captured in your logs expands over time.

    Together with the standard fields included for each log entry is an extra *http.request.body.content* field. This extra field is there just to give you some additional, interesting data to work with, and also to demonstrate how you can add optional fields to your log data. Check the [ECS Field Reference](asciidocalypse://docs/ecs/docs/reference/ecs-field-reference.md) for the full list of available fields.

2. Let’s give the Python script a test run. Open a terminal instance in the location where you saved *elvis.py* and run the following:

    ```sh
    python elvis.py
    ```

    After the script has run for about 15 seconds, enter *CTRL + C* to stop it. Have a look at the newly generated *elvis.json*. It should contain one or more entries like this one:

    ```json
    {"@timestamp":"2021-06-16T02:19:34.687Z","log.level":"info","message":"Elvis has left the building.","ecs":{"version":"1.6.0"},"http":{"request":{"body":{"content":"Elvis has left the building."}}},"log":{"logger":"app","origin":{"file":{"line":39,"name":"elvis.py"},"function":"<module>"},"original":"Elvis has left the building."},"process":{"name":"MainProcess","pid":3044,"thread":{"id":4444857792,"name":"MainThread"}}}
    ```

3. After confirming that *elvis.py* runs as expected, you can delete *elvis.json*.


## Set up Filebeat [ec-python-logs-filebeat]

Filebeat offers a straightforward, easy to configure way to monitor your Python log files and port the log data into your deployment.

**Get Filebeat**

[Download Filebeat](https://www.elastic.co/downloads/beats/filebeat) and unpack it on the local server from which you want to collect data.

**Configure Filebeat to access {{ech}} or {{ece}}**

In *<localpath>/filebeat-<version>/* (where *<localpath>* is the directory where Filebeat is installed and *<version>* is the Filebeat version number), open the *filebeat.yml* configuration file for editing.

```txt
# =============================== Elastic Cloud ================================

# These settings simplify using Filebeat with the Elastic Cloud (https://cloud.elastic.co/).

# The cloud.id setting overwrites the `output.elasticsearch.hosts` and
# `setup.kibana.host` options.
# You can find the `cloud.id` in the Elastic Cloud web UI.
cloud.id: my-deployment:long-hash <1>

# The cloud.auth setting overwrites the `output.elasticsearch.username` and
# `output.elasticsearch.password` settings. The format is `<user>:<pass>`.
cloud.auth: elastic:password <2>
```

1. Uncomment the `cloud.id` line and add the deployment’s Cloud ID. You can include or omit the *<deploymentname>:* prefix at the beginning of the Cloud ID. Both versions work fine. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.
2. Uncomment the `cloud.auth` line and add the username and password for your deployment that you recorded when you created your deployment. The format is *<username>:<password>*, for example *elastic:57ugj782kvkwmSKg8uVe*.


**Configure Filebeat inputs**

Filebeat has several ways to collect logs. For this example, you’ll configure log collection manually.

In the *filebeat.inputs* section of *filebeat.yml*, set *enabled:* to *true*, and set *paths:* to the location of your log file or files. In this example, set the same directory where you saved *elvis.py*:

```txt
filebeat.inputs:

# Each - is an input. Most options can be set at the input level, so
# you can use different inputs for various configurations.
# Below are the input specific configurations.

- type: log

  # Change to true to enable this input configuration.
  enabled: true

  # Paths that should be crawled and fetched. Glob based paths.
  paths:
    - /path/to/log/files/*.json
```

You can specify a wildcard (***) character to indicate that all log files in the specified directory should be read. You can also use a wildcard to read logs from multiple directories. For example `/var/log/*/*.log`.

**Add the JSON input options**

Filebeat’s input configuration options include several settings for decoding JSON messages. Log files are decoded line by line, so it’s important that they contain one JSON object per line.

For this example, Filebeat uses the following four decoding options.

```txt
  json.keys_under_root: true
  json.overwrite_keys: true
  json.add_error_key: true
  json.expand_keys: true
```

To learn more about these settings, check [JSON input configuration options](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-input-log.md#filebeat-input-log-config-json) and [Decode JSON fields](asciidocalypse://docs/beats/docs/reference/filebeat/decode-json-fields.md) in the Filebeat Reference.

Append the four JSON decoding options to the *Filebeat inputs* section of *filebeat.yml*, so that the section now looks like this:

```yaml
# ============================== Filebeat inputs ===============================

filebeat.inputs:

# Each - is an input. Most options can be set at the input level, so
# you can use different inputs for various configurations.
# Below are the input specific configurations.

- type: log

  # Change to true to enable this input configuration.
  enabled: true

  # Paths that should be crawled and fetched. Glob based paths.
  paths:
    - /path/to/log/files/*.json
  json.keys_under_root: true
  json.overwrite_keys: true
  json.add_error_key: true
  json.expand_keys: true
```

**Finish setting up Filebeat**

Filebeat comes with predefined assets for parsing, indexing, and visualizing your data. To load these assets, run the following from the Filebeat installation directory:

```txt
./filebeat setup -e
```

::::{important}
Depending on variables including the installation location, environment, and local permissions, you might need to [change the ownership](asciidocalypse://docs/beats/docs/reference/libbeat/config-file-permissions.md) of filebeat.yml. You can also try running the command as *root*: *sudo ./filebeat setup -e* or you can disable strict permission checks by running the command with the `--strict.perms=false` option.
::::


The setup process takes a couple of minutes. If everything goes successfully you should get a confirmation message:

```txt
Loaded Ingest pipelines
```

The Filebeat data view (formerly *index pattern*) is now available in Elasticsearch. To verify:

::::{note}
Beginning with Elastic Stack version 8.0, Kibana *index patterns* have been renamed to *data views*. To learn more, check the Kibana [What’s new in 8.0](https://www.elastic.co/guide/en/kibana/8.0/whats-new.html#index-pattern-rename) page.
::::


1. [Login to Kibana](../../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
2. Open the {{kib}} main menu and select **Management** > **{{kib}}** > **Data views**.
3. In the search bar, search for *filebeat*. You should get *filebeat-** in the search results.

**Optional: Use an API key to authenticate**

For additional security, instead of using basic authentication you can generate an Elasticsearch API key through the through the {{ech}} or {{ece}} console, and then configure Filebeat to use the new key to connect securely to your deployment.

1. For {{ech}}, log into [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), or for {{ece}}, log into the admin console.
2. Select the deployment name and go to **☰** > **Management** > **Dev Tools**.
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

    This creates an API key with the cluster `monitor` privilege which gives read-only access for determining the cluster state, and `manage_index_templates` which allows all operations on index templates. Some additional privileges also allow `create_index`, `write`, and `manage` operations for the specified index. The index `manage` privilege is added to enable index refreshes.

4. Click **▶**. The output should be similar to the following:

    ```json
    {
      "api_key": "tV1dnfF-GHI59ykgv4N0U3",
      "id": "2TBR42gBabmINotmvZjv",
      "name": "filebeat-api-key"
    }
    ```

5. Add your API key information to the *Elasticsearch Output* section of `filebeat.yml`, just below *output.elasticsearch:*. Use the format `<id>:<api_key>`. If your results are as shown in this example, enter `2TBR42gBabmINotmvZjv:tV1dnfF-GHI59ykgv4N0U3`.
6. Add a pound (`#`) sign to comment out the *cloud.auth: elastic:<password>* line, since Filebeat will use the API key instead of the deployment username and password to authenticate.

    ```txt
    # =============================== Elastic Cloud ================================

    # These settings simplify using Filebeat with the Elastic Cloud (https://cloud.elastic.co/).

    # The cloud.id setting overwrites the `output.elasticsearch.hosts` and
    # `setup.kibana.host` options.
    # You can find the `cloud.id` in the Elastic Cloud web UI.
    cloud.id: my-deployment:yTMtd5VzdKEuP2NwPbNsb3VkLtKzLmldJDcyMzUyNjBhZGP7MjQ4OTZiNTIxZTQyOPY2C2NeOGQwJGQ2YWQ4M5FhNjIyYjQ9ODZhYWNjKDdlX2Yz4ELhRYJ7

    # The cloud.auth setting overwrites the `output.elasticsearch.username` and
    # `output.elasticsearch.password` settings. The format is `<user>:<pass>`.
    #cloud.auth: elastic:591KhtuAgTP46by9C4EmhGuk

    # ================================== Outputs ===================================

    # Configure what output to use when sending the data collected by the beat.

    # ---------------------------- Elasticsearch Output ----------------------------
    output.elasticsearch:
      # Array of hosts to connect to.
      api_key: "2TBR42gBabmINotmvZjv:tV1dnfF-GHI59ykgv4N0U3"
    ```



## Send the Python logs to Elasticsearch [ec-python-logs-send-ess]

It’s time to send some log data into E{{es}}!

**Launch Filebeat and elvis.py**

Launch Filebeat by running the following from the Filebeat installation directory:

```txt
./filebeat -e -c filebeat.yml
```

In this command:

* The *-e* flag sends output to the standard error instead of the configured log output.
* The *-c* flag specifies the path to the Filebeat config file.

::::{note}
Just in case the command doesn’t work as expected, check the [Filebeat quick start](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-installation-configuration.md#start) for the detailed command syntax for your operating system. You can also try running the command as *root*: *sudo ./filebeat -e -c filebeat.yml*.
::::


Filebeat should now be running and monitoring the contents of *elvis.json*, which actually doesn’t exist yet. So, let’s create it. Open a new terminal instance and run the *elvis.py* Python script:

```sh
python elvis.py
```

Let the script run for a few minutes and maybe brew up a quick coffee or tea ☕ . After that, make sure that the *elvis.json* file is generated as expected and is populated with several log entries.

**Verify the log entries**

The next step is to confirm that the log data has successfully found it’s way into your deployment.

1. [Login to Kibana](../../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
2. Open the {{kib}} main menu and select **Management** > **{{kib}}** > **Data views**.
3. In the search bar, search for *filebeat_. You should get *filebeat-** in the search results.
4. Select *filebeat-**.

The filebeat data view shows a list of fields and their details.


## Create log visualizations in Kibana [ec-python-logs-view-kibana]

Now it’s time to create visualizations based off of the Python application log data.

1. Open the Kibana main menu and select **Dashboard**, then **Create dashboard**.
2. Select **Create visualization**. The [Lens](../../../explore-analyze/visualize/lens.md) visualization editor opens.
3. In the data view dropdown box, select **filebeat-**, if it isn’t already selected.
4. In the **Visualization type dropdown**, select **Bar vertical stacked**, if it isn’t already selected.
5. Check that the [time filter](../../../explore-analyze/query-filter/filtering.md) is set to **Last 15 minutes**.
6. From the **Available fields** list, drag and drop the **@timestamp** field onto the visualization builder.
7. Drag and drop the *log.level* field onto the visualization builder.
8. In the chart settings area, under **Break down by**, select **Top values of log.level** and set **Number of values** to *4*. Since there are four log severity levels, this parameter sets all of them to appear in the chart legend.
9. Select **Refresh**. A stacked bar chart now shows the relative frequency of each of the four log severity levels over time.

    ![A screen capture of the Kibana "Bar vertical stacked" visualization with several bars. The X axis shows "Count of records" and the Y axis shows "@timestamp per 30 seconds". Each bar is divided into the four log severity levels.](../../../images/cloud-ec-python-logs-levels.png "")

10. Select **Save and return** to add this visualization to your dashboard.

Let’s create a second visualization.

1. Select **Create visualization**.
2. Again, make sure that **Visualization type dropdown** is set to **Bar vertical stacked**.
3. From the **Available fields** list, drag and drop the **@timestamp** field onto the visualization builder.
4. Drag and drop the **http.request.body.content** field onto the visualization builder.
5. In the chart settings area, under **Break down by**, select **Top values of http.request.body.content** and set **Number of values** to *12*. Since there are twelve different log messages, this parameter sets all of them to appear in the chart legend.
6. Select **Refresh**. A stacked bar chart now shows the relative frequency of each of the log messages over time.

    ![A screen capture of the visualization builder](../../../images/cloud-ec-python-logs-content.png "")

7. Select **Save and return** to add this visualization to your dashboard.

And now for the final visualization.

1. Select **Create visualization**.
2. In the **Visualization type dropdown** dropdown, select **Donut**.
3. From the list of available fields, drag and drop the **log.level** field onto the visualization builder. A donut chart appears.

    ![A screen capture of a donut chart divided into four sections](../../../images/cloud-ec-python-logs-donut.png "")

4. Select **Save and return** to add this visualization to your dashboard.
5. Select **Save** and add a title to save your new dashboard.

You now have a Kibana dashboard with three visualizations: a stacked bar chart showing the frequency of each log severity level over time, another stacked bar chart showing the frequency of various message strings over time (from the added *http.request.body.content* parameter), and a donut chart showing the relative frequency of each log severity type.

You can add titles to the visualizations, resize and position them as you like, and then save your changes.

**View log data updates in real time**

1. Select **Refresh** on the Kibana dashboard. Since *elvis.py* continues to run and generate log data, your Kibana visualizations update with each refresh.

    ![A screen capture of the completed Kibana dashboard](../../../images/cloud-ec-python-logs-final-dashboard.png "")

2. As your final step, remember to stop Filebeat and the Python script. Enter *CTRL + C* in both your Filebeat terminal and in your `elvis.py` terminal.

You now know how to monitor log files from a Python application, deliver the log event data securely into an {{ech}} or {{ece}} deployment, and then visualize the results in Kibana in real time. Consult the [Filebeat documentation](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-overview.md) to learn more about the ingestion and processing options available for your data. You can also explore our [documentation](../../../manage-data/ingest.md) to learn all about all about ingesting data.

