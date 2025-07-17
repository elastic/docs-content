---
applies_to:
  deployment: ga
navigation_title: 
products:
  - id: apm
  - id: beats
  - id: elastic-agent
  - id: fleet
applies_to:
  stack: preview 9.1

---

# FIPS mode for Ingest tools [fips-ingest]

{{agent}}, {{fleet}}, {{filebeat}}, {{metricbeat}}, and {{apm-server}} binaries are built and can be configured to use FIPS 140-2 compliant cryptography.
Generally speaking FIPS 140-2 requirements can be summarized as:
- linking against a FIPS certified cryptographic library
- using only FIPS approved cryptographic functions
- ensuring that the configuration of the component is FIPS 140-2 compliant.


## Limitations [limitations-all]

### TLS 
Only FIPS 140-2 compliant TLS protocols, ciphers and curve types can be used. 
* The supported TLS versions are `TLS v1.2` and `TLS v1.3`. 
* The supported cipher suites are:
  * `TLS v1.2`: `ECDHE-RSA-AES-128-GCM-SHA256`, `ECDHE-RSA-AES-256-GCM-SHA384`, `ECDHE-ECDSA-AES-128-GCM-SHA256`, `ECDHE-ECDSA-AES-256-GCM-SHA384`
  * `TLS v1.3`: `TLS-AES-128-GCM-SHA256`, `TLS-AES-256-GCM-SHA384`
* The supported curve types are `P-256`, `P-384` and `P-521`.

Support for encrypted private keys is not available, as the cryptographic modules used for decrypting password protected keys are not FIPS validated. If an output or any other component with an SSL key that is password protected is configured, the components will fail to load the key. When running in FIPS mode, non-encrypted keys must be provided. 
Ensure to enforce security in your FIPS environments through other means, such as for example strict file permissions and access controls on the key file itself. 

These TLS related restrictions apply to all components listed. 

### General output and input limitations
The Kerberos protocol is not supported for any output or input, which also impacts the available `sasl.mechanism` for the Kafka output where only `PLAIN` is supported. 

This impacts [Filebeat](https://www.elastic.co/docs/reference/beats/filebeat/configuration-kerberos), [Metricbeat](https://www.elastic.co/docs/reference/beats/metricbeat/configuration-kerberos) and APM server, as well as output configurations for Elastic Agent with Fleet Server. 


### APM Server 
* The [Secrets Keystore](https://www.elastic.co/docs/solutions/observability/apm/secrets-keystore-for-secure-settings) is not supported. 

### Filebeat
* The [Secrets Keystore](https://www.elastic.co/docs/reference/beats/filebeat/keystore) is not supported. 
* The [Translate GUID Processor](https://www.elastic.co/docs/reference/beats/filebeat/processor-translate-guid) is not supported.
* The [Fingerprint Processor](https://www.elastic.co/docs/reference/beats/filebeat/fingerprint) does not support the md5 and sha1 method. 
* The [Community ID Network Flowhash Processor](https://www.elastic.co/docs/reference/beats/filebeat/community-id) is not supported. 
* The [Azure Module](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-module-azure) including the [Azure eventhub Input](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-azure-eventhub) and the [Office 365 Module (Beta)](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-module-o365) is currently not supported. The [Add Cloud Metadata Processor](https://www.elastic.co/docs/reference/beats/filebeat/add-cloud-metadata) does currently not support the Azure Virtual Machine provider. 
* The [GCP Pub/Sub Input](https://www.elastic.co/docs/reference/beats/filebeat/filebeat-input-gcp-pubsub) is not supported for now. 

### Metricbeat
* The [Secrets Keystore](https://www.elastic.co/docs/reference/beats/metricbeat/keystore) is not supported. 
* The [Translate GUID Processor](https://www.elastic.co/docs/reference/beats/metricbeat/processor-translate-guid) is not supported.
* The [Fingerprint Processor](https://www.elastic.co/docs/reference/beats/metricbeat/fingerprint) does not support the md5 and sha1 method. 
* The [Community ID Network Flowhash Processor](https://www.elastic.co/docs/reference/beats/metricbeat/community-id) is not supported. 
* The [Azure Module](https://www.elastic.co/docs/reference/beats/metricbeat/metricbeat-module-azure) is currently not supported. The [Add Cloud Metadata Processor](https://www.elastic.co/docs/reference/beats/metricbeat/add-cloud-metadata) does currently not support the Azure Virtual Machine provider. 
* The [Beta KVM Module](https://www.elastic.co/docs/reference/beats/metricbeat/metricbeat-module-kvm) is not yet supported.
* The [Mongo DB Module](http://elastic.co/docs/reference/beats/metricbeat/metricbeat-module-mongodb) is not supported. 
* The [MySQL](https://www.elastic.co/docs/reference/beats/metricbeat/metricbeat-module-mysql), [PostgreSQL](https://www.elastic.co/docs/reference/beats/metricbeat/metricbeat-module-postgresql), [MSSQL](https://www.elastic.co/docs/reference/beats/metricbeat/metricbeat-module-mssql) and [SQL](https://www.elastic.co/docs/reference/beats/metricbeat/metricbeat-module-sql) Modules are not supported. 
* The [Oracle Module](https://www.elastic.co/docs/reference/beats/metricbeat/metricbeat-module-oracle) is not supported. 

### Elastic Agent and Fleet Server
When using Elastic Agent and Fleet Server, the same restrictions as listed above for metricbeat and filebeat modules, inputs and processors apply to the respective Integrations. 
Additionally, following limitations apply:
* The [Prometheus Receiver](https://www.elastic.co/docs/reference/integrations/prometheus) is not supported. 
* Running the Elastic Agent in [OpenTelemetry mode](https://github.com/elastic/elastic-agent/blob/main/internal/pkg/otel/README.md) is not yet supported. 
