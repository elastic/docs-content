---
applies_to:
  deployment:
    self: ga
mapped_urls:
  - https://www.elastic.co/guide/en/kibana/current/using-kibana-with-security.html
---

$$$kibana-roles$$$

# Configure security in {{kib}} [using-kibana-with-security]

When you start {{es}} for the first time, {{stack-security-features}} are enabled on your cluster and TLS is configured automatically. The security configuration process generates a password for the `elastic` user and an enrollment token for {{kib}}. [Start the {{stack}} with security enabled](/deploy-manage/security/security-certificates-keys.md) and then enroll {{kib}} as part of the configuration process.

You can then log in to {{kib}} as the `elastic` user to create additional roles and users.

::::{note}
When a user is not authorized to view data in an index (such as an {{es}} index), the entire index will be inaccessible and not display in {{kib}}.
::::


## Configure security settings [security-configure-settings]

Set an encryption key so that sessions are not invalidated. You can optionally configure additional security settings and authentication.

1. Set the `xpack.security.encryptionKey` property in the `kibana.yml` configuration file. You can use any text string that is 32 characters or longer as the encryption key. Refer to [`xpack.security.encryptionKey`](kibana://reference/configuration-reference/security-settings.md#xpack-security-encryptionkey).

    ```yaml
    xpack.security.encryptionKey: "something_at_least_32_characters"
    ```

    {{kib}}'s reporting and saved objects features also have encryption key settings. Refer to [`xpack.reporting.encryptionKey`](kibana://reference/configuration-reference/reporting-settings.md#xpack-reporting-encryptionkey) and [`xpack.encryptedSavedObjects.encryptionKey`](kibana://reference/configuration-reference/security-settings.md#xpack-encryptedsavedobjects-encryptionkey) respectively.

2. Optional: [Configure {{kib}}'s session expiration settings](/deploy-manage/security/kibana-session-management.md).
3. Optional: [Configure {{kib}} to authenticate to {{es}} with a client certificate](/deploy-manage/security/secure-cluster-communications.md).
4. Restart {{kib}}.


## Create roles and users [security-create-roles]

Configure roles for your {{kib}} users to control what data those users can access.

1. Temporarily log in to {{kib}} using the built-in `elastic` superuser so you can create new users and assign roles. If you are running {{kib}} locally, go to `https://localhost:5601` to view the login page.

    ::::{note}
    The password for the built-in `elastic` user is generated as part of the security configuration process on {{es}}. If you need to reset the password for the `elastic` user or other built-in users, run the [`elasticsearch-reset-password`](elasticsearch://reference/elasticsearch/command-line-tools/reset-password.md) tool.
    ::::

2. $$$kibana-roles$$$Create roles and users to grant access to {{kib}}.

    To manage privileges in {{kib}}, go to the **Roles** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md). The built-in `kibana_admin` role will grant access to {{kib}} with administrator privileges. Alternatively, you can create additional roles that grant limited access to {{kib}}.

    If you’re using the default native realm with Basic Authentication, go to the **Users** management page using the navigation menu or the [global search field](/explore-analyze/find-and-organize/find-apps-and-objects.md) to create users and assign roles, or use the {{es}} [user management APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security). For example, the following creates a user named `jacknich` and assigns it the `kibana_admin` role:

    ```console
    POST /_security/user/jacknich
    {
      "password" : "t0pS3cr3t",
      "roles" : [ "kibana_admin" ]
    }
    ```

    ::::{tip}
    For more information on Basic Authentication and additional methods of authenticating {{kib}} users, see [Authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md).
    ::::

3. Grant users access to the indices that they will be working with in {{kib}}.

    ::::{tip}
    You can define as many different roles for your {{kib}} users as you need.
    ::::


    For example, create roles that have `read` and `view_index_metadata` privileges on specific data views. For more information, see [User authorization](/deploy-manage/users-roles/cluster-or-deployment-auth/user-roles.md).

4. Log out of {{kib}} and verify that you can log in as a normal user. If you are running {{kib}} locally, go to `https://localhost:5601` and enter the credentials for a user you’ve assigned a {{kib}} user role. For example, you could log in as the user `jacknich`.

    ::::{note}
    This must be a user who has been assigned [Kibana privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md). {{kib}} server credentials (the built-in `kibana_system` user) should only be used internally by the {{kib}} server.
    ::::

## Additional Kibana security configurations [Security-production-considerations]

To secure your {{kib}} installation in production, consider these high-priority topics to ensure that only authorized users can access {{kib}}.

### Enable SSL/TLS [enabling-ssl]

You should use SSL/TLS encryption to ensure that traffic between browsers and the {{kib}} server cannot be viewed or tampered with by third parties. See [encrypt HTTP client communications for {{kib}}](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-http).

### Enabling mutual TLS between {{kib}} and {{es}}

Refer to [](/deploy-manage/security/secure-http-communications.md#elasticsearch-mutual-tls) for information on how to enable mutual TLS between {{kib}} and {{es}}.

### Use {{stack}} {{security-features}} [configuring-kibana-shield]

You can use {{stack}} {{security-features}} to control what {{es}} data users can access through {{kib}}.

When {{security-features}} are enabled, {{kib}} users have to log in. They must have a role granting [{{kib}} privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) and access to the indices that they will be working with in {{kib}}.

If a user loads a {{kib}} dashboard that accesses data in an index that they are not authorized to view, they get an error that indicates the index does not exist.

For more information on granting access to {{kib}}, see [](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).


### Use secure HTTP headers [configuring-security-headers]

The {{kib}} server can instruct browsers to enable additional security controls using HTTP headers.

1. Enable HTTP Strict-Transport-Security.

    Use [`strictTransportSecurity`](https://www.elastic.co/guide/en/kibana/current/settings.html#server-securityResponseHeaders-strictTransportSecurity) to ensure that browsers will only attempt to access {{kib}} with SSL/TLS encryption. This is designed to prevent manipulator-in-the-middle attacks. To configure this with a lifetime of one year in your `kibana.yml`:

    ```js
    server.securityResponseHeaders.strictTransportSecurity: "max-age=31536000"
    ```

    ::::{warning}
    This header will block unencrypted connections for the entire domain. If you host more than one web application on the same domain using different ports or paths, all of them will be affected.
    ::::

2. Disable embedding.

    Use [`disableEmbedding`](https://www.elastic.co/guide/en/kibana/current/settings.html#server-securityResponseHeaders-disableEmbedding) to ensure that {{kib}} cannot be embedded in other websites. To configure this in your `kibana.yml`:

    ```js
    server.securityResponseHeaders.disableEmbedding: true
    ```

### Require a Content Security Policy [csp-strict-mode]

{{kib}} uses a Content Security Policy (CSP) to prevent the browser from allowing unsafe scripting, but older browsers will silently ignore this policy. If your organization does not need to support very old versions of our supported browsers, we recommend that you enable {{kib}}'s `strict` mode for the CSP. This will block access to {{kib}} for any browser that does not enforce even a rudimentary set of CSP protections.

To do this, set `csp.strict` to `true` in your `kibana.yml`:

```js
csp.strict: true
```

