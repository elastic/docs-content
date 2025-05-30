---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-configuration-memory.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Disable swapping [setup-configuration-memory]

Most operating systems try to use as much memory as possible for file system caches and eagerly swap out unused application memory. This can result in parts of the JVM heap or even its executable pages being swapped out to disk.

Swapping is very bad for performance, for node stability, and should be avoided at all costs. It can cause garbage collections to last for minutes instead of milliseconds and can cause nodes to respond slowly or even to disconnect from the cluster. In a resilient distributed system, it’s more effective to let the operating system kill the node.

There are three approaches to disabling swapping. The preferred option is to completely disable swap. If this is not an option, whether or not to prefer minimizing swappiness versus memory locking is dependent on your environment.

## Disable all swap files [disable-swap-files]

Usually {{es}} is the only service running on a box, and its memory usage is controlled by the JVM options. There should be no need to have swap enabled.

On Linux systems, you can disable swap temporarily by running:

```sh
sudo swapoff -a
```

This doesn’t require a restart of {{es}}.

To disable it permanently, you will need to edit the `/etc/fstab` file and comment out any lines that contain the word `swap`.

On Windows, the equivalent can be achieved by disabling the paging file entirely via `System Properties → Advanced → Performance → Advanced → Virtual memory`.


## Configure `swappiness` [swappiness]

Another option available on Linux systems is to ensure that the sysctl value `vm.swappiness` is set to `1`. This reduces the kernel’s tendency to swap and should not lead to swapping under normal circumstances, while still allowing the whole system to swap in emergency conditions.


## Enable `bootstrap.memory_lock` [bootstrap-memory_lock]

Another option is to use [mlockall](http://opengroup.org/onlinepubs/007908799/xsh/mlockall.md) on Linux/Unix systems, or [VirtualLock](https://msdn.microsoft.com/en-us/library/windows/desktop/aa366895%28v=vs.85%29.aspx) on Windows, to try to lock the process address space into RAM, preventing any {{es}} heap memory from being swapped out.

::::{note}
Some platforms still swap off-heap memory when using a memory lock. To prevent off-heap memory swaps, [disable all swap files](#disable-swap-files) instead.
::::


To enable a memory lock, set `bootstrap.memory_lock` to `true` in [`elasticsearch.yml`](/deploy-manage/deploy/self-managed/configure-elasticsearch.md):

```yaml
bootstrap.memory_lock: true
```

::::{warning}
`mlockall` might cause the JVM or shell session to exit if it tries to allocate more memory than is available.
::::


After starting {{es}}, you can see whether this setting was applied successfully by checking the value of `mlockall` in the output from this request:

```console
GET _nodes?filter_path=**.mlockall
```

If you see that `mlockall` is `false`, then it means that the `mlockall` request has failed. You will also see a line with more information in the logs with the words `Unable to lock JVM Memory`.

The most probable reason, on Linux/Unix systems, is that the user running {{es}} doesn’t have permission to lock memory. This can be granted as follows:

`.zip` and `.tar.gz`
:   Set [`ulimit -l unlimited`](setting-system-settings.md#ulimit) as root before starting {{es}}. Alternatively, set `memlock` to `unlimited` in `/etc/security/limits.conf`:

    ```sh
    # allow user 'elasticsearch' mlockall
    elasticsearch soft memlock unlimited
    elasticsearch hard memlock unlimited
    ```


RPM and Debian
:   Set `LimitMEMLOCK` to `infinity` in the [systemd configuration](setting-system-settings.md#systemd).

Another possible reason why `mlockall` can fail is that [the JNA temporary directory (usually a sub-directory of `/tmp`) is mounted with the `noexec` option](executable-jna-tmpdir.md). This can be solved by specifying a new temporary directory for JNA using the `ES_JAVA_OPTS` environment variable:

```sh
export ES_JAVA_OPTS="$ES_JAVA_OPTS -Djna.tmpdir=<path>"
./bin/elasticsearch
```

or setting this JVM flag in the jvm.options configuration file.
