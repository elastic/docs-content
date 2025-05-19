---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/starting-elasticsearch.html
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/stopping-elasticsearch.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
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

### Debian or RPM packages (using `systemd`) [start-deb]

:::{include} /deploy-manage/deploy/self-managed/_snippets/systemd-startup.md
:::

:::{include} /deploy-manage/deploy/self-managed/_snippets/systemd.md
:::

:::{include} /deploy-manage/deploy/self-managed/_snippets/systemd-startup-timeout.md
:::

### Docker images [start-docker]

If you installed a Docker image, you can start {{es}} from the command line. There are different methods depending on whether you’re using development mode or production mode. See [](../../../deploy-manage/deploy/self-managed/install-elasticsearch-with-docker.md).

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
$ ./bin/elasticsearch -p /tmp/elasticsearch-pid -d
$ cat /tmp/elasticsearch-pid && echo
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
