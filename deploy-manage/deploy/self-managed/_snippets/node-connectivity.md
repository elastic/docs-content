% RPM and Debian only

When {{es}} starts for the first time, the security auto-configuration process binds the HTTP layer to `0.0.0.0`, but only binds the transport layer to `localhost`. This intended behavior ensures that you can start a single-node cluster with security enabled by default without any additional configuration.

Before enrolling a new node, additional actions such as binding to an address other than `localhost` or satisfying bootstrap checks are typically necessary in production clusters. During that time, an auto-generated enrollment token could expire, which is why enrollment tokens aren’t generated automatically.

Only nodes on the same host can join the cluster without additional configuration. If you want nodes from another host to join your cluster, you need make your instance reachable. 

* If you're installing the first node in a multi-node cluster across multiple hosts, then you need to [configure the node so that other hosts are able to connect to it](#first-node).

* If you're installing additional nodes for a cluster, then you need to [generate an enrollment token and then reconfigure the new node to join an existing cluster](#existing-cluster).

If you're running a single-node cluster, then skip to the next step.

For more information about the cluster formation process, refer to [](/deploy-manage/distributed-architecture/discovery-cluster-formation.md).