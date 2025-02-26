---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/setup-upgrade.html
---

# Index compatibility [setup-upgrade]

::::{important}
:name: upgrade-pre-release

This documentation is for {{es}} 9.0.0-beta1, which is not yet released. You can upgrade from a previously released version to a pre-release build, if following a supported upgrade path. Upgrading from a pre-release build to any other build is not supported, and can result in errors or silent data loss. If you run a pre-release build for testing, discard the contents of the cluster before upgrading to another build of {{es}}.
::::


{{es}} clusters can usually be upgraded one node at a time so upgrading does not interrupt service. For upgrade instructions, refer to [Upgrading to Elastic 9.0.0-beta1](../deployment-or-cluster.md).

::::{admonition} Upgrade from 7.x
:class: important

To upgrade to 9.0.0-beta1 from 7.16 or an earlier version, **you must first upgrade to 8.17**, even if you opt to do a full-cluster restart instead of a rolling upgrade. This enables you to use the **Upgrade Assistant** to identify and resolve issues, reindex indices created before 7.0, and then perform a rolling upgrade. You must resolve all critical issues before proceeding with the upgrade. For instructions, refer to [Prepare to upgrade from 7.x](../deployment-or-cluster.md#prepare-to-upgrade).
::::



## Index compatibility [upgrade-index-compatibility]

{{es}} has full query and write support for indices created in the previous major version. If you have indices created in 6.x or earlier, you might use the [archive functionality](../deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md) to import them into newer {{es}} versions, or you must reindex or delete them before upgrading to 9.0.0-beta1. {{es}} nodes will fail to start if incompatible indices are present. Snapshots of 6.x or earlier indices can only restored using the [archive functionality](../deployment-or-cluster/reading-indices-from-older-elasticsearch-versions.md) to a 8.x cluster even if they were created by a 7.x cluster. The **Upgrade Assistant** in 8.17 identifies any indices that need to be reindexed or removed.


## REST API compatibility [upgrade-rest-api-compatibility]

[REST API compatibility](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/rest-apis/compatibility.md) is a per-request opt-in feature that can help REST clients mitigate non-compatible (breaking) changes to the REST API.


## FIPS Compliance and Java 17 [upgrade-fips-java17]

{{es}} 8.0+ requires Java 17 or later. {{es}} 8.13+ has been tested with [Bouncy Castle](https://www.bouncycastle.org/java.md)'s Java 17 [certified](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4616) FIPS implementation and is the recommended Java security provider when running {{es}} in FIPS 140-2 mode. Note - {{es}} does not ship with a FIPS certified security provider and requires explicit installation and configuration.

Alternatively, consider using {{ech}} in the [FedRAMP-certified GovCloud region](https://www.elastic.co/industries/public-sector/fedramp).
