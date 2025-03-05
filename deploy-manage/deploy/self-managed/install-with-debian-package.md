---
navigation_title: "Install with Debian package"
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/deb.html
sub:
  stack-version: "9.0.0"
---



# Install with Debian package [deb]


The Debian package for {{kib}} can be [downloaded from our website](#install-deb) or from our [APT repository](#deb-repo). It can be used to install {{kib}} on any Debian-based system such as Debian and Ubuntu.

This package contains both free and subscription features. [Start a 30-day trial](../../license/manage-your-license-in-self-managed-cluster.md) to try out all of the features.

The latest stable version of {{kib}} can be found on the [Download Kibana](https://elastic.co/downloads/kibana) page. Other versions can be found on the [Past Releases page](https://elastic.co/downloads/past-releases).

## Import the Elastic PGP key [deb-key]

:::{include} _snippets/pgp-key.md
:::

```sh
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
```

## Install from the APT repository [deb-repo]

You may need to install the `apt-transport-https` package on Debian before proceeding:

```sh
sudo apt-get install apt-transport-https
```

Save the repository definition to `/etc/apt/sources.list.d/elastic-9.x.list`:

```sh
echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-9.x.list
```

:::{warning}
Do not use `add-apt-repository` as it will add a `deb-src` entry as well, but we do not provide a source package. If you have added the `deb-src` entry, you will see an error like the following:

```
Unable to find expected entry 'main/source/Sources' in Release file
(Wrong sources.list entry or malformed file)
```

Delete the `deb-src` entry from the `/etc/apt/sources.list` file and the installation should work as expected.
:::

You can install the {{kib}} Debian package with:

```sh
sudo apt-get update && sudo apt-get install kibana
```

:::{warning}
If two entries exist for the same {{kib}} repository, you will see an error like this during `apt-get update`:

```
Duplicate sources.list entry https://artifacts.elastic.co/packages/8.x/apt/ ...`
```

Examine `/etc/apt/sources.list.d/kibana-8.x.list` for the duplicate entry or locate the duplicate entry amongst the files in `/etc/apt/sources.list.d/` and the `/etc/apt/sources.list` file.
:::

## Download and install the Debian package manually [install-deb]

The Debian package for {{kib}} {{stack-version}} can be downloaded from the website and installed as follows:
```sh
wget https://artifacts.elastic.co/downloads/kibana/kibana-{{stack-version}}-amd64.deb
shasum -a 512 kibana-{{stack-version}}-amd64.deb <1>
sudo dpkg -i kibana-{{stack-version}}-amd64.deb
```

1. 	Compare the SHA produced by shasum with the [published SHA](https://artifacts.elastic.co/downloads/kibana/kibana-9.0.0-amd64.deb.sha512).

% version manually specified in the link above

## Start {{es}} and generate an enrollment token for {{kib}} [deb-enroll]

When you start {{es}} for the first time, the following security configuration occurs automatically:

* Authentication and authorization are enabled, and a password is generated for the `elastic` built-in superuser.
* Certificates and keys for TLS are generated for the transport and HTTP layer, and TLS is enabled and configured with these keys and certificates.

The password and certificate and keys are output to your terminal.

You can then generate an enrollment token for {{kib}} with the [`elasticsearch-create-enrollment-token`](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool:

```sh
bin/elasticsearch-create-enrollment-token -s kibana
```

Start {{kib}} and enter the enrollment token to securely connect {{kib}} with {{es}}.


## Run {{kib}} with `systemd` [deb-running-systemd]

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


## Configure {{kib}} via the config file [deb-configuring]

{{kib}} loads its configuration from the `/etc/kibana/kibana.yml` file by default.  The format of this config file is explained in [Configuring Kibana](configure.md).


## Directory layout of Debian package [deb-layout]

The Debian package places config files, logs, and the data directory in the appropriate locations for a Debian-based system:

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | {{kib}} home directory or `$KIBANA_HOME` | `/usr/share/kibana` |  |
| bin | Binary scripts including `kibana` to start the {{kib}} server    and `kibana-plugin` to install plugins | `/usr/share/kibana/bin` |  |
| config | Configuration files including `kibana.yml` | `/etc/kibana` | `[KBN_PATH_CONF](configure.md)` |
| data | The location of the data files written to disk by {{kib}} and its plugins | `/var/lib/kibana` | `path.data` |
| logs | Logs files location | `/var/log/kibana` | `[Logging configuration](../../monitor/logging-configuration/kibana-logging.md)` |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `/usr/share/kibana/plugins` |  |
