---
navigation_title: "Install with RPM"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/rpm.html
---



# Install with RPM [rpm]


The RPM for {{kib}} can be [downloaded from our website](#install-rpm) or from our [RPM repository](#rpm-repo). It can be used to install {{kib}} on any RPM-based system such as OpenSuSE, SLES, Red Hat, and Oracle Enterprise.

::::{note}
RPM install is not supported on distributions with old versions of RPM, such as SLES 11. Refer to [Install from archive on Linux or macOS](install-from-archive-on-linux-macos.md) instead.
::::


This package contains both free and subscription features. [Start a 30-day trial](../../license/manage-your-license-in-self-managed-cluster.md) to try out all of the features.

The latest stable version of {{kib}} can be found on the [Download Kibana](https://elastic.co/downloads/kibana) page. Other versions can be found on the [Past Releases page](https://elastic.co/downloads/past-releases).

::::{tip}
For a step-by-step example of setting up the {{stack}} on your own premises, try out our tutorial: [Installing a self-managed Elastic Stack](installing-elasticsearch.md).
::::


## Import the Elastic PGP key [rpm-key]

:::{include} _snippets/pgp-key.md
:::

```sh
rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
```


## Installing from the RPM repository [rpm-repo]

Create a file called `kibana.repo` in the `/etc/yum.repos.d/` directory for RedHat based distributions, or in the `/etc/zypp/repos.d/` directory for OpenSuSE based distributions, containing:

```sh
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


## Download and install the RPM manually [install-rpm]

The RPM for {{kib}} {{stack-version}} can be downloaded from the website and installed as follows:

```sh
wget https://artifacts.elastic.co/downloads/kibana/kibana-{{stack-version}}-x86_64.rpm
wget https://artifacts.elastic.co/downloads/kibana/kibana-{{stack-version}}-x86_64.rpm.sha512
shasum -a 512 -c kibana-{{stack-version}}-x86_64.rpm.sha512 <1>
sudo rpm --install kibana-{{stack-version}}-x86_64.rpm
```

1. Compares the SHA of the downloaded RPM and the published checksum, which should output `kibana-{version}-x86_64.rpm: OK`.


## Start {{es}} and generate an enrollment token for {{kib}} [rpm-enroll]


When you start {{es}} for the first time, the following security configuration occurs automatically:

* Authentication and authorization are enabled, and a password is generated for the `elastic` built-in superuser.
* Certificates and keys for TLS are generated for the transport and HTTP layer, and TLS is enabled and configured with these keys and certificates.

The password and certificate and keys are output to your terminal.

You can then generate an enrollment token for {{kib}} with the [`elasticsearch-create-enrollment-token`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool:

```sh
bin/elasticsearch-create-enrollment-token -s kibana
```

Start {{kib}} and enter the enrollment token to securely connect {{kib}} with {{es}}.


## Run {{kib}} with `systemd` [rpm-running-systemd]

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

These commands provide no feedback as to whether {{kib}} was started successfully or not. Log information can be accessed via `journalctl -u kibana.service`.


## Configure {{kib}} via the config file [rpm-configuring]

{{kib}} loads its configuration from the `/etc/kibana/kibana.yml` file by default.  The format of this config file is explained in [Configuring Kibana](configure.md).


## Directory layout of RPM [rpm-layout]

The RPM places config files, logs, and the data directory in the appropriate locations for an RPM-based system:

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | {{kib}} home directory or `$KIBANA_HOME` | `/usr/share/kibana` |  |
| bin | Binary scripts including `kibana` to start the {{kib}} server    and `kibana-plugin` to install plugins | `/usr/share/kibana/bin` |  |
| config | Configuration files including `kibana.yml` | `/etc/kibana` | `[KBN_PATH_CONF](configure.md)` |
| data | The location of the data files written to disk by {{kib}} and its plugins | `/var/lib/kibana` | `path.data` |
| logs | Logs files location | `/var/log/kibana` | `[Logging configuration](../../monitor/logging-configuration/kibana-logging.md)` |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `/usr/share/kibana/plugins` |  |
