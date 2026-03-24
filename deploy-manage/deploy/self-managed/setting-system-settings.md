---
navigation_title: Configuration methods
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/setting-system-settings.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# System settings configuration methods [setting-system-settings]

This page describes **where and how** to apply operating system limits and environment variables for {{es}}, depending on your installation package and `init` system.

For **which** limits and values you must set (such as file descriptors, threads, memory lock, virtual memory, and so on), see [Important system configuration](important-system-configuration.md) and the pages linked from there.

Where to configure system settings depends on how {{es}} is installed and started, and which operating system you are using:

* When using the `.zip` or `.tar.gz` packages, {{es}} is typically started manually from a shell. In this case, system limits can be configured using `/etc/security/limits.conf` or by setting them directly in the shell using `ulimit` before starting {{es}}.

* When using `.deb` or `.rpm` packages, Elasticsearch runs as a system service managed by systemd. In this case, system limits must be configured in the service definition (for example, using `LimitNOFILE` in a systemd override file).

* Temporarily with [`ulimit`](#ulimit).
* Permanently in [`/etc/security/limits.conf`](#limits.conf).

When using the RPM or Debian packages, most system settings are set in the [system configuration file](#sysconfig). However, systems which use systemd require that system limits are specified in a [systemd configuration file](#systemd).


## `ulimit` [ulimit]

On Linux systems, you can use `ulimit` to change resource limits on a temporary basis. Limits usually need to be set as `root` before switching to the user that will run {{es}}.

Common options for `ulimit` include:

* `-n` — maximum number of open file descriptors
* `-u` — maximum number of processes available to a single user
* `-l` — maximum size of memory that may be locked into RAM
* `-a` — show all current soft resource limits (use this to verify what is in effect)

For the full list of options, run `help ulimit` in Bash.

Use the option and value required for your setting (see the pages under [Important system configuration](important-system-configuration.md)). For example:

```sh
sudo su  <1>
ulimit -n 65535 <2>
ulimit -u 4096 <3>
ulimit -l unlimited <4>
su elasticsearch <5>
```

1. Become `root`.
2. Set the [open file descriptor limit](/deploy-manage/deploy/self-managed/file-descriptors.md) for this session.
3. Set the [maximum number of threads](/deploy-manage/deploy/self-managed/max-number-of-threads.md) for this session.
4. Allow [memory locking](/deploy-manage/deploy/self-managed/setup-configuration-memory.md#bootstrap-memory_lock) for this session.
5. Become the user that will run {{es}} (for example `elasticsearch`) before starting the process.

The new limit is only applied during the current session.


## `/etc/security/limits.conf` [limits.conf]

On Linux systems, persistent limits can be set for a particular user by editing the `/etc/security/limits.conf` file. Add lines for the `elasticsearch` user (or the account that runs {{es}}) with the limit type and value your deployment requires. The exact limit name depends on what you are configuring. For example, you can configure `nofile` (open files), `nproc` (processes), or `memlock` (locked memory). Replace `<limit>` and `<value>` accordingly:

```sh
elasticsearch  -  nofile  65535
elasticsearch  -  nproc  4096
elasticsearch  -  memlock  unlimited
```

This change will only take effect the next time the `elasticsearch` user opens a new session.

::::{admonition} Ubuntu and limits.conf
:class: note

Ubuntu ignores the `limits.conf` file for processes started by `init.d`. To enable the `limits.conf` file, edit `/etc/pam.d/su` and uncomment the following line:

```sh
# session    required   pam_limits.so
```

::::



## Sysconfig file [sysconfig]

When using the RPM or Debian packages, environment variables can be specified in the system configuration file, which is located in the relevant location for your package type:

| Package type | Location |
| --- | --- | 
| RPM | `/etc/sysconfig/elasticsearch`|
| Debian | `/etc/default/elasticsearch` | 

However, system limits need to be specified via [systemd](#systemd).

Use the topic pages under [Important system configuration](important-system-configuration.md) to determine which environment variables or JVM options you need (for example `ES_JAVA_OPTS`, `ES_TMPDIR`, or paths set in `jvm.options`).


## Systemd configuration [systemd]

When using the RPM or Debian packages on systems that use [systemd](https://en.wikipedia.org/wiki/Systemd), system limits must be specified via systemd.

The systemd service file (`/usr/lib/systemd/system/elasticsearch.service`) contains the limits that are applied by default.

To override them, add a file called `/etc/systemd/system/elasticsearch.service.d/override.conf` (alternatively, you may run `sudo systemctl edit elasticsearch` which opens the file automatically inside your default editor). Set any changes in this file. For example, for resource limits and environment variables, include:

```ini
[Service]
Environment="MY_VAR=my-value"
LimitNOFILE=65535
LimitNPROC=4096
LimitMEMLOCK=infinity
```

Replace the directives with those required for your deployment.

Once finished, run the following command to reload units:

```sh
sudo systemctl daemon-reload
```
