---
applies_to:
  deployment: ga
navigation_title:
products:
  - id: apm
  - id: elastic-agent
  - id: beats
  - id: fleet
applies_to:
  stack: preview 9.1

---

# FIPS mode for Ingest tools [fips-ingest]

{{agent}}, {{fleet}}, {{filebeat}}, {{metricbeat}}, and {{apm-server}} are FIPS 140-3 capable. They use Go's native FIPS 140-3 module (`GOFIPS140=v1.0.0`, CMVP Certificate [#5247](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/5247)) for cryptographic operations. Specific components and configurations that fall outside the certified boundary are documented in the limitations sections below.

## FIPS-compatible binaries and configuration [fips-binaries]

FIPS compatible binaries for {{agent}}, {{fleet}}, {{filebeat}}, {{metricbeat}}, and {{apm-server}} are available for [download](https://www.elastic.co/downloads). Look for the `Linux 64-bit (FIPS)` or `Linux aarch64 (FIPS)` platform option on the product download pages for {{agent}} and {{fleet}}, {{filebeat}}, and {{metricbeat}}. Look for the `Linux x86_64 (FIPS)` or `Linux aarch64 (FIPS)` platform option on the {{apm-server}} download page.

:::{important}
The default configurations provided in the binaries are designed for FIPS-capable operation. Review the limitations below to ensure your full deployment stays within the certified boundary.
:::

## Limitations [ingest-limitations-all]

### TLS [ingest-limitations-tls]

Only FIPS 140-3 compliant TLS protocols, ciphers, and curve types are allowed to be used as listed in the following section.
* The supported TLS versions are `TLS v1.2` and `TLS v1.3`.
* The supported cipher suites are:
  * `TLS v1.2`: `ECDHE-RSA-AES-128-GCM-SHA256`, `ECDHE-RSA-AES-256-GCM-SHA384`, `ECDHE-ECDSA-AES-128-GCM-SHA256`, `ECDHE-ECDSA-AES-256-GCM-SHA384`
  * `TLS v1.3`: `TLS-AES-128-GCM-SHA256`, `TLS-AES-256-GCM-SHA384`
* The supported curve types are `P-256`, `P-384` and `P-521`.
* The minimum key length is 2048 bits for RSA keys. EC key size is determined by the curve in use; see the supported curve types above.

Support for encrypted private keys is not available, as the cryptographic modules used for decrypting password protected keys are not FIPS validated. If an output or any other component with an SSL key that is password protected is configured, the components will fail to load the key. When running in FIPS mode, you must provide non-encrypted keys.
Be sure to enforce security in your FIPS environments through other means, such as strict file permissions and access controls on the key file itself, for example.

These TLS related restrictions apply to all components listed in the preceding section.

### General output and input limitations (Kerberos protocol) [ingest-inputoutput-limitations]

The Kerberos protocol is not supported for outputs and inputs in {{filebeat}}, {{metricbeat}}, {{apm-server}}, and {{fleet-server}} configurations. This also restricts the available `sasl.mechanism` for the Kafka output, where only `PLAIN` is supported.

This impacts [Filebeat](beats://reference/filebeat/configuration-kerberos.md), [Metricbeat](beats://reference/metricbeat/configuration-kerberos.md) and {{apm-server}}, as well as output configurations for {{agent}} with {{fleet-server}}.


### APM Server [ingest-apm-limitations]

* The [Secrets Keystore](/solutions/observability/apm/apm-server/secrets-keystore-for-secure-settings.md) is not supported.

### Filebeat [ingest-filebeat-limitations]

* The [Secrets Keystore](beats://reference/filebeat/keystore.md) is not supported.
* The [Translate GUID processor](beats://reference/filebeat/processor-translate-guid.md) is not supported.
* The [Fingerprint processor](beats://reference/filebeat/fingerprint.md) does not support the md5 and sha1 method.
* The [Community ID Network Flowhash processor](beats://reference/filebeat/community-id.md) is not supported.
* The [Azure module](beats://reference/filebeat/filebeat-module-azure.md) including the [Azure eventhub input](beats://reference/filebeat/filebeat-input-azure-eventhub.md) and the [Azure Blob Storage Input](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-azure-blob-storage) are not supported. The [Add Cloud Metadata processor](beats://reference/filebeat/add-cloud-metadata.md) does not support the Azure Virtual Machine provider.
* The [Office 365 module (Beta)](beats://reference/filebeat/filebeat-module-o365.md) and the [Office 365 input (Deprecated)](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-o365audit) are not supported.
* The [GCP Pub/Sub input](beats://reference/filebeat/filebeat-input-gcp-pubsub.md) and the [Google Cloud Storage input](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-gcs) are not supported.
* The [Entity Analytics input](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-entity-analytics) is not supported.

### Metricbeat [ingest-metricbeat-limitations]

* The [Secrets Keystore](beats://reference/metricbeat/keystore.md) is not supported.
* The [Translate GUID processor](beats://reference/metricbeat/processor-translate-guid.md) is not supported.
* The [Fingerprint processor](beats://reference/metricbeat/fingerprint.md) does not support the md5 and sha1 method.
* The [Community ID Network Flowhash processor](beats://reference/metricbeat/community-id.md) is not supported.
* The [Azure module](beats://reference/metricbeat/metricbeat-module-azure.md) is not supported. The [Add Cloud Metadata processor](beats://reference/metricbeat/add-cloud-metadata.md) does not support the Azure Virtual Machine provider.
* The [Google Cloud Platform module](https://www.elastic.co/docs/reference/beats/metricbeat/metricbeat-module-gcp) is not supported.
* The [Beta KVM module](beats://reference/metricbeat/metricbeat-module-kvm.md) is not supported.
* The [Mongo DB module](beats://reference/metricbeat/metricbeat-module-mongodb.md) is not supported.
* The [MySQL](beats://reference/metricbeat/metricbeat-module-mysql.md), [PostgreSQL](beats://reference/metricbeat/metricbeat-module-postgresql.md), [MSSQL](beats://reference/metricbeat/metricbeat-module-mssql.md) and [SQL](beats://reference/metricbeat/metricbeat-module-sql.md) modules are not supported.
* The [Oracle module](beats://reference/metricbeat/metricbeat-module-oracle.md) is not supported.

### Elastic Agent and Fleet Server [ingest-limitations-agent]

When you use {{agent}} and {{fleet-server}}, these limitations apply:
* Some Elastic Integrations are not FIPS compatible, as they depend on functionality that is not supported for FIPS configuration. In general, when using {{agent}} and {{fleet-server}}, the same restrictions listed previously for {{metricbeat}} and {{filebeat}} modules, inputs, and processors apply.
* Agent upgrade artifact verification uses GPG signature checking, which is outside Go's certified FIPS module boundary.

### Elastic Agent in OpenTelemetry mode (EDOT) [ingest-limitations-edot]

When running {{agent}} in [OpenTelemetry mode](https://github.com/elastic/elastic-agent/blob/main/internal/pkg/otel/README.md) (EDOT), these additional limitations apply:

* **Azure integrations**: PKCS#12 (`.pfx`) client certificates are not supported for Azure Active Directory authentication. Use client secrets, workload identity, managed identity, or PEM-encoded certificate and key files instead.
* **Kafka metrics receiver**: SASL GSSAPI (Kerberos) is not supported. SASL SCRAM (SCRAM-SHA-256, SCRAM-SHA-512) is not FIPS-compliant. Use SASL/PLAIN over TLS or mTLS.
* **MongoDB receiver**: Not supported in FIPS mode.
* **MySQL receiver**: Not supported in FIPS mode.
* **Microsoft SQL Server receiver**: Not supported in FIPS mode.
* **Kerberos authentication for beat receivers**: Kerberos/GSSAPI authentication for beat receivers (Filebeat receiver, Metricbeat receiver) is not supported.
* **API key authentication extension**: Not FIPS-compliant. Uses a PBKDF2 implementation outside the certified FIPS module boundary when active.

If you are using a component not listed here and are unsure whether it is FIPS compliant, contact [Elastic Support](https://www.elastic.co/support).

### Elastic Integrations that are not FIPS compatible [ingest-limitations-integrations]

The following Elastic Integrations (Fleet-managed) use cryptographic implementations outside Go's certified FIPS module boundary for core functionality and **cannot** be used in FIPS environments. For EDOT-specific limitations, see [Elastic Agent in OpenTelemetry mode (EDOT)](#ingest-limitations-edot).

- [Azure Logs Integration (v2 preview)](integration-docs://reference/azure/events.md)
- [Azure Event Hub Input](integration-docs://reference/azure/eventhub.md)
- [Azure AI Foundry Integration](integration-docs://reference/azure_ai_foundry.md)
- [Azure App Service Integration](integration-docs://reference/azure_app_service.md)
- [Azure Application Insights Integration](integration-docs://reference/azure_application_insights.md)
- [Azure Billing Metrics Integration](integration-docs://reference/azure_billing.md)
- [Azure Functions Integration](integration-docs://reference/azure_functions.md)
- [Custom Azure Logs Integration](integration-docs://reference/azure_logs.md)
- [Azure Resource Metrics Integration](integration-docs://reference/azure_metrics.md)
- [Azure OpenAI Integration](integration-docs://reference/azure_openai.md)
- [SQL Input](integration-docs://reference/sql.md)
- [PostgreSQL Integration](integration-docs://reference/postgresql.md)
- [MongoDB Integration](integration-docs://reference/mongodb.md)
- [MySQL Integration](integration-docs://reference/mysql.md)
- [Microsoft SQL Server Integration](integration-docs://reference/microsoft_sqlserver.md)
- [Oracle Integration](integration-docs://reference/oracle.md)
- [Elastic Defend](integration-docs://reference/endpoint.md)
