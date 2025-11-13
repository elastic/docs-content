---
mapped_pages:
  - https://www.elastic.co/guide/en/observability/current/apm-agent-tls.html
applies_to:
  stack: ga
products:
  - id: observability
  - id: apm
---

# APM agent TLS communication [apm-agent-tls]

TLS is disabled by default. When TLS is enabled for APM Server inbound communication, agents will verify the identity of the APM Server by authenticating its certificate.

When TLS is enabled, a certificate and corresponding private key are required. The certificate and private key can either be issued by a trusted certificate authority (CA) or be [self-signed](#apm-agent-self-sign).

## Use a self-signed certificate [apm-agent-self-sign]

### Step 1: Create a self-signed certificate [apm-agent-self-sign-1]

The {{es}} distribution offers the `certutil` tool for the creation of self-signed certificates:

1. Create a CA: `./bin/elasticsearch-certutil ca --pem`. You’ll be prompted to enter the desired location of the output zip archive containing the certificate and the private key.
2. Extract the contents of the CA archive.
3. Create the self-signed certificate: `./bin/elasticsearch-certutil cert --ca-cert <path-to-ca-crt>/ca.crt --ca-key <path-to-ca-key>/ca.key --pem --name localhost`
4. Extract the certificate and key from the resulted zip archive.

### Step 2: Configure the APM Server [apm-agent-self-sign-2]

Enable TLS and configure the APM Server to point to the extracted certificate and key:

:::::::{tab-set}

::::::{tab-item} Fleet-managed
Enable TLS in the APM integration settings and use the [SSL/TLS input settings](/solutions/observability/apm/apm-server/ssl-tls-input-settings.md) to set the path to the server certificate and key.
::::::

::::::{tab-item} APM Server binary
The following is a basic APM Server SSL config with secure communication enabled. This will make APM Server serve HTTPS requests instead of HTTP.

```yaml
apm-server.ssl.enabled: true
apm-server.ssl.certificate: "/path/to/apm-server.crt"
apm-server.ssl.key: "/path/to/apm-server.key"
```

A full list of configuration options is available in [SSL/TLS input settings](/solutions/observability/apm/apm-server/ssl-tls-input-settings.md).

::::{tip}
If APM agents are authenticating themselves using a certificate that cannot be authenticated through known CAs (e.g. self signed certificates), use the `ssl.certificate_authorities` to set a custom CA. This will automatically modify the `ssl.client_authentication` configuration to require authentication.
::::
::::::

:::::::

### Step 3: Configure APM agents [apm-agent-self-sign-3]

When the APM server uses a certificate that is not chained to a publicly-trusted certificate (e.g. self-signed), additional configuration is required in the {{apm-agent}}:

* **Go agent**: certificate pinning through [`ELASTIC_APM_SERVER_CERT`](apm-agent-go://reference/configuration.md#config-server-cert)
* **Python agent**: certificate pinning through [`server_cert`](apm-agent-python://reference/configuration.md#config-server-cert)
* **Ruby agent**: certificate pinning through [`server_ca_cert`](apm-agent-ruby://reference/configuration.md#config-ssl-ca-cert)
* **.NET agent**: [`ServerCert`](apm-agent-dotnet://reference/config-reporter.md#config-server-cert)
* **Node.js agent**: custom CA setting through [`serverCaCertFile`](apm-agent-nodejs://reference/configuration.md#server-ca-cert-file)
* **Java agent**: adding the certificate to the JVM `trustStore`. See [APM Server authentication](apm-agent-java://reference/ssl-configuration.md#ssl-server-authentication) for more details.

We do not recommend disabling {{apm-agent}} verification of the server’s certificate, but it is possible:

* **Go agent**: [`ELASTIC_APM_VERIFY_SERVER_CERT`](apm-agent-go://reference/configuration.md#config-verify-server-cert)
* **.NET agent**: [`VerifyServerCert`](apm-agent-dotnet://reference/config-reporter.md#config-verify-server-cert)
* **Java agent**: [`verify_server_cert`](apm-agent-java://reference/config-reporter.md#config-verify-server-cert)
* **PHP agent**: [`verify_server_cert`](apm-agent-php://reference/configuration-reference.md#config-verify-server-cert)
* **Python agent**: [`verify_server_cert`](apm-agent-python://reference/configuration.md#config-verify-server-cert)
* **Ruby agent**: [`verify_server_cert`](apm-agent-ruby://reference/configuration.md#config-verify-server-cert)
* **Node.js agent**: [`verifyServerCert`](apm-agent-nodejs://reference/configuration.md#validate-server-cert)

## Client certificate authentication [apm-agent-client-cert]

APM Server does not require agents to provide a certificate for authentication, and there is no dedicated support for SSL/TLS client certificate authentication in Elastic’s backend agents.

