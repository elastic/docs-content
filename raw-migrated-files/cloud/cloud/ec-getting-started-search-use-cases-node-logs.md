# Ingest logs from a Node.js web application using Filebeat [ec-getting-started-search-use-cases-node-logs]

This guide demonstrates how to ingest logs from a Node.js web application and deliver them securely into an {{ech}} deployment. You’ll set up Filebeat to monitor a JSON-structured log file that has standard Elastic Common Schema (ECS) formatted fields, and you’ll then view real-time visualizations of the log events in Kibana as requests are made to the Node.js server. While Node.js is used for this example, this approach to monitoring log output is applicable across many client types. Check the list of [available ECS logging plugins](asciidocalypse://docs/ecs-logging/docs/reference/intro.md#_get_started).

This guide presents:

1. [Prerequisites](../../../manage-data/ingest/ingesting-data-from-applications/ingest-logs-from-nodejs-web-application-using-filebeat.md#ec-node-logs-prerequisites)
2. [Get {{ech}}](../../../manage-data/ingest/ingesting-data-from-applications/ingest-logs-from-nodejs-web-application-using-filebeat.md#ec-node-logs-trial)
3. [Connect securely](../../../manage-data/ingest/ingesting-data-from-applications/ingest-logs-from-nodejs-web-application-using-filebeat.md#ec-node-logs-connect-securely)
4. [Create a Node.js web application with logging](../../../manage-data/ingest/ingesting-data-from-applications/ingest-logs-from-nodejs-web-application-using-filebeat.md#ec-node-logs-create-server-script)
5. [Create a Node.js HTTP request application](../../../manage-data/ingest/ingesting-data-from-applications/ingest-logs-from-nodejs-web-application-using-filebeat.md#ec-node-logs-create-request-script)
6. [Set up Filebeat](../../../manage-data/ingest/ingesting-data-from-applications/ingest-logs-from-nodejs-web-application-using-filebeat.md#ec-node-logs-filebeat)
7. [Send the Node.js logs to Elasticsearch](../../../manage-data/ingest/ingesting-data-from-applications/ingest-logs-from-nodejs-web-application-using-filebeat.md#ec-node-logs-send-ess)
8. [Create log visualizations in Kibana](../../../manage-data/ingest/ingesting-data-from-applications/ingest-logs-from-nodejs-web-application-using-filebeat.md#ec-node-logs-view-kibana)

*Time required: 1.5 hours*


## Prerequisites [ec-node-logs-prerequisites]

To complete these steps you need the following applications installed on your system:

* [Node.js](https://nodejs.org/) - You will set up a simple Node.js web server and client application. Check the Node.js download page for installation instructions.

::::{tip}
For the three following packages, you can create a working directory to install the packages using the Node package manager (NPM). Then, you can run your Node.js webserver and client from the same directory so that it can use the packages. Alternatively, you can also install the Node packages globally by running the Node package install commands with the `-g` option. Refer to the NPM [package installation instructions](https://docs.npmjs.com/downloading-and-installing-packages-globally) for details.
::::


* [winston](https://www.npmjs.com/package/winston) - This is a popular logging package for Node.js. Create a new, local directory and run the following command to install winston in it:

    ```sh
    npm install winston
    ```

* The [Elastic Common Schema (ECS) formatter](asciidocalypse://docs/ecs-logging-nodejs/docs/reference/winston.md) for the Node.js winston logger - This plugin formats your Node.js logs into an ECS structured JSON format ideally suited for ingestion into Elasticsearch. To install the ECS winston logger, run the following command in your working directory so that the package is installed in the same location as the winston package:

    ```sh
    npm install @elastic/ecs-winston-format
    ```

* [Got](https://www.npmjs.com/package/got) - Got is a "Human-friendly and powerful HTTP request library for Node.js." - This plugin can be used to query the sample web server used in the tutorial. To install the Got package, run the following command in your working directory:

    ```sh
    npm install got
    ```



## Get {{ech}} [ec-node-logs-trial]

1. [Get a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
2. Log into [Elastic Cloud](https://cloud.elastic.co?page=docs&placement=docs-body).
3. Select **Create deployment**.
4. Give your deployment a name. You can leave all other settings at their default values.
5. Select **Create deployment** and save your Elastic deployment credentials. You need these credentials later on.
6. When the deployment is ready, click **Continue** and a page of **Setup guides** is displayed. To continue to the deployment homepage click **I’d like to do something else**.

Prefer not to subscribe to yet another service? You can also get {{ech}} through [AWS, Azure, and GCP marketplaces](../../../deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md).


## Connect securely [ec-node-logs-connect-securely]

When connecting to {{ech}} you can use a Cloud ID to specify the connection details. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.

To connect to, stream data to, and issue queries with {{ech}}, you need to think about authentication. Two authentication mechanisms are supported, *API key* and *basic authentication*. Here, to get you started quickly, we’ll show you how to use basic authentication, but you can also generate API keys as shown later on. API keys are safer and preferred for production environments.


## Create a Node.js web application with logging [ec-node-logs-create-server-script]

Next, create a basic Node.js script that runs a web server and logs HTTP requests.

1. In the same local directory where you installed the winston and ECS formatter packages, create a new file *webserver.js* and save it with these contents:

    ```javascript
    const http = require('http')
    const winston = require('winston')
    const ecsFormat = require('@elastic/ecs-winston-format')

    const logger = winston.createLogger({
      level: 'debug',
      format: ecsFormat({ convertReqRes: true }),
      transports: [
        //new winston.transports.Console(),
        new winston.transports.File({
          //path to log file
          filename: 'logs/log.json',
          level: 'debug'
        })
      ]
    })

    const server = http.createServer(handler)
    server.listen(3000, () => {
      logger.info('listening at http://localhost:3000')
    })

    function handler (req, res) {
     res.setHeader('Foo', 'Bar')
      res.end('ok')
      logger.info('handled request', { req, res })
    }
    ```

    This Node.js script runs a web server at `http://localhost:3000` and uses the winston logger to send logging events, based on HTTP requests, to the file `log.json`.

2. Try a test run of the Node.js script:

    ```sh
    node webserver.js
    ```

3. With the script running, open a web browser to `http://localhost:3000` and there should be a simple `ok` message.
4. In the directory where you created `webserver.js`, you should now find a newly created `log.json` file. Open the file and check the contents. There should be one log entry indicating that Node.js is listening on the localhost port, and another entry for the HTTP request from when you opened `localhost` in your browser.

    Leave `webserver.js` running for now and we’ll send it some HTTP requests.



## Create a Node.js HTTP request application [ec-node-logs-create-request-script]

In this step, you’ll create a Node.js application that sends HTTP requests to your web server.

1. In your working directory, create a file `webrequests.js` and save it with these contents:

    ```javascript
    const got = require('got');

    const addresses = [
        'aardvark@the.zoo',
        'crocodile@the.zoo',
        'elephant@the.zoo',
        'emu@the.zoo',
        'hippopotamus@the.zoo',
        'llama@the.zoo',
        'octopus@the.zoo',
        'otter@the.zoo',
        'panda@the.zoo',
        'pangolin@the.zoo',
        'tortoise@the.zoo',
        'walrus@the.zoo'
    ];

    const method = [
        'get',
        'put',
        'post'
    ];

    async function sleep(millis) {
        return new Promise(resolve => setTimeout(resolve, millis));
    }

    (async () => {
        while (true) {
            var type = Math.floor(Math.random() * method.length);
            var email = Math.floor(Math.random() * addresses.length);
            var sleeping = Math.floor(Math.random() * 9) + 1;

            switch (method[type]) {
                case 'get':
                    try {
                        const response = await got.get('http://localhost:3000/', {
                            headers: {
                                from: addresses[email]
                            }
                        }).json();
                        console.log(response.body);
                    } catch (error) {
                        console.log(error.response.body);
                    }
                    break; // end case 'get'
                case 'put':
                    try {
                        const response = await got.put('http://localhost:3000/', {
                            headers: {
                                from: addresses[email]
                            }
                        }).json();
                        console.log(response.body);
                    } catch (error) {
                        console.log(error.response.body);
                    }
                    break; // end case 'put'
                case 'post':
                    try {
                        const {
                            data
                        } = await got.post('http://localhost:3000/', {
                            headers: {
                                from: addresses[email]
                            }
                        }).json();
                        console.log(data);
                    } catch (error) {
                        console.log(error.response.body);
                    }
                    break; // end case 'post'
            } // end switch on method
        await sleep(sleeping * 1000);
        }
    })();
    ```

    This Node.js app generates HTTP requests with a random method of type `GET`, `POST`, or `PUT`, and a random `from` request header using various pretend email addresses. The requests are sent at random intervals between 1 and 10 seconds.

    The [Got package](https://www.npmjs.com/package/got) is used to send the requests, and they are directed to your web server at `http://localhost:3000`. To learn about sending custom headers such as the `from` field used in this example, check [headers](https://github.com/sindresorhus/got/blob/0fb6ec60d299fd9b48966608a4c3f201746d821c/documentation/2-options.md#headers) in the Got documentation.

2. In a new terminal window, give the Node.js script a trial run:

    ```sh
    node webrequests.js
    ```

3. After the script has run for about 30 seconds, enter *CTRL + C* to stop it. Have a look at your Node.js `logs/log.json` file. It should contain some entries like this one:

    ```json
    {"@timestamp":"2021-09-09T18:42:20.799Z","log.level":"info","message":"handled request","ecs":{"version":"1.6.0"},"http":{"version":"1.1","request":{"method":"POST","headers":{"user-agent":"got (https://github.com/sindresorhus/got)","from":"octopus@the.zoo","accept":"application/json","accept-encoding":"gzip, deflate, br","host":"localhost:3000","connection":"close","content-length":"0"},"body":{"bytes":0}},"response":{"status_code":200,"headers":{"foo":"Bar"}}},"url":{"path":"/","full":"http://localhost:3000/"},"client":{"address":"::ffff:127.0.0.1","ip":"::ffff:127.0.0.1","port":49930},"user_agent":{"original":"got (https://github.com/sindresorhus/got)"}}
    ```

    Each log entry contains details of the HTTP request. In particular, in this example you can find the timestamp of the request, a request method of type `PUT`, and a request `from` header with the email address `octopus@the.zoo`. Your example will likely be a bit different since the request type and the email address are generated randomly.

    Having your logs written in a JSON format with ECS fields allows for easy parsing and analysis, and for standardization with other applications. A standard, easily parsible format becomes increasingly important as the volume and type of data captured in your logs expands over time.

4. After confirming that both `webserver.js` and `webrequests.js` run as expected, enter *CTRL + C* to stop the Node.js script, and also delete `log.json`.


## Set up Filebeat [ec-node-logs-filebeat]

Filebeat offers a straightforward, easy to configure way to monitor your Node.js log files and port the log data into {{ech}}.

**Get Filebeat**

[Download Filebeat](https://www.elastic.co/downloads/beats/filebeat) and unpack it on the local server from which you want to collect data.

**Configure Filebeat to access {{ech}}**

In *<localpath>/filebeat-<version>/* (where *<localpath>* is the directory where Filebeat is installed and *<version>* is the Filebeat version number), open the *filebeat.yml* configuration file for editing.

```txt
# =============================== Elastic Cloud ================================

# These settings simplify using Filebeat with the Elastic Cloud (https://cloud.elastic.co/).

# The cloud.id setting overwrites the `output.elasticsearch.hosts` and
# `setup.kibana.host` options.
# You can find the `cloud.id` in the Elastic Cloud web UI.
cloud.id: my-deployment:yTMtd5VzdKEuP2NwPbNsb3VkLtKzLmldJDcyMzUyNjBhZGP7MjQ4OTZiNTIxZTQyOPY2C2NeOGQwJGQ2YWQ4M5FhNjIyYjQ9ODZhYWNjKDdlX2Yz4ELhRYJ7 <1>

# The cloud.auth setting overwrites the `output.elasticsearch.username` and
# `output.elasticsearch.password` settings. The format is `<user>:<pass>`.
cloud.auth: elastic:591KhtuAgTP46by9C4EmhGuk <2>
```

1. Uncomment the `cloud.id` line and add the deployment’s Cloud ID. You can include or omit the *<deploymentname>:* prefix at the beginning of the Cloud ID. Both versions work fine. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.
2. Uncomment the `cloud.auth` line and add the username and password for your deployment that you recorded when you created your deployment. The format is *<username>:<password>*, for example *elastic:57ugj782kvkwmSKg8uVe*.


**Configure Filebeat inputs**

Filebeat has several ways to collect logs. For this example, you’ll configure log collection manually.

In the *filebeat.inputs* section of *filebeat.yml*, set *enabled:* to *true*, and set *paths:* to the location of your web server log file. In this example, set the same directory where you saved *webserver.js*:

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
    - /path/to/logs/log.json
```

::::{tip}
You can specify a wildcard (***) character to indicate that all log files in the specified directory should be read. You can also use a wildcard to read logs from multiple directories. For example `/var/log/*/*.log`.
::::


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
    - /path/to/logs/log.json
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

The Filebeat data view is now available in Elasticsearch. To verify:

1. [Login to Kibana](../../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
2. Open the {{kib}} main menu and select **Management** > **{{kib}}** > **Data views**.
3. In the search bar, search for *filebeat*. You should get *filebeat-** in the search results.

**Optional: Use an API key to authenticate**

For additional security, instead of using basic authentication you can generate an Elasticsearch API key through the {{ecloud}} Console, and then configure Filebeat to use the new key to connect securely to the {{ech}} deployment.

1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
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

5. Add your API key information to the *Elasticsearch Output* section of *filebeat.yml*, just below *output.elasticsearch:*. Use the format `<id>:<api_key>`. If your results are as shown in this example, enter `2TBR42gBabmINotmvZjv:tV1dnfF-GHI59ykgv4N0U3`.
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



## Send the Node.js logs to Elasticsearch [ec-node-logs-send-ess]

It’s time to send some log data into {{es}}!

**Launch Filebeat and webserver.js**

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


Filebeat should now be running and monitoring the contents of *log.json*, which actually doesn’t exist yet. So, let’s create it. Open a new terminal instance and run the *webserver.js* Node.js script:

```sh
node webserver.js
```

Next, run the Node.js `webrequests.js` script to send random requests to the Node.js web server.

```sh
node webrequests.js
```

Let the script run for a few minutes and maybe brew up a quick coffee or tea ☕ . After that, make sure that the *log.json* file is generated as expected and is populated with several log entries.

**Verify the log entries in {{ech}}**

The next step is to confirm that the log data has successfully found it’s way into {{ech}}.

1. [Login to Kibana](../../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
2. Open the {{kib}} main menu and select **Management** > **{{kib}}** > **Data views**.
3. In the search bar, search for *filebeat*. You should get *filebeat-** in the search results.
4. Select *filebeat-**.

The filebeat data view shows a list of fields and their details.


## Create log visualizations in Kibana [ec-node-logs-view-kibana]

Now it’s time to create visualizations based off of the application log data.

1. Open the Kibana main menu and select **Dashboard**, then **Create dashboard**.
2. Select **Create visualization**. The [Lens](../../../explore-analyze/visualize/lens.md) visualization editor opens.
3. In the data view dropdown box, select **filebeat-***, if it isn’t already selected.
4. In the **CHART TYPE** dropdown box, select **Bar vertical stacked**, if it isn’t already selected.
5. Check that the [time filter](../../../explore-analyze/query-filter/filtering.md) is set to **Last 15 minutes**.
6. From the **Available fields** list, drag and drop the **@timestamp** field onto the visualization builder.
7. Drag and drop the **http.request.method** field onto the visualization builder.
8. A stacked bar chart now shows the relative frequency of each of the three request methods used in our example, measured over time.

    ![A screen capture of the Kibana "Bar vertical stacked" visualization with several bars. The X axis shows "Count of records" and the Y axis shows "@timestamp per 30 seconds". Each bar is divided into three HTTP request methods: GET](../../../images/cloud-ec-node-logs-methods.png "")

9. Select **Save and return** to add this visualization to your dashboard.

Let’s create a second visualization.

1. Select **Create visualization**.
2. Again, make sure that **CHART TYPE** is set to **Bar vertical stacked**.
3. From the **Available fields** list, drag and drop the **@timestamp** field onto the visualization builder.
4. Drag and drop the **http.request.headers.from** field onto the visualization builder.
5. In the chart settings area, under **Break down by**, select **Top values of http.request.headers.from** and set **Number of values** to *12*. In this example there are twelve different email addresses used in the HTTP *from* header, so this parameter sets all of them to appear in the chart legend.
6. Select **Refresh**. A stacked bar chart now shows the relative frequency of each of the HTTP *from* headers over time.

    ![A screen capture of the visualization builder](../../../images/cloud-ec-node-logs-content.png "")

7. Select **Save and return** to add this visualization to your dashboard.

And now for the final visualization.

1. Select **Create visualization**.
2. In the **CHART TYPE** dropdown box, select **Donut**.
3. From the list of available fields, drag and drop the **http.request.method** field onto the visualization builder. A donut chart appears.

    ![A screen capture of a donut chart divided into three sections](../../../images/cloud-ec-node-logs-donut.png "")

4. Select **Save and return** to add this visualization to your dashboard.
5. Select **Save** and add a title to save your new dashboard.

You now have a Kibana dashboard with three visualizations: a stacked bar chart showing the frequency of each HTTP request method over time, another stacked bar chart showing the frequency of various HTTP *from* headers over time, and a donut chart showing the relative frequency of each HTTP request method type.

You can add titles to the visualizations, resize and position them as you like, and then save your changes.

**View log data updates in real time**

1. Select **Refresh** on the Kibana dashboard. Since the application `webrequests.js` continues to run and send HTTP requests to the Node.js server, `webserver.js` continues to generate log data, and your Kibana visualizations update with that data with each page refresh.

    ![A screen capture of the completed Kibana dashboard](../../../images/cloud-ec-node-logs-final-dashboard.png "")

2. As your final step, remember to stop Filebeat, the Node.js web server, and the client. Enter *CTRL + C* in the terminal window for each application to stop them.

You now know how to monitor log files from a Node.js web application, deliver the log event data securely into an {{ech}} deployment, and then visualize the results in Kibana in real time. Consult the [Filebeat documentation](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-overview.md) to learn more about the ingestion and processing options available for your data. You can also explore our [documentation](../../../manage-data/ingest.md) to learn all about working in {{ech}}.

