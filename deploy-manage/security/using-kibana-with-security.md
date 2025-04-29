---
applies_to:
  deployment:
    self: ga
mapped_pages:
  - https://www.elastic.co/guide/en/kibana/current/using-kibana-with-security.html
  - https://www.elastic.co/guide/en/kibana/current/Security-production-considerations.html
---

# Configure security in {{kib}} [using-kibana-with-security]

This document describes security settings you may need to configure in self-managed deployments of {{kib}}. These settings help secure access, manage connections, and ensure consistent behavior across multiple instances.

Additional {{kib}} security features that apply to all deployment types, such as session management, saved objects encryption, and audit logging, are covered in a separate section [at the end of this document](#additional-security-topics).

## Configure encryption keys [security-configure-settings]

Set an encryption key so that sessions are not invalidated. You can optionally configure additional security settings and authentication.

::::{important}
When {{kib}} traffic is balanced across multiple instances connected to the same deployment, it is critical to configure these settings with identical values across all instances. Refer to [](/deploy-manage/production-guidance/kibana-load-balance-traffic.md) for more information.
::::

1. Set the `xpack.security.encryptionKey` property in the [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file. You can use any text string that is 32 characters or longer as the encryption key. Refer to [`xpack.security.encryptionKey`](kibana://reference/configuration-reference/security-settings.md#xpack-security-encryptionkey).

    ```yaml
    xpack.security.encryptionKey: "something_at_least_32_characters"
    ```

    {{kib}}'s reporting and saved objects features also have encryption key settings. Refer to [`xpack.reporting.encryptionKey`](kibana://reference/configuration-reference/reporting-settings.md#xpack-reporting-encryptionkey) and [`xpack.encryptedSavedObjects.encryptionKey`](kibana://reference/configuration-reference/security-settings.md#xpack-encryptedsavedobjects-encryptionkey) respectively.

2. Optional: [Configure {{kib}}'s session expiration settings](/deploy-manage/security/kibana-session-management.md).
3. Restart {{kib}}.

## Use secure HTTP headers [configuring-security-headers]

The {{kib}} server can instruct browsers to enable additional security controls using HTTP headers.

1. Enable `HTTP Strict Transport Security (HSTS)`.

    Use [`strictTransportSecurity`](kibana://reference/configuration-reference/general-settings.md#server-securityresponseheaders-stricttransportsecurity) to ensure that browsers will only attempt to access [{{kib}} with SSL/TLS encryption](./set-up-basic-security-plus-https.md#encrypt-kibana-browser). This is designed to prevent manipulator-in-the-middle attacks. To configure this with a lifetime of one year in your [`kibana.yml`](/deploy-manage/stack-settings.md):

    ```js
    server.securityResponseHeaders.strictTransportSecurity: "max-age=31536000"
    ```

    ::::{warning}
    This header will block unencrypted connections for the entire domain. If you host more than one web application on the same domain using different ports or paths, all of them will be affected.
    ::::

2. Disable embedding.

    Use [`disableEmbedding`](kibana://reference/configuration-reference/general-settings.md#server-securityresponseheaders-disableembedding) to ensure that {{kib}} cannot be embedded in other websites. To configure this in your [`kibana.yml`](/deploy-manage/stack-settings.md):

    ```js
    server.securityResponseHeaders.disableEmbedding: true
    ```

## Require a Content Security Policy [csp-strict-mode]

{{kib}} uses a Content Security Policy (CSP) to prevent the browser from allowing unsafe scripting, but older browsers will silently ignore this policy. If your organization does not need to support very old versions of our supported browsers, we recommend that you enable {{kib}}'s `strict` mode for the CSP. This will block access to {{kib}} for any browser that does not enforce even a rudimentary set of CSP protections.

To do this, set `csp.strict` to `true` in your [`kibana.yml`](/deploy-manage/stack-settings.md):

```js
csp.strict: true
```

## Additional security topics [additional-security-topics]

For guidance on managing user access to {{kib}}, refer to [](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) and [](/deploy-manage/users-roles/cluster-or-deployment-auth.md).

For TLS encryption configuration, refer to [](./set-up-basic-security-plus-https.md#encrypt-kibana-browser).

The following {{kib}} security features are not covered in this document because they apply to all deployment types, not just self-managed ones. However, they’re also important to consider:

* [Session management](./kibana-session-management.md)
* [Saved objects encryption](./secure-saved-objects.md)
* [Secure settings](./secure-settings.md)
* [Security events audit logging](./logging-configuration/security-event-audit-logging.md)

For a complete overview of available security features, refer to [](./secure-your-cluster-deployment.md).
