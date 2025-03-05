---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/rpm.html
sub:
  es-conf: "/etc/elasticsearch"
  slash: "/"
  distro: "RPM"
  export: "export"
  escape: "\\"
  stack-version: "9.0.0"
navigation_title: "RPM"
---

# Install {{es}} with RPM [rpm]

The RPM package for {{es}} can be [downloaded from our website](#install-rpm) or from our  [RPM repository](#rpm-repo). It can be used to install {{es}} on any RPM-based system such as OpenSuSE, SLES, Centos, Red Hat, and Oracle Enterprise.

::::{note}
RPM install is not supported on distributions with old versions of RPM, such as SLES 11 and CentOS 5. Please see [Install {{es}} from archive on Linux or MacOS](install-elasticsearch-from-archive-on-linux-macos.md) instead.
::::

:::{include} _snippets/trial.md
:::

:::{include} _snippets/es-releases.md
:::

::::{note}
{{es}} includes a bundled version of [OpenJDK](https://openjdk.java.net) from the JDK maintainers (GPLv2+CE). To use your own version of Java, see the [JVM version requirements](installing-elasticsearch.md#jvm-version)
::::

::::{tip}
For a step-by-step example of setting up the {{stack}} on your own premises, try out our tutorial: [Installing a self-managed Elastic Stack](installing-elasticsearch.md).
::::

## Import the {{es}} PGP key [rpm-key]

:::{include} _snippets/pgp-key.md
:::

```sh
rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
```

## Installing from the RPM repository [rpm-repo]

Create a file called `elasticsearch.repo` in the `/etc/yum.repos.d/` directory for RedHat based distributions, or in the `/etc/zypp/repos.d/` directory for OpenSuSE based distributions, containing:

## Download and install the RPM manually [install-rpm]

The RPM for {{es}} {{stack-version}} can be downloaded from the website and installed as follows:

```sh
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{stack-version}}-x86_64.rpm
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{stack-version}}-x86_64.rpm.sha512
shasum -a 512 -c elasticsearch-{{stack-version}}-x86_64.rpm.sha512 <1>
sudo rpm --install elasticsearch-{{stack-version}}-x86_64.rpm
```

1. Compares the SHA of the downloaded RPM and the published checksum, which should output `elasticsearch-{{version}}-x86_64.rpm: OK`.

:::{include} _snippets/skip-set-kernel-params.md
:::

## Start {{es}} with security enabled [rpm-security-configuration]

:::{include} _snippets/auto-security-config.md
:::

:::{include} _snippets/pw-env-var.md
:::

### Reconfigure a node to join an existing cluster [_reconfigure_a_node_to_join_an_existing_cluster_2]

:::{include} _snippets/join-existing-cluster.md
:::

## Enable automatic creation of system indices [rpm-enable-indices]

:::{include} _snippets/enable-auto-indices.md
:::

## Running {{es}} with `systemd` [running-systemd]

:::{include} _snippets/systemd.md
:::

## Check that {{es}} is running [rpm-check-running]

:::{include} _snippets/check-es-running.md
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
| conf | Configuration files including `elasticsearch.yml` | `/etc/elasticsearch` | `[ES_PATH_CONF](configure-elasticsearch.md#config-files-location)` |
| conf | Environment variables including heap size, file descriptors. | `/etc/sysconfig/elasticsearch` |  |
| conf | Generated TLS keys and certificates for the transport and http layer. | `/etc/elasticsearch/certs` |  |
| data | The location of the data files of each index / shard allocated    on the node. | `/var/lib/elasticsearch` | `path.data` |
| jdk | The bundled Java Development Kit used to run {{es}}. Can    be overridden by setting the `ES_JAVA_HOME` environment variable    in `/etc/sysconfig/elasticsearch`. | `/usr/share/elasticsearch/jdk` |  |
| logs | Log files location. | `/var/log/elasticsearch` | `path.logs` |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `/usr/share/elasticsearch/plugins` |  |
| repo | Shared file system repository locations. Can hold multiple locations. A file system repository can be placed in to any subdirectory of any directory specified here. | Not configured | `path.repo` |

### Security certificates and keys [_security_certificates_and_keys]

:::{include} _snippets/security-files.md
:::

## Next steps [_next_steps]

:::{include} _snippets/install-next-steps.md
:::
