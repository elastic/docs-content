After completing the upgrade, verify that your system is fully operational. Check that data ingestion and search are working as expected, clients and integrations can connect, and {{kib}} is accessible.

Confirm that the cluster is healthy and reports the expected version. You can use the following APIs to validate the cluster status after the upgrade:

* Check cluster health
  ```console
  GET _cluster/health?pretty
  ```
  Ensure the status is green, or yellow if that is expected for your configuration (for example, in single-node clusters).

* Check nodes and version
  ```console
  GET _cat/nodes?v&h=name,node.role,master,ip,version
  ```
  Verify that all nodes report the upgraded version in the version column.
