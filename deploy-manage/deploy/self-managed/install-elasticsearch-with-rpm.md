---
navigation_title: Install with RPM package
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
sub:
  es-conf: /etc/elasticsearch
  slash: /
  distro: RPM
  export: export
  pkg-conf: /etc/sysconfig/elasticsearch
---

# Install {{es}} with RPM [rpm]

The RPM package for {{es}} can be [downloaded from our website](#install-rpm) or from our  [RPM repository](#rpm-repo). It can be used to install {{es}} on any RPM-based system such as openSUSE, SUSE Linux Enterprise Server (SLES), CentOS, Red Hat Enterprise Linux (RHEL), and Oracle Linux.

::::{note}
RPM install is not supported on distributions with old versions of RPM, such as SLES 11 and CentOS 5. Refer to [Install {{es}} from archive on Linux or MacOS](install-elasticsearch-from-archive-on-linux-macos.md) instead.
::::

:::{include} _snippets/trial.md
:::

:::{include} _snippets/es-releases.md
:::

:::{include} _snippets/java-version.md
:::

## Before you start

:::{include} _snippets/prereqs.md
:::

## Step 1: Import the {{es}} PGP key [rpm-key]

:::{include} _snippets/pgp-key.md
:::

```sh
rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
```

## Step 2: Install {{es}}

You have two options for installing the {{es}} RPM package:

* [From the RPM repository](#rpm-repo)
* [Manually](#install-rpm)

### Install from the RPM repository [rpm-repo]

1. Define a repository for {{es}}.

::::{tab-set}
:group:linux-distros
:::{tab-item} RedHat distributions
:sync: rhel
For RedHat based distributions, create a file called `elasticsearch.repo` in the `/etc/yum.repos.d/` directory and include the following configuration: 

```ini subs=true
[elasticsearch]
name={{es}} repository for 9.x packages
baseurl=https://artifacts.elastic.co/packages/9.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=0
type=rpm-md
```
::: 

:::{tab-item} openSUSE distributions
:sync: suse
For openSUSE based distributions, create a file called `elasticsearch.repo` in the `/etc/zypp/repos.d/` directory and include the following configuration:

```ini subs=true
[elasticsearch]
name={{es}} repository for 9.x packages
baseurl=https://artifacts.elastic.co/packages/9.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=0
autorefresh=1
type=rpm-md
```
:::
:::: 

2. Install {{es}} from the repository you defined earlier.

::::{tab-set}
:group:linux-distros
:::{tab-item} RedHat distributions
:sync: rhel
If you use Fedora, or Red Hat Enterprise Linux 8 and later, enter the following command:

```sh
sudo dnf install --enablerepo=elasticsearch elasticsearch
```

If you use CentOS, or Red Hat Enterprise Linux 7 and earlier, enter the following command:
```sh
sudo yum install --enablerepo=elasticsearch elasticsearch
```
:::
:::{tab-item} openSUSE distributions
:sync: suse
Enter the following command:

```sh
sudo zypper modifyrepo --enable elasticsearch && \
  sudo zypper install elasticsearch; \
  sudo zypper modifyrepo --disable elasticsearch
```
::: 
:::: 


### Download and install the RPM manually [install-rpm]

1. Download and install the RPM for {{es}} with the following commands:

::::{tab-set}

:::{tab-item} Latest
To download and install the {{es}} {{version.stack}} RPM, enter:
  ```sh subs=true
  wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{version.stack}}-x86_64.rpm
  wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{version.stack}}-x86_64.rpm.sha512
  shasum -a 512 -c elasticsearch-{{version.stack}}-x86_64.rpm.sha512 <1>
  sudo rpm --install elasticsearch-{{version.stack}}-x86_64.rpm
  ```
  1. Compares the SHA of the downloaded RPM and the published checksum, which should output `elasticsearch-<version>-x86_64.rpm: OK`.
  
  :::{include} _snippets/skip-set-kernel-params.md
  :::

:::

:::{tab-item} Specific version
Replace `<SPECIFIC.VERSION.NUMBER>` with the {{es}} version number you want. For example, you can replace `<SPECIFIC.VERSION.NUMBER>` with {{version.stack.base}}.
  ```sh subs=true
  wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-<SPECIFIC.VERSION.NUMBER>-x86_64.rpm
  wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-<SPECIFIC.VERSION.NUMBER>-x86_64.rpm.sha512
  shasum -a 512 -c elasticsearch-<SPECIFIC.VERSION.NUMBER>-x86_64.rpm.sha512 <1>
  sudo rpm --install elasticsearch-<SPECIFIC.VERSION.NUMBER>-x86_64.rpm
  ```
  1. Compares the SHA of the downloaded RPM and the published checksum, which should output `elasticsearch-<SPECIFIC.VERSION.NUMBER>-x86_64.rpm: OK`.
  
  :::{include} _snippets/skip-set-kernel-params.md
  :::

:::
::::
 

  


2. Copy the terminal output from the install command to a local file. In particular, you’ll need the password for the built-in `elastic` superuser account. The output also contains the commands to enable {{es}} to [run as a service](#running-systemd).

## Step 3: Set up the node for connectivity

:::{include} _snippets/node-connectivity.md
:::

### Set up a node as the first node in a cluster [first-node]

:::{include} _snippets/first-node.md
:::

### Reconfigure a node to join an existing cluster [existing-cluster]

:::{include} _snippets/join-existing-cluster.md
:::

## Step 4: Enable automatic creation of system indices [rpm-enable-indices]

:::{include} _snippets/enable-auto-indices.md
:::

## Step 5: Run {{es}} with `systemd` [running-systemd]

:::{include} _snippets/systemd.md
:::

### Start {{es}} automatically

:::{include} _snippets/systemd-startup.md
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

## Step 7: Check that {{es}} is running [rpm-check-running]

:::{include} _snippets/check-es-running.md
:::

## Step 8 (Multi-node clusters only): Update the config files [update-config-files]

If you are deploying a multi-node cluster, then the `elasticsearch-reconfigure-node` tool adds all existing nodes to each newly enrolled node's `discovery.seed_hosts` setting. However, you need to go back to all of the nodes in the cluster and edit them so each node in the cluster can restart and rejoin the cluster as expected.

:::{note}
Because the initial node in the cluster is bootstrapped as a single-node cluster, it won't have `discovery.seed_hosts` configured. This setting is mandatory for multi-node clusters and must be added manually to the first node.
:::

:::{include} _snippets/clean-up-multinode.md
:::

## Configuring {{es}} [rpm-configuring]

:::{include} _snippets/etc-elasticsearch.md
:::

## Connect clients to {{es}} [_connect_clients_to_es_4]

:::{include} _snippets/connect-clients.md
:::

### Use the CA fingerprint [_use_the_ca_fingerprint_2]

:::{include} _snippets/ca-fingerprint.md
:::

### Use the CA certificate [_use_the_ca_certificate_2]

:::{include} _snippets/ca-cert.md
:::

## Directory layout of RPM [rpm-layout]

The RPM places config files, logs, and the data directory in the appropriate locations for an RPM-based system:

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home |{{es}} home directory or `$ES_HOME` | `/usr/share/elasticsearch` |  |
| bin | Binary scripts including `elasticsearch` to start a node    and `elasticsearch-plugin` to install plugins | `/usr/share/elasticsearch/bin` |  |
| conf | Configuration files including `elasticsearch.yml` | `/etc/elasticsearch` | [`ES_PATH_CONF`](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#config-files-location) |
| conf | Environment variables including heap size, file descriptors. | `/etc/sysconfig/elasticsearch` |  |
| conf | Generated TLS keys and certificates for the transport and http layer. | `/etc/elasticsearch/certs` |  |
| data | The location of the data files of each index / shard allocated    on the node. | `/var/lib/elasticsearch` | [`path.data`](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings) |
| jdk | The bundled Java Development Kit used to run {{es}}. Can    be overridden by setting the `ES_JAVA_HOME` environment variable    in `/etc/sysconfig/elasticsearch`. | `/usr/share/elasticsearch/jdk` |  |
| logs | Log files location. | `/var/log/elasticsearch` | [`path.logs`](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings) |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `/usr/share/elasticsearch/plugins` |  |
| repo | Shared file system repository locations. Can hold multiple locations. A file system repository can be placed in to any subdirectory of any directory specified here. | Not configured | [`path.repo`](/deploy-manage/tools/snapshot-and-restore/shared-file-system-repository.md) |

## Next steps [_next_steps]

:::{include} _snippets/install-next-steps.md
:::
