---
navigation_title: Debian
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/deb.html
products:
  - id: kibana
---



# Install {{kib}} with Debian package [deb]


The Debian package for {{kib}} can be [downloaded from our website](#install-deb) or from our [APT repository](#deb-repo). It can be used to install {{kib}} on any Debian-based system such as Debian and Ubuntu.

:::{include} _snippets/trial.md
:::

:::{include} _snippets/kib-releases.md
:::

## Step 1: Import the Elastic PGP key [deb-key]

:::{include} _snippets/pgp-key.md
:::

```sh
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
```

## Step 2: Install {{kib}}

You have several options for installing the {{es}} Debian package:

* [From the APT repository](#deb-repo)
* [Manually](#install-deb)

### Install from the APT repository [deb-repo]

1. You may need to install the `apt-transport-https` package on Debian before proceeding:

    ```sh
    sudo apt-get install apt-transport-https
    ```

2. Save the repository definition to `/etc/apt/sources.list.d/elastic-9.x.list`:

    ```sh
    echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/9.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-9.x.list
    ```

3. Install the {{kib}} Debian package:

    ```sh
    sudo apt-get update && sudo apt-get install kibana
    ```

:::{warning}
Do not use `add-apt-repository` as it will add a `deb-src` entry as well, but we do not provide a source package. If you have added the `deb-src` entry, you will see an error like the following:

```
Unable to find expected entry 'main/source/Sources' in Release file
(Wrong sources.list entry or malformed file)
```

Delete the `deb-src` entry from the `/etc/apt/sources.list` file and the installation should work as expected.
:::

:::{warning}
If two entries exist for the same {{kib}} repository, you will see an error like this during `apt-get update`:

```
Duplicate sources.list entry https://artifacts.elastic.co/packages/9.x/apt/ ...`
```

Examine `/etc/apt/sources.list.d/kibana-9.x.list` for the duplicate entry or locate the duplicate entry amongst the files in `/etc/apt/sources.list.d/` and the `/etc/apt/sources.list` file.
:::

### Download and install the Debian package manually [install-deb]

The Debian package for {{kib}} {{version.stack}} can be downloaded from the website and installed as follows:

::::{tab-set}

:::{tab-item} Latest
To download and install the {{kib}} {{version.stack}} package, enter:
```sh subs=true
wget https://artifacts.elastic.co/downloads/kibana/kibana-{{version.stack}}-amd64.deb
shasum -a 512 kibana-{{version.stack}}-amd64.deb <1>
sudo dpkg -i kibana-{{version.stack}}-amd64.deb
```

1. 	Compare the SHA produced by shasum with the [published SHA](https://artifacts.elastic.co/downloads/kibana/kibana-9.0.0-amd64.deb.sha512).
% version manually specified in the link above
:::

:::{tab-item} Specific version
Because {{kib}} is an {{stack}} product, you must install the same version number as the rest of your {{stack}} components. Replace `<SPECIFIC.VERSION.NUMBER>` with the version that's used across your entire stack. For example, you can use {{version.stack.base}}.
```sh subs=true
wget https://artifacts.elastic.co/downloads/kibana/kibana-<SPECIFIC.VERSION.NUMBER>-amd64.deb
shasum -a 512 kibana-<SPECIFIC.VERSION.NUMBER>-amd64.deb <1>
sudo dpkg -i kibana-<SPECIFIC.VERSION.NUMBER>-amd64.deb
```

1. 	Compare the SHA produced by shasum with the [published SHA](https://artifacts.elastic.co/downloads/kibana/kibana-9.0.0-amd64.deb.sha512).
% version manually specified in the link above
:::
::::

## Step 3: Start {{es}} and generate an enrollment token for {{kib}} [deb-enroll]

[Start {{es}}](/deploy-manage/maintenance/start-stop-services/start-stop-elasticsearch.md).

:::{include} _snippets/auto-security-config.md
:::

:::{include} _snippets/new-enrollment-token.md
:::

## Step 4 (Optional): Make {{kib}} externally accessible

:::{include} _snippets/kibana-ip.md
:::

## Step 5: Run {{kib}} with `systemd` [deb-running-systemd]

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

## Step 7: Configure {{kib}} using the config file [deb-configuring]

{{kib}} loads its configuration from the `/etc/kibana/kibana.yml` file by default.  The format of this config file is explained in [](configure-kibana.md).

## Directory layout of Debian package [deb-layout]

The Debian package places config files, logs, and the data directory in the appropriate locations for a Debian-based system:

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