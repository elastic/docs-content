---
navigation_title: SSL/TLS
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/elastic-agent-ssl-configuration.html
products:
  - id: fleet
  - id: elastic-agent
---

# Configure SSL/TLS for standalone {{agent}}s [elastic-agent-ssl-configuration]


There are a number of SSL configuration settings available depending on whether you are configuring a client, server, or both. See the following tables for available settings:

* [Table 7, Common configuration options](#common-ssl-options). These settings are valid in both client and server configurations.
* [Table 8, Client configuration options](#client-ssl-options)
* [Table 9, Server configuration options](#server-ssl-options)

::::{tip}
For more information about using certificates, refer to [Secure connections](/reference/fleet/secure.md).
::::

$$$common-ssl-options$$$

`ssl.ca_sha256` $$$ssl.ca_sha256-common-setting$$$
:   (string) This configures a certificate pin that you can use to ensure that a specific certificate is part of the verified chain.

    The pin is a base64 encoded string of the SHA-256 of the certificate.

    ::::{note}
    This check is not a replacement for the normal SSL validation, but it adds additional validation. If this setting is used with  `verification_mode` set to `none`, the check will always fail because it will not receive any verified chains.
    ::::


`ssl.cipher_suites` $$$ssl.cipher_suites-common-setting$$$
:   (list) The list of cipher suites to use. The first entry has the highest priority. If this option is omitted, the Go crypto library's [default suites](https://golang.org/pkg/crypto/tls/) are used (recommended). TLS 1.3 cipher suites are not individually configurable in Go, so they are not included in this list.

    The following cipher suites are available:

    * ECDHE-ECDSA-AES-128-CBC-SHA
    * ECDHE-ECDSA-AES-128-CBC-SHA256: TLS 1.2 only. Disabled by default.
    * ECDHE-ECDSA-AES-128-GCM-SHA256: TLS 1.2 only.
    * ECDHE-ECDSA-AES-256-CBC-SHA
    * ECDHE-ECDSA-AES-256-GCM-SHA384: TLS 1.2 only.
    * ECDHE-ECDSA-CHACHA20-POLY1305: TLS 1.2 only.
    * ECDHE-ECDSA-RC4-128-SHA: Disabled by default. RC4 not recommended.
    * ECDHE-RSA-3DES-CBC3-SHA
    * ECDHE-RSA-AES-128-CBC-SHA
    * ECDHE-RSA-AES-128-CBC-SHA256: TLS 1.2 only. Disabled by default.
    * ECDHE-RSA-AES-128-GCM-SHA256: TLS 1.2 only.
    * ECDHE-RSA-AES-256-CBC-SHA
    * ECDHE-RSA-AES-256-GCM-SHA384: TLS 1.2 only.
    * ECDHE-RSA-CHACHA20-POLY1205: TLS 1.2 only.
    * ECDHE-RSA-RC4-128-SHA: Disabled by default. RC4 not recommended.
    * RSA-3DES-CBC3-SHA
    * RSA-AES-128-CBC-SHA
    * RSA-AES-128-CBC-SHA256: TLS 1.2 only. Disabled by default.
    * RSA-AES-128-GCM-SHA256: TLS 1.2 only.
    * RSA-AES-256-CBC-SHA
    * RSA-AES-256-GCM-SHA384: TLS 1.2 only.
    * RSA-RC4-128-SHA: Disabled by default. RC4 not recommended.

    Here is a list of acronyms used in defining the cipher suites:

    * 3DES: Cipher suites using triple DES
    * AES-128/256: Cipher suites using AES with 128/256-bit keys.
    * CBC: Cipher using Cipher Block Chaining as block cipher mode.
    * ECDHE: Cipher suites using Elliptic Curve Diffie-Hellman (DH) ephemeral key exchange.
    * ECDSA: Cipher suites using Elliptic Curve Digital Signature Algorithm for authentication.
    * GCM: Galois/Counter mode is used for symmetric key cryptography.
    * RC4: Cipher suites using RC4.
    * RSA: Cipher suites using RSA.
    * SHA, SHA256, SHA384: Cipher suites using SHA-1, SHA-256 or SHA-384.

`ssl.curve_types` $$$ssl.curve_types-common-setting$$$
:   (list) The list of curve types for ECDHE (Elliptic Curve Diffie-Hellman ephemeral key exchange).

    The following elliptic curve types are available:

    * P-256
    * P-384
    * P-521
    * X25519

`ssl.enabled` $$$ssl.enabled-common-setting$$$
:   (boolean) Enables or disables the SSL configuration.

    **Default:** `true`

    ::::{note}
    SSL settings are disabled if either `enabled` is set to `false` or the `ssl` section is missing.
    ::::


`ssl.supported_protocols` $$$ssl.supported_protocols-common-setting$$$
:   (list) List of allowed SSL/TLS versions. If the SSL/TLS server supports none of the specified versions, the connection will be dropped during or after the handshake. The list of allowed protocol versions include: `TLSv1.1`, `TLSv1.2`, and `TLSv1.3`.

    **Default:** `[TLSv1.2, TLSv1.3]`

$$$client-ssl-options$$$

`ssl.certificate` $$$ssl.certificate-client-setting$$$
:   (string) The path to the certificate for SSL client authentication. This setting is only required if `client_authentication` is specified. If `certificate` is not specified, client authentication is not available, and the connection might fail if the server requests client authentication. If the SSL server does not require client authentication, the certificate will be loaded, but not requested or used by the server.

    Example:

    ```yaml
    ssl.certificate: "/path/to/cert.pem"
    ```

    When this setting is configured, the `ssl.key` setting is also required.

    Specify a path, or embed a certificate directly in the `YAML` configuration:

    ```yaml
    ssl.certificate: &#124;
        -----BEGIN CERTIFICATE-----
        CERTIFICATE CONTENT APPEARS HERE
        -----END CERTIFICATE-----
    ```

`ssl.certificate_authorities` $$$ssl.certificate_authorities-client-setting$$$
:   (list) The list of root certificates for verifications (required). If `certificate_authorities` is empty or not set, the system keystore is used. If `certificate_authorities` is self-signed, the host system needs to trust that CA cert as well.

    Example:

    ```yaml
    ssl.certificate_authorities: ["/path/to/root/ca.pem"]
    ```

    Specify a list of files that {{agent}} will read, or embed a certificate directly in the `YAML` configuration:

    ```yaml
    ssl.certificate_authorities:
      - &#124;
        -----BEGIN CERTIFICATE-----
        CERTIFICATE CONTENT APPEARS HERE
        -----END CERTIFICATE-----
    ```

`ssl.key` $$$ssl.key-client-setting$$$
:   (string) The client certificate key used for client authentication. Only required if `client_authentication` is configured.

    Example:

    ```yaml
    ssl.key: "/path/to/cert.key"
    ```

    Specify a path, or embed the private key directly in the `YAML` configuration:

    ```yaml
    ssl.key: &#124;
        -----BEGIN PRIVATE KEY-----
        KEY CONTENT APPEARS HERE
        -----END PRIVATE KEY-----
    ```

`ssl.key_passphrase` $$$ssl.key_passphrase-client-setting$$$
:   (string) The passphrase used to decrypt an encrypted key stored in the configured `key` file.

`ssl.verification_mode` $$$ssl.verification_mode-client-setting$$$
:   (string) Controls the verification of server certificates. Valid values are:

    `full`
    :   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate.

    `strict`
    :   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate. If the Subject Alternative Name is empty, it returns an error.

    `certificate`
    :   Verifies that the provided certificate is signed by a trusted authority (CA), but does not perform any hostname verification.

    `none`
    :   Performs *no verification* of the server’s certificate. This mode disables many of the security benefits of SSL/TLS and should only be used after cautious consideration. It is primarily intended as a temporary diagnostic mechanism when attempting to resolve TLS errors; its use in production environments is strongly discouraged.

    **Default:** `full`

`ssl.ca_trusted_fingerprint` $$$ssl.ca_trusted_fingerprint$$$
:   (string) A HEX encoded SHA-256 of a CA certificate. If this certificate is present in the chain during the handshake, it will be added to the `certificate_authorities` list and the handshake will continue normally.

    Example:

    ```yaml
    ssl.ca_trusted_fingerprint: 3b24d33844d6553...826
    ```

$$$server-ssl-options$$$

`ssl.certificate` $$$ssl.certificate-server-setting$$$
:   (string) The path to the certificate for SSL server authentication. If the certificate is not specified, startup will fail.

    Example:

    ```yaml
    ssl.certificate: "/path/to/server/cert.pem"
    ```

    When this setting is configured, the `key` setting is also required.

    Specify a path, or embed a certificate directly in the `YAML` configuration:

    ```yaml
    ssl.certificate: &#124;
        -----BEGIN CERTIFICATE-----
        CERTIFICATE CONTENT APPEARS HERE
        -----END CERTIFICATE-----
    ```

`ssl.certificate_authorities` $$$ssl.certificate_authorities-server-setting$$$
:   (list) The list of root certificates for client verifications is only required if  `client_authentication` is configured. If `certificate_authorities` is empty or not set, and `client_authentication` is configured, the system keystore is used. If `certificate_authorities` is self-signed, the host system needs to trust that CA cert too.

    Example:

    ```yaml
    ssl.certificate_authorities: ["/path/to/root/ca.pem"]
    ```

    Specify a list of files that {{agent}} will read, or embed a certificate directly in the `YAML` configuration:

    ```yaml
    ssl.certificate_authorities:
      - &#124;
        -----BEGIN CERTIFICATE-----
        CERTIFICATE CONTENT APPEARS HERE
        -----END CERTIFICATE-----
    ```

`ssl.client_authentication` $$$ssl.client_authentication-server-setting$$$
:   (string) Configures client authentication. The valid options are:

    `none`
    :   Disables client authentication.

    `optional`
    :   When a client certificate is supplied, the server will verify it.

    `required`
    :   Requires clients to provide a valid certificate.

    **Default:** `required` (if `certificate_authorities` is set); otherwise, `none`

`ssl.key` $$$ssl.key-server-setting$$$
:   (string) The server certificate key used for authentication (required).

    Example:

    ```yaml
    ssl.key: "/path/to/server/cert.key"
    ```

    Specify a path, or embed the private key directly in the `YAML` configuration:

    ```yaml
    ssl.key: &#124;
        -----BEGIN PRIVATE KEY-----
        KEY CONTENT APPEARS HERE
        -----END PRIVATE KEY-----
    ```

`ssl.key_passphrase` $$$ssl.key_passphrase-server-setting$$$
:   (string) The passphrase used to decrypt an encrypted key stored in the configured `key` file.

`ssl.renegotiation` $$$ssl.renegotiation-server-setting$$$
:   (string) Configures the type of TLS renegotiation to support. The valid options are:

    `never`
    :   Disables renegotiation.

    `once`
    :   Allows a remote server to request renegotiation once per connection.

    `freely`
    :   Allows a remote server to request renegotiation repeatedly.

    **Default:** `never`

`ssl.verification_mode` $$$ssl.verification_mode-server-setting$$$
:   (string) Controls the verification of client certificates. Valid values are:

    `full`
    :   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate.

    `strict`
    :   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate. If the Subject Alternative Name is empty, it returns an error.

    `certificate`
    :   Verifies that the provided certificate is signed by a trusted authority (CA), but does not perform any hostname verification.

    `none`
    :   Performs *no verification* of the server’s certificate. This mode disables many of the security benefits of SSL/TLS and should only be used after cautious consideration. It is primarily intended as a temporary diagnostic mechanism when attempting to resolve TLS errors; its use in production environments is strongly discouraged.

    **Default:** `full`

