---
navigation_title: "Project paths"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuration-path.html
applies_to:
  stack: all
---



# Configure project paths [apm-configuration-path]


::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-no.svg "")

This documentation is only relevant for APM Server binary users. Fleet-managed paths are defined in [Installation layout](installation-layout.md).

::::


The `path` section of the `apm-server.yml` config file contains configuration options that define where APM Server looks for its files. For example, APM Server looks for the {{es}} template file in the configuration path and writes log files in the logs path.

Please see the [Installation layout](installation-layout.md) section for more details.

Here is an example configuration:

```yaml
path.home: /usr/share/beat
path.config: /etc/beat
path.data: /var/lib/beat
path.logs: /var/log/
```

Note that it is possible to override these options by using command line flags.


## Configuration options [_configuration_options_8]

You can specify the following options in the `path` section of the `apm-server.yml` config file:


### `home` [_home]

The home path for the APM Server installation. This is the default base path for all other path settings and for miscellaneous files that come with the distribution (for example, the sample dashboards). If not set by a CLI flag or in the configuration file, the default for the home path is the location of the APM Server binary.

Example:

```yaml
path.home: /usr/share/beats
```


### `config` [_config]

The configuration path for the APM Server installation. This is the default base path for configuration files, including the main YAML configuration file and the {{es}} template file. If not set by a CLI flag or in the configuration file, the default for the configuration path is the home path.

Example:

```yaml
path.config: /usr/share/beats/config
```


### `data` [_data]

The data path for the APM Server installation. This is the default base path for all the files in which APM Server needs to store its data. If not set by a CLI flag or in the configuration file, the default for the data path is a `data` subdirectory inside the home path.

Example:

```yaml
path.data: /var/lib/beats
```

::::{tip}
When running multiple APM Server instances on the same host, make sure they each have a distinct `path.data` value.
::::



### `logs` [_logs]

The logs path for a APM Server installation. This is the default location for APM Server’s log files. If not set by a CLI flag or in the configuration file, the default for the logs path is a `logs` subdirectory inside the home path.

Example:

```yaml
path.logs: /var/log/beats
```


### `system.hostfs` [_system_hostfs]

Specifies the mount point of the host’s file system for use in monitoring a host. This can either be set in the config, or with the `--system.hostfs` CLI flag. This is used for cgroup self-monitoring.

Example:

```yaml
system.hostfs: /mount/rootfs
```

