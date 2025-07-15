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
  stack: ga 9.1

---

# FIPS mode for Ingest tools [fips-ingest]

FIPS mode binaries are available for {{agent}}, {{fleet}}, {{filebeat}}, {{metricbeat}}, and {{apm-server}}.

Compliance with FIPS 140-2 requires using only FIPS approved/NIST recommended cryptographic algorithms. For {{agent}}, Fleet Server, the listed {{Beats}}, and APM Server, this can be summarized as:
- linking against a FIPS certified cryptographic library
- using only FIPS approved cryptographic functions
- ensuring that the configuration of the component is FIPS 140-2 compliant.


## FIPS mode for {{agent}}, {{fleet}}, {{filebeat}}, {{metricbeat}}, and {{apm-server}} artifacts [fips-ingest-all]

These limitations apply to all FIPS mode artifacts for Ingest: 

- Keystore functionality is disabled
- Kerberos is disabled by pulling in latest version of https://github.com/elastic/sarama and an error is returned when setting Kerberos configuration options
- Encrypted private key support is disabled
- Only fips compliant TLS options are accepted
- TranslateLDAPAttribute Processor is disabled
- For Kafka output, SCRAM SASL is disabled as it was using a custom pbkdf2 functionality
- flowhash/communityid is disabled 
- Azure Virtual Machine provider in the add_cloud_metadata processor is disabled: this would have pulled in several non-compliant golang.org/x/crypto functionality

In addition to limitations that apply to all FIPS mode ingest artifacts, be sure to check out changes for specific ingest tools.
- [FIPS mode for {{agent}}](#fips-agent)
- [FIPS mode for {{fleet}}](#fips-fleet)
- [FIPS mode for {{beats}}](#fips-beats)
- [FIPS mode for {{apm-server}}](#fips-apm-server)


### {{agent}} in FIPS mode [fips-agent]

These limitations apply to {{agent}} and {{beats}} in FIPS mode:

- Support for Prometheus receiver, Kafka receiver, and Kafka exporter is removed in OTel mode
- Some components introduce x/crypto dependencies into {{agent}} and cannot easily be removed. If you use service providers such as GCP, Azure, or MongoDB, you must deploy your {{agent}} in a FIPS environment in order to be compliant.

  These components include: 
  - github.com/elastic/beats/v7/metricbeat/module/mongodb
  - github.com/elastic/beats/v7/metricbeat/module/kvm/dommemstat
  - github.com/elastic/beats/v7/x-pack/filebeat/input/gcppubsub
  - github.com/elastic/beats/v7/libbeat/processors/translate_ldap_attribute (will be removed)
  - github.com/elastic/beats/v7/libbeat/processors/add_cloud_metadata
  - github.com/elastic/beats/v7/x-pack/filebeat/input/azureeventhub

  - x-pack/metricbeat/module/sql
  - x-pack/metricbeat/module/oracle
  - metricbeat/module/postgresql
  - metricbeat/module/mysql
  - metricbeat/module/mongodb

- See also [changes to all FIPS mode ingest artifacts](#fips-ingest-all).

### Fleet Server [fips-fleet]

- See also [changes to all FIPS mode ingest artifacts](#fips-ingest-all).


### FIPS compliance for {{metricbeat}}, {{filebeat}} [fips-beats]

#### {{filebeat}} in FIPS mode [fips-filebeat]

These limitations apply to {{filebeat}} in FIPS mode:

- flowhash/communityid is disabled for input netflow
- gcppubsub input is disabled
- azure-eventhub input and azure module are disabled:  this would have pulled in several non-compliant golang.org/x/crypto functionality
- o365audit input and o365 module are disabled: this would have pulled in several non-compliant golang.org/x/crypto functionality
- See also [changes to all FIPS mode ingest artifacts](#fips-ingest-all).

#### {{metricbeat}} in FIPS mode [fips-metricbeat]

These limitations apply to {{metricbeat}} in FIPS mode:

- kvm module is disabled: this would have pulled in several non-compliant golang.org/x/crypto functionality
- mongodb module is disabled: this would have pulled in several non-compliant golang.org/x/crypto functionality
- disable mysql, postgresql, oracle and sql module: this would have pulled in several non-compliant crypto usages as part of their dependencies
- azure module is disabled: this would have pulled in several non-compliant golang.org/x/crypto functionality
- mssql module is disabled: this would have pulled in several non-compliant golang.org/x/crypto functionality
- See also [changes to all FIPS mode ingest artifacts](#fips-ingest-all).

