---
navigation_title: "Troubleshoot upgrades"
description: "Common upgrade issues and resolutions."
type: troubleshooting
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Troubleshoot upgrades [troubleshooting-upgrades]

Usually, [{{es}} upgrades](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md) proceed smoothly due to due diligence in upgrade [planning](/deploy-manage/upgrade/plan-upgrade.md) and [preparation](/deploy-manage/upgrade/prepare-to-upgrade.md). 

To avoid majority of errors discussed below, ensure to resolve all [Upgrade Assistant](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md) critical items before beginning upgrading. For more information, refer to [Troubleshoot Upgrade Assistant](/troubleshoot/elasticsearch/troubleshooting-upgrade-assistant.md).

If you suspect an issue monitoring your upgrade, inspect progress through the following outline. We have compiled the most common error resolutions encountered for your reference to review based on your findings.

## Monitor upgrade [troubleshooting-upgrades-monitor]

{{es}} supports running two versions during a rolling upgrade, from an earlier version to later version. It does not ever support running more than two versions. It does not support two versions beyond the duration of the rolling upgrade.

Assuming {{es}} configuration uniformity outside of [node role](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md) designations and that the [nodes upgrade order](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md#upgrade-order) is respected, then the majority of rolling upgrade errors will surface when the first node upgrades.

You can monitor the rolling upgrade high-level by checking cluster nodes' list and low-level by tailing the restarting node's logs.

### Poll cluster nodes [troubleshooting-upgrades-monitor-list]

To monitor which nodes have been upgraded, use the [CAT nodes](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) API:

```console
GET _cat/nodes?v=true&h=name,ip,role,master,version,uptime&s=uptime
```

For an example three node cluster, this first node's upgrade could appear like

1. All nodes report in cluster.

	```console-result
	name                  ip          role   master version uptime
	instance-0000000000   10.42.4.93  himrst *      8.19.x   20d
	instance-0000000001   10.42.1.10  himrst -      8.19.x   20d
	tiebreaker-0000000003 10.42.0.222 mv     -      8.19.x   20d
	```

2. As the node shuts down, it stops syncing to the elected-master.

	```console-result
	name                  ip          role   master version uptime
	instance-0000000000   10.42.4.93  himrst *      8.19.x   20d
	instance-0000000001
	tiebreaker-0000000003 10.42.0.222 mv     -      8.19.x   20d
	```

3. The elected-master removes the node from the cluster and it no longer shows.

	```console-result
	name                  ip          role   master version uptime
	instance-0000000000   10.42.4.93  himrst *      8.19.x   20d
	tiebreaker-0000000003 10.42.0.222 mv     -      8.19.x   20d
	```

4. After the node starts back up and rejoins cluster, it again reports in cluster.

	```console-result
	name                  ip          role   master version uptime
	instance-0000000001   10.42.1.10  himrst -      9.x.x     5s
	instance-0000000000   10.42.4.93  himrst *      8.19.x   20d
	tiebreaker-0000000003 10.42.0.222 mv     -      8.19.x   20d
	```

If a node does not rejoin cluster, you will inspect its restart logs.

### Check node logs [troubleshooting-upgrades-monitor-logs]

While the node is restarting, you can tail its logs for information related to its upgrade and restart. 

You would commonly filter to logs specific to [discovery and cluster formation](/deploy-manage/distributed-architecture/discovery-cluster-formation.md) events. For example, from:

* An attached [monitoring cluster](/deploy-manage/monitor/stack-monitoring.md), you could [Lucene filter](/explore-analyze/query-filter/languages/lucene-query-syntax.md) in [Discover](/explore-analyze/discover.md) for `.monitoring*`:

	```text
	"node-join" OR "node-left" OR "master node changed" OR "elected-as-master" exitcode OR initializing OR fatal OR "publish_address"
	```

* The host's terminal, doing a `tail` of the [{{es}} logging](/deploy-manage/monitor/logging-configuration.md) with a `grep` filter:

	```text
	grep -Ei 'node-join|node-left|master node changed|elected-as-master|exitcode|initializing|fatal|publish_address'
	```

We have compiled the most [common error resolutions](#troubleshooting-upgrades-errors) encountered for your reference to review based on your findings.

## Rolling upgrades considerations [troubleshooting-upgrades-theory]

During a rolling upgrade, the cluster continues to operate normally. 

New functionality is either inactive or operates in a backward-compatible mode until the last node of earlier version leaves the cluster. New functionality becomes operational when all nodes in the cluster are running the later version. 

Usually, the earlier version nodes only leave the cluster when you shut them down to upgrade them. In this case, the last earlier version node leaves the cluster when there are no more nodes to upgrade.

The following outline edge cases and their impacts where:

* One or more nodes unexpectedly leave cluster.
* Nodes leave cluster out of expected [upgrade order](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md#upgrade-order).
* Cluster was not architected to be [highly available](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md).

### Unexpected node disconnect [troubleshooting-upgrades-theory-disconnect]

It is possible that an earlier version node might temporarily or permanently (until intervened) leave the cluster before you purposely shut it down due to [cluster fault detection](/deploy-manage/distributed-architecture/discovery-cluster-formation/cluster-fault-detection.md). You should normally recover node into cluster before continuing rolling upgrade.

:::{note} :applies_to: { ece:, ess: }
A node unexpectedly out of cluster during a rolling upgrade can cause the platform to stall the upgrade to avoid data loss. If this occurs, the [Deployment Activity](/deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md)'s {{es}} plan step "Performing a rolling change" status "Waiting until cluster recovers" will report a subset of expected node counts.
:::

### Premature cluster version update [troubleshooting-upgrades-theory-version]

If all the remaining earlier version nodes unexpectedly leave the cluster during an upgrade, the cluster will 

* consider itself to be fully-upgraded
* automatically activate new functionality
* leave its backward-compatible mode

Once that has happened, there is no way to return the cluster to a state that is compatible with the earlier version nodes. 

Nodes running the earlier version will not be able to join this fully-upgraded cluster. Their {{es}} logs will report `failed to join` issues due to `Caused by` errors like

* `node version [x.x.x] may not join a cluster comprising only nodes of version [y.y.y] or greater`
* `node with version [x.x.x] may not join a cluster with minimum version [y.y.y]`
* `node with system index mappings versions [y.y.y] may not join a cluster with minimum system index mappings versions [x.x.x]`
* `handshake with [NODE_ID] failed: remote node version [x.x.x] is incompatible with local node version [y.y.y]`

{{es}} maintains the data in the data paths of the older nodes and will recover the cluster to health using this data after the nodes are fully upgraded. Therefore, to bring these nodes back into the cluster, upgrade them.

:::{note} :applies_to: { ece:, ess: }
You can re-trigger your [Deployment Upgrade](/deploy-manage/upgrade/deployment-or-cluster/upgrade-on-ech.md#perform-cloud-upgrade) to pick up upgrade where it left off to complete it.

If the node out of cluster causes a [Cluster health](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-health) API status of `red`, then plans will be blocked for data safety. 

If this is the case, [contact us](/troubleshoot/index.md#contact-us) with either the

* {{ech}} deployment ID
* [{{ece}} diagnostic](/troubleshoot/deployments/cloud-enterprise/run-ece-diagnostics-tool.md) flagged `--deployments` for the problematic deployment ID after attempting a [pause and resume instance](/deploy-manage/maintenance/ece/pause-instance.md)
:::

### Stopping master-eligible nodes [troubleshooting-upgrades-theory-masters]

If you stop half or more of the master-eligible nodes all at once during the upgrade, the cluster will [become unavailable](/troubleshoot/elasticsearch/discovery-troubleshooting.md#discovery-no-master) due to insufficient [voting configurations](/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-voting.md).

Production environments should have [at least three master-eligible nodes for high availability](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md). In a testing or development environment with only one or two master-eligible nodes, you cannot avoid stopping half or more of the master-eligible nodes, so the cluster will always [become unavailable](/troubleshoot/elasticsearch/discovery-troubleshooting.md#discovery-no-master) at some point during the upgrade.

You must restart all the stopped master-eligible nodes to allow the cluster to re-form. This might cause a [premature cluster version update](#troubleshooting-upgrades-theory-version).

[Upgrade the master-eligible nodes last](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md#upgrade-order) to make it less likely that this occurs.


## Common issues [troubleshooting-upgrades-errors]

Restarting nodes can encounter errors which might otherwise surface. Most commonly:

* during start-up due to misconfigured [`systemctl` timeout settings](/deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md#start-deb)
* during start-up due to misconfigured settings tripping [bootstrap check failures](/deploy-manage/deploy/self-managed/bootstrap-checks.md)
* during [node discovery and cluster formation](/troubleshoot/elasticsearch/discovery-troubleshooting.md)
* [circuit breaker](/troubleshoot/elasticsearch/circuit-breaker-errors.md) or [watermark errors](/troubleshoot/elasticsearch/fix-watermark-errors.md) due to temporary resource unavailability
* related to lack of [high availability](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md) architecture

The following supplements this list with errors specific to the rolling upgrade period.

### Bootstrap checks [troubleshooting-upgrades-errors-bootstrap]

The following are [bootstrap checks](/deploy-manage/deploy/self-managed/bootstrap-checks.md#checks) which uniquely surface during rolling upgrades.

#### Index compatibility [troubleshooting-upgrades-errors-bootstrap-index]

{{es}} indices are [compatible for sequential major versions](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md). Restarting nodes will error attempting to load metadata for outdated incompatible versions like

* `The index [index-000001] created in version [y-1.x.x] with current compatibility version [y-1.x.x] must be marked as read-only using the setting [index.blocks.write] set to [true] before upgrading to y+1.z.z.`
* `Cannot start this node because it holds metadata for indices with version [y-1.x.x] with which this node of version [y+1.z.z] is incompatible. Revert this node to version [y.y.y] and delete any indices with versions earlier than [y.0.0] before upgrading to version [y+1.z.z]. If all such indices have already been deleted, revert this node to version [y.y.y] and wait for it to join the cluster to clean up any older indices from its metadata.`
* `cannot upgrade node because incompatible indices created with version [y-1.x.x] exist, while the minimum compatible index version is [y.y.y]. Upgrade your older indices by reindexing them in version [y+1.z.z] first`

This error indicates the [Upgrade Assistant](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md) was not fully completed during [upgrade preparation work](/deploy-manage/upgrade/prepare-to-upgrade.md).

You should reset this node's version upgrade, rejoin it to cluster at the earlier version, and complete the [Upgrade Assistant](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md) critical items before beginning upgrading. Refer also to [Troubleshoot Upgrade Assistant](/troubleshoot/elasticsearch/troubleshooting-upgrade-assistant.md).

#### Unknown settings [troubleshooting-upgrades-errors-bootstrap-unknown]

If the [{{es}} configuration](/deploy-manage/deploy/self-managed/configure-elasticsearch.md) contains settings deprecated on the later version, it might error like:

* `unknown setting [X] please check that any required plugins are installed, or check the breaking changes documentation for removed settings`
* `The configuration setting [X] is required`

This error indicates the [Preparation steps' Review breaking changes](/deploy-manage/upgrade/prepare-to-upgrade.md) was not sufficiently completed. You will need to resolve all `unknown setting` startup errors. For the most common examples, refer to [Troubleshooting node bootlooping](/troubleshoot/monitoring/node-bootlooping.md).

### Shard allocation issues [troubleshooting-upgrades-errors-allocation]

You might experience [shard allocation issues](/troubleshoot/elasticsearch/diagnose-unassigned-shards.md) if 

* [nodes upgrade order](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md#upgrade-order) was not respected
* one of the earlier [rolling upgrades considerations](#troubleshooting-upgrades-theory) triggers

The following supplement [common allocation issues](/troubleshoot/elasticsearch/cluster-allocation-api-examples.md) with errors which uniquely surface during rolling upgrades:

* incompatible index versions

	* `illegal_argument_exception: The index [my_index] was created with version [X.X.X] but the minimum compatible version is [Y.Y.Y]`
	* `java.lang.IllegalStateException: index [my_index] version not supported: X.X.X maximum compatible index version is: Y.Y.Y`
	
* incompatible shard versions

	* `cannot allocate replica shard to a node with version [X.X.X] since this is older than the primary version [Y.Y.Y]`

If any of these are encountered, you should continue rolling upgrading your nodes. As more nodes on expected later version become available, the data will allocate.

### Post-upgrade [troubleshooting-upgrades-errors-post]

The following are common issues which surface after {{es}} upgrade from unfinished upgrade tasks.

### Kibana availability [troubleshooting-upgrades-errors-post-kibana]

If {{kib}} does not start after [its upgrade](/deploy-manage/upgrade/deployment-or-cluster/kibana.md) but continues to be unavailable or report [`Kibana server is not ready yet`](/troubleshoot/kibana/error-server-not-ready.md) then ensure you [re-enabled shard allocation](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md#re-enable-shard-allocation).

### Transform upgrade mode [troubleshooting-upgrades-errors-post-transforms]

If you [Set upgrade_mode for transform indices]({{es-apis}}operation-transform-set-upgrade-mode), then you might encounter errors unexpected after upgrade like

* `Cannot stop any Transform while the Transform feature is upgrading (408)`
* `Transform task will not be assigned while upgrade mode is enabled.`

Update this to `enabled=false` to exit upgrade mode for transforms.

### Machine Learning upgrade mode [troubleshooting-upgrades-errors-post-ml]

If you [Set upgrade_mode for machine learning indices]({{es-apis}}operation/operation-ml-set-upgrade-mode), then you might encounter errors unexpected after upgrade like:

* `You don't have permission to manage Machine Learning jobs. Access to the plugin requires the Machine Learning feature to be visible in this space.`
* `Index migration in progress. Indices related to Machine Learning are currently being upgraded. Some actions will not be available during this time.`

Update this to `enabled=false` to exit upgrade mode for machine learning.
