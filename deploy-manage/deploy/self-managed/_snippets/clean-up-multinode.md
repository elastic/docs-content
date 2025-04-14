Perform the following steps on each node in the cluster:

1. Open `elasticsearch.yml` in a text editor.
2. Comment out or remove the `cluster.initial_master_nodes` setting, if present.
3. Update the `discovery.seed_hosts` value so it contains the IP address and port of each of the master-eligible {{es}} nodes in the cluster. In the first node in the cluster, you need to add the `discovery.seed_hosts` setting manually.
4. Optionally, [restart the {{es}} service](/deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md) to validate your configuration changes.

If you don't perform these steps, then one or more nodes will fail the [discovery configuration bootstrap check](/deploy-manage/deploy/self-managed/bootstrap-checks.md#bootstrap-checks-discovery-configuration) when they are restarted.

For more information, refer to [](/deploy-manage/distributed-architecture/discovery-cluster-formation.md).