---
navigation_title: Certificate fingerprints
description: Use certificate fingerprints to secure Elastic Agent connections to Fleet Server and Elasticsearch without CA certificate files.
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: fleet
  - id: elastic-agent
---

# Using certificate fingerprints [certificate-fingerprints]

Certificate fingerprints provide an alternative to using certificate authority (CA) files when securing connections between {{agent}}, {{fleet-server}}, and {{es}}.

## How certificate fingerprints work [how-fingerprints-work]

Certificate fingerprints and CA certificate files establish trust in different ways during the TLS handshake. Fingerprints require the CA certificate to be in the presented chain whereas using CA files works even when the root CA is not sent by the server.

### Fingerprint method

When using `ca_trusted_fingerprint` in the configuration or the `--fleet-server-es-ca-trusted-fingerprint` CLI option:

1. The server presents its certificate chain during the TLS handshake.
2. Before validating the server certificate, the client examines each certificate in the presented chain.
3. If the client finds a CA certificate whose fingerprint matches the configured fingerprint, it adds that certificate to the in-memory list of trusted CAs.
4. The TLS handshake continues with normal certificate validation using all configured CAs including the newly added one.

::::{important}
The certificate whose fingerprint you configure must be present in the certificate chain sent by the server during the TLS handshake. If the certificate is not in the chain, the fingerprint cannot be matched, and the connection will fail with a `certificate signed by unknown authority` error.
::::

### CA certificate method

When using `ssl.certificate_authorities` in the configuration or the `--fleet-server-es-ca` CLI option:

1. The server presents its certificate chain during the TLS handshake.
2. The client uses the CA certificate file to validate the chain.
3. The root CA does not need to be in the server's presented chain because the client already has it locally.

## Requirements [fingerprint-requirements]

For a certificate fingerprint to work correctly, the certificate and fingerprint must meet these requirements:

* [The certificate must be in the server's presented chain](#fingerprint-requirements-1)
* [The certificate must be a CA certificate](#fingerprint-requirements-2)
* [The fingerprint must be correctly formatted](#fingerprint-requirements-3)

### The certificate must be in the server's presented chain [fingerprint-requirements-1]

The certificate must be included in the certificate file that the server presents during the TLS handshake. For {{es}}, this is the file specified in the `xpack.security.http.ssl.certificate` setting. For {{fleet-server}}, this is the certificate specified in the {{fleet-server}} configuration.

Certificates that exist only in the server's certificate authorities file cannot be used 
for fingerprints because they are not sent during the TLS handshake.

For a practical example of how this works with a real certificate chain, refer to [Choosing which certificate to use](#choosing-certificate).

### The certificate must be a CA certificate [fingerprint-requirements-2]

The certificate must have `CA:TRUE` in its X509v3 Basic Constraints. Server certificates cannot be used with the fingerprint method.

To check if a certificate is a CA certificate, use:

```bash
openssl x509 -noout -text -in certificate.crt
```

Look for this section in the output:

```text
X509v3 extensions:
    X509v3 Basic Constraints: critical
        CA:TRUE
```

If `CA:TRUE` is present, the certificate can be used with the fingerprint method.

### The fingerprint must be correctly formatted [fingerprint-requirements-3]

The fingerprint must be a HEX-encoded SHA-256 hash with colons removed.

## Choosing which certificate to use [choosing-certificate]

Before generating a fingerprint, you need to identify which certificate from your certificate 
chain to use. You must use a CA certificate from the certificate file that the server presents 
during the TLS handshake, and not from the server's certificate authorities file.

### Understanding your certificate chain

Consider this certificate chain as an example:

```text
Root CA → Intermediate CA 1 → Intermediate CA 2 → Server Certificate
```

Let's assume that this chain is split across two certificate files in the {{es}} configuration:

```yaml
xpack.security.http.ssl.certificate: certs/server-intermediate2-intermediate1.pem
xpack.security.http.ssl.certificate_authorities: ["certs/root-ca.pem"]
```

:::{note}
This example shows Elasticsearch configuration settings. If you're connecting to Fleet Server, the 
configuration will use different setting names, but the principle is the same.
:::

The certificate file presented during the TLS handshake (`server-intermediate2-intermediate1.pem`) 
contains:
* Server certificate
* Intermediate CA 2 certificate
* Intermediate CA 1 certificate

The certificate authorities file (`root-ca.pem`) contains:
* Root CA certificate

Based on this server configuration, the following table shows which certificates can be used for fingerprints and why:

| Fingerprint of | Result | Reason |
|----------------|--------|--------|
| Root CA | ❌ **Fails** | Not in the server's presented certificate file (not sent during the TLS handshake) |
| Intermediate CA 1 | ✅ **Works** | In the server's presented certificate file and has `CA:TRUE` |
| Intermediate CA 2 | ✅ **Works** | In the server's presented certificate file and has `CA:TRUE` |
| Server certificate | ❌ **Fails** | Not a CA certificate (`CA:FALSE`) |

**Key takeaway**: You need to use a CA certificate from the certificate file that the server presents during the TLS handshake. You cannot use the root CA if it's only in the server's certificate authorities file, and you cannot use the server certificate itself.

## Generate a certificate fingerprint [generate-fingerprint]

Use this command to generate the SHA-256 fingerprint for the CA certificate:

:::::{tab-set}
::::{tab-item} Linux
:sync: linux

```bash
openssl x509 -fingerprint -sha256 -noout -in ca.crt | \
  awk -F"=" '{print $2}' | \
  sed 's/://g'
```
::::

::::{tab-item} macOS
:sync: macos

```bash
openssl x509 -fingerprint -sha256 -noout -in ca.crt | \
  awk -F"=" '{print $2}' | \
  sed 's/://g'
```
::::

::::{tab-item} Windows
:sync: windows

In PowerShell, run:

```powershell
(openssl x509 -fingerprint -sha256 -noout -in ca.crt) -replace '.*=', '' -replace ':', ''
```

:::{note}
This requires OpenSSL for Windows to be installed.
:::
::::
:::::

This outputs a string like:

```text
A1B2C3D4E5F6789012345678901234567890123456789012345678901234ABCD
```

Use this value in the fingerprint configuration fields.

## Configuration examples [fingerprint-examples]

### CLI configuration for {{fleet-server}}

Using the [certificate chain example](#choosing-certificate) where Intermediate CA 1 is in the server's certificate file, you can install a {{fleet-server}} with the fingerprint:

```bash
sudo ./elastic-agent install \
  --url=https://fleet-server:8220 \
  --fleet-server-es=https://elasticsearch:9200 \
  --fleet-server-service-token=SERVICE_TOKEN \
  --fleet-server-policy=fleet-server-policy \
  --fleet-server-es-ca-trusted-fingerprint=INTERMEDIATE_CA1_FINGERPRINT \ <1>
  --fleet-server-port=8220
```

1. Replace `INTERMEDIATE_CA1_FINGERPRINT` with the fingerprint value of the intermediate CA certificate.

### Fleet UI configuration

1. In {{kib}}, go to **{{fleet}} > Settings**.
2. Under **Outputs**, edit your {{es}} output.
3. In the **Elasticsearch CA trusted fingerprint** field, enter the fingerprint of a CA certificate that's present in the certificate chain sent by {{es}}.

::::{note}
Refer to [Choosing which certificate to use](#choosing-certificate) to determine which certificate from your chain is appropriate for the fingerprint.
::::

## Related topics

* [Configure SSL/TLS for self-managed {{fleet-server}}s](/reference/fleet/secure-connections.md)
* [Rotate SSL/TLS CA certificates](/reference/fleet/certificates-rotation.md)
* [{{agent}} SSL configuration options](/reference/fleet/elastic-agent-ssl-configuration.md)
