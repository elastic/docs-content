---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-enterprise/current/ece-create-saml-profiles.html
---

# SAML [ece-create-saml-profiles]

You can configure Elastic Cloud Enterprise to delegate authentication of users to a Security Assertion Markup Language (SAML) authentication provider. Elastic Cloud Enterprise supports the SAML 2.0 Web Browser Single Sign On Profile only and this requires the use of a web browser. Due to this, SAML profiles should not be used for standard API clients. The security deployment acts as a SAML 2.0 compliant *service provider*.

There are several sections to the profile:

* Specify the [general SAML settings](#ece-saml-general-settings).
* Specify the necessary [attribute mappings](#ece-saml-attributes)
* Create [role mappings](#ece-saml-role-mapping), either to all users that match the profile or assign roles to specific attribute values.
* Add any [custom configuration](#ece-saml-custom-configuration) advanced settings to the YAML file. For example, if you need to ignore the SSL check for the SSL certificate of the Domain Controller in a testing environment, you might add `ssl.verification_mode: none`. Note that all entries added should omit `xpack.security.authc.realms.saml.$realm_id` prefix, as ECE will insert this itself and automatically account for any differences in format across Elasticsearch versions.
* Optional: Prepare the [trusted SSL certificate bundle](#ece-saml-ssl-certificates).
* Sign the [outgoing SAML messages](#ece-configure-saml-signing-certificates).
* [Encrypt SAML messages](#ece-encrypt-saml).

$$$ece-saml-general-settings$$$Begin the provider profile by adding the general settings:

1. [Log into the Cloud UI](../../deploy/cloud-enterprise/log-into-cloud-ui.md).
2. Go to **Users** and then **Authentication providers**.
3. From the **Add provider** drop-down menu, select **SAML**.
4. Provide a unique profile name. This name becomes the realm ID, with any spaces replaced by hyphens.

    The name can be changed, but the realm ID cannot. The realm ID becomes part of the [certificate bundle](#ece-saml-ssl-certificates).

5. Enter the Assertion Consumer Service URL endpoint within Elastic Cloud Enterprise that receives the SAML assertion.

    Example: `https://HOSTNAME_OR_IP_ADDRESS:12443/api/v1/users/auth/saml/_callback`

6. Enter the URL that receives logout messages from the authentication provider.

    Example: `https://HOSTNAME_OR_IP_ADDRESS:12443/api/v1/users/auth/_logout`

7. Enter the URI for the SAML **identity provider entity ID**. The value for this will be usually provided by the Identity Provider administrator.

    Example: `urn:example:idp`

8. Enter the URI for the SAML **service provider entity ID** that represents Elastic Cloud Enterprise. The only restriction is that this is a valid URI, but the common practice is to use the domain name where the Service Provider is available.

    Example: `http://SECURITY_DEPLOYMENT_IP:12443`

9. Specify the HTTPS URL to the metadata file of the Identity Provider.

    Example: `https://HOSTNAME_OR_IP_ADDRESS:7000/metadata`



## Map SAML attributes to User Properties [ece-saml-attributes]

The SAML assertion about a user usually includes attribute names and values that can be used for role mapping. The configuration in this section allows to configure a mapping between these SAML attribute values and [Elasticsearch user properties](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-elasticsearch-authentication). When the attributes have been mapped to user properties such as `groups`, these can then be used to configure  [role mappings](#ece-saml-role-mapping). Mapping the `principal` user property is required and the `groups` property is recommended for a minimum configuration.

Note that some additional attention must be paid to the `principal` user property. Although the SAML specification does not have many restrictions on the type of value that is mapped, ECE requires that the mapped value is also a valid Elasticsearch native realm identifier. Specifically, this means the mapped identifier should not contain any commas or slashes, and should be otherwise URL friendly.


## Create role mappings [ece-saml-role-mapping]

When a user is authenticated, the role mapping assigns them roles in Elastic Cloud Enterprise. You can assign roles by:

* Assigning all authenticated users a single role, select one of the **Default roles**.
* Assigning roles according to the user properties (such as `dn`, `groups`, `username`), use the **Add role mapping rule** fields.

In the following example, you have configured the Elasticsearch user property `groups` to map to the SAML attribute with name `SAML_Roles` and you want only users whose SAML assertion contains the `SAML_Roles` attribute with value `p_viewer` to get the `Platform viewer` role in Elastic Cloud Enterprise.

To complete the role mapping:

1. Select **Add role mapping rule**.
2. Select `groups` from the `User Property` drop down list.
3. Enter `p_viewer` in the `Value` field.
4. Select `Platform Viewer` in the `Roles` drop down list.
5. Select `Add role mapping`.


## Custom configuration [ece-saml-custom-configuration]

You can add any additional settings to the **Advanced configuration** YAML file.

You can also enable some other options:

* **Use single logout (SLO)** makes sure that when a user logs out of Elastic Cloud Enterprise, they will also be redirected to the SAML Identity Provider so that they can logout there and subsequently logout from all of the other SAML sessions they might have with other SAML Service Providers.
* **Enable force authentication** means that the Identity Provider must re-authenticate the user for each new session, even if the user has an existing, authenticated session with the Identity Provider.


## Prepare SAML SSL certificates [ece-saml-ssl-certificates]

Though optional, you can add one or more certificate authorities (CAs) to validate the SSL/TLS certificate of the server that is hosting the metadata file. This might be useful when the Identity Provider uses a certificate for TLS that is signed by an organization specific Certification Authority, that is not trusted by default by Elastic Cloud Enterprise.

1. Expand the **Advanced settings**.
2. Provide the **SSL certificate URL** to the ZIP file.

    The bundle should be a ZIP file containing a single `keystore.ks` file in the directory `/saml/:id/truststore`, where `:id` is the value of the **Realm ID** field created in the [General settings](#ece-saml-general-settings). This keystore should contain the CA certificates to be trusted. The keystore file can either be a JKS or a PKCS#12 keystore, but the name of the file should be `keystore.ks`.

3. Select a keystore type for the provided keystore.
4. If the keystore is password protected, add the password to decrypt the keystore.


## Configure SAML signing certificates [ece-configure-saml-signing-certificates]

Elastic Cloud Enterprise can be configured to sign all outgoing SAML messages. Signing the outgoing messages provides assurance that the messages are coming from the expected service.

1. Provide the **Signing certificate URL** to the ZIP file with the private key and certificate.

    The bundle should be a ZIP file containing two files named `signing.key` and `signing.pem` in the directory `/saml/:id/`, where `:id` is the value of the **Realm ID** field created in the [General settings](#ece-saml-general-settings). `signing.key` should be the private key and `signing.pem` should be the corresponding certificate to be used for signing outgoing messages.

2. If the `signing.key` file is password protected, add the password to decrypt the private key.
3. Select which types of messages get signed.


## Configure for the encryption of SAML messages [ece-encrypt-saml]

If your environment requires SAML messages to be encrypted communications, Elastic Cloud Enterprise can be configured with an encryption certificate and key pair. When the Identity Provider uses the public key in this certificate to encrypt the SAML Response ( or parts of it ), Elastic Cloud Enterprise will use the corresponding key to decrypt the message.

1. Provide the **Encryption certificate URL** to the ZIP file with the private key and certificate.

    The bundle should be a ZIP file containing two files named `encryption.key` and `encryption.pem` in the directory `/saml/:id/`, where `:id` is the value of the **Realm ID** field created in the [General settings](#ece-saml-general-settings). `encryption.key` should be the private key and `encryption.pem` should be the corresponding certificate to be used to decrypt incoming SAML messages.

2. If the `encryption.key` file is password protected, add the password to decrypt the private key.

::::{important}
API keys created by users from SAML providers are not deleted or disabled when the user is deleted or disabled in the SAML realm. When you delete a user in the SAML provider, make sure to also remove the user’s API key or delete the user in ECE.
::::


