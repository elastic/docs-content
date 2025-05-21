---
navigation_title: Minimal security setup
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/security-minimal-setup.html
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---

% Scope: enable security, reset passwords and configure kibana to use authentication. Alternative approach to the automatic security configuration.
% Original title: Set up minimal security
# Minimal security setup [security-minimal-setup]

::::{important}
You only need to complete the following steps if you’re running an existing, unsecured cluster and want to enable the {{es}} {{security-features}}.
::::

In {{es}} 8.0 and later, security is [enabled automatically](./self-auto-setup.md) when you start {{es}} for the first time.

If you’re running an existing {{es}} cluster where security is disabled, you can manually enable the {{es}} {{security-features}} and then create passwords for [built-in users](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md). You can add more users later, but using the built-in users simplifies the process of enabling security for your cluster.

::::{important}
The minimal security scenario described in this document is not sufficient for [production mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode) clusters. If your cluster has multiple nodes, you must follow this guide, together with [configure Transport Layer Security (TLS)](./set-up-basic-security.md) between nodes.
::::


## Enable {{es}} security features [_enable_es_security_features]

Enabling the {{es}} security features provides basic authentication so that you can run a local cluster with username and password authentication.

1. On **every** node in your cluster, stop both {{kib}} and {{es}} if they are running.
2. On **every** node in your cluster, add the `xpack.security.enabled` setting to the `$ES_PATH_CONF/elasticsearch.yml` file and set the value to `true`:

    ```yaml
    xpack.security.enabled: true
    ```

    ::::{note}
    The `$ES_PATH_CONF` variable is the path for the {{es}} configuration files. If you installed {{es}} using archive distributions (`zip` or `tar.gz`), the variable defaults to `$ES_HOME/config`. If you used package distributions (Debian or RPM), the variable defaults to `/etc/elasticsearch`.
    ::::

3. If your cluster has a single node, add the `discovery.type` setting in the `$ES_PATH_CONF/elasticsearch.yml` file and set the value to `single-node`. This setting ensures that your node does not inadvertently connect to other clusters that might be running on your network.

    ```yaml
    discovery.type: single-node
    ```

## Set passwords for built-in users [security-create-builtin-users]

To communicate with your cluster, you must configure a password for the `elastic` and `kibana_system` [built-in users](/deploy-manage/users-roles/cluster-or-deployment-auth/built-in-users.md). Unless you enable anonymous access (not recommended), all requests that don’t include credentials are rejected.

1. On **every** node in your cluster, start {{es}}. For example, if you installed {{es}} with a `.tar.gz` package, run the following command from the `ES_HOME` directory:

    ```shell
    ./bin/elasticsearch
    ```

    ::::{note}
    If you are following this procedure for a multi-node cluster, you will have to set up [transport TLS certificates](./set-up-basic-security.md) in your nodes before being able to start the nodes.
    ::::

2. On any node in your cluster, open another terminal window and set the password for the `elastic` built-in user by running the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) utility. This command resets the password to an auto-generated value.

    ```shell
    ./bin/elasticsearch-reset-password -u elastic
    ```

    If you want to set the password to a specific value, run the command with the interactive (`-i`) parameter.

    ```shell
    ./bin/elasticsearch-reset-password -i -u elastic
    ```

3. Set the password for the `kibana_system` built-in user.

    ```shell
    ./bin/elasticsearch-reset-password -u kibana_system
    ```

4. Save the new passwords. In the next step, you’ll add the password for the `kibana_system` user to {{kib}}.

**Next**: [Configure {{kib}} to connect to {{es}} with a password](#add-built-in-users)


## Configure {{kib}} to connect to {{es}} with a password [add-built-in-users]

% Consider including a note here or updating the procedure to use newer auth methods like service tokens

When the {{es}} security features are enabled, users must log in to {{kib}} with a valid username and password.

You’ll configure {{kib}} to use the built-in `kibana_system` user and the password that you created earlier. {{kib}} performs some background tasks that require use of the `kibana_system` user.

This account is not meant for individual users and does not have permission to log in to {{kib}} from a browser. Instead, you’ll log in to {{kib}} as the `elastic` superuser.

1. Add the `elasticsearch.username` setting to the `KBN_PATH_CONF/kibana.yml` file and set the value to the `kibana_system` user:

    ```yaml
    elasticsearch.username: "kibana_system"
    ```

    ::::{note}
    The `KBN_PATH_CONF` variable is the path for the {{kib}} configuration files. If you installed {{kib}} using archive distributions (`zip` or `tar.gz`), the variable defaults to `KIB_HOME/config`. If you used package distributions (Debian or RPM), the variable defaults to `/etc/kibana`.
    ::::

2. From the directory where you installed {{kib}}, run the following commands to create the {{kib}} keystore and add the [secure settings](/deploy-manage/security/secure-settings.md):

    1. Create the {{kib}} keystore:

        ```shell
        ./bin/kibana-keystore create
        ```

    2. Add the password for the `kibana_system` user to the {{kib}} keystore:

        ```shell
        ./bin/kibana-keystore add elasticsearch.password
        ```

        When prompted, enter the password for the `kibana_system` user.

3. Restart {{kib}}. For example, if you installed {{kib}} with a `.tar.gz` package, run the following command from the {{kib}} directory:

    ```shell
    ./bin/kibana
    ```

4. Log in to {{kib}} as the `elastic` user. Use this superuser account to [manage spaces, create new users, and assign roles](../users-roles/cluster-or-deployment-auth/quickstart.md). If you’re running {{kib}} locally, go to `http://localhost:5601` to view the login page.


## What’s next? [minimal-security-whatsnext]

Congratulations! You enabled password protection for your local cluster to prevent unauthorized access. You can log in to {{kib}} as the `elastic` user and create additional users and roles, but take in mind that your browser connections and the traffic between {{kib}} and {{es}} will still be unencrypted with plain HTTP.

If your cluster has multiple nodes, then you must [configure Transport Layer Security (TLS) between nodes](./set-up-basic-security.md). [Production mode](../deploy/self-managed/bootstrap-checks.md#dev-vs-prod-mode) clusters will not start if you do not enable TLS.

Regardless of your cluster being a [single-node](../deploy/self-managed/bootstrap-checks.md#single-node-discovery) or a multi-node cluster, it's highly recommended to [secure the HTTP layer](./set-up-basic-security-plus-https.md) with TLS certificates.
