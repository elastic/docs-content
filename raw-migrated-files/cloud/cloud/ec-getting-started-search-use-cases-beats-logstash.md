# Ingest data from Beats to {{ech}} with {{ls}} as a proxy [ec-getting-started-search-use-cases-beats-logstash]

This guide explains how to ingest data from Filebeat and Metricbeat to {{ls}} as an intermediary, and then send that data to {{ech}}. Using {{ls}} as a proxy limits your Elastic stack traffic through a single, external-facing firewall exception or rule. Consider the following features of this type of setup:

* You can send multiple instances of Beats data through your local network’s demilitarized zone (DMZ) to {{ls}}. {{ls}} then acts as a proxy through your firewall to send the Beats data to {{ech}}, as shown in the following diagram:

    ![A diagram showing data from multiple Beats into Logstash](../../../images/cloud-ec-logstash-beats-dataflow.png "")

* This proxying reduces the firewall exceptions or rules necessary for Beats to communicate with {{ech}}. It’s common to have many Beats dispersed across a network, each installed close to the data that it monitors, and each Beat individually communicating with an {{ech}} deployment. Multiple Beats support multiple servers. Rather than configure each Beat to send its data directly to {{ech}}, you can use {{ls}} to proxy this traffic through one firewall exception or rule.
* This setup is not suitable in simple scenarios when there is only one or a couple of Beats in use. {{ls}} makes the most sense for proxying when there are many Beats.

The configuration in this example makes use of the System module, available for both Filebeat and Metricbeat. Filebeat’s System sends server system log details (that is, login success/failures, sudo *superuser do* command usage, and other key usage details). Metricbeat’s System module sends memory, CPU, disk, and other server usage metrics.

In the following sections you are going to learn how to:

1. [Get {{ech}}](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-beats-to-elasticsearch-service-with-logstash-as-proxy.md#ec-beats-logstash-trial)
2. [Connect securely](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-beats-to-elasticsearch-service-with-logstash-as-proxy.md#ec-beats-logstash-connect-securely)
3. [Set up {{ls}}](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-beats-to-elasticsearch-service-with-logstash-as-proxy.md#ec-beats-logstash-logstash)
4. [Set up Metricbeat](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-beats-to-elasticsearch-service-with-logstash-as-proxy.md#ec-beats-logstash-metricbeat)
5. [Configure Metricbeat to send data to {{ls}}](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-beats-to-elasticsearch-service-with-logstash-as-proxy.md#ec-beats-logstash-metricbeat-send)
6. [Set up Filebeat](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-beats-to-elasticsearch-service-with-logstash-as-proxy.md#ec-beats-logstash-filebeat)
7. [Configure {{ls}} to listen for Beats](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-beats-to-elasticsearch-service-with-logstash-as-proxy.md#ec-beats-logstash-listen)
8. [Output {{ls}} data to stdout](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-beats-to-elasticsearch-service-with-logstash-as-proxy.md#ec-beats-logstash-stdout)
9. [Output {{ls}} data to {{es}}](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-beats-to-elasticsearch-service-with-logstash-as-proxy.md#ec-beats-logstash-elasticsearch)
10. [View data in Kibana](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-beats-to-elasticsearch-service-with-logstash-as-proxy.md#ec-beats-logstash-view-kibana)

*Time required: 1 hour*


## Get {{ech}} [ec-beats-logstash-trial]

1. [Get a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
2. Log into [Elastic Cloud](https://cloud.elastic.co?page=docs&placement=docs-body).
3. Select **Create deployment**.
4. Give your deployment a name. You can leave all other settings at their default values.
5. Select **Create deployment** and save your Elastic deployment credentials. You need these credentials later on.
6. When the deployment is ready, click **Continue** and a page of **Setup guides** is displayed. To continue to the deployment homepage click **I’d like to do something else**.

Prefer not to subscribe to yet another service? You can also get {{ech}} through [AWS, Azure, and GCP marketplaces](../../../deploy-manage/deploy/elastic-cloud/subscribe-from-marketplace.md).


## Connect securely [ec-beats-logstash-connect-securely]

When connecting to {{ech}} you can use a Cloud ID to specify the connection details. You must pass the Cloud ID that you can find in the cloud console.  Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.

To connect to, stream data to, and issue queries with {{ech}}, you need to think about authentication. Two authentication mechanisms are supported, *API key* and *basic authentication*. Here, to get you started quickly, we’ll show you how to use basic authentication, but you can also generate API keys as shown later on. API keys are safer and preferred for production environments.


## Set up {{ls}} [ec-beats-logstash-logstash]

[Download](https://www.elastic.co/downloads/logstash) and unpack {{ls}} on the local machine that hosts Beats or another machine granted access to the Beats machines.


## Set up Metricbeat [ec-beats-logstash-metricbeat]

Now that {{ls}} is downloaded and your {{ech}} deployment is set up, you can configure Metricbeat to send operational data to {{ls}}.

Install Metricbeat as close as possible to the service that you want to monitor. For example, if you have four servers with MySQL running, we recommend that you run Metricbeat on each server. This allows Metricbeat to access your service from *localhost*. This setup does not cause any additional network traffic and enables Metricbeat to collect metrics even in the event of network problems. Metrics from multiple Metricbeat instances are combined on the {{ls}} server.

If you have multiple servers with metrics data, repeat the following steps to configure Metricbeat on each server.

**Download Metricbeat**

[Download Metricbeat](https://www.elastic.co/downloads/beats/metricbeat) and unpack it on the local server from which you want to collect data.

**About Metricbeat modules**

Metricbeat has [many modules](asciidocalypse://docs/beats/docs/reference/metricbeat/metricbeat-modules.md) available that collect common metrics. You can [configure additional modules](asciidocalypse://docs/beats/docs/reference/metricbeat/configuration-metricbeat.md) as needed. For this example we’re using Metricbeat’s default configuration, which has the [System module](asciidocalypse://docs/beats/docs/reference/metricbeat/metricbeat-module-system.md) enabled. The System module allows you to monitor servers with the default set of metrics: *cpu*, *load*, *memory*, *network*, *process*, *process_summary*, *socket_summary*, *filesystem*, *fsstat*, and *uptime*.

**Load the Metricbeat Kibana dashboards**

Metricbeat comes packaged with example dashboards, visualizations, and searches for visualizing Metricbeat data in Kibana. Before you can use the dashboards, you need to create the data view (formerly *index pattern*) *metricbeat-**, and load the dashboards into Kibana. This needs to be done from a local Beats machine that has access to the {{ech}} deployment.

::::{note}
Beginning with Elastic Stack version 8.0, Kibana *index patterns* have been renamed to *data views*. To learn more, check the Kibana [What’s new in 8.0](https://www.elastic.co/guide/en/kibana/8.0/whats-new.html#index-pattern-rename) page.
::::


1. Open a command line instance and then go to *<localpath>/metricbeat-<version>/*
2. Run the following command:

```txt
sudo ./metricbeat setup \
  -E cloud.id=<cloudID> \ <1>
  -E cloud.auth=<username>:<password> <2>
```

1. Specify the Cloud ID of your {{ech}} deployment. You can include or omit the `<Deploymentname>:` prefix at the beginning of the Cloud ID. Both versions work fine. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.
2. Specify the username and password provided to you when creating the deployment. Make sure to keep the colon between *<username>* and *<password>*.::::{important}
Depending on variables including the installation location, environment and local permissions, you might need to [change the ownership](asciidocalypse://docs/beats/docs/reference/libbeat/config-file-permissions.md) of the metricbeat.yml.

You might encounter similar permissions hurdles as you work through multiple sections of this document. These permission requirements are there for a good reason, a security safeguard to prevent unauthorized access and modification of key Elastic files.

If this isn’t a production environment and you want a fast-pass with less permissions hassles, then you can disable strict permission checks from the command line by using `--strict.perms=false` when executing Beats (for example, `./metricbeat --strict.perms=false`).

Depending on your system, you may also find that some commands need to be run as root, by prefixing `sudo` to the command.

::::




Your results should be similar to the following:

```txt
Index setup finished.
Loading dashboards (Kibana must be running and reachable)
Loaded dashboards
```


## Configure Metricbeat to send data to {{ls}} [ec-beats-logstash-metricbeat-send]

1. In *<localpath>/metricbeat-<version>/* (where *<localpath>* is the directory where Metricbeat is installed), open the *metricbeat.yml* configuration file for editing.
2. Scroll down to the *Elasticsearch Output* section. Place a comment pound sign (*#*) in front of *output.elasticsearch* and {{es}} *hosts*.
3. Scroll down to the *Logstash Output* section. Remove the comment pound sign (*#*) from in front of *output.logstash* and *hosts*, as follows:

```txt
# ---------------- Logstash Output -----------------
output.logstash:
  # The Logstash hosts
  hosts: ["localhost:5044"] <1>
```

1. Replace `localhost` and the port number with the hostname and port number where Logstash is listening.



## Set up Filebeat [ec-beats-logstash-filebeat]

The next step is to configure Filebeat to send operational data to Logstash. As with Metricbeat, install Filebeat as close as possible to the service that you want to monitor.

**Download Filebeat**

[Download Filebeat](https://www.elastic.co/downloads/beats/filebeat) and unpack it on the local server from which you want to collect data.

**Enable the Filebeat system module**

Filebeat has [many modules](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-modules.md) available that collect common log types. You can [configure additional modules](asciidocalypse://docs/beats/docs/reference/filebeat/configuration-filebeat-modules.md) as needed. For this example we’re using Filebeat’s [System module](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-module-system.md). This module reads in the various system log files (with information including login successes or failures, sudo command usage, and other key usage details) based on the detected operating system. For this example, a Linux-based OS is used and Filebeat ingests logs from the */var/log/* folder. It’s important to verify that Filebeat is given permission to access your logs folder through standard file and folder permissions.

1. Go to *<localpath>/filebeat-<version>/modules.d/* where *<localpath>* is the directory where Filebeat is installed.
2. Filebeat requires at least one fileset to be enabled. In file *<localpath>/filebeat-<version>/modules.d/system.yml.disabled*, under both `syslog` and `auth` set `enabled` to `true`:

```txt
- module: system
  # Syslog
  syslog:
    enabled: true

  # Authorization logs
  auth:
    enabled: true
```

From the *<localpath>/filebeat-<version>* directory, run the `filebeat modules` command as shown:

```txt
./filebeat modules enable system
```

The system module is now enabled in Filebeat and it will be used the next time Filebeat starts.

**Load the Filebeat Kibana dashboards**

Filebeat comes packaged with example Kibana dashboards, visualizations, and searches for visualizing Filebeat data in Kibana. Before you can use the dashboards, you need to create the data view *filebeat-**, and load the dashboards into Kibana. This needs to be done from a Beats machine that has access to the Internet.

1. Open a command line instance and then go to *<localpath>/filebeat-<version>/*
2. Run the following command:

```txt
sudo ./filebeat setup \
  -E cloud.id=<cloudID> \ <1>
  -E cloud.auth=<username>:<password> <2>
```

1. Specify the Cloud ID of your {{ech}} deployment. You can include or omit the `<Deploymentname>:` prefix at the beginning of the Cloud ID. Both versions work fine. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.
2. Specify the username and password provided to you when creating the deployment. Make sure to keep the colon between *<username>* and *<password>*.::::{important}
Depending on variables including the installation location, environment, and local permissions, you might need to [change the ownership](asciidocalypse://docs/beats/docs/reference/libbeat/config-file-permissions.md) of the filebeat.yml.
::::




Your results should be similar to the following:

```txt
Index setup finished.
Loading dashboards (Kibana must be running and reachable)
Loaded dashboards
Setting up ML using setup --machine-learning is going to be removed in 8.0.0. Please use the ML app instead.
See more: /explore-analyze/machine-learning.md
Loaded machine learning job configurations
Loaded Ingest pipelines
```

1. Exit the CLI.

The data views for *filebeat-** and *metricbeat-** are now available in {{es}}. To verify:

1. [Login to Kibana](../../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
2. Open the Kibana main menu and select **Management** and go to **Kibana** > **Data views**.
3. In the search bar, search for *data views*.
4. In the search results, choose *Kibana / Data Views Management*.

**Finish configuring Filebeat**

1. In *<localpath>/filebeat-<version>/* (where *<localpath>* is the directory where Filebeat is installed), open the *filebeat.yml* configuration file for editing.
2. Scroll down to the *Outputs* section. Place a comment pound sign (*#*) in front of *output.elasticsearch* and {{es}} *hosts*.
3. Scroll down to the *Logstash Output* section. Remove the comment pound sign (*#*) from in front of *output.logstash* and *hosts* as follows:

```txt
# ---------------- Logstash Output -----------------
output.logstash:
  # The Logstash hosts
  hosts: ["localhost:5044"] <1>
```

1. Replace `localhost` and the port number with the hostname and port number where Logstash is listening.



## Configure {{ls}} to listen for Beats [ec-beats-logstash-listen]

Now the Filebeat and Metricbeat are set up, let’s configure a {{ls}} pipeline to input data from Beats and send results to the standard output. This enables you to verify the data output before sending it for indexing in {{es}}.

1. In *<localpath>/logstash-<version>/*, create a new text file named *beats.conf*.
2. Copy and paste the following code into the new text file. This code creates a {{ls}} pipeline that listens for connections from Beats on port 5044 and writes to standard out (typically to your terminal) with formatting provided by the {{ls}} rubydebug output plugin.

    ```txt
    input {
      beats{port => 5044} <1>
    }
    output {
      stdout{codec => rubydebug} <2>
    }
    ```

    1. {{ls}} listens for Beats input on the default port of 5044. Only one line is needed to do this. {{ls}} can handle input from many Beats of the same and also of varying types (Metricbeat, Filebeat, and others).
    2. This sends output to the standard output, which displays through your command line interface. This plugin enables you to verify the data before you send it to {{es}}, in a later step.

3. Save the new *beats.conf* file in your Logstash folder. To learn more about the file format and options, check [{{ls}} Configuration Examples](asciidocalypse://docs/logstash/docs/reference/config-examples.md).


## Output {{ls}} data to stdout [ec-beats-logstash-stdout]

Now, let’s try out the {{ls}} pipeline with the Metricbeats and Filebeats configurations from the prior steps. Each Beat sends data into a {{ls}} pipeline, and the results display on the standard output where you can verify that everything looks correct.

**Test Metricbeat to stdout**

1. Open a command line interface instance. Go to *<localpath>/logstash-<version>/*, where <localpath> is the directory where {{ls}} is installed, and start {{ls}} by running the following command:

    ```txt
    bin/logstash -f beats.conf
    ```

2. Open a second command line interface instance. Go to *<localpath>/metricbeat-<version>/*, where <localpath> is the directory where Metricbeat is installed, and start Metricbeat by running the following command:

    ```txt
    ./metricbeat -c metricbeat.yml
    ```

3. Switch back to your first command line interface instance with {{ls}}. Now, Metricbeat events are input into {{ls}} and the output data is directed to the standard output. Your results should be similar to the following:

    ```txt
    "tags" => [
              [0] "beats_input_raw_event"
    ],
    "agent" => {
              "type" => "metricbeat",
              "name" => "john-VirtualBox",
           "version" => "8.13.1",
      "ephemeral_id" => "1e69064c-d49f-4ec0-8414-9ab79b6f27a4",
                "id" => "1b6c39e8-025f-4310-bcf1-818930a411d4",
          "hostname" => "john-VirtualBox"
    },
    "service" => {
              "type" => "system"
    },
    "event" => {
          "duration" => 39833,
            "module" => "system",
           "dataset" => "system.cpu"
    },
        "@timestamp" => 2021-04-21T17:06:05.231Z,
         "metricset" => {
              "name" => "cpu",
            "period" => 10000
    },
    "@version" => "1","host" => {
                "id" => "939972095cf1459c8b22cc608eff85da",
                "ip" => [
                  [0] "10.0.2.15",
                  [1] "fe80::3700:763c:4ba3:e48c"
    ],
    "name" => "john-VirtualBox","mac" => [
                  [0] "08:00:27:a3:c7:a9"
    ],
    "os" => {
              "type" => "linux",
    ```

4. Switch back to the Metricbeat command line instance. Enter *CTRL + C* to shut down Metricbeat, and then exit the CLI.
5. Switch back to the {{ls}} command line instance. Enter *CTRL + C* to shut down {{ls}}, and then exit the CLI.

**Test Filebeat to stdout**

1. Open a command line interface instance. Go to *<localpath>/logstash-<version>/*, where <localpath> is the directory where {{ls}} is installed, and start {{ls}} by running the following command:

    ```txt
    bin/logstash -f beats.conf
    ```

2. Open a second command line interface instance. Go to *<localpath>/filebeat-<version>/*, where <localpath> is the directory where Filebeat is installed, and start Filebeat by running the following command:

    ```txt
    ./filebeat -c filebeat.yml
    ```

3. Switch back to your first command line interface instance with {{ls}}. Now, Filebeat events are input into {{ls}} and the output data is directed to the standard output. Your results should be similar to the following:

    ```txt
    {
           "service" => {
            "type" => "system"
        },
             "event" => {
            "timezone" => "-04:00",
             "dataset" => "system.syslog",
              "module" => "system"
        },
           "fileset" => {
            "name" => "syslog"
        },
             "agent" => {
                      "id" => "113dc127-21fa-4ebb-ab86-8a151d6a23a6",
                    "type" => "filebeat",
                 "version" => "8.13.1",
                "hostname" => "john-VirtualBox",
            "ephemeral_id" => "1058ad74-8494-4a5e-9f48-ad7c5b9da915",
                    "name" => "john-VirtualBox"
        },
        "@timestamp" => 2021-04-28T15:33:41.727Z,
             "input" => {
            "type" => "log"
        },
               "ecs" => {
            "version" => "1.8.0"
        },
          "@version" => "1",
               "log" => {
            "offset" => 73281,
              "file" => {
                "path" => "/var/log/syslog"
            }
        },
    ```

4. Review the {{ls}} output results to make sure your data looks correct. Enter *CTRL + C* to shut down {{ls}}.
5. Switch back to the Filebeats CLI. Enter *CTRL + C* to shut down Filebeat.


## Output {{ls}} data to {{es}} [ec-beats-logstash-elasticsearch]

In this section, you configure {{ls}} to send the Metricbeat and Filebeat data to {{es}}. You modify the *beats.conf* created earlier, and specify the output credentials needed for our {{ech}} deployment. Then, you start {{ls}} to send the Beats data into {{es}}.

1. In your *<localpath>/logstash-<version>/* folder, open *beats.conf* for editing.
2. Replace the *output {}* section of the JSON with the following code:

    ```txt
    output {
      elasticsearch {
        index => "%{[@metadata][beat]}-%{[@metadata][version]}"
        ilm_enabled => true
        cloud_id => "<DeploymentName>:<ID>" <1>
        cloud_auth => "elastic:<Password>" <2>
        ssl => true
        # api_key => "<myAPIid:myAPIkey>"
      }
    }
    ```

    1. Use the Cloud ID of your {{ech}} deployment. You can include or omit the `<DeploymentName>:` prefix at the beginning of the Cloud ID. Both versions work fine. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.
    2. the default usename is `elastic`.  It is not recommended to use the `elastic` account for ingesting data as this is a superuser.  We recommend using a user with reduced permissions, or an API Key with permissions specific to the indices or data streams that will be written to.  Check the [Grant access to secured resources](asciidocalypse://docs/beats/docs/reference/filebeat/feature-roles.md) for information on the writer role and API Keys. Use the password provided when you created the deployment if using the `elastic` user, or the password used when creating a new ingest user with the roles specified in the [Grant access to secured resources](asciidocalypse://docs/beats/docs/reference/filebeat/feature-roles.md) documentation.


    Following are some additional details about the configuration file settings:

    * *index*: We specify the name of the {{es}} index with which to associate the Beats output.

        * *%{[@metadata][beat]}* sets the first part of the index name to the value of the Beat metadata field.
        * *%{[@metadata][version]}* sets the second part of the index name to the Beat version.

            If you use Metricbeat version 8.13.1, the index created in {{es}} is named *metricbeat-8.13.1*. Similarly, using the 8.13.1 version of Filebeat, the {{es}} index is named *filebeat-8.13.1*.

    * *cloud_id*: This is the ID that uniquely identifies your {{ech}} deployment.
    * *ssl*: This should be set to `true` so that Secure Socket Layer (SSL) certificates are used for secure communication between {{ls}} and your {{ech}} deployment.
    * *ilm_enabled*: Enables and disables {{ech}} [index lifecycle management](../../../manage-data/lifecycle/index-lifecycle-management.md).
    * *api_key*: If you choose to use an API key to authenticate (as discussed in the next step), you can provide it here.

3. **Optional**: For additional security, you can generate an {{es}} API key through the {{ecloud}} Console and configure {{ls}} to use the new key to connect securely to {{ecloud}}.

    1. Log in to the [{{ecloud}} Console](https://cloud.elastic.co?page=docs&placement=docs-body).
    2. Select the deployment and go to **☰** > **Management** > **Dev Tools**.
    3. Enter the following:

        ```json
        POST /_security/api_key
        {
         "name": "logstash-apikey",
         "role_descriptors": {
           "logstash_read_write": {
             "cluster": ["manage_index_templates", "monitor"],
             "index": [
               {
                 "names": ["logstash-*","metricbeat-*","filebeat-*"],
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
          "api_key": "aB1cdeF-GJI23jble4NOH4",
          "id": "2GBe63fBcxgJAetmgZeh",
          "name": "logstash_api_key"
        }
        ```

    5. Enter your new `api_key` value into the {{ls}} `beats.conf` file, in the format `<id>:<api_key>`. If your results were as shown in this example, you would enter `2GBe63fBcxgJAetmgZeh:aB1cdeF-GJI23jble4NOH4`. Remember to remove the pound (`#`) sign to uncomment the line, and comment out the `username` and `password` lines:

        ```txt
        output {
          elasticsearch {
            index => "%{[@metadata][beat]}-%{[@metadata][version]}"
            cloud_id => "<myDeployment>"
            ssl => true
            ilm_enabled => true
            api_key => "2GBe63fBcxgJAetmgZeh:aB1cdeF-GJI23jble4NOH4"
            # user => "<Username>"
            # password => "<Password>"
          }
        }
        ```

4. Open a command line interface instance, go to your {{ls}} installation path, and start {{ls}}:

    ```txt
    bin/logstash -f beats.conf
    ```

5. Open a second command line interface instance, go to your Metricbeat installation path, and start Metricbeat:

    ```txt
    ./metricbeat -c metricbeat.yml
    ```

6. Open a third command line interface instance, go to your Filebeat installation path, and start Filebeat:

    ```txt
    ./filebeat -c filebeat.yml
    ```

7. {{ls}} now outputs the Filebeat and Metricbeat data to your {{ech}} instance.

::::{note}
In this guide, you manually launch each of the Elastic stack applications through the command line interface. In production, you may prefer to configure {{ls}}, Metricbeat, and Filebeat to run as System Services. Check the following pages for the steps to configure each application to run as a service:

* [Running {{ls}} as a service on Debian or RPM](asciidocalypse://docs/logstash/docs/reference/running-logstash.md)
* [Metricbeat and systemd](asciidocalypse://docs/beats/docs/reference/metricbeat/running-with-systemd.md)
* [Start filebeat](asciidocalypse://docs/beats/docs/reference/filebeat/filebeat-starting.md)

::::



## View data in Kibana [ec-beats-logstash-view-kibana]

In this section, you log into {{ech}}, open Kibana, and view the Kibana dashboards populated with our Metricbeat and Filebeat data.

**View the Metricbeat dashboard**

1. [Login to Kibana](../../../deploy-manage/deploy/elastic-cloud/access-kibana.md).
2. Open the Kibana main menu and select **Analytics**, then **Dashboard**.
3. In the search box, search for *metricbeat system*. The search results show several dashboards available for you to explore.
4. In the search results, choose *[Metricbeat System] Overview ECS*. A Metricbeat dashboard opens:

![A screencapture of the Kibana dashboard named Metricbeat System Overview ECS](../../../images/cloud-ec-logstash-beats-metricbeat-dashboard.png "")

**View the Filebeat dashboard**

1. Open the Kibana main menu and select **Analytics**, then **Dashboard**.
2. In the search box, search for *filebeat system*.
3. In the search results, choose *[Filebeat System] Syslog dashboard ECS*. A Filebeat dashboard displaying your Filebeat data:

![A screencapture of the Kibana dashboard named Filebeat System ECS](../../../images/cloud-ec-logstash-beats-filebeat-dashboard.png "")

Now, you should have a good understanding of how to configure {{ls}} to ingest data from multiple Beats. You have the basics needed to begin experimenting with your own combination of Beats and modules.

