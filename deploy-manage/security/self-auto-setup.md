---
navigation_title: Automatic security setup
applies_to:
  self: ga
sub:
  es-conf: "/etc/elasticsearch"
  slash: "/"
  escape: "\\"
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/configuring-stack-security.html
---

% Scope: Automatic setup
% Original title: Start the Elastic Stack with security enabled automatically
# Automatic security setup [configuring-stack-security]

:::{include} /deploy-manage/deploy/self-managed/_snippets/auto-security-config.md
:::

## Prerequisites [_prerequisites_12]

* [Download](https://www.elastic.co/downloads/elasticsearch) and unpack the `elasticsearch` package distribution for your environment.
* [Download](https://www.elastic.co/downloads/kibana) and unpack the `kibana` package distribution for your environment.

::::{note}
This guide assumes a `.tar.gz` installation of {{es}} and {{kib}} on Linux.
For instructions tailored to other installation packages (such as DEB, RPM, Docker, or macOS), refer to the [{{es}}](/deploy-manage/deploy/self-managed/installing-elasticsearch.md#elasticsearch-install-packages) and [{{kib}}](/deploy-manage/deploy/self-managed/install-kibana.md#install) installation guides.
::::

## Start {{es}} and enroll {{kib}} with security enabled [stack-start-with-security]

1. From the installation directory, start {{es}}.

    ```shell
    bin/elasticsearch
    ```

    The command prints the `elastic` user password and an enrollment token for {{kib}}.

2. Copy the generated `elastic` password and enrollment token. These credentials are only shown when you start {{es}} for the first time.

    ::::{note}
    If you need to reset the password for the `elastic` user or other built-in users, run the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) tool. To generate new enrollment tokens for {{kib}} or {{es}} nodes, run the [`elasticsearch-create-enrollment-token`](elasticsearch://reference/elasticsearch/command-line-tools/create-enrollment-token.md) tool. These tools are available in the {{es}} `bin` directory.

    ::::


    We recommend storing the `elastic` password as an environment variable in your shell. Example:

    ```sh
    export ELASTIC_PASSWORD="your_password"
    ```

3. (Optional) Open a new terminal and verify that you can connect to your {{es}} cluster by making an authenticated call.

    ```shell
    curl --cacert config/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
    ```

4. From the directory where you installed {{kib}}, start {{kib}}.

    ```shell
    bin/kibana
    ```

5. Enroll {{kib}} using either interactive or detached mode.

    * **Interactive mode** (browser)

        1. In your terminal, click the generated link to open {{kib}} in your browser.
        2. In your browser, paste the enrollment token that you copied and click the button to connect your {{kib}} instance with {{es}}.

            ::::{note}
            {{kib}} won’t enter interactive mode if it detects existing credentials for {{es}} (`elasticsearch.username` and `elasticsearch.password`) or an existing URL for `elasticsearch.hosts`.

            ::::

    * **Detached mode** (non-browser)

        Run the `kibana-setup` tool and pass the generated enrollment token with the `--enrollment-token` parameter.

        ```sh
        bin/kibana-setup --enrollment-token <enrollment-token>
        ```

## Enroll additional nodes in your cluster [stack-enroll-nodes]

:::{include} /deploy-manage/deploy/self-managed/_snippets/enroll-nodes.md
:::

## Connect clients to {{es}} [_connect_clients_to_es_5]

:::{include} /deploy-manage/deploy/self-managed/_snippets/connect-clients.md
:::

### Use the CA fingerprint [_use_the_ca_fingerprint_5]

:::{include} /deploy-manage/deploy/self-managed/_snippets/ca-fingerprint.md
:::

### Use the CA certificate [_use_the_ca_certificate_5]

:::{include} /deploy-manage/deploy/self-managed/_snippets/ca-cert.md
:::

## What’s next? [_whats_next]

Congratulations! You’ve successfully started the {{stack}} with security enabled. {{es}} and {{kib}} are secured with TLS on the HTTP layer, and internode communication is encrypted. If you want to enable HTTPS for web traffic, you can [encrypt traffic between your browser and {{kib}}](set-up-basic-security-plus-https.md#encrypt-kibana-browser).


## Security certificates and keys [stack-security-certificates]

:::{include} /deploy-manage/deploy/self-managed/_snippets/security-files.md
:::

## Cases when security auto configuration is skipped [stack-skip-auto-configuration]

When you start {{es}} for the first time, the node startup process tries to automatically configure security for you. The process runs some checks to determine:

* If this is the first time that the node is starting
* Whether security is already configured
* If the startup process can modify the node configuration

If any of those checks fail, there’s a good indication that you manually configured security, or don’t want security to be configured automatically. In these cases, the node starts normally using the existing configuration.

::::{important}
If you redirect {{es}} output to a file, security autoconfiguration is skipped. Autoconfigured credentials can only be viewed on the terminal the first time you start {{es}}. If you need to redirect output to a file, start {{es}} without redirection the first time and use redirection on all subsequent starts.
::::

### Existing environment detected [stack-existing-environment-detected]

If certain directories already exist, there’s a strong indication that the node was started previously. Similarly, if certain files *don’t* exist, or we can’t read or write to specific files or directories, then we’re likely not running as the user who installed {{es}} or an administrator imposed restrictions. If any of the following environment checks are true, security isn’t configured automatically.

The {{es}} `/data` directory exists and isn’t empty
:   The existence of this directory is a strong indicator that the node was started previously, and might already be part of a cluster.

The `elasticsearch.yml` file doesn’t exist (or isn’t readable), or the `elasticsearch.keystore` isn’t readable
:   If either of these files aren’t readable, we can’t determine whether {{es}} security features are already enabled. This state can also indicate that the node startup process isn’t running as a user with sufficient privileges to modify the node configuration.

The {{es}} configuration directory isn’t writable
:   This state likely indicates that an administrator made this directory read-only, or that the user who is starting {{es}} is not the user that installed {{es}}.


### Existing settings detected [stack-existing-settings-detected]

The following settings are incompatible with security auto configuration. If any of these settings exist, the node startup process skips configuring security automatically and the node starts normally.

* [`node.roles`](elasticsearch://reference/elasticsearch/configuration-reference/node-settings.md#node-roles) is set to a value where the node can’t be elected as `master`, or if the node can’t hold data
* [`xpack.security.autoconfiguration.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#general-security-settings) is set to `false`
* [`xpack.security.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#general-security-settings) has a value set
* Any of the [`xpack.security.transport.ssl.*`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#transport-tls-ssl-settings) or [`xpack.security.http.ssl.*`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#http-tls-ssl-settings) settings have a value set in the `elasticsearch.yml` configuration file or in the `elasticsearch.keystore`
* Any of the `discovery.type`, `discovery.seed_hosts`, or `cluster.initial_master_nodes` [discovery and cluster formation settings](elasticsearch://reference/elasticsearch/configuration-reference/discovery-cluster-formation-settings.md) have a value set

    ::::{note}
    Exceptions are when `discovery.type` is set to `single-node`, or when `cluster.initial_master_nodes` exists but contains only the name of the current node.

    ::::
