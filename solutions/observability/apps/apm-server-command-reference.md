---
navigation_title: "Command reference"
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-command-line-options.html
applies_to:
  stack: all
---



# APM Server command reference [apm-command-line-options]


::::{important}
These commands only apply to the APM Server binary installation method.
::::


APM Server provides a command-line interface for starting APM Server and performing common tasks, like testing configuration files.

The command-line also supports [global flags](#apm-global-flags) for controlling global behaviors.

::::{tip}
Use `sudo` to run the following commands if:

* the config file is owned by `root`, or
* APM Server is configured to capture data that requires `root` access

::::


Some of the features described here require an Elastic license. For more information, see [https://www.elastic.co/subscriptions](https://www.elastic.co/subscriptions) and [License Management](../../../deploy-manage/license/manage-your-license-in-self-managed-cluster.md).

| Commands |  |
| --- | --- |
| [`apikey`](#apm-apikey-command) | Manage API Keys for communication between APM agents and server. [8.6.0] |
| [`export`](#apm-export-command) | Exports the configuration, index template, or {{ilm-init}} policy to stdout. |
| [`help`](#apm-help-command) | Shows help for any command. |
| [`keystore`](#apm-keystore-command) | Manages the [secrets keystore](secrets-keystore-for-secure-settings.md). |
| [`run`](#apm-run-command) | Runs APM Server. This command is used by default if you start APM Server without specifying a command. |
| [`test`](#apm-test-command) | Tests the configuration. |
| [`version`](#apm-version-command) | Shows information about the current version. |

Also see [Global flags](#apm-global-flags).


## `apikey` command [apm-apikey-command]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


::::{admonition} Deprecated in 8.6.0.
:class: warning

Users should create API Keys through {{kib}} or the {{es}} REST API. See [API keys](api-keys.md).
::::


Communication between APM agents and APM Server now supports sending an [API Key in the Authorization header](api-keys.md). APM Server provides an `apikey` command that can create, verify, invalidate, and show information about API Keys for agent/server communication. Most operations require the `manage_own_api_key` cluster privilege, and you must ensure that `apm-server.api_key` or `output.elasticsearch` are configured appropriately.

**SYNOPSIS**

```sh
apm-server apikey SUBCOMMAND [FLAGS]
```

**`SUBCOMMAND`**

**`create`**
:   Create an API Key with the specified privilege(s). No required flags.

    The user requesting to create an API Key needs to have APM privileges used by the APM Server. A superuser, by default, has these privileges.

    ::::{dropdown} Expand for more information on assigning these privileges to other users
    To create an APM Server user with the required privileges for creating and managing API keys:

    1. Create an **API key role**, called something like `apm_api_key`, that has the following `cluster` level privileges:

        | Privilege | Purpose |
        | --- | --- |
        | `manage_own_api_key` | Allow APM Server to create, retrieve, and invalidate API keys |

    2. Depending on what the **API key role** will be used for, also assign the appropriate `apm` application-level privileges:

        * To **receive Agent configuration**, assign `config_agent:read`.
        * To **ingest agent data**, assign `event:write`.
        * To **upload source maps**, assign `sourcemap:write`.


    ::::


**`info`**
:   Query API Key(s). `--id` or `--name` required.

**`invalidate`**
:   Invalidate API Key(s). `--id` or `--name` required.

**`verify`**
:   Check if a credentials string has the given privilege(s). `--credentials` required.

**FLAGS**

**`--agent-config`**
:   Required for agents to read configuration remotely. Valid with the `create` and `verify` subcommands. When used with `create`, gives the `config_agent:read` privilege to the created key. When used with `verify`, asks for the `config_agent:read` privilege.

**`--credentials CREDS`**
:   Required for the `verify` subcommand. Specifies the credentials for which to check privileges. Credentials are the base64 encoded representation of the API key’s `id:api_key`.

**`--expiration TIME`**
:   When used with `create`, specifies the expiration for the key, e.g., "1d" (default never).

**`--id ID`**
:   ID of the API key. Valid with the `info` and `invalidate` subcommands. When used with `info`, queries the specified ID. When used with `invalidate`, deletes the specified ID.

**`--ingest`**
:   Required for ingesting events. Valid with the `create` and `verify` subcommands. When used with `create`, gives the `event:write` privilege to the created key. When used with `verify`, asks for the `event:write` privilege.

**`--json`**
:   Prints the output of the command as JSON. Valid with all `apikey` subcommands.

**`--name NAME`**
:   Name of the API key(s). Valid with the `create`, `info`, and `invalidate` subcommands. When used with `create`, specifies the name of the API key to be created (default: "apm-key"). When used with `info`, specifies the API key to query (multiple matches are possible). When used with `invalidate`, specifies the API key to delete (multiple matches are possible).

**`--sourcemap`**
:   Required for uploading source maps. Valid with the `create` and `verify` subcommands. When used with `create`, gives the `sourcemap:write` privilege to the created key. When used with `verify`, asks for the `sourcemap:write` privilege.

**`--valid-only`**
:   When used with `info`, only returns valid API Keys (not expired or invalidated).

Also see [Global flags](#apm-global-flags).

**EXAMPLES**

```sh
apm-server apikey create --ingest --agent-config --name example-001
apm-server apikey info --name example-001 --valid-only
apm-server apikey invalidate --name example-001
```

For more information, see [API keys](api-keys.md).


## `export` command [apm-export-command]

Exports the configuration, index template, or {{ilm-init}} policy to stdout. You can use this command to quickly view your configuration or see the contents of the index template or the {{ilm-init}} policy.

**SYNOPSIS**

```sh
apm-server export SUBCOMMAND [FLAGS]
```

**`SUBCOMMAND`**

**`config`**
:   Exports the current configuration to stdout. If you use the `-c` flag, this command exports the configuration that’s defined in the specified file.

$$$apm-template-subcommand$$$**`template`**
:   Exports the index template to stdout. You can specify the `--es.version` and `--index` flags to further define what gets exported. Furthermore you can export the template to a file instead of `stdout` by defining a directory via `--dir`.

$$$apm-ilm-policy-subcommand$$$

**`ilm-policy`**
:   Exports the {{ilm}} policy to stdout. You can specify the `--es.version` and a `--dir` to which the policy should be exported as a file rather than exporting to `stdout`.

**FLAGS**

**`--es.version VERSION`**
:   When used with [`template`](#apm-template-subcommand), exports an index template that is compatible with the specified version. When used with [`ilm-policy`](#apm-ilm-policy-subcommand), exports the {{ilm-init}} policy if the specified ES version is enabled for {{ilm-init}}.

**`-h, --help`**
:   Shows help for the `export` command.

**`--index BASE_NAME`**
:   When used with [`template`](#apm-template-subcommand), sets the base name to use for the index template. If this flag is not specified, the default base name is `apm-server`.

**`--dir DIRNAME`**
:   Define a directory to which the template and {{ilm-init}} policy should be exported to as files instead of printing them to `stdout`.

Also see [Global flags](#apm-global-flags).

**EXAMPLES**

```sh
apm-server export config
apm-server export template --es.version 9.0.0-beta1 --index myindexname
```


## `help` command [apm-help-command]

Shows help for any command. If no command is specified, shows help for the `run` command.

**SYNOPSIS**

```sh
apm-server help COMMAND_NAME [FLAGS]
```

**`COMMAND_NAME`**
:   Specifies the name of the command to show help for.

**FLAGS**

**`-h, --help`**
:   Shows help for the `help` command.

Also see [Global flags](#apm-global-flags).

**EXAMPLE**

```sh
apm-server help export
```


## `keystore` command [apm-keystore-command]

Manages the [secrets keystore](secrets-keystore-for-secure-settings.md).

**SYNOPSIS**

```sh
apm-server keystore SUBCOMMAND [FLAGS]
```

**`SUBCOMMAND`**

**`add KEY`**
:   Adds the specified key to the keystore. Use the `--force` flag to overwrite an existing key. Use the `--stdin` flag to pass the value through `stdin`.

**`create`**
:   Creates a keystore to hold secrets. Use the `--force` flag to overwrite the existing keystore.

**`list`**
:   Lists the keys in the keystore.

**`remove KEY`**
:   Removes the specified key from the keystore.

**FLAGS**

**`--force`**
:   Valid with the `add` and `create` subcommands. When used with `add`, overwrites the specified key. When used with `create`, overwrites the keystore.

**`--stdin`**
:   When used with `add`, uses the stdin as the source of the key’s value.

**`-h, --help`**
:   Shows help for the `keystore` command.

Also see [Global flags](#apm-global-flags).

**EXAMPLES**

```sh
apm-server keystore create
apm-server keystore add ES_PWD
apm-server keystore remove ES_PWD
apm-server keystore list
```

See [Secrets keystore](secrets-keystore-for-secure-settings.md) for more examples.


## `run` command [apm-run-command]

Runs APM Server. This command is used by default if you start APM Server without specifying a command.

**SYNOPSIS**

```sh
apm-server run [FLAGS]
```

Or:

```sh
apm-server [FLAGS]
```

**FLAGS**

**`-N, --N`**
:   Disables publishing for testing purposes.

**`--cpuprofile FILE`**
:   Writes CPU profile data to the specified file. This option is useful for troubleshooting APM Server.

**`-h, --help`**
:   Shows help for the `run` command.

**`--httpprof [HOST]:PORT`**
:   Starts an HTTP server for profiling. This option is useful for troubleshooting and profiling APM Server.

**`--memprofile FILE`**
:   Writes memory profile data to the specified output file. This option is useful for troubleshooting APM Server.

**`--system.hostfs MOUNT_POINT`**
:   Specifies the mount point of the host’s file system for use in monitoring a host.

Also see [Global flags](#apm-global-flags).

**EXAMPLE**

```sh
apm-server run -e
```

Or:

```sh
apm-server -e
```


## `test` command [apm-test-command]

Tests the configuration.

**SYNOPSIS**

```sh
apm-server test SUBCOMMAND [FLAGS]
```

**`SUBCOMMAND`**

**`config`**
:   Tests the configuration settings.

**`output`**
:   Tests that APM Server can connect to the output by using the current settings.

**FLAGS**

**`-h, --help`**
:   Shows help for the `test` command.

Also see [Global flags](#apm-global-flags).

**EXAMPLE**

```sh
apm-server test config
```


## `version` command [apm-version-command]

Shows information about the current version.

**SYNOPSIS**

```sh
apm-server version [FLAGS]
```

**FLAGS**

**`-h, --help`**
:   Shows help for the `version` command.

Also see [Global flags](#apm-global-flags).

**EXAMPLE**

```sh
apm-server version
```


## Global flags [apm-global-flags]

These global flags are available whenever you run APM Server.

**`-E, --E "SETTING_NAME=VALUE"`**
:   Overrides a specific configuration setting. You can specify multiple overrides. For example:

    ```sh
    apm-server -E "name=mybeat" -E "output.elasticsearch.hosts=['http://myhost:9200']"
    ```

    This setting is applied to the currently running APM Server process. The APM Server configuration file is not changed.


**`-c, --c FILE`**
:   Specifies the configuration file to use for APM Server. The file you specify here is relative to `path.config`. If the `-c` flag is not specified, the default config file, `apm-server.yml`, is used.

**`-d, --d SELECTORS`**
:   Enables debugging for the specified selectors. For the selectors, you can specify a comma-separated list of components, or you can use `-d "*"` to enable debugging for all components. For example, `-d "publisher"` displays all the publisher-related messages.

**`-e, --e`**
:   Logs to stderr and disables syslog/file output.

**`-environment`**
:   For logging purposes, specifies the environment that APM Server is running in. This setting is used to select a default log output when no log output is configured. Supported values are: `systemd`, `container`, `macos_service`, and `windows_service`. If `systemd` or `container` is specified, APM Server will log to stdout and stderr by default.

**`--path.config`**
:   Sets the path for configuration files. See the [Installation layout](installation-layout.md) section for details.

**`--path.data`**
:   Sets the path for data files. See the [Installation layout](installation-layout.md) section for details.

**`--path.home`**
:   Sets the path for miscellaneous files. See the [Installation layout](installation-layout.md) section for details.

**`--path.logs`**
:   Sets the path for log files. See the [Installation layout](installation-layout.md) section for details.

**`--strict.perms`**
:   Sets strict permission checking on configuration files. The default is `-strict.perms=true`. See [Configuration file ownership](apm-server-systemd.md#apm-config-file-ownership) for more information.

**`-v, --v`**
:   Logs INFO-level messages.
