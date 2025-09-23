---
navigation_title: Built-in users
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/built-in-users.html
applies_to:
  deployment:
    self:
products:
  - id: elasticsearch
---

# Built-in users in self-managed clusters [built-in-users]

The {{stack-security-features}} provide built-in user credentials to help you get up and running. These users have a fixed set of privileges and cannot be authenticated until their passwords have been set. The `elastic` user can be used to [set all of the built-in user passwords](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md#set-built-in-user-passwords).

In orchestrated deployments (ECH, ECE, and ECK), the `elastic` user is managed by the platform, while other default users are not accessible to end users. To learn how to reset the `elastic` user in an {{ech}}, {{ece}}, or {{eck}} environment, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/orchestrator-managed-users-overview.md).

::::{admonition} Create users with minimum privileges
The built-in users serve specific purposes and are not intended for general use. In particular, do not use the `elastic` superuser unless full access to the cluster is absolutely required. On self-managed deployments, use the `elastic` user to create users that have the minimum necessary roles or privileges for their activities.
::::

::::{note}
On {{ecloud}}, [operator privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/operator-privileges.md) are enabled. These privileges restrict some infrastructure functionality, even if a role would otherwise permit a user to complete an administrative task.
::::

## Built-in users

The following built-in users are available:

`elastic`
:   A built-in [superuser](elasticsearch://reference/elasticsearch/roles.md#built-in-roles-superuser).

    Anyone who can log in as the `elastic` user has direct read-only access to restricted indices, such as `.security`. This user also has the ability to manage security and create roles with unlimited privileges.

`kibana_system`
:   The user {{kib}} uses to connect and communicate with {{es}}.

`logstash_system`
:   The user Logstash uses when storing monitoring information in {{es}}.

`beats_system`
:   The user the Beats use when storing monitoring information in {{es}}.

`apm_system`
:   The user the APM server uses when storing monitoring information in {{es}}.

`remote_monitoring_user`
:   The user {{metricbeat}} uses when collecting and storing monitoring information in {{es}}. It has the `remote_monitoring_agent` and `remote_monitoring_collector` built-in roles.


## How the built-in users work [built-in-user-explanation]

These built-in users are stored in a special `.security` index, which is managed by {{es}}. If a built-in user is disabled or its password changes, the change is automatically reflected on each node in the cluster. If your `.security` index is deleted or restored from a snapshot, however, any changes you have applied are lost.

Although they share the same API, the built-in users are separate and distinct from users managed by the [native realm](/deploy-manage/users-roles/cluster-or-deployment-auth/native.md). Disabling the native realm will not have any effect on the built-in users. The built-in users can be disabled individually, using the [disable users API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-disable-user).


## The Elastic bootstrap password [bootstrap-elastic-passwords]
```{{applies_to}}
deployment:
  self:
```

```{{tip}}
{{ech}}, {{ece}}, and {{eck}} manage the `elastic` user differently. [Learn more](/deploy-manage/users-roles/cluster-or-deployment-auth/orchestrator-managed-users-overview.md).
```

When you install {{es}}, if the `elastic` user does not already have a password, it uses a default bootstrap password. The bootstrap password is a transient password that enables you to run the tools that set all the built-in user passwords.

By default, the bootstrap password is derived from a randomized `keystore.seed` setting, which is added to the keystore during installation. You do not need to know or change this bootstrap password. If you have defined a `bootstrap.password` setting in the keystore, however, that value is used instead. For more information about interacting with the keystore, see [Secure settings](/deploy-manage/security/secure-settings.md).

::::{note}
After you [set passwords for the built-in users](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md#set-built-in-user-passwords), in particular for the `elastic` user, there is no further use for the bootstrap password.
::::

## Setting initial built-in user passwords [set-built-in-user-passwords]
```{{applies_to}}
deployment:
  self:
```

You must set the passwords for all built-in users. You can set or reset passwords using several methods.

* Using `elasticsearch-setup-passwords`
* Using {{kib}} user management
* Using the change password API

If you want to reset built-in user passwords after initial setup, refer to [Set passwords for native and built-in users in self-managed clusters](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-sm.md).

```{{tip}}
{{ech}}, {{ece}}, and {{eck}} manage the `elastic` user differently. [Learn more](/deploy-manage/users-roles/cluster-or-deployment-auth/orchestrator-managed-users-overview.md).
```

### Using `elasticsearch-setup-passwords`

The `elasticsearch-setup-passwords` tool is the simplest method to set the built-in users' passwords for the first time. It uses the `elastic` user’s bootstrap password to run user management API requests. For example, you can run the command in an "interactive" mode, which prompts you to enter new passwords for the `elastic`, `kibana_system`, `logstash_system`, `beats_system`, `apm_system`, and `remote_monitoring_user` users:

```shell
bin/elasticsearch-setup-passwords interactive
```

For more information about the command options, see [elasticsearch-setup-passwords](elasticsearch://reference/elasticsearch/command-line-tools/setup-passwords.md).

::::{important}
After you set a password for the `elastic` user, the bootstrap password is no longer valid; you cannot run the `elasticsearch-setup-passwords` command a second time.
::::

### Using {{kib}} user management or the change password API

You can set the initial passwords for the built-in users by using the **Management > Users** page in {{kib}} or the [change password API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-change-password).

To use these methods, you must supply the `elastic` user and its bootstrap password to log in to {{kib}} or run the API. This requirement means that you can't use the default bootstrap password that is derived from the `keystore.seed` setting. Instead, you must explicitly set a `bootstrap.password` setting in the keystore before you start {{es}}. For example, the following command prompts you to enter a new bootstrap password:

```shell
bin/elasticsearch-keystore add "bootstrap.password"
```

You can then start {{es}} and {{kib}} and use the `elastic` user and bootstrap password to log in to {{kib}} and change the passwords.

### Using the Change Password API

Alternatively, you can submit Change Password API requests for each built-in user. These methods are better suited for changing your passwords after the initial setup is complete, since at that point the bootstrap password is no longer required.

## Adding built-in user passwords to {{kib}} [add-built-in-user-kibana]

After the `kibana_system` user password is set, you need to update the {{kib}} server with the new password by setting `elasticsearch.password` in the [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file:

```yaml
elasticsearch.password: kibanapassword
```

See [Configuring security in {{kib}}](/deploy-manage/security.md).


## Adding built-in user passwords to {{ls}} [add-built-in-user-logstash]

The `logstash_system` user is used internally within Logstash when monitoring is enabled for Logstash.

To enable this feature in Logstash, you need to update the Logstash configuration with the new password by setting `xpack.monitoring.elasticsearch.password` in the `logstash.yml` configuration file:

```yaml
xpack.monitoring.elasticsearch.password: logstashpassword
```

If you have upgraded from an older version of {{es}}, the `logstash_system` user may have defaulted to *disabled* for security reasons. Once the password has been changed, you can enable the user via the following API call:

```console
PUT _security/user/logstash_system/_enable
```

See [Configuring credentials for {{ls}} monitoring](logstash://reference/secure-connection.md#ls-monitoring-user).


## Adding built-in user passwords to Beats [add-built-in-user-beats]

The `beats_system` user is used internally within Beats when monitoring is enabled for Beats.

To enable this feature in Beats, you need to update the configuration for each of your beats to reference the correct username and password. For example:

```yaml
xpack.monitoring.elasticsearch.username: beats_system
xpack.monitoring.elasticsearch.password: beatspassword
```

For example, see [Monitoring {{metricbeat}}](beats://reference/metricbeat/monitoring.md).

The `remote_monitoring_user` is used when {{metricbeat}} collects and stores monitoring data for the {{stack}}. See [*Monitoring in a production environment*](/deploy-manage/monitor/stack-monitoring/elasticsearch-monitoring-self-managed.md).

If you have upgraded from an older version of {{es}}, then you may not have set a password for the `beats_system` or `remote_monitoring_user` users. If this is the case, then you should use the **Management > Users** page in {{kib}} or the [change password API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-change-password) to set a password for these users.


## Adding built-in user passwords to APM [add-built-in-user-apm]

The `apm_system` user is used internally within APM when monitoring is enabled.

To enable this feature in APM, you need to update the `apm-server.yml` configuration file to reference the correct username and password. For example:

```yaml
xpack.monitoring.elasticsearch.username: apm_system
xpack.monitoring.elasticsearch.password: apmserverpassword
```

If you have upgraded from an older version of {{es}}, then you may not have set a password for the `apm_system` user. If this is the case, then you should use the **Management > Users** page in {{kib}} or the [change password API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-change-password) to set a password for these users.


## Disabling default password functionality [disabling-default-password]

::::{important}
This setting is deprecated. The elastic user no longer has a default password. The password must be set before the user can be used. See [The Elastic bootstrap password](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md#bootstrap-elastic-passwords).

::::


