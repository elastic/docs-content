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

:::{note}
In {{es}} RPM and Debian package installations, the `elastic` user password is not output at startup and must be [manually reset](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-sm.md#using-elasticsearch-reset-password).
:::

To learn how to start {{es}} and {{kib}} with security enabled, follow one of our installation guides. Select the product that you want to install, and then select the guide your preferred installation method: 

* [Install {{es}}](/deploy-manage/deploy/self-managed/installing-elasticsearch.md#installation-methods)
* [Install {{kib}}](/deploy-manage/deploy/self-managed/install-kibana.md#install)

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
