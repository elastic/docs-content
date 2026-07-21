---
navigation_title: SAML signing and encryption
description: Configure Elasticsearch to sign outgoing SAML messages and decrypt incoming encrypted assertions, including certificate generation for PEM, PKCS#12, and JKS formats.
applies_to:
  stack: all
products:
  - id: elasticsearch
---

# Configure SAML signing and encryption [saml-enc-sign]

The {{stack}} supports generating signed SAML messages (for authentication and/or logout), verifying signed SAML messages from the IdP (for both authentication and logout) and can process encrypted content.

You can configure {{es}} for signing, encryption or both, using a single key or individual keys.

The {{stack}} uses X.509 certificates with RSA private keys for SAML cryptography. These keys can be generated using any standard SSL tool, including the `elasticsearch-certutil` tool.

Your IdP may require that the {{stack}} have a cryptographic key for signing SAML messages, and that you provide the corresponding signing certificate within the Service Provider configuration (either within the {{stack}} SAML metadata file, or manually configured within the IdP administration interface).

While most IdPs do not expect authentication requests to be signed, it is commonly the case that signatures are required for logout requests. Your IdP will validate these signatures against the signing certificate that has been configured for the {{stack}} Service Provider.

Encryption certificates are rarely needed, but the {{stack}} supports them for cases where IdPs or local policies mandate their use.

## Generate certificates and keys [saml-sign-generate-certs]

{{es}} supports certificates and keys in either PEM, PKCS#12 or JKS format. Some Identity Providers are more restrictive in the formats they support, and will require you to provide the certificates as a file in a particular format. You should consult the documentation for your IdP to determine what formats they support.

### Example: Using `openssl`

```sh
openssl req -new -x509 -days 3650 -nodes -sha256 -out saml-sign.crt -keyout saml-sign.key
```

### Example: Using `elasticsearch-certutil`

```{applies_to}
deployment:
  self:
```

Using the [`elasticsearch-certutil` tool](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md), you can generate a signing certificate with the following command. Because PEM format is the most commonly supported format, the example generates a certificate in that format.

```sh
bin/elasticsearch-certutil cert --self-signed --pem --days 1100 --name saml-sign --out saml-sign.zip
```

This will do the following:

* generate a certificate and key pair (the `cert` subcommand)
* create the files in PEM format (`--pem` option)
* generate a certificate that is valid for 3 years (`--days 1100`)
* name the certificate `saml-sign` (`--name` option)
* save the certificate and key in the `saml-sign.zip` file (`--out` option)

The generated zip archive will contain 3 files:

* `saml-sign.crt`, the public certificate to be used for signing
* `saml-sign.key`, the private key for the certificate
* `ca.crt`, a CA certificate that is not needed, and can be ignored.

Encryption certificates can be generated with the same process.

## Sign outgoing SAML messages [saml-sign-configure]

By default, {{es}} will sign *all* outgoing SAML messages if a signing certificate and key has been configured.

:::{tip}
* In self-managed clusters, file path settings are resolved relative to the {{es}} config directory. {{es}} will automatically monitor this file for changes and will reload the configuration whenever it is updated.
* If you're using {{ech}} or {{ece}}, then you must upload any certificate or keystore files before they can be referenced in the configuration. For {{ech}}, upload them [as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md). For {{ece}}, follow the equivalent [ECE procedure](/deploy-manage/deploy/cloud-enterprise/add-custom-bundles-plugins.md). In both cases, you can add the files to your existing SAML bundle.
* If you're using {{eck}}, then install the files as [custom configuration files](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).
:::

::::{tab-set}
:::{tab-item} PEM-formatted keys

If you want to use **PEM formatted** keys and certificates for signing, then you should configure the following settings on the SAML realm:

`signing.certificate`
:   The path to the PEM formatted certificate file. e.g. `saml/saml-sign.crt`

    :::::{note}
    Only the single leaf certificate is required for the `signing.certificate` setting, even when using an internal or non-public Certificate Authority (CA).
    If additional certificates are included, {{es}} attempts to validate the resulting chain, and the chain must be valid and complete.
    :::::

`signing.key`
:   The path to the PEM formatted key file. e.g. `saml/saml-sign.key`

`signing.secure_key_passphrase`
:   The passphrase for the key, if the file is encrypted. This is a secure setting that must be uploaded to your [{{es}} keystore](/deploy-manage/security/secure-settings.md).

:::
:::{tab-item} PKCS#12 or Java Keystore
If you want to use **PKCS#12 formatted** files or a **Java Keystore** for signing, then you should configure the following settings on the SAML realm:

`signing.keystore.path`
:   The path to the PKCS#12 or JKS keystore. e.g. `saml/saml-sign.p12`

`signing.keystore.alias`
:   The alias of the key within the keystore. e.g. `signing-key`

`signing.keystore.secure_password`
:   The passphrase for the keystore, if the file is encrypted. This is a secure setting that must be uploaded to your [{{es}} keystore](/deploy-manage/security/secure-settings.md).
:::
::::

### Sign only certain message types

If you want to sign some, but not all outgoing SAML messages, then configure `signing.saml_messages` with a comma separated list of message types to sign. Supported values are `AuthnRequest`, `LogoutRequest` and `LogoutResponse` and the default value is `*`.

For example:

```yaml
xpack:
  security:
    authc:
      realms:
        saml-realm-name:
          order: 2
          ...
          signing.saml_messages: AuthnRequest # <1>
          ...
```

1. This configuration ensures that only SAML authentication requests will be sent signed to the Identity Provider.

## Configure {{es}} for encrypted messages [saml-encryption-configure]

The {{es}} {{security-features}} support a single key for message decryption. If a key is configured, then {{es}} attempts to use it to decrypt `EncryptedAssertion` and `EncryptedAttribute` elements in Authentication responses, and `EncryptedID` elements in Logout requests.

{{es}} rejects any SAML message that contains an `EncryptedAssertion` that cannot be decrypted.

If an `Assertion` contains both encrypted and plain-text attributes, then failure to decrypt the encrypted attributes will not cause an automatic rejection. Rather, {{es}} processes the available plain-text attributes (and any `EncryptedAttributes` that could be decrypted).

:::{tip}
* In self-managed clusters, file path settings are resolved relative to the {{es}} config directory. {{es}} will automatically monitor this file for changes and will reload the configuration whenever it is updated.
* If you're using {{ech}} or {{ece}}, then you must upload any certificate or keystore files before they can be referenced in the configuration. For {{ech}}, upload them [as a custom bundle](/deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md). For {{ece}}, follow the equivalent [ECE procedure](/deploy-manage/deploy/cloud-enterprise/add-custom-bundles-plugins.md). In both cases, you can add the files to your existing SAML bundle.
* If you're using {{eck}}, then install the files as [custom configuration files](/deploy-manage/deploy/cloud-on-k8s/custom-configuration-files-plugins.md#use-a-volume-and-volume-mount-together-with-a-configmap-or-secret).
:::

::::{tab-set}
:::{tab-item} PEM-formatted keys

If you want to use **PEM formatted** keys and certificates for SAML encryption, then you should configure the following settings on the SAML realm:

`encryption.certificate`
:   The path to the PEM formatted certificate file. e.g. `saml/saml-crypt.crt`

    :::::{note}
    Only the single leaf certificate is required for the `encryption.certificate` setting, even when using an internal or non-public Certificate Authority (CA).
    If additional certificates are included, {{es}} will attempt to validate the resulting chain, and the chain must be valid and complete.
    :::::

`encryption.key`
:   The path to the PEM formatted key file. e.g. `saml/saml-crypt.key`

`encryption.secure_key_passphrase`
:   The passphrase for the key, if the file is encrypted. This is a secure setting that must be uploaded to your [{{es}} keystore](/deploy-manage/security/secure-settings.md).

:::
:::{tab-item} PKCS#12 or Java Keystore

If you want to use **PKCS#12 formatted** files or a **Java Keystore** for SAML encryption, then you should configure the following settings on the SAML realm:

`encryption.keystore.path`
:   The path to the PKCS#12 or JKS keystore. e.g. `saml/saml-crypt.p12`

`encryption.keystore.alias`
:   The alias of the key within the keystore. e.g. `encryption-key`

`encryption.keystore.secure_password`
:   The passphrase for the keystore, if the file is encrypted. This is a secure setting that must be uploaded to your [{{es}} keystore](/deploy-manage/security/secure-settings.md).

:::
::::
