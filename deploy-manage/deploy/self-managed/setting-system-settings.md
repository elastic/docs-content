---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/setting-system-settings.html
---

# Configuring system settings [setting-system-settings]

Where to configure systems settings depends on which package you have used to install Elasticsearch, and which operating system you are using.

When using the `.zip` or `.tar.gz` packages, system settings can be configured:

* Temporarily with [`ulimit`](#ulimit).
* Permanently in [`/etc/security/limits.conf`](#limits.conf).

When using the RPM or Debian packages, most system settings are set in the [system configuration file](#sysconfig). However, systems which use systemd require that system limits are specified in a [systemd configuration file](#systemd).

## `ulimit` [ulimit]

On Linux systems, `ulimit` can be used to change resource limits on a temporary basis. Limits usually need to be set as `root` before switching to the user that will run Elasticsearch. For example, to set the number of open file handles (`ulimit -n`) to 65,535, you can do the following:

```sh
sudo su  <1>
ulimit -n 65535 <2>
su elasticsearch <3>
```

1. Become `root`.
2. Change the max number of open files.
3. Become the `elasticsearch` user in order to start Elasticsearch.


The new limit is only applied during the current session.

You can consult all currently applied limits with `ulimit -a`.


## `/etc/security/limits.conf` [limits.conf]

On Linux systems, persistent limits can be set for a particular user by editing the `/etc/security/limits.conf` file. To set the maximum number of open files for the `elasticsearch` user to 65,535, add the following line to the `limits.conf` file:

```sh
elasticsearch  -  nofile  65535
```

This change will only take effect the next time the `elasticsearch` user opens a new session.

::::{admonition} Ubuntu and `limits.conf`
:class: note

Ubuntu ignores the `limits.conf` file for processes started by `init.d`. To enable the `limits.conf` file, edit `/etc/pam.d/su` and uncomment the following line:

```sh
# session    required   pam_limits.so
```

::::



## Sysconfig file [sysconfig]

When using the RPM or Debian packages, environment variables can be specified in the system configuration file, which is located in:

RPM
:   `/etc/sysconfig/elasticsearch`

Debian
:   `/etc/default/elasticsearch`

However, system limits need to be specified via [systemd](#systemd).


## Systemd configuration [systemd]

When using the RPM or Debian packages on systems that use [systemd](https://en.wikipedia.org/wiki/Systemd), system limits must be specified via systemd.

The systemd service file (`/usr/lib/systemd/system/elasticsearch.service`) contains the limits that are applied by default.

To override them, add a file called `/etc/systemd/system/elasticsearch.service.d/override.conf` (alternatively, you may run `sudo systemctl edit elasticsearch` which opens the file automatically inside your default editor). Set any changes in this file, such as:

```sh
[Service]
LimitMEMLOCK=infinity
```

Once finished, run the following command to reload units:

```sh
sudo systemctl daemon-reload
```


