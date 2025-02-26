---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/configure-operator-privileges.html
applies_to:
  deployment:
    ess: 
    ece: 
    eck: 
---

# Configure operator privileges [configure-operator-privileges]

::::{admonition} Indirect use only
This feature is designed for indirect use by {{ech}}, {{ece}}, and {{eck}}. Direct use is not supported.
::::

Before you can use operator privileges, you must [enable the feature](#enable-operator-privileges) on all nodes in the cluster and [designate operator users](#designate-operator-users).

## Enable operator privileges [enable-operator-privileges]

In order to use the operator privileges feature, it must be enabled explicitly on each node in the cluster. Add the following setting in each `elasticsearch.yml` file:

```yaml
xpack.security.operator_privileges.enabled: true
```

If the node is already running before you make this change, you must restart the node for the feature to take effect.

::::{warning} 
The feature needs to be either enabled or disabled consistently across all nodes in a cluster. Otherwise, you can get inconsistent behaviour depending on which node first receives a request and which node executes it.
::::


When operator privileges are enabled on a cluster, [specific functionalities](operator-only-functionality.md) are restricted and can be executed only by users who have been explicitly designated as operator users. If a regular user attempts to execute these functionalities (even if they have the `superuser` role), a security exception occurs.


## Designate operator users [designate-operator-users]

Operator users are just normal {{es}} users with special rights to perform operator-only functionalities. They are specified in an `operator_users.yml` file, which is located in the config directory (as defined by the `ES_PATH_CONF` environment variable). Similar to [other security config files](file-based.md#file-realm-configuration), the `operator_users.yml` file is local to a node and does not apply globally to the cluster. This means, in most cases, the same file should be distributed or copied to all nodes in a cluster.

The `operator_users.yml` file defines a set of criteria that an authenticating user must match to be considered as an operator user. The following snippet shows an example of such a file:

```yaml
operator: <1>
  - usernames: ["system_agent_1","system_agent_2"] <2>
    realm_type: "file" <3>
    auth_type: "realm" <4>
```

1. A fixed value of `operator` signals the beginning of the definition.
2. A list of user names allowed for operator users. This field is mandatory.
3. The type of the authenticating realm allowed for operator users. The default and only acceptable value is [`file`](file-based.md).
4. The authentication type allowed for operator users. The default and only acceptable value is `realm`.


You must specify at least the `usernames` field. If no other fields are specified, their default values are used. All fields must be matched for a user to be qualified as an operator user. You can also specify multiple groups of criteria. This is currently not very useful since this feature does not yet support other realms or authentication types.

There are also two implicit rules that affect which users are operator users:

1. If the authenticating user [runs as](submitting-requests-on-behalf-of-other-users.md) another user, neither of them are considered to be operator users.
2. All [Internal users](internal-users.md) are implicitly operator users.

::::{important} 
After a user is designated as an operator user, they are still subject to regular [RBAC user authorization](user-roles.md) checks. That is to say, in addition to specifying that a user is an operator user, you must also grant them the necessary {{es}} roles to perform their tasks. Consequently, it is entirely possible that an operator user can encounter an "access denied" error and fail to perform certain actions due to RBAC check failures. In short, an operator user is **not** automatically a `superuser`.
::::



