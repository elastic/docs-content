---
navigation_title: "Security"
---

# Security production considerations [Security-production-considerations]


To secure your {{kib}} installation in production, consider these high-priority topics to ensure that only authorized users can access {{kib}}. For more information on {{kib}}'s security controls, see [Configure security](using-kibana-with-security.md).


## Enable SSL/TLS [enabling-ssl]

You should use SSL/TLS encryption to ensure that traffic between browsers and the {{kib}} server cannot be viewed or tampered with by third parties. See [encrypt HTTP client communications for {{kib}}](../../../deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-http).

encrypt-kibana-http


## Use {{stack}} {{security-features}} [configuring-kibana-shield]

You can use {{stack}} {{security-features}} to control what {{es}} data users can access through {{kib}}.

When {{security-features}} are enabled, {{kib}} users have to log in. They must have a role granting [{{kib}} privileges](../../../deploy-manage/users-roles/cluster-or-deployment-auth/kibana-privileges.md) and access to the indices that they will be working with in {{kib}}.

If a user loads a {{kib}} dashboard that accesses data in an index that they are not authorized to view, they get an error that indicates the index does not exist.

For more information on granting access to {{kib}}, see [Granting access to {{kib}}](xpack-security-authorization.md).


## Use secure HTTP headers [configuring-security-headers]

The {{kib}} server can instruct browsers to enable additional security controls using HTTP headers.

1. Enable HTTP Strict-Transport-Security.

    Use [`strictTransportSecurity`](../../../deploy-manage/deploy/self-managed/configure.md#server-securityResponseHeaders-strictTransportSecurity) to ensure that browsers will only attempt to access {{kib}} with SSL/TLS encryption. This is designed to prevent manipulator-in-the-middle attacks. To configure this with a lifetime of one year in your `kibana.yml`:

    ```js
    server.securityResponseHeaders.strictTransportSecurity: "max-age=31536000"
    ```

    ::::{warning}
    This header will block unencrypted connections for the entire domain. If you host more than one web application on the same domain using different ports or paths, all of them will be affected.
    ::::

2. Disable embedding.

    Use [`disableEmbedding`](https://www.elastic.co/guide/en/kibana/master/settings.html#server-securityResponseHeaders-disableEmbedding) to ensure that {{kib}} cannot be embedded in other websites. To configure this in your `kibana.yml`:

    ```js
    server.securityResponseHeaders.disableEmbedding: true
    ```



## Require a Content Security Policy [csp-strict-mode]

{{kib}} uses a Content Security Policy (CSP) to prevent the browser from allowing unsafe scripting, but older browsers will silently ignore this policy. If your organization does not need to support very old versions of our supported browsers, we recommend that you enable {{kib}}'s `strict` mode for the CSP. This will block access to {{kib}} for any browser that does not enforce even a rudimentary set of CSP protections.

To do this, set `csp.strict` to `true` in your `kibana.yml`:

```js
csp.strict: true
```

