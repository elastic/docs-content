---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-agent-server-ssl.html
applies_to:
  stack: all
---

# SSL/TLS input settings [apm-agent-server-ssl]

::::{note}
![supported deployment methods](../../../images/observability-binary-yes-fm-yes.svg "")

Most options on this page are supported by all APM Server deployment methods.

::::


These settings apply to SSL/TLS communication between the APM Server and APM Agents. See [{{apm-agent}} TLS communication](apm-agent-tls-communication.md) to learn more.

:::::::{tab-set}

::::::{tab-item} Fleet-managed
Enable TLS in the APM integration settings and use the SSL/TLS input settings to set the path to the server certificate and key.
::::::

::::::{tab-item} APM Server binary
The following is a basic APM Server SSL config with secure communication enabled. This will make APM Server serve HTTPS requests instead of HTTP.

```yaml
apm-server.ssl.enabled: true
apm-server.ssl.certificate: "/path/to/apm-server.crt"
apm-server.ssl.key: "/path/to/apm-server.key"
```

::::{tip}
If APM agents are authenticating themselves using a certificate that cannot be authenticated through known CAs (e.g. self signed certificates), use the `ssl.certificate_authorities` to set a custom CA. This will automatically modify the `ssl.client_authentication` configuration to require authentication.
::::
::::::

:::::::

## Enable TLS [_enable_tls]

Enable or disable TLS. Disabled by default.

|     |     |
| --- | --- |
| APM Server binary | `apm-server.ssl.enabled` |
| Fleet-managed | `Enable TLS` |


## File path to server certificate [_file_path_to_server_certificate]

The path to the file containing the certificate for Server authentication. Required if TLS is enabled.

|     |     |
| --- | --- |
| APM Server binary | `apm-server.ssl.certificate` |
| Fleet-managed | `File path to server certificate` |


## File path to server certificate key [_file_path_to_server_certificate_key]

The path to the file containing the Server certificate key. Required if TLS is enabled.

|     |     |
| --- | --- |
| APM Server binary | `apm-server.ssl.key` |
| Fleet-managed | `File path to server certificate key` |


## Key passphrase [_key_passphrase]

The passphrase used to decrypt an encrypted key stored in the configured `apm-server.ssl.key` file.

|     |     |
| --- | --- |
| APM Server binary | `apm-server.ssl.key_passphrase` |
| Fleet-managed | N/A |


## Supported protocol versions [_supported_protocol_versions]

This setting is a list of allowed protocol versions: `SSLv3`, `TLSv1.0`, `TLSv1.1`, `TLSv1.2` and `TLSv1.3`. We do not recommend using `SSLv3` or `TLSv1.0`. The default value is `[TLSv1.1, TLSv1.2, TLSv1.3]`.

|     |     |
| --- | --- |
| APM Server binary | `apm-server.ssl.supported_protocols` |
| Fleet-managed | `Supported protocol versions` |


## Cipher suites for TLS connections [_cipher_suites_for_tls_connections]

The list of cipher suites to use. The first entry has the highest priority. If this option is omitted, the Go crypto library’s [default suites](https://golang.org/pkg/crypto/tls/) are used (recommended). Note that TLS 1.3 cipher suites are not individually configurable in Go, so they are not included in this list.

|     |     |
| --- | --- |
| APM Server binary | `apm-server.ssl.cipher_suites` |
| Fleet-managed | `Cipher suites for TLS connections` |

The following cipher suites are available:

| Cypher | Notes |
| --- | --- |
| ECDHE-ECDSA-AES-128-CBC-SHA |  |
| ECDHE-ECDSA-AES-128-CBC-SHA256 | TLS 1.2 only. Disabled by default. |
| ECDHE-ECDSA-AES-128-GCM-SHA256 | TLS 1.2 only. |
| ECDHE-ECDSA-AES-256-CBC-SHA |  |
| ECDHE-ECDSA-AES-256-GCM-SHA384 | TLS 1.2 only. |
| ECDHE-ECDSA-CHACHA20-POLY1305 | TLS 1.2 only. |
| ECDHE-ECDSA-RC4-128-SHA | Disabled by default. RC4 not recommended. |
| ECDHE-RSA-3DES-CBC3-SHA |  |
| ECDHE-RSA-AES-128-CBC-SHA |  |
| ECDHE-RSA-AES-128-CBC-SHA256 | TLS 1.2 only. Disabled by default. |
| ECDHE-RSA-AES-128-GCM-SHA256 | TLS 1.2 only. |
| ECDHE-RSA-AES-256-CBC-SHA |  |
| ECDHE-RSA-AES-256-GCM-SHA384 | TLS 1.2 only. |
| ECDHE-RSA-CHACHA20-POLY1205 | TLS 1.2 only. |
| ECDHE-RSA-RC4-128-SHA | Disabled by default. RC4 not recommended. |
| RSA-3DES-CBC3-SHA |  |
| RSA-AES-128-CBC-SHA |  |
| RSA-AES-128-CBC-SHA256 | TLS 1.2 only. Disabled by default. |
| RSA-AES-128-GCM-SHA256 | TLS 1.2 only. |
| RSA-AES-256-CBC-SHA |  |
| RSA-AES-256-GCM-SHA384 | TLS 1.2 only. |
| RSA-RC4-128-SHA | Disabled by default. RC4 not recommended. |

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


## Curve types for ECDHE based cipher suites [_curve_types_for_ecdhe_based_cipher_suites]

The list of curve types for ECDHE (Elliptic Curve Diffie-Hellman ephemeral key exchange).

|     |     |
| --- | --- |
| APM Server binary | `apm-server.ssl.curve_types` |
| Fleet-managed | `Curve types for ECDHE based cipher suites` |


## List of root certificates for verifying client certificates [_list_of_root_certificates_for_verifying_client_certificates]

The list of root certificates for verifying client certificates. If `certificate_authorities` is empty or not set, the trusted certificate authorities of the host system are used. If `certificate_authorities` is set, `client_authentication` will be automatically set to `required`. Sending client certificates is currently only supported by the RUM agent through the browser, the Java agent (see [Agent certificate authentication](asciidocalypse://docs/apm-agent-java/docs/reference/ssl-configuration.md)), and the Jaeger agent.

|     |     |
| --- | --- |
| APM Server binary | `apm-server.ssl.certificate_authorities` |
| Fleet-managed | N/A |


## Client authentication [_client_authentication]

This configures what types of client authentication are supported. The valid options are `none`, `optional`, and `required`. The default is `none`. If `certificate_authorities` has been specified, this setting will automatically change to `required`. This option only needs to be configured when the agent is expected to provide a client certificate. Sending client certificates is currently only supported by the RUM agent through the browser, the Java agent (see [Agent certificate authentication](asciidocalypse://docs/apm-agent-java/docs/reference/ssl-configuration.md)), and the Jaeger agent.

* `none` - Disables client authentication.
* `optional` - When a client certificate is given, the server will verify it.
* `required` - Requires clients to provide a valid certificate.

|     |     |
| --- | --- |
| APM Server binary | `apm-server.ssl.client_authentication` |
| Fleet-managed | N/A |

