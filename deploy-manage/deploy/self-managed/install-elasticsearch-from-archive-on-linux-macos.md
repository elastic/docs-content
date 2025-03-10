---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html
---

# Install Elasticsearch from archive on Linux or MacOS [targz]

{{es}} is available as a `.tar.gz` archive for Linux and MacOS.

This package contains both free and subscription features. [Start a 30-day trial](elasticsearch://reference/elasticsearch/configuration-reference/license-settings.md) to try out all of the features.

The latest stable version of {{es}} can be found on the [Download {{es}}](https://elastic.co/downloads/elasticsearch) page. Other versions can be found on the [Past Releases page](https://elastic.co/downloads/past-releases).

::::{note}
{{es}} includes a bundled version of [OpenJDK](https://openjdk.java.net) from the JDK maintainers (GPLv2+CE). To use your own version of Java, see the [JVM version requirements](installing-elasticsearch.md#jvm-version)
::::


## Download and install archive for Linux [install-linux]

::::{warning}
Version 9.0.0-beta1 of {{es}} has not yet been released. The archive might not be available.
::::


The Linux archive for {{es}} v9.0.0-beta1 can be downloaded and installed as follows:

```sh
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-linux-x86_64.tar.gz
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-linux-x86_64.tar.gz.sha512
shasum -a 512 -c elasticsearch-9.0.0-beta1-linux-x86_64.tar.gz.sha512 <1>
tar -xzf elasticsearch-9.0.0-beta1-linux-x86_64.tar.gz
cd elasticsearch-9.0.0-beta1/ <2>
```

1. Compares the SHA of the downloaded `.tar.gz` archive and the published checksum, which should output `elasticsearch-{{version}}-linux-x86_64.tar.gz: OK`.
2. This directory is known as `$ES_HOME`.



## Download and install archive for MacOS [install-macos]

::::{warning}
Version 9.0.0-beta1 of {{es}} has not yet been released. The archive might not be available.
::::


::::{admonition} macOS Gatekeeper warnings
:class: important

Apple’s rollout of stricter notarization requirements affected the notarization of the 9.0.0-beta1 {{es}} artifacts. If macOS displays a dialog when you first run {{es}} that interrupts it, then you need to take an action to allow it to run.

To prevent Gatekeeper checks on the {{es}} files, run the following command on the downloaded .tar.gz archive or the directory to which was extracted:

```sh
xattr -d -r com.apple.quarantine <archive-or-directory>
```

Alternatively, you can add a security override by following the instructions in the *If you want to open an app that hasn’t been notarized or is from an unidentified developer* section of [Safely open apps on your Mac](https://support.apple.com/en-us/HT202491).

::::


The MacOS archive for {{es}} v9.0.0-beta1 can be downloaded and installed as follows:

```sh
curl -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-darwin-x86_64.tar.gz
curl https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-darwin-x86_64.tar.gz.sha512 | shasum -a 512 -c - <1>
tar -xzf elasticsearch-9.0.0-beta1-darwin-x86_64.tar.gz
cd elasticsearch-9.0.0-beta1/ <2>
```

1. Compares the SHA of the downloaded `.tar.gz` archive and the published checksum, which should output `elasticsearch-{{version}}-darwin-x86_64.tar.gz: OK`.
2. This directory is known as `$ES_HOME`.
%  NOTCONSOLE


## Enable automatic creation of system indices [targz-enable-indices]

Some commercial features automatically create indices within {{es}}. By default, {{es}} is configured to allow automatic index creation, and no additional steps are required. However, if you have disabled automatic index creation in {{es}}, you must configure [`action.auto_create_index`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create) in `elasticsearch.yml` to allow the commercial features to create the following indices:

```yaml
action.auto_create_index: .monitoring*,.watches,.triggered_watches,.watcher-history*,.ml*
```

::::{important}
If you are using [Logstash](https://www.elastic.co/products/logstash) or [Beats](https://www.elastic.co/products/beats) then you will most likely require additional index names in your `action.auto_create_index` setting, and the exact value will depend on your local configuration. If you are unsure of the correct value for your environment, you may consider setting the value to `*` which will allow automatic creation of all indices.

::::



## Run {{es}} from the command line [targz-running]

Run the following command to start {{es}} from the command line:

```sh
./bin/elasticsearch
```

When starting {{es}} for the first time, security features are enabled and configured by default. The following security configuration occurs automatically:

* Authentication and authorization are enabled, and a password is generated for the `elastic` built-in superuser.
* Certificates and keys for TLS are generated for the transport and HTTP layer, and TLS is enabled and configured with these keys and certificates.
* An enrollment token is generated for {{kib}}, which is valid for 30 minutes.

The password for the `elastic` user and the enrollment token for {{kib}} are output to your terminal.

We recommend storing the `elastic` password as an environment variable in your shell. Example:

```sh
export ELASTIC_PASSWORD="your_password"
```

If you have password-protected the {{es}} keystore, you will be prompted to enter the keystore’s password. See [Secure settings](../../security/secure-settings.md) for more details.

By default {{es}} prints its logs to the console (`stdout`) and to the `<cluster name>.log` file within the [logs directory](important-settings-configuration.md#path-settings). {{es}} logs some information while it is starting, but after it has finished initializing it will continue to run in the foreground and won’t log anything further until something happens that is worth recording. While {{es}} is running you can interact with it through its HTTP interface which is on port `9200` by default.

To stop {{es}}, press `Ctrl-C`.

::::{note}
All scripts packaged with {{es}} require a version of Bash that supports arrays and assume that Bash is available at `/bin/bash`. As such, Bash should be available at this path either directly or via a symbolic link.
::::



### Enroll nodes in an existing cluster [_enroll_nodes_in_an_existing_cluster]

When {{es}} starts for the first time, the security auto-configuration process binds the HTTP layer to `0.0.0.0`, but only binds the transport layer to localhost. This intended behavior ensures that you can start a single-node cluster with security enabled by default without any additional configuration.

Before enrolling a new node, additional actions such as binding to an address other than `localhost` or satisfying bootstrap checks are typically necessary in production clusters. During that time, an auto-generated enrollment token could expire, which is why enrollment tokens aren’t generated automatically.

Additionally, only nodes on the same host can join the cluster without additional configuration. If you want nodes from another host to join your cluster, you need to set `transport.host` to a [supported value](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#network-interface-values) (such as uncommenting the suggested value of `0.0.0.0`), or an IP address that’s bound to an interface where other hosts can reach it. Refer to [transport settings](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#transport-settings) for more information.

To enroll new nodes in your cluster, create an enrollment token with the `elasticsearch-create-enrollment-token` tool on any existing node in your cluster. You can then start a new node with the `--enrollment-token` parameter so that it joins an existing cluster.

1. In a separate terminal from where {{es}} is running, navigate to the directory where you installed {{es}} and run the [`elasticsearch-create-enrollment-token`](elasticsearch://reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool to generate an enrollment token for your new nodes.

    ```sh
    bin/elasticsearch-create-enrollment-token -s node
    ```

    Copy the enrollment token, which you’ll use to enroll new nodes with your {{es}} cluster.

2. From the installation directory of your new node, start {{es}} and pass the enrollment token with the `--enrollment-token` parameter.

    ```sh
    bin/elasticsearch --enrollment-token <enrollment-token>
    ```

    {{es}} automatically generates certificates and keys in the following directory:

    ```sh
    config/certs
    ```

3. Repeat the previous step for any new nodes that you want to enroll.


## Check that Elasticsearch is running [_check_that_elasticsearch_is_running]

You can test that your {{es}} node is running by sending an HTTPS request to port `9200` on `localhost`:

```sh
curl --cacert $ES_HOME/config/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200 <1>
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

Log printing to `stdout` can be disabled using the `-q` or `--quiet` option on the command line.


## Run as a daemon [setup-installation-daemon]

To run Elasticsearch as a daemon, specify `-d` on the command line, and record the process ID in a file using the `-p` option:

```sh
./bin/elasticsearch -d -p pid
```

If you have password-protected the {{es}} keystore, you will be prompted to enter the keystore’s password. See [Secure settings](../../security/secure-settings.md) for more details.

Log messages can be found in the `$ES_HOME/logs/` directory.

To shut down Elasticsearch, kill the process ID recorded in the `pid` file:

```sh
pkill -F pid
```

::::{note}
The {{es}} `.tar.gz` package does not include the `systemd` module. To manage {{es}} as a service, use the [Debian](../../maintenance/start-stop-services/start-stop-elasticsearch.md#start-deb) or [RPM](../../maintenance/start-stop-services/start-stop-elasticsearch.md#start-rpm) package instead.
::::



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

When you start {{es}} for the first time, TLS is configured automatically for the HTTP layer. A CA certificate is generated and stored on disk at:

```sh
$ES_HOME/config/certs/http_ca.crt
```

The hex-encoded SHA-256 fingerprint of this certificate is also output to the terminal. Any clients that connect to {{es}}, such as the [{{es}} Clients](https://www.elastic.co/guide/en/elasticsearch/client/index.html), {{beats}}, standalone {{agent}}s, and {{ls}} must validate that they trust the certificate that {{es}} uses for HTTPS. {{fleet-server}} and {{fleet}}-managed {{agent}}s are automatically configured to trust the CA certificate. Other clients can establish trust by using either the fingerprint of the CA certificate or the CA certificate itself.

If the auto-configuration process already completed, you can still obtain the fingerprint of the security certificate. You can also copy the CA certificate to your machine and configure your client to use it.


#### Use the CA fingerprint [_use_the_ca_fingerprint]

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


#### Use the CA certificate [_use_the_ca_certificate]

If your library doesn’t support a method of validating the fingerprint, the auto-generated CA certificate is created in the following directory on each {{es}} node:

```sh
$ES_HOME/config/certs/http_ca.crt
```

Copy the `http_ca.crt` file to your machine and configure your client to use this certificate to establish trust when it connects to {{es}}.


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



## Next steps [_next_steps]

You now have a test {{es}} environment set up. Before you start serious development or go into production with {{es}}, you must do some additional setup:

* Learn how to [configure Elasticsearch](configure-elasticsearch.md).
* Configure [important Elasticsearch settings](important-settings-configuration.md).
* Configure [important system settings](important-system-configuration.md).
