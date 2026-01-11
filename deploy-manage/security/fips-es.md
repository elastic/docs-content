---
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---

# FIPS compliance for {{es}} [fips-elasticsearch]

{{es}} supports both FIPS 140-2 and FIPS 140-3 compliant modes.

:::{important}
The JVM bundled with {{es}} is not configured for FIPS. You must configure an external JDK with a FIPS certified Java Security Provider. Refer to the {{es}} [JVM support matrix](https://www.elastic.co/support/matrix#matrix_jvm) for supported JVM configurations. See [subscriptions](https://www.elastic.co/subscriptions) for required licensing.
:::

Compliance with FIPS 140-2 or FIPS 140-3 requires using only FIPS approved / NIST recommended cryptographic algorithms. Generally this can be done by the following:

* Installation and configuration of a FIPS certified Java security provider.
* Ensuring the configuration of {{es}} is FIPS compliant as documented below.
* Setting `xpack.security.fips_mode.enabled` to `true` in [`elasticsearch.yml`](/deploy-manage/stack-settings.md). Note - this setting alone is not sufficient to be compliant with FIPS.


:::{note}
If you are running {{es}} through {{eck}}, refer to [ECK FIPS compatibility](/deploy-manage/deploy/cloud-on-k8s/deploy-fips-compatible-version-of-eck.md).
:::

## Configuring {{es}} for FIPS [_configuring_es_for_fips_140_2]

Detailed instructions for the configuration required for FIPS compliance is beyond the scope of this document. It is the responsibility of the user to ensure compliance with FIPS 140-2 or FIPS 140-3. {{es}} has been tested with specific configurations described below. However, there are other configurations possible to achieve compliance.

Here is a high-level overview of the required configuration:

* Use an externally installed Java installation. The JVM bundled with {{es}} is not configured for FIPS.
* Install a FIPS certified security provider .jar file(s) in {{es}}'s `lib` directory.
* Configure Java to use a FIPS certified security provider ([see below](#java-security-provider)).
* Configure {{es}}'s security manager to allow use of the FIPS certified provider ([see below](#java-security-manager)).
* Ensure the keystore and truststore are configured correctly ([see below](#keystore-fips-password)).
* Ensure the TLS settings are configured correctly ([see below](#fips-tls)).
* Ensure the password hashing settings are configured correctly ([see below](#fips-stored-password-hashing)).
* Ensure the cached password hashing settings are configured correctly ([see below](#fips-cached-password-hashing)).
* Configure `elasticsearch.yml` to use FIPS mode, see ([below](#configuring-es-yml)).
* Verify the security provider is installed and configured correctly ([see below](#verify-security-provider)).
* Review the upgrade considerations ([see below](#fips-upgrade-considerations)) and limitations ([see below](#fips-limitations)).


### Java security provider [java-security-provider]

Detailed instructions for installation and configuration of a FIPS certified Java security provider is beyond the scope of this document. Specifically, a FIPS certified [JCA](https://docs.oracle.com/en/java/javase/17/security/java-cryptography-architecture-jca-reference-guide.html) and [JSSE](https://docs.oracle.com/en/java/javase/17/security/java-secure-socket-extension-jsse-reference-guide.html) implementation is required so that the JVM uses FIPS validated implementations of NIST recommended cryptographic algorithms.

{{es}} has been tested with [Bouncy Castle](https://www.bouncycastle.org/fips-java) FIPS libraries. The required libraries depend on whether you are configuring for FIPS 140-2 or FIPS 140-3 compliance:

**For FIPS 140-2 compliance:**
* [bc-fips 1.0.2.6](https://repo1.maven.org/maven2/org/bouncycastle/bc-fips/1.0.2.6/bc-fips-1.0.2.6.jar)
* [bctls-fips 1.0.19](https://repo1.maven.org/maven2/org/bouncycastle/bctls-fips/1.0.19/bctls-fips-1.0.19.jar)

**For FIPS 140-3 compliance:**
* [bc-fips 2.0.1](https://repo1.maven.org/maven2/org/bouncycastle/bc-fips/2.0.1/bc-fips-2.0.1.jar)
* [bctls-fips 2.0.22](https://repo1.maven.org/maven2/org/bouncycastle/bctls-fips/2.0.22/bctls-fips-2.0.22.jar)
* [bcutil-fips 2.0.5](https://repo1.maven.org/maven2/org/bouncycastle/bcutil-fips/2.0.5/bcutil-fips-2.0.5.jar)

:::{note}
FIPS 140-3 requires an additional library (`bcutil-fips`) that is not needed for FIPS 140-2.
:::

See the {{es}} [JVM support matrix](https://www.elastic.co/support/matrix#matrix_jvm) for details on which combinations of JVM and security provider are supported in FIPS mode. {{es}} does not ship with a FIPS certified provider. It is the responsibility of the user to install and configure the security provider to ensure FIPS compliance. Using a FIPS certified provider will ensure that only approved cryptographic algorithms are used.

To configure {{es}} to use additional security provider(s) configure {{es}}'s [JVM property](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-options) `java.security.properties` to point to a file ([example](https://raw.githubusercontent.com/elastic/elasticsearch/main/build-tools-internal/src/main/resources/fips_java.security)) in {{es}}'s `config` directory. Ensure the FIPS certified security provider is configured with the lowest order. This file should contain the necessary configuration to instruct Java to use the FIPS certified security provider.


### Java security manager [java-security-manager]

All code running in {{es}} is subject to the security restrictions enforced by the Java security manager. The security provider you have installed and configured may require additional permissions in order to function correctly. You can grant these permissions by providing your own [Java security policy](https://docs.oracle.com/javase/8/docs/technotes/guides/security/PolicyFiles.md#FileSyntax)

To configure {{es}}'s security manager configure the JVM property `java.security.policy` to point a file ([example](https://raw.githubusercontent.com/elastic/elasticsearch/main/build-tools-internal/src/main/resources/fips_java.policy))in {{es}}'s `config` directory with the desired permissions. This file should contain the necessary configuration for the Java security manager to grant the required permissions needed by the security provider.


### {{es}} Keystore [keystore-fips-password]

FIPS (via NIST Special Publication 800-132) dictates that encryption keys should at least have an effective strength of 112 bits. As such, the {{es}} keystore that stores the node's [secure settings](/deploy-manage/security/secure-settings.md) needs to be password protected with a password that satisfies this requirement. This means that the password needs to be 14 bytes long which is equivalent to a 14 character ASCII encoded password, or a 7 character UTF-8 encoded password. You can use the [elasticsearch-keystore passwd](elasticsearch://reference/elasticsearch/command-line-tools/elasticsearch-keystore.md) subcommand to change or set the password of an existing keystore. Note that when the keystore is password-protected, you must supply the password each time {{es}} starts.


### TLS [fips-tls]

SSLv2 and SSLv3 are not allowed by FIPS, so `SSLv2Hello` and `SSLv3` cannot be used for [`ssl.supported_protocols`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ssl-tls-settings).

::::{note}
The use of TLS ciphers is mainly governed by the relevant crypto module (the FIPS Approved Security Provider that your JVM uses). All the ciphers that are configured by default in {{es}} are FIPS compliant and as such can be used in a FIPS-configured JVM. See [`ssl.cipher_suites`](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ssl-tls-settings).
::::



### TLS keystores and keys [_tls_keystores_and_keys]

Keystores can be used in a number of [General TLS settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ssl-tls-settings) in order to conveniently store key and trust material. Neither `JKS`, nor `PKCS#12` keystores can be used in a FIPS-configured JVM. Avoid using these types of keystores. Your FIPS provider may provide a compliant keystore implementation that can be used, or you can use PEM encoded files. To use PEM encoded key material, you can use the relevant `\*.key` and `*.certificate` configuration options, and for trust material you can use `*.certificate_authorities`.

FIPS compliance dictates that the length of the public keys used for TLS must correspond to the strength of the symmetric key algorithm in use in TLS. Depending on the value of `ssl.cipher_suites` that you select to use, the TLS keys must have corresponding length according to the following table:

#### Comparable key strength [comparable-key-strength]

| Symmetric Key Algorithm | RSA key Length | ECC key length |
| --- | --- | --- |
| `3DES` | 2048 | 224-255 |
| `AES-128` | 3072 | 256-383 |
| `AES-256` | 15630 | 512+ |


### Stored password hashing [fips-stored-password-hashing]

While {{es}} offers a number of algorithms for securely hashing credentials on disk, only the `PBKDF2` based family of algorithms is compliant with FIPS for stored password hashing. However, since `PBKDF2` is essentially a key derivation function, your JVM security provider may enforce a [112-bit key strength requirement](#keystore-fips-password). Although FIPS does not mandate user password standards, this requirement may affect password hashing in {{es}}. To comply with this requirement, while allowing you to use passwords that satisfy your security policy, {{es}} offers [pbkdf2_stretch](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#hashing-settings) which is the suggested hashing algorithm when running {{es}} in FIPS environments. `pbkdf2_stretch` performs a single round of SHA-512 on the user password before passing it to the `PBKDF2` implementation.

::::{note}
You can still use one of the plain `pbkdf2` options instead of `pbkdf2_stretch` if you have external policies and tools that can ensure all user passwords for the reserved, native, and file realms are longer than 14 bytes.
::::


You must set the `xpack.security.authc.password_hashing.algorithm` setting to one of the available `pbkdf_stretch_*` values. When FIPS mode is enabled, the default value for `xpack.security.authc.password_hashing.algorithm` is `pbkdf2_stretch`. See [User cache and password hash algorithms](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#hashing-settings).

Password hashing configuration changes are not retroactive so the stored hashed credentials of existing users of the reserved, native, and file realms are not updated on disk. To ensure FIPS compliance, recreate users or change their password using the [elasticsearch-user](elasticsearch://reference/elasticsearch/command-line-tools/users-command.md) CLI tool for the file realm and the [create users](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-user) and [change password](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-change-password) APIs for the native and reserved realms. Other types of realms are not affected and do not require any changes.


### Cached password hashing [fips-cached-password-hashing]

`ssha256` (salted `sha256`) is recommended for cache hashing. Though `PBKDF2` is compliant with FIPS, it is — by design — slow, and thus not generally suitable as a cache hashing algorithm. Cached credentials are never stored on disk, and salted `sha256` provides an adequate level of security for in-memory credential hashing, without imposing prohibitive performance overhead. You *may* use `PBKDF2`, however you should carefully assess performance impact first. Depending on your deployment, the overhead of `PBKDF2` could undo most of the performance gain of using a cache.

Either set all `cache.hash_algo` settings to `ssha256` or leave them undefined, since `ssha256` is the default value for all `cache.hash_algo` settings. See [User cache and password hash algorithms](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#hashing-settings).

The user cache will be emptied upon node restart, so any existing hashes using non-compliant algorithms will be discarded and the new ones will be created using the algorithm you have selected.


### Configure {{es}} elasticsearch.yml [configuring-es-yml]

* Set `xpack.security.fips_mode.enabled` to `true` in [`elasticsearch.yml`](/deploy-manage/stack-settings.md). This setting is used to ensure to configure some internal configuration to be FIPS compliant and provides some additional verification.
* Set `xpack.security.autoconfiguration.enabled` to `false`. This will disable the automatic configuration of the security settings. Users must ensure that the security settings are configured correctly for FIPS compliance. This is only applicable for new installations.
* Set `xpack.security.authc.password_hashing.algorithm` appropriately see [above](#fips-stored-password-hashing).
* Other relevant security settings. For example, TLS for the transport and HTTP interfaces. (not explicitly covered here or in the example below)
* Optional: Set `xpack.security.fips_mode.required_providers` in [`elasticsearch.yml`](/deploy-manage/stack-settings.md) to ensure the required security providers (8.13+). see [below](#verify-security-provider).

```yaml
xpack.security.fips_mode.enabled: true
xpack.security.autoconfiguration.enabled: false
xpack.security.fips_mode.required_providers: ["BCFIPS", "BCJSSE"]
xpack.security.authc.password_hashing.algorithm: "pbkdf2_stretch"
```


### Verify the security provider is installed [verify-security-provider]

To verify that the security provider is installed and in use, you can use any of the following steps:

* Verify the required security providers are configured with the lowest order in the file pointed to by `java.security.properties`. For example, `security.provider.1` is a lower order than `security.provider.2`
* Set `xpack.security.fips_mode.required_providers` in [`elasticsearch.yml`](/deploy-manage/stack-settings.md) to the list of required security providers. This setting is used to ensure that the correct security provider is installed and configured. (8.13+) If the security provider is not installed correctly, {{es}} will fail to start.

The `xpack.security.fips_mode.required_providers` setting supports two formats:

* **Name only**: `["BCFIPS", "BCJSSE"]` — verifies that the named providers are installed.
* **Name and version**: `["BCFIPS:2*", "BCJSSE:2*"]` — verifies both the provider name and version. The version supports simple wildcard patterns (for example, `2*` matches any version starting with `2`).

The name-and-version format is useful when you need to verify that a specific version of the security provider is in use, such as distinguishing between Bouncy Castle 1.x (FIPS 140-2) and 2.x (FIPS 140-3) libraries.


## Upgrade considerations [fips-upgrade-considerations]

{{es}} 8.0+ requires Java 17 or later. {{es}} has been tested with [Bouncy Castle](https://www.bouncycastle.org/java.html)'s FIPS implementations and is the recommended Java security provider when running {{es}} in FIPS mode:

* For FIPS 140-2: Bouncy Castle 1.x libraries ([certified](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4616))
* For FIPS 140-3: Bouncy Castle 2.x libraries ([certified](https://csrc.nist.gov/projects/cryptographic-module-validation-program/certificate/4743))

Note that {{es}} does not ship with a FIPS certified security provider and requires explicit installation and configuration.

Alternatively, consider using {{ech}} in the [FedRAMP-certified GovCloud region](https://www.elastic.co/industries/public-sector/fedramp).

:::{important}
Some encryption algorithms may no longer be available by default in updated FIPS security providers. Notably, Triple DES and PKCS1.5 RSA are now discouraged and [Bouncy Castle](https://www.bouncycastle.org/fips-java) now requires explicit configuration to continue using these algorithms.
:::


If you plan to upgrade your existing cluster to a version that can be run in a FIPS-configured JVM, we recommend to first perform a rolling upgrade to the new version in your existing JVM and perform all necessary configuration changes in preparation for running in FIPS mode. You can then perform a rolling restart of the nodes, starting each node in a FIPS-configured JVM. During the restart, {{es}}:

* Upgrades [secure settings](/deploy-manage/security/secure-settings.md) to the latest, compliant format. A FIPS-configured JVM cannot load previous format versions. If your keystore is not password-protected, you must manually set a password. See [{{es}} Keystore](#keystore-fips-password).
* Upgrades self-generated trial licenses to the latest FIPS compliant format.

If your [subscription](https://www.elastic.co/subscriptions) already supports FIPS mode, you can elect to perform a rolling upgrade while at the same time running each upgraded node in a FIPS-configured JVM. In this case, you would need to also manually regenerate your `elasticsearch.keystore` and migrate all secure settings to it, in addition to the necessary configuration changes outlined below, before starting each node.


## Limitations [fips-limitations]

Due to the limitations that FIPS compliance enforces, a small number of features are not available while running in FIPS mode. The list is as follows:

* Azure Classic Discovery Plugin
* The [`elasticsearch-certutil`](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md) tool. However, `elasticsearch-certutil` can very well be used in a non-FIPS configured JVM (pointing `ES_JAVA_HOME` environment variable to a different java installation) in order to generate the keys and certificates that can be later used in the FIPS-configured JVM.
* The SQL CLI client cannot run in a FIPS-configured JVM while using TLS for transport security or PKI for client authentication.

