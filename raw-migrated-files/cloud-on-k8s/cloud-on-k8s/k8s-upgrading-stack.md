# Upgrade the Elastic Stack version [k8s-upgrading-stack]

::::{warning}
We have identified an issue with Elasticsearch 8.15.1 and 8.15.2 that prevents security role mappings configured via Stack configuration policies to work correctly. Avoid these versions and upgrade to 8.16.0 to remedy this issue if you are affected.
::::


The operator can safely perform upgrades to newer versions of the various Elastic Stack resources.

Follow the instructions in the [Elasticsearch documentation](/deploy-manage/upgrade/deployment-or-cluster.md). Make sure that your cluster is compatible with the target version, take backups, and follow the specific upgrade instructions for each resource type. When you are ready, modify the `version` field in the resource spec to the desired stack version and the operator will start the upgrade process automatically.

ECK will make sure that Elastic Stack resources are upgraded in the correct order. Upgrades to dependent stack resources are delayed until the dependency is upgraded. For example, the Kibana upgrade will be rolled out only when the associated Elasticsearch cluster has been upgraded.

Check [Nodes orchestration](../../../deploy-manage/upgrade/deployment-or-cluster.md) for more information on how the operator performs upgrades and how to tune its behavior.
