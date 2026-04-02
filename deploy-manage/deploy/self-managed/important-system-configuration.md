---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/system-config.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Important system configuration [system-config]

Ideally, {{es}} should run alone on a server and use all of the resources available to it. In order to do so, you need to configure your operating system to allow the user running {{es}} to access more resources than allowed by default.

The following settings **must** be considered before going to production:

* [](/deploy-manage/deploy/self-managed/elasticsearch-service-user.md): Run as a dedicated unprivileged user, keep numeric UID and GID consistent across nodes, and set correct ownership on config and data paths.
* [](/deploy-manage/deploy/self-managed/setting-system-settings.md): Where and how to apply operating-system limits and environment variables for your install type.
* [](/deploy-manage/deploy/self-managed/setup-configuration-memory.md): Avoid heap or process memory being swapped out; options include disabling swap, lowering swappiness, and `bootstrap.memory_lock`.
* [](/deploy-manage/deploy/self-managed/vm-max-map-count.md): Set `vm.max_map_count` high enough for mmap-based index storage (for example `1048576` when required).
* [](/deploy-manage/deploy/self-managed/max-number-of-threads.md): Allow the {{es}} user to create at least `4096` threads on Linux when you manage limits yourself.
* [](/deploy-manage/deploy/self-managed/file-descriptors.md): Raise open file handles to at least `65,535` (Linux and macOS only).
* [](/deploy-manage/deploy/self-managed/executable-jna-tmpdir.md): Ensure JNA and native libraries can execute from a temp path that is not mounted `noexec` (Linux only).
* [](/deploy-manage/deploy/self-managed/system-config-tcpretries.md): Lower `net.ipv4.tcp_retries2` so node and network failures are detected sooner than the Linux default (Linux only).

:::{tip}
For examples of applying the relevant settings in a Docker environment, refer to [](/deploy-manage/deploy/self-managed/install-elasticsearch-docker-prod.md).
:::

::::{admonition} Use dedicated hosts
:::{include} _snippets/dedicated-hosts.md
:::
::::

## Bootstrap checks

{{es}} has bootstrap checks that run at startup to ensure that users have configured all important settings. 

For a list of the checks and their meaning, refer to [](/deploy-manage/deploy/self-managed/bootstrap-checks.md).

### Development mode vs. production mode [dev-vs-prod] 

By default, {{es}} assumes that you are working in development mode. If any of the above settings are not configured correctly, the relevant bootstrap check will fail and a warning will be written to the log file, but you will be able to start and run your {{es}} node.

As soon as you configure a network setting like `network.host`, {{es}} assumes that you are moving to production and will upgrade the above warnings to exceptions. These exceptions will prevent your {{es}} node from starting. This is an important safety measure to ensure that you will not lose data because of a misconfigured server.









