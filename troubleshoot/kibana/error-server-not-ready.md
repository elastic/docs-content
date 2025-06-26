---
navigation_title: "Error: Server not ready"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/access.html#not-ready
applies_to:
  deployment:
    ess: all
    ece: all
    self: all
    eck: all
products:
  - id: kibana
---

# Error: {{kib}} server is not ready yet [not-ready]

To troubleshoot the `Kibana server is not ready yet` error, try these steps:

1. From within a {{kib}} node, confirm the connection to {{es}}:

    ```sh
    curl -XGET elasticsearch_ip_or_hostname:9200/
    ```

2. Guarantee the health of the three {{kib}}-backing indices.  All indices must appear and display `status:green` and `status:open`:

    ```sh
    curl -XGET elasticsearch_ip_or_hostname:9200/_cat/indices/.kibana,.kibana_task_manager,.kibana_security_session,.security*?v=true
    ```

    These {{kib}}-backing indices must also not have [index settings](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-get-settings) flagging `read_only_allow_delete` or `write` [index blocks](elasticsearch://reference/elasticsearch/index-settings/index-block.md).

3. [Shut down all {{kib}} nodes](../../deploy-manage/maintenance/start-stop-services/start-stop-kibana.md).
4. Choose any {{kib}} node, then update the config to set the [debug logging](../../deploy-manage/monitor/logging-configuration/kibana-log-settings-examples.md#change-overall-log-level).
5. [Start the node](../../deploy-manage/maintenance/start-stop-services/start-stop-kibana.md), then check the start-up debug logs for `ERROR` messages or other start-up issues.

    For example:

    * When {{kib}} is unable to connect to a healthy {{es}} cluster, errors like `master_not_discovered_exception` or `unable to revive connection` or `license is not available` errors appear.
    * When one or more {{kib}}-backing indices are unhealthy, the `index_not_green_timeout` error appears.

## Resources
* [{{kib}} health troubleshooting walkthrough](https://www.elastic.co/blog/troubleshooting-kibana-health)
* [{{kib}} health troubleshooting video](https://www.youtube.com/watch?v=AlgGYcpGvOA)

