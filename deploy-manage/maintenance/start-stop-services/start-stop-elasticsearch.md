---
mapped_urls:
  - https://www.elastic.co/guide/en/{{es}}/reference/current/starting-elasticsearch.html
  - https://www.elastic.co/guide/en/{{es}}/reference/current/stopping-elasticsearch.html
applies_to:
  deployment:
     self:
---

# Start and stop {{es}}

Understanding how to properly start and stop {{es}} is essential for maintaining a stable and efficient cluster. This guide outlines the recommended methods for starting and stopping {{es}} safely, considering the different installation types, including package-based installations, Docker containers, and manually extracted archives.

## Starting {{es}} [starting-{{es}}]

The method for starting {{es}} varies depending on how you installed it.

### Archive packages (`.tar.gz`) [start-targz]

If you installed {{es}} on Linux or MacOS with a `.tar.gz` package, you can start {{es}} from the command line.

#### Run {{es}} from the command line [_run_es_from_the_command_line]

:::{include} /deploy-manage/deploy/self-managed/_snippets/targz-start.md
:::

If you're starting {{es}} for the first time, then {{es}} also enables and configures security. [Learn more](/deploy-manage/deploy/self-managed/install-elasticsearch-from-archive-on-linux-macos.md#security-at-startup).

#### Run as a daemon [_run_as_a_daemon]

:::{include} /deploy-manage/deploy/self-managed/_snippets/targz-daemon.md
:::

### Archive packages (`.zip`) [start-zip]

If you installed {{es}} on Windows with a `.zip` package, you can start {{es}} from the command line. If you want {{es}} to start automatically at boot time without any user interaction, [install {{es}} as a service](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-zip-on-windows.md#windows-service).

:::{include} /deploy-manage/deploy/self-managed/_snippets/zip-windows-start.md
:::

If you're starting {{es}} for the first time, then {{es}} also enables and configures security. [Learn more](/deploy-manage/deploy/self-managed/install-elasticsearch-with-zip-on-windows.md#security-at-startup).

### Debian packages [start-deb]

#### Running {{es}} with `systemd` [start-es-deb-systemd]

To configure {{es}} to start automatically when the system boots up, run the following commands:

```sh
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
```

{{es}} can be started and stopped as follows:

```sh
sudo systemctl start elasticsearch.service
sudo systemctl stop elasticsearch.service
```

These commands provide no feedback as to whether {{es}} was started successfully or not. Instead, this information will be written in the log files located in `/var/log/{{es}}/`.

If you have password-protected your {{es}} keystore, you will need to provide `systemd` with the keystore password using a local file and systemd environment variables. This local file should be protected while it exists and may be safely deleted once {{es}} is up and running.

```sh
echo "keystore_password" > /path/to/my_pwd_file.tmp
chmod 600 /path/to/my_pwd_file.tmp
sudo systemctl set-environment ES_KEYSTORE_PASSPHRASE_FILE=/path/to/my_pwd_file.tmp
sudo systemctl start elasticsearch.service
```

By default the {{es}} service doesn’t log information in the `systemd` journal. To enable `journalctl` logging, the `--quiet` option must be removed from the `ExecStart` command line in the `elasticsearch.service` file.

When `systemd` logging is enabled, the logging information are available using the `journalctl` commands:

To tail the journal:

```sh
sudo journalctl -f
```

To list journal entries for the {{es}} service:

```sh
sudo journalctl --unit elasticsearch
```

To list journal entries for the {{es}} service starting from a given time:

```sh
sudo journalctl --unit elasticsearch --since  "2016-10-30 18:17:16"
```

Check `man journalctl` or [https://www.freedesktop.org/software/systemd/man/journalctl.html](https://www.freedesktop.org/software/systemd/man/journalctl.md) for more command line options.

::::{admonition} Startup timeouts with older systemd versions
:class: tip

By default {{es}} sets the `TimeoutStartSec` parameter to `systemd` to `900s`. If you are running at least version 238 of `systemd` then {{es}} can automatically extend the startup timeout, and will do so repeatedly until startup is complete even if it takes longer than 900s.

Versions of `systemd` prior to 238 do not support the timeout extension mechanism and will terminate the {{es}} process if it has not fully started up within the configured timeout. If this happens, {{es}} will report in its logs that it was shut down normally a short time after it started:

```text
[2022-01-31T01:22:31,077][INFO ][o.e.n.Node               ] [instance-0000000123] starting ...
...
[2022-01-31T01:37:15,077][INFO ][o.e.n.Node               ] [instance-0000000123] stopping ...
```

However the `systemd` logs will report that the startup timed out:

```text
Jan 31 01:22:30 debian systemd[1]: Starting elasticsearch...
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Start operation timed out. Terminating.
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Main process exited, code=killed, status=15/TERM
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Failed with result 'timeout'.
Jan 31 01:37:15 debian systemd[1]: Failed to start elasticsearch.
```

To avoid this, upgrade your `systemd` to at least version 238. You can also temporarily work around the problem by extending the `TimeoutStartSec` parameter.

::::

### Docker images [start-docker]

If you installed a Docker image, you can start {{es}} from the command line. There are different methods depending on whether you’re using development mode or production mode. See [](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-docker.md).

### RPM packages [start-rpm]

#### Running {{es}} with `systemd` [start-es-rpm-systemd]

To configure {{es}} to start automatically when the system boots up, run the following commands:

```sh
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
```

{{es}} can be started and stopped as follows:

```sh
sudo systemctl start elasticsearch.service
sudo systemctl stop elasticsearch.service
```

These commands provide no feedback as to whether {{es}} was started successfully or not. Instead, this information will be written in the log files located in `/var/log/{{es}}/`.

If you have password-protected your {{es}} keystore, you will need to provide `systemd` with the keystore password using a local file and systemd environment variables. This local file should be protected while it exists and may be safely deleted once {{es}} is up and running.

```sh
echo "keystore_password" > /path/to/my_pwd_file.tmp
chmod 600 /path/to/my_pwd_file.tmp
sudo systemctl set-environment ES_KEYSTORE_PASSPHRASE_FILE=/path/to/my_pwd_file.tmp
sudo systemctl start elasticsearch.service
```

By default the {{es}} service doesn’t log information in the `systemd` journal. To enable `journalctl` logging, the `--quiet` option must be removed from the `ExecStart` command line in the `elasticsearch.service` file.

When `systemd` logging is enabled, the logging information are available using the `journalctl` commands:

To tail the journal:

```sh
sudo journalctl -f
```

To list journal entries for the {{es}} service:

```sh
sudo journalctl --unit elasticsearch
```

To list journal entries for the {{es}} service starting from a given time:

```sh
sudo journalctl --unit elasticsearch --since  "2016-10-30 18:17:16"
```

Check `man journalctl` or [https://www.freedesktop.org/software/systemd/man/journalctl.html](https://www.freedesktop.org/software/systemd/man/journalctl.md) for more command line options.

::::{admonition} Startup timeouts with older systemd versions
:class: tip

By default {{es}} sets the `TimeoutStartSec` parameter to `systemd` to `900s`. If you are running at least version 238 of `systemd` then {{es}} can automatically extend the startup timeout, and will do so repeatedly until startup is complete even if it takes longer than 900s.

Versions of `systemd` prior to 238 do not support the timeout extension mechanism and will terminate the {{es}} process if it has not fully started up within the configured timeout. If this happens, {{es}} will report in its logs that it was shut down normally a short time after it started:

```text
[2022-01-31T01:22:31,077][INFO ][o.e.n.Node               ] [instance-0000000123] starting ...
...
[2022-01-31T01:37:15,077][INFO ][o.e.n.Node               ] [instance-0000000123] stopping ...
```

However the `systemd` logs will report that the startup timed out:

```text
Jan 31 01:22:30 debian systemd[1]: Starting elasticsearch...
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Start operation timed out. Terminating.
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Main process exited, code=killed, status=15/TERM
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Failed with result 'timeout'.
Jan 31 01:37:15 debian systemd[1]: Failed to start elasticsearch.
```

To avoid this, upgrade your `systemd` to at least version 238. You can also temporarily work around the problem by extending the `TimeoutStartSec` parameter.

::::

## Stopping {{es}} [stopping-elasticsearch]

An orderly shutdown of {{es}} ensures that {{es}} has a chance to cleanup and close outstanding resources. For example, a node that is shutdown in an orderly fashion will remove itself from the cluster, sync translogs to disk, and perform other related cleanup activities. You can help ensure an orderly shutdown by properly stopping {{es}}.

If you’re running {{es}} as a service, you can stop {{es}} via the service management functionality provided by your installation.

If you’re running {{es}} directly, you can stop {{es}} by sending `Ctrl`+`C` if you’re running {{es}} in the console, or by sending `SIGTERM` to the {{es}} process on a POSIX system. You can obtain the PID to send the signal to via various tools (for example, `ps` or `jps`):

```sh
$ jps | grep elasticsearch
14542 elasticsearch
```

From the {{es}} startup logs:

```sh
[2016-07-07 12:26:18,908][INFO ][node                     ] [I8hydUG] version[5.0.0-alpha4], pid[15399], build[3f5b994/2016-06-27T16:23:46.861Z], OS[Mac OS X/10.11.5/x86_64], JVM[Oracle Corporation/Java HotSpot(TM) 64-Bit Server VM/1.8.0_92/25.92-b14]
```

Or by specifying a location to write a PID file to on startup (`-p <path>`):

```sh
$ ./bin/{{es}} -p /tmp/{{es}}-pid -d
$ cat /tmp/{{es}}-pid && echo
15516
$ kill -SIGTERM 15516
```

### Stopping on fatal errors [fatal-errors]

During the life of the {{es}} virtual machine, certain fatal errors could arise that put the virtual machine in a questionable state. Such fatal errors include out of memory errors, internal errors in virtual machine, and serious I/O errors.

When {{es}} detects that the virtual machine has encountered such a fatal error {{es}} will attempt to log the error and then will halt the virtual machine. When {{es}} initiates such a shutdown, it does not go through an orderly shutdown as described above. The {{es}} process will also return with a special status code indicating the nature of the error.

| Status code | Error | 
| --- | --- |
| 1   | Unknown fatal error | 
| 78  | Bootstrap check failure | 
| 124 | Serious I/O error |
| 125 | Unknown virtual machine error |
| 126 | Stack overflow error |  
| 127 | Out of memory error | 
| 128 | JVM internal error | 
| 134 | Segmentation fault |
| 137 | Slain by kernel oom-killer |
| 143 | User or kernel SIGTERM |
| 158 | Killed by jvmkiller agent |
