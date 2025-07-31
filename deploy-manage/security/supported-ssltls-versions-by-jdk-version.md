---
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/jdk-tls-versions.html
applies_to:
  deployment:
    self: all
products:
  - id: elasticsearch
---

# Supported SSL/TLS versions by JDK version [jdk-tls-versions]

{{es}} relies on your JDK’s implementation of SSL and TLS.

Different JDK versions support different versions of SSL, and this may affect how {{es}} operates.

::::{note}
This support applies when running on the default JSSE provider in the JDK. JVMs that are configured to use a [FIPS 140-2](fips.md) security provider might have a custom TLS implementation, which might support TLS protocol versions that differ from this list.

Check your security provider’s release notes for information on TLS support.

::::


`SSLv3`
:   SSL v3 is supported on all {{es}} [compatible JDKs](../deploy/self-managed/installing-elasticsearch.md#jvm-version) but is disabled by default. See [Enabling additional SSL/TLS versions on your JDK](#jdk-enable-tls-protocol).

`TLSv1`
:   TLS v1.0 is supported on all {{es}} [compatible JDKs](../deploy/self-managed/installing-elasticsearch.md#jvm-version) but is disabled by default. See [Enabling additional SSL/TLS versions on your JDK](#jdk-enable-tls-protocol).

`TLSv1.1`
:   TLS v1.1 is supported on all {{es}} [compatible JDKs](../deploy/self-managed/installing-elasticsearch.md#jvm-version) but is disabled by default. See [Enabling additional SSL/TLS versions on your JDK](#jdk-enable-tls-protocol).

`TLSv1.2`
:   TLS v1.2 is supported on all {{es}} [compatible JDKs](../deploy/self-managed/installing-elasticsearch.md#jvm-version). It is enabled by default on all JDKs that are supported by {{es}}, including the bundled JDK.

`TLSv1.3`
:   TLS v1.3 is supported on all {{es}} [compatible JDKs](../deploy/self-managed/installing-elasticsearch.md#jvm-version). It is enabled by default on all JDKs that are supported by {{es}}, including the bundled JDK.


## Enabling additional SSL/TLS versions on your JDK [jdk-enable-tls-protocol]

The set of supported SSL/TLS versions for a JDK is controlled by a java security properties file that is installed as part of your JDK.

This configuration file lists the SSL/TLS algorithms that are disabled in that JDK. Complete these steps to remove a TLS version from that list and use it in your JDK.

1. Locate the configuration file for your JDK.
2. Copy the `jdk.tls.disabledAlgorithms` setting from that file, and add it to a custom configuration file within the {{es}} configuration directory.
3. In the custom configuration file, remove the value for the TLS version you want to use from `jdk.tls.disabledAlgorithms`.
4. Configure {{es}} to pass a custom system property to the JDK so that your custom configuration file is used.

### Locate the configuration file for your JDK [_locate_the_configuration_file_for_your_jdk]

For the {{es}} **bundled JDK**, the configuration file is in a sub directory of the {{es}} home directory (`$ES_HOME`):

* Linux: `$ES_HOME/jdk/conf/security/java.security`
* Windows: `$ES_HOME/jdk/conf/security/java.security`
* macOS:`$ES_HOME/jdk.app/Contents/Home/conf/security/java.security`

For **JDK11 or later**, the configuration file is within the `conf/security` directory of the Java installation. If `$JAVA_HOME` points to the home directory of the JDK that you use to run {{es}}, then the configuration file will be in:

* `$JAVA_HOME/conf/security/java.security`


### Copy the disabledAlgorithms setting [_copy_the_disabledalgorithms_setting]

Within the JDK configuration file is a line that starts with `jdk.tls.disabledAlgorithms=`. This setting controls which protocols and algorithms are *disabled* in your JDK. The value of that setting will typically span multiple lines.

For example, in OpenJDK 21 the setting is:

```text
jdk.tls.disabledAlgorithms=SSLv3, TLSv1, TLSv1.1, DTLSv1.0, RC4, DES, \
    MD5withRSA, DH keySize < 1024, EC keySize < 224, 3DES_EDE_CBC, anon, NULL, \
    ECDH
```

Create a new file in your in your {{es}} configuration directory named `es.java.security`. Copy the `jdk.tls.disabledAlgorithms` setting from the JDK’s default configuration file into `es.java.security`. You do not need to copy any other settings.


### Enable required TLS versions [_enable_required_tls_versions]

Edit the `es.java.security` file in your {{es}} configuration directory, and modify the `jdk.tls.disabledAlgorithms` setting so that any SSL or TLS versions that you wish to use are no longer listed.

For example, to enable TLSv1.1 on OpenJDK 21 (which uses the `jdk.tls.disabledAlgorithms` settings shown previously), the `es.java.security` file would contain the previously disabled TLS algorithms *except* `TLSv1.1`:

```text
jdk.tls.disabledAlgorithms=SSLv3, TLSv1, DTLSv1.0, RC4, DES, \
    MD5withRSA, DH keySize < 1024, EC keySize < 224, 3DES_EDE_CBC, anon, NULL, \
    ECDH
```


### Enable your custom security configuration [_enable_your_custom_security_configuration]

To enable your custom security policy, add a file in the [`jvm.options.d`](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-options) directory within your {{es}} configuration directory.

To enable your custom security policy, create a file named `java.security.options` within the [jvm.options.d](elasticsearch://reference/elasticsearch/jvm-settings.md#set-jvm-options) directory of your {{es}} configuration directory, with this content:

```text
-Djava.security.properties=/path/to/your/es.java.security
```



## Enabling TLS versions in {{es}} [_enabling_tls_versions_in_es]

SSL/TLS versions can be enabled and disabled within {{es}} via the [`ssl.supported_protocols` settings](elasticsearch://reference/elasticsearch/configuration-reference/security-settings.md#ssl-tls-settings).

{{es}} will only support the TLS versions that are enabled by the underlying JDK. If you configure `ssl.supported_protocols` to include a TLS version that is not enabled in your JDK, then it will be silently ignored.

Similarly, a TLS version that is enabled in your JDK, will not be used unless it is configured as one of the `ssl.supported_protocols` in {{es}}.
