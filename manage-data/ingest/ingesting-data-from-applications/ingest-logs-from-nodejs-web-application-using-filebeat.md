---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud/current/ec-getting-started-search-use-cases-node-logs.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-getting-started-search-use-cases-node-logs.html
applies_to:
  stack: 
    - ga 9.0
products:
  - id: cloud-hosted
  - id: cloud-enterprise
---

# Ingest logs from a Node.js web application using Filebeat

This guide demonstrates how to ingest logs from a Node.js web application and deliver them securely into an {{ech}} or {{ece}} deployment. You'll do that by using Filebeat and the Filestream input. You’ll run a simple Node.js server that emits ECS-formatted JSON logs, forward them securely to {{cloud}}, and explore them in Kibana.

While Node.js is used for this example, this approach to monitoring log output is applicable across many client types. Check the list of [available ECS logging plugins](ecs-logging://reference/intro.md#_get_started).

*Time required: 1.5 hours*


## Prerequisites [ec-node-logs-prerequisites]

To complete these steps you need the following applications installed on your system:

* [Node.js](https://nodejs.org/) (LTS or later) - you will set up a simple Node.js web server and client application. Check the Node.js download page for installation instructions.
* [Filebeat](https://www.elastic.co/downloads/beats/filebeat)

::::{tip}
For the three following packages, you can create a working directory to install the packages using the Node package manager (NPM). Then, you can run your Node.js webserver and client from the same directory so that it can use the packages. Alternatively, you can also install the Node packages globally by running the Node package install commands with the `-g` option. Refer to the NPM [package installation instructions](https://docs.npmjs.com/downloading-and-installing-packages-globally) for details.
::::


* [winston](https://www.npmjs.com/package/winston) - This is a popular logging package for Node.js. Create a new, local directory and run the following command to install winston in it:

    ```sh
    npm install winston
    ```

* The [Elastic Common Schema (ECS) formatter](ecs-logging-nodejs://reference/winston.md) for the Node.js winston logger - This plugin formats your Node.js logs into an ECS structured JSON format ideally suited for ingestion into Elasticsearch. To install the ECS winston logger, run the following command in your working directory so that the package is installed in the same location as the winston package:

    ```sh
    npm install @elastic/ecs-winston-format
    ```

* [Got](https://www.npmjs.com/package/got) - Got is a "Human-friendly and powerful HTTP request library for Node.js." - This plugin can be used to query the sample web server used in the tutorial. To install the Got package, run the following command in your working directory:

    ```sh
    npm install got
    ```


## Before you begin

Make sure you have access to an [Elastic Cloud deployment](../../../deploy-manage/deploy/elastic-cloud/create-an-elastic-cloud-hosted-deployment.md). You’ll need the **Cloud ID** and credentials to connect Filebeat later.

To find your **Cloud ID**, open the Elastic Cloud console, locate your deployment, and select **Manage**. On the **Deployment overview** page, copy the **Cloud ID** value displayed. You’ll use it in your `filebeat.yml` configuration.

To connect to, stream data to, and issue queries, you need to think about authentication. Two authentication mechanisms are supported, *API key* and *basic authentication*. Here, to get you started quickly, we’ll show you how to use basic authentication, but you can also generate API keys as shown later on. API keys are safer and preferred for production environments.


## Create a Node.js web application with ECS-formatted logs [ec-node-logs-create-server-script]

Next, create a basic Node.js script that runs a web server and logs HTTP requests.

:::::{stepper}

::::{step} Install dependencies

```bash
npm init -y
npm install winston @elastic/ecs-winston-format got
```

::::

::::{step} Create `webserver.js`

```javascript
const http = require('http')
const winston = require('winston')
const ecsFormat = require('@elastic/ecs-winston-format')

const logger = winston.createLogger({
  level: 'info',
  format: ecsFormat({ convertReqRes: true }),
  transports: [
    new winston.transports.File({
      filename: 'logs/log.json',
      level: 'info'
    })
  ]
})

const server = http.createServer((req, res) => {
  res.setHeader('Foo', 'Bar')
  res.end('ok')
  logger.info('handled request', { req, res })
})

server.listen(3000, () => {
  logger.info('listening at http://localhost:3000')
})
```

::::

::::{step} Run the server

```bash
node webserver.js
```

::::

::::{step} Test the application

With the script running, open a web browser to `http://localhost:3000` and there should be a simple `ok` message.

::::

:::::

In the directory where you created `webserver.js`, you should now find a newly created `log.json` file. Open the file and check the contents. There should be one log entry indicating that Node.js is listening on the localhost port, and another entry for the HTTP request from when you opened `localhost` in your browser.

Leave `webserver.js` running for now and we’ll send it some HTTP requests.


## Generate sample traffic [ec-node-logs-create-request-script]

In this step, you’ll create a Node.js application that sends HTTP requests to your web server.

:::::{stepper}

::::{step} Create the traffic generator

Create `webrequests.js` to send random HTTP requests:

```javascript
const got = require('got')

const addresses = ['aardvark@zoo', 'emu@zoo', 'otter@zoo']
const methods = ['get', 'post', 'put']

async function sleep(ms) {
  return new Promise(r => setTimeout(r, ms))
}

;(async () => {
  while (true) {
    const method = methods[Math.floor(Math.random() * methods.length)]
    const from = addresses[Math.floor(Math.random() * addresses.length)]
    try {
      await got[method]('http://localhost:3000', { headers: { from } })
    } catch {}
    await sleep(Math.random() * 5000 + 2000)
  }
})()
```

This Node.js app generates HTTP requests with a random method of type `GET`, `POST`, or `PUT`, and a random `from` request header using various pretend email addresses. The requests are sent at random intervals between 1 and 10 seconds.

The [Got package](https://www.npmjs.com/package/got) is used to send the requests, and they are directed to your web server at `http://localhost:3000`. To learn about sending custom headers such as the `from` field used in this example, check [headers](https://github.com/sindresorhus/got/blob/0fb6ec60d299fd9b48966608a4c3f201746d821c/documentation/2-options.md#headers) in the Got documentation.

::::

::::{step} Run the traffic generator

In a new terminal window, give the Node.js script a trial run:

```bash
node webrequests.js
```

::::

::::{step} Verify log generation

After the script has run for about 30 seconds, enter *CTRL + C* to stop it. Have a look at your Node.js `logs/log.json` file. It should contain some entries like this one:

```json
{"@timestamp":"2021-09-09T18:42:20.799Z","log.level":"info","message":"handled request","ecs":{"version":"1.6.0"},"http":{"version":"1.1","request":{"method":"POST","headers":{"user-agent":"got (https://github.com/sindresorhus/got)","from":"octopus@the.zoo","accept":"application/json","accept-encoding":"gzip, deflate, br","host":"localhost:3000","connection":"close","content-length":"0"},"body":{"bytes":0}},"response":{"status_code":200,"headers":{"foo":"Bar"}}},"url":{"path":"/","full":"http://localhost:3000/"},"client":{"address":"::ffff:127.0.0.1","ip":"::ffff:127.0.0.1","port":49930},"user_agent":{"original":"got (https://github.com/sindresorhus/got)"}}
```

Each log entry contains details of the HTTP request. In particular, in this example you can find the timestamp of the request, a request method of type `PUT`, and a request `from` header with the email address `octopus@the.zoo`. Your example will likely be a bit different since the request type and the email address are generated randomly.

Having your logs written in a JSON format with ECS fields allows for easy parsing and analysis, and for standardization with other applications. A standard, easily parsible format becomes increasingly important as the volume and type of data captured in your logs expands over time.

::::

::::{step} Clean up for next section

After confirming that both `webserver.js` and `webrequests.js` run as expected, enter *CTRL + C* to stop the Node.js script, and also delete `log.json`.

::::

:::::


## Get Filebeat

To collect and forward your Node.js application logs to Elastic Cloud, you'll need to set up Filebeat as your log shipper.

:::::{stepper}

::::{step} Download and install Filebeat

[Download Filebeat](https://www.elastic.co/downloads/beats/filebeat) and unpack it on the local server from which you want to collect data.

::::

::::{step} Configure Filebeat to access {{ech}} or {{ece}}

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

1. Uncomment the `cloud.id` line and add the deployment's Cloud ID. You can include or omit the *<deploymentname>:* prefix at the beginning of the Cloud ID. Both versions work fine. To find your Cloud ID, open the [Elastic Cloud console](https://cloud.elastic.co), locate your deployment, and select **Manage**. On the **Deployment overview** page, copy the **Cloud ID** value displayed.”
2. Uncomment the `cloud.auth` line and add the username and password for your deployment that you recorded when you created your deployment. The format is *<username>:<password>*, for example *elastic:57ugj782kvkwmSKg8uVe*.

::::

:::::


## Set up Filebeat [ec-node-logs-filebeat]

Filebeat offers a straightforward, easy to configure way to monitor your Node.js log files and port the log data into your deployment.

:::::{stepper}

::::{step} Configure Elastic Cloud credentials

Open the `filebeat.yml` file in the Filebeat installation directory and configure your Elastic Cloud credentials:

```yaml
cloud.id: "my-deployment:xxxxxxxxxxxx"
cloud.auth: "elastic:your_password"
```

::::

::::{step} Define a Filestream input

Configure Filebeat to monitor your Node.js log files:

```yaml
filebeat.inputs:
- type: filestream
  id: nodejs-logs
  enabled: true
  paths:
    - /full/path/to/logs/log.json
  parsers:
    - json:
        keys_under_root: true
        overwrite_keys: true
        add_error_key: true
        expand_keys: true
```

:::{important}
The old `log` input is deprecated and no longer supported. Use `filestream` instead — it provides better file state tracking and performance. Refer to [Filestream input reference](beats://reference/filebeat/filebeat-input-filestream.md) for more information.
:::

::::

::::{step} Optional: Configure API key authentication

You can replace `cloud.auth` with an API key for enhanced security:

```yaml
output.elasticsearch:
  api_key: "id:api_key"
```

::::

:::::


## Start Filebeat

Filebeat comes with predefined assets for parsing, indexing, and visualizing your data. Follow these steps to start Filebeat and begin shipping your Node.js logs to Elasticsearch.

:::::{stepper}

::::{step} Set up Filebeat assets

Load the predefined assets by running the following commands from the Filebeat installation directory:

```bash
./filebeat setup -e
./filebeat -e -c filebeat.yml
```

::::{important}
Depending on variables including the installation location, environment, and local permissions, you might need to [change the ownership](beats://reference/libbeat/config-file-permissions.md) of filebeat.yml. You can also try running the command as *root*: *sudo ./filebeat setup -e* or you can disable strict permission checks by running the command with the `--strict.perms=false` option.
::::

::::

::::{step} Handle permission issues (if needed)

If you encounter permissions errors, try running Filebeat with elevated permissions:

```bash
sudo ./filebeat -e -c filebeat.yml --strict.perms=false
```

::::

::::{step} Verify data ingestion

Filebeat should begin tailing `logs/log.json` and shipping events to Elasticsearch. To verify the setup:

1. [Login to Kibana](../../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
2. Open the {{kib}} main menu and select **Management** > **{{kib}}** > **Data views**.
3. In the search bar, search for *filebeat*. You should get _filebeat-*_ in the search results.

To verify ingestion is working, check the Filebeat logs for messages like:

```
Successfully published events
```
::::

:::::


## Optional: Use an API key to authenticate

For additional security, instead of using basic authentication you can generate an Elasticsearch API key through the {{ech}} or {{ece}} console, and then configure Filebeat to use the new key to connect securely to your deployment.

:::::{stepper}

::::{step} Access the console

For {{ech}}, log into [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body), or for {{ece}}, log into the admin console.

::::

::::{step} Navigate to Dev Tools

Select the deployment name and go to **☰** > **Management** > **Dev Tools**.

::::

::::{step} Generate the API key

Enter the following request:

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

::::

::::{step} Execute and copy the API key

Click **▶**. The output should be similar to the following:

```json
{
  "api_key": "tV1dnfF-GHI59ykgv4N0U3",
  "id": "2TBR42gBabmINotmvZjv",
  "name": "filebeat-api-key"
}
```

::::

::::{step} Configure Filebeat to use the API key

Add your API key information to the *Elasticsearch Output* section of *filebeat.yml*, just below *output.elasticsearch:*. Use the format `<id>:<api_key>`. If your results are as shown in this example, enter `2TBR42gBabmINotmvZjv:tV1dnfF-GHI59ykgv4N0U3`.

Add a pound (`#`) sign to comment out the *cloud.auth: elastic:<password>* line, since Filebeat will use the API key instead of the deployment username and password to authenticate.

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

::::

:::::



## Send the Node.js logs to Elasticsearch [ec-node-logs-send-ess]

It's time to send some log data into {{es}}! Follow these steps to start the data pipeline and verify that your logs are successfully ingested.

:::::{stepper}

::::{step} Launch Filebeat

Launch Filebeat by running the following from the Filebeat installation directory:

```bash
./filebeat -e -c filebeat.yml
```

In this command:

* The *-e* flag sends output to the standard error instead of the configured log output.
* The *-c* flag specifies the path to the Filebeat config file.

::::{note}
Just in case the command doesn't work as expected, check the [Filebeat quick start](beats://reference/filebeat/filebeat-installation-configuration.md#installation) for the detailed command syntax for your operating system. You can also try running the command as *root*: *sudo ./filebeat -e -c filebeat.yml*.
::::

::::

::::{step} Start the Node.js web server

Filebeat should now be running and monitoring the contents of *log.json*, which actually doesn't exist yet. So, let's create it. Open a new terminal instance and run the *webserver.js* Node.js script:

```bash
node webserver.js
```

::::

::::{step} Generate log traffic

Run the Node.js `webrequests.js` script to send random requests to the Node.js web server:

```bash
node webrequests.js
```

Let the script run for a few minutes and maybe brew up a quick coffee or tea ☕ . After that, make sure that the *log.json* file is generated as expected and is populated with several log entries.

::::

::::{step} Verify log ingestion in Kibana

The next step is to confirm that the log data has successfully found its way into {{ech}} or {{ece}}:

1. [Login to Kibana](../../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
2. Open the {{kib}} main menu and select **Management** > **{{kib}}** > **Data views**.
3. In the search bar, search for *filebeat*. You should get _filebeat-*_ in the search results.
4. Select _filebeat-*_.

The filebeat data view shows a list of fields and their details.

::::

:::::


## Create log visualizations in Kibana [ec-node-logs-view-kibana]

Now it's time to explore and visualize your ingested log data in Kibana to gain insights from your Node.js application.

:::::{stepper}

::::{step} View data in Discover

Log into Kibana and explore your data:

1. Go to **Analytics** → **Discover**.
2. Select the default data view (it should include `filebeat-*`).
3. Filter by fields such as `http.request.method` or `http.request.headers.from`.

You should see structured log entries generated by the Node.js app.

::::

::::{step} Create visualizations

You can now visualize your log data using Lens:

1. Go to **Analytics** → **Dashboard** → **Create dashboard**.
2. Click **Create visualization**.
3. Choose **Lens** and select the `filebeat-*` data view.
4. Drag `@timestamp` to the horizontal axis.
5. Drag `http.request.method` to the vertical axis.
6. Select **Bar** → **Stacked vertical**.
7. Repeat for other fields such as `http.request.headers.from` or create a **Donut** chart showing relative request types.
8. Save your dashboard and watch events update in real time.

::::{tip}
If logs stop appearing, verify that the log file exceeds 1 KB — the Filestream input only fingerprints files once they reach that size. Refer to [File identity and fingerprinting](beats://reference/filebeat/how-filebeat-works.md#_file_identity_and_fingerprinting) for more details.
::::

::::

::::{step} Clean up

Stop all running processes by pressing `Ctrl + C` in each terminal window.

You can delete temporary files such as `log.json` and the `node_modules` directory when finished.

::::

:::::


You now know how to monitor log files from a Node.js web application, deliver the log event data securely into an {{ech}} or {{ece}} deployment, and then visualize the results in Kibana in real time. Consult the [Filebeat documentation](beats://reference/filebeat/index.md) to learn more about the ingestion and processing options available for your data. You can also explore our [documentation](../../../manage-data/ingest.md) to learn all about ingesting data.