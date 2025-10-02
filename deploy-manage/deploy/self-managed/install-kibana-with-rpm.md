---
navigation_title: RPM
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/rpm.html
products:
  - id: kibana
---

# Install {{kib}} with RPM [rpm]

The RPM for {{kib}} can be [downloaded from our website](#install-rpm) or from our [RPM repository](#rpm-repo). It can be used to install {{kib}} on any RPM-based system such as OpenSuSE, SLES, Red Hat, and Oracle Enterprise.

::::{note}
RPM install is not supported on distributions with old versions of RPM, such as SLES 11. Refer to [Install from archive on Linux or macOS](install-kibana-from-archive-on-linux-macos.md) instead.
::::

:::{include} _snippets/trial.md
:::

:::{include} _snippets/kib-releases.md
:::

## Step 1: Import the Elastic PGP key [rpm-key]

:::{include} _snippets/pgp-key.md
:::

```sh
rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
```


## Step 2: Install {{kib}}

You have the following options for installing the {{es}} RPM package:

* [From the RPM repository](#rpm-repo)
* [Manually](#install-rpm)

### Install from the RPM repository [rpm-repo]

Create a file called `kibana.repo` in the `/etc/yum.repos.d/` directory for RedHat based distributions, or in the `/etc/zypp/repos.d/` directory for OpenSuSE based distributions, containing:

```sh subs=true
[kibana-9.X]
name={{kib}} repository for 9.x packages
baseurl=https://artifacts.elastic.co/packages/9.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=1
autorefresh=1
type=rpm-md
```

And your repository is ready for use. You can now install {{kib}} with one of the following commands:

```sh
sudo yum install kibana <1>
sudo dnf install kibana <2>
sudo zypper install kibana <3>
```

1. Use yum on older Red Hat based distributions.
2. Use dnf on Fedora and other newer Red Hat distributions.
3. Use zypper on OpenSUSE based distributions


### Download and install the RPM manually [install-rpm]

The RPM for {{kib}} {{version.stack}} can be downloaded from the website and installed as follows:

::::{tab-set}

:::{tab-item} Latest
To download and install the {{kib}} {{version.stack}} RPM, enter:
```sh subs=true
wget https://artifacts.elastic.co/downloads/kibana/kibana-{{version.stack}}-x86_64.rpm
wget https://artifacts.elastic.co/downloads/kibana/kibana-{{version.stack}}-x86_64.rpm.sha512
shasum -a 512 -c kibana-{{version.stack}}-x86_64.rpm.sha512 <1>
sudo rpm --install kibana-{{version.stack}}-x86_64.rpm
```

1. Compares the SHA of the downloaded RPM and the published checksum, which should output `kibana-<version>-x86_64.rpm: OK`.
:::

:::{tab-item} Specific version
Because {{kib}} is an {{stack}} product, you must install the same version number as the rest of your {{stack}} components. Replace `<SPECIFIC.VERSION.NUMBER>` with the version that's used across your entire stack. For example, you can use {{version.stack.base}}.
```sh subs=true
wget https://artifacts.elastic.co/downloads/kibana/kibana-<SPECIFIC.VERSION.NUMBER>-x86_64.rpm
wget https://artifacts.elastic.co/downloads/kibana/kibana-<SPECIFIC.VERSION.NUMBER>-x86_64.rpm.sha512
shasum -a 512 -c kibana-<SPECIFIC.VERSION.NUMBER>-x86_64.rpm.sha512 <1>
sudo rpm --install kibana-<SPECIFIC.VERSION.NUMBER>-x86_64.rpm
```

1. Compares the SHA of the downloaded RPM and the published checksum, which should output `kibana-<SPECIFIC.VERSION.NUMBER>-x86_64.rpm: OK`.
:::
::::

## Step 3: Start {{es}} and generate an enrollment token for {{kib}} [rpm-enroll]

[Start {{es}}](/deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md).

:::{include} _snippets/auto-security-config.md
:::

:::{include} _snippets/new-enrollment-token.md
:::

## Step 4 (Optional): Make {{kib}} externally accessible

:::{include} _snippets/kibana-ip.md
:::


## Step 5: Run {{kib}} with `systemd` [rpm-running-systemd]

To configure {{kib}} to start automatically when the system starts, run the following commands:

```sh
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable kibana.service
```

{{kib}} can be started and stopped as follows:

```sh
sudo systemctl start kibana.service
sudo systemctl stop kibana.service
```

These commands provide no feedback as to whether {{kib}} was started successfully or not. Log information can be accessed using `journalctl -u kibana.service`.


## Step 6: Enroll {{kib}} with {{es}}

:::{include} _snippets/enroll-systemd.md
:::

## Step 7: Configure {{kib}} using the config file [rpm-configuring]

{{kib}} loads its configuration from the `/etc/kibana/kibana.yml` file by default.  The format of this config file is explained in [](configure-kibana.md).


## Directory layout of RPM [rpm-layout]

The RPM places config files, logs, and the data directory in the appropriate locations for an RPM-based system:

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | {{kib}} home directory or `$KIBANA_HOME` | `/usr/share/kibana` |  |
| bin | Binary scripts including `kibana` to start the {{kib}} server    and `kibana-plugin` to install plugins | `/usr/share/kibana/bin` |  |
| config | Configuration files including `kibana.yml` | `/etc/kibana` | `[KBN_PATH_CONF](configure-kibana.md)` |
| data | The location of the data files written to disk by {{kib}} and its plugins | `/var/lib/kibana` | `path.data` |
| logs | Logs files location | `/var/log/kibana` | `[Logging configuration](../../monitor/logging-configuration/kibana-logging.md)` |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `/usr/share/kibana/plugins` |  |

## Next steps

:::{include} _snippets/install-kib-next-steps.md
:::