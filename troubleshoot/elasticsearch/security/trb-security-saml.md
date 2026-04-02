---
navigation_title: SAML
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/trb-security-saml.html
applies_to:
  stack:
products:
  - id: elasticsearch
---

# Common SAML issues [trb-security-saml]

Some of the common SAML problems are shown below with tips on how to resolve these issues.

:::{note}
This topic describes troubleshooting SAML SSO at the deployment or cluster level, for the purposes of authenticating with a {{kib}} instance. To learn about SAML SSO, for your organization or orchestrator, refer to the following topics:
* [Elastic Cloud SAML SSO](/deploy-manage/users-roles/cloud-organization/configure-saml-authentication.md)
* [{{ece}} SAML](/deploy-manage/users-roles/cloud-enterprise-orchestrator/saml.md) and [SSO](/deploy-manage/users-roles/cloud-enterprise-orchestrator/configure-sso-for-deployments.md)
:::

1. **Symptoms:**

    Authentication in {{kib}} fails and the following error is printed in the {{es}} logs:

    ```
    Cannot find any matching realm for [SamlPrepareAuthenticationRequest{realmName=saml1,
    assertionConsumerServiceURL=https://my.kibana.url/api/security/saml/callback}]
    ```
    **Resolution:**

    In order to initiate a SAML authentication, {{kib}} needs to know which SAML realm it should use from the ones that are configured in {{es}}. You can use the `xpack.security.authc.providers.saml.<provider-name>.realm` setting to explicitly set the SAML realm name in {{kib}}. It must match the name of the SAML realm that is configured in {{es}}.

    If you get an error like the one above, it possibly means that the value of `xpack.security.authc.providers.saml.<provider-name>.realm` in your {{kib}} configuration is wrong. Verify that it matches the name of the configured realm in {{es}}, which is the string after `xpack.security.authc.realms.saml.` in your {{es}} configuration.

2. **Symptoms:**

    Authentication in {{kib}} fails and the following error is printed in the {{es}} logs:

    ```
    Authentication to realm saml1 failed - Provided SAML response is not valid for realm
    saml/saml1 (Caused by ElasticsearchSecurityException[Conditions
    [https://5aadb9778c594cc3aad0efc126a0f92e.kibana.company....ple.com/]
    do not match required audience
    [https://5aadb9778c594cc3aad0efc126a0f92e.kibana.company.example.com]])
    ```
    **Resolution:**

    We received a SAML response that is addressed to another SAML Service Provider. This usually means that the configured SAML Service Provider Entity ID in [`elasticsearch.yml`](/deploy-manage/stack-settings.md) (`sp.entity_id`) does not match what has been configured as the SAML Service Provider Entity ID in the SAML Identity Provider documentation.

    To resolve this issue, ensure that both the saml realm in {{es}} and the IdP are configured with the same string for the SAML Entity ID of the Service Provider.

    In the {{es}} log, just before the exception message (above), there will also be one or more `INFO` level messages of the form

    ```
    Audience restriction
    [https://5aadb9778c594cc3aad0efc126a0f92e.kibana.company.example.com/]
    does not match required audience
    [https://5aadb9778c594cc3aad0efc126a0f92e.kibana.company.example.com]
    (difference starts at character [#68] [/] vs [])
    ```
    This log message can assist in determining the difference between the value that was received from the IdP and the value at has been configured in {{es}}. The text in parentheses that describes the difference between the two audience identifiers will only be shown if the two strings are considered to be similar.

    ::::{tip}
    These strings are compared as case-sensitive strings and not as canonicalized URLs even when the values are URL-like. Be mindful of trailing slashes, port numbers, etc.
    ::::

3. **Symptoms:**

    Authentication in {{kib}} fails and the following error is printed in the {{es}} logs:

    ```
    Cannot find metadata for entity [your:entity.id] in [metadata.xml]
    ```
    **Resolution:**

    We could not find the metadata for the SAML Entity ID `your:entity.id` in the configured metadata file (`metadata.xml`).

    1. Ensure that the `metadata.xml` file you are using is indeed the one provided by your SAML Identity Provider.
    2. Ensure that the `metadata.xml` file contains one <EntityDescriptor> element as follows: `<EntityDescriptor ID="0597c9aa-e69b-46e7-a1c6-636c7b8a8070" entityID="https://saml.example.com/f174199a-a96e-4201-88f1-0d57a610c522/" ...` where the value of the `entityID` attribute is the same as the value of the `idp.entity_id` that you have set in your SAML realm configuration in [`elasticsearch.yml`](/deploy-manage/stack-settings.md).
    3. Note that these are also compared as case-sensitive strings and not as canonicalized URLs even when the values are URL-like.

4. **Symptoms:**

    Authentication in {{kib}} fails and the following error is printed in the {{es}} logs:

    ```
    unable to authenticate user [<unauthenticated-saml-user>]
    for action [cluster:admin/xpack/security/saml/authenticate]
    ```
    **Resolution:**

    This error indicates that {{es}} failed to process the incoming SAML authentication message. Since the message can’t be processed, {{es}} is not aware of who the to-be authenticated user is and the `<unauthenticated-saml-user>` placeholder is used instead. To diagnose the *actual* problem, you must check the {{es}} logs for further details.

5. **Symptoms:**

    Authentication in {{kib}} fails and the following error is printed in the {{es}} logs:

    ```
    Authentication to realm <saml-realm-name> failed - SAML Attribute [<AttributeName0>] for
    [xpack.security.authc.realms.saml.<saml-realm-name>.attributes.principal] not found in saml attributes
    [<AttributeName1>=<AttributeValue1>, <AttributeName2>=<AttributeValue2>, ...] or NameID [ NameID(format)=value ]
    ```
    **Resolution:**

    This error indicates that {{es}} failed to find the necessary SAML attribute in the SAML response that the Identity Provider sent. In this example, {{es}} is configured as follows:

    ```
    xpack.security.authc.realms.saml.<saml-realm-name>.attributes.principal: AttributeName0
    ```
    This configuration means that {{es}} expects to find a SAML Attribute with the name `AttributeName0` or a `NameID` with the appropriate format in the SAML response so that [it can map it](../../../deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-attributes-mapping) to the `principal` user property. The `principal` user property is a mandatory one, so if this mapping can’t happen, the authentication fails.

    If you are attempting to map a `NameID`, make sure that the expected `NameID` format matches the one that is sent. See [Special attribute names](../../../deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-attribute-mapping-nameid) for more details.

    If you are attempting to map a SAML attribute and it is not part of the list in the error message, it might mean that you have misspelled the attribute name, or that the IdP is not sending this particular attribute. You might be able to use another attribute from the list to map to `principal` or consult with your IdP administrator to determine if the required attribute can be sent.

6. **Symptoms:**

    Authentication in {{kib}} fails and the following error is printed in the {{es}} logs:

    ```
    Cannot find [{urn:oasis:names:tc:SAML:2.0:metadata}IDPSSODescriptor]/[urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect] in descriptor
    ```
    **Resolution:**

    This error indicates that the SAML metadata for your Identity Provider do not contain a `<SingleSignOnService>` endpoint with binding of HTTP-Redirect (urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect). {{es}} supports only the `HTTP-Redirect` binding for SAML authentication requests (and it doesn’t support the `HTTP-POST` binding). Consult your IdP administrator in order to enable at least one `<SingleSignOnService>` supporting `HTTP-Redirect` binding and update your IdP SAML Metadata.

7. **Symptoms:**

    Authentication in {{kib}} fails and the following error is printed in the {{es}} logs:

    ```
    Authentication to realm my-saml-realm failed -
    Provided SAML response is not valid for realm saml/my-saml-realm
    (Caused by ElasticsearchSecurityException[SAML Response is not a 'success' response:
     The SAML IdP did not grant the request. It indicated that the Elastic Stack side sent
     something invalid (urn:oasis:names:tc:SAML:2.0:status:Requester). Specific status code which might
     indicate what the issue is: [urn:oasis:names:tc:SAML:2.0:status:InvalidNameIDPolicy]]
    )
    ```
    **Resolution:**

    This means that the SAML Identity Provider failed to authenticate the user and sent a SAML Response to the Service Provider ({{stack}}) indicating this failure. The message will convey whether the SAML Identity Provider thinks that the problem is with the Service Provider ({{stack}}) or with the Identity Provider itself and the specific status code that follows is extremely useful as it usually indicates the underlying issue. The list of specific error codes is defined in the [SAML 2.0 Core specification - Section 3.2.2.2](https://docs.oasis-open.org/security/saml/v2.0/saml-core-2.0-os.pdf) and the most commonly encountered ones are:

    1. `urn:oasis:names:tc:SAML:2.0:status:AuthnFailed`: The SAML Identity Provider failed to authenticate the user. There is not much to troubleshoot on the {{stack}} side for this status, the logs of the SAML Identity Provider will hopefully offer much more information.
    2. `urn:oasis:names:tc:SAML:2.0:status:InvalidNameIDPolicy`: The SAML Identity Provider cannot support releasing a NameID with the requested format. When creating SAML Authentication Requests, {{es}} sets the NameIDPolicy element of the Authentication request with the appropriate value. This is controlled by the [`nameid_format`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-saml-settings) configuration parameter in [`elasticsearch.yml`](/deploy-manage/stack-settings.md), which if not set defaults to `urn:oasis:names:tc:SAML:2.0:nameid-format:transient`. This instructs the Identity Provider to return a NameID with that specific format in the SAML Response. If the SAML Identity Provider cannot grant that request, for example because it is configured to release a NameID format with `urn:oasis:names:tc:SAML:2.0:nameid-format:persistent` format instead, it returns this error indicating an invalid NameID policy. This issue can be resolved by adjusting `nameid_format` to match the format the SAML Identity Provider can return or by setting it to `urn:oasis:names:tc:SAML:2.0:nameid-format:unspecified` so that the Identity Provider is allowed to return any format it wants.

8. **Symptoms:**

    Authentication in {{kib}} fails and the following error is printed in the {{es}} logs:

    ```
    The XML Signature of this SAML message cannot be validated. Please verify that the saml
    realm uses the correct SAMLmetadata file/URL for this Identity Provider
    ```
    **Resolution:**

    This means that {{es}} failed to validate the digital signature of the SAML message that the Identity Provider sent. {{es}} uses the public key of the Identity Provider that is included in the SAML metadata, in order to validate the signature that the IdP has created using its corresponding private key. Failure to do so, can have a number of causes:

    1. As the error message indicates, the most common cause is that the wrong metadata file is used and as such the public key it contains doesn’t correspond to the private key the Identity Provider uses.
    2. The configuration of the Identity Provider has changed or the key has been rotated and the metadata file that {{es}} is using has not been updated.
    3. The SAML Response has been altered in transit and the signature cannot be validated even though the correct key is used.

    ::::{note}
    The private keys and public keys and self-signed X.509 certificates that are used in SAML for digital signatures as described above have no relation to the keys and certificates that are used for TLS either on the transport or the http layer. A failure such as the one described above has nothing to do with your `xpack.ssl` related configuration.
    ::::

9. **Symptoms:**

    Users are unable to login with a local username and password in {{kib}} because SAML is enabled.

    **Resolution:**

    If you want your users to be able to use local credentials to authenticate to {{kib}} in addition to using the SAML realm for Single Sign-On, you must enable the `basic` `authProvider` in {{kib}}. The process is documented in the [SAML Guide](../../../deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-kibana-basic)

10. **Symptoms:**

    No SAML request ID values are being passed from {{kib}} to {{es}}:

    ```
    Caused by org.elasticsearch.ElasticsearchSecurityException: SAML content is in-response-to [_A1B2C3D4E5F6G8H9I0] but expected one of []
    ```
    **Resolution:** This error indicates that {{es}} received a SAML response tied to a particular SAML request, but {{kib}} didn’t explicitly specify ID of that request. This usually means that {{kib}} cannot find the user session where it previously stored the SAML request ID.

    To resolve this issue, ensure that in your {{kib}} configuration `xpack.security.sameSiteCookies` is not set to `Strict`. Depending on your configuration, you may be able to rely on the default value or explicitly set the value to `None`.

    For further information, read [MDN SameSite cookies](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)

    If you serve multiple {{kib}} installations behind a load balancer make sure to use the [same security configuration](/deploy-manage/production-guidance/kibana-load-balance-traffic.md#load-balancing-kibana) for all installations.


**Logging:**

If the previous resolutions do not solve your issue, enable additional logging for the SAML realm to troubleshoot further. You can enable debug logging by configuring the following persistent setting:

```console
PUT /_cluster/settings
{
  "persistent": {
    "logger.org.elasticsearch.xpack.security.authc.saml": "debug"
  }
}
```

Alternatively, you can add the following lines to the end of the `log4j2.properties` configuration file in the `ES_PATH_CONF`:

```properties
logger.saml.name = org.elasticsearch.xpack.security.authc.saml
logger.saml.level = DEBUG
```

Refer to [configuring logging levels](/deploy-manage/monitor/logging-configuration/update-elasticsearch-logging-levels.md) for more information.

