---
navigation_title: Install on Windows
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/zip-windows.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
sub:
  es-conf: "%ES_HOME%\\config"
  slash: \
  export: $
  escape: ^
  auto: .bat
  ipcommand: ipconfig /all
  ipvalue: inet
---

# Install {{es}} with .zip on Windows [zip-windows]

{{es}} can be installed on Windows using the Windows `.zip` archive. This comes with a `elasticsearch-service.bat` command which will set up {{es}} to [run as a service](#windows-service).

:::{include} _snippets/trial.md
:::

:::{include} _snippets/es-releases.md
:::

:::{include} _snippets/java-version.md
:::

::::{note}
On Windows, the {{es}} {{ml}} feature requires the Microsoft Universal C Runtime library. This is built into Windows 10, Windows Server 2016 and more recent versions of Windows. For older versions of Windows, it can be installed through Windows Update, or from a [separate download](https://support.microsoft.com/en-us/help/2999226/update-for-universal-c-runtime-in-windows). If you can't install the Microsoft Universal C Runtime library, you can still use the rest of {{es}} if you disable the {{ml}} feature.
::::

## Before you start

:::{include} _snippets/prereqs.md
:::

## Step 1: Download and install the `.zip` package [install-windows]

::::{tab-set}

:::{tab-item} Latest
% link url manually set
Download the `.zip` archive for {{es}} {{version.stack}} from: [https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{version.stack}}-windows-x86_64.zip](https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-{{version.stack}}-windows-x86_64.zip)

Unzip it with your favorite unzip tool. This will create a folder with the following name:

```text subs=true
elasticsearch-{{version.stack}}
```

We will refer to this folder as `%ES_HOME%`. 

In a terminal window, `cd` to the `%ES_HOME%` directory, for example:

```sh subs=true
cd C:\Program Files\elasticsearch-{{version.stack}}
```
:::

:::{tab-item} Specific version
Download the `.zip` archive for the {{es}} version that you want from the [Past Releases](https://www.elastic.co/downloads/past-releases) page.

Unzip it with your favorite unzip tool. This will create a folder called `elasticsearch-<SPECIFIC.VERSION.NUMBER>`, where `<SPECIFIC.VERSION.NUMBER>` is the version you downloaded. We will refer to this folder as `%ES_HOME%`. 

In a terminal window, `cd` to the `%ES_HOME%` directory, for example:

```sh subs=true
cd C:\Program Files\elasticsearch-<SPECIFIC.VERSION.NUMBER>
```
Replace `<SPECIFIC.VERSION.NUMBER>` with the {{es}} version you installed.
:::
::::


## Step 2: Enable automatic creation of system indices [windows-enable-indices]

:::{include} _snippets/enable-auto-indices.md
:::

## Step 3: Set up the node for connectivity

:::{include} _snippets/cluster-formation-brief.md
:::

* If you're installing the first node in a multi-node cluster across multiple hosts, then you need to [configure the node so that other hosts are able to connect to it](#first-node).

* If you're installing additional nodes for a cluster, then you need to [generate an enrollment token and pass it when starting {{es}} for the first time](#existing-cluster).

### Set up a node as the first node in a multi-host cluster [first-node]

:::{include} _snippets/first-node.md
:::

### Enroll the node in an existing cluster [existing-cluster]

:::{include} _snippets/enroll-nodes.md
:::

## Step 4: Run {{es}}

You have several options for starting {{es}}:

* [Run from the command line](#command-line)
* [Install and run as a service](#windows-service)

If you're starting a node that will be enrolled in an existing cluster, refer to [Enroll the node in an existing cluster](#existing-cluster).

### Run {{es}} from the command line [command-line]

:::{include} _snippets/zip-windows-start.md
:::

#### Security at startup [security-at-startup]

:::{include} _snippets/auto-security-config.md
:::

The password for the `elastic` user and the enrollment token for {{kib}} are output to your terminal.

:::{include} _snippets/pw-env-var.md
:::

#### Configure {{es}} on the command line [windows-configuring]

:::{include} _snippets/cmd-line-config.md
:::

### Install and run {{es}} as a service on Windows [windows-service]

You can install {{es}} as a service that runs in the background or starts automatically at boot time without user interaction.

1. Install {{es}} as a service. The name of the service and the value of `ES_JAVA_HOME` will be made available during install:

    ```sh subs=true
    .\bin\elasticsearch-service.bat install
    ```

    Response:
    ```
    Installing service      :  "elasticsearch-service-x64"
    Using ES_JAVA_HOME (64-bit):  "C:\jvm\jdk1.8"
    The service 'elasticsearch-service-x64' has been installed.
    ```

    `ES_JAVA_HOME` is the installation directory of the desired JVM to run the service under. You can change this value using an [environment variable](#windows-service-settings).

    ::::{note}
    While a JRE can be used for the {{es}} service, its use is discouraged and using a JRE will trigger a warning. Use is discouraged due to its use of a client VM, as opposed to a server JVM which offers better performance for long-running applications.
    ::::

2. Start {{es}} as a service. When {{es}} starts, authentication is enabled by default:

    ```sh subs=true
    .\bin\elasticsearch-service.bat start
    ```

    ::::{note}
    TLS is not enabled or configured when you start {{es}} as a service.
    ::::

3. Generate a password for the `elastic` user with the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) tool. The password is output to the command line.

    ```sh subs=true
    .\bin\elasticsearch-reset-password -u elastic
    ```

#### Manage {{es}} as a service on Windows [windows-service-manage]

Use the `elasticsearch-service.bat` script located in the `bin\` folder to install, remove, manage, start, or stop the service from the command line. Starting and stopping are only available if the service is already installed.

Usage:
```
elasticsearch-service.bat install|remove|start|stop|manager [SERVICE_ID]
```

The script requires one parameter (the command to execute), followed by an optional one indicating the service ID (useful when installing multiple {{es}} services).

The commands available are:

| Command | Description |
| --- | --- |
|
| `install` | Install {{es}} as a service |
| `remove`  | Remove the installed {{es}} service (and stop the service if started) |
| `start`   | Start the {{es}} service (if installed) |
| `stop`    |  Stop the {{es}} service (if started) |
| `manager` | Start a GUI for managing the installed service |


#### Customize service settings [windows-service-settings]

You can customize the service settings before installation using environment variables, or after installation using the Manager GUI.

`elasticsearch-service.bat` relies on [Apache Commons Daemon](https://commons.apache.org/proper/commons-daemon/) project to install the service. Environment variables set prior to the service installation are copied and will be used during the service lifecycle. This means any changes made to them after the installation will not be picked up unless the service is reinstalled.

::::{tab-set}
:::{tab-item} Environment variables (pre-install)

The {{es}} service can be configured prior to installation by setting the following environment variables (either using the [set command](https://technet.microsoft.com/en-us/library/cc754250(v=ws.10).aspx) from the command line, or through the **System Properties > Environment Variables** GUI).

| Environment variable | Description |
| --- | --- |
| `SERVICE_ID` | A unique identifier for the service. Useful if installing multiple instances on the same machine. Defaults to `elasticsearch-service-x64`. |
| `SERVICE_USERNAME` | The user to run as, defaults to the local system account. |
| `SERVICE_PASSWORD` | The password for the user specified in `%SERVICE_USERNAME%`. |
| `SERVICE_DISPLAY_NAME` | The name of the service. Defaults to `Elasticsearch<version> %SERVICE_ID%`. |
| `SERVICE_DESCRIPTION` | The description of the service. Defaults to `Elasticsearch<version> Windows Service - https://elastic.co`. |
| `ES_JAVA_HOME` | The installation directory of the desired JVM to run the service under. |
| `SERVICE_LOG_DIR` | Service log directory, defaults to `%ES_HOME%\logs`. Note that this does not control the path for the {{es}} logs; the path for these is set via the setting `path.logs` in the `elasticsearch.yml` configuration file, or on the command line. |
| `ES_PATH_CONF` | Configuration file directory (which needs to include `elasticsearch.yml`, `jvm.options`, and `log4j2.properties` files), defaults to `%ES_HOME%\config`. |
| `ES_JAVA_OPTS` | Any additional JVM system properties you may want to apply. |
| `ES_START_TYPE` | Startup mode for the service. Can be either `auto` or `manual` (default). |
| `ES_STOP_TIMEOUT` | The timeout in seconds that procrun waits for service to exit gracefully. Defaults to `0`. |

:::
:::{tab-item} Manager GUI (post-install)

It is also possible to configure the service after it’s been installed using the manager GUI (`elasticsearch-service-mgr.exe`), which offers insight into the installed service, including its status, startup type, JVM, start and stop settings amongst other things. To open the manager GUI, run the following command:

```sh
elasticsearch-service.bat manager
```

Most changes (like JVM settings) made through the manager GUI will require a restart of the service to take affect.
:::
::::

##### Considerations

* By default, {{es}} automatically sizes JVM heap based on a node’s [roles](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles) and total memory. We recommend this default sizing for most production environments. If needed, you can override default sizing by manually setting the heap size.

  When installing {{es}} on Windows as a service for the first time or running {{es}} from the command line, you can manually [Set the JVM heap size](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-heap-size). To resize the heap for an already installed service, use the manager GUI.

* The service automatically configures a private temporary directory for use by {{es}} when it is running. This private temporary directory is configured as a sub-directory of the private temporary directory for the user running the installation. If the service will run under a different user, you can configure the location of the temporary directory that the service should use by setting the environment variable `ES_TMPDIR` to the preferred location before you execute the service installation.

* The system environment variable `ES_JAVA_HOME` should be set to the path of the JDK installation that you want the service to use. If you upgrade the JDK, you are not required to the reinstall the service, but you must set the value of the system environment variable `ES_JAVA_HOME` to the path to the new JDK installation. Upgrading across JVM types (e.g. JRE versus SE) is not supported, and requires the service to be reinstalled.

## Step 5: Check that {{es}} is running [_check_that_elasticsearch_is_running_2]

:::{include} _snippets/check-es-running.md
:::

## Step 6 (Multi-node clusters only): Update the config files [update-config-files]

If you are deploying a multi-node cluster, then the enrollment process adds all existing nodes to each newly enrolled node's `discovery.seed_hosts` setting. However, you need to go back to all of the nodes in the cluster and edit them so each node in the cluster can restart and rejoin the cluster as expected.

:::{note}
Because the initial node in the cluster is bootstrapped as a single-node cluster, it won't have `discovery.seed_hosts` configured. This setting is mandatory for multi-node clusters and must be added manually to the first node.
:::

:::{include} _snippets/clean-up-multinode.md
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

## Directory layout of `.zip` archive [windows-layout]

The `.zip` package is entirely self-contained. All files and directories are, by default, contained within `%ES_HOME%` — the directory created when unpacking the archive.

This is very convenient because you don’t have to create any directories to start using {{es}}, and uninstalling {{es}} is as easy as removing the `%ES_HOME%` directory. However, it is advisable to change the default locations of the config directory, the data directory, and the logs directory so that you do not delete important data later on.

| Type | Description | Default Location | Setting |
| --- | --- | --- | --- |
| home | {{es}} home directory or `%ES_HOME%` | Directory created by unpacking the archive |  |
| bin | Binary scripts including `elasticsearch` to start a node    and `elasticsearch-plugin` to install plugins | `%ES_HOME%\bin` |  |
| conf | Configuration files including `elasticsearch.yml` | `%ES_HOME%\config` | [`ES_PATH_CONF`](/deploy-manage/deploy/self-managed/configure-elasticsearch.md#config-files-location) |
| conf | Generated TLS keys and certificates for the transport and HTTP layer. | `%ES_HOME%\config\certs` |  |
| data | The location of the data files of each index / shard allocated    on the node. | `%ES_HOME%\data` | [`path.data`](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings) |
| logs | Log files location. | `%ES_HOME%\logs` | [`path.logs`](/deploy-manage/deploy/self-managed/important-settings-configuration.md#path-settings) |
| plugins | Plugin files location. Each plugin will be contained in a subdirectory. | `%ES_HOME%\plugins` |  |
| repo | Shared file system repository locations. Can hold multiple locations. A file system repository can be placed in to any subdirectory of any directory specified here. | Not configured | [`path.repo`](/deploy-manage/tools/snapshot-and-restore/shared-file-system-repository.md) |



## Next steps [_next_steps]

:::{include} _snippets/install-next-steps.md
:::