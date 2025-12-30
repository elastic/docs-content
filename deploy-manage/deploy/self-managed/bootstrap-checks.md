---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-xpack.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-heap-size.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-file-descriptor.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-memory-lock.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/max-number-threads-check.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-max-file-size.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/max-size-virtual-memory-check.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-max-map-count.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-client-jvm.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-serial-collector.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-syscall-filter.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-onerror.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-early-access.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-all-permission.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks-discovery-configuration.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Bootstrap checks [bootstrap-checks]

{{es}} has bootstrap checks that run at startup to ensure that users have configured all [important settings](/deploy-manage/deploy/self-managed/important-settings-configuration.md).

These bootstrap checks inspect a variety of {{es}} and system settings and compare them to values that are safe for the operation of {{es}}. If {{es}} is in development mode, any bootstrap checks that fail appear as warnings in the {{es}} log. If {{es}} is in production mode, any bootstrap checks that fail will cause {{es}} to refuse to start.

There are some bootstrap checks that are always enforced to prevent {{es}} from running with incompatible settings. These checks are documented individually.

## Development vs. production mode [dev-vs-prod-mode]

By default, {{es}} binds to loopback addresses for [HTTP and transport (internal) communication](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md). This is fine for downloading and playing with {{es}} as well as everyday development, but it’s useless for production systems. To join a cluster, an {{es}} node must be reachable via transport communication. To join a cluster via a non-loopback address, a node must bind transport to a non-loopback address and not be using [single-node discovery](/deploy-manage/deploy/self-managed/bootstrap-checks.md#single-node-discovery). Thus, we consider an {{es}} node to be in development mode if it can not form a cluster with another machine via a non-loopback address, and is otherwise in production mode if it can join a cluster via non-loopback addresses.

Note that HTTP and transport can be configured independently via [`http.host`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#http-settings) and [`transport.host`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#transport-settings). This can be useful for configuring a single node to be reachable via HTTP for testing purposes without triggering production mode.


## Single-node discovery [single-node-discovery]

Some users need to bind the transport to an external interface for testing a remote-cluster configuration. For this situation, we provide the discovery type `single-node`. To enable it, set `discovery.type` to `single-node`. In this situation, a node will elect itself master, and will not join a cluster with any other node.


## Forcing the bootstrap checks [_forcing_the_bootstrap_checks]

If you are running a single node in production, it is possible to evade the bootstrap checks, either by not binding transport to an external interface, or by binding transport to an external interface and setting the discovery type to `single-node`. For this situation, you can force execution of the bootstrap checks by setting the system property `es.enforce.bootstrap.checks` to `true` in the [JVM options](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-options). We strongly encourage you to do this if you are in this specific situation. This system property can be used to force execution of the bootstrap checks independent of the node configuration.

## Checks

:::{dropdown} Heap size check

$$$heap-size$$$

By default, {{es}} automatically sizes JVM heap based on a node’s [roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles) and total memory. If you manually override the default sizing and start the JVM with different initial and max heap sizes, the JVM may pause as it resizes the heap during system usage. If you enable [`bootstrap.memory_lock`](setup-configuration-memory.md#bootstrap-memory_lock), the JVM locks the initial heap size on startup. If the initial heap size is not equal to the maximum heap size, some JVM heap may not be locked after a resize.

To avoid these issues, start the JVM with an initial heap size equal to the maximum heap size.
:::

:::{dropdown} File descriptor check

$$$bootstrap-checks-file-descriptor$$$

File descriptors are a Unix construct for tracking open "files". In Unix though, [everything is a file](https://en.wikipedia.org/wiki/Everything_is_a_file). For example, "files" could be a physical file, a virtual file (e.g., `/proc/loadavg`), or network sockets. {{es}} requires lots of file descriptors (e.g., every shard is composed of multiple segments and other files, plus connections to other nodes, etc.). This bootstrap check is enforced on OS X and Linux.

To pass the file descriptor check, you might have to configure [file descriptors](file-descriptors.md).
:::

:::{dropdown} Memory lock check

$$$bootstrap-checks-memory-lock$$$

When the JVM does a major garbage collection it touches every page of the heap. If any of those pages are swapped out to disk they will have to be swapped back in to memory. That causes lots of disk thrashing that {{es}} would much rather use to service requests. There are several ways to configure a system to disallow swapping. One way is by requesting the JVM to lock the heap in memory through `mlockall` (Unix) or virtual lock (Windows). This is done via the {{es}} setting [`bootstrap.memory_lock`](setup-configuration-memory.md#bootstrap-memory_lock). However, there are cases where this setting can be passed to {{es}} but {{es}} is not able to lock the heap (e.g., if the `elasticsearch` user does not have `memlock unlimited`). The memory lock check verifies that **if** the `bootstrap.memory_lock` setting is enabled, that the JVM was successfully able to lock the heap.

To pass the memory lock check, you might have to configure [`bootstrap.memory_lock`](setup-configuration-memory.md#bootstrap-memory_lock).
:::

:::{dropdown} Maximum number of threads check

$$$max-number-threads-check$$$

{{es}} executes requests by breaking the request down into stages and handing those stages off to different thread pool executors. There are different [thread pool executors](elasticsearch://reference/elasticsearch/configuration-reference/thread-pool-settings.md) for a variety of tasks within {{es}}. Thus, {{es}} needs the ability to create a lot of threads. The maximum number of threads check ensures that the {{es}} process has the rights to create enough threads under normal use. This check is enforced only on Linux.

If you are on Linux, to pass the maximum number of threads check, you must configure your system to allow the {{es}} process the ability to create at least 4096 threads. This can be done via `/etc/security/limits.conf` using the `nproc` setting (note that you might have to increase the limits for the `root` user too).
:::

:::{dropdown} Max file size check

$$$bootstrap-checks-max-file-size$$$

The segment files that are the components of individual shards and the translog generations that are components of the translog can get large (exceeding multiple gigabytes). On systems where the max size of files that can be created by the {{es}} process is limited, this can lead to failed writes. Therefore, the safest option here is that the max file size is unlimited and that is what the max file size bootstrap check enforces.

To pass the max file check, you must configure your system to allow the {{es}} process the ability to write files of unlimited size. This can be done via `/etc/security/limits.conf` using the `fsize` setting to `unlimited` (note that you might have to increase the limits for the `root` user too).
:::

:::{dropdown} Maximum size virtual memory check

$$$max-size-virtual-memory-check$$$

{{es}} and Lucene use `mmap` to great effect to map portions of an index into the {{es}} address space. This keeps certain index data off the JVM heap but in memory for blazing fast access. For this to be effective, the {{es}} should have unlimited address space. The maximum size virtual memory check enforces that the {{es}} process has unlimited address space and is enforced only on Linux.

To pass the maximum size virtual memory check, you must configure your system to allow the {{es}} process the ability to have unlimited address space. This can be done via adding `<user> - as unlimited` to `/etc/security/limits.conf`. This may require you to increase the limits for the `root` user too.
:::

:::{dropdown} Maximum map count check

$$$bootstrap-checks-max-map-count$$$

In addition to [unlimited address space](#max-size-virtual-memory-check), to use `mmap` effectively, {{es}} also requires the ability to create many memory-mapped areas. The maximum map count check checks that the kernel allows a process to have at least 262,144 memory-mapped areas and is enforced on Linux only.

To pass the maximum map count check, you must configure `vm.max_map_count` via `sysctl` to be at least `262144`. The recommended value is `1048576`.

Alternatively, the maximum map count check is only needed if you are using `mmapfs` or `hybridfs` as the [store type](elasticsearch://reference/elasticsearch/index-settings/store.md) for your indices. If you [do not allow](elasticsearch://reference/elasticsearch/index-settings/store.md#allow-mmap) the use of `mmap` then this bootstrap check will not be enforced.
:::

:::{dropdown} Client JVM check

$$$bootstrap-checks-client-jvm$$$

There are two different JVMs provided by OpenJDK-derived JVMs: the client JVM and the server JVM. These JVMs use different compilers for producing executable machine code from Java bytecode. The client JVM is tuned for startup time and memory footprint while the server JVM is tuned for maximizing performance. The difference in performance between the two VMs can be substantial. The client JVM check ensures that {{es}} is not running inside the client JVM.

To pass the client JVM check, you must start {{es}} with the server VM. On modern systems and operating systems, the server VM is the default.
:::

:::{dropdown} Use serial collector check

$$$bootstrap-checks-serial-collector$$$

There are various garbage collectors for the OpenJDK-derived JVMs targeting different workloads. The serial collector in particular is best suited for single logical CPU machines or extremely small heaps, neither of which are suitable for running {{es}}. Using the serial collector with {{es}} can be devastating for performance. The serial collector check ensures that {{es}} is not configured to run with the serial collector.

To pass the serial collector check, you must not start {{es}} with the serial collector (whether it’s from the defaults for the JVM that you’re using, or you’ve explicitly specified it with `-XX:+UseSerialGC`). Note that the default JVM configuration that ships with {{es}} configures {{es}} to use the G1GC garbage collector with JDK14 and later versions. For earlier JDK versions, the configuration defaults to the CMS collector.
:::

:::{dropdown} System call filter check

$$$bootstrap-checks-syscall-filter$$$

{{es}} installs system call filters of various flavors depending on the operating system (e.g., seccomp on Linux). These system call filters are installed to prevent the ability to execute system calls related to forking as a defense mechanism against arbitrary code execution attacks on {{es}}. The system call filter check ensures that if system call filters are enabled, then they were successfully installed.

To pass the system call filter check you must fix any configuration errors on your system that prevented system call filters from installing (check your logs).
:::

:::{dropdown} OnError and OnOutOfMemoryError checks

$$$bootstrap-checks-onerror$$$

The JVM options `OnError` and `OnOutOfMemoryError` enable executing arbitrary commands if the JVM encounters a fatal error (`OnError`) or an `OutOfMemoryError` (`OnOutOfMemoryError`). However, by default, {{es}} system call filters (seccomp) are enabled and these filters prevent forking. Thus, using `OnError` or `OnOutOfMemoryError` and system call filters are incompatible. The `OnError` and `OnOutOfMemoryError` checks prevent {{es}} from starting if either of these JVM options are used and system call filters are enabled. This check is always enforced.

To pass this check, do not enable `OnError` nor `OnOutOfMemoryError`; instead, upgrade to Java 8u92 and use the JVM flag `ExitOnOutOfMemoryError`. While this does not have the full capabilities of `OnError` nor `OnOutOfMemoryError`, arbitrary forking will not be supported with seccomp enabled.
:::

:::{dropdown} Early-access check

$$$bootstrap-checks-early-access$$$

The OpenJDK project provides early-access snapshots of upcoming releases. These releases are not suitable for production. The early-access check detects these early-access snapshots.

To pass this check, you must start {{es}} on a release build of the JVM.
:::

:::{dropdown} All permission check

$$$bootstrap-checks-all-permission$$$

The all permission check ensures that the security policy used during bootstrap does not grant the `java.security.AllPermission` to {{es}}. Running with the all permission granted is equivalent to disabling the security manager.
:::

:::{dropdown} Discovery configuration check

$$$bootstrap-checks-discovery-configuration$$$

By default, when {{es}} first starts up it will try and discover other nodes running on the same host. If no elected master can be discovered within a few seconds then {{es}} will form a cluster that includes any other nodes that were discovered. It is useful to be able to form this cluster without any extra configuration in development mode, but this is unsuitable for production because it’s possible to form multiple clusters and lose data as a result.

This bootstrap check ensures that discovery is not running with the default configuration. It can be satisfied by setting at least one of the following properties:

* `discovery.seed_hosts`
* `discovery.seed_providers`
* `cluster.initial_master_nodes`

Note that you must [remove `cluster.initial_master_nodes` from the configuration of every node](/deploy-manage/deploy/self-managed/important-settings-configuration.md#initial_master_nodes) after the cluster has started for the first time. Instead, configure `discovery.seed_hosts` or `discovery.seed_providers`. If you do not need any discovery configuration, for instance if running a single-node cluster, set `discovery.seed_hosts: []` to disable discovery and satisfy this bootstrap check.
:::

:::{dropdown} Encrypt sensitive data check

$$$bootstrap-checks-xpack-encrypt-sensitive-data$$$

If you use {{watcher}} and have chosen to encrypt sensitive data (by setting `xpack.watcher.encrypt_sensitive_data` to `true`), you must also place a key in the secure settings store.

To pass this bootstrap check, you must set the `xpack.watcher.encryption_key` on each node in the cluster. For more information, see [Encrypting sensitive data in Watcher](../../../explore-analyze/alerts-cases/watcher/encrypting-data.md).
:::

:::{dropdown} PKI realm check

$$$bootstrap-checks-xpack-pki-realm$$$

If you use {{es}} {{security-features}} and a Public Key Infrastructure (PKI) realm, you must configure Transport Layer Security (TLS) on your cluster and enable client authentication on the network layers (either transport or http). For more information, see [PKI user authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/pki.md) and [Set up basic security plus HTTPS](/deploy-manage/security/set-up-basic-security-plus-https.md).

To pass this bootstrap check, if a PKI realm is enabled, you must configure TLS and enable client authentication on at least one network communication layer.
:::

:::{dropdown} Role mappings check

$$$bootstrap-checks-xpack-role-mappings$$$

If you authenticate users with realms other than `native` or `file` realms, you must create role mappings. These role mappings define which roles are assigned to each user.

If you use files to manage the role mappings, you must configure a YAML file and copy it to each node in the cluster. By default, role mappings are stored in `ES_PATH_CONF/role_mapping.yml`. Alternatively, you can specify a different role mapping file for each type of realm and specify its location in the [`elasticsearch.yml`](/deploy-manage/deploy/self-managed/configure-elasticsearch.md) file. For more information, see [Using role mapping files](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-file).

To pass this bootstrap check, the role mapping files must exist and must be valid. The Distinguished Names (DNs) that are listed in the role mappings files must also be valid.
:::

::::{dropdown} SSL/TLS check

$$$bootstrap-checks-tls$$$

If you enable {{es}} {{security-features}}, unless you have a trial license, you must configure SSL/TLS for internode-communication.

:::{note}
Single-node clusters that use a loopback interface do not have this requirement. For more information, see [*Start the {{stack}} with security enabled automatically*](/deploy-manage/security/self-auto-setup.md).
:::

To pass this bootstrap check, you must [set up SSL/TLS in your cluster](/deploy-manage/security/set-up-basic-security.md#encrypt-internode-communication).
::::

:::{dropdown} Token SSL check

$$$bootstrap-checks-xpack-token-ssl$$$

If you use {{es}} {{security-features}} and the built-in token service is enabled, you must configure your cluster to use SSL/TLS for the HTTP interface. HTTPS is required in order to use the token service.

In particular, if `xpack.security.authc.token.enabled` is set to `true` in the [`elasticsearch.yml`](/deploy-manage/deploy/self-managed/configure-elasticsearch.md) file, you must also set `xpack.security.http.ssl.enabled` to `true`. For more information about these settings, see [Security settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md) and [Advanced HTTP settings](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#http-settings).

To pass this bootstrap check, you must enable HTTPS or disable the built-in token service.

