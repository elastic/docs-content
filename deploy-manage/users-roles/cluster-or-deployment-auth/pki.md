---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/pki-realm.html
applies_to:
  deployment:
    self:
    ece:
    eck:
products:
  - id: elasticsearch
---

# PKI [pki-realm]

:::{{warning}}
This type of user authentication cannot be configured on {{ech}} deployments.
:::

You can configure {{es}} to use Public Key Infrastructure (PKI) certificates to authenticate users. In this scenario, clients connecting directly to {{es}} must present X.509 certificates. First, the certificates must be accepted for authentication on the SSL/TLS layer on {{es}}. Then they are optionally further validated by a PKI realm. See [PKI authentication for clients connecting directly to {{es}}](#pki-realm-for-direct-clients).

You can also use PKI certificates to authenticate to {{kib}}, however this requires some additional configuration. On {{es}}, this configuration enables {{kib}} to act as a proxy for SSL/TLS authentication and to submit the client certificates to {{es}} for further validation by a PKI realm. See [PKI authentication for clients connecting to {{kib}}](#pki-realm-for-proxied-clients).

## PKI authentication for clients connecting directly to {{es}} [pki-realm-for-direct-clients]

To use PKI in {{es}}, you configure a PKI realm, enable client authentication on the desired network layers (transport or http), and map the Distinguished Names (DNs) from the `Subject` field in the user certificates to roles. You create the mappings in a role mapping file or use the role mappings API.

1. Add a realm configuration for a `pki` realm to [`elasticsearch.yml`](/deploy-manage/stack-settings.md) under the `xpack.security.authc.realms.pki` namespace. You must explicitly set the `order` attribute. See [PKI realm settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-pki-settings) for all of the options you can set for a `pki` realm.

    For example, the following snippet shows the most basic `pki` realm configuration:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            pki:
              pki1:
                order: 1
    ```

    With this configuration, any certificate trusted by the {{es}} SSL/TLS layer is accepted for authentication. The username is the common name (CN) extracted from the DN in the Subject field of the end-entity certificate. This configuration is not sufficient to permit PKI authentication to {{kib}}; additional steps are required.

    ::::{important}
    When you configure realms in `elasticsearch.yml`, only the realms you specify are used for authentication. If you also want to use the `native` or `file` realms, you must include them in the realm chain.
    ::::

2. Optional: The username is defined by the [username_pattern](https://docs-v3-preview.elastic.dev/elastic/elasticsearch/tree/main/reference/elasticsearch/configuration-reference/security-settings#ref-pki-settings). If you want to use something other than the CN of the Subject DN as the username, you can use one of the following methods to extract the username:

    * {applies_to}`stack: ga 9.1` Extract the username from a specific RDN attribute in the Subject DN.
	* Using the [[username_pattern](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-pki-settings) setting, specify a regex to extract the desired username. The regex is applied on the Subject DN.

	:::::{tab-set}

   ::::{tab-item} Specific RDN attribute
   The username can be extracted from a specific RDN attribute in the Subject DN by using [username_rdn_name](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-pki-settings) or [username_rdn_oid](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ref-pki-settings). When an RDN attribute configuration is provided, it supersedes `username_pattern`.

   For example, to extract the username from the `CN` RDN attribute:

   ```yaml
   xpack:
     security:
       authc:
         realms:
           pki:
             pki1:
               order: 1
               username_rdn_name: "CN"
   ```
   ::::

	::::{tab-item} Regex
	Specify a regex to extract the desired username. The regex is applied on the Subject DN.
	
	For example, the regex in the following configuration extracts the email address from the Subject DN:
	
	```yaml
	xpack:
	  security:
	    authc:
	      realms:
	        pki:
	          pki1:
	            order: 1
	            username_pattern: "EMAILADDRESS=(.*?)(?:,|$)"
	```
	:::{note}
	If the regex is too restrictive and does not match the Subject DN of the client’s certificate, then the realm does not authenticate the certificate.
	:::
	::::
	
	:::::

3. Optional: If you want the same users to also be authenticated using certificates when they connect to {{kib}}, you must configure the {{es}} PKI realm to allow delegation. See [PKI authentication for clients connecting to {{kib}}](#pki-realm-for-proxied-clients).
4. Restart {{es}} because realm configuration is not reloaded automatically. If you’re following through with the next steps, you might wish to hold the restart for last.
5. If you're using a self-managed cluster, then [enable SSL/TLS](../../security/secure-cluster-communications.md#encrypt-internode-communication).
6. If you're using a self-managed cluster or {{eck}}, then enable client authentication on the desired network layers (transport or http).

    ::::{important}
    To use PKI when clients connect directly to {{es}}, you must enable SSL/TLS with client authentication by setting `xpack.security.transport.ssl.client_authentication` and `xpack.security.http.ssl.client_authentication` to `optional` or `required`. If the setting value is `optional`, clients without certificates can authenticate with other credentials.
    ::::

    When clients connect directly to {{es}} and are not proxy-authenticated, the PKI realm relies on the TLS settings of the node’s network interface. The realm can be configured to be more restrictive than the underlying network connection. That is, it is possible to configure the node such that some connections are accepted by the network interface but then fail to be authenticated by the PKI realm. However, the reverse is not possible. The PKI realm cannot authenticate a connection that has been refused by the network interface.

    In particular this means:

    * The transport or http interface must request client certificates by setting `client_authentication` to `optional` or `required`.
    * The interface must *trust* the certificate that is presented by the client by configuring either the `truststore` or `certificate_authorities` paths, or by setting `verification_mode` to `none`.
    * The *protocols* supported by the interface must be compatible with those used by the client.

    For an explanation of these settings, see [General TLS settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ssl-tls-settings).

7. Optional: Configure the PKI realm to trust a subset of certificates.

   The relevant network interface (transport or http) must be configured to trust any certificate that is to be used within the PKI realm. However, it is possible to configure the PKI realm to trust only a *subset* of the certificates accepted by the network interface. This is useful when the SSL/TLS layer trusts clients with certificates that are signed by a different CA than the one that signs your users' certificates.

     1. To configure the PKI realm with its own trust store, specify the `truststore.path` option. The path must be located within the {{es}} configuration directory (`ES_PATH_CONF`). For example:

      ```yaml
      xpack:
        security:
          authc:
            realms:
              pki:
                pki1:
                  order: 1
                  truststore:
                    path: "pki1_truststore.jks"
      ```

      :::{tip}
      If you're using {{ece}} or {{ech}}, then you must [upload this file as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) before it can be referenced.

      If you're using {{eck}}, then install the file as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).

      If you're using a self-managed cluster, then the file must be present on each node.
      :::

      The `certificate_authorities` option can be used as an alternative to the `truststore.path` setting, when the certificate files are PEM formatted. The setting accepts a list. The two options are exclusive, they cannot be both used simultaneously.

    1. If the trust store is password protected, the password should be configured by adding the appropriate `secure_password` setting [to the {{es}} keystore](/deploy-manage/security/secure-settings.md). For example, in a self-managed cluster, the following command adds the password for the example realm above:

    ```shell
    bin/elasticsearch-keystore add \
    xpack.security.authc.realms.pki.pki1.truststore.secure_password
    ```

8. Map roles for PKI users.

    You map roles for PKI users through the [role mapping APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security) or by using a file. Both configuration options are merged together. When a user authenticates against a PKI realm, the privileges for that user are the union of all privileges defined by the roles to which the user is mapped.

    You identify a user by the distinguished name in their certificate. For example, the following mapping configuration maps `John Doe` to the `user` role using the role mapping API:

    ```console
    PUT /_security/role_mapping/users
    {
      "roles" : [ "user" ],
      "rules" : { "field" : {
        "dn" : "cn=John Doe,ou=example,o=com" <1>
      } },
      "enabled": true
    }
    ```

    1. The distinguished name (DN) of a PKI user.


    Alternatively, use a role-mapping file. For example:

    ```yaml
    user: <1>
      - "cn=John Doe,ou=example,o=com" <2>
    ```

    1. The name of a role.
    2. The distinguished name (DN) of a PKI user.

    :::{tip}
    If you're using {{ece}} or {{ech}}, then you must [upload this file as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) before it can be referenced.

    If you're using {{eck}}, then install the file as a [custom configuration file](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).

    If you're using a self-managed cluster, then the file must be present on each node.
    :::

    The file’s path defaults to `ES_PATH_CONF/role_mapping.yml`. You can specify a different path (which must be within `ES_PATH_CONF`) by using the `files.role_mapping` realm setting (e.g. `xpack.security.authc.realms.pki.pki1.files.role_mapping`).

    The distinguished name for a PKI user follows X.500 naming conventions which place the most specific fields (like `cn` or `uid`) at the beginning of the name and the most general fields (like `o` or `dc`) at the end of the name. Some tools, such as *openssl*, may print out the subject name in a different format.

    One way that you can determine the correct DN for a certificate is to use the [authenticate API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-authenticate) (use the relevant PKI certificate as the means of authentication) and inspect the metadata field in the result. The user’s distinguished name will be populated under the `pki_dn` key. You can also use the authenticate API to validate your role mapping.

    For more information, see [Mapping users and groups to roles](mapping-users-groups-to-roles.md).

    ::::{note}
    The PKI realm supports [authorization realms](realm-chains.md#authorization_realms) as an alternative to role mapping.
    ::::

## PKI authentication for clients connecting to {{kib}} [pki-realm-for-proxied-clients]

By default, the PKI realm relies on the node’s network interface to perform the SSL/TLS handshake and extract the client certificate. This behavior requires that clients connect directly to {{es}} so that their SSL connection is terminated by the {{es}} node. If SSL/TLS authentication is to be performed by {{kib}}, the PKI realm must be configured to permit delegation.

Specifically, when clients presenting X.509 certificates connect to {{kib}}, {{kib}} performs the SSL/TLS authentication. {{kib}} then forwards the client’s certificate chain (by calling an {{es}} API) to have them further validated by the PKI realms that have been configured for delegation.

To permit authentication delegation for a specific {{es}} PKI realm, start by [configuring the realm](#pki-realm-for-direct-clients). In this scenario, for self-managed clusters, it is mandatory that you [encrypt HTTP client communications](../../security/secure-cluster-communications.md#encrypt-http-communication) when you enable TLS.

You must also explicitly configure a `truststore` (or, equivalently `certificate_authorities`) even though it is the same trust configuration that you have configured on the network layer. The `xpack.security.authc.token.enabled` and `delegation.enabled` settings must also be `true`. For example:

```yaml
xpack:
  security:
    authc:
      token.enabled: true
      realms:
        pki:
          pki1:
            order: 1
            delegation.enabled: true
            truststore:
              path: "pki1_truststore.jks"
```

After you restart {{es}}, this realm can validate delegated PKI authentication. You must then [configure {{kib}} to allow PKI certificate authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md#pki-authentication).

A PKI realm with `delegation.enabled` still works unchanged for clients connecting directly to {{es}}. Directly authenticated users and users that are PKI authenticated by delegation to {{kib}} both follow the same [role mapping rules](mapping-users-groups-to-roles.md) or [authorization realms configurations](realm-chains.md#authorization_realms).

If you use the [role mapping APIs](https://www.elastic.co/docs/api/doc/elasticsearch/group/endpoint-security), however, you can distinguish between users that are authenticated by delegation and users that are authenticated directly. The former have the extra fields `pki_delegated_by_user` and `pki_delegated_by_realm` in the user’s metadata. In the common setup, where authentication is delegated to {{kib}}, the values of these fields are `kibana` and `reserved`, respectively. For example, the following role mapping rule assigns the `role_for_pki1_direct` role to all users that have been authenticated directly by the `pki1` realm, by connecting to {{es}} instead of going through {{kib}}:

```console
PUT /_security/role_mapping/direct_pki_only
{
  "roles" : [ "role_for_pki1_direct" ],
  "rules" : {
    "all": [
      {
        "field": {"realm.name": "pki1"}
      },
      {
        "field": {
          "metadata.pki_delegated_by_user": null <1>
        }
      }
    ]
  },
  "enabled": true
}
```

1. If this metadata field is set (that is to say, it is **not** `null`), the user has been authenticated in the delegation scenario.

## Use PKI authentication for {{kib}} [pki-realm-kibana]

If you want to use PKI authentication to authenticate using your browser and {{kib}}, you need to enable the relevant authentication provider in {{kib}} configuration. See [{{kib}} authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md#pki-authentication).