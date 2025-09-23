The `/etc/elasticsearch` directory contains the default runtime configuration for {{es}}. The ownership of this directory and all contained files are set to `root:elasticsearch` on package installations.

The `setgid` flag applies group permissions on the `/etc/elasticsearch` directory to ensure that {{es}} can read any contained files and subdirectories. All files and subdirectories inherit the `root:elasticsearch` ownership. Running commands from this directory or any subdirectories, such as the [elasticsearch-keystore tool](/deploy-manage/security/secure-settings.md), requires `root:elasticsearch` permissions.

{{es}} loads its configuration from the `/etc/elasticsearch/elasticsearch.yml` file by default. The format of this config file is explained in [](/deploy-manage/deploy/self-managed/configure-elasticsearch.md).

The {{distro}} package also has a system configuration file at the following path:
 
```txt subs=true
{{pkg-conf}}
```

In this file, you can set the following parameters:

| Parameter | Description |
| --- | --- |
| `ES_JAVA_HOME` | Set a custom Java path to be used. |
| `ES_PATH_CONF` | Configuration file directory (which needs to include `elasticsearch.yml`, `jvm.options`, and `log4j2.properties` files); defaults to `/etc/elasticsearch`. |
| `ES_JAVA_OPTS` | Any additional JVM system properties you may want to apply. |
| `RESTART_ON_UPGRADE` | Configure restart on package upgrade, defaults to `false`. This means you will have to restart your {{es}} instance after installing a package  manually. The reason for this is to ensure, that upgrades in a cluster do not result in a continuous shard reallocation resulting in high network traffic and reducing the response times of your cluster. |

::::{note}
Distributions that use `systemd` require that system resource limits be configured via `systemd` rather than via the {{pkg-conf}} file. See [Systemd configuration](/deploy-manage/deploy/self-managed/setting-system-settings.md#systemd) for more information.
::::