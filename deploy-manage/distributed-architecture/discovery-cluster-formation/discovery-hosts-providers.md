---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/discovery-hosts-providers.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Discovery [discovery-hosts-providers]

Discovery is the process by which the cluster formation module finds other nodes with which to form a cluster. This process runs when you start an {{es}} node or when a node believes the master node failed and continues until the master node is found or a new master node is elected.

This process starts with a list of *seed* addresses from one or more [seed hosts providers](#built-in-hosts-providers), together with the addresses of any master-eligible nodes that were in the last-known cluster. The process operates in two phases: First, each node probes the seed addresses by connecting to each address and attempting to identify the node to which it is connected and to verify that it is master-eligible. Secondly, if successful, it shares with the remote node a list of all of its known master-eligible peers and the remote node responds with *its* peers in turn. The node then probes all the new nodes that it just discovered, requests their peers, and so on.

If the node is not master-eligible then it continues this discovery process until it has discovered an elected master node. If no elected master is discovered then the node will retry after `discovery.find_peers_interval` which defaults to `1s`.

If the node is master-eligible then it continues this discovery process until it has either discovered an elected master node or else it has discovered enough masterless master-eligible nodes to complete an election. If neither of these occur quickly enough then the node will retry after `discovery.find_peers_interval` which defaults to `1s`.

Once a master is elected, it will normally remain as the elected master until it is deliberately stopped. It may also stop acting as the master if [fault detection](cluster-fault-detection.md) determines the cluster to be faulty. When a node stops being the elected master, it begins the discovery process again.

Refer to [Troubleshooting discovery](../../../troubleshoot/elasticsearch/discovery-troubleshooting.md) for troubleshooting issues with discovery.

## Seed hosts providers [built-in-hosts-providers]

By default the cluster formation module offers two seed hosts providers to configure the list of seed nodes: a *settings*-based and a *file*-based seed hosts provider. It can be extended to support cloud environments and other forms of seed hosts providers via [discovery plugins](elasticsearch://reference/elasticsearch-plugins/discovery-plugins.md). Seed hosts providers are configured using the `discovery.seed_providers` setting, which defaults to the *settings*-based hosts provider. This setting accepts a list of different providers, allowing you to make use of multiple ways to find the seed hosts for your cluster.

Each seed hosts provider yields the IP addresses or hostnames of the seed nodes. If it returns any hostnames then these are resolved to IP addresses using a DNS lookup. If a hostname resolves to multiple IP addresses then {{es}} tries to find a seed node at all of these addresses. If the hosts provider does not explicitly give the TCP port of the node by then, it will implicitly use the first port in the port range given by `transport.profiles.default.port`, or by `transport.port` if `transport.profiles.default.port` is not set. The number of concurrent lookups is controlled by `discovery.seed_resolver.max_concurrent_resolvers` which defaults to `10`, and the timeout for each lookup is controlled by `discovery.seed_resolver.timeout` which defaults to `5s`. Note that DNS lookups are subject to [JVM DNS caching](../../deploy/self-managed/networkaddress-cache-ttl.md).

#### Settings-based seed hosts provider [settings-based-hosts-provider]

The settings-based seed hosts provider uses a node setting to configure a static list of the addresses of the seed nodes. These addresses can be given as hostnames or IP addresses; hosts specified as hostnames are resolved to IP addresses during each round of discovery.

The list of hosts is set using the [`discovery.seed_hosts`](../../deploy/self-managed/important-settings-configuration.md#unicast.hosts) static setting. For example:

```yaml
discovery.seed_hosts:
   - 192.168.1.10:9300
   - 192.168.1.11 <1>
   - seeds.mydomain.com <2>
```

1. The port will default to `transport.profiles.default.port` and fallback to `transport.port` if not specified.
2. If a hostname resolves to multiple IP addresses, {{es}} will attempt to connect to every resolved address.

#### File-based seed hosts provider [file-based-hosts-provider]

The file-based seed hosts provider configures a list of hosts via an external file.  {{es}} reloads this file when it changes, so that the list of seed nodes can change dynamically without needing to restart each node. For example, this gives a convenient mechanism for an {{es}} instance that is run in a Docker container to be dynamically supplied with a list of IP addresses to connect to when those IP addresses may not be known at node startup.

To enable file-based discovery, configure the `file` hosts provider as follows in the [`elasticsearch.yml`](/deploy-manage/stack-settings.md) file:

```yaml
discovery.seed_providers: file
```

Then create a file at `$ES_PATH_CONF/unicast_hosts.txt` in the format described below. Any time a change is made to the `unicast_hosts.txt` file the new changes will be picked up by {{es}} and the new hosts list will be used.

Note that the file-based discovery plugin augments the unicast hosts list in [`elasticsearch.yml`](/deploy-manage/stack-settings.md): if there are valid seed addresses in `discovery.seed_hosts` then {{es}} uses those addresses in addition to those supplied in `unicast_hosts.txt`.

The `unicast_hosts.txt` file contains one node entry per line. Each node entry consists of the host (host name or IP address) and an optional transport port number. If the port number is specified, it must come immediately after the host (on the same line) separated by a `:`. If the port number is not specified, {{es}} will implicitly use the first port in the port range given by `transport.profiles.default.port`, or by `transport.port` if `transport.profiles.default.port` is not set.

For example, this is an example of `unicast_hosts.txt` for a cluster with four nodes that participate in discovery, some of which are not running on the default port:

```txt
10.10.10.5
10.10.10.6:9305
10.10.10.5:10005
# an IPv6 address
[2001:0db8:85a3:0000:0000:8a2e:0370:7334]:9301
```

Host names are allowed instead of IP addresses and are resolved by DNS as described above. IPv6 addresses must be given in brackets with the port, if needed, coming after the brackets.

You can also add comments to this file. All comments must appear on their lines starting with `#` (i.e. comments cannot start in the middle of a line).

#### EC2 hosts provider [ec2-hosts-provider]

The [EC2 discovery plugin](elasticsearch://reference/elasticsearch-plugins/discovery-ec2.md) adds a hosts provider that uses the [AWS API](https://github.com/aws/aws-sdk-java) to find a list of seed nodes.

#### Azure Classic hosts provider [azure-classic-hosts-provider]

The [Azure Classic discovery plugin](elasticsearch://reference/elasticsearch-plugins/discovery-azure-classic.md) adds a hosts provider that uses the Azure Classic API find a list of seed nodes.

#### Google Compute Engine hosts provider [gce-hosts-provider]

The [GCE discovery plugin](elasticsearch://reference/elasticsearch-plugins/discovery-gce.md) adds a hosts provider that uses the GCE API find a list of seed nodes.
