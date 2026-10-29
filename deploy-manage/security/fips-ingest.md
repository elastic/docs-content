---
products:
  - id: apm
  - id: elastic-agent
  - id: beats
  - id: fleet-server
applies_to:
  stack: preview 9.1, ga 9.3+
---

# FIPS mode for Ingest tools [fips-ingest]

{{agent}}, {{fleet-server}}, {{filebeat}}, {{metricbeat}}, and {{apm-server}} FIPS binaries are built and configured to use FIPS 140 validated cryptography. FIPS mode for these tools was in technical preview in 9.1 and 9.2 and is generally available from 9.3. The FIPS standard and the platforms covered depend on the product and version:

| Ingest tool | FIPS 140-2 | FIPS 140-3 |
|---|---|---|
| {{agent}} and {{fleet-server}} | 9.1–9.5 on Linux | 9.6+ on Linux and Windows |
| {{filebeat}} and {{metricbeat}} | 9.1–9.2, 9.3.0–9.3.7, and 9.4.0–9.4.3 on Linux | 9.3.8+, 9.4.4+, and 9.5+ on Linux<br><br>9.6+ on Linux and Windows |
| {{apm-server}} | 9.1–9.2, 9.3.0–9.3.7, and 9.4.0–9.4.3 on Linux | 9.3.8+, 9.4.4+, and 9.5+ on Linux |

{{auditbeat}} FIPS binaries are also available and follow the same versions and platforms as {{filebeat}} and {{metricbeat}}. This page doesn't document {{auditbeat}}-specific limitations.

All FIPS 140-3 binaries listed in the table use the [Go Cryptographic Module](https://go.dev/doc/security/fips140), the native FIPS 140-3 module in the Go standard library, which is validated under the Cryptographic Module Validation Program (CMVP). Specific components and configurations that fall outside the validated module boundary are documented in the [Limitations](#ingest-limitations-all) section.

{applies_to}`stack: ga 9.6+` {{agent}}, including the bundled {{fleet-server}}, is FIPS 140-3 compliant. In 9.6, they use Go Cryptographic Module v1.0.0 (CMVP Certificate [#5247](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/5247)).

## FIPS-compatible binaries and configuration [fips-binaries]

FIPS compatible binaries for {{agent}}, {{fleet-server}}, {{filebeat}}, {{metricbeat}}, and {{apm-server}} are available for [download](https://www.elastic.co/downloads). Look for the `Linux 64-bit (FIPS)` or `Linux aarch64 (FIPS)` platform option on the product download pages for {{agent}} (which includes {{fleet-server}}), {{filebeat}}, and {{metricbeat}}. Look for the `Linux x86_64 (FIPS)` or `Linux aarch64 (FIPS)` platform option on the {{apm-server}} download page.

{applies_to}`stack: ga 9.6+` FIPS binaries for Windows are also available for {{agent}}, {{filebeat}}, and {{metricbeat}}. Look for the Windows FIPS platform options on the product download pages. The {{agent}} Windows FIPS binary includes {{fleet-server}}, so you can use it to run {{fleet-server}} on Windows in FIPS mode.

:::{important}
The default configurations provided in the binaries are FIPS compatible. Be sure to check and understand the implications of changing default configurations.
:::

## Limitations [ingest-limitations-all]

### TLS [ingest-limitations-tls]

Only FIPS-approved TLS protocols, cipher suites, and curve types are allowed. For FIPS 140-3 binaries, these are the algorithms approved in the CMVP validation of the Go Cryptographic Module, such as [CMVP Certificate #5247](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/5247). The certificate number changes when Go revalidates the module.
* The supported TLS versions are `TLS v1.2` and `TLS v1.3`.
* The supported cipher suites are:
  * `TLS v1.2`: `ECDHE-RSA-AES-128-GCM-SHA256`, `ECDHE-RSA-AES-256-GCM-SHA384`, `ECDHE-ECDSA-AES-128-GCM-SHA256`, `ECDHE-ECDSA-AES-256-GCM-SHA384`
  * `TLS v1.3`: `TLS-AES-128-GCM-SHA256`, `TLS-AES-256-GCM-SHA384`
* The supported curve types are `P-256`, `P-384` and `P-521`.
* The minimum key length is 2048 bits for RSA keys. EC key size is determined by the curve in use.

Support for encrypted private keys is not available, as the cryptographic modules used for decrypting password protected keys are not FIPS validated. If an output or any other component with an SSL key that is password protected is configured, the components will fail to load the key. When running in FIPS mode, you must provide non-encrypted keys.
Be sure to enforce security in your FIPS environments through other means, such as strict file permissions and access controls on the key file itself, for example.

These TLS related restrictions apply to {{agent}}, {{fleet-server}}, {{filebeat}}, {{metricbeat}}, and {{apm-server}}.

### General output and input limitations (Kerberos protocol) [ingest-inputoutput-limitations]

The Kerberos protocol is not supported for any output or input. This impacts [Filebeat](beats://reference/filebeat/configuration-kerberos.md), [Metricbeat](beats://reference/metricbeat/configuration-kerberos.md) and {{apm-server}}, as well as output configurations for {{agent}} with {{fleet-server}}.

This also limits the available `sasl.mechanism` values for Kafka connections, including the Kafka output, the {{filebeat}} Kafka input, and the {{metricbeat}} Kafka module:

* {applies_to}`stack: ga 9.6+` `PLAIN`, `SCRAM-SHA-256`, and `SCRAM-SHA-512` are supported.
* {applies_to}`stack: preview 9.1-9.2, ga 9.3-9.5` Only `PLAIN` is supported.


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

### {{agent}} and {{fleet-server}} [ingest-limitations-agent]

When you use {{agent}} and {{fleet-server}}, these limitations apply:
* Some Elastic Integrations are not FIPS compatible, as they depend on functionality that is not supported for FIPS configuration. In general, when using {{agent}} and {{fleet-server}}, the same restrictions listed previously for {{metricbeat}} and {{filebeat}} modules, inputs, and processors apply.
* Agent upgrade artifact verification uses GPG signature checking, which is outside the validated FIPS module boundary.
* Browser Synthetics monitors are not supported in FIPS mode.
* {applies_to}`stack: ga 9.6+` Lightweight Synthetics monitors don't support NTLM authentication for HTTP monitors.
* {applies_to}`stack: preview 9.1-9.2, ga 9.3-9.5` Lightweight Synthetics monitors are not supported, because {{heartbeat}} is not included in the {{agent}} FIPS build.

#### {{agent}} configured as an OTel Collector [ingest-limitations-edot]

::::{applies-switch}

:::{applies-item} stack: ga 9.3+
When you run [{{agent}} configured as an OTel Collector](/reference/fleet/otel-agent.md), these additional limitations apply:

* **Azure integrations**: PKCS#12 (`.pfx`) client certificates are not supported for Azure Active Directory authentication. Use client secrets, workload identity, managed identity, or PEM-encoded certificate and key files instead.
* {applies_to}`stack: ga 9.4+` **Kafka metrics receiver**: SASL GSSAPI (Kerberos) is not supported. Use SASL/PLAIN or SASL/SCRAM over TLS, or mTLS. In 9.4.0 and 9.4.1, SASL/SCRAM uses cryptography outside the validated FIPS module boundary, so use SASL/PLAIN over TLS or mTLS instead.
* **Kafka receiver** and **Kafka exporter**: Not included in FIPS builds in 9.3, 9.4.0–9.4.8, and 9.5.0–9.5.4. Included starting in 9.4.9, 9.5.5, and 9.6.0. When included, SASL GSSAPI (Kerberos) is not supported. Use SASL/PLAIN or SASL/SCRAM over TLS, or mTLS.
* **Prometheus receiver**: Not included in FIPS builds.
* The following receivers are not supported in FIPS mode:
  * **MongoDB receiver**
  * **MySQL receiver**
  * **Microsoft SQL Server receiver**
* **Kerberos authentication for beat receivers**: Kerberos/GSSAPI authentication for beat receivers ({{filebeat}} receiver, {{metricbeat}} receiver) is not supported.
* **API key authentication extension**: Uses a PBKDF2 implementation outside the validated FIPS module boundary when active, so it is not supported in FIPS mode.

If you are using a component not listed here and are unsure whether it is supported in FIPS mode, contact [Elastic Support](https://www.elastic.co/support).
:::

:::{applies-item} stack: preview 9.1-9.2
Running [{{agent}} configured as an OTel Collector](/reference/fleet/otel-agent.md) is not supported in FIPS mode. This includes all receivers, such as the {{filebeat}} receiver, the {{metricbeat}} receiver, and the [Prometheus receiver](https://www.elastic.co/docs/reference/integrations/prometheus).
:::

::::

### Elastic Integrations that are not FIPS compatible [ingest-limitations-integrations]

The following {{fleet}}-managed Elastic Integrations use cryptographic implementations outside Go's validated FIPS module boundary for core functionality. These integrations cannot be used in FIPS environments, even if combined with other ingest tools that offer FIPS mode. 

For limitations that apply when {{agent}} is configured as an OTel Collector, refer to [{{agent}} configured as an OTel Collector](#ingest-limitations-edot).

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
