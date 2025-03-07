---
navigation_title: "Hot spotting"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/hotspotting.html
---



# Hot spotting [hotspotting]


Computer [hot spotting](https://en.wikipedia.org/wiki/Hot_spot_(computer_programming)) may occur in {{es}} when resource utilizations are unevenly distributed across [nodes](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md). Temporary spikes are not usually considered problematic, but ongoing significantly unique utilization may lead to cluster bottlenecks and should be reviewed.

::::{tip}
If you’re using Elastic Cloud Hosted, then you can use AutoOps to monitor your cluster. AutoOps significantly simplifies cluster management with performance recommendations, resource utilization visibility, real-time issue detection and resolution paths. For more information, refer to [Monitor with AutoOps](/deploy-manage/monitor/autoops.md).

::::


See [this video](https://www.youtube.com/watch?v=Q5ODJ5nIKAM) for a walkthrough of troubleshooting a hot spotting issue.


## Detect hot spotting [detect]

Hot spotting most commonly surfaces as significantly elevated resource utilization (of `disk.percent`, `heap.percent`, or `cpu`) among a subset of nodes as reported via [cat nodes](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes). Individual spikes aren’t necessarily problematic, but if utilization repeatedly spikes or consistently remains high over time (for example longer than 30 seconds), the resource may be experiencing problematic hot spotting.

For example, let’s show case two separate plausible issues using cat nodes:

```console
GET _cat/nodes?v&s=master,name&h=name,master,node.role,heap.percent,disk.used_percent,cpu
```

Pretend this same output pulled twice across five minutes:

```console-result
name   master node.role heap.percent disk.used_percent cpu
node_1 *      hirstm              24                20  95
node_2 -      hirstm              23                18  18
node_3 -      hirstmv             25                90  10
```
%  TEST[skip:illustrative response only]

Here we see two significantly unique utilizations: where the master node is at `cpu: 95` and a hot node is at `disk.used_percent: 90%`. This would indicate hot spotting was occurring on these two nodes, and not necessarily from the same root cause.


## Causes [causes]

Historically, clusters experience hot spotting mainly as an effect of hardware, shard distributions, and/or task load. We’ll review these sequentially in order of their potentially impacting scope.


## Hardware [causes-hardware]

Here are some common improper hardware setups which may contribute to hot spotting:

* Resources are allocated non-uniformly. For example, if one hot node is given half the CPU of its peers. {{es}} expects all nodes on a [data tier](../../manage-data/lifecycle/data-tiers.md) to share the same hardware profiles or specifications.
* Resources are consumed by another service on the host, including other {{es}} nodes. Refer to our [dedicated host](../../deploy-manage/deploy/self-managed/deploy-cluster.md#dedicated-host) recommendation.
* Resources experience different network or disk throughputs. For example, if one node’s I/O is lower than its peers. Refer to [Use faster hardware](../../deploy-manage/production-guidance/optimize-performance/indexing-speed.md) for more information.
* A JVM that has been configured with a heap larger than 31GB. Refer to [Set the JVM heap size](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-heap-size) for more information.
* Problematic resources uniquely report [memory swapping](../../deploy-manage/deploy/self-managed/setup-configuration-memory.md).


## Shard distributions [causes-shards]

{{es}} indices are divided into one or more [shards](https://en.wikipedia.org/wiki/Shard_(database_architecture)) which can sometimes be poorly distributed. {{es}} accounts for this by [balancing shard counts](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md) across data nodes. As [introduced in version 8.6](https://www.elastic.co/blog/whats-new-elasticsearch-kibana-cloud-8-6-0), {{es}} by default also enables [desired balancing](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md) to account for ingest load. A node may still experience hot spotting either due to write-heavy indices or by the overall shards it’s hosting.


### Node level [causes-shards-nodes]

You can check for shard balancing via [cat allocation](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-allocation), though as of version 8.6, [desired balancing](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md) may no longer fully expect to balance shards. Kindly note, both methods may temporarily show problematic imbalance during [cluster stability issues](../../deploy-manage/distributed-architecture/discovery-cluster-formation/cluster-fault-detection.md).

For example, let’s showcase two separate plausible issues using cat allocation:

```console
GET _cat/allocation?v&s=node&h=node,shards,disk.percent,disk.indices,disk.used
```

Which could return:

```console-result
node   shards disk.percent disk.indices disk.used
node_1    446           19      154.8gb   173.1gb
node_2     31           52       44.6gb   372.7gb
node_3    445           43      271.5gb   289.4gb
```
%  TEST[skip:illustrative response only]

Here we see two significantly unique situations. `node_2` has recently restarted, so it has a much lower number of shards than all other nodes. This also relates to `disk.indices` being much smaller than `disk.used` while shards are recovering as seen via [cat recovery](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-recovery). While `node_2`'s shard count is low, it may become a write hot spot due to ongoing [ILM rollovers](elasticsearch://reference/elasticsearch/index-lifecycle-actions/ilm-rollover.md). This is a common root cause of write hot spots covered in the next section.

The second situation is that `node_3` has a higher `disk.percent` than `node_1`, even though they hold roughly the same number of shards. This occurs when either shards are not evenly sized (refer to [Aim for shards of up to 200M documents, or with sizes between 10GB and 50GB](../../deploy-manage/production-guidance/optimize-performance/size-shards.md#shard-size-recommendation)) or when there are a lot of empty indices.

Cluster rebalancing based on desired balance does much of the heavy lifting of keeping nodes from hot spotting. It can be limited by either nodes hitting [watermarks](elasticsearch://reference/elasticsearch/configuration-reference/cluster-level-shard-allocation-routing-settings.md#disk-based-shard-allocation) (refer to [fixing disk watermark errors](fix-watermark-errors.md)) or by a write-heavy index’s total shards being much lower than the written-to nodes.

You can confirm hot spotted nodes via [the nodes stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-stats), potentially polling twice over time to only checking for the stats differences between them rather than polling once giving you stats for the node’s full [node uptime](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-usage). For example, to check all nodes indexing stats:

```console
GET _nodes/stats?human&filter_path=nodes.*.name,nodes.*.indices.indexing
```


### Index level [causes-shards-index]

Hot spotted nodes frequently surface via [cat thread pool](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-thread-pool)'s `write` and `search` queue backups. For example:

```console
GET _cat/thread_pool/write,search?v=true&s=n,nn&h=n,nn,q,a,r,c
```

Which could return:

```console-result
n      nn       q a r    c
search node_1   3 1 0 1287
search node_2   0 2 0 1159
search node_3   0 1 0 1302
write  node_1 100 3 0 4259
write  node_2   0 4 0  980
write  node_3   1 5 0 8714
```
%  TEST[skip:illustrative response only]

Here you can see two significantly unique situations. Firstly, `node_1` has a severely backed up write queue compared to other nodes. Secondly, `node_3` shows historically completed writes that are double any other node. These are both probably due to either poorly distributed write-heavy indices, or to multiple write-heavy indices allocated to the same node. Since primary and replica writes are majorly the same amount of cluster work, we usually recommend setting [`index.routing.allocation.total_shards_per_node`](elasticsearch://reference/elasticsearch/index-settings/total-shards-per-node.md#total-shards-per-node) to force index spreading after lining up index shard counts to total nodes.

We normally recommend heavy-write indices have sufficient primary `number_of_shards` and replica `number_of_replicas` to evenly spread across indexing nodes. Alternatively, you can [reroute](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-reroute) shards to more quiet nodes to alleviate the nodes with write hot spotting.

If it’s non-obvious what indices are problematic, you can introspect further via [the index stats API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-indices-stats) by running:

```console
GET _stats?level=shards&human&expand_wildcards=all&filter_path=indices.*.total.indexing.index_total
```

For more advanced analysis, you can poll for shard-level stats, which lets you compare joint index-level and node-level stats. This analysis wouldn’t account for node restarts and/or shards rerouting, but serves as overview:

```console
GET _stats/indexing,search?level=shards&human&expand_wildcards=all
```

You can for example use the [third-party JQ tool](https://stedolan.github.io/jq), to process the output saved as `indices_stats.json`:

```sh
cat indices_stats.json | jq -rc ['.indices|to_entries[]|.key as $i|.value.shards|to_entries[]|.key as $s|.value[]|{node:.routing.node[:4], index:$i, shard:$s, primary:.routing.primary, size:.store.size, total_indexing:.indexing.index_total, time_indexing:.indexing.index_time_in_millis, total_query:.search.query_total, time_query:.search.query_time_in_millis } | .+{ avg_indexing: (if .total_indexing>0 then (.time_indexing/.total_indexing|round) else 0 end), avg_search: (if .total_search>0 then (.time_search/.total_search|round) else 0 end) }'] > shard_stats.json

# show top written-to shard simplified stats which contain their index and node references
cat shard_stats.json | jq -rc 'sort_by(-.avg_indexing)[]' | head
```


## Task loads [causes-tasks]

Shard distribution problems will most-likely surface as task load as seen above in the [cat thread pool](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-thread-pool) example. It is also possible for tasks to hot spot a node either due to individual qualitative expensiveness or overall quantitative traffic loads.

For example, if [cat thread pool](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-thread-pool) reported a high queue on the `warmer` [thread pool](elasticsearch://reference/elasticsearch/configuration-reference/thread-pool-settings.md), you would look-up the effected node’s [hot threads](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads). Let’s say it reported `warmer` threads at `100% cpu` related to `GlobalOrdinalsBuilder`. This would let you know to inspect [field data’s global ordinals](elasticsearch://reference/elasticsearch/mapping-reference/eager-global-ordinals.md).

Alternatively, let’s say [cat nodes](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-nodes) shows a hot spotted master node and [cat thread pool](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-thread-pool) shows general queuing across nodes. This would suggest the master node is overwhelmed. To resolve this, first ensure [hardware high availability](../../deploy-manage/production-guidance/availability-and-resilience/resilience-in-small-clusters.md) setup and then look to ephemeral causes. In this example, [the nodes hot threads API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-nodes-hot-threads) reports multiple threads in `other` which indicates they’re waiting on or blocked by either garbage collection or I/O.

For either of these example situations, a good way to confirm the problematic tasks is to look at longest running non-continuous (designated `[c]`) tasks via [cat task management](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-tasks). This can be supplemented checking longest running cluster sync tasks via [cat pending tasks](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cat-pending-tasks). Using a third example,

```console
GET _cat/tasks?v&s=time:desc&h=type,action,running_time,node,cancellable
```

This could return:

```console-result
type   action                running_time  node    cancellable
direct indices:data/read/eql 10m           node_1  true
...
```
%  TEST[skip:illustrative response only]

This surfaces a problematic [EQL query](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-search). We can gain further insight on it via [the task management API](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-tasks),

```console
GET _tasks?human&detailed
```

Its response contains a `description` that reports this query:

```eql
indices[winlogbeat-*,logs-window*], sequence by winlog.computer_name with maxspan=1m\n\n[authentication where host.os.type == "windows" and event.action:"logged-in" and\n event.outcome == "success" and process.name == "svchost.exe" ] by winlog.event_data.TargetLogonId
```

This lets you know which indices to check (`winlogbeat-*,logs-window*`), as well as the [EQL search](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-eql-search) request body. Most likely this is [SIEM related](/solutions/security.md). You can combine this with [audit logging](../../deploy-manage/monitor/logging-configuration/enabling-audit-logs.md) as needed to trace the request source.

