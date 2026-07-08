---
navigation_title: "Upgrades"
description: "Common Elasticsearch rolling upgrade errors and how to resolve them."
type: troubleshooting
applies_to:
  stack: ga
products:
  - id: elasticsearch
---

# Troubleshoot upgrades [troubleshooting-upgrades]

Most {{es}} [upgrades](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md) succeed without issues, as long as you [plan](/deploy-manage/upgrade/plan-upgrade.md) and [prepare](/deploy-manage/upgrade/prepare-to-upgrade.md) for them carefully. This page describes the problems you're most likely to encounter during a rolling upgrade, and how to resolve them.

You can avoid most of these issues by completing the steps in the [](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md) before you start. For more information, refer to [](/troubleshoot/elasticsearch/troubleshooting-upgrade-assistant.md).

## Monitor an upgrade [troubleshooting-upgrades-monitor]

During a rolling upgrade, {{es}} supports running two versions at the same time (the earlier version and the later version), but never more than two, and only for the duration of the upgrade.

If your nodes share the same configuration (other than [node roles](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles.md)), and you follow the [recommended upgrade order](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md#upgrade-order), any potential issues will surface as you upgrade the first node.

Monitor the upgrade at a high level by checking the list of cluster nodes, and at a low level by tailing the logs of the restarting node.

### Poll cluster nodes [troubleshooting-upgrades-monitor-list]

To monitor which nodes have been upgraded, use the [cat nodes API]({{es-apis}}operation/operation-cat-nodes):

```console
GET _cat/nodes?v=true&h=name,ip,role,master,version,uptime&s=uptime
```

In an example three-node cluster, the first node's upgrade progresses as follows:

1. All nodes are present in the cluster.

	```console-result
	name                  ip          role   master version uptime
	instance-0000000000   10.42.4.93  himrst *      8.19.x   20d
	instance-0000000001   10.42.1.10  himrst -      8.19.x   20d
	tiebreaker-0000000003 10.42.0.222 mv     -      8.19.x   20d
	```

2. As the node shuts down, it stops syncing with the elected master.

	```console-result
	name                  ip          role   master version uptime
	instance-0000000000   10.42.4.93  himrst *      8.19.x   20d
	instance-0000000001
	tiebreaker-0000000003 10.42.0.222 mv     -      8.19.x   20d
	```

3. The elected master removes the node from the cluster, so it no longer appears.

	```console-result
	name                  ip          role   master version uptime
	instance-0000000000   10.42.4.93  himrst *      8.19.x   20d
	tiebreaker-0000000003 10.42.0.222 mv     -      8.19.x   20d
	```

4. After the node restarts and rejoins the cluster, it appears again, now running the later version.

	```console-result
	name                  ip          role   master version uptime
	instance-0000000001   10.42.1.10  himrst -      9.x.x     5s
	instance-0000000000   10.42.4.93  himrst *      8.19.x   20d
	tiebreaker-0000000003 10.42.0.222 mv     -      8.19.x   20d
	```

If a node doesn't rejoin the cluster, inspect its restart logs.

### Check node logs [troubleshooting-upgrades-monitor-logs]

While a node is restarting, you can tail its logs for information about the upgrade-and-restart process. Try filtering for logs related to [discovery and cluster formation](/deploy-manage/distributed-architecture/discovery-cluster-formation.md) events. For example:

* In [Discover](/explore-analyze/discover.md) on an attached [monitoring cluster](/deploy-manage/monitor/stack-monitoring.md), apply a [Lucene filter](/explore-analyze/query-filter/languages/lucene-query-syntax.md) on `.monitoring*`:

	```text
	"node-join" OR "node-left" OR "master node changed" OR "elected-as-master" exitcode OR initializing OR fatal OR "publish_address"
	```

* On the host, `tail` the [{{es}} logs](/deploy-manage/monitor/logging-configuration.md) through a `grep` filter:

	```text
	grep -Ei 'node-join|node-left|master node changed|elected-as-master|exitcode|initializing|fatal|publish_address'
	```

Based on your findings, refer to the [common error resolutions](#troubleshooting-upgrades-errors).

## How a rolling upgrade works [troubleshooting-upgrades-theory]

During a rolling upgrade, the cluster continues to operate normally.

New functionality stays inactive, or runs in a backward-compatible mode, until the last node running the earlier version leaves the cluster. New and updated features become fully operational only when every node is running the later version.

Normally, a node running the earlier version leaves the cluster only when you shut it down to upgrade it. The last earlier-version node leaves when there are no more nodes to upgrade.

The following sections describe edge cases that can disrupt this process:

* A node unexpectedly leaves the cluster.
* Nodes are upgraded out of the [recommended order](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md#upgrade-order).
* The cluster isn't [highly available](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md).

### Unexpected node disconnect [troubleshooting-upgrades-theory-disconnect]

Because of [cluster fault detection](/deploy-manage/distributed-architecture/discovery-cluster-formation/cluster-fault-detection.md), a node running the earlier version might leave the cluster before you deliberately shut it down (temporarily, or indefinitely until you intervene). Recover the node into the cluster before you continue the rolling upgrade.

:::{note}
:applies_to: { ece:, ess: }

If a node unexpectedly leaves the cluster during a rolling upgrade, the upgrade might pause to prevent data loss. When this happens, the [Deployment Activity](/deploy-manage/deploy/elastic-cloud/keep-track-of-deployment-activity.md) shows the status **Waiting until cluster recovers** and reports fewer nodes than expected.
:::

### Premature cluster version update [troubleshooting-upgrades-theory-version]

If all the remaining earlier version nodes unexpectedly leave the cluster during an upgrade, the cluster does the following:

* Reports its state as fully upgraded
* Automatically activates new functionality
* Leaves its backward-compatible mode

Afterward, you can't return the cluster to a state that's compatible with the earlier version nodes.

Nodes running the earlier version can no longer join the fully upgraded cluster. Their {{es}} logs report `failed to join` errors, with a `Caused by` such as:

* `node version [x.x.x] may not join a cluster comprising only nodes of version [y.y.y] or greater`
* `node with version [x.x.x] may not join a cluster with minimum version [y.y.y]`
* `node with system index mappings versions [y.y.y] may not join a cluster with minimum system index mappings versions [x.x.x]`
* `handshake with [NODE_ID] failed: remote node version [x.x.x] is incompatible with local node version [y.y.y]`

{{es}} preserves the data in the data paths of the older nodes and uses it to recover the cluster to health after you fully upgrade them. To bring these nodes back into the cluster, upgrade them.

:::{note}
:applies_to: { ece:, ess: }

If a node leaving the cluster causes the [cluster health API]({{es-apis}}operation/operation-cluster-health) to report `red`, the upgrade might pause to protect your data. If this happens, [contact us](/troubleshoot/index.md#contact-us) with one of the following:

* {{ech}} deployment ID
* [{{ece}} diagnostic](/troubleshoot/deployments/cloud-enterprise/run-ece-diagnostics-tool.md) flagged `--deployments` for the problematic deployment ID, after attempting a [pause and resume instance](/deploy-manage/maintenance/ece/pause-instance.md)

:::

### Stopping master-eligible nodes [troubleshooting-upgrades-theory-masters]

If you stop half or more of the master-eligible nodes at the same time during the upgrade, the cluster [becomes unavailable](/troubleshoot/elasticsearch/discovery-troubleshooting.md#discovery-no-master) because too few remain to form a [voting quorum](/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-voting.md).

Production environments should have [at least three master-eligible nodes for high availability](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md). In a test or development environment with only one or two master-eligible nodes, you can't avoid stopping half or more of them, so the cluster always [becomes unavailable](/troubleshoot/elasticsearch/discovery-troubleshooting.md#discovery-no-master) at some point during the upgrade.

Restart all the stopped master-eligible nodes so the cluster can re-form. This might trigger a [premature cluster version update](#troubleshooting-upgrades-theory-version); to reduce this risk, [upgrade the master-eligible nodes last](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md#upgrade-order).


## Common issues [troubleshooting-upgrades-errors]

When nodes restart, they can encounter errors that also occur outside of upgrades. The most common are:

* Startup failures from misconfigured [`systemctl` timeout settings](/deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md#start-deb)
* Startup failures from misconfigured settings that trip [bootstrap checks](/deploy-manage/deploy/self-managed/bootstrap-checks.md)
* Errors during [node discovery and cluster formation](/troubleshoot/elasticsearch/discovery-troubleshooting.md)
* [Circuit breaker](/troubleshoot/elasticsearch/circuit-breaker-errors.md) or [watermark errors](/troubleshoot/elasticsearch/fix-watermark-errors.md) from temporary resource shortages
* Issues caused by insufficient [high availability](/deploy-manage/deploy/elastic-cloud/elastic-cloud-hosted-planning.md)

The rest of this page covers errors specific to the rolling upgrade itself.

### Bootstrap checks [troubleshooting-upgrades-errors-bootstrap]

These [bootstrap checks](/deploy-manage/deploy/self-managed/bootstrap-checks.md#checks) occur only during rolling upgrades.

#### Index compatibility [troubleshooting-upgrades-errors-bootstrap-index]

{{es}} indices are [compatible across sequential major versions](/deploy-manage/upgrade/deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md) only. When a restarting node tries to load metadata for an outdated, incompatible index, it fails with an error such as:

* `The index [index-000001] created in version [y-1.x.x] with current compatibility version [y-1.x.x] must be marked as read-only using the setting [index.blocks.write] set to [true] before upgrading to y+1.z.z.`
* `Cannot start this node because it holds metadata for indices with version [y-1.x.x] with which this node of version [y+1.z.z] is incompatible. Revert this node to version [y.y.y] and delete any indices with versions earlier than [y.0.0] before upgrading to version [y+1.z.z]. If all such indices have already been deleted, revert this node to version [y.y.y] and wait for it to join the cluster to clean up any older indices from its metadata.`
* `cannot upgrade node because incompatible indices created with version [y-1.x.x] exist, while the minimum compatible index version is [y.y.y]. Upgrade your older indices by reindexing them in version [y+1.z.z] first`

This error means the [](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md) found issues that still need to be resolved.

Before you begin the upgrade again, revert the node to the earlier version, rejoin it to the cluster, and complete every critical item in the [](/deploy-manage/upgrade/prepare-to-upgrade/upgrade-assistant.md). For more details, refer to [](/troubleshoot/elasticsearch/troubleshooting-upgrade-assistant.md).

#### Unknown settings [troubleshooting-upgrades-errors-bootstrap-unknown]

If the [{{es}} configuration](/deploy-manage/deploy/self-managed/configure-elasticsearch.md) contains settings that are no longer valid in the later version, the node might fail to start with an error such as:

* `unknown setting [X] please check that any required plugins are installed, or check the breaking changes documentation for removed settings`
* `The configuration setting [X] is required`

This error means you didn't fully [review breaking changes](/deploy-manage/upgrade/prepare-to-upgrade.md) during preparation. Resolve every `unknown setting` startup error before you continue. For common examples, refer to [](/troubleshoot/monitoring/node-bootlooping.md).

### Shard allocation issues [troubleshooting-upgrades-errors-allocation]

You might see [shard allocation issues](/troubleshoot/elasticsearch/diagnose-unassigned-shards.md) if:

* Node upgrades didn't follow the [recommended upgrade order](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md#upgrade-order)
* One of the [edge cases](#troubleshooting-upgrades-theory) described earlier occurs

Beyond the [common allocation issues](/troubleshoot/elasticsearch/cluster-allocation-api-examples.md), these errors appear only during rolling upgrades:

* incompatible index versions

	* `illegal_argument_exception: The index [my_index] was created with version [X.X.X] but the minimum compatible version is [Y.Y.Y]`
	* `java.lang.IllegalStateException: index [my_index] version not supported: X.X.X maximum compatible index version is: Y.Y.Y`
	
* incompatible shard versions

	* `cannot allocate replica shard to a node with version [X.X.X] since this is older than the primary version [Y.Y.Y]`

If you encounter any of these, continue upgrading your nodes. The data allocates as more nodes reach the later version.

### Post-upgrade issues [troubleshooting-upgrades-errors-post]

These issues can appear after an {{es}} upgrade if specific upgrade tasks remain unfinished.

#### Kibana availability [troubleshooting-upgrades-errors-post-kibana]

If {{kib}} doesn't start after [its upgrade](/deploy-manage/upgrade/deployment-or-cluster/kibana.md), or reports [`Kibana server is not ready yet`](/troubleshoot/kibana/error-server-not-ready.md), make sure you [re-enabled shard allocation](/deploy-manage/upgrade/deployment-or-cluster/elasticsearch.md#re-enable-shard-allocation).

#### Transform upgrade mode [troubleshooting-upgrades-errors-post-transforms]

If you [set `upgrade_mode` for transform indices]({{es-apis}}operation/operation-transform-set-upgrade-mode), you might see unexpected errors after the upgrade, such as:

* `Cannot stop any Transform while the Transform feature is upgrading (408)`
* `Transform task will not be assigned while upgrade mode is enabled.`

Set `enabled=false` to exit upgrade mode for transforms.

#### Machine learning upgrade mode [troubleshooting-upgrades-errors-post-ml]

If you [set `upgrade_mode` for machine learning indices]({{es-apis}}operation/operation-ml-set-upgrade-mode), you might see unexpected errors after the upgrade, such as:

* `You don't have permission to manage Machine Learning jobs. Access to the plugin requires the Machine Learning feature to be visible in this space.`
* `Index migration in progress. Indices related to Machine Learning are currently being upgraded. Some actions will not be available during this time.`

Set `enabled=false` to exit upgrade mode for machine learning.
