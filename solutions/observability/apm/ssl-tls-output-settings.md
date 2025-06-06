---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-configuration-ssl.html
applies_to:
  stack: all
products:
  - id: observability
  - id: apm
---

# SSL/TLS output settings [apm-configuration-ssl]

::::{note}
![supported deployment methods](/solutions/images/observability-binary-yes-fm-no.svg "")

These configuration options are only relevant to APM Server binary users. Fleet-managed users should see the [Fleet output settings](/reference/fleet/fleet-settings.md).

::::

You can specify SSL/TLS options with any output that supports SSL, like {{es}}, {{ls}}, or Kafka. Example output config with SSL/TLS enabled:

```yaml
output.elasticsearch.hosts: ["https://192.168.1.42:9200"]
output.elasticsearch.ssl.certificate_authorities: ["/etc/pki/root/ca.pem"]
output.elasticsearch.ssl.certificate: "/etc/pki/client/cert.pem"
output.elasticsearch.ssl.key: "/etc/pki/client/cert.key"
```

There are a number of SSL/TLS configuration options available to you:

* [Common configuration options](#apm-ssl-common-config)
* [Client configuration options](#apm-ssl-client-config)
* [Server configuration options](#apm-ssl-server-config)

## Common configuration options [apm-ssl-common-config]

Common SSL configuration options can be used in both client and server configurations. You can specify the following options in the `ssl` section of each subsystem that supports SSL.

### `enabled` [apm-enabled]

To disable SSL configuration, set the value to `false`. The default value is `true`.

::::{note}
SSL settings are disabled if either `enabled` is set to `false` or the `ssl` section is missing.

::::

### `supported_protocols` [apm-supported-protocols]

List of allowed SSL/TLS versions. If SSL/TLS server decides for protocol versions not configured, the connection will be dropped during or after the handshake. The setting is a list of allowed protocol versions: `SSLv3`, `TLSv1` for TLS version 1.0, `TLSv1.0`, `TLSv1.1`, `TLSv1.2`, and `TLSv1.3`.

The default value is `[TLSv1.1, TLSv1.2, TLSv1.3]`.

### `cipher_suites` [apm-cipher-suites]

The list of cipher suites to use. The first entry has the highest priority. If this option is omitted, the Go crypto library’s [default suites](https://golang.org/pkg/crypto/tls/) are used (recommended). Note that TLS 1.3 cipher suites are not individually configurable in Go, so they are not included in this list.

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

### `curve_types` [apm-curve-types]

The list of curve types for ECDHE (Elliptic Curve Diffie-Hellman ephemeral key exchange).

The following elliptic curve types are available:

* P-256
* P-384
* P-521
* X25519

### `ca_sha256` [apm-ca-sha256]

This configures a certificate pin that you can use to ensure that a specific certificate is part of the verified chain.

The pin is a base64 encoded string of the SHA-256 of the certificate.

::::{note}
This check is not a replacement for the normal SSL validation, but it adds additional validation. If this option is used with  `verification_mode` set to `none`, the check will always fail because it will not receive any verified chains.
::::

## Client configuration options [apm-ssl-client-config]

You can specify the following options in the `ssl` section of each subsystem that supports SSL.

### `certificate_authorities` [apm-client-certificate-authorities]

The list of root certificates for verifications is required. If `certificate_authorities` is self-signed, the host system needs to trust that CA cert as well.

By default you can specify a list of files that `apm-server` will read, but you can also embed a certificate directly in the `YAML` configuration:

```yaml
certificate_authorities:
  - |
    -----BEGIN CERTIFICATE-----
    MIIDCjCCAfKgAwIBAgITJ706Mu2wJlKckpIvkWxEHvEyijANBgkqhkiG9w0BAQsF
    ADAUMRIwEAYDVQQDDAlsb2NhbGhvc3QwIBcNMTkwNzIyMTkyOTA0WhgPMjExOTA2
    MjgxOTI5MDRaMBQxEjAQBgNVBAMMCWxvY2FsaG9zdDCCASIwDQYJKoZIhvcNAQEB
    BQADggEPADCCAQoCggEBANce58Y/JykI58iyOXpxGfw0/gMvF0hUQAcUrSMxEO6n
    fZRA49b4OV4SwWmA3395uL2eB2NB8y8qdQ9muXUdPBWE4l9rMZ6gmfu90N5B5uEl
    94NcfBfYOKi1fJQ9i7WKhTjlRkMCgBkWPkUokvBZFRt8RtF7zI77BSEorHGQCk9t
    /D7BS0GJyfVEhftbWcFEAG3VRcoMhF7kUzYwp+qESoriFRYLeDWv68ZOvG7eoWnP
    PsvZStEVEimjvK5NSESEQa9xWyJOmlOKXhkdymtcUd/nXnx6UTCFgnkgzSdTWV41
    CI6B6aJ9svCTI2QuoIq2HxX/ix7OvW1huVmcyHVxyUECAwEAAaNTMFEwHQYDVR0O
    BBYEFPwN1OceFGm9v6ux8G+DZ3TUDYxqMB8GA1UdIwQYMBaAFPwN1OceFGm9v6ux
    8G+DZ3TUDYxqMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAG5D
    874A4YI7YUwOVsVAdbWtgp1d0zKcPRR+r2OdSbTAV5/gcS3jgBJ3i1BN34JuDVFw
    3DeJSYT3nxy2Y56lLnxDeF8CUTUtVQx3CuGkRg1ouGAHpO/6OqOhwLLorEmxi7tA
    H2O8mtT0poX5AnOAhzVy7QW0D/k4WaoLyckM5hUa6RtvgvLxOwA0U+VGurCDoctu
    8F4QOgTAWyh8EZIwaKCliFRSynDpv3JTUwtfZkxo6K6nce1RhCWFAsMvDZL8Dgc0
    yvgJ38BRsFOtkRuAGSf6ZUwTO8JJRRIFnpUzXflAnGivK9M13D5GEQMmIl6U9Pvk
    sxSmbIUfc2SGJGCJD4I=
    -----END CERTIFICATE-----
```

### `certificate: "/etc/pki/client/cert.pem"` [apm-client-certificate]

The path to the certificate for SSL client authentication is only required if `client_authentication` is specified. If the certificate is not specified, client authentication is not available. The connection might fail if the server requests client authentication. If the SSL server does not require client authentication, the certificate will be loaded, but not requested or used by the server.

When this option is configured, the [`key`](#apm-client-key) option is also required. The certificate option support embedding of the certificate:

```yaml
certificate: |
    -----BEGIN CERTIFICATE-----
    MIIDCjCCAfKgAwIBAgITJ706Mu2wJlKckpIvkWxEHvEyijANBgkqhkiG9w0BAQsF
    ADAUMRIwEAYDVQQDDAlsb2NhbGhvc3QwIBcNMTkwNzIyMTkyOTA0WhgPMjExOTA2
    MjgxOTI5MDRaMBQxEjAQBgNVBAMMCWxvY2FsaG9zdDCCASIwDQYJKoZIhvcNAQEB
    BQADggEPADCCAQoCggEBANce58Y/JykI58iyOXpxGfw0/gMvF0hUQAcUrSMxEO6n
    fZRA49b4OV4SwWmA3395uL2eB2NB8y8qdQ9muXUdPBWE4l9rMZ6gmfu90N5B5uEl
    94NcfBfYOKi1fJQ9i7WKhTjlRkMCgBkWPkUokvBZFRt8RtF7zI77BSEorHGQCk9t
    /D7BS0GJyfVEhftbWcFEAG3VRcoMhF7kUzYwp+qESoriFRYLeDWv68ZOvG7eoWnP
    PsvZStEVEimjvK5NSESEQa9xWyJOmlOKXhkdymtcUd/nXnx6UTCFgnkgzSdTWV41
    CI6B6aJ9svCTI2QuoIq2HxX/ix7OvW1huVmcyHVxyUECAwEAAaNTMFEwHQYDVR0O
    BBYEFPwN1OceFGm9v6ux8G+DZ3TUDYxqMB8GA1UdIwQYMBaAFPwN1OceFGm9v6ux
    8G+DZ3TUDYxqMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAG5D
    874A4YI7YUwOVsVAdbWtgp1d0zKcPRR+r2OdSbTAV5/gcS3jgBJ3i1BN34JuDVFw
    3DeJSYT3nxy2Y56lLnxDeF8CUTUtVQx3CuGkRg1ouGAHpO/6OqOhwLLorEmxi7tA
    H2O8mtT0poX5AnOAhzVy7QW0D/k4WaoLyckM5hUa6RtvgvLxOwA0U+VGurCDoctu
    8F4QOgTAWyh8EZIwaKCliFRSynDpv3JTUwtfZkxo6K6nce1RhCWFAsMvDZL8Dgc0
    yvgJ38BRsFOtkRuAGSf6ZUwTO8JJRRIFnpUzXflAnGivK9M13D5GEQMmIl6U9Pvk
    sxSmbIUfc2SGJGCJD4I=
    -----END CERTIFICATE-----
```

### `key: "/etc/pki/client/cert.key"` [apm-client-key]

The client certificate key used for client authentication and is only required if `client_authentication` is configured. The key option support embedding of the private key:

```yaml
key: |
    -----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDXHufGPycpCOfI
    sjl6cRn8NP4DLxdIVEAHFK0jMRDup32UQOPW+DleEsFpgN9/ebi9ngdjQfMvKnUP
    Zrl1HTwVhOJfazGeoJn7vdDeQebhJfeDXHwX2DiotXyUPYu1ioU45UZDAoAZFj5F
    KJLwWRUbfEbRe8yO+wUhKKxxkApPbfw+wUtBicn1RIX7W1nBRABt1UXKDIRe5FM2
    MKfqhEqK4hUWC3g1r+vGTrxu3qFpzz7L2UrRFRIpo7yuTUhEhEGvcVsiTppTil4Z
    HcprXFHf5158elEwhYJ5IM0nU1leNQiOgemifbLwkyNkLqCKth8V/4sezr1tYblZ
    nMh1cclBAgMBAAECggEBAKdP5jyOicqknoG9/G564RcDsDyRt64NuO7I6hBg7SZx
    Jn7UKWDdFuFP/RYtoabn6QOxkVVlydp5Typ3Xu7zmfOyss479Q/HIXxmmbkD0Kp0
    eRm2KN3y0b6FySsS40KDRjKGQCuGGlNotW3crMw6vOvvsLTlcKgUHF054UVCHoK/
    Piz7igkDU7NjvJeha53vXL4hIjb10UtJNaGPxIyFLYRZdRPyyBJX7Yt3w8dgz8WM
    epOPu0dq3bUrY3WQXcxKZo6sQjE1h7kdl4TNji5jaFlvD01Y8LnyG0oThOzf0tve
    Gaw+kuy17gTGZGMIfGVcdeb+SlioXMAAfOps+mNIwTECgYEA/gTO8W0hgYpOQJzn
    BpWkic3LAoBXWNpvsQkkC3uba8Fcps7iiEzotXGfwYcb5Ewf5O3Lrz1EwLj7GTW8
    VNhB3gb7bGOvuwI/6vYk2/dwo84bwW9qRWP5hqPhNZ2AWl8kxmZgHns6WTTxpkRU
    zrfZ5eUrBDWjRU2R8uppgRImsxMCgYEA2MxuL/C/Ko0d7XsSX1kM4JHJiGpQDvb5
    GUrlKjP/qVyUysNF92B9xAZZHxxfPWpdfGGBynhw7X6s+YeIoxTzFPZVV9hlkpAA
    5igma0n8ZpZEqzttjVdpOQZK8o/Oni/Q2S10WGftQOOGw5Is8+LY30XnLvHBJhO7
    TKMurJ4KCNsCgYAe5TDSVmaj3dGEtFC5EUxQ4nHVnQyCpxa8npL+vor5wSvmsfUF
    hO0s3GQE4sz2qHecnXuPldEd66HGwC1m2GKygYDk/v7prO1fQ47aHi9aDQB9N3Li
    e7Vmtdn3bm+lDjtn0h3Qt0YygWj+wwLZnazn9EaWHXv9OuEMfYxVgYKpdwKBgEze
    Zy8+WDm5IWRjn8cI5wT1DBT/RPWZYgcyxABrwXmGZwdhp3wnzU/kxFLAl5BKF22T
    kRZ+D+RVZvVutebE9c937BiilJkb0AXLNJwT9pdVLnHcN2LHHHronUhV7vetkop+
    kGMMLlY0lkLfoGq1AxpfSbIea9KZam6o6VKxEnPDAoGAFDCJm+ZtsJK9nE5GEMav
    NHy+PwkYsHhbrPl4dgStTNXLenJLIJ+Ke0Pcld4ZPfYdSyu/Tv4rNswZBNpNsW9K
    0NwJlyMBfayoPNcJKXrH/csJY7hbKviAHr1eYy9/8OL0dHf85FV+9uY5YndLcsDc
    nygO9KTJuUiBrLr0AHEnqko=
    -----END PRIVATE KEY-----
```

### `key_passphrase` [apm-client-key-passphrase]

The passphrase used to decrypt an encrypted key stored in the configured `key` file.

### `verification_mode` [apm-client-verification-mode]

Controls the verification of server certificates. Valid values are:

`full`
:   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate.

`strict`
:   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate. If the Subject Alternative Name is empty, it returns an error.

`certificate`
:   Verifies that the provided certificate is signed by a trusted authority (CA), but does not perform any hostname verification.

`none`
:   Performs *no verification* of the server’s certificate. This mode disables many of the security benefits of SSL/TLS and should only be used after cautious consideration. It is primarily intended as a temporary diagnostic mechanism when attempting to resolve TLS errors; its use in production environments is strongly discouraged.

    The default value is `full`.

## Server configuration options [apm-ssl-server-config]

You can specify the following options in the `ssl` section of each subsystem that supports SSL.

### `certificate_authorities` [apm-server-certificate-authorities]

The list of root certificates for client verifications is only required if `client_authentication` is configured. If `certificate_authorities` is empty or not set, and `client_authentication` is configured, the system keystore is used.

If `certificate_authorities` is self-signed, the host system needs to trust that CA cert as well. By default you can specify a list of files that `apm-server` will read, but you can also embed a certificate directly in the `YAML` configuration:

```yaml
certificate_authorities:
  - |
    -----BEGIN CERTIFICATE-----
    MIIDCjCCAfKgAwIBAgITJ706Mu2wJlKckpIvkWxEHvEyijANBgkqhkiG9w0BAQsF
    ADAUMRIwEAYDVQQDDAlsb2NhbGhvc3QwIBcNMTkwNzIyMTkyOTA0WhgPMjExOTA2
    MjgxOTI5MDRaMBQxEjAQBgNVBAMMCWxvY2FsaG9zdDCCASIwDQYJKoZIhvcNAQEB
    BQADggEPADCCAQoCggEBANce58Y/JykI58iyOXpxGfw0/gMvF0hUQAcUrSMxEO6n
    fZRA49b4OV4SwWmA3395uL2eB2NB8y8qdQ9muXUdPBWE4l9rMZ6gmfu90N5B5uEl
    94NcfBfYOKi1fJQ9i7WKhTjlRkMCgBkWPkUokvBZFRt8RtF7zI77BSEorHGQCk9t
    /D7BS0GJyfVEhftbWcFEAG3VRcoMhF7kUzYwp+qESoriFRYLeDWv68ZOvG7eoWnP
    PsvZStEVEimjvK5NSESEQa9xWyJOmlOKXhkdymtcUd/nXnx6UTCFgnkgzSdTWV41
    CI6B6aJ9svCTI2QuoIq2HxX/ix7OvW1huVmcyHVxyUECAwEAAaNTMFEwHQYDVR0O
    BBYEFPwN1OceFGm9v6ux8G+DZ3TUDYxqMB8GA1UdIwQYMBaAFPwN1OceFGm9v6ux
    8G+DZ3TUDYxqMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAG5D
    874A4YI7YUwOVsVAdbWtgp1d0zKcPRR+r2OdSbTAV5/gcS3jgBJ3i1BN34JuDVFw
    3DeJSYT3nxy2Y56lLnxDeF8CUTUtVQx3CuGkRg1ouGAHpO/6OqOhwLLorEmxi7tA
    H2O8mtT0poX5AnOAhzVy7QW0D/k4WaoLyckM5hUa6RtvgvLxOwA0U+VGurCDoctu
    8F4QOgTAWyh8EZIwaKCliFRSynDpv3JTUwtfZkxo6K6nce1RhCWFAsMvDZL8Dgc0
    yvgJ38BRsFOtkRuAGSf6ZUwTO8JJRRIFnpUzXflAnGivK9M13D5GEQMmIl6U9Pvk
    sxSmbIUfc2SGJGCJD4I=
    -----END CERTIFICATE-----
```

### `certificate: "/etc/pki/server/cert.pem"` [apm-server-certificate]

For server authentication, the path to the SSL authentication certificate must be specified for TLS. If the certificate is not specified, startup will fail.

When this option is configured, the [`key`](#apm-server-key) option is also required. The certificate option support embedding of the certificate:

```yaml
certificate: |
    -----BEGIN CERTIFICATE-----
    MIIDCjCCAfKgAwIBAgITJ706Mu2wJlKckpIvkWxEHvEyijANBgkqhkiG9w0BAQsF
    ADAUMRIwEAYDVQQDDAlsb2NhbGhvc3QwIBcNMTkwNzIyMTkyOTA0WhgPMjExOTA2
    MjgxOTI5MDRaMBQxEjAQBgNVBAMMCWxvY2FsaG9zdDCCASIwDQYJKoZIhvcNAQEB
    BQADggEPADCCAQoCggEBANce58Y/JykI58iyOXpxGfw0/gMvF0hUQAcUrSMxEO6n
    fZRA49b4OV4SwWmA3395uL2eB2NB8y8qdQ9muXUdPBWE4l9rMZ6gmfu90N5B5uEl
    94NcfBfYOKi1fJQ9i7WKhTjlRkMCgBkWPkUokvBZFRt8RtF7zI77BSEorHGQCk9t
    /D7BS0GJyfVEhftbWcFEAG3VRcoMhF7kUzYwp+qESoriFRYLeDWv68ZOvG7eoWnP
    PsvZStEVEimjvK5NSESEQa9xWyJOmlOKXhkdymtcUd/nXnx6UTCFgnkgzSdTWV41
    CI6B6aJ9svCTI2QuoIq2HxX/ix7OvW1huVmcyHVxyUECAwEAAaNTMFEwHQYDVR0O
    BBYEFPwN1OceFGm9v6ux8G+DZ3TUDYxqMB8GA1UdIwQYMBaAFPwN1OceFGm9v6ux
    8G+DZ3TUDYxqMA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggEBAG5D
    874A4YI7YUwOVsVAdbWtgp1d0zKcPRR+r2OdSbTAV5/gcS3jgBJ3i1BN34JuDVFw
    3DeJSYT3nxy2Y56lLnxDeF8CUTUtVQx3CuGkRg1ouGAHpO/6OqOhwLLorEmxi7tA
    H2O8mtT0poX5AnOAhzVy7QW0D/k4WaoLyckM5hUa6RtvgvLxOwA0U+VGurCDoctu
    8F4QOgTAWyh8EZIwaKCliFRSynDpv3JTUwtfZkxo6K6nce1RhCWFAsMvDZL8Dgc0
    yvgJ38BRsFOtkRuAGSf6ZUwTO8JJRRIFnpUzXflAnGivK9M13D5GEQMmIl6U9Pvk
    sxSmbIUfc2SGJGCJD4I=
    -----END CERTIFICATE-----
```

### `key: "/etc/pki/server/cert.key"` [apm-server-key]

The server certificate key used for authentication is required. The key option support embedding of the private key:

```yaml
key: |
    -----BEGIN PRIVATE KEY-----
    MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDXHufGPycpCOfI
    sjl6cRn8NP4DLxdIVEAHFK0jMRDup32UQOPW+DleEsFpgN9/ebi9ngdjQfMvKnUP
    Zrl1HTwVhOJfazGeoJn7vdDeQebhJfeDXHwX2DiotXyUPYu1ioU45UZDAoAZFj5F
    KJLwWRUbfEbRe8yO+wUhKKxxkApPbfw+wUtBicn1RIX7W1nBRABt1UXKDIRe5FM2
    MKfqhEqK4hUWC3g1r+vGTrxu3qFpzz7L2UrRFRIpo7yuTUhEhEGvcVsiTppTil4Z
    HcprXFHf5158elEwhYJ5IM0nU1leNQiOgemifbLwkyNkLqCKth8V/4sezr1tYblZ
    nMh1cclBAgMBAAECggEBAKdP5jyOicqknoG9/G564RcDsDyRt64NuO7I6hBg7SZx
    Jn7UKWDdFuFP/RYtoabn6QOxkVVlydp5Typ3Xu7zmfOyss479Q/HIXxmmbkD0Kp0
    eRm2KN3y0b6FySsS40KDRjKGQCuGGlNotW3crMw6vOvvsLTlcKgUHF054UVCHoK/
    Piz7igkDU7NjvJeha53vXL4hIjb10UtJNaGPxIyFLYRZdRPyyBJX7Yt3w8dgz8WM
    epOPu0dq3bUrY3WQXcxKZo6sQjE1h7kdl4TNji5jaFlvD01Y8LnyG0oThOzf0tve
    Gaw+kuy17gTGZGMIfGVcdeb+SlioXMAAfOps+mNIwTECgYEA/gTO8W0hgYpOQJzn
    BpWkic3LAoBXWNpvsQkkC3uba8Fcps7iiEzotXGfwYcb5Ewf5O3Lrz1EwLj7GTW8
    VNhB3gb7bGOvuwI/6vYk2/dwo84bwW9qRWP5hqPhNZ2AWl8kxmZgHns6WTTxpkRU
    zrfZ5eUrBDWjRU2R8uppgRImsxMCgYEA2MxuL/C/Ko0d7XsSX1kM4JHJiGpQDvb5
    GUrlKjP/qVyUysNF92B9xAZZHxxfPWpdfGGBynhw7X6s+YeIoxTzFPZVV9hlkpAA
    5igma0n8ZpZEqzttjVdpOQZK8o/Oni/Q2S10WGftQOOGw5Is8+LY30XnLvHBJhO7
    TKMurJ4KCNsCgYAe5TDSVmaj3dGEtFC5EUxQ4nHVnQyCpxa8npL+vor5wSvmsfUF
    hO0s3GQE4sz2qHecnXuPldEd66HGwC1m2GKygYDk/v7prO1fQ47aHi9aDQB9N3Li
    e7Vmtdn3bm+lDjtn0h3Qt0YygWj+wwLZnazn9EaWHXv9OuEMfYxVgYKpdwKBgEze
    Zy8+WDm5IWRjn8cI5wT1DBT/RPWZYgcyxABrwXmGZwdhp3wnzU/kxFLAl5BKF22T
    kRZ+D+RVZvVutebE9c937BiilJkb0AXLNJwT9pdVLnHcN2LHHHronUhV7vetkop+
    kGMMLlY0lkLfoGq1AxpfSbIea9KZam6o6VKxEnPDAoGAFDCJm+ZtsJK9nE5GEMav
    NHy+PwkYsHhbrPl4dgStTNXLenJLIJ+Ke0Pcld4ZPfYdSyu/Tv4rNswZBNpNsW9K
    0NwJlyMBfayoPNcJKXrH/csJY7hbKviAHr1eYy9/8OL0dHf85FV+9uY5YndLcsDc
    nygO9KTJuUiBrLr0AHEnqko=
    -----END PRIVATE KEY-----
```

### `key_passphrase` [apm-server-key-passphrase]

The passphrase is used to decrypt an encrypted key stored in the configured `key` file.

### `verification_mode` [apm-server-verification-mode]

Controls the verification of client certificates. Valid values are:

`full`
:   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate.

`strict`
:   Verifies that the provided certificate is signed by a trusted authority (CA) and also verifies that the server’s hostname (or IP address) matches the names identified within the certificate. If the Subject Alternative Name is empty, it returns an error.

`certificate`
:   Verifies that the provided certificate is signed by a trusted authority (CA), but does not perform any hostname verification.

`none`
:   Performs *no verification* of the server’s certificate. This mode disables many of the security benefits of SSL/TLS and should only be used after cautious consideration. It is primarily intended as a temporary diagnostic mechanism when attempting to resolve TLS errors; its use in production environments is strongly discouraged.

    The default value is `full`.

### `renegotiation` [apm-server-renegotiation]

This configures what types of TLS renegotiation are supported. The valid options are:

`never`
:   Disables renegotiation.

`once`
:   Allows a remote server to request renegotiation once per connection.

`freely`
:   Allows a remote server to request renegotiation repeatedly.

    The default value is `never`.

