---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/fips-140-compliance.html
  - https://www.elastic.co/guide/en/kibana/current/xpack-security-fips-140-2.html
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
  - id: kibana
  - id: elastic-agent
  - id: beats
  - id: fleet
  - id: apm
---

# FIPS 140-2 compliance

The Federal Information Processing Standard (FIPS) Publication 140-2, (FIPS PUB 140-2), titled "Security Requirements for Cryptographic Modules" is a U.S. government computer security standard used to approve cryptographic modules.
- [{{es}}](/deploy-manage/security/fips-es.md) offers a FIPS 140-2 compliant mode and as such can run in a FIPS 140-2 configured JVM.
- [{{kib}}](/deploy-manage/security/fips-kib.md) offers a FIPS 140-2 compliant mode and as such can run in a Node.js environment configured with a FIPS 140-2 compliant OpenSSL3 provider.
- Some [Ingest tools](/deploy-manage/security/fips-ingest.md), including {{agent}}, {{fleet}}, {{filebeat}}, {{metricbeat}}, and {{apm-server}}, are available as FIPS compatible binaries and can be configured to use FIPS 140-2 compliant cryptography.

:::{note}
If you are running {{es}} through {{eck}}, refer to [ECK FIPS compatibility](/deploy-manage/deploy/cloud-on-k8s/deploy-fips-compatible-version-of-eck.md).

FIPS compliance is not officially supported in {{ece}} (ECE). While ECE may function on FIPS-enabled systems, this configuration has not been validated through our testing processes and is not recommended for production environments.
:::

