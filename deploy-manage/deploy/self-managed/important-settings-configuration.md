---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/important-settings.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/networkaddress-cache-ttl.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Important settings configuration [important-settings]

{{es}} requires very little configuration to get started, but there are a number of items which **must** be considered before using your cluster in production:

* [Path settings](#path-settings)
* [Cluster name setting](#_cluster_name_setting)
* [Node name setting](#node-name)
* [Network host settings](#network.host)
* [Discovery settings](#discovery-settings)
* [Heap size settings](#heap-size-settings)
* [JVM heap dump path setting](#heap-dump-path)
* [GC logging settings](#_gc_logging_settings)
* [Temporary directory settings](#es-tmpdir)
* [JVM fatal error log setting](#_jvm_fatal_error_log_setting)
* [Cluster backups](#important-settings-backups)
* [DNS cache settings](#networkaddress-cache-ttl)

## Path settings [path-settings]

{{es}} writes the data you index to indices and data streams to a `data` directory. {{es}} writes its own application logs, which contain information about cluster health and operations, to a `logs` directory.

For [macOS `.tar.gz`](install-elasticsearch-from-archive-on-linux-macos.md), [Linux `.tar.gz`](install-elasticsearch-from-archive-on-linux-macos.md), and [Windows `.zip`](install-elasticsearch-with-zip-on-windows.md) installations, `data` and `logs` are subdirectories of `$ES_HOME` by default. However, files in `$ES_HOME` risk deletion during an upgrade.

In production, we strongly recommend you set the `path.data` and `path.logs` in [`elasticsearch.yml`](/deploy-manage/deploy/self-managed/configure-elasticsearch.md) to locations outside of `$ES_HOME`. [Docker](install-elasticsearch-with-docker.md), [Debian](install-elasticsearch-with-debian-package.md), and [RPM](install-elasticsearch-with-rpm.md) installations write data and log to locations outside of `$ES_HOME` by default.

Supported `path.data` and `path.logs` values vary by platform:

:::::::{tab-set}

::::::{tab-item} Unix-like systems
Linux and macOS installations support Unix-style paths:

```yaml
path:
  data: /var/data/elasticsearch
  logs: /var/log/elasticsearch
```
::::::

::::::{tab-item} Windows
Windows installations support DOS paths with escaped backslashes:

```yaml
path:
  data: "C:\\Elastic\\Elasticsearch\\data"
  logs: "C:\\Elastic\\Elasticsearch\\logs"
```
::::::
:::::::

{{es}} offers a deprecated setting that allows you to specify multiple paths in `path.data`. To learn about this setting, and how to migrate away from it, refer to [Multiple data paths](elasticsearch://reference/elasticsearch/index-settings/path.md#multiple-data-paths).

::::{warning}
* Don’t modify anything within the data directory or run processes that might interfere with its contents.

  If something other than {{es}} modifies the contents of the data directory, then {{es}} may fail, reporting corruption or other data inconsistencies, or may appear to work correctly having silently lost some of your data.
* Don’t attempt to take filesystem backups of the data directory; there is no supported way to restore such a backup. Instead, use [Snapshot and restore](../../tools/snapshot-and-restore.md) to take backups safely.
* Don’t run virus scanners on the data directory. A virus scanner can prevent {{es}} from working correctly and may modify the contents of the data directory. The data directory contains no executables so a virus scan will only find false positives.
::::


## Cluster name setting [_cluster_name_setting]

A node can only join a cluster when it shares its `cluster.name` with all the other nodes in the cluster. The default name is `elasticsearch`, but you should change it to an appropriate name that describes the purpose of the cluster.

```yaml
cluster.name: logging-prod
```

::::{important}
Do not reuse the same cluster names in different environments. Otherwise, nodes might join the wrong cluster.
::::


::::{note}
Changing the name of a cluster requires a [full cluster restart](../../maintenance/start-stop-services/full-cluster-restart-rolling-restart-procedures.md#restart-cluster-full).
::::



## Node name setting [node-name]

{{es}} uses `node.name` as a human-readable identifier for a particular instance of {{es}}. This name is included in the response of many APIs. The node name defaults to the hostname of the machine when {{es}} starts, but can be configured explicitly in [`elasticsearch.yml`](/deploy-manage/deploy/self-managed/configure-elasticsearch.md):

```yaml
node.name: prod-data-2
```


## Network host setting [network.host]

By default, {{es}} only binds to loopback addresses such as `127.0.0.1` and `[::1]`. This is sufficient to run a cluster of one or more nodes on a single server for development and testing, but a [resilient production cluster](../../production-guidance/availability-and-resilience.md) must involve nodes on other servers. There are many [network settings](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) but usually all you need to configure is `network.host`:

```yaml
network.host: 192.168.1.10
```

::::{important}
When you provide a value for `network.host`, {{es}} assumes that you are moving from development mode to production mode, and upgrades a number of system startup checks from warnings to exceptions. See the differences between [development and production modes](important-system-configuration.md#dev-vs-prod).
::::



## Discovery and cluster formation settings [discovery-settings]

Configure two important discovery and cluster formation settings before going to production so that nodes in the cluster can [discover](/deploy-manage/distributed-architecture/discovery-cluster-formation/discovery-hosts-providers.md) each other and elect a master node.


### `discovery.seed_hosts` [unicast.hosts]

Out of the box, without any network configuration, {{es}} will bind to the available loopback addresses and scan local ports `9300` to `9305` to connect with other nodes running on the same server. This behavior provides an auto-clustering experience without having to do any configuration.

When you want to form a cluster with nodes on other hosts, use the [static](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#static-cluster-setting) `discovery.seed_hosts` setting. This setting provides a list of other nodes in the cluster that are master-eligible and likely to be live and contactable to seed the [discovery process](/deploy-manage/distributed-architecture/discovery-cluster-formation/discovery-hosts-providers.md). This setting accepts a YAML sequence or array of the addresses of all the master-eligible nodes in the cluster. Each address can be either an IP address or a hostname that resolves to one or more IP addresses via DNS.

```yaml
discovery.seed_hosts:
   - 192.168.1.10:9300
   - 192.168.1.11 <1>
   - seeds.mydomain.com <2>
   - [0:0:0:0:0:ffff:c0a8:10c]:9301 <3>
```

1. The port is optional and defaults to `9300`, but can be [overridden](../../distributed-architecture/discovery-cluster-formation/discovery-hosts-providers.md#built-in-hosts-providers).
2. If a hostname resolves to multiple IP addresses, the node will attempt to discover other nodes at all resolved addresses.
3. IPv6 addresses must be enclosed in square brackets.


If your master-eligible nodes do not have fixed names or addresses, use an [alternative hosts provider](../../distributed-architecture/discovery-cluster-formation/discovery-hosts-providers.md#built-in-hosts-providers) to find their addresses dynamically.


### `cluster.initial_master_nodes` [initial_master_nodes]

When you start an {{es}} cluster for the first time, a [cluster bootstrapping](../../distributed-architecture/discovery-cluster-formation/modules-discovery-bootstrap-cluster.md) step determines the set of master-eligible nodes whose votes are counted in the first election. In [development mode](/deploy-manage/deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode), with no discovery settings configured, this step is performed automatically by the nodes themselves.

Because auto-bootstrapping is [inherently unsafe](../../distributed-architecture/discovery-cluster-formation/modules-discovery-quorums.md), when starting a new cluster in production mode, you must explicitly list the master-eligible nodes whose votes should be counted in the very first election. You set this list using the `cluster.initial_master_nodes` setting on every master-eligible node. Do not configure this setting on master-ineligible nodes.

::::{important}
After the cluster forms successfully for the first time, remove the `cluster.initial_master_nodes` setting from each node’s configuration and never set it again for this cluster. Do not configure this setting on nodes joining an existing cluster. Do not configure this setting on nodes which are restarting. Do not configure this setting when performing a full-cluster restart. See [Bootstrapping a cluster](../../distributed-architecture/discovery-cluster-formation/modules-discovery-bootstrap-cluster.md).
::::


```yaml
discovery.seed_hosts:
   - 192.168.1.10:9300
   - 192.168.1.11
   - seeds.mydomain.com
   - [0:0:0:0:0:ffff:c0a8:10c]:9301
cluster.initial_master_nodes: <1>
   - master-node-a
   - master-node-b
   - master-node-c
```

1. Identify the initial master nodes by their [`node.name`](#node-name), which defaults to their hostname. Ensure that the value in `cluster.initial_master_nodes` matches the `node.name` exactly. If you use a fully-qualified domain name (FQDN) such as `master-node-a.example.com` for your node names, then you must use the FQDN in this list. Conversely, if `node.name` is a bare hostname without any trailing qualifiers, you must also omit the trailing qualifiers in `cluster.initial_master_nodes`.


See [bootstrapping a cluster](../../distributed-architecture/discovery-cluster-formation/modules-discovery-bootstrap-cluster.md) and [discovery and cluster formation settings](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md).


## Heap size settings [heap-size-settings]

By default, {{es}} automatically sets the JVM heap size based on a node’s [roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles) and total memory. We recommend the default sizing for most production environments.

If needed, you can override the default sizing by manually [setting the JVM heap size](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-heap-size).


## JVM heap dump path setting [heap-dump-path]

By default, {{es}} configures the JVM to dump the heap on out of memory exceptions to the default data directory. On [RPM](install-elasticsearch-with-rpm.md) and [Debian](install-elasticsearch-with-debian-package.md) packages, the data directory is `/var/lib/elasticsearch`. On [Linux and MacOS](install-elasticsearch-from-archive-on-linux-macos.md) and [Windows](install-elasticsearch-with-zip-on-windows.md) distributions, the `data` directory is located under the root of the {{es}} installation.

If this path is not suitable for receiving heap dumps, modify the `-XX:HeapDumpPath=...` entry in [`jvm.options`](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-options):

* If you specify a directory, the JVM will generate a filename for the heap dump based on the PID of the running instance.
* If you specify a fixed filename instead of a directory, the file must not exist when the JVM needs to perform a heap dump on an out of memory exception. Otherwise, the heap dump will fail.


## GC logging settings [_gc_logging_settings]

By default, {{es}} enables garbage collection (GC) logs. These are configured in [`jvm.options`](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-options) and output to the same default location as the {{es}} logs. The default configuration rotates the logs every 64 MB and can consume up to 2 GB of disk space.

You can reconfigure JVM logging using the command line options described in [JEP 158: Unified JVM Logging](https://openjdk.java.net/jeps/158). Unless you change the default `jvm.options` file directly, the {{es}} default configuration is applied in addition to your own settings. To disable the default configuration, first disable logging by supplying the `-Xlog:disable` option, then supply your own command line options. This disables *all* JVM logging, so be sure to review the available options and enable everything that you require.

To see further options not contained in the original JEP, see [Enable Logging with the JVM Unified Logging Framework](https://docs.oracle.com/en/java/javase/13/docs/specs/man/java.html#enable-logging-with-the-jvm-unified-logging-framework).


### Examples [_examples]

Change the default GC log output location to `/opt/my-app/gc.log` by creating `$ES_HOME/config/jvm.options.d/gc.options` with some sample options:

```sh
# Turn off all previous logging configuratons
-Xlog:disable

# Default settings from JEP 158, but with `utctime` instead of `uptime` to match the next line
-Xlog:all=warning:stderr:utctime,level,tags

# Enable GC logging to a custom location with a variety of options
-Xlog:gc*,gc+age=trace,safepoint:file=/opt/my-app/gc.log:utctime,level,pid,tags:filecount=32,filesize=64m
```

Configure an {{es}} [Docker container](install-elasticsearch-with-docker.md) to send GC debug logs to standard error (`stderr`). This lets the container orchestrator handle the output. If using the `ES_JAVA_OPTS` environment variable, specify:

```sh
MY_OPTS="-Xlog:disable -Xlog:all=warning:stderr:utctime,level,tags -Xlog:gc=debug:stderr:utctime"
docker run -e ES_JAVA_OPTS="$MY_OPTS" # etc
```


## Temporary directory settings [es-tmpdir]

By default, {{es}} uses a private temporary directory that the startup script creates immediately below the system temporary directory.

On some Linux distributions, a system utility will clean files and directories from `/tmp` if they have not been recently accessed. This behavior can lead to the private temporary directory being removed while {{es}} is running if features that require the temporary directory are not used for a long time. Removing the private temporary directory causes problems if a feature that requires this directory is subsequently used.

If you install {{es}} using the `.deb` or `.rpm` packages and run it under `systemd`, the private temporary directory that {{es}} uses is excluded from periodic cleanup.

If you intend to run the `.tar.gz` distribution on Linux or MacOS for an extended period, consider creating a dedicated temporary directory for {{es}} that is not under a path that will have old files and directories cleaned from it. This directory should have permissions set so that only the user that {{es}} runs as can access it. Then, set the `$ES_TMPDIR` environment variable to point to this directory before starting {{es}}.


## JVM fatal error log setting [_jvm_fatal_error_log_setting]

By default, {{es}} configures the JVM to write fatal error logs to the default logging directory. On [RPM](install-elasticsearch-with-rpm.md) and [Debian](install-elasticsearch-with-debian-package.md) packages, this directory is `/var/log/elasticsearch`. On [Linux and MacOS](install-elasticsearch-from-archive-on-linux-macos.md) and [Windows](install-elasticsearch-with-zip-on-windows.md) distributions, the `logs` directory is located under the root of the {{es}} installation.

These are logs produced by the JVM when it encounters a fatal error, such as a segmentation fault. If this path is not suitable for receiving logs, modify the `-XX:ErrorFile=...` entry in [`jvm.options`](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-options).


## Cluster backups [important-settings-backups]

In a disaster, [snapshots](../../tools/snapshot-and-restore.md) can prevent permanent data loss. [{{slm-cap}}](../../tools/snapshot-and-restore/create-snapshots.md#automate-snapshots-slm) is the easiest way to take regular backups of your cluster. For more information, see [](../../tools/snapshot-and-restore/create-snapshots.md).

::::{warning}
**Taking a snapshot is the only reliable and supported way to back up a cluster.** You cannot back up an {{es}} cluster by making copies of the data directories of its nodes. There are no supported methods to restore any data from a file system-level backup. If you try to restore a cluster from such a backup, it may fail with reports of corruption or missing files or other data inconsistencies, or it may appear to have succeeded having silently lost some of your data.

::::

## DNS cache settings [networkaddress-cache-ttl]

{{es}} runs with a security manager in place. With a security manager in place, the JVM defaults to caching positive hostname resolutions indefinitely and defaults to caching negative hostname resolutions for ten seconds. {{es}} overrides this behavior with default values to cache positive lookups for sixty seconds, and to cache negative lookups for ten seconds. These values should be suitable for most environments, including environments where DNS resolutions vary with time. If not, you can edit the values `es.networkaddress.cache.ttl` and `es.networkaddress.cache.negative.ttl` in the [JVM options](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-options). Note that the values [`networkaddress.cache.ttl=<timeout>`](https://docs.oracle.com/javase/8/docs/technotes/guides/net/properties.md) and [`networkaddress.cache.negative.ttl=<timeout>`](https://docs.oracle.com/javase/8/docs/technotes/guides/net/properties.md) in the [Java security policy](https://docs.oracle.com/javase/8/docs/technotes/guides/security/PolicyFiles.md) are ignored by {{es}} unless you remove the settings for `es.networkaddress.cache.ttl` and `es.networkaddress.cache.negative.ttl`.
