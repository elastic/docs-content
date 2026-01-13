---
navigation_title: How to deploy Fleet Server
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: fleet
  - id: elastic-agent
---

# How to deploy {{fleet-server}} [deploy-fleet-server]

This guide covers deploying {{fleet-server}}, including configuration flags, environment variables, mutual TLS (mTLS) setup, and best practices for managing configuration through policies and CLI.

For platform-specific deployment instructions, refer to:
* [Deploy on-premises and self-managed {{fleet-server}}](/reference/fleet/add-fleet-server-on-prem.md)
* [Deploy {{fleet-server}} on {{k8s}}](/reference/fleet/add-fleet-server-kubernetes.md)
* [Deploy {{fleet-server}} on {{ecloud}}](/reference/fleet/add-fleet-server-cloud.md)
* [Deploy {{fleet-server}} in a mixed environment](/reference/fleet/add-fleet-server-mixed.md)

## Prerequisites [deploy-fleet-server-prereq]

Before deploying {{fleet-server}}, ensure you have:

* A {{fleet}} policy configured with the {{fleet-server}} integration
* A service token for {{fleet-server}} to authenticate with {{es}}
* TLS certificates (for production deployments)
* Network connectivity between {{fleet-server}} and {{es}}, and between {{agent}}s and {{fleet-server}}

For more information about prerequisites, refer to the platform-specific deployment guides listed above.

## Configuration overview [deploy-fleet-server-config-overview]

{{fleet-server}} requires configuration for two main connection types:

* [Configuration for {{fleet-server}} to communicate with {{es}}](#deploy-fleet-server-fs-to-es)
* [Configuration for {{fleet-server}} to accept connections from {{agent}}s (server-side)](#deploy-fleet-server-ea-to-fs)

The following sections organize all configuration flags and environment variables by connection type.

## {{fleet-server}} to {{es}} [deploy-fleet-server-fs-to-es]

These settings configure how {{fleet-server}} connects to {{es}}.

### CLI flags [deploy-fleet-server-fs-to-es-cli]

The following CLI flags are available for configuring the connection from {{fleet-server}} to {{es}}:

| Flag | Purpose | Required | Can be overridden by policy? |
| --- | --- | --- | --- |
| `--fleet-server-es` | {{es}} URL where {{fleet-server}} should connect | Yes | Yes - configured in {{es}} output associated with the policy |
| `--fleet-server-es-ca` | Path to CA certificate to validate {{es}} certificate | Optional* | Yes - configured in {{es}} output |
| `--fleet-server-es-ca-trusted-fingerprint` | SHA-256 fingerprint of CA used to sign {{es}} certificates | Optional* | No - must be CLI |
| `--fleet-server-es-cert` | Client certificate for mTLS connection to {{es}} | Optional (mTLS only) | Yes - configured in {{es}} output |
| `--fleet-server-es-cert-key` | Private key for mTLS client certificate | Optional (mTLS only) | Yes - configured in {{es}} output |
| `--fleet-server-es-insecure` | Deactivate certificate verification (not recommended) | No - not recommended | No - must be CLI |
| `--fleet-server-service-token` | Service token for {{fleet-server}} to authenticate with {{es}} | Yes | No - must be CLI or environment variable |
| `--fleet-server-service-token-path` | Path to file containing service token | Yes** | No - must be CLI or environment variable |

\* Required if {{es}} uses certificates signed by a private or intermediate CA not publicly trusted  
\** Mutually exclusive with `--fleet-server-service-token`

### Environment variables [deploy-fleet-server-fs-to-es-env]

You can also configure the connection using environment variables instead of CLI flags:

| Environment Variable | Purpose | CLI Flag Equivalent | Can be overridden by policy? |
| --- | --- | --- | --- |
| `FLEET_SERVER_ELASTICSEARCH_HOST` | {{es}} host URL | `--fleet-server-es` | Yes - configured in {{es}} output |
| `FLEET_SERVER_ELASTICSEARCH_CA` | Path to CA certificate | `--fleet-server-es-ca` | Yes - configured in {{es}} output |
| `FLEET_SERVER_ES_CERT` | Path to client certificate for mTLS | `--fleet-server-es-cert` | Yes - configured in {{es}} output |
| `FLEET_SERVER_ES_CERT_KEY` | Path to private key for mTLS | `--fleet-server-es-cert-key` | Yes - configured in {{es}} output |
| `FLEET_SERVER_SERVICE_TOKEN` | Service token value | `--fleet-server-service-token` | No - must be CLI or environment variable |
| `FLEET_SERVER_SERVICE_TOKEN_PATH` | Path to service token file | `--fleet-server-service-token-path` | No - must be CLI or environment variable |

The {{es}} host URL and CA information must be configured in both the {{es}} output associated with the {{fleet-server}} policy and in the environment variables or CLI flags provided during installation. Environment variables are only used during the bootstrap process. After bootstrap, {{fleet-server}} uses the configuration from the policy's {{es}} output.

If the URL that {{fleet-server}} uses to access {{es}} differs from the {{es}} URL used by other clients, create a dedicated {{es}} output for {{fleet-server}}.

### One-way TLS configuration [deploy-fleet-server-fs-to-es-one-way]

For one-way TLS ({{fleet-server}} validates {{es}} certificate, but {{es}} does not validate {{fleet-server}}), use the following command:

```shell
elastic-agent install \
  --fleet-server-es=https://elasticsearch:9200 \
  --fleet-server-service-token=AAEBAWVsYXm0aWMvZmxlZXQtc2XydmVyL3Rva2VuLTE2MjM4OTAztDU1OTQ6dllfVW1mYnFTVjJwTC2ZQ0EtVnVZQQ \
  --fleet-server-policy=fleet-server-policy-id \
  --fleet-server-es-ca=/path/to/elasticsearch-ca.crt
```

### Mutual TLS configuration [deploy-fleet-server-fs-to-es-mtls]

For mutual TLS (both {{fleet-server}} and {{es}} validate each other's certificates), use the following command:

```shell
elastic-agent install \
  --fleet-server-es=https://elasticsearch:9200 \
  --fleet-server-service-token=AAEBAWVsYXm0aWMvZmxlZXQtc2XydmVyL3Rva2VuLTE2MjM4OTAztDU1OTQ6dllfVW1mYnFTVjJwTC2ZQ0EtVnVZQQ \
  --fleet-server-policy=fleet-server-policy-id \
  --fleet-server-es-ca=/path/to/elasticsearch-ca.crt \
  --fleet-server-es-cert=/path/to/fleet-server-es-client.crt \
  --fleet-server-es-cert-key=/path/to/fleet-server-es-client.key
```

When configuring mTLS for {{fleet-server}} to {{es}}, also configure the corresponding settings in the {{es}} output in {{fleet}} settings. For more information, refer to [Output SSL options](/reference/fleet/tls-overview.md#output-ssl-options).

## {{agent}} to {{fleet-server}} [deploy-fleet-server-ea-to-fs]

These settings configure how {{fleet-server}} accepts connections from {{agent}}s (server-side).

### CLI flags [deploy-fleet-server-ea-to-fs-cli]

The following CLI flags are available for configuring how {{fleet-server}} accepts connections from {{agent}}s:

| Flag | Purpose | Required | Can be overridden by policy? |
| --- | --- | --- | --- |
| `--fleet-server-cert` | TLS certificate {{fleet-server}} presents to {{agent}}s | Optional* | Yes - configured in {{fleet}} settings |
| `--fleet-server-cert-key` | Private key for {{fleet-server}} certificate | Optional* | Yes - configured in {{fleet}} settings |
| `--fleet-server-cert-key-passphrase` | Path to passphrase file for encrypted private key | Optional | Yes - configured in {{fleet}} settings |
| `--certificate-authorities` | CA certificates to validate {{agent}} client certificates (for mTLS) | Optional (mTLS only) | Yes - configured in {{fleet}} settings |
| `--fleet-server-client-auth` | Client authentication mode: `none`, `optional`, or `required` | Optional | Yes - configured in {{fleet}} settings |
| `--fleet-server-host` | Binding host for {{fleet-server}} HTTP endpoint | Optional | Yes - configured in {{fleet-server}} integration policy |
| `--fleet-server-port` | Binding port for {{fleet-server}} HTTP endpoint | Optional | Yes - configured in {{fleet-server}} integration policy |
| `--fleet-server-timeout` | Timeout waiting for {{fleet-server}} to be ready | Optional | No - must be CLI or environment variable |

\* If not specified, {{fleet-server}} auto-generates a self-signed certificate. This is not recommended for production.

### Environment variables [deploy-fleet-server-ea-to-fs-env]

You can also configure these settings using environment variables instead of CLI flags:

| Environment Variable | Purpose | CLI Flag Equivalent | Can be overridden by policy? |
| --- | --- | --- | --- |
| `FLEET_SERVER_CERT` | Path to TLS certificate | `--fleet-server-cert` | Yes - configured in {{fleet}} settings |
| `FLEET_SERVER_CERT_KEY` | Path to private key | `--fleet-server-cert-key` | Yes - configured in {{fleet}} settings |
| `FLEET_SERVER_CERT_KEY_PASSPHRASE` | Path to passphrase file | `--fleet-server-cert-key-passphrase` | Yes - configured in {{fleet}} settings |
| `FLEET_CA` | Path to CA certificate for validating agent certificates | `--certificate-authorities` | Yes - configured in {{fleet}} settings |
| `FLEET_SERVER_CLIENT_AUTH` | Client authentication mode | `--fleet-server-client-auth` | Yes - configured in {{fleet}} settings |
| `FLEET_SERVER_HOST` | Binding host | `--fleet-server-host` | Yes - configured in {{fleet-server}} integration |
| `FLEET_SERVER_PORT` | Binding port | `--fleet-server-port` | Yes - configured in {{fleet-server}} integration |
| `FLEET_SERVER_TIMEOUT` | Timeout for {{fleet-server}} readiness | `--fleet-server-timeout` | No - must be CLI or environment variable |
| `FLEET_URL` | URL that {{fleet-server}} uses to access itself during bootstrap | N/A | No - must be CLI or environment variable |

The `FLEET_URL` environment variable is used by {{fleet-server}} during bootstrap to access its own endpoint. This URL must match the hostname in the {{fleet-server}} certificate's Subject Alternative Name (SAN) list. In {{k8s}} environments, if the service is not immediately available, use `https://localhost:8220` and ensure `localhost` is included in the certificate's SAN.

### One-way TLS configuration [deploy-fleet-server-ea-to-fs-oneway]

For one-way TLS ({{agent}}s validate {{fleet-server}} certificate, but {{fleet-server}} does not validate {{agent}} certificates), use the following command:

```shell
elastic-agent install \
  --fleet-server-es=https://elasticsearch:9200 \
  --fleet-server-service-token=AAEBAWVsYXm0aWMvZmxlZXQtc2XydmVyL3Rva2VuLTE2MjM4OTAztDU1OTQ6dllfVW1mYnFTVjJwTC2ZQ0EtVnVZQQ \
  --fleet-server-policy=fleet-server-policy-id \
  --fleet-server-cert=/path/to/fleet-server.crt \
  --fleet-server-cert-key=/path/to/fleet-server.key \
  --certificate-authorities=/path/to/fleet-ca.crt
```

### Mutual TLS configuration [deploy-fleet-server-ea-to-fs-mtls]

For mutual TLS (both {{fleet-server}} and {{agent}}s validate each other's certificates), use the following command:

```shell
elastic-agent install \
  --fleet-server-es=https://elasticsearch:9200 \
  --fleet-server-service-token=AAEBAWVsYXm0aWMvZmxlZXQtc2XydmVyL3Rva2VuLTE2MjM4OTAztDU1OTQ6dllfVW1mYnFTVjJwTC2ZQ0EtVnVZQQ \
  --fleet-server-policy=fleet-server-policy-id \
  --fleet-server-cert=/path/to/fleet-server.crt \
  --fleet-server-cert-key=/path/to/fleet-server.key \
  --certificate-authorities=/path/to/agent-ca.crt \
  --fleet-server-client-auth=required
```

When `--fleet-server-client-auth` is set to `optional` or `required`, {{fleet-server}} verifies client certificates presented by {{agent}}s using the CA certificates specified in `--certificate-authorities`. {{agent}}s must be enrolled with the corresponding client certificates using `--elastic-agent-cert` and `--elastic-agent-cert-key` flags. For more information, refer to [How to deploy {{agent}}](/reference/fleet/deploy-elastic-agent.md).

## Policy and CLI precedence [deploy-fleet-server-policy-precedence]

:::{include} /reference/fleet/_snippets/policy-cli-precedence-intro.md
:::

### Must be provided using CLI or environment variables [deploy-fleet-server-must-cli]

The following settings cannot be overridden by policy and must be provided during installation:

* **Service token**: `--fleet-server-service-token` or `FLEET_SERVER_SERVICE_TOKEN`
* **Policy ID**: `--fleet-server-policy` or `FLEET_SERVER_POLICY_ID`
* **{{es}} CA trusted fingerprint**: `--fleet-server-es-ca-trusted-fingerprint` (if using self-signed certificates)
* **{{fleet-server}} timeout**: `--fleet-server-timeout` or `FLEET_SERVER_TIMEOUT`
* **{{fleet-server}} URL for bootstrap**: `FLEET_URL` (environment variable only)

### Can be overridden by policy [deploy-fleet-server-can-override]

The following settings can be set using CLI during installation, but can also be updated using policy after enrollment:

* **{{es}} connection settings**: Configured in the {{es}} output associated with the {{fleet-server}} policy
  * {{es}} host URL
  * {{es}} CA certificate
  * mTLS client certificate and key for {{es}}
* **{{fleet-server}} TLS settings**: Configured in {{fleet}} settings under **{{fleet-server}} hosts**
  * {{fleet-server}} certificate and key
  * CA certificates for validating agent certificates
  * Client authentication mode
* **{{fleet-server}} binding settings**: Configured in the {{fleet-server}} integration policy
  * Host and port

### Configuration hierarchy [deploy-fleet-server-config-hierarchy]

:::{include} /reference/fleet/_snippets/config-hierarchy.md
:::

## Mutual TLS (mTLS) configuration [deploy-fleet-server-mtls]

Mutual TLS provides enhanced security by requiring both parties in a connection to authenticate using certificates.

### mTLS between {{fleet-server}} and {{es}} [deploy-fleet-server-mtls-fs-es]

Use this option when you need {{es}} to verify the identity of {{fleet-server}} in addition to {{fleet-server}} verifying {{es}}.

Configure the following settings:

1. **During installation** (CLI or environment variables):
   * `--fleet-server-es-cert` / `FLEET_SERVER_ES_CERT`: Client certificate for {{fleet-server}}
   * `--fleet-server-es-cert-key` / `FLEET_SERVER_ES_CERT_KEY`: Private key for client certificate
   * `--fleet-server-es-ca` / `FLEET_SERVER_ELASTICSEARCH_CA`: CA to validate {{es}} certificate

2. **In {{fleet}} settings** ({{es}} output):
   * `ssl.certificate`: Path to client certificate (or embed certificate)
   * `ssl.key`: Path to private key (or embed key)
   * `ssl.certificate_authorities`: CA to validate {{es}} certificate

For more information, refer to [Mutual TLS connection](/reference/fleet/mutual-tls.md#mutual-tls-on-premise).

### mTLS between {{agent}} and {{fleet-server}} [deploy-fleet-server-mtls-ea-fs]

Use this option when you need {{fleet-server}} to verify the identity of connecting {{agent}}s in addition to {{agent}}s verifying {{fleet-server}}.

Configure the following settings:

1. **During {{fleet-server}} installation** (CLI or environment variables):
   * `--fleet-server-cert` / `FLEET_SERVER_CERT`: Server certificate for {{fleet-server}}
   * `--fleet-server-cert-key` / `FLEET_SERVER_CERT_KEY`: Private key for server certificate
   * `--certificate-authorities` / `FLEET_CA`: CA to validate agent client certificates
   * `--fleet-server-client-auth=required` / `FLEET_SERVER_CLIENT_AUTH=required`: Enable client authentication

2. **During {{agent}} enrollment** (CLI or environment variables):
   * `--elastic-agent-cert` / `ELASTIC_AGENT_CERT`: Client certificate for {{agent}}
   * `--elastic-agent-cert-key` / `ELASTIC_AGENT_CERT_KEY`: Private key for client certificate
   * `--certificate-authorities` / `FLEET_CA`: CA to validate {{fleet-server}} certificate

3. **In {{fleet}} settings** ({{fleet-server}} hosts):
   * Server SSL certificate authorities: CA to validate agent certificates
   * Client SSL certificate: {{fleet-server}} certificate
   * Client SSL certificate key: {{fleet-server}} private key
   * Enable client authentication: Set to `required`

For more information, refer to [Mutual TLS connection](/reference/fleet/mutual-tls.md#mutual-tls-on-premise) and [How to deploy {{agent}}](/reference/fleet/deploy-elastic-agent.md).

## Best practices [deploy-fleet-server-best-practices]

The following sections provide best practices for deploying and managing {{fleet-server}}:

:::{include} /reference/fleet/_snippets/best-practices-certificates.md
:::

:::{include} /reference/fleet/_snippets/best-practices-config-management.md
:::

If {{fleet-server}} needs different {{es}} connection settings than other agents, create a dedicated {{es}} output for {{fleet-server}}.

### Security considerations [deploy-fleet-server-best-practices-security]

:::{include} /reference/fleet/_snippets/security-considerations-common.md
:::

## Next steps [deploy-fleet-server-next]

After deploying {{fleet-server}}, you can:

* [Deploy {{agents}}](/reference/fleet/deploy-elastic-agent.md) to connect to your {{fleet-server}}
* [Monitor {{fleet-server}}](/reference/fleet/fleet-server-monitoring.md) to ensure it's running correctly
* [Scale {{fleet-server}}](/reference/fleet/fleet-server-scalability.md) as your deployment grows
* Review [{{fleet-server}} secrets management](/reference/fleet/fleet-server-secrets.md) for secure credential handling

