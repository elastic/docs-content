---
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/access.html#not-ready
---

# Error: Server not ready [access]

The fastest way to access {{kib}} is to use our hosted {{es}} Service. If you [installed {{kib}} on your own](../../deploy-manage/deploy/self-managed/install-kibana.md), access {{kib}} through the web application.


## Set up on cloud [_set_up_on_cloud]

There’s no faster way to get started than with our hosted {{ess}} on Elastic Cloud:

1. [Get a free trial](https://cloud.elastic.co/registration?page=docs&placement=docs-body).
2. Log into [Elastic Cloud](https://cloud.elastic.co?page=docs&placement=docs-body).
3. Click **Create deployment**.
4. Give your deployment a name.
5. Click **Create deployment** and download the password for the `elastic` user.

That’s it! Now that you are up and running, it’s time to get some data into {{kib}}. {{kib}} will open as soon as your deployment is ready.


## Log on to the web application [log-on-to-the-web-application]

If you are using a self-managed deployment, access {{kib}} through the web application on port 5601.

1. Point your web browser to the machine where you are running {{kib}} and specify the port number. For example, `localhost:5601` or `http://YOURDOMAIN.com:5601`.

    To remotely connect to {{kib}}, set [server.host](../../deploy-manage/deploy/self-managed/configure.md#server-host) to a non-loopback address.

2. Log on to your account.
3. Go to the home page, then click **{{kib}}**.
4. To make the {{kib}} page your landing page, click **Make this my landing page**.


## Check the {{kib}} status [status]

The status page displays information about the server resource usage and installed plugins.

To view the {{kib}} status page, use the status endpoint. For example, `localhost:5601/status`.

:::{image} ../../images/kibana-kibana-status-page-7_14_0.png
:alt: Kibana server status page
:class: screenshot
:::

For JSON-formatted server status details, use the `localhost:5601/api/status` API endpoint.


## Troubleshoot {{kib}} UI error [not-ready]

Troubleshoot the `Kibana Server is not Ready yet` error.

1. From within a {{kib}} node, confirm the connection to {{es}}:

    ```sh
    curl -XGET elasticsearch_ip_or_hostname:9200/
    ```

2. Guarantee the health of the three {{kib}}-backing indices.  All indices must appear and display `status:green` and `status:open`:

    ```sh
    curl -XGET elasticsearch_ip_or_hostname:9200/_cat/indices/.kibana,.kibana_task_manager,.kibana_security_session?v=true
    ```

    These {{kib}}-backing indices must also not have [index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) flagging `read_only_allow_delete` or `write` [index blocks](https://www.elastic.co/guide/en/elasticsearch/reference/current/index-modules-blocks.html).

3. [Shut down all {{kib}} nodes](../../deploy-manage/maintenance/start-stop-services/start-stop-kibana.md).
4. Choose any {{kib}} node, then update the config to set the [debug logging](../../deploy-manage/monitor/logging-configuration/kibana-log-settings-examples.md#change-overall-log-level).
5. [Start the node](../../deploy-manage/maintenance/start-stop-services/start-stop-kibana.md), then check the start-up debug logs for `ERROR` messages or other start-up issues.

    For example:

    * When {{kib}} is unable to connect to a healthy {{es}} cluster, errors like `master_not_discovered_exception` or `unable to revive connection` or `license is not available` errors appear.
    * When one or more {{kib}}-backing indices are unhealthy, the `index_not_green_timeout` error appears.


You can find a Kibana health troubleshooting walkthrough in [this blog](https://www.elastic.co/blog/troubleshooting-kibana-health) or in [this video](https://www.youtube.com/watch?v=AlgGYcpGvOA).

