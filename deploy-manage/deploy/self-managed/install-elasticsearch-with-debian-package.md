---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/deb.html
---

# Install Elasticsearch with Debian Package [deb]

The Debian package for Elasticsearch can be [downloaded from our website](#install-deb) or from our [APT repository](#deb-repo). It can be used to install Elasticsearch on any Debian-based system such as Debian and Ubuntu.

This package contains both free and subscription features. [Start a 30-day trial](elasticsearch://reference/elasticsearch/configuration-reference/license-settings.md) to try out all of the features.

The latest stable version of Elasticsearch can be found on the [Download Elasticsearch](https://elastic.co/downloads/elasticsearch) page. Other versions can be found on the [Past Releases page](https://elastic.co/downloads/past-releases).

::::{note}
Elasticsearch includes a bundled version of [OpenJDK](https://openjdk.java.net) from the JDK maintainers (GPLv2+CE). To use your own version of Java, see the [JVM version requirements](installing-elasticsearch.md#jvm-version)
::::


## Import the Elasticsearch PGP Key [deb-key]

We sign all of our packages with the Elasticsearch Signing Key (PGP key [D88E42B4](https://pgp.mit.edu/pks/lookup?op=vindex&search=0xD27D666CD88E42B4), available from [https://pgp.mit.edu](https://pgp.mit.edu)) with fingerprint:

```
4609 5ACC 8548 582C 1A26 99A9 D27D 666C D88E 42B4
```
Download and install the public signing key:

```sh
wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo gpg --dearmor -o /usr/share/keyrings/elasticsearch-keyring.gpg
```


## Installing from the APT repository [deb-repo]

::::{warning}
Version 9.0.0-beta1 of Elasticsearch has not yet been released.
::::


You may need to install the `apt-transport-https` package on Debian before proceeding:

```sh
sudo apt-get install apt-transport-https
```

Save the repository definition to  `/etc/apt/sources.list.d/elastic-9.x.list`:

::::{note}
On systemd-based distributions, the installation scripts will attempt to set kernel parameters (e.g., `vm.max_map_count`); you can skip this by masking the systemd-sysctl.service unit.
::::



## Download and install the Debian package manually [install-deb]

::::{warning}
Version 9.0.0-beta1 of Elasticsearch has not yet been released. The package might not be available.
::::


The Debian package for Elasticsearch v9.0.0-beta1 can be downloaded from the website and installed as follows:

```sh
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-amd64.deb
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-amd64.deb.sha512
shasum -a 512 -c elasticsearch-9.0.0-beta1-amd64.deb.sha512 <1>
sudo dpkg -i elasticsearch-9.0.0-beta1-amd64.deb
```

1. Compares the SHA of the downloaded Debian package and the published checksum, which should output `elasticsearch-{{version}}-amd64.deb: OK`.



## Start {{es}} with security enabled [deb-security-configuration]

When installing {{es}}, security features are enabled and configured by default. When you install {{es}}, the following security configuration occurs automatically:

* Authentication and authorization are enabled, and a password is generated for the `elastic` built-in superuser.
* Certificates and keys for TLS are generated for the transport and HTTP layer, and TLS is enabled and configured with these keys and certificates.

The password and certificate and keys are output to your terminal. You can reset the password for the `elastic` user with the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) command.

We recommend storing the `elastic` password as an environment variable in your shell. For example:

```sh
export ELASTIC_PASSWORD="your_password"
```

### Reconfigure a node to join an existing cluster [_reconfigure_a_node_to_join_an_existing_cluster]

When you install {{es}}, the installation process configures a single-node cluster by default. If you want a node to join an existing cluster instead, generate an enrollment token on an existing node *before* you start the new node for the first time.

1. On any node in your existing cluster, generate a node enrollment token:

    ```sh
    /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s node
    ```

2. Copy the enrollment token, which is output to your terminal.
3. On your new {{es}} node, pass the enrollment token as a parameter to the `elasticsearch-reconfigure-node` tool:

    ```sh
    /usr/share/elasticsearch/bin/elasticsearch-reconfigure-node --enrollment-token <enrollment-token>
    ```

    {{es}} is now configured to join the existing cluster.

4. [Start your new node using `systemd`](#deb-running-systemd).



## Enable automatic creation of system indices [deb-enable-indices]

Some commercial features automatically create indices within {{es}}. By default, {{es}} is configured to allow automatic index creation, and no additional steps are required. However, if you have disabled automatic index creation in {{es}}, you must configure [`action.auto_create_index`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create) in `elasticsearch.yml` to allow the commercial features to create the following indices:

```yaml
action.auto_create_index: .monitoring*,.watches,.triggered_watches,.watcher-history*,.ml*
```

::::{important}
If you are using [Logstash](https://www.elastic.co/products/logstash) or [Beats](https://www.elastic.co/products/beats) then you will most likely require additional index names in your `action.auto_create_index` setting, and the exact value will depend on your local configuration. If you are unsure of the correct value for your environment, you may consider setting the value to `*` which will allow automatic creation of all indices.

::::



## Running Elasticsearch with `systemd` [deb-running-systemd]

To configure Elasticsearch to start automatically when the system boots up, run the following commands:

```sh
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl enable elasticsearch.service
```

Elasticsearch can be started and stopped as follows:

```sh
sudo systemctl start elasticsearch.service
sudo systemctl stop elasticsearch.service
```

These commands provide no feedback as to whether Elasticsearch was started successfully or not. Instead, this information will be written in the log files located in `/var/log/elasticsearch/`.

If you have password-protected your {{es}} keystore, you will need to provide `systemd` with the keystore password using a local file and systemd environment variables. This local file should be protected while it exists and may be safely deleted once Elasticsearch is up and running.

```sh
echo "keystore_password" > /path/to/my_pwd_file.tmp
chmod 600 /path/to/my_pwd_file.tmp
sudo systemctl set-environment ES_KEYSTORE_PASSPHRASE_FILE=/path/to/my_pwd_file.tmp
sudo systemctl start elasticsearch.service
```

By default the Elasticsearch service doesn’t log information in the `systemd` journal. To enable `journalctl` logging, the `--quiet` option must be removed from the `ExecStart` command line in the `elasticsearch.service` file.

When `systemd` logging is enabled, the logging information are available using the `journalctl` commands:

To tail the journal:

```sh
sudo journalctl -f
```

To list journal entries for the elasticsearch service:

```sh
sudo journalctl --unit elasticsearch
```

To list journal entries for the elasticsearch service starting from a given time:

```sh
sudo journalctl --unit elasticsearch --since  "2016-10-30 18:17:16"
```

Check `man journalctl` or [https://www.freedesktop.org/software/systemd/man/journalctl.html](https://www.freedesktop.org/software/systemd/man/journalctl.html) for more command line options.

::::{admonition} Startup timeouts with older `systemd` versions
:class: tip

By default {{es}} sets the `TimeoutStartSec` parameter to `systemd` to `900s`. If you are running at least version 238 of `systemd` then {{es}} can automatically extend the startup timeout, and will do so repeatedly until startup is complete even if it takes longer than 900s.

Versions of `systemd` prior to 238 do not support the timeout extension mechanism and will terminate the {{es}} process if it has not fully started up within the configured timeout. If this happens, {{es}} will report in its logs that it was shut down normally a short time after it started:

```text
[2022-01-31T01:22:31,077][INFO ][o.e.n.Node               ] [instance-0000000123] starting ...
...
[2022-01-31T01:37:15,077][INFO ][o.e.n.Node               ] [instance-0000000123] stopping ...
```

However the `systemd` logs will report that the startup timed out:

```text
Jan 31 01:22:30 debian systemd[1]: Starting Elasticsearch...
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Start operation timed out. Terminating.
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Main process exited, code=killed, status=15/TERM
Jan 31 01:37:15 debian systemd[1]: elasticsearch.service: Failed with result 'timeout'.
Jan 31 01:37:15 debian systemd[1]: Failed to start Elasticsearch.
```

To avoid this, upgrade your `systemd` to at least version 238. You can also temporarily work around the problem by extending the `TimeoutStartSec` parameter.

::::



## Check that Elasticsearch is running [deb-check-running]

You can test that your {{es}} node is running by sending an HTTPS request to port `9200` on `localhost`:

```sh
curl --cacert /etc/elasticsearch/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200 <1>
```

1. Ensure that you use `https` in your call, or the request will fail.`--cacert`
:   Path to the generated `http_ca.crt` certificate for the HTTP layer.
%  NOTCONSOLE


The call returns a response like this:

```js
{
  "name" : "Cp8oag6",
  "cluster_name" : "elasticsearch",
  "cluster_uuid" : "AT69_T_DTp-1qgIJlatQqA",
  "version" : {
    "number" : "9.0.0-SNAPSHOT",
    "build_type" : "tar",
    "build_hash" : "f27399d",
    "build_flavor" : "default",
    "build_date" : "2016-03-30T09:51:41.449Z",
    "build_snapshot" : false,
    "lucene_version" : "10.0.0",
    "minimum_wire_compatibility_version" : "1.2.3",
    "minimum_index_compatibility_version" : "1.2.3"
  },
  "tagline" : "You Know, for Search"
}
```


## Configuring Elasticsearch [deb-configuring]

The `/etc/elasticsearch` directory contains the default runtime configuration for {{es}}. The ownership of this directory and all contained files are set to `root:elasticsearch` on package installations.

The `setgid` flag applies group permissions on the `/etc/elasticsearch` directory to ensure that {{es}} can read any contained files and subdirectories. All files and subdirectories inherit the `root:elasticsearch` ownership. Running commands from this directory or any subdirectories, such as the [elasticsearch-keystore tool](../../security/secure-settings.md), requires `root:elasticsearch` permissions.

Elasticsearch loads its configuration from the `/etc/elasticsearch/elasticsearch.yml` file by default. The format of this config file is explained in [*Configuring {{es}}*](configure-elasticsearch.md).

The Debian package also has a system configuration file (`/etc/default/elasticsearch`), which allows you to set the following parameters:

`ES_JAVA_HOME`
:   Set a custom Java path to be used.

`ES_PATH_CONF`
:   Configuration file directory (which needs to include `elasticsearch.yml`, `jvm.options`, and `log4j2.properties` files); defaults to `/etc/elasticsearch`.

`ES_JAVA_OPTS`
:   Any additional JVM system properties you may want to apply.

`RESTART_ON_UPGRADE`
:   Configure restart on package upgrade, defaults to `false`. This means you will have to restart your Elasticsearch instance after installing a package manually. The reason for this is to ensure, that upgrades in a cluster do not result in a continuous shard reallocation resulting in high network traffic and reducing the response times of your cluster.

::::{note}
Distributions that use `systemd` require that system resource limits be configured via `systemd` rather than via the `/etc/sysconfig/elasticsearch` file. See [Systemd configuration](setting-system-settings.md#systemd) for more information.
::::



## Connect clients to {{es}} [_connect_clients_to_es_3]

When you start {{es}} for the first time, TLS is configured automatically for the HTTP layer. A CA certificate is generated and stored on disk at:

```sh
/etc/elasticsearch/certs/http_ca.crt
```

The hex-encoded SHA-256 fingerprint of this certificate is also output to the terminal. Any clients that connect to {{es}}, such as the [{{es}} Clients](https://www.elastic.co/guide/en/elasticsearch/client/index.html), {{beats}}, standalone {{agent}}s, and {{ls}} must validate that they trust the certificate that {{es}} uses for HTTPS. {{fleet-server}} and {{fleet}}-managed {{agent}}s are automatically configured to trust the CA certificate. Other clients can establish trust by using either the fingerprint of the CA certificate or the CA certificate itself.

If the auto-configuration process already completed, you can still obtain the fingerprint of the security certificate. You can also copy the CA certificate to your machine and configure your client to use it.


#### Use the CA fingerprint [_use_the_ca_fingerprint_3]

Copy the fingerprint value that’s output to your terminal when {{es}} starts, and configure your client to use this fingerprint to establish trust when it connects to {{es}}.

If the auto-configuration process already completed, you can still obtain the fingerprint of the security certificate by running the following command. The path is to the auto-generated CA certificate for the HTTP layer.

```sh
openssl x509 -fingerprint -sha256 -in config/certs/http_ca.crt
```

The command returns the security certificate, including the fingerprint. The `issuer` should be `Elasticsearch security auto-configuration HTTP CA`.

```sh
issuer= /CN=Elasticsearch security auto-configuration HTTP CA
SHA256 Fingerprint=<fingerprint>
```


#### Use the CA certificate [_use_the_ca_certificate_3]

If your library doesn’t support a method of validating the fingerprint, the auto-generated CA certificate is created in the following directory on each {{es}} node:

```sh
/etc/elasticsearch/certs/http_ca.crt
```

Copy the `http_ca.crt` file to your machine and configure your client to use this certificate to establish trust when it connects to {{es}}.


## Directory layout of Debian package [deb-layout]

The Debian package places config files, logs, and the data directory in the appropriate locations for a Debian-based system:

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | Elasticsearch home directory or `$ES_HOME` | `/usr/share/elasticsearch` |  |
| bin | Binary scripts including `elasticsearch` to start a node    and `elasticsearch-plugin` to install plugins | `/usr/share/elasticsearch/bin` |  |
| conf | Configuration files including `elasticsearch.yml` | `/etc/elasticsearch` | `[ES_PATH_CONF](configure-elasticsearch.md#config-files-location)` |
| conf | Environment variables including heap size, file descriptors. | `/etc/default/elasticsearch` |  |
| conf | Generated TLS keys and certificates for the transport and http layer. | `/etc/elasticsearch/certs` |  |
| data | The location of the data files of each index / shard allocated    on the node. | `/var/lib/elasticsearch` | `path.data` |
| jdk | The bundled Java Development Kit used to run Elasticsearch. Can    be overridden by setting the `ES_JAVA_HOME` environment variable    in `/etc/default/elasticsearch`. | `/usr/share/elasticsearch/jdk` |  |
| logs | Log files location. | `/var/log/elasticsearch` | `path.logs` |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `/usr/share/elasticsearch/plugins` |  |
| repo | Shared file system repository locations. Can hold multiple locations. A file system repository can be placed in to any subdirectory of any directory specified here. | Not configured | `path.repo` |

### Security certificates and keys [_security_certificates_and_keys_2]

When you install {{es}}, the following certificates and keys are generated in the {{es}} configuration directory, which are used to connect a {{kib}} instance to your secured {{es}} cluster and to encrypt internode communication. The files are listed here for reference.

`http_ca.crt`
:   The CA certificate that is used to sign the certificates for the HTTP layer of this {{es}} cluster.

`http.p12`
:   Keystore that contains the key and certificate for the HTTP layer for this node.

`transport.p12`
:   Keystore that contains the key and certificate for the transport layer for all the nodes in your cluster.

`http.p12` and `transport.p12` are password-protected PKCS#12 keystores. {{es}} stores the passwords for these keystores as [secure settings](../../security/secure-settings.md). To retrieve the passwords so that you can inspect or change the keystore contents, use the [`bin/elasticsearch-keystore`](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-keystore.md) tool.

Use the following command to retrieve the password for `http.p12`:

```sh
bin/elasticsearch-keystore show xpack.security.http.ssl.keystore.secure_password
```

Use the following command to retrieve the password for `transport.p12`:

```sh
bin/elasticsearch-keystore show xpack.security.transport.ssl.keystore.secure_password
```



## Next steps [_next_steps_3]

You now have a test {{es}} environment set up. Before you start serious development or go into production with {{es}}, you must do some additional setup:

* Learn how to [configure Elasticsearch](configure-elasticsearch.md).
* Configure [important Elasticsearch settings](important-settings-configuration.md).
* Configure [important system settings](important-system-configuration.md).
