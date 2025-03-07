---
mapped_urls:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/stopping-elasticsearch.html
applies_to:
  deployment:
     self:
---

# Start and stop Elasticsearch

Understanding how to properly start and stop Elasticsearch is essential for maintaining a stable and efficient cluster. This guide outlines the recommended methods for starting and stopping {{es}} safely, considering the different installation types, including package-based installations, Docker containers, and manually extracted archives.

## Starting Elasticsearch [starting-elasticsearch]

The method for starting {{es}} varies depending on how you installed it.

### Archive packages (`.tar.gz`) [start-targz]

If you installed {{es}} with a `.tar.gz` package, you can start {{es}} from the command line.

#### Run {{es}} from the command line [_run_es_from_the_command_line]

Run the following command to start {{es}} from the command line:

```sh
./bin/elasticsearch
```

When starting {{es}} for the first time, security features are enabled and configured by default. The following security configuration occurs automatically:

* Authentication and authorization are enabled, and a password is generated for the `elastic` built-in superuser.
* Certificates and keys for TLS are generated for the transport and HTTP layer, and TLS is enabled and configured with these keys and certificates.
* An enrollment token is generated for {{kib}}, which is valid for 30 minutes.

The password for the `elastic` user and the enrollment token for {{kib}} are output to your terminal.

We recommend storing the `elastic` password as an environment variable in your shell. Example:

```sh
export ELASTIC_PASSWORD="your_password"
```

If you have password-protected the {{es}} keystore, you will be prompted to enter the keystore’s password. See [Secure settings](../../../deploy-manage/security/secure-settings.md) for more details.

By default {{es}} prints its logs to the console (`stdout`) and to the `<cluster name>.log` file within the [logs directory](../../../deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings). {{es}} logs some information while it is starting, but after it has finished initializing it will continue to run in the foreground and won’t log anything further until something happens that is worth recording. While {{es}} is running you can interact with it through its HTTP interface which is on port `9200` by default.

To stop {{es}}, press `Ctrl-C`.

::::{note}
All scripts packaged with {{es}} require a version of Bash that supports arrays and assume that Bash is available at `/bin/bash`. As such, Bash should be available at this path either directly or via a symbolic link.
::::

#### Run as a daemon [_run_as_a_daemon]

To run Elasticsearch as a daemon, specify `-d` on the command line, and record the process ID in a file using the `-p` option:

```sh
./bin/elasticsearch -d -p pid
```

If you have password-protected the {{es}} keystore, you will be prompted to enter the keystore’s password. Refer to [Secure settings](../../../deploy-manage/security/secure-settings.md) for more details.

Log messages can be found in the `$ES_HOME/logs/` directory.

To shut down Elasticsearch, kill the process ID recorded in the `pid` file:

```sh
pkill -F pid
```

::::{note}
The {{es}} `.tar.gz` package does not include the `systemd` module. To manage {{es}} as a service, use the [Debian](../../../deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md#start-deb) or [RPM](../../../deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md#start-rpm) package instead.
::::

### Archive packages (`.zip`) [start-zip]

If you installed {{es}} on Windows with a `.zip` package, you can start {{es}} from the command line. If you want {{es}} to start automatically at boot time without any user interaction, [install {{es}} as a service](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-zip-on-windows.md#windows-service).

#### Run {{es}} from the command line [_run_es_from_the_command_line_2]

Run the following command to start {{es}} from the command line:

```sh
.\bin\elasticsearch.bat
```

When starting {{es}} for the first time, security features are enabled and configured by default. The following security configuration occurs automatically:

* Authentication and authorization are enabled, and a password is generated for the `elastic` built-in superuser.
* Certificates and keys for TLS are generated for the transport and HTTP layer, and TLS is enabled and configured with these keys and certificates.
* An enrollment token is generated for {{kib}}, which is valid for 30 minutes.

The password for the `elastic` user and the enrollment token for {{kib}} are output to your terminal.

We recommend storing the `elastic` password as an environment variable in your shell. Example:

```sh
$ELASTIC_PASSWORD = "your_password"
```

If you have password-protected the {{es}} keystore, you will be prompted to enter the keystore’s password. See [Secure settings](../../../deploy-manage/security/secure-settings.md) for more details.

By default {{es}} prints its logs to the console (`STDOUT`) and to the `<cluster name>.log` file within the [logs directory](../../../deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings). {{es}} logs some information while it is starting, but after it has finished initializing it will continue to run in the foreground and won’t log anything further until something happens that is worth recording. While {{es}} is running you can interact with it through its HTTP interface which is on port `9200` by default.

To stop {{es}}, press `Ctrl-C`.

### Debian packages [start-deb]

#### Running Elasticsearch with `systemd` [start-es-deb-systemd]

To configure Elasticsearch to start automatically when the system boots up, run the following commands:

```sh
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
```

Elasticsearch can be started and stopped as follows:

```sh
sudo systemctl start elasticsearch.service
sudo systemctl stop elasticsearch.service
```

These commands provide no feedback as to whether Elasticsearch was started successfully or not. Instead, this information will be written in the log files located in `/var/log/elasticsearch/`.

If you have password-protected your {{es}} keystore, you will need to provide `systemd` with the keystore password using a local file and systemd environment variables. This local file should be protected while it exists and may be safely deleted once Elasticsearch is up and running.

```sh
echo "keystore_password" > /path/to/my_pwd_file.tmp
chmod 600 /path/to/my_pwd_file.tmp
sudo systemctl set-environment ES_KEYSTORE_PASSPHRASE_FILE=/path/to/my_pwd_file.tmp
sudo systemctl start elasticsearch.service
```

By default the Elasticsearch service doesn’t log information in the `systemd` journal. To enable `journalctl` logging, the `--quiet` option must be removed from the `ExecStart` command line in the `elasticsearch.service` file.

When `systemd` logging is enabled, the logging information are available using the `journalctl` commands:

To tail the journal:

```sh
sudo journalctl -f
```

To list journal entries for the elasticsearch service:

```sh
sudo journalctl --unit elasticsearch
```

To list journal entries for the elasticsearch service starting from a given time:

```sh
sudo journalctl --unit elasticsearch --since  "2016-10-30 18:17:16"
```

Check `man journalctl` or [https://www.freedesktop.org/software/systemd/man/journalctl.html](https://www.freedesktop.org/software/systemd/man/journalctl.html) for more command line options.

::::{admonition} Startup timeouts with older `systemd` versions
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
Jan 31 01:22:30 debian systemd[1]: Starting Elasticsearch...
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Start operation timed out. Terminating.
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Main process exited, code=killed, status=15/TERM
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Failed with result 'timeout'.
Jan 31 01:37:15 debian systemd[1]: Failed to start Elasticsearch.
```

To avoid this, upgrade your `systemd` to at least version 238. You can also temporarily work around the problem by extending the `TimeoutStartSec` parameter.

::::

### Docker images [start-docker]

If you installed a Docker image, you can start {{es}} from the command line. There are different methods depending on whether you’re using development mode or production mode. See [Run {{es}} in Docker](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-docker.md#docker-cli-run-dev-mode).

### RPM packages [start-rpm]

#### Running Elasticsearch with `systemd` [start-es-rpm-systemd]

To configure Elasticsearch to start automatically when the system boots up, run the following commands:

```sh
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
```

Elasticsearch can be started and stopped as follows:

```sh
sudo systemctl start elasticsearch.service
sudo systemctl stop elasticsearch.service
```

These commands provide no feedback as to whether Elasticsearch was started successfully or not. Instead, this information will be written in the log files located in `/var/log/elasticsearch/`.

If you have password-protected your {{es}} keystore, you will need to provide `systemd` with the keystore password using a local file and systemd environment variables. This local file should be protected while it exists and may be safely deleted once Elasticsearch is up and running.

```sh
echo "keystore_password" > /path/to/my_pwd_file.tmp
chmod 600 /path/to/my_pwd_file.tmp
sudo systemctl set-environment ES_KEYSTORE_PASSPHRASE_FILE=/path/to/my_pwd_file.tmp
sudo systemctl start elasticsearch.service
```

By default the Elasticsearch service doesn’t log information in the `systemd` journal. To enable `journalctl` logging, the `--quiet` option must be removed from the `ExecStart` command line in the `elasticsearch.service` file.

When `systemd` logging is enabled, the logging information are available using the `journalctl` commands:

To tail the journal:

```sh
sudo journalctl -f
```

To list journal entries for the elasticsearch service:

```sh
sudo journalctl --unit elasticsearch
```

To list journal entries for the elasticsearch service starting from a given time:

```sh
sudo journalctl --unit elasticsearch --since  "2016-10-30 18:17:16"
```

Check `man journalctl` or [https://www.freedesktop.org/software/systemd/man/journalctl.html](https://www.freedesktop.org/software/systemd/man/journalctl.html) for more command line options.

::::{admonition} Startup timeouts with older `systemd` versions
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
Jan 31 01:22:30 debian systemd[1]: Starting Elasticsearch...
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Start operation timed out. Terminating.
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Main process exited, code=killed, status=15/TERM
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Failed with result 'timeout'.
Jan 31 01:37:15 debian systemd[1]: Failed to start Elasticsearch.
```

To avoid this, upgrade your `systemd` to at least version 238. You can also temporarily work around the problem by extending the `TimeoutStartSec` parameter.

::::

## Stopping Elasticsearch [stopping-elasticsearch]

An orderly shutdown of Elasticsearch ensures that Elasticsearch has a chance to cleanup and close outstanding resources. For example, a node that is shutdown in an orderly fashion will remove itself from the cluster, sync translogs to disk, and perform other related cleanup activities. You can help ensure an orderly shutdown by properly stopping Elasticsearch.

If you’re running Elasticsearch as a service, you can stop Elasticsearch via the service management functionality provided by your installation.

If you’re running Elasticsearch directly, you can stop Elasticsearch by sending control-C if you’re running Elasticsearch in the console, or by sending `SIGTERM` to the Elasticsearch process on a POSIX system. You can obtain the PID to send the signal to via various tools (for example, `ps` or `jps`):

```sh
$ jps | grep Elasticsearch
14542 Elasticsearch
```

From the Elasticsearch startup logs:

```sh
[2016-07-07 12:26:18,908][INFO ][node                     ] [I8hydUG] version[5.0.0-alpha4], pid[15399], build[3f5b994/2016-06-27T16:23:46.861Z], OS[Mac OS X/10.11.5/x86_64], JVM[Oracle Corporation/Java HotSpot(TM) 64-Bit Server VM/1.8.0_92/25.92-b14]
```

Or by specifying a location to write a PID file to on startup (`-p <path>`):

```sh
$ ./bin/elasticsearch -p /tmp/elasticsearch-pid -d
$ cat /tmp/elasticsearch-pid && echo
15516
$ kill -SIGTERM 15516
```

### Stopping on Fatal Errors [fatal-errors]

During the life of the Elasticsearch virtual machine, certain fatal errors could arise that put the virtual machine in a questionable state. Such fatal errors include out of memory errors, internal errors in virtual machine, and serious I/O errors.

When Elasticsearch detects that the virtual machine has encountered such a fatal error Elasticsearch will attempt to log the error and then will halt the virtual machine. When Elasticsearch initiates such a shutdown, it does not go through an orderly shutdown as described above. The Elasticsearch process will also return with a special status code indicating the nature of the error.

Killed by jvmkiller agent
:   158

User or kernel SIGTERM
:   143

Slain by kernel oom-killer
:   137

Segmentation fault
:   134

JVM internal error
:   128

Out of memory error
:   127

Stack overflow error
:   126

Unknown virtual machine error
:   125

Serious I/O error
:   124

Bootstrap check failure
:   78

Unknown fatal error
:   1
