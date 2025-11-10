---
navigation_title: "{{kib}} authentication"
applies_to:
  deployment:
    ess:
    ece:
    eck:
    self:
---

# Authentication in {{kib}} [kibana-authentication]

After you configure an authentication method in {{es}}, you can configure an authentication mechanism to log in to {{kib}}.

{{kib}} supports the following authentication mechanisms:

* [Multiple authentication providers](#multiple-authentication-providers)
* [Basic authentication](#basic-authentication)
* [Token authentication](#token-authentication)
* [Public key infrastructure (PKI) authentication](#pki-authentication)
* [SAML single sign-on](#saml)
* [OpenID Connect single sign-on](#oidc)
* [Kerberos single sign-on](#kerberos)
* [Anonymous authentication](#anonymous-authentication)
* [HTTP authentication](#http-authentication)
* [Embedded content authentication](#embedded-content-authentication)

## Multiple authentication providers [multiple-authentication-providers]

Enable multiple authentication mechanisms at the same time by specifying a prioritized list of the authentication *providers* (typically of various types) in the configuration. Providers are consulted in ascending order. Make sure each configured provider has a unique name (e.g. `basic1` or `saml1` in the configuration example) and `order` setting. In the event that two or more providers have the same name or `order`, {{kib}} will fail to start.

When two or more providers are configured, you can choose the provider you want to use on the Login Selector UI. The order the providers appear is determined by the `order` setting. The appearance of the specific provider entry can be customized with the `description`, `hint`, and `icon` settings.

::::{tip}
To provide login instructions to users, use the `xpack.security.loginHelp` setting, which supports Markdown format. When you specify the `xpack.security.loginHelp` setting, the Login Selector UI displays a `Need help?` link that lets users access login help information.
::::


If you don’t want a specific provider to show up at the Login Selector UI (for example, if you only want to support third-party initiated login) you can hide it with `showInSelector` setting set to `false`. Or, if you only want to show a provider for a specific origin(s), you can use the `origin` setting. However, in both cases the provider is still part of the provider chain and may be used during authentication based on its order. To fully disable a provider, use the `enabled` setting.

::::{tip}
The Login Selector UI can also be disabled or enabled with `xpack.security.authc.selector.enabled` setting.
::::


Here is how your [`kibana.yml`](/deploy-manage/stack-settings.md) and Login Selector UI can look like if you deal with multiple authentication providers:

```yaml
xpack.security.loginHelp: "**Help** info with a [link](...)"
xpack.security.authc.providers:
  basic.basic1:
    order: 0
    icon: "logoElasticsearch"
    hint: "Typically for administrators"
  saml.saml1:
    order: 1
    realm: saml1
    description: "Log in with SSO"
    icon: "<my-company-url>/saml-logo.svg"
  saml.saml2:
    order: 2
    realm: saml2
    showInSelector: false
  kerberos.kerberos1:
    order: 3
    enabled: false
```

:::{image} /deploy-manage/images/kibana-kibana-login.png
:alt: Login Selector UI
:screenshot:
:::

For more information, refer to [authentication security settings](kibana://reference/configuration-reference/security-settings.md#authentication-security-settings).

::::{tip}
If you have multiple authentication providers configured, you can use the `auth_provider_hint` URL query parameter to create a deep link to any provider and bypass the Login Selector UI. Using the [`kibana.yml`](/deploy-manage/stack-settings.md) above as an example, you can add `?auth_provider_hint=basic1` to the login page URL, which will take you directly to the basic login page.
::::



## Basic authentication [basic-authentication]

To successfully log in to {{kib}}, basic authentication requires a username and password. Basic authentication is enabled by default, and is based on the [Native](native.md), [LDAP](ldap.md), or [Active Directory](active-directory.md) security realm that is provided by {{es}}. The basic authentication provider uses a {{kib}} provided login form, and supports authentication using the `Authorization` request header `Basic` scheme.

::::{note}
You can configure only one Basic provider per {{kib}} instance.
::::

## Token authentication [token-authentication]

Token authentication is a [subscription feature](https://www.elastic.co/subscriptions). This allows users to log in using the same {{kib}} provided login form as basic authentication, and is based on the [Native](native.md) or [LDAP](ldap.md) security realm that is provided by {{es}}. The token authentication provider is built on {{es}} token APIs.

Prior to configuring {{kib}}, ensure that token support is enabled in {{es}}. See the [{{es}} token API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-token) documentation for more information.

::::{note}
You can configure only one token provider per {{kib}} instance.
::::

To enable the token authentication provider in {{kib}}, set the following value in your [`kibana.yml`](/deploy-manage/stack-settings.md):

```yaml
xpack.security.authc.providers:
  token.token1:
    order: 0
```

Switching to the token authentication provider from the basic one will make {{kib}} to reject requests from applications like `curl` that usually use `Authorization` request header with the `Basic` scheme for authentication. If you still want to support such applications, you’ll have to either switch to using `Bearer` scheme with the tokens [created by {{es}} token API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-get-token), or add the `Basic` scheme to the list of supported schemes for the [HTTP authentication](#http-authentication).


## Public key infrastructure (PKI) authentication [pki-authentication]

::::{important}
PKI authentication will not work if {{kib}} is hosted behind a TLS termination reverse proxy. In this configuration, {{kib}} does not have direct access to the client certificates and cannot authenticate the user.

::::


PKI authentication is a [subscription feature](https://www.elastic.co/subscriptions). This allows users to log into {{kib}} using X.509 client certificates that must be presented while connecting to {{kib}}. The certificates must first be accepted for authentication on the {{kib}} TLS layer, and then they are further validated by an {{es}} PKI realm. The PKI authentication provider relies on the {{es}} [Delegate PKI authentication API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-delegate-pki) to exchange X.509 client certificates to access tokens. All subsequent requests to {{es}} APIs on behalf of users will be authenticated using these access tokens.

Prior to configuring {{kib}}, ensure that the PKI realm is enabled in {{es}} and configured to permit delegation. See [Configuring a PKI realm](/deploy-manage/users-roles/cluster-or-deployment-auth/pki.md) for more information.

To enable the PKI authentication provider in {{kib}}, you must first [configure {{kib}} to encrypt communications between the browser and {{kib}} server](/deploy-manage/security/set-up-basic-security-plus-https.md#encrypt-kibana-http). You must also enable TLS client authentication and include the certificate authority (CA) used to sign client certificates into a list of CAs trusted by {{kib}} in your [`kibana.yml`](/deploy-manage/stack-settings.md):

::::{note}
You can configure only one PKI provider per {{kib}} instance.
::::


```yaml
server.ssl.certificateAuthorities: /path/to/your/cacert.pem
server.ssl.clientAuthentication: required
xpack.security.authc.providers:
  pki.pki1:
    order: 0
```

If you're using {{ece}} or {{ech}}, then you must [upload this file as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) before it can be referenced. If you're using {{eck}}, then install the file as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret). If you're using a self-managed cluster, then the file must be present on each node.

::::{note}
Trusted CAs can also be specified in a PKCS #12 keystore bundled with your {{kib}} server certificate/key using `server.ssl.keystore.path` or in a separate trust store using `server.ssl.truststore.path`.
::::


You can also configure both PKI and basic authentication for the same {{kib}} instance:

```yaml
server.ssl.clientAuthentication: optional
xpack.security.authc.providers:
  pki.pki1:
    order: 0
  basic.basic1:
    order: 1
```

Note that with `server.ssl.clientAuthentication` set to `required`, users are asked to provide a valid client certificate, even if they want to authenticate with username and password. Depending on the security policies, it may or may not be desired. If not, `server.ssl.clientAuthentication` can be set to `optional`. In this case, {{kib}} still requests a client certificate, but the client won’t be required to present one. The `optional` client authentication mode might also be needed in other cases, for example, when PKI authentication is used in conjunction with Reporting.


## SAML single sign-on [saml]

SAML authentication is part of single sign-on (SSO), a [subscription feature](https://www.elastic.co/subscriptions). This allows users to log in to {{kib}} with an external Identity Provider, such as Okta or Auth0. Make sure that SAML is enabled and configured in {{es}} before setting it up in {{kib}}. See [Configuring SAML single sign-on on the {{stack}}](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md).

Enable SAML authentication by specifying which SAML realm in {{es}} should be used:

```yaml
xpack.security.authc.providers:
  saml.saml1:
    order: 0
    realm: saml1
```

You can log in to {{kib}} via SAML SSO by navigating directly to the {{kib}} URL. If you aren’t authenticated, you are redirected to the Identity Provider for login. Most Identity Providers maintain a long-lived session. If you log in to a different application using the same Identity Provider in the same browser, you are automatically authenticated. An exception is if {{es}} or the Identity Provider is configured to force you to re-authenticate. This login scenario is called *Service Provider initiated login*.

It’s also possible to configure multiple SAML authentication providers at the same time. In this case, you will need to choose which provider to use for login at the Login Selector UI:

```yaml
xpack.security.authc.providers:
  saml.saml1:
    order: 0
    realm: saml1
    description: "Log in with Elastic"
  saml.saml2:
    order: 1
    realm: saml2
    description: "Log in with Auth0"
```


#### SAML and basic authentication [_saml_and_basic_authentication]

You can also configure both SAML and basic authentication for the same {{kib}} instance. This might be the case for {{kib}} or {{es}} admins whose accounts aren’t linked to the SSO users database:

```yaml
xpack.security.authc.providers:
  saml.saml1:
    order: 0
    realm: saml1
    description: "Log in with Elastic"
  basic.basic1:
    order: 1
```

Basic authentication is supported *only* if the `basic` authentication provider is explicitly declared in `xpack.security.authc.providers` setting, in addition to `saml`.

To support basic authentication for the applications like `curl` or when the `Authorization: Basic base64(username:password)` HTTP header is included in the request (for example, by reverse proxy), add `Basic` scheme to the list of supported schemes for the [HTTP authentication](#http-authentication).


## OpenID Connect single sign-on [oidc]

OpenID Connect (OIDC) authentication is part of single sign-on (SSO), a [subscription feature](https://www.elastic.co/subscriptions). Similar to SAML, authentication with OIDC allows users to log in to {{kib}} using an OIDC Provider such as Google, or Okta. OIDC should also be configured in {{es}}. For more details, see [Configuring single sign-on to the {{stack}} using OpenID Connect](/deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md).

Enable OIDC authentication by specifying which OIDC realm in {{es}} to use:

```yaml
xpack.security.authc.providers:
  oidc.oidc1:
    order: 0
    realm: oidc1
```

To use third party initiated SSO, configure your OpenID Provider to use `/api/security/oidc/initiate_login` as `Initiate Login URI`.

It’s also possible to configure multiple OpenID Connect authentication providers at the same time. In this case, you need to choose which provider to use for login at the Login Selector UI:

```yaml
xpack.security.authc.providers:
  oidc.oidc1:
    order: 0
    realm: oidc1
    description: "Log in with Elastic"
  oidc.oidc2:
    order: 1
    realm: oidc2
    description: "Log in with Auth0"
```


#### OpenID Connect and basic authentication [_openid_connect_and_basic_authentication]

You can also configure both OpenID Connect and basic authentication for the same {{kib}} instance. This might be the case for {{kib}} or {{es}} admins whose accounts aren’t linked to the SSO users database:

```yaml
xpack.security.authc.providers:
  oidc.oidc1:
    order: 0
    realm: oidc1
    description: "Log in with Elastic"
  basic.basic1:
    order: 1
```

Basic authentication is supported *only* if the `basic` authentication provider is explicitly declared in `xpack.security.authc.providers` setting, in addition to `oidc`.

To support basic authentication for the applications like `curl` or when the `Authorization: Basic base64(username:password)` HTTP header is included in the request (for example, by reverse proxy), add `Basic` scheme to the list of supported schemes for the [HTTP authentication](#http-authentication).


### Single sign-on provider details [_single_sign_on_provider_details]

The following sections apply both to [SAML single sign-on](#saml) and [OpenID Connect single sign-on](#oidc).


#### Access and refresh tokens [_access_and_refresh_tokens]

Once the user logs in to {{kib}} with SSO, either using SAML or OpenID Connect, {{es}} issues access and refresh tokens that {{kib}} encrypts and stores as a part of its own session. This way, the user isn’t redirected to the Identity Provider for every request that requires authentication. It also means that the {{kib}} session depends on the [`xpack.security.session.idleTimeout` and `xpack.security.session.lifespan`](kibana://reference/configuration-reference/security-settings.md#security-session-and-cookie-settings) settings, and the user is automatically logged out if the session expires. An access token that is stored in the session can expire, in which case {{kib}} will automatically renew it with a one-time-use refresh token and store it in the same session.

{{kib}} can only determine if an access token has expired if it receives a request that requires authentication. If both access and refresh tokens have already expired (for example, after 24 hours of inactivity), {{kib}} initiates a new "handshake" and redirects the user to the external authentication provider (SAML Identity Provider or OpenID Connect Provider) Depending on {{es}} and the external authentication provider configuration, the user might be asked to re-enter credentials.

If {{kib}} can’t redirect the user to the external authentication provider (for example, for AJAX/XHR requests), an error indicates that both access and refresh tokens are expired. Reloading the current {{kib}} page fixes the error.


#### Local and global logout [_local_and_global_logout]

During logout, both the {{kib}} session and {{es}} access/refresh token pair are invalidated. This is known as "local" logout.

{{kib}} can also initiate a "global" logout or *Single Logout* if it’s supported by the external authentication provider and not explicitly disabled by {{es}}. In this case, the user is redirected to the external authentication provider for log out of all applications associated with the active provider session.


## Kerberos single sign-on [kerberos]

Kerberos authentication is part of single sign-on (SSO), a [subscription feature](https://www.elastic.co/subscriptions). Make sure that Kerberos is enabled and configured in {{es}} before setting it up in {{kib}}. See [Kerberos authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kerberos.md).

Next, to enable Kerberos in {{kib}}, you will need to enable the Kerberos authentication provider in the [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file, as follows:

::::{note}
You can configure only one Kerberos provider per {{kib}} instance.
::::


```yaml
xpack.security.authc.providers:
  kerberos.kerberos1:
    order: 0
```

You may want to be able to authenticate with the basic authentication provider as a secondary mechanism or while you are setting up Kerberos for the stack:

```yaml
xpack.security.authc.providers:
  kerberos.kerberos1:
    order: 0
    description: "Log in with Kerberos"
  basic.basic1:
    order: 1
```

::::{important}
{{kib}} uses SPNEGO, which wraps the Kerberos protocol for use with HTTP, extending it to web applications. At the end of the Kerberos handshake, {{kib}} forwards the service ticket to {{es}}, then {{es}} unpacks the service ticket and responds with an access and refresh token, which are used for subsequent authentication. On every {{es}} node that {{kib}} connects to, the keytab file should always contain the HTTP service principal for the {{kib}} host. The HTTP service principal name must have the `HTTP/kibana.domain.local@KIBANA.DOMAIN.LOCAL` format.
::::


## Anonymous authentication [anonymous-authentication]

::::{important}
Anyone with access to the network {{kib}} is exposed to will be able to access {{kib}}. Make sure that you’ve properly restricted the capabilities of the anonymous service account so that anonymous users can’t perform destructive actions or escalate their own privileges.

::::


Anonymous authentication gives users access to {{kib}} without requiring them to provide credentials. This can be useful if you want your users to skip the login step when you embed dashboards in another application or set up a demo {{kib}} instance in your internal network, while still keeping other security features intact.

To enable anonymous authentication in {{kib}}, you must specify the credentials the anonymous service account {{kib}} should use internally to authenticate anonymous requests.

::::{note}
You can configure only one anonymous authentication provider per {{kib}} instance.
::::


You must have a user account that can authenticate to {{es}} using a username and password, for instance from the [Native](native.md) or [LDAP](ldap.md) security realms, so that you can use these credentials to impersonate the anonymous users. Here is how your [`kibana.yml`](/deploy-manage/stack-settings.md) might look:

```yaml
xpack.security.authc.providers:
  anonymous.anonymous1:
    order: 0
    credentials:
      username: "anonymous_service_account"
      password: "anonymous_service_account_password"
```


#### Anonymous access and other types of authentication [_anonymous_access_and_other_types_of_authentication]

You can configure more authentication providers in addition to anonymous access in {{kib}}. In this case, the Login Selector presents a configurable **Continue as Guest** option for anonymous access:

```yaml
xpack.security.authc.providers:
  basic.basic1:
    order: 0
  anonymous.anonymous1:
    order: 1
    credentials:
      username: "anonymous_service_account"
      password: "anonymous_service_account_password"
```


#### Anonymous access and embedding [anonymous-access-and-embedding]

One of the most popular use cases for anonymous access is when you embed {{kib}} into other applications and don’t want to force your users to log in to view it. If you configured {{kib}} to use anonymous access as the sole authentication mechanism, you don’t need to do anything special while embedding {{kib}}.

For information on how to embed, refer to [Embed {{kib}} content in a web page](/explore-analyze/report-and-share.md#embed-code).


#### Anonymous access session [anonymous-access-session]

{{kib}} maintains a separate [session](/deploy-manage/security/kibana-session-management.md) for every anonymous user, as it does for all other authentication mechanisms.

You can configure [session idle timeout](/deploy-manage/security/kibana-session-management.md#session-idle-timeout) and [session lifespan](/deploy-manage/security/kibana-session-management.md#session-lifespan) for anonymous sessions the same as you do for any other session with the exception that idle timeout is explicitly disabled for anonymous sessions by default. The global [`xpack.security.session.idleTimeout`](kibana://reference/configuration-reference/security-settings.md#security-session-and-cookie-settings) setting doesn’t affect anonymous sessions. To change the idle timeout for anonymous sessions, you must configure the provider-level [`xpack.security.authc.providers.anonymous.<provider-name>.session.idleTimeout`](kibana://reference/configuration-reference/security-settings.md#anonymous-authentication-provider-settings) setting.


## HTTP authentication [http-authentication]

::::{important}
Be very careful when you modify HTTP authentication settings as it may indirectly affect other important {{kib}} features that implicitly rely on HTTP authentication (e.g. Reporting).

::::


HTTP protocol provides a simple authentication framework that can be used by a client to provide authentication information. It uses a case-insensitive token as a means to identify the authentication scheme, followed by additional information necessary for achieving authentication via that scheme.

This type of authentication is usually useful for machine-to-machine interaction that requires authentication and where human intervention is not desired or just infeasible. There are a number of use cases when HTTP authentication support comes in handy for {{kib}} users as well.

::::{important}
API keys are intended for programmatic access to {{kib}} and {{es}}. Do not use API keys to authenticate access via a web browser.

::::


By default {{kib}} supports [`ApiKey`](/deploy-manage/api-keys/elasticsearch-api-keys.md) authentication scheme *and* any scheme supported by the currently enabled authentication provider. For example, `Basic` authentication scheme is automatically supported when basic authentication provider is enabled, or `Bearer` scheme when any of the token based authentication providers is enabled (Token, SAML, OpenID Connect, PKI or Kerberos). But it’s also possible to add support for any other authentication scheme in the [`kibana.yml`](/deploy-manage/stack-settings.md) configuration file, as follows:

::::{note}
Don’t forget to explicitly specify the default `apikey` and `bearer` schemes when you just want to add a new one to the list.
::::


```yaml
xpack.security.authc.http.schemes: [apikey, bearer, basic, something-custom]
```

With this configuration, you can send requests to {{kib}} with the `Authorization` header using `ApiKey`, `Bearer`, `Basic` or `Something-Custom` HTTP schemes (case insensitive). Under the hood, {{kib}} relays this header to {{es}}, then {{es}} authenticates the request using the credentials in the header.


### Embedded content authentication [embedded-content-authentication]

Once you create a dashboard or a visualization, you might want to share it with your colleagues or friends. The easiest way to do this is to share a direct link to your dashboard or visualization. However, some users might not have access to your {{kib}}. With the {{kib}} embedding functionality, you can display the content you created in {{kib}} to an internal company website or a personal web page.

$$$embedding-cookies$$$
To minimize security risk, embedding with iframes requires careful consideration. By default, modern web browsers enforce the [same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) to restrict the behavior of framed pages. When {{stack-security-features}} are enabled on your cluster, make sure the browsers can transmit session cookies to a {{kib}} server. The setting you need to be aware of is [`xpack.security.sameSiteCookies`](kibana://reference/configuration-reference/security-settings.md#xpack-security-samesitecookies). To support modern browsers, you must set it to `None`:

```yaml
xpack.security.sameSiteCookies: "None"
```

For more information about possible values and implications, refer to [xpack.security.sameSiteCookies](kibana://reference/configuration-reference/security-settings.md#xpack-security-samesitecookies). For more information about iframe and cookies, refer to [iframe](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/iframe) and [SameSite cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite).

If you’re embedding {{kib}} in a website that supports single sign-on (SSO) with SAML, OpenID Connect, Kerberos, or PKI, it’s highly advisable to configure {{kib}} as a part of the SSO setup. Operating in a single and properly configured security domain provides you with the most secure and seamless user experience.

If you have multiple authentication providers enabled, and you want to automatically log in anonymous users when embedding anything other than dashboards and visualizations, then you will need to add the `auth_provider_hint=<anonymous-provider-name>` query string parameter to the {{kib}} URL that you’re embedding.

For example, if you craft the iframe code to embed {{kib}}, it might look like this:

```html
<iframe src="https://localhost:5601/app/monitoring#/elasticsearch/nodes?embed=true&_g=(....)" height="600" width="800"></iframe>
```

To make this iframe leverage anonymous access automatically, you will need to modify a link to {{kib}} in the `src` iframe attribute to look like this:

```html
<iframe src="https://localhost:5601/app/monitoring?auth_provider_hint=anonymous1#/elasticsearch/nodes?embed=true&_g=(....)" height="600" width="800"></iframe>
```

::::{note}
`auth_provider_hint` query string parameter goes **before** the hash URL fragment.
::::


For more information, refer to [Embed code](../../../explore-analyze/report-and-share.md#embed-code).