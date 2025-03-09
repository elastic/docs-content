---
navigation_title: Master node not discovered
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/master-node-not-discovered.html
---

# Master node not discovered [master-node-not-discovered]

An Elasticsearch cluster requires a master node to be identified in the cluster in order for it to start properly. Furthermore, the election of the master node requires that there be a quorum of 50% and one of the nodes must have voting rights. If the cluster lacks a quorum, it will not start. Misconfiguration of the cluster can lead to "split-brain" situations where the cluster is split into multiple clusters, each with their own master nodes.

For more information on properly bootstrapping a cluster, see [this guide](/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-bootstrap-cluster).

## Possible causes

### Incorrect discovery settings

If you are getting this warning in the logs:
```
Master node not discovered yet this node has not previously joined a bootstrapped cluster
```
Then the most likely explanation is that you have incorrect settings in elasticsearch.yml, which prevent the node from correctly discovering its peer nodes.

```
discovery.seed_hosts:
   - 192.168.1.1:9300
   - 192.168.1.2 
   - nodes.mycluster.com
```
The discovery seed hosts should contain a list of nodes in the cluster (of which at least one must be available the first time the node joins the cluster) in order for the discovery function to work.

If it is the first time the cluster has started, then the following setting is also important:
```
cluster.initial_master_nodes:
  - master-node-name1
  - master-node-name2
  - master-node-name3
```
Note that here the settings are the node names (not IP addresses) of eligible master nodes that have the setting:
```
node.master: true 
```

Be sure to remove cluster.initial_master_nodes from elasticsearch.yml after the initial cluster bootstrapping has finished.

See [this guide](/deploy-manage/distributed-architecture/discovery-cluster-formation/discovery-hosts-providers) for more information correctly configuring the discovery settings.

### Master not elected
If you see the message:
```
master not discovered or elected yet, an election requires at least 2 nodes with ids from [UIDIdndidisz99dkhslihn, xkenktjsiasnKKKhdb s, YZ6m2ioDQWqi1cNnOteB6w]
```
This suggests that a number of master nodes previously existed in the cluster, but insufficient master nodes are now available. The likely cause is that master nodes have been removed from the cluster and so a quorum has not been reached to elect a new master node. If you have recently stopped master nodes, then you will need to add them back, or wait for Elasticsearch to adjust the quorum down to the actual number of master nodes available.

See [this guide](/deploy-manage/distributed-architecture/discovery-cluster-formation/modules-discovery-quorums) for more information on this.

### Node stability issues
If the master nodes also have the data node role, and are under stress due to heavy indexing or searching, then this can cause them to become unavailable, which in turn can affect the capacity of the cluster to elect a new master. In clusters that are subject to heavy indexing or search demand, it is recommended to create [dedicated master nodes](/deploy-manage/distributed-architecture/clusters-nodes-shards/node-roles#dedicated-master-node)

If you have other applications running on the same machines as your master nodes, then it is possible that these processes can leave the master node with insufficient resources to carry out its job, which will result in cluster instability.  

In particular if you are running your cluster using containerization technologies such as Docker or Kubernetes, ensure that your master nodes are guaranteed sufficient resources to be able to do their job and are not destabilized by other processes running on the host machines where the master nodes are running.


