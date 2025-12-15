---
navigation_title: How to deploy Elastic Agent
mapped_pages:
  - https://www.elastic.co/guide/en/fleet/current/deploy-elastic-agent.html
applies_to:
  stack: ga
products:
  - id: fleet
  - id: elastic-agent
---

# How to deploy {{agent}} [deploy-elastic-agent]

This guide provides comprehensive information about deploying {{agent}}, including configuration flags, environment variables, mutual TLS (mTLS) setup, and best practices for managing configuration through policies versus command-line interface (CLI).

For platform-specific installation instructions, refer to:
- [Install {{fleet}}-managed {{agent}}s](/reference/fleet/install-fleet-managed-elastic-agent.md)
- [Install {{agent}}s in containers](/reference/fleet/install-elastic-agents-in-containers.md)
- [Install standalone {{agent}}s](/reference/fleet/install-standalone-elastic-agent.md)

## Prerequisites [deploy-elastic-agent-prereq]

Before deploying {{agent}}, ensure you have:

* A running {{fleet-server}} accessible to your {{agent}}
* An enrollment token from {{fleet}} for the agent policy you want to use
* TLS certificates (if {{fleet-server}} uses custom certificates)
* Network connectivity between {{agent}} and {{fleet-server}}, and between {{agent}} and output destinations ({{es}}, {{ls}}, and so on)

For more information about prerequisites, refer to the platform-specific installation guides listed above.

## Configuration overview [deploy-elastic-agent-config-overview]

{{agent}} requires configuration for two main connection types:

* [Configuration for {{agent}} to enroll and communicate with {{fleet-server}}](#deploy-elastic-agent-ea-to-fs)
* [Configuration for {{agent}} to send data to output destinations](#deploy-elastic-agent-ea-to-outputs)

The following sections organize all configuration flags and environment variables by connection type.

## {{agent}} to {{fleet-server}} [deploy-elastic-agent-ea-to-fs]

These settings configure how {{agent}} connects to {{fleet-server}}.

### CLI flags [deploy-elastic-agent-ea-to-fs-cli]

The following CLI flags are available for configuring the connection from {{agent}} to {{fleet-server}}:

| Flag | Purpose | Required | Can be overridden by policy? |
| --- | --- | --- | --- |
| `--url` | {{fleet-server}} URL to enroll into | Yes | No - must be CLI or environment variable |
| `--enrollment-token` | Enrollment token for the agent policy | Yes | No - must be CLI or environment variable |
| `--certificate-authorities` | CA certificates to validate {{fleet-server}} certificate | Optional* | Yes - configured in {{fleet}} settings |
| `--ca-sha256` | SHA-256 fingerprint of CA for certificate pinning | Optional* | No - must be CLI |
| `--elastic-agent-cert` | Client certificate for mTLS connection to {{fleet-server}} | Optional (mTLS only) | Yes - configured in {{fleet}} settings |
| `--elastic-agent-cert-key` | Private key for mTLS client certificate | Optional (mTLS only) | Yes - configured in {{fleet}} settings |
| `--elastic-agent-cert-key-passphrase` | Path to passphrase file for encrypted private key | Optional | Yes - configured in {{fleet}} settings |
| `--insecure` | Disable certificate verification (not recommended) | No - not recommended | No - must be CLI or environment variable |
| `--id` | Unique agent identifier | Optional | No - must be CLI or environment variable |
| `--replace-token` | Token to replace an existing agent with same ID | Optional | No - must be CLI or environment variable |
| `--tag` | Comma-separated list of tags for the agent | Optional | No - must be CLI or environment variable |
| `--proxy-url` | Proxy URL for {{fleet-server}} connections | Optional | Yes - configured in agent policy |
| `--proxy-disabled` | Disable proxy support | Optional | No - must be CLI |
| `--proxy-header` | Additional headers for proxy CONNECT requests | Optional | No - must be CLI |

\* Required if {{fleet-server}} uses certificates signed by a private or intermediate CA not publicly trusted

### Environment variables [deploy-elastic-agent-ea-to-fs-env]

You can also configure the connection using environment variables instead of CLI flags:

| Environment variable | Purpose | CLI flag equivalent | Can be overridden by policy? |
| --- | --- | --- | --- |
| `FLEET_URL` | {{fleet-server}} URL | `--url` | No - must be CLI or environment variable |
| `FLEET_ENROLLMENT_TOKEN` | Enrollment token | `--enrollment-token` | No - must be CLI or environment variable |
| `FLEET_CA` | Path to CA certificate | `--certificate-authorities` | Yes - configured in {{fleet}} settings |
| `ELASTIC_AGENT_CERT` | Path to client certificate for mTLS | `--elastic-agent-cert` | Yes - configured in {{fleet}} settings |
| `ELASTIC_AGENT_CERT_KEY` | Path to private key for mTLS | `--elastic-agent-cert-key` | Yes - configured in {{fleet}} settings |
| `ELASTIC_AGENT_CERT_KEY_PASSPHRASE` | Path to passphrase file | `--elastic-agent-cert-key-passphrase` | Yes - configured in {{fleet}} settings |
| `FLEET_INSECURE` | Disable certificate verification | `--insecure` | No - must be CLI or environment variable |
| `ELASTIC_AGENT_ID` | Unique agent identifier | `--id` | No - must be CLI or environment variable |
| `FLEET_REPLACE_TOKEN` | Token to replace existing agent | `--replace-token` | No - must be CLI or environment variable |
| `ELASTIC_AGENT_TAGS` | Comma-separated tags | `--tag` | No - must be CLI or environment variable |

### One-way TLS configuration [deploy-elastic-agent-ea-to-fs-one-way]

For one-way TLS ({{agent}} validates {{fleet-server}} certificate, but {{fleet-server}} does not validate {{agent}} certificate), use the following command:

```shell
elastic-agent install \
  --url=https://fleet-server:8220 \
  --enrollment-token=NEFmVllaa0JLRXhKebVKVTR5TTI6N2JaVlJpSGpScmV0ZUVnZVlRUExFQQ== \
  --certificate-authorities=/path/to/fleet-ca.crt
```

### Mutual TLS configuration [deploy-elastic-agent-ea-to-fs-mtls]

For mutual TLS (both {{agent}} and {{fleet-server}} validate each other's certificates), use the following command:

```shell
elastic-agent install \
  --url=https://fleet-server:8220 \
  --enrollment-token=NEFmVllaa0JLRXhKebVKVTR5TTI6N2JaVlJpSGpScmV0ZUVnZVlRUExFQQ== \
  --certificate-authorities=/path/to/fleet-ca.crt \
  --elastic-agent-cert=/path/to/agent-client.crt \
  --elastic-agent-cert-key=/path/to/agent-client.key
```

::::{note}
When using mTLS between {{agent}} and {{fleet-server}}, the {{fleet-server}} must be configured with `--fleet-server-client-auth=required` (or `optional`) and the corresponding CA certificates. For more information, refer to [How to deploy {{fleet-server}}](/reference/fleet/deploy-fleet-server.md).
::::

## {{agent}} to {{es}}, {{ls}} or other outputs [deploy-elastic-agent-ea-to-outputs]

These settings configure how {{agent}} sends data to output destinations ({{es}}, {{ls}}, Kafka, and so on).

### Configuration method [deploy-elastic-agent-ea-to-outputs-method]

Output configuration for {{fleet}}-managed {{agent}}s is primarily managed through {{fleet}} settings and agent policies, not CLI flags. However, some settings can be configured using environment variables for containerized deployments.

### Environment variables [deploy-elastic-agent-ea-to-outputs-env]

The following environment variables can be used for output configuration:

| Environment variable | Purpose | Can be overridden by policy? |
| --- | --- | --- |
| `ELASTICSEARCH_HOST` | {{es}} host URL | Yes - configured in {{es}} output |
| `ELASTICSEARCH_USERNAME` | Basic authentication username | Yes - configured in {{es}} output |
| `ELASTICSEARCH_PASSWORD` | Basic authentication password | Yes - configured in {{es}} output |
| `ELASTICSEARCH_API_KEY` | API key for authentication | Yes - configured in {{es}} output |
| `ELASTICSEARCH_CA` | Path to CA certificate | Yes - configured in {{es}} output |

::::{note}
Environment variables are typically used for containerized deployments or when using the [env provider](/reference/fleet/env-provider.md) to reference values in policies.

For standalone {{agent}}s, output configuration is done in the `elastic-agent.yml` file. For more information, refer to [Configure outputs for standalone {{agent}}s](/reference/fleet/elastic-agent-output-configuration.md).
::::

### One-way TLS configuration [deploy-elastic-agent-ea-to-outputs-one-way]

For one-way TLS ({{agent}} validates the output's certificate, but the output does not validate {{agent}}'s certificate), configure the following:

**In {{fleet}} settings ({{es}} output)**:
- Configure the output host URL
- Add CA certificate in {{es}} CA trusted fingerprint or advanced YAML configuration:

  ```yaml
  ssl.certificate_authorities: ["/path/to/es-ca.crt"]
  ```

**Using environment variables** (containerized deployments):

```shell
ELASTICSEARCH_HOST=https://elasticsearch:9200
ELASTICSEARCH_CA=/path/to/es-ca.crt
```

### Mutual TLS configuration [deploy-elastic-agent-ea-to-outputs-mtls]

For mutual TLS (both {{agent}} and output validate each other's certificates), configure the following:

**In {{fleet}} settings ({{es}} output - advanced YAML configuration)**:

```yaml
ssl.certificate_authorities:
  - /path/to/es-ca.crt
ssl.certificate: /path/to/agent-client.crt
ssl.key: /path/to/agent-client.key
```

::::{important}
When configuring mTLS for {{agent}} to {{es}} connections:
* The certificate and key paths must be available on all hosts running {{agent}}s. Alternatively, you can embed the certificates directly in the YAML configuration.
* The CA used to sign the agent certificate must be trusted by {{es}}.

For more information, refer to [Mutual TLS connection](/reference/fleet/mutual-tls.md#mutual-tls-on-premise) and [Output SSL options](/reference/fleet/tls-overview.md#output-ssl-options).
::::

### {{ls}} output configuration [deploy-elastic-agent-ea-to-outputs-logstash]

For {{agent}} to {{ls}} connections, configure the output in {{fleet}} settings as follows:

- Configure the {{ls}} host URL
- Configure TLS settings if required. For one-way TLS, only include `ssl.certificate_authorities`. For mutual TLS, also include `ssl.certificate` and `ssl.key`:

  ```yaml
  ssl.certificate_authorities:
    - /path/to/logstash-ca.crt
  ssl.certificate: /path/to/agent-client.crt
  ssl.key: /path/to/agent-client.key
  ```

For more information, refer to [Configure {{ls}} output](/reference/fleet/ls-output-settings.md) and [Secure {{ls}} connections](/reference/fleet/secure-logstash-connections.md).

## Policy and CLI precedence [deploy-elastic-agent-policy-precedence]

Understanding what can be configured using policy and what must be provided using CLI or environment variables is crucial for managing {{agent}} deployments.

### Must be provided using CLI or environment variables [deploy-elastic-agent-must-cli]

The following settings cannot be overridden by policy and must be provided during enrollment:

* **{{fleet-server}} URL**: `--url` or `FLEET_URL`
* **Enrollment token**: `--enrollment-token` or `FLEET_ENROLLMENT_TOKEN`
* **Agent ID**: `--id` or `ELASTIC_AGENT_ID` (if specified)
* **Replace token**: `--replace-token` or `FLEET_REPLACE_TOKEN` (if replacing an agent)
* **Tags**: `--tag` or `ELASTIC_AGENT_TAGS`
* **CA fingerprint**: `--ca-sha256` (if using certificate pinning)
* **Insecure flag**: `--insecure` or `FLEET_INSECURE` (not recommended)

### Can be overridden by policy [deploy-elastic-agent-can-override]

The following settings can be set using CLI during enrollment, but can also be updated using policy after enrollment:

* **CA certificates for {{fleet-server}}**: Configured in {{fleet}} settings under **{{fleet-server}} hosts**
* **mTLS client certificates for {{fleet-server}}**: Configured in {{fleet}} settings under **{{fleet-server}} hosts**
* **Output configuration**: Configured in {{fleet}} settings under **Outputs**
  * Output host URLs
  * Output authentication (API keys, usernames/passwords)
  * Output TLS/mTLS settings
* **Proxy settings**: Configured in agent policy

### Configuration hierarchy [deploy-elastic-agent-config-hierarchy]

The configuration precedence is as follows (highest to lowest):

1. CLI flags (during installation/enrollment)
2. Environment variables (during installation/enrollment)
3. Policy configuration (after enrollment, downloaded from {{fleet-server}})

Settings provided using CLI or environment variables during enrollment are used for the initial connection to {{fleet-server}}. After enrollment, the {{agent}} downloads its policy from {{fleet-server}}, and policy settings take precedence for most configuration options (except those listed in the [Must be provided using CLI or environment variables](#deploy-elastic-agent-must-cli) section above).

::::{note}
If the agent policy contains mTLS configuration settings, those settings will take precedence over those used during enrollment. This includes both the mTLS settings used for connectivity between {{agent}} and {{fleet-server}}, and the settings used between {{agent}} and its specified output.

The initial TLS, mTLS, or proxy configuration settings specified when {{agent}} is enrolled cannot be removed through the agent policy; they can only be updated.
::::

## Mutual TLS (mTLS) configuration [deploy-elastic-agent-mtls]

Mutual TLS provides enhanced security by requiring both parties in a connection to authenticate using certificates.

### mTLS between {{agent}} and {{fleet-server}} [deploy-elastic-agent-mtls-ea-fs]

Use this option when you need {{fleet-server}} to verify the identity of connecting {{agent}}s in addition to {{agent}}s verifying {{fleet-server}}.

Configure the following settings:

1. **During {{agent}} enrollment** (CLI or environment variables):
   * `--elastic-agent-cert` / `ELASTIC_AGENT_CERT`: Client certificate for {{agent}}
   * `--elastic-agent-cert-key` / `ELASTIC_AGENT_CERT_KEY`: Private key for client certificate
   * `--certificate-authorities` / `FLEET_CA`: CA to validate {{fleet-server}} certificate

2. **During {{fleet-server}} installation** (must be configured):
   * `--fleet-server-client-auth=required` / `FLEET_SERVER_CLIENT_AUTH=required`: Enable client authentication
   * `--certificate-authorities` / `FLEET_CA`: CA to validate agent client certificates

3. **In {{fleet}} settings** ({{fleet-server}} hosts):
   * Server SSL certificate authorities: CA to validate agent certificates
   * Enable client authentication: Set to `required`

For more information, refer to [Mutual TLS connection](/reference/fleet/mutual-tls.md#mutual-tls-on-premise) and [How to deploy {{fleet-server}}](/reference/fleet/deploy-fleet-server.md).

### mTLS between {{agent}} and {{es}}/{{ls}} [deploy-elastic-agent-mtls-ea-outputs]

Use this option when you need output destinations ({{es}}, {{ls}}) to verify the identity of {{agent}}s in addition to {{agent}}s verifying the output.

Configure the following settings:

1. **In {{fleet}} settings** ({{es}} or {{ls}} output - advanced YAML configuration):

   ```yaml
   ssl.certificate_authorities:
     - /path/to/output-ca.crt
   ssl.certificate: /path/to/agent-client.crt
   ssl.key: /path/to/agent-client.key
   ```

2. **On the output side** ({{es}} or {{ls}}):
   * Configure the output to require client certificates
   * Ensure the CA used to sign agent certificates is trusted by the output

::::{note}
For {{es}} outputs, mTLS configuration is done in the output settings. For {{ls}} outputs, mTLS configuration is also done in the output settings, but you might also need to configure {{ls}} itself to require client certificates.

For more information, refer to [Mutual TLS connection](/reference/fleet/mutual-tls.md#mutual-tls-on-premise) and [Secure {{ls}} connections](/reference/fleet/secure-logstash-connections.md).
::::

## Best practices [deploy-elastic-agent-best-practices]

The following sections provide best practices for deploying and managing {{agent}}:

### Certificate management [deploy-elastic-agent-best-practices-certs]

Follow these best practices for managing certificates:

* Never use self-signed certificates in production. Generate certificates using a trusted CA or your organization's CA.
* When generating certificates, include all hostnames and IP addresses that will be used in the certificate's Subject Alternative Name (SAN) list.
* Store private keys securely and use appropriate file permissions. Consider using encrypted keys with passphrases.
* Plan for certificate rotation. For more information, refer to [Certificate rotation](/reference/fleet/certificates-rotation.md).

### Configuration management [deploy-elastic-agent-best-practices-config]

Follow these best practices for managing configuration:

* After initial enrollment, manage most settings through {{fleet}} policies rather than CLI flags.
* Document your configuration to keep track of which settings are configured using CLI, environment variables, and policies.
* Test policy changes in a non-production environment before applying to production.
* For containerized {{agent}}s, use environment variables to provide host-specific settings while keeping policies generic.

### Security considerations [deploy-elastic-agent-best-practices-security]

Follow these security best practices:

* Use mutual TLS for both {{agent}} to {{fleet-server}} and {{fleet-server}} to {{agent}} to output connections in high-security environments.
* Prefer API keys or service tokens over basic authentication for output connections.
* Consider network segmentation to limit which hosts can connect to {{fleet-server}} and outputs.
* Keep {{agent}} versions up to date to benefit from security patches.

## Next steps [deploy-elastic-agent-next]

After deploying {{agent}}, you can:

* [Manage {{agent}}s in {{fleet}}](/reference/fleet/manage-elastic-agents-in-fleet.md) to monitor and update agent configurations
* [Monitor {{agent}}](/reference/fleet/monitor-elastic-agent.md) to ensure it's running correctly
* [Upgrade {{agent}}](/reference/fleet/upgrade-elastic-agent.md) to newer versions
* Review [{{agent}} environment variables](/reference/fleet/agent-environment-variables.md) (for containerized deployments)