---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html
sub:
  es-conf: "$ES_HOME/config"
  slash: "/"
  export: "export"
  escape: "\\"
navigation_title: "Linux or MacOS"
---

# Install {{es}} from archive on Linux or MacOS [targz]

{{es}} is available as a `.tar.gz` archive for Linux and MacOS.

:::{include} _snippets/trial.md
:::

:::{include} _snippets/es-releases.md
:::

::::{note}
{{es}} includes a bundled version of [OpenJDK](https://openjdk.java.net) from the JDK maintainers (GPLv2+CE). To use your own version of Java, see the [JVM version requirements](installing-elasticsearch.md#jvm-version)
::::


## Step 1: Download and install the archive

Download and install the archive for Linux or MacOS.

### Linux [install-linux]

The Linux archive for {{es}} {{stack-version}} can be downloaded and installed as follows:

```sh
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{stack-version}}-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{stack-version}}-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-{{stack-version}}-linux-x86_64.tar.gz.sha512 <1>
tar -xzf elasticsearch-{{stack-version}}-linux-x86_64.tar.gz
cd elasticsearch-{{stack-version}}/ <2>
```

1. Compares the SHA of the downloaded `.tar.gz` archive and the published checksum, which should output `elasticsearch-<version>-linux-x86_64.tar.gz: OK`.
2. This directory is known as `$ES_HOME`.



### MacOS [install-macos]

The MacOS archive for {{es}} {{stack-version}} can be downloaded and installed as follows:

```sh
curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{stack-version}}-darwin-x86_64.tar.gz
curl https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{stack-version}}-darwin-x86_64.tar.gz.sha512 | shasum -a 512 -c - <1>
tar -xzf elasticsearch-{{stack-version}}-darwin-x86_64.tar.gz
cd elasticsearch-{{stack-version}}/ <2>
```

1. Compares the SHA of the downloaded `.tar.gz` archive and the published checksum, which should output `elasticsearch-<version>-darwin-x86_64.tar.gz: OK`.
2. This directory is known as `$ES_HOME`.

::::{admonition} macOS Gatekeeper warnings
:class: important

Apple’s rollout of stricter notarization requirements affected the notarization of the {{stack-version}} {{es}} artifacts. If macOS displays a dialog when you first run {{es}} that interrupts it, then you need to take an action to allow it to run.

To prevent Gatekeeper checks on the {{es}} files, run the following command on the downloaded .tar.gz archive or the directory to which was extracted:

```sh
xattr -d -r com.apple.quarantine <archive-or-directory>
```

Alternatively, you can add a security override by following the instructions in the *If you want to open an app that hasn’t been notarized or is from an unidentified developer* section of [Safely open apps on your Mac](https://support.apple.com/en-us/HT202491).
::::

## Step 2: Enable automatic creation of system indices [targz-enable-indices]

:::{include} _snippets/enable-auto-indices.md
:::

## Step 3: Start {{es}} [targz-running]

You have several options for starting {{es}}

* [Run from the command line](#command-line)
* [Run the node to be enrolled in an existing cluster](#existing-cluster)
* [Run as a daemon](#setup-installation-daemon)

### Run {{es}} from the command line [command-line]

:::{include} _snippets/targz-start.md
:::

#### Security at startup [security-at-startup]

:::{include} _snippets/auto-security-config.md
:::

:::{include} _snippets/pw-env-var.md
:::

### Enroll the node in an existing cluster [existing-cluster]

:::{include} _snippets/enroll-nodes.md
:::

### Run as a daemon [setup-installation-daemon]

:::{include} _snippets/targz-daemon.md
:::

## Step 4: Check that {{es}} is running [_check_that_elasticsearch_is_running]

:::{include} _snippets/check-es-running.md
:::

## Configure {{es}} on the command line [targz-configuring]

{{es}} loads its configuration from the `$ES_HOME/config/elasticsearch.yml` file by default. The format of this config file is explained in [*Configuring {{es}}*](configure-elasticsearch.md).

Any settings that can be specified in the config file can also be specified on the command line, using the `-E` syntax as follows:

```sh
./bin/elasticsearch -d -Ecluster.name=my_cluster -Enode.name=node_1
```

::::{tip}
Typically, any cluster-wide settings (like `cluster.name`) should be added to the `elasticsearch.yml` config file, while any node-specific settings such as `node.name` could be specified on the command line.
::::

## Connect clients to {{es}} [_connect_clients_to_es]

:::{include} _snippets/connect-clients.md
:::

### Use the CA fingerprint [_use_the_ca_fingerprint_2]

:::{include} _snippets/ca-fingerprint.md
:::

### Use the CA certificate [_use_the_ca_certificate_2]

:::{include} _snippets/ca-cert.md
:::

## Directory layout of archives [targz-layout]

The archive distributions are entirely self-contained. All files and directories are, by default, contained within `$ES_HOME` — the directory created when unpacking the archive.

This is very convenient because you don’t have to create any directories to start using {{es}}, and uninstalling {{es}} is as easy as removing the `$ES_HOME` directory. However, it is advisable to change the default locations of the config directory, the data directory, and the logs directory so that you do not delete important data later on.

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | {{es}} home directory or `$ES_HOME` | Directory created by unpacking the archive |  |
| bin | Binary scripts including `elasticsearch` to start a node    and `elasticsearch-plugin` to install plugins | `$ES_HOME/bin` |  |
| conf | Configuration files including `elasticsearch.yml` | `$ES_HOME/config` | `[ES_PATH_CONF](configure-elasticsearch.md#config-files-location)` |
| conf | Generated TLS keys and certificates for the transport and HTTP layer. | `$ES_HOME/config/certs` |  |
| data | The location of the data files of each index / shard allocated    on the node. | `$ES_HOME/data` | `path.data` |
| logs | Log files location. | `$ES_HOME/logs` | `path.logs` |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `$ES_HOME/plugins` |  |
| repo | Shared file system repository locations. Can hold multiple locations. A file system repository can be placed in to any subdirectory of any directory specified here. | Not configured | `path.repo` |

### Security certificates and keys [_security_certificates_and_keys]

:::{include} _snippets/security-files.md
:::

## Next steps [_next_steps]

:::{include} _snippets/install-next-steps.md
:::