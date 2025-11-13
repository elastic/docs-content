---
navigation_title: Install with Debian package
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
sub:
  es-conf: /etc/elasticsearch
  slash: /
  distro: Debian
  export: "export "
  escape: \
  pkg-conf: /etc/default/elasticsearch
---

# Install {{es}} with a Debian package [deb]

The Debian package for {{es}} can be [downloaded from our website](#install-deb) or from our [APT repository](#deb-repo). It can be used to install {{es}} on any Debian-based system such as Debian and Ubuntu.

:::{include} _snippets/trial.md
:::

:::{include} _snippets/es-releases.md
:::

:::{include} _snippets/java-version.md
:::

## Before you start

:::{include} _snippets/prereqs.md
:::


## Step 1: Import the {{es}} PGP key [deb-key]

:::{include} _snippets/pgp-key.md
:::

```sh
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
```

## Step 2: Install {{es}}

You have several options for installing the {{es}} Debian package:

* [From the APT repository](#deb-repo)
* [Manually](#install-deb)

### Install from the APT repository [deb-repo]

1. You may need to install the `apt-transport-https` package on Debian before proceeding:

    ```sh
    sudo apt-get install apt-transport-https
    ```

2. Save the repository definition to  `/etc/apt/sources.list.d/elastic-9.x.list`:

    ```sh
    echo "deb [signed-by=/usr/share/keyrings/elasticsearch-keyring.gpg] https://artifacts.elastic.co/packages/9.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-9.x.list
    ```

3. Install the {{es}} Debian package:

    ```sh
    sudo apt-get update && sudo apt-get install elasticsearch
    ```

:::{note}
These instructions do not use `add-apt-repository` for several reasons:

1. `add-apt-repository` adds entries to the system `/etc/apt/sources.list` file rather than a clean per-repository file in `/etc/apt/sources.list.d`.
2. `add-apt-repository` is not part of the default install on many distributions and requires a number of non-default dependencies.
3. Older versions of `add-apt-repository` always add a `deb-src` entry which will cause errors because we do not provide a source package. If you have added the `deb-src` entry, you will see an error like the following until you delete the `deb-src` line:

    ```text
    Unable to find expected entry 'main/source/Sources' in Release file
    (Wrong sources.list entry or malformed file)
    ```
:::

:::{warning}
If two entries exist for the same {{es}} repository, you will see an error like this during `apt-get update`:

```text
Duplicate sources.list entry https://artifacts.elastic.co/packages/9.x/apt/ ...
```

Examine `/etc/apt/sources.list.d/elasticsearch-9.x.list` for the duplicate entry or locate the duplicate entry amongst the files in `/etc/apt/sources.list.d/` and the `/etc/apt/sources.list` file.
:::

:::{include} _snippets/skip-set-kernel-params.md
:::

### Download and install the Debian package manually [install-deb]

The Debian package for {{es}} can be downloaded from the website and installed as follows:

::::{tab-set}

:::{tab-item} Latest
To download and install the {{es}} {{version.stack}} package, enter:
```sh subs=true
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{version.stack}}-amd64.deb
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{version.stack}}-amd64.deb.sha512
shasum -a 512 -c elasticsearch-{{version.stack}}-amd64.deb.sha512 <1>
sudo dpkg -i elasticsearch-{{version.stack}}-amd64.deb
```
1. Compares the SHA of the downloaded Debian package and the published checksum, which should output `elasticsearch-<version>-amd64.deb: OK`.
:::

:::{tab-item} Specific version
Replace `<SPECIFIC.VERSION.NUMBER>` with the {{es}} version number you want. For example, you can replace `<SPECIFIC.VERSION.NUMBER>` with {{version.stack.base}}.
```sh subs=true
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-<SPECIFIC.VERSION.NUMBER>-amd64.deb
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-<SPECIFIC.VERSION.NUMBER>-amd64.deb.sha512
shasum -a 512 -c elasticsearch-<SPECIFIC.VERSION.NUMBER>-amd64.deb.sha512 <1>
sudo dpkg -i elasticsearch-<SPECIFIC.VERSION.NUMBER>-amd64.deb
```
1. Compares the SHA of the downloaded Debian package and the published checksum, which should output `elasticsearch-<SPECIFIC.VERSION.NUMBER>-amd64.deb: OK`.
:::
::::

## Step 3: Set up the node for connectivity

:::{include} _snippets/node-connectivity.md
:::

### Set up a node as the first node in a cluster [first-node]

:::{include} _snippets/first-node.md
:::

### Reconfigure a node to join an existing cluster [existing-cluster]

:::{include} _snippets/join-existing-cluster.md
:::

## Step 4: Enable automatic creation of system indices [deb-enable-indices]

:::{include} _snippets/enable-auto-indices.md
:::

## Step 5: Run {{es}} with `systemd` [running-systemd]

:::{include} _snippets/systemd-startup.md
:::

:::{include} _snippets/systemd.md
:::

### Log to the systemd journal

:::{include} _snippets/systemd-journal.md
:::

:::{include} _snippets/systemd-startup-timeout.md
:::

### Security at startup [deb-security-configuration]

:::{include} _snippets/auto-security-config-rpm-deb.md
:::

## Step 6: Reset the `elastic` superuser password

:::{include} _snippets/reset-superuser-rpm-deb.md
:::

:::{include} _snippets/pw-env-var.md
:::

## Step 7: Check that {{es}} is running [deb-check-running]

:::{include} _snippets/check-es-running.md
:::

## Step 8 (Multi-node clusters only): Update the config files [update-config-files]

If you are deploying a multi-node cluster, then the `elasticsearch-reconfigure-node` tool adds all existing nodes to each newly enrolled node's `discovery.seed_hosts` setting. However, you need to go back to all of the nodes in the cluster and edit them so each node in the cluster can restart and rejoin the cluster as expected.

:::{note}
Because the initial node in the cluster is bootstrapped as a single-node cluster, it won't have `discovery.seed_hosts` configured. This setting is mandatory for multi-node clusters and must be added manually to the first node.
:::

:::{include} _snippets/clean-up-multinode.md
:::

## Configuring {{es}} [deb-configuring]

:::{include} _snippets/etc-elasticsearch.md
:::

## Connect clients to {{es}} [_connect_clients_to_es_3]

:::{include} _snippets/connect-clients.md
:::

### Use the CA fingerprint [_use_the_ca_fingerprint_2]

:::{include} _snippets/ca-fingerprint.md
:::

### Use the CA certificate [_use_the_ca_certificate_2]

:::{include} _snippets/ca-cert.md
:::

## Directory layout of Debian package [deb-layout]

The Debian package places config files, logs, and the data directory in the appropriate locations for a Debian-based system:

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | {{es}} home directory or `$ES_HOME` | `/usr/share/elasticsearch` |  |
| bin | Binary scripts including `elasticsearch` to start a node    and `elasticsearch-plugin` to install plugins | `/usr/share/elasticsearch/bin` |  |
| conf | Configuration files including `elasticsearch.yml` | `/etc/elasticsearch` | [`ES_PATH_CONF`](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#config-files-location) |
| conf | Environment variables including heap size, file descriptors. | `/etc/default/elasticsearch` |  |
| conf | Generated TLS keys and certificates for the transport and http layer. | `/etc/elasticsearch/certs` |  |
| data | The location of the data files of each index / shard allocated    on the node. | `/var/lib/elasticsearch` | [`path.data`](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings) |
| jdk | The bundled Java Development Kit used to run {{es}}. Can    be overridden by setting the `ES_JAVA_HOME` environment variable    in `/etc/default/elasticsearch`. | `/usr/share/elasticsearch/jdk` |  |
| logs | Log files location. | `/var/log/elasticsearch` | [`path.logs`](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings) |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `/usr/share/elasticsearch/plugins` |  |
| repo | Shared file system repository locations. Can hold multiple locations. A file system repository can be placed in to any subdirectory of any directory specified here. | Not configured | [`path.repo`](/deploy-manage/tools/snapshot-and-restore/shared-file-system-repository.md) |

## Next steps [_next_steps]

:::{include} _snippets/install-next-steps.md
:::
