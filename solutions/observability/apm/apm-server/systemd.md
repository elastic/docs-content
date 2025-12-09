---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-running-with-systemd.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# APM Server and systemd [apm-running-with-systemd]

::::{important}
These commands only apply to the APM Server binary installation method. Fleet-managed users should see [Start and stop {{agent}}s on edge hosts](/reference/fleet/start-stop-elastic-agent.md).
::::

The DEB and RPM packages include a service unit for Linux systems with systemd. On these systems, you can manage APM Server by using the usual systemd commands.

We recommend that the apm-server process is run as a non-root user. Therefore, that is the default setup for APM Server’s DEB package and RPM installation.

## Start and stop APM Server [_start_and_stop_apm_server]

Use `systemctl` to start or stop APM Server:

```sh
sudo systemctl start apm-server
```

```sh
sudo systemctl stop apm-server
```

By default, the APM Server service starts automatically when the system boots. To enable or disable auto start use:

```sh
sudo systemctl enable apm-server
```

```sh
sudo systemctl disable apm-server
```

## APM Server status and logs [_apm_server_status_and_logs]

To get the service status, use `systemctl`:

```sh
systemctl status apm-server
```

Logs are stored by default in journald. To view the Logs, use `journalctl`:

```sh
journalctl -u apm-server.service
```

## Customize systemd unit for APM Server [_customize_systemd_unit_for_apm_server]

The systemd service unit file includes environment variables that you can override to change the default options.

| Variable | Description | Default value |
| --- | --- | --- |
| `BEAT_LOG_OPTS` | Log options |  |
| `BEAT_CONFIG_OPTS` | Flags for configuration file path | ``-c /etc/apm-server/apm-server.yml`` |
| `BEAT_PATH_OPTS` | Other paths | ``-path.home /usr/share/apm-server -path.config /etc/apm-server -path.data /var/lib/apm-server -path.logs /var/log/apm-server`` |

::::{note}
You can use `BEAT_LOG_OPTS` to set debug selectors for logging. However, to configure logging behavior, set the logging options described in [Configure logging](/solutions/observability/apm/apm-server/configure-logging.md).
::::

To override these variables, create a drop-in unit file in the `/etc/systemd/system/apm-server.service.d` directory.

For example a file with the following content placed in `/etc/systemd/system/apm-server.service.d/debug.conf` would override `BEAT_LOG_OPTS` to enable debug for {{es}} output.

```ini
[Service]
Environment="BEAT_LOG_OPTS=-d elasticsearch"
```

To apply your changes, reload the systemd configuration and restart the service:

```sh
systemctl daemon-reload
systemctl restart apm-server
```

::::{note}
It is recommended that you use a configuration management tool to include drop-in unit files. If you need to add a drop-in manually, use `systemctl edit apm-server.service`.
::::

#### Configuring the NOFILE limit [configuring-nofile-limit]

::::{note}
There should be no need to manually configure this limit when running APM Server.
::::

In systemd the `LimitNOFILE` defaults are set to `1024` (soft) and `524288` (hard) and most Linux systems with systemd do not change these values or reduce them drastically. Golang, starting from version 1.19 (refer to [golang/go#46279](https://github.com/golang/go/issues/46279)), automatically bump the process limit up to the available hard limit. This means that by default APM Server runs with the limit set to the hard limit value by the Operating System is being run on, generally `524287` on a recent system. There should be no reason to change this limit, as back-pressure from too many open files happens through memory usage.

For guidelines on the value to set this value to refer to [modifying the `nofile` ulimit](/solutions/observability/apm/apm-server/binary.md#modify-nofile-ulimit).

#### Configuration file ownership [apm-config-file-ownership]

On systems with POSIX file permissions, the APM Server configuration file is subject to ownership and file permission checks. These checks prevent unauthorized users from providing or modifying configurations that are run by APM Server.

When installed via an RPM or DEB package, the configuration file at `/etc/apm-server/apm-server.yml` will be owned by `apm-server`, and have file permissions of `0600` (`-rw-------`).

APM Server will only start if the configuration file is owned by the user running the process, or by running as root with configuration ownership set to `root:root`

You may encounter the following errors if your configuration file fails these checks:

```text
Exiting: error loading config file: config file ("/etc/apm-server/apm-server.yml")
must be owned by the user identifier (uid=1000) or root
```

To correct this problem you can change the ownership of the configuration file with: `chown apm-server:apm-server /etc/apm-server/apm-server.yml`.

You can also make root the config owner, although this is not recommended: `sudo chown root:root /etc/apm-server/apm-server.yml`.

```text
Exiting: error loading config file: config file ("/etc/apm-server/apm-server.yml")
can only be writable by the owner but the permissions are "-rw-rw-r--"
(to fix the permissions use: 'chmod go-w /etc/apm-server/apm-server.yml')
```

To correct this problem, use `chmod go-w /etc/apm-server/apm-server.yml` to remove write privileges from anyone other than the owner.

##### Disabling strict permission checks [_disabling_strict_permission_checks]

You can disable strict permission checks from the command line by using `--strict.perms=false`, but we strongly encourage you to leave the checks enabled.

