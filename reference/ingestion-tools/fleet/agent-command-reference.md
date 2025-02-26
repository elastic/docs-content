---
navigation_title: "Command reference"
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-cmd-options.html
---

# {{agent}} command reference [elastic-agent-cmd-options]


{{agent}} provides commands for running {{agent}}, managing {{fleet-server}}, and doing common tasks. The commands listed here apply to both [{{fleet}}-managed](/reference/ingestion-tools/fleet/manage-elastic-agents-in-fleet.md) and [standalone](/reference/ingestion-tools/fleet/configure-standalone-elastic-agents.md) {{agent}}.

::::{admonition} Restrictions
:class: important

Note the following restrictions for running {{agent}} commands:

* You might need to log in as a root user (or Administrator on Windows) to run the commands described here. After the {{agent}} service is installed and running, make sure you run these commands without prepending them with `./` to avoid invoking the wrong binary.
* Running {{agent}} commands using the Windows PowerShell ISE is not supported.

::::


* [diagnostics](#elastic-agent-diagnostics-command)
* [enroll](#elastic-agent-enroll-command)
* [help](#elastic-agent-help-command)
* [inspect](#elastic-agent-inspect-command)
* [install](#elastic-agent-install-command)
* [otel](#elastic-agent-otel-command) [preview]
* [privileged](#elastic-agent-privileged-command)
* [restart](#elastic-agent-restart-command)
* [run](#elastic-agent-run-command)
* [status](#elastic-agent-status-command)
* [uninstall](#elastic-agent-uninstall-command)
* [upgrade](#elastic-agent-upgrade-command)
* [logs](#elastic-agent-logs-command)
* [unprivileged](#elastic-agent-unprivileged-command)
* [version](#elastic-agent-version-command)

<hr>

## elastic-agent diagnostics [elastic-agent-diagnostics-command]

Gather diagnostics information from the {{agent}} and component/unit it’s running. This command produces an archive that contains:

* version.txt - version information
* pre-config.yaml - pre-configuration before variable substitution
* variables.yaml - current variable contexts from providers
* computed-config.yaml - configuration after variable substitution
* components-expected.yaml - expected computed components model from the computed-config.yaml
* components-actual.yaml - actual running components model as reported by the runtime manager
* state.yaml - current state information of all running components
* Components Directory - diagnostic information from each running component:

    * goroutine.txt - goroutine dump
    * heap.txt - memory allocation of live objects
    * allocs.txt - sampling past memory allocations
    * threadcreate.txt - traces led to creation of new OS threads
    * block.txt - stack traces that led to blocking on synchronization primitives
    * mutex.txt - stack traces of holders of contended mutexes
    * Unit Directory - If a given unit provides specific diagnostics, it will be placed here.


Note that **credentials may not be redacted** in the archive; they may appear in plain text in the configuration or policy files inside the archive.

This command is intended for debugging purposes only. The output format and structure of the archive may change between releases.


### Synopsis [_synopsis]

```shell
elastic-agent diagnostics [--file <string>]
                          [--cpu-profile]
                          [--exclude-events]
                          [--help]
                          [global-flags]
```


### Options [_options]

`--file`
:   Specifies the output archive name. Defaults to `elastic-agent-diagnostics-<timestamp>.zip`, where the timestamp is the current time in UTC.

`--help`
:   Show help for the `diagnostics` command.

`--cpu-profile`
:   Additionally runs a 30-second CPU profile on each running component. This will generate an additional `cpu.pprof` file for each component.

`--p`
:   Alias for `--cpu-profile`.

`--exclude-events`
:   Exclude the events log files from the diagnostics archive.

For more flags, see [Global flags](#elastic-agent-global-flags).


### Example [_example_38]

```shell
elastic-agent diagnostics
```

<hr>

## elastic-agent enroll [elastic-agent-enroll-command]

Enroll the {{agent}} in {{fleet}}.

Use this command to enroll the {{agent}} in {{fleet}} without installing the agent as a service. You will need to do this if you installed the {{agent}} from a DEB or RPM package and plan to use systemd commands to start and manage the service. This command is also useful for testing {{agent}} prior to installing it.

If you’ve already installed {{agent}}, use this command to modify the settings that {{agent}} runs with.

::::{tip}
To enroll an {{agent}} *and* install it as a service, use the [`install` command](#elastic-agent-install-command) instead. Installing as a service is the most common scenario.
::::


We recommend that you run the `enroll` (or `install`) command as the root user because some integrations require root privileges to collect sensitive data. This command overwrites the `elastic-agent.yml` file in the agent directory.

This command includes optional flags to set up [{{fleet-server}}](/reference/ingestion-tools/fleet/fleet-server.md).

::::{important}
This command enrolls the {{agent}} in {{fleet}}; it does not start the agent. To start the agent, either [start the service](/reference/ingestion-tools/fleet/start-stop-elastic-agent.md#start-elastic-agent-service), if one exists, or use the [`run` command](#elastic-agent-run-command) to start the agent from a terminal.
::::



### Synopsis [_synopsis_2]

To enroll the {{agent}} in {{fleet}}:

```shell
elastic-agent enroll --url <string>
                     --enrollment-token <string>
                     [--ca-sha256 <string>]
                     [--certificate-authorities <string>]
                     [--daemon-timeout <duration>]
                     [--delay-enroll]
                     [--elastic-agent-cert <string>]
                     [--elastic-agent-cert-key <string>]
                     [--elastic-agent-cert-key-passphrase <string>]
                     [--force]
                     [--header <strings>]
                     [--help]
                     [--insecure ]
                     [--proxy-disabled]
                     [--proxy-header <strings>]
                     [--proxy-url <string>]
                     [--staging <string>]
                     [--tag <string>]
                     [global-flags]
```

To enroll the {{agent}} in {{fleet}} and set up {{fleet-server}}:

```shell
elastic-agent enroll --fleet-server-es <string>
                     --fleet-server-service-token <string>
                     [--fleet-server-service-token-path <string>]
                     [--ca-sha256 <string>]
                     [--certificate-authorities <string>]
                     [--daemon-timeout <duration>]
                     [--delay-enroll]
                     [--elastic-agent-cert <string>]
                     [--elastic-agent-cert-key <string>]
                     [--elastic-agent-cert-key-passphrase <string>]
                     [--fleet-server-cert <string>] <1>
                     [--fleet-server-cert-key <string>]
                     [--fleet-server-cert-key-passphrase <string>]
                     [--fleet-server-client-auth <string>]
                     [--fleet-server-es-ca <string>]
                     [--fleet-server-es-ca-trusted-fingerprint <string>] <2>
                     [--fleet-server-es-cert <string>]
                     [--fleet-server-es-cert-key <string>]
                     [--fleet-server-es-insecure]
                     [--fleet-server-host <string>]
                     [--fleet-server-policy <string>]
                     [--fleet-server-port <uint16>]
                     [--fleet-server-timeout <duration>]
                     [--force]
                     [--header <strings>]
                     [--help]
                     [--non-interactive]
                     [--proxy-disabled]
                     [--proxy-header <strings>]
                     [--proxy-url <string>]
                     [--staging <string>]
                     [--tag <string>]
                     [--url <string>] <3>
                     [global-flags]
```

1. If no `fleet-server-cert*` flags are specified, {{agent}} auto-generates a self-signed certificate with the hostname of the machine. Remote {{agent}}s enrolling into a {{fleet-server}} with self-signed certificates must specify the `--insecure` flag.
2. Required when using self-signed certificates with {{es}}.
3. Required when enrolling in a {{fleet-server}} with custom certificates. The URL must match the DNS name used to generate the certificate specified by `--fleet-server-cert`.


For more information about custom certificates, refer to [Configure SSL/TLS for self-managed {{fleet-server}}s](/reference/ingestion-tools/fleet/secure-connections.md).


### Options [_options_2]

`--ca-sha256 <string>`
:   Comma-separated list of certificate authority hash pins used for certificate verification.

`--certificate-authorities <string>`
:   Comma-separated list of root certificates used for server verification.

`--daemon-timeout <duration>`
:   Timeout waiting for {{agent}} daemon.

`--delay-enroll`
:   Delays enrollment to occur on first start of the {{agent}} service. This setting is useful when you don’t want the {{agent}} to enroll until the next reboot or manual start of the service, for example, when you’re preparing an image that includes {{agent}}.

`--elastic-agent-cert`
:   Certificate to use as the client certificate for the {{agent}}'s connections to {{fleet-server}}.

`--elastic-agent-cert-key`
:   Private key to use as for the {{agent}}'s connections to {{fleet-server}}.

`--elastic-agent-cert-key-passphrase`
:   The path to the file that contains the passphrase for the mutual TLS private key that {{agent}} will use to connect to {{fleet-server}}. The file must only contain the characters of the passphrase, no newline or extra non-printing characters.

    This option is only used if the `--elastic-agent-cert-key` is encrypted and requires a passphrase to use.


`--enrollment-token <string>`
:   Enrollment token to use to enroll {{agent}} into {{fleet}}. You can use the same enrollment token for multiple agents.

`--fleet-server-cert <string>`
:   Certificate to use for exposed {{fleet-server}} HTTPS endpoint.

`--fleet-server-cert-key <string>`
:   Private key to use for exposed {{fleet-server}} HTTPS endpoint.

`--fleet-server-cert-key-passphrase <string>`
:   Path to passphrase file for decrypting {{fleet-server}}'s private key if an encrypted private key is used.

`--fleet-server-client-auth <string>`
:   One of `none`, `optional`, or `required`. Defaults to `none`. {{fleet-server}}'s `client_authentication` option for client mTLS connections. If `optional`, or `required` is specified, client certificates are verified using CAs specified in the `--certificate-authorities` flag.

`--fleet-server-es <string>`
:   Start a {{fleet-server}} process when {{agent}} is started, and connect to the specified {{es}} URL.

`--fleet-server-es-ca <string>`
:   Path to certificate authority to use to communicate with {{es}}.

`--fleet-server-es-ca-trusted-fingerprint <string>`
:   The SHA-256 fingerprint (hash) of the certificate authority used to self-sign {{es}} certificates. This fingerprint will be used to verify self-signed certificates presented by {{fleet-server}} and any inputs started by {{agent}} for communication. This flag is required when using self-signed certificates with {{es}}.

`--fleet-server-es-cert`
:   The path to the client certificate that {{fleet-server}} will use when connecting to {{es}}.

`--fleet-server-es-cert-key`
:   The path to the private key that {{fleet-server}} will use when connecting to {{es}}.

`--fleet-server-es-insecure`
:   Allows fleet server to connect to {{es}} in the following situations:

    * When connecting to an HTTP server.
    * When connecting to an HTTPs server and the certificate chain cannot be verified. The content is encrypted, but the certificate is not verified.

    When this flag is used the certificate verification is disabled.


`--fleet-server-host <string>`
:   {{fleet-server}} HTTP binding host (overrides the policy).

`--fleet-server-policy <string>`
:   Used when starting a self-managed {{fleet-server}} to allow a specific policy to be used.

`--fleet-server-port <uint16>`
:   {{fleet-server}} HTTP binding port (overrides the policy).

`--fleet-server-service-token <string>`
:   Service token to use for communication with {{es}}. Mutually exclusive with `--fleet-server-service-token-path`.

`--fleet-server-service-token-path <string>`
:   Service token file to use for communication with {{es}}. Mutually exclusive with `--fleet-server-service-token`.

`--fleet-server-timeout <duration>`
:   Timeout waiting for {{fleet-server}} to be ready to start enrollment.

`--force`
:   Force overwrite of current configuration without prompting for confirmation. This flag is helpful when using automation software or scripted deployments.

    ::::{note}
    If the {{agent}} is already installed on the host, using `--force` may result in unpredictable behavior with duplicate {{agent}}s appearing in {{fleet}}.
    ::::


`--header <strings>`
:   Headers used in communication with elasticsearch.

`--help`
:   Show help for the `enroll` command.

`--insecure`
:   Allow the {{agent}} to connect to {{fleet-server}} over insecure connections. This setting is required in the following situations:

    * When connecting to an HTTP server. The API keys are sent in clear text.
    * When connecting to an HTTPs server and the certificate chain cannot be verified. The content is encrypted, but the certificate is not verified.
    * When using self-signed certificates generated by {{agent}}.

    We strongly recommend that you use a secure connection.


`--non-interactive`
:   Install {{agent}} in a non-interactive mode. This flag is helpful when using automation software or scripted deployments. If {{agent}} is already installed on the host, the installation will terminate.

`--proxy-disabled`
:   Disable proxy support including environment variables.

`--proxy-header <strings>`
:   Proxy headers used with CONNECT request.

`--proxy-url <string>`
:   Configures the proxy URL.

`--staging <string>`
:   Configures agent to download artifacts from a staging build.

`--tag <string>`
:   A comma-separated list of tags to apply to {{fleet}}-managed {{agent}}s. You can use these tags to filter the list of agents in {{fleet}}.

    ::::{note}
    Currently, there is no way to remove or edit existing tags. To change the tags, you must unenroll the {{agent}}, then re-enroll it using new tags.
    ::::


`--url <string>`
:   {{fleet-server}} URL to use to enroll the {{agent}} into {{fleet}}.

For more flags, see [Global flags](#elastic-agent-global-flags).


### Examples [_examples_11]

Enroll the {{agent}} in {{fleet}}:

```shell
elastic-agent enroll \
  --url=https://cedd4e0e21e240b4s2bbbebdf1d6d52f.fleet.eu-west-1.aws.cld.elstc.co:443 \
  --enrollment-token=NEFmVllaa0JLRXhKebVKVTR5TTI6N2JaVlJpSGpScmV0ZUVnZVlRUExFQQ==
```

Enroll the {{agent}} in {{fleet}} and set up {{fleet-server}}:

```shell
elastic-agent enroll --fleet-server-es=http://elasticsearch:9200 \
  --fleet-server-service-token=AbEAAdesYXN1abMvZmxlZXQtc2VldmVyL3Rva2VuLTE2MTkxMzg3MzIzMTg7dzEta0JDTmZUcGlDTjlwRmNVTjNVQQ \
  --fleet-server-policy=a35fd520-26f5-11ec-8bd9-3374690g57b6
```

Start {{agent}} with {{fleet-server}} (running on a custom CA). This example assumes you’ve generated the certificates with the following names:

* `ca.crt`: Root CA certificate
* `fleet-server.crt`: {{fleet-server}} certificate
* `fleet-server.key`: {{fleet-server}} private key
* `elasticsearch-ca.crt`: CA certificate to use to connect to {es}

```shell
elastic-agent enroll \
  --url=https://fleet-server:8220 \
  --fleet-server-es=https://elasticsearch:9200 \
  --fleet-server-service-token=AAEBAWVsYXm0aWMvZmxlZXQtc2XydmVyL3Rva2VuLTE2MjM4OTAztDU1OTQ6dllfVW1mYnFTVjJwTC2ZQ0EtVnVZQQ \
  --fleet-server-policy=a35fd520-26f5-11ec-8bd9-3374690g57b6 \
  --certificate-authorities=/path/to/ca.crt \
  --fleet-server-es-ca=/path/to/elasticsearch-ca.crt \
  --fleet-server-cert=/path/to/fleet-server.crt \
  --fleet-server-cert-key=/path/to/fleet-server.key \
  --fleet-server-port=8220
```

Then enroll another {{agent}} into the {{fleet-server}} started in the previous example:

```shell
elastic-agent enroll --url=https://fleet-server:8220 \
  --enrollment-token=NEFmVllaa0JLRXhKebVKVTR5TTI6N2JaVlJpSGpScmV0ZUVnZVlRUExFQQ== \
  --certificate-authorities=/path/to/ca.crt
```

<hr>

## elastic-agent help [elastic-agent-help-command]

Show help for a specific command.


### Synopsis [_synopsis_3]

```shell
elastic-agent help <command> [--help] [global-flags]
```


### Options [_options_3]

`command`
:   The name of the command.

`--help`
:   Show help for the `help` command.

For more flags, see [Global flags](#elastic-agent-global-flags).


### Example [_example_39]

```shell
elastic-agent help enroll
```

<hr>

## elastic-agent inspect [elastic-agent-inspect-command]

Show the current {{agent}} configuration.

If no parameters are specified, shows the full {{agent}} configuration.


### Synopsis [_synopsis_4]

```shell
elastic-agent inspect [--help]
elastic-agent inspect components [--show-config]
                             [--show-spec]
                             [--help]
                             [id]
```


### Options [_options_4]

`components`
:   Display the current configuration for the component. This command accepts additional flags:

    `--show-config`
    :   Use to display the configuration in all units.

    `--show-spec`
    :   Use to get input/output runtime spectification for a component.


`--help`
:   Show help for the `inspect` command.

For more flags, see [Global flags](#elastic-agent-global-flags).


### Examples [_examples_12]

```shell
elastic-agent inspect
elastic-agent inspect components --show-config
elastic-agent inspect components log-default
```

<hr>

## elastic-agent privileged [elastic-agent-privileged-command]

Run {{agent}} with full superuser privileges. This is the usual, default running mode for {{agent}}. The `privileged` command allows you to switch back to running an agent with full administrative privileges when you have been running it in `unprivileged` mode.

Refer to [Run {{agent}} without administrative privileges](/reference/ingestion-tools/fleet/elastic-agent-unprivileged.md) for more detail.


### Examples [_examples_13]

```shell
elastic-agent privileged
```

<hr>

## elastic-agent install [elastic-agent-install-command]

Install {{agent}} permanently on the system and manage it by using the system’s service manager. The agent will start automatically after installation is complete. On Linux (tar package), this command requires a system and service manager like systemd.

::::{important}
If you installed {{agent}} from a DEB or RPM package, the `install` command will skip the installation itself and function as an alias of the [`enroll` command](#elastic-agent-enroll-command) instead. Note that after an upgrade of the {{agent}} using DEB or RPM the {{agent}} service needs to be restarted.
::::


You must run this command as the root user (or Administrator on Windows) to write files to the correct locations. This command overwrites the `elastic-agent.yml` file in the agent directory.

The syntax for running this command varies by platform. For platform-specific examples, refer to [*Install {{agent}}s*](/reference/ingestion-tools/fleet/install-elastic-agents.md).


### Synopsis [_synopsis_5]

To install the {{agent}} as a service, enroll it in {{fleet}}, and start the `elastic-agent` service:

```shell
elastic-agent install --url <string>
                      --enrollment-token <string>
                      [--base-path <string>]
                      [--ca-sha256 <string>]
                      [--certificate-authorities <string>]
                      [--daemon-timeout <duration>]
                      [--delay-enroll]
                      [--elastic-agent-cert <string>]
                      [--elastic-agent-cert-key <string>]
                      [--elastic-agent-cert-key-passphrase <string>]
                      [--force]
                      [--header <strings>]
                      [--help]
                      [--insecure ]
                      [--non-interactive]
                      [--privileged]
                      [--proxy-disabled]
                      [--proxy-header <strings>]
                      [--proxy-url <string>]
                      [--staging <string>]
                      [--tag <string>]
                      [--unprivileged]
                      [global-flags]
```

To install the {{agent}} as a service, enroll it in {{fleet}}, and start a `fleet-server` process alongside the `elastic-agent` service:

```shell
elastic-agent install --fleet-server-es <string>
                      --fleet-server-service-token <string>
                      [--fleet-server-service-token-path <string>]
                      [--base-path <string>]
                      [--ca-sha256 <string>]
                      [--certificate-authorities <string>]
                      [--daemon-timeout <duration>]
                      [--delay-enroll]
                      [--elastic-agent-cert <string>]
                      [--elastic-agent-cert-key <string>]
                      [--elastic-agent-cert-key-passphrase <string>]
                      [--fleet-server-cert <string>] <1>
                      [--fleet-server-cert-key <string>]
                      [--fleet-server-cert-key-passphrase <string>]
                      [--fleet-server-client-auth <string>]
                      [--fleet-server-es-ca <string>]
                      [--fleet-server-es-ca-trusted-fingerprint <string>] <2>
                      [--fleet-server-es-cert <string>]
                      [--fleet-server-es-cert-key <string>]
                      [--fleet-server-es-insecure]
                      [--fleet-server-host <string>]
                      [--fleet-server-policy <string>]
                      [--fleet-server-port <uint16>]
                      [--fleet-server-timeout <duration>]
                      [--force]
                      [--header <strings>]
                      [--help]
                      [--non-interactive]
                      [--privileged]
                      [--proxy-disabled]
                      [--proxy-header <strings>]
                      [--proxy-url <string>]
                      [--staging <string>]
                      [--tag <string>]
                      [--unprivileged]
                      [--url <string>] <3>
                      [global-flags]
```

1. If no `fleet-server-cert*` flags are specified, {{agent}} auto-generates a self-signed certificate with the hostname of the machine. Remote {{agent}}s enrolling into a {{fleet-server}} with self-signed certificates must specify the `--insecure` flag.
2. Required when using self-signed certificate on {{es}} side.
3. Required when enrolling in a {{fleet-server}} with custom certificates. The URL must match the DNS name used to generate the certificate specified by `--fleet-server-cert`.


For more information about custom certificates, refer to [Configure SSL/TLS for self-managed {{fleet-server}}s](/reference/ingestion-tools/fleet/secure-connections.md).


### Options [_options_5]

`--base-path <string>`
:   Install {{agent}} in a location other than the [default](/reference/ingestion-tools/fleet/installation-layout.md). Specify the custom base path for the install.

    The `--base-path` option is not currently supported with [{{elastic-defend}}](/reference/security/elastic-defend/install-endpoint.md).


`--ca-sha256 <string>`
:   Comma-separated list of certificate authority hash pins used for certificate verification.

`--certificate-authorities <string>`
:   Comma-separated list of root certificates used for server verification.

`--daemon-timeout <duration>`
:   Timeout waiting for {{agent}} daemon.

`--delay-enroll`
:   Delays enrollment to occur on first start of the {{agent}} service. This setting is useful when you don’t want the {{agent}} to enroll until the next reboot or manual start of the service, for example, when you’re preparing an image that includes {{agent}}.

`--elastic-agent-cert`
:   Certificate to use as the client certificate for the {{agent}}'s connections to {{fleet-server}}.

`--elastic-agent-cert-key`
:   Private key to use as for the {{agent}}'s connections to {{fleet-server}}.

`--elastic-agent-cert-key-passphrase`
:   The path to the file that contains the passphrase for the mutual TLS private key that {{agent}} will use to connect to {{fleet-server}}. The file must only contain the characters of the passphrase, no newline or extra non-printing characters.

    This option is only used if the `--elastic-agent-cert-key` is encrypted and requires a passphrase to use.


`--enrollment-token <string>`
:   Enrollment token to use to enroll {{agent}} into {{fleet}}. You can use the same enrollment token for multiple agents.

`--fleet-server-cert <string>`
:   Certificate to use for exposed {{fleet-server}} HTTPS endpoint.

`--fleet-server-cert-key <string>`
:   Private key to use for exposed {{fleet-server}} HTTPS endpoint.

`--fleet-server-cert-key-passphrase <string>`
:   Path to passphrase file for decrypting {{fleet-server}}'s private key if an encrypted private key is used.

`--fleet-server-client-auth <string>`
:   One of `none`, `optional`, or `required`. Defaults to `none`. {{fleet-server}}'s `client_authentication` option for client mTLS connections. If `optional`, or `required` is specified, client certificates are verified using CAs specified in the `--certificate-authorities` flag.

`--fleet-server-es <string>`
:   Start a {{fleet-server}} process when {{agent}} is started, and connect to the specified {{es}} URL.

`--fleet-server-es-ca <string>`
:   Path to certificate authority to use to communicate with {{es}}.

`--fleet-server-es-ca-trusted-fingerprint <string>`
:   The SHA-256 fingerprint (hash) of the certificate authority used to self-sign {{es}} certificates. This fingerprint will be used to verify self-signed certificates presented by {{fleet-server}} and any inputs started by {{agent}} for communication. This flag is required when using self-signed certificates with {{es}}.

`--fleet-server-es-cert`
:   The path to the client certificate that {{fleet-server}} will use when connecting to {{es}}.

`--fleet-server-es-cert-key`
:   The path to the private key that {{fleet-server}} will use when connecting to {{es}}.

`--fleet-server-es-insecure`
:   Allows fleet server to connect to {{es}} in the following situations:

    * When connecting to an HTTP server.
    * When connecting to an HTTPs server and the certificate chain cannot be verified. The content is encrypted, but the certificate is not verified.

    When this flag is used the certificate verification is disabled.


`--fleet-server-host <string>`
:   {{fleet-server}} HTTP binding host (overrides the policy).

`--fleet-server-policy <string>`
:   Used when starting a self-managed {{fleet-server}} to allow a specific policy to be used.

`--fleet-server-port <uint16>`
:   {{fleet-server}} HTTP binding port (overrides the policy).

`--fleet-server-service-token <string>`
:   Service token to use for communication with {{es}}. Mutually exclusive with `--fleet-server-service-token-path`.

`--fleet-server-service-token-path <string>`
:   Service token file to use for communication with {{es}}. Mutually exclusive with `--fleet-server-service-token`.

`--fleet-server-timeout <duration>`
:   Timeout waiting for {{fleet-server}} to be ready to start enrollment.

`--force`
:   Force overwrite of current configuration without prompting for confirmation. This flag is helpful when using automation software or scripted deployments.

    ::::{note}
    If the {{agent}} is already installed on the host, using `--force` may result in unpredictable behavior with duplicate {{agent}}s appearing in {{fleet}}.
    ::::


`--header <strings>`
:   Headers used in communication with elasticsearch.

`--help`
:   Show help for the `enroll` command.

`--insecure`
:   Allow the {{agent}} to connect to {{fleet-server}} over insecure connections. This setting is required in the following situations:

    * When connecting to an HTTP server. The API keys are sent in clear text.
    * When connecting to an HTTPs server and the certificate chain cannot be verified. The content is encrypted, but the certificate is not verified.
    * When using self-signed certificates generated by {{agent}}.

    We strongly recommend that you use a secure connection.


`--non-interactive`
:   Install {{agent}} in a non-interactive mode. This flag is helpful when using automation software or scripted deployments. If {{agent}} is already installed on the host, the installation will terminate.

`--privileged`
:   Run {{agent}} with full superuser privileges. This is the usual, default running mode for {{agent}}. The `--privileged` option allows you to switch back to running an agent with full administrative privileges when you have been running it in `unprivileged`.

See the `--unprivileged` option and [Run {{agent}} without administrative privileges](/reference/ingestion-tools/fleet/elastic-agent-unprivileged.md) for more detail.

`--proxy-disabled`
:   Disable proxy support including environment variables.

`--proxy-header <strings>`
:   Proxy headers used with CONNECT request.

`--proxy-url <string>`
:   Configures the proxy URL.

`--staging <string>`
:   Configures agent to download artifacts from a staging build.

`--tag <strings>`
:   A comma-separated list of tags to apply to {{fleet}}-managed {{agent}}s. You can use these tags to filter the list of agents in {{fleet}}.

    ::::{note}
    Currently, there is no way to remove or edit existing tags. To change the tags, you must unenroll the {{agent}}, then re-enroll it using new tags.
    ::::


`--unprivileged`
:   Run {{agent}} without full superuser privileges. This option is useful in organizations that limit `root` access on Linux or macOS systems, or `admin` access on Windows systems. For details and limitations for running {{agent}} in this mode, refer to [Run {{agent}} without administrative privileges](/reference/ingestion-tools/fleet/elastic-agent-unprivileged.md).

    Note that changing to `unprivileged` mode is prevented if the agent is currently enrolled in a policy that includes an integration that requires administrative access, such as the {{elastic-defend}} integration.

    [preview] To run {{agent}} without superuser privileges as a pre-existing user or group, for instance under an Active Directory account, you can specify the user or group, and the password to use.

    For example:

    ```shell
    elastic-agent install --unprivileged  --user="my.path\username" --password="mypassword"
    ```

    ```shell
    elastic-agent install --unprivileged  --group="my.path\groupname" --password="mypassword"
    ```


`--url <string>`
:   {{fleet-server}} URL to use to enroll the {{agent}} into {{fleet}}.

For more flags, see [Global flags](#elastic-agent-global-flags).


### Examples [_examples_14]

Install the {{agent}} as a service, enroll it in {{fleet}}, and start the `elastic-agent` service:

```shell
elastic-agent install \
  --url=https://cedd4e0e21e240b4s2bbbebdf1d6d52f.fleet.eu-west-1.aws.cld.elstc.co:443 \
  --enrollment-token=NEFmVllaa0JLRXhKebVKVTR5TTI6N2JaVlJpSGpScmV0ZUVnZVlRUExFQQ==
```

Install the {{agent}} as a service, enroll it in {{fleet}}, and start a `fleet-server` process alongside the `elastic-agent` service:

```shell
elastic-agent install --fleet-server-es=http://elasticsearch:9200 \
  --fleet-server-service-token=AbEAAdesYXN1abMvZmxlZXQtc2VldmVyL3Rva2VuLTE2MTkxMzg3MzIzMTg7dzEta0JDTmZUcGlDTjlwRmNVTjNVQQ \
  --fleet-server-policy=a35fd620-26f6-11ec-8bd9-3374690f57b6
```

Start {{agent}} with {{fleet-server}} (running on a custom CA). This example assumes you’ve generated the certificates with the following names:

* `ca.crt`: Root CA certificate
* `fleet-server.crt`: {{fleet-server}} certificate
* `fleet-server.key`: {{fleet-server}} private key
* `elasticsearch-ca.crt`: CA certificate to use to connect to {es}

```shell
elastic-agent install \
  --url=https://fleet-server:8220 \
  --fleet-server-es=https://elasticsearch:9200 \
  --fleet-server-service-token=AAEBAWVsYXm0aWMvZmxlZXQtc2XydmVyL3Rva2VuLTE2MjM4OTAztDU1OTQ6dllfVW1mYnFTVjJwTC2ZQ0EtVnVZQQ \
  --fleet-server-policy=a35fd520-26f5-11ec-8bd9-3374690g57b6 \
  --certificate-authorities=/path/to/ca.crt \
  --fleet-server-es-ca=/path/to/elasticsearch-ca.crt \
  --fleet-server-cert=/path/to/fleet-server.crt \
  --fleet-server-cert-key=/path/to/fleet-server.key \
  --fleet-server-port=8220
```

Then install another {{agent}} and enroll it into the {{fleet-server}} started in the previous example:

```shell
elastic-agent install --url=https://fleet-server:8220 \
  --enrollment-token=NEFmVllaa0JLRXhKebVKVTR5TTI6N2JaVlJpSGpScmV0ZUVnZVlRUExFQQ== \
  --certificate-authorities=/path/to/ca.crt
```

<hr>

## elastic-agent otel [elastic-agent-otel-command]

::::{warning}
This functionality is in technical preview and may be changed or removed in a future release. Elastic will work to fix any issues, but features in technical preview are not subject to the support SLA of official GA features.
::::


Run {{agent}} as an [OpenTelemetry Collector](/reference/ingestion-tools/fleet/otel-agent.md).


### Synopsis [_synopsis_6]

```shell
elastic-agent otel [flags]
elastic-agent otel [command]
```

::::{note}
You can also run the `./otelcol` command, which calls `./elastic-agent otel` and passes any arguments to it.
::::



### Available commands [_available_commands]

`validate`
:   Validates the OpenTelemetry collector configuration without running the collector.


### Flags [_flags]

`--config=file:/path/to/first --config=file:path/to/second`
:   Locations to the config file(s). Note that only a single location can be set per flag entry, for example `--config=file:/path/to/first --config=file:path/to/second`.

`--feature-gates flag`
:   Comma-delimited list of feature gate identifiers. Prefix with `-` to disable the feature. Prefixing with `+` or no prefix will enable the feature.

`-h, --help`
:   Get help for the `otel` sub-command. Use `elastic-agent otel [command] --help` for more information about a command.

`--set string`
:   Set an arbitrary component config property. The component has to be defined in the configuration file and the flag has a higher precedence. Array configuration properties are overridden and maps are joined. For example, `--set=processors::batch::timeout=2s`.


### Examples [_examples_15]

Run {{agent}} as on OTel Collector using the supplied `otel.yml` configuration file.

```shell
./elastic-agent otel --config otel.yml
```

Change the default verbosity setting in the {{agent}} OTel configuration from `detailed` to `normal`.

```shell
./elastic-agent otel --config otel.yml --set "exporters::debug::verbosity=normal"
```

<hr>

## elastic-agent restart [elastic-agent-restart-command]

Restart the currently running {{agent}} daemon.


### Synopsis [_synopsis_7]

```shell
elastic-agent restart [--help] [global-flags]
```


### Options [_options_6]

`--help`
:   Show help for the `restart` command.

For more flags, see [Global flags](#elastic-agent-global-flags).


### Examples [_examples_16]

```shell
elastic-agent restart
```

<hr>

## elastic-agent run [elastic-agent-run-command]

Start the `elastic-agent` process.


### Synopsis [_synopsis_8]

```shell
elastic-agent run [global-flags]
```


### Global flags [elastic-agent-global-flags]

These flags are valid whenever you run `elastic-agent` on the command line.

`-c <string>`
:   The configuration file to use. If not specified, {{agent}} uses `{path.config}/elastic-agent.yml`.

`--e`
:   Log to stderr and disable syslog/file output.

`--environment <environmentVar>`
:   The environment in which the agent will run.

`--path.config <string>`
:   The directory where {{agent}} looks for its configuration file. The default varies by platform.

`--path.home <string>`
:   The root directory of {{agent}}. `path.home` determines the location of the configuration files and data directory.

    If not specified, {{agent}} uses the current working directory.


`--path.logs <string>`
:   Path to the log output for {{agent}}. The default varies by platform.

`--v`
:   Set log level to INFO.


### Example [_example_40]

```shell
elastic-agent run -c myagentconfig.yml
```

<hr>

## elastic-agent status [elastic-agent-status-command]

Returns the current status of the running {{agent}} daemon and of each process in the {{agent}}.  The last known status of the {{fleet}} server is also returned. The `output` option controls the level of detail and formatting of the information.


### Synopsis [_synopsis_9]

```shell
elastic-agent status [--output <string>]
                     [--help]
                     [global-flags]
```


### Options [_options_7]

`--output <string>`
:   Output the status information in either `human` (the default), `full`, `json`, or `yaml`.  `human` returns limited information when {{agent}} is in the `HEALTHY` state. If any components or units are not in `HEALTHY` state, then full details are displayed for that component or unit.  `full`, `json` and `yaml` always return the full status information.  Components map to individual processes running underneath {{agent}}, for example {{filebeat}} or {{endpoint-sec}}. Units map to discrete configuration units within that process, for example {{filebeat}} inputs or {{metricbeat}} modules.

When the output is `json` or `yaml`, status codes are returned as numerical values.  The status codes can be mapped using the following table:

+

| Code | Status |
| --- | --- |
| 0 | `STARTING` |
| 1 | `CONFIGURING` |
| 2 | `HEALTHY` |
| 3 | `DEGRADED` |
| 4 | `FAILED` |
| 5 | `STOPPING` |
| 6 | `UPGRADING` |
| 7 | `ROLLBACK` |

`--help`
:   Show help for the `status` command.

For more flags, see [Global flags](#elastic-agent-global-flags).


### Examples [_examples_17]

```shell
elastic-agent status
```

<hr>

## elastic-agent uninstall [elastic-agent-uninstall-command]

Permanently uninstall {{agent}} from the system.

You must run this command as the root user (or Administrator on Windows) to remove files.

::::{important}
Be sure to run the `uninstall` command from a directory outside of where {{agent}} is installed.

For example, on a Windows system the install location is `C:\Program Files\Elastic\Agent`. Run the uninstall command from `C:\Program Files\Elastic` or `\tmp`, or even your default home directory:

```shell
C:\"Program Files"\Elastic\Agent\elastic-agent.exe uninstall
```

::::


:::::::{tab-set}

::::::{tab-item} macOS
::::{tip}
You must run this command as the root user.
::::


```shell
sudo /Library/Elastic/Agent/elastic-agent uninstall
```
::::::

::::::{tab-item} Linux
::::{tip}
You must run this command as the root user.
::::


```shell
sudo /opt/Elastic/Agent/elastic-agent uninstall
```
::::::

::::::{tab-item} Windows
Open a PowerShell prompt as an Administrator (right-click the PowerShell icon and select **Run As Administrator**).

From the PowerShell prompt, run:

```shell
C:\"Program Files"\Elastic\Agent\elastic-agent.exe uninstall
```
::::::

:::::::

### Synopsis [_synopsis_10]

```shell
elastic-agent uninstall [--force] [--help] [global-flags]
```


### Options [_options_8]

`--force`
:   Uninstall {{agent}} and do not prompt for confirmation. This flag is helpful when using automation software or scripted deployments.

`--skip-fleet-audit`
:   Skip auditing with the {{fleet-server}}.

`--help`
:   Show help for the `uninstall` command.

For more flags, see [Global flags](#elastic-agent-global-flags).


### Examples [_examples_18]

```shell
elastic-agent uninstall
```

<hr>

## elastic-agent unprivileged [elastic-agent-unprivileged-command]

Run {{agent}} without full superuser privileges. This is useful in organizations that limit `root` access on Linux or macOS systems, or `admin` access on Windows systems. For details and limitations for running {{agent}} in this mode, refer to [Run {{agent}} without administrative privileges](/reference/ingestion-tools/fleet/elastic-agent-unprivileged.md).

Note that changing a running {{agent}} to `unprivileged` mode is prevented if the agent is currently enrolled with a policy that contains the {{elastic-defend}} integration.

[preview] To run {{agent}} without superuser privileges as a pre-existing user or group, for instance under an Active Directory account, add either a `--user` or `--group` parameter together with a `--password` parameter.


### Examples [_examples_19]

Run {{agent}} without administrative privileges:

```shell
elastic-agent unprivileged
```

[preview] Run {{agent}} without administrative privileges, as a pre-existing user:

```shell
elastic-agent unprivileged --user="my.pathl\username" --password="mypassword"
```

[preview] Run {{agent}} without administrative privileges, as a pre-existing group:

```shell
elastic-agent unprivileged --group="my.pathl\groupname" --password="mypassword"
```

<hr>

## elastic-agent upgrade [elastic-agent-upgrade-command]

Upgrade the currently running {{agent}} to the specified version. This should only be used with agents running in standalone mode. Agents enrolled in {{fleet}} should be upgraded through {{fleet}}.


### Synopsis [_synopsis_11]

```shell
elastic-agent upgrade <version> [--source-uri <string>] [--help] [flags]
```


### Options [_options_9]

`version`
:   The version of {{agent}} to upgrade to.

`--source-uri <string>`
:   The source URI to download the new version from. By default, {{agent}} uses the Elastic Artifacts URL.

`--skip-verify`
:   Skip the package verification process. This option is not recommended as it is insecure.

`--pgp-path <string>`
:   Use a locally stored copy of the PGP key to verify the upgrade package.

`--pgp-uri <string>`
:   Use the specified online PGP key to verify the upgrade package.

`--help`
:   Show help for the `upgrade` command.

For details about using the `--skip-verify`, `--pgp-path <string>`, and `--pgp-uri <string>` package verification options, refer to [Verifying {{agent}} package signatures](/reference/ingestion-tools/fleet/upgrade-standalone.md#upgrade-standalone-verify-package).

For more flags, see [Global flags](#elastic-agent-global-flags).


### Examples [_examples_20]

```shell
elastic-agent upgrade 7.10.1
```

<hr>

## elastic-agent logs [elastic-agent-logs-command]

Show the logs of the running {{agent}}.


### Synopsis [_synopsis_12]

```shell
elastic-agent logs [--follow] [--number <int>] [--component <string>] [--no-color] [--help] [global-flags]
```


### Options [_options_10]

`--follow` or `-f`
:   Follow log updates until the command is interrupted (for example with `Ctrl-C`).

`--number <int>` or `-n <int>`
:   How many lines of logs to print. If logs following is enabled, affects the initial output.

`--component <string>` or `-C <string>`
:   Filter logs based on the component name.

`--no-color`
:   Disable color based on log-level of each entry.

`--help`
:   Show help for the `logs` command.

For more flags, see [Global flags](#elastic-agent-global-flags).


### Example [_example_41]

```shell
elastic-agent logs -n 100 -f -C "system/metrics-default"
```

<hr>

## elastic-agent version [elastic-agent-version-command]

Show the version of {{agent}}.


### Synopsis [_synopsis_13]

```shell
elastic-agent version [--help] [global-flags]
```


### Options [_options_11]

`--help`
:   Show help for the `version` command.

For more flags, see [Global flags](#elastic-agent-global-flags).


### Example [_example_42]

```shell
elastic-agent version
```

<hr>
