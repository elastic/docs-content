---
mapped_urls:
  - https://www.elastic.co/guide/en/cloud/current/ec-getting-started-search-use-cases-db-logstash.html
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-getting-started-search-use-cases-db-logstash.html
---

# Ingest data from a relational database

% Internal links rely on the following IDs being on this page (e.g. as a heading ID, paragraph ID, etc):

$$$ec-db-logstash-connect-securely$$$

$$$ec-db-logstash-database-structure$$$

$$$ec-db-logstash-database$$$

$$$ec-db-logstash-driver$$$

$$$ec-db-logstash-output$$$

$$$ec-db-logstash-pipeline$$$

$$$ec-db-logstash-prerequisites$$$

$$$ec-db-logstash-trial$$$

$$$ece-db-logstash-connect-securely$$$

$$$ece-db-logstash-database-structure$$$

$$$ece-db-logstash-database$$$

$$$ece-db-logstash-deployment$$$

$$$ece-db-logstash-driver$$$

$$$ece-db-logstash-output$$$

$$$ece-db-logstash-pipeline$$$

$$$ece-db-logstash-prerequisites$$$

This guide explains how to ingest data from a relational database into {{ecloud}} through [{{ls}}](asciidocalypse://docs/logstash/docs/reference/index.md), using the Logstash [JDBC input plugin](asciidocalypse://docs/logstash/docs/reference/plugins-inputs-jdbc.md). It demonstrates how Logstash can be used to efficiently copy records and to receive updates from a relational database, and then send them into {{es}} in an {{ech}} or {{ece}} deployment.

The code and methods presented here have been tested with MySQL. They should work with other relational databases.

The Logstash Java Database Connectivity (JDBC) input plugin enables you to pull in data from many popular relational databases including MySQL and Postgres. Conceptually, the JDBC input plugin runs a loop that periodically polls the relational database for records that were inserted or modified since the last iteration of this loop.

*Time required: 2 hours*


## Prerequisites [ec-db-logstash-prerequisites]

For this tutorial you need a source MySQL instance for Logstash to read from. A free version of MySQL is available from the [MySQL Community Server section](https://dev.mysql.com/downloads/mysql/) of the MySQL Community Downloads site.


## Create a deployment [ec-db-logstash-trial]

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

## Connect securely [ec-db-logstash-connect-securely]

When connecting to {{ech}} or {{ece}} you can use a Cloud ID to specify the connection details. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.

To connect to, stream data to, and issue queries, you need to think about authentication. Two authentication mechanisms are supported, *API key* and *basic authentication*. Here, to get you started quickly, we’ll show you how to use basic authentication, but you can also generate API keys as shown later on. API keys are safer and preferred for production environments.

1. [Download](https://www.elastic.co/downloads/logstash) and unpack Logstash on the local machine that hosts MySQL or another machine granted access to the MySQL machine.


## Get the MySQL JDBC driver [ec-db-logstash-driver]

The Logstash JDBC input plugin does not include any database connection drivers. You need a JDBC driver for your relational database for the steps in the later section [Configure a Logstash pipeline with the JDBC input plugin](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-relational-database-into-elasticsearch-service.md#ec-db-logstash-pipeline).

1. Download and unpack the JDBC driver for MySQL from the [Connector/J section](https://dev.mysql.com/downloads/connector/j/) of the MySQL Community Downloads site.
2. Make a note of the driver’s location as it’s needed in the steps that follow.


## Prepare a source MySQL database [ec-db-logstash-database]

Let’s look at a simple database from which you’ll import data and send it to an {{ech}} or {{ece}} deployment. This example uses a MySQL database with timestamped records. The timestamps enable you to determine easily what’s changed in the database since the most recent data transfer.


### Consider the database structure and design [ec-db-logstash-database-structure]

For this example, let’s create a new database *es_db* with table *es_table*, as the source of our Elasticsearch data.

1. Run the following SQL statement to generate a new MySQL database with a three column table:

    ```txt
    CREATE DATABASE es_db;
    USE es_db;
    DROP TABLE IF EXISTS es_table;
    CREATE TABLE es_table (
      id BIGINT(20) UNSIGNED NOT NULL,
      PRIMARY KEY (id),
      UNIQUE KEY unique_id (id),
      client_name VARCHAR(32) NOT NULL,
      modification_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    ```

    Let’s explore the key concepts in this SQL snippet:

    es_table
    :   The name of the table that stores the data.

    id
    :   The unique identifier for records. *id* is defined as both a PRIMARY KEY and UNIQUE KEY to guarantee that each *id* appears only once in the current table. This is translated to *_id* for updating or inserting the document into Elasticsearch.

    client_name
    :   The data that will ultimately be ingested into Elasticsearch. For simplicity, this example includes only a single data field.

    modification_time
    :   The timestamp of when the record was inserted or last updated. Further in, you can use this timestamp to determine what has changed since the last data transfer into Elasticsearch.

2. Consider how to handle deletions and how to notify Elasticsearch about them. Often, deleting a record results in its immediate removal from the MySQL database. There’s no record of that deletion. The change isn’t detected by Logstash, so that record remains in Elasticsearch.

    There are two possible ways to address this:

    * You can use "soft deletes" in your source database. Essentially, a record is first marked for deletion through a boolean flag. Other programs that are currently using your source database would have to filter out "soft deletes" in their queries. The "soft deletes" are sent over to Elasticsearch, where they can be processed. After that, your source database and Elasticsearch must both remove these "soft deletes."
    * You can periodically clear the Elasticsearch indices that are based off of the database, and then refresh Elasticsearch with a fresh ingest of the contents of the database.

3. Log in to your MySQL server and add three records to your new database:

    ```txt
    use es_db
    INSERT INTO es_table (id, client_name)
    VALUES (1,"Targaryen"),
    (2,"Lannister"),
    (3,"Stark");
    ```

4. Verify your data with a SQL statement:

    ```txt
    select * from es_table;
    ```

    The output should look similar to the following:

    ```txt
    +----+-------------+---------------------+
    | id | client_name | modification_time   |
    +----+-------------+---------------------+
    |  1 | Targaryen   | 2021-04-21 12:17:16 |
    |  2 | Lannister   | 2021-04-21 12:17:16 |
    |  3 | Stark       | 2021-04-21 12:17:16 |
    +----+-------------+---------------------+
    ```

    Now, let’s go back to Logstash and configure it to ingest this data.



## Configure a Logstash pipeline with the JDBC input plugin [ec-db-logstash-pipeline]

Let’s set up a sample Logstash input pipeline to ingest data from your new JDBC Plugin and MySQL database. Beyond MySQL, you can input data from any database that supports JDBC.

1. In `<localpath>/logstash-7.12.0/`, create a new text file named `jdbc.conf`.
2. Copy and paste the following code into this new text file. This code creates a Logstash pipeline through a JDBC plugin.

    ```txt
    input {
      jdbc {
        jdbc_driver_library => "<driverpath>/mysql-connector-java-<versionNumber>.jar" <1>
        jdbc_driver_class => "com.mysql.jdbc.Driver"
        jdbc_connection_string => "jdbc:mysql://<MySQL host>:3306/es_db" <2>
        jdbc_user => "<myusername>" <3>
        jdbc_password => "<mypassword>" <3>
        jdbc_paging_enabled => true
        tracking_column => "unix_ts_in_secs"
        use_column_value => true
        tracking_column_type => "numeric"
        schedule => "*/5 * * * * *"
        statement => "SELECT *, UNIX_TIMESTAMP(modification_time) AS unix_ts_in_secs FROM es_table WHERE (UNIX_TIMESTAMP(modification_time) > :sql_last_value AND modification_time < NOW()) ORDER BY modification_time ASC"
      }
    }
    filter {
      mutate {
        copy => { "id" => "[@metadata][_id]"}
        remove_field => ["id", "@version", "unix_ts_in_secs"]
      }
    }
    output {
      stdout { codec =>  "rubydebug"}
    }
    ```

    1. Specify the full path to your local JDBC driver .jar file (including version number). For example: `jdbc_driver_library => "/usr/share/mysql/mysql-connector-java-8.0.24.jar"`
    2. Provide the IP address or hostname and the port of your MySQL host. For example, `jdbc_connection_string => "jdbc:mysql://127.0.0.1:3306/es_db"`
    3. Provide your MySQL credentials. The username and password must both be enclosed in quotation marks.


    ::::{note}
    If you are using MariaDB (a popular open source community fork of MySQL), there are a couple of things that you need to do differently:

    In place of the MySQL JDBC driver, download and unpack the [JDBC driver for MariaDB](https://downloads.mariadb.org/connector-java/).

    Substitute the following lines in the `jdbc.conf` code, including the `ANSI_QUOTES` snippet in the last line:

    ```txt
    jdbc_driver_library => "<driverPath>/mariadb-java-client-<versionNumber>.jar"
    jdbc_driver_class => "org.mariadb.jdbc.Driver"
    jdbc_connection_string => "jdbc:mariadb://<mySQLHost>:3306/es_db?sessionVariables=sql_mode=ANSI_QUOTES"
    ```

    ::::


    Following are some additional details about the Logstash pipeline code:

    jdbc_driver_library
    :   The Logstash JDBC plugin does not come packaged with JDBC driver libraries. The JDBC driver library must be passed explicitly into the plugin using the `jdbc_driver_library` configuration option.

    tracking_column
    :   This parameter specifies the field `unix_ts_in_secs` that tracks the last document read by Logstash from MySQL, stored on disk in [logstash_jdbc_last_run](asciidocalypse://docs/logstash/docs/reference/plugins-inputs-jdbc.md#plugins-inputs-jdbc-last_run_metadata_path). The parameter determines the starting value for documents that Logstash requests in the next iteration of its polling loop. The value stored in `logstash_jdbc_last_run` can be accessed in a SELECT statement as `sql_last_value`.

    unix_ts_in_secs
    :   The field generated by the SELECT statement, which contains the `modification_time` as a standard [Unix timestamp](https://en.wikipedia.org/wiki/Unix_time) (seconds since the epoch). The field is referenced by the `tracking column`. A Unix timestamp is used for tracking progress rather than a normal timestamp, as a normal timestamp may cause errors due to the complexity of correctly converting back and forth between UMT and the local timezone.

    sql_last_value
    :   This is a [built-in parameter](asciidocalypse://docs/logstash/docs/reference/plugins-inputs-jdbc.md#_predefined_parameters) containing the starting point of the current iteration of the Logstash polling loop, and it is referenced in the SELECT statement line of the JDBC input configuration. This parameter is set to the most recent value of `unix_ts_in_secs`, which is read from `.logstash_jdbc_last_run`. This value is the starting point for documents returned by the MySQL query that is executed in the Logstash polling loop. Including this variable in the query guarantees that we’re not resending data that is already stored in Elasticsearch.

    schedule
    :   This uses cron syntax to specify how often Logstash should poll MySQL for changes. The specification `*/5 * * * * *` tells Logstash to contact MySQL every 5 seconds.  Input from this plugin can be scheduled to run periodically according to a specific schedule. This scheduling syntax is powered by [rufus-scheduler](https://github.com/jmettraux/rufus-scheduler). The syntax is cron-like with some extensions specific to Rufus (for example, timezone support).

    modification_time < NOW()
    :   This portion of the SELECT is explained in detail in the next section.

    filter
    :   In this section, the value `id` is copied from the MySQL record into a metadata field called `_id`, which is later referenced in the output to ensure that each document is written into Elasticsearch with the correct `_id` value. Using a metadata field ensures that this temporary value does not cause a new field to be created. The `id`, `@version`, and `unix_ts_in_secs` fields are also removed from the document, since they don’t need to be written to Elasticsearch.

    output
    :   This section specifies that each document should be written to the standard output using the rubydebug output to help with debugging.

3. Launch Logstash with your new JDBC configuration file:

    ```txt
    bin/logstash -f jdbc.conf
    ```

    Logstash outputs your MySQL data through standard output (`stdout`), your command line interface. The results for the initial data load should look similar to the following:

    ```txt
    [INFO ] 2021-04-21 12:32:32.816 [Ruby-0-Thread-15: :1] jdbc - (0.009082s) SELECT * FROM (SELECT *, UNIX_TIMESTAMP(modification_time) AS unix_ts_in_secs FROM es_table WHERE (UNIX_TIMESTAMP(modification_time) > 0 AND modification_time < NOW()) ORDER BY modification_time ASC) AS 't1' LIMIT 100000 OFFSET 0
    {
              "client_name" => "Targaryen",
        "modification_time" => 2021-04-21T12:17:16.000Z,
               "@timestamp" => 2021-04-21T12:17:16.923Z
    }
    {
              "client_name" => "Lannister",
        "modification_time" => 2021-04-21T12:17:16.000Z,
               "@timestamp" => 2021-04-21T12:17:16.961Z
    }
    {
              "client_name" => "Stark",
        "modification_time" => 2021-04-21T12:17:16.000Z,
               "@timestamp" => 2021-04-21T12:17:16.963Z
    }
    ```

    The Logstash results periodically display SQL SELECT statements, even when there’s nothing new or modified in the MySQL database:

    ```txt
    [INFO ] 2021-04-21 12:33:30.407 [Ruby-0-Thread-15: :1] jdbc - (0.002835s) SELECT count(*) AS 'count' FROM (SELECT *, UNIX_TIMESTAMP(modification_time) AS unix_ts_in_secs FROM es_table WHERE (UNIX_TIMESTAMP(modification_time) > 1618935436 AND modification_time < NOW()) ORDER BY modification_time ASC) AS 't1' LIMIT 1
    ```

4. Open your MySQL console. Let’s insert another record into that database using the following SQL statement:

    ```txt
    use es_db
    INSERT INTO es_table (id, client_name)
    VALUES (4,"Baratheon");
    ```

    Switch back to your Logstash console. Logstash detects the new record and the console displays results similar to the following:

    ```txt
    [INFO ] 2021-04-21 12:37:05.303 [Ruby-0-Thread-15: :1] jdbc - (0.001205s) SELECT * FROM (SELECT *, UNIX_TIMESTAMP(modification_time) AS unix_ts_in_secs FROM es_table WHERE (UNIX_TIMESTAMP(modification_time) > 1618935436 AND modification_time < NOW()) ORDER BY modification_time ASC) AS 't1' LIMIT 100000 OFFSET 0
    {
              "client_name" => "Baratheon",
        "modification_time" => 2021-04-21T12:37:01.000Z,
               "@timestamp" => 2021-04-21T12:37:05.312Z
    }
    ```

5. Review the Logstash output results to make sure your data looks correct. Use `CTRL + C` to shut down Logstash.


## Output to Elasticsearch [ec-db-logstash-output]

In this section, we configure Logstash to send the MySQL data to Elasticsearch. We modify the configuration file created in the section [Configure a Logstash pipeline with the JDBC input plugin](../../../manage-data/ingest/ingesting-data-from-applications/ingest-data-from-relational-database-into-elasticsearch-service.md#ec-db-logstash-pipeline) so that data is output directly to Elasticsearch. We start Logstash to send the data, and then log into your deployment to verify the data in Kibana.

1. Open the `jdbc.conf` file in the Logstash folder for editing.
2. Update the output section with the one that follows:

    ```txt
    output {
      elasticsearch {
        index => "rdbms_idx"
        ilm_enabled => false
        cloud_id => "<DeploymentName>:<ID>" <1>
        cloud_auth => "elastic:<Password>" <2>
        ssl => true
        # api_key => "<myAPIid:myAPIkey>"
      }
    }
    ```

    1. Use the Cloud ID of your {{ech}} or {{ece}} deployment. You can include or omit the `<DeploymentName>:` prefix at the beginning of the Cloud ID. Both versions work fine. Find your Cloud ID by going to the {{kib}} main menu and selecting Management > Integrations, and then selecting View deployment details.
    2. the default username is `elastic`.  It is not recommended to use the `elastic` account for ingesting data as this is a superuser.  We recommend using a user with reduced permissions, or an API Key with permissions specific to the indices or data streams that will be written to.  Check [Configuring security in Logstash](asciidocalypse://docs/logstash/docs/reference/secure-connection.md) for information on roles and API Keys. Use the password provided when you created the deployment if using the `elastic` user, or the password used when creating a new ingest user with the roles specified in the [Configuring security in Logstash](asciidocalypse://docs/logstash/docs/reference/secure-connection.md) documentation.


    Following are some additional details about the configuration file settings:

    index
    :   The name of the Elasticsearch index, `rdbms_idx`, to associate the documents.

    api_key
    :   If you choose to use an API key to authenticate (as discussed in the next step), you can provide it here.

3. **Optional**: For additional security, you can generate an Elasticsearch API key through the {{ech}} or {{ece}} console and configure Logstash to use the new key to connect securely to your deployment.

    1. For {{ech}}, log into [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body), or for {{ece}}, log into the admin console.
    2. Select the deployment name and go to **☰** > **Management** > **Dev Tools**.
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
                 "names": ["logstash-*","rdbms_idx"],
                 "privileges": ["create_index", "write", "read", "manage"]
               }
             ]
           }
         }
        }
        ```

        This creates an API key with the cluster `monitor` privilege which gives read-only access for determining the cluster state, and `manage_index_templates` allows all operations on index templates. Some additional privileges also allow `create_index`, `write`, and `manage` operations for the specified index. The index `manage` privilege is added to enable index refreshes.

    4. Click **▶**. The output should be similar to the following:

        ```json
        {
          "api_key": "tV1dnfF-GHI59ykgv4N0U3",
          "id": "2TBR42gBabmINotmvZjv",
          "name": "logstash_api_key"
        }
        ```

    5. Enter your new `api_key` value into the Logstash `jdbc.conf` file, in the format `<id>:<api_key>`. If your results were as shown in this example, you would enter `2TBR42gBabmINotmvZjv:tV1dnfF-GHI59ykgv4N0U3`. Remember to remove the pound (`#`) sign to uncomment the line, and comment out the `username` and `password` lines:

        ```txt
        output {
          elasticsearch {
            index => "rdbms_idx"
            cloud_id => "<myDeployment>"
            ssl => true
            ilm_enabled => false
            api_key => "2TBR42gBabmINotmvZjv:tV1dnfF-GHI59ykgv4N0U3"
            # user => "<Username>"
            # password => "<Password>"
          }
        }
        ```

4. At this point, if you simply restart Logstash as is with your new output, then no MySQL data is sent to our Elasticsearch index.

    Why? Logstash retains the previous `sql_last_value` timestamp and sees that no new changes have occurred in the MySQL database since that time. Therefore, based on the SQL query that we configured, there’s no new data to send to Logstash.

    Solution:  Add `clean_run => true` as a new line in the JDBC input section of the `jdbc.conf` file. When set to `true`, this parameter resets `sql_last_value` back to zero.

    ```txt
    input {
      jdbc {
          ...
          clean_run => true
          ...
        }
    }
    ```

    After running Logstash once with `sql_last_value` set to `true` you can remove the `clean_run` line, unless you prefer the reset behavior to happen again at each restart of Logstash

5. Open a command line interface instance, go to your Logstash installation path, and start Logstash:

    ```txt
    bin/logstash -f jdbc.conf
    ```

6. Logstash outputs the MySQL data to your {{ech}} or {{ece}} deployment. Let’s take a look in Kibana and verify that data:

    1. For {{ech}}, log into [{{ecloud}}](https://cloud.elastic.co?page=docs&placement=docs-body), or for {{ece}}, log into the admin console.
    2. Select the deployment and go to **☰** > **Management** > **Dev Tools**
    3. Copy and paste the following API GET request into the Console pane, and then click **▶**. This queries all records in the new `rdbms_idx` index.

        ```txt
        GET rdbms_idx/_search
        {
          "query": {
            "match_all": {}
          }
        }
        ```

    4. The Results pane lists the `client_name` records originating from your MySQL database, similar to the following example:

        ![A picture showing query results with three records](../../../images/cloud-ec-logstash-db-results-scenarios.png "")


Now, you should have a good understanding of how to configure Logstash to ingest data from your relational database through the JDBC Plugin. You have some design considerations to track records that are new, modified, and deleted. You should have the basics needed to begin experimenting with your own database and Elasticsearch.

