---
applies_to:
  deployment:
    self: ga
mapped_urls:
  - https://www.elastic.co/guide/en/kibana/current/using-kibana-with-security.html
  - https://www.elastic.co/guide/en/kibana/current/Security-production-considerations.html
---

% Kibana security had 2 original docs:
% https://www.elastic.co/guide/en/kibana/current/using-kibana-with-security.html
% https://www.elastic.co/guide/en/kibana/current/Security-production-considerations.html

# Configure security in {{kib}} [using-kibana-with-security]

For more information on granting access to {{kib}}, see [](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md).

::::{note}
When a user is not authorized to view data in an index (such as an {{es}} index), the entire index will be inaccessible and not display in {{kib}}.
::::

## Configure encryption keys [security-configure-settings]

Set an encryption key so that sessions are not invalidated. You can optionally configure additional security settings and authentication.

1. Set the `xpack.security.encryptionKey` property in the `kibana.yml` configuration file. You can use any text string that is 32 characters or longer as the encryption key. Refer to [`xpack.security.encryptionKey`](kibana://reference/configuration-reference/security-settings.md#xpack-security-encryptionkey).

    ```yaml
    xpack.security.encryptionKey: "something_at_least_32_characters"
    ```

    {{kib}}'s reporting and saved objects features also have encryption key settings. Refer to [`xpack.reporting.encryptionKey`](kibana://reference/configuration-reference/reporting-settings.md#xpack-reporting-encryptionkey) and [`xpack.encryptedSavedObjects.encryptionKey`](kibana://reference/configuration-reference/security-settings.md#xpack-encryptedsavedobjects-encryptionkey) respectively.

2. Optional: [Configure {{kib}}'s session expiration settings](/deploy-manage/security/kibana-session-management.md).
3. Optional: [Configure {{kib}} to authenticate to {{es}} with a client certificate (mutual authentication)](/deploy-manage/security/kibana-es-mutual-tls.md).
4. Restart {{kib}}.

## Additional Kibana security configurations [Security-production-considerations]

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

