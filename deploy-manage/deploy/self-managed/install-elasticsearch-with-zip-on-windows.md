---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/zip-windows.html
---

# Install Elasticsearch with .zip on Windows [zip-windows]

{{es}} can be installed on Windows using the Windows `.zip` archive. This comes with a `elasticsearch-service.bat` command which will setup {{es}} to run as a service.

This package contains both free and subscription features. [Start a 30-day trial](elasticsearch://reference/elasticsearch/configuration-reference/license-settings.md) to try out all of the features.

::::{note}
On Windows the {{es}} {{ml}} feature requires the Microsoft Universal C Runtime library. This is built into Windows 10, Windows Server 2016 and more recent versions of Windows. For older versions of Windows it can be installed via Windows Update, or from a [separate download](https://support.microsoft.com/en-us/help/2999226/update-for-universal-c-runtime-in-windows). If you cannot install the Microsoft Universal C Runtime library you can still use the rest of {{es}} if you disable the {{ml}} feature.
::::


The latest stable version of {{es}} can be found on the [Download {{es}}](https://elastic.co/downloads/elasticsearch) page. Other versions can be found on the [Past Releases page](https://elastic.co/downloads/past-releases).

::::{note}
{{es}} includes a bundled version of [OpenJDK](https://openjdk.java.net) from the JDK maintainers (GPLv2+CE). To use your own version of Java, see the [JVM version requirements](installing-elasticsearch.md#jvm-version)
::::


## Download and install the `.zip` package [install-windows]

::::{warning}
Version 9.0.0-beta1 of {{es}} has not yet been released. The archive might not be available.
::::


Download the `.zip` archive for {{es}} 9.0.0-beta1 from: [https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-windows-x86_64.zip](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-9.0.0-beta1-windows-x86_64.zip)

Unzip it with your favorite unzip tool. This will create a folder called `elasticsearch-9.0.0-beta1`, which we will refer to as `%ES_HOME%`. In a terminal window, `cd` to the `%ES_HOME%` directory, for instance:

```sh
cd C:\Program Files\elasticsearch-9.0.0-beta1
```


## Enable automatic creation of system indices [windows-enable-indices]

Some commercial features automatically create indices within {{es}}. By default, {{es}} is configured to allow automatic index creation, and no additional steps are required. However, if you have disabled automatic index creation in {{es}}, you must configure [`action.auto_create_index`](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-create) in `elasticsearch.yml` to allow the commercial features to create the following indices:

```yaml
action.auto_create_index: .monitoring*,.watches,.triggered_watches,.watcher-history*,.ml*
```

::::{important}
If you are using [Logstash](https://www.elastic.co/products/logstash) or [Beats](https://www.elastic.co/products/beats) then you will most likely require additional index names in your `action.auto_create_index` setting, and the exact value will depend on your local configuration. If you are unsure of the correct value for your environment, you may consider setting the value to `*` which will allow automatic creation of all indices.

::::



## Run {{es}} from the command line [windows-running]

Run the following command to start {{es}} from the command line:

```sh
.\bin\elasticsearch.bat
```

When starting {{es}} for the first time, security features are enabled and configured by default. The following security configuration occurs automatically:

* Authentication and authorization are enabled, and a password is generated for the `elastic` built-in superuser.
* Certificates and keys for TLS are generated for the transport and HTTP layer, and TLS is enabled and configured with these keys and certificates.
* An enrollment token is generated for {{kib}}, which is valid for 30 minutes.

The password for the `elastic` user and the enrollment token for {{kib}} are output to your terminal.

We recommend storing the `elastic` password as an environment variable in your shell. Example:

```sh
$ELASTIC_PASSWORD = "your_password"
```

If you have password-protected the {{es}} keystore, you will be prompted to enter the keystore’s password. See [Secure settings](../../security/secure-settings.md) for more details.

By default {{es}} prints its logs to the console (`STDOUT`) and to the `<cluster name>.log` file within the [logs directory](important-settings-configuration.md#path-settings). {{es}} logs some information while it is starting, but after it has finished initializing it will continue to run in the foreground and won’t log anything further until something happens that is worth recording. While {{es}} is running you can interact with it through its HTTP interface which is on port `9200` by default.

To stop {{es}}, press `Ctrl-C`.


### Enroll nodes in an existing cluster [_enroll_nodes_in_an_existing_cluster_2]

When {{es}} starts for the first time, the security auto-configuration process binds the HTTP layer to `0.0.0.0`, but only binds the transport layer to localhost. This intended behavior ensures that you can start a single-node cluster with security enabled by default without any additional configuration.

Before enrolling a new node, additional actions such as binding to an address other than `localhost` or satisfying bootstrap checks are typically necessary in production clusters. During that time, an auto-generated enrollment token could expire, which is why enrollment tokens aren’t generated automatically.

Additionally, only nodes on the same host can join the cluster without additional configuration. If you want nodes from another host to join your cluster, you need to set `transport.host` to a [supported value](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#network-interface-values) (such as uncommenting the suggested value of `0.0.0.0`), or an IP address that’s bound to an interface where other hosts can reach it. Refer to [transport settings](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#transport-settings) for more information.

To enroll new nodes in your cluster, create an enrollment token with the `elasticsearch-create-enrollment-token` tool on any existing node in your cluster. You can then start a new node with the `--enrollment-token` parameter so that it joins an existing cluster.

1. In a separate terminal from where {{es}} is running, navigate to the directory where you installed {{es}} and run the [`elasticsearch-create-enrollment-token`](elasticsearch://reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool to generate an enrollment token for your new nodes.

    ```sh
    bin\elasticsearch-create-enrollment-token -s node
    ```

    Copy the enrollment token, which you’ll use to enroll new nodes with your {{es}} cluster.

2. From the installation directory of your new node, start {{es}} and pass the enrollment token with the `--enrollment-token` parameter.

    ```sh
    bin\elasticsearch --enrollment-token <enrollment-token>
    ```

    {{es}} automatically generates certificates and keys in the following directory:

    ```sh
    config\certs
    ```

3. Repeat the previous step for any new nodes that you want to enroll.


## Configure {{es}} on the command line [windows-configuring]

{{es}} loads its configuration from the `%ES_HOME%\config\elasticsearch.yml` file by default. The format of this config file is explained in [*Configuring {{es}}*](configure-elasticsearch.md).

Any settings that can be specified in the config file can also be specified on the command line, using the `-E` syntax as follows:

```sh
.\bin\elasticsearch.bat -Ecluster.name=my_cluster -Enode.name=node_1
```

::::{note}
Values that contain spaces must be surrounded with quotes. For instance `-Epath.logs="C:\My Logs\logs"`.
::::


::::{tip}
Typically, any cluster-wide settings (like `cluster.name`) should be added to the `elasticsearch.yml` config file, while any node-specific settings such as `node.name` could be specified on the command line.
::::



## Check that Elasticsearch is running [_check_that_elasticsearch_is_running_2]

You can test that your {{es}} node is running by sending an HTTPS request to port `9200` on `localhost`:

```sh
curl --cacert %ES_HOME%\config\certs\http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200 <1>
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


## Install and run {{es}} as a service on Windows [windows-service]

You can install {{es}} as a service that runs in the background or starts automatically at boot time without user interaction.

1. Install {{es}} as a service. The name of the service and the value of `ES_JAVA_HOME` will be made available during install:

    ```sh
    C:\Program Files\elasticsearch-9.0.0-beta1\bin>elasticsearch-service.bat install
    Installing service      :  "elasticsearch-service-x64"
    Using ES_JAVA_HOME (64-bit):  "C:\jvm\jdk1.8"
    The service 'elasticsearch-service-x64' has been installed.
    ```

2. Start {{es}} as a service. When {{es}} starts, authentication is enabled by default:

    ```sh
    C:\Program Files\elasticsearch-9.0.0-beta1\bin>bin\elasticsearch-service.bat start
    ```

    ::::{note}
    TLS is not enabled or configured when you start {{es}} as a service.
    ::::

3. Generate a password for the `elastic` user with the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) tool. The password is output to the command line.

    ```sh
    C:\Program Files\elasticsearch-9.0.0-beta1\bin>\bin\elasticsearch-reset-password -u elastic
    ```


::::{note}
While a JRE can be used for the {{es}} service, due to its use of a client VM (as opposed to a server JVM which offers better performance for long-running applications) its usage is discouraged and a warning will be issued.
::::


::::{note}
The system environment variable `ES_JAVA_HOME` should be set to the path of the JDK installation that you want the service to use. If you upgrade the JDK, you are not required to the reinstall the service but you must set the value of the system environment variable `ES_JAVA_HOME` to the path to the new JDK installation. However, upgrading across JVM types (e.g. JRE versus SE) is not supported, and does require the service to be reinstalled.
::::


### Manage {{es}} as a service on Windows [windows-service-manage]

Run the `elasticsearch-service.bat` script in the `bin\` folder to install, remove, manage, or configure the service and potentially start and stop the service from the command line.

```sh
C:\Program Files\elasticsearch-9.0.0-beta1\bin>elasticsearch-service.bat

Usage: elasticsearch-service.bat install|remove|start|stop|manager [SERVICE_ID]
```

The script requires one parameter (the command to execute), followed by an optional one indicating the service id (useful when installing multiple {{es}} services).

The commands available are:

`install`
:   Install {{es}} as a service

`remove`
:   Remove the installed {{es}} service (and stop the service if started)

`start`
:   Start the {{es}} service (if installed)

`stop`
:   Stop the {{es}} service (if started)

`manager`
:   Start a GUI for managing the installed service


## Customize service settings [windows-service-settings]

The {{es}} service can be configured prior to installation by setting the following environment variables (either using the [set command](https://technet.microsoft.com/en-us/library/cc754250(v=ws.10).aspx) from the command line, or through the **System Properties→Environment Variables** GUI).

`SERVICE_ID`
:   A unique identifier for the service. Useful if installing multiple instances on the same machine. Defaults to `elasticsearch-service-x64`.

`SERVICE_USERNAME`
:   The user to run as, defaults to the local system account.

`SERVICE_PASSWORD`
:   The password for the user specified in `%SERVICE_USERNAME%`.

`SERVICE_DISPLAY_NAME`
:   The name of the service. Defaults to `{{es}} <version> %SERVICE_ID%`.

`SERVICE_DESCRIPTION`
:   The description of the service. Defaults to `{{es}} <version> Windows Service - https://elastic.co`.

`ES_JAVA_HOME`
:   The installation directory of the desired JVM to run the service under.

`SERVICE_LOG_DIR`
:   Service log directory, defaults to `%ES_HOME%\logs`. Note that this does not control the path for the {{es}} logs; the path for these is set via the setting `path.logs` in the `elasticsearch.yml` configuration file, or on the command line.

`ES_PATH_CONF`
:   Configuration file directory (which needs to include `elasticsearch.yml`, `jvm.options`, and `log4j2.properties` files), defaults to `%ES_HOME%\config`.

`ES_JAVA_OPTS`
:   Any additional JVM system properties you may want to apply.

`ES_START_TYPE`
:   Startup mode for the service. Can be either `auto` or `manual` (default).

`ES_STOP_TIMEOUT`
:   The timeout in seconds that procrun waits for service to exit gracefully. Defaults to `0`.

::::{note}
At its core, `elasticsearch-service.bat` relies on [Apache Commons Daemon](https://commons.apache.org/proper/commons-daemon/) project to install the service. Environment variables set prior to the service installation are copied and will be used during the service lifecycle. This means any changes made to them after the installation will not be picked up unless the service is reinstalled.
::::


::::{note}
By default, {{es}} automatically sizes JVM heap based on a node’s [roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles) and total memory. We recommend this default sizing for most production environments. If needed, you can override default sizing by manually setting the heap size.

When installing {{es}} on Windows as a service for the first time or running {{es}} from the command line, you can manually [Set the JVM heap size](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-heap-size). To resize the heap for an already installed service, use the service manager: `bin\elasticsearch-service.bat manager`.

::::


::::{note}
The service automatically configures a private temporary directory for use by {{es}} when it is running. This private temporary directory is configured as a sub-directory of the private temporary directory for the user running the installation. If the service will run under a different user, you can configure the location of the temporary directory that the service should use by setting the environment variable `ES_TMPDIR` to the preferred location before you execute the service installation.
::::


Using the Manager GUI
:   It is also possible to configure the service after it’s been installed using the manager GUI (`elasticsearch-service-mgr.exe`), which offers insight into the installed service, including its status, startup type, JVM, start and stop settings amongst other things. Invoke `elasticsearch-service.bat manager` from the command-line to open the manager window.

Most changes (like JVM settings) made through the manager GUI will require a restart of the service to take affect.



## Connect clients to {{es}} [_connect_clients_to_es_2]

When you start {{es}} for the first time, TLS is configured automatically for the HTTP layer. A CA certificate is generated and stored on disk at:

```sh
%ES_HOME%\config\certs\http_ca.crt
```

The hex-encoded SHA-256 fingerprint of this certificate is also output to the terminal. Any clients that connect to {{es}}, such as the [{{es}} Clients](https://www.elastic.co/guide/en/elasticsearch/client/index.html), {{beats}}, standalone {{agent}}s, and {{ls}} must validate that they trust the certificate that {{es}} uses for HTTPS. {{fleet-server}} and {{fleet}}-managed {{agent}}s are automatically configured to trust the CA certificate. Other clients can establish trust by using either the fingerprint of the CA certificate or the CA certificate itself.

If the auto-configuration process already completed, you can still obtain the fingerprint of the security certificate. You can also copy the CA certificate to your machine and configure your client to use it.


#### Use the CA fingerprint [_use_the_ca_fingerprint_2]

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


#### Use the CA certificate [_use_the_ca_certificate_2]

If your library doesn’t support a method of validating the fingerprint, the auto-generated CA certificate is created in the following directory on each {{es}} node:

```sh
%ES_HOME%\config\certs\http_ca.crt
```

Copy the `http_ca.crt` file to your machine and configure your client to use this certificate to establish trust when it connects to {{es}}.


## Directory layout of `.zip` archive [windows-layout]

The `.zip` package is entirely self-contained. All files and directories are, by default, contained within `%ES_HOME%` — the directory created when unpacking the archive.

This is very convenient because you don’t have to create any directories to start using {{es}}, and uninstalling {{es}} is as easy as removing the `%ES_HOME%` directory. However, it is advisable to change the default locations of the config directory, the data directory, and the logs directory so that you do not delete important data later on.

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | {{es}} home directory or `%ES_HOME%` | Directory created by unpacking the archive |  |
| bin | Binary scripts including `elasticsearch` to start a node    and `elasticsearch-plugin` to install plugins | `%ES_HOME%\bin` |  |
| conf | Configuration files including `elasticsearch.yml` | `%ES_HOME%\config` | `[ES_PATH_CONF](configure-elasticsearch.md#config-files-location)` |
| conf | Generated TLS keys and certificates for the transport and HTTP layer. | `%ES_HOME%\config\certs` |  |
| data | The location of the data files of each index / shard allocated    on the node. | `%ES_HOME%\data` | `path.data` |
| logs | Log files location. | `%ES_HOME%\logs` | `path.logs` |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `%ES_HOME%\plugins` |  |
| repo | Shared file system repository locations. Can hold multiple locations. A file system repository can be placed in to any subdirectory of any directory specified here. | Not configured | `path.repo` |


## Next steps [_next_steps_2]

You now have a test {{es}} environment set up. Before you start serious development or go into production with {{es}}, you must do some additional setup:

* Learn how to [configure Elasticsearch](configure-elasticsearch.md).
* Configure [important Elasticsearch settings](important-settings-configuration.md).
* Configure [important system settings](important-system-configuration.md).
