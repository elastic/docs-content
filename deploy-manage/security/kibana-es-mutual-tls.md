---
navigation_title: Mutual authentication
applies_to:
  deployment:
    self: all
mapped_urls:
  - https://www.elastic.co/guide/en/kibana/current/elasticsearch-mutual-tls.html
---

# Mutual TLS authentication between {{kib}} and {{es}} [elasticsearch-mutual-tls]

Secure Sockets Layer (SSL) and Transport Layer Security (TLS) provide encryption for data-in-transit. While these terms are often used interchangeably, {{kib}} supports only TLS, which supersedes the old SSL protocols.

TLS requires X.509 certificates to authenticate the communicating parties and perform encryption of data-in-transit. Each certificate contains a public key and has and an associated — but separate — private key; these keys are used for cryptographic operations. {{kib}} supports certificates and private keys in PEM or PKCS#12 format.

In a standard TLS configuration, the server presents a signed certificate to authenticate itself to the client. In a mutual TLS configuration, the client also presents a signed certificate to authenticate itself to the server.

{{es}} {{security-features}} are enabled on your cluster by default, so each request that {{kib}} (the client) makes to {{es}} (the server) is authenticated. Most requests made by end users through {{kib}} to {{es}} are authenticated by using the credentials of the logged-in user.

To [enroll {{kib}} with an {{es}} cluster](/deploy-manage/security/self-auto-setup.md#stack-start-with-security), you pass a generated enrollment token. This token configures {{kib}} to authenticate with {{es}} using a [service account token](/deploy-manage/users-roles/cluster-or-deployment-auth/service-accounts.md#service-accounts-tokens). {{kib}} also supports mutual TLS authentication with {{es}} via a [Public Key Infrastructure (PKI) realm](/deploy-manage/users-roles/cluster-or-deployment-auth/pki.md). With this setup, {{es}} needs to verify the signature on the {{kib}} client certificate, and it also needs to map the client certificate’s distinguished name (DN) to the appropriate `kibana_system` role.

::::{note}
Using a PKI realm is a [subscription feature](https://www.elastic.co/subscriptions).
::::

## Configure {{kib}} and {{es}} to use mutual TLS authentication [_configure_kib_and_es_to_use_mutual_tls_authentication]

If you haven’t already, start {{kib}} and connect it to {{es}} using the [enrollment token](/deploy-manage/security/self-auto-setup.md#stack-start-with-security).

1. Obtain a client certificate and private key for {{kib}}.

    {{kib}} uses the client certificate and corresponding private key when connecting to {{es}}.

    ::::{note}
    This is not the same as the server certificate that {{kib}} will present to web browsers.
    ::::


    You may choose to generate a client certificate and private key using the [`elasticsearch-certutil`](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md) tool. If you followed the {{es}} documentation for [generating the certificates authority](/deploy-manage/security/set-up-basic-security.md#generate-certificates), then you already have a certificate authority (CA) to sign the {{es}} server certificate. You may choose to use the same CA to sign the {{kib}} client certificate. For example:

    ```sh
    bin/elasticsearch-certutil cert -ca elastic-stack-ca.p12 -name kibana-client -dns <your_kibana_hostname>
    ```

    This will generate a client certificate and private key in a PKCS#12 file named `kibana-client.p12`. In this example, the client certificate has a Common Name (CN) of `"kibana-client"` and a subject alternative name (SAN) of `"<your_kibana_hostname>"`. The SAN may be required if you have hostname verification enabled on {{es}}.

2. Obtain the certificate authority (CA) certificate chain for {{kib}}.

    {{es}} needs the appropriate CA certificate chain to properly establish trust when receiving connections from {{kib}}.

    If you followed the instructions to generate a client certificate, then you will have a PKCS#12 file for {{kib}}. You can extract the CA certificate chain from this file. For example:

    ```sh
    openssl pkcs12 -in kibana-client.p12 -cacerts -nokeys -out kibana-ca.crt
    ```

    This will produce a PEM-formatted file named `kibana-ca.crt` that contains the CA certificate from the PKCS#12 file.

3. Configure {{es}} with a PKI realm and a native realm.

    By default, {{es}} provides a native realm for authenticating with a username and password. However, to support both a PKI realm (for {{kib}}) and a native realm (for end users), you must configure each realm in `elasticsearch.yml`:

    ```yaml
    xpack.security.authc.realms.pki.realm1.order: 1
    xpack.security.authc.realms.pki.realm1.certificate_authorities: "/path/to/kibana-ca.crt"
    xpack.security.authc.realms.native.realm2.order: 2
    ```

4. Configure {{es}} to request client certificates.

    By default, {{es}} will not request a client certificate when establishing a TLS connection. To change this, you must set up optional client certificate authentication in `elasticsearch.yml`:

    ```yaml
    xpack.security.http.ssl.client_authentication: "optional"
    ```

5. Restart {{es}}.
6. Use {{kib}} to create a role mapping in {{es}} for the client certificate.

    This role mapping will assign the `kibana_system` role to any user that matches the included mapping rule, which is set to equal the client certificate’s DN attribute:

    ![Role mapping for the {{kib}} client certificate](/deploy-manage/images/kibana-mutual-tls-role-mapping.png "")

    For more information, see [](/deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md).

7. Configure {{kib}} to use the client certificate and private key.

    You need to specify the information required to access your client certificate and corresponding private key.

    1. If your certificate and private key are contained in a PKCS#12 file:

        Specify your PKCS#12 file in `kibana.yml`:

        ```yaml
        elasticsearch.ssl.keystore.path: "/path/to/kibana-client.p12"
        ```

        If your PKCS#12 file is encrypted, add the decryption password to your [{{kib}} keystore](secure-settings.md):

        ```yaml
        bin/kibana-keystore add elasticsearch.ssl.keystore.password
        ```

        ::::{tip}
        If your PKCS#12 file isn’t protected with a password, depending on how it was generated, you may need to set `elasticsearch.ssl.keystore.password` to an empty string.
        ::::

    2. Otherwise, if your certificate and private key are in PEM format:

        Specify your certificate and private key in `kibana.yml`:

        ```yaml
        elasticsearch.ssl.certificate: "/path/to/kibana-client.crt"
        elasticsearch.ssl.key: "/path/to/kibana-client.key"
        ```

        If your private key is encrypted, add the decryption password to your [{{kib}} keystore](secure-settings.md):

        ```yaml
        bin/kibana-keystore add elasticsearch.ssl.keyPassphrase
        ```

8. Configure {{kib}} *not* to use a username and password for {{es}}.

    You must remove the `elasticsearch.username` and `elasticsearch.password` settings from `kibana.yml`. If these are present, {{kib}} will attempt to use them to authenticate to {{es}} via the native realm.

9. Restart {{kib}}.

These steps enable {{kib}} to authenticate to {{es}} using a certificate. However, end users will only be able to authenticate to {{kib}} with a username and password. To allow end users to authenticate to {{kib}} using a client certificate, see [{{kib}} PKI authentication](/deploy-manage/users-roles/cluster-or-deployment-auth/kibana-authentication.md#pki-authentication).

