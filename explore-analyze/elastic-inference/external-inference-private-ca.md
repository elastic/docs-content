---
navigation_title: Use a private CA
description: Connect external inference endpoints to model providers that use a private or internal certificate authority by adding the CA to the Elasticsearch JVM trust store.
applies_to:
  deployment:
    self: ga
    ece: ga
    eck: ga
products:
  - id: elasticsearch
---

# Use a private certificate authority with external {{infer}} endpoints [inference-private-ca]

If your model provider presents a TLS certificate signed by a private or internal certificate authority (CA), {{es}} rejects the connection. Because {{es}} sends a test request when you create an endpoint, the error appears as soon as you try to save it:

```txt
PKIX path building failed: sun.security.provider.certpath.SunCertPathBuilderException: unable to find valid certification path to requested target
```

{{es}} sends requests to external {{infer}} services through the default JVM trust store. Unlike {{kib}} connectors, {{infer}} endpoints have no per-endpoint SSL settings, and you can't turn off certificate verification. To fix the error, add your CA certificate to the trust store that the {{es}} JVM uses.

:::{note}
The `xpack.inference.elastic.http.ssl.*` settings apply only to the Elastic {{infer-cap}} Service (EIS). They have no effect on external {{infer}} services.
:::

Before you start, keep the following in mind:

- The trust store applies to the whole node. Every outbound TLS connection that uses the default JVM trust store trusts your CA, not only {{infer}} endpoints.
- Add the CA on every node in the cluster. Any node can send {{infer}} requests, so a missing CA on one node causes intermittent failures.
- The JVM reads the trust store at startup, so you need to restart each node after you change it.
- Trusting the CA doesn't relax hostname verification. The server certificate must still include a subject alternative name (SAN) that matches the host in the endpoint `url`.

## Add your CA to the {{es}} trust store [inference-private-ca-add]

:::::{applies-switch}

::::{applies-item} deployment: { self: ga }
Create a dedicated trust store that contains the default public CAs plus your own CA, then point the JVM at it.

:::{warning}
The custom trust store replaces the default JVM trust store. Start from a copy of the bundled JDK's `cacerts` file, as shown in the following steps. A trust store that contains only your CA breaks every other TLS connection the node makes, such as connections to snapshot repositories and EIS.
:::

1. Copy the bundled JDK trust store into a new PKCS#12 file in your {{es}} configuration directory:

    ```sh
    $ES_HOME/jdk/bin/keytool -importkeystore \
      -srckeystore $ES_HOME/jdk/lib/security/cacerts \
      -srcstorepass changeit \
      -destkeystore $ES_PATH_CONF/inference-truststore.p12 \
      -deststoretype PKCS12 \
      -deststorepass <TRUSTSTORE_PASSWORD>
    ```

1. Import your CA certificate into the new trust store:

    ```sh
    $ES_HOME/jdk/bin/keytool -importcert -noprompt \
      -alias my-internal-ca \
      -file /path/to/ca.crt \
      -keystore $ES_PATH_CONF/inference-truststore.p12 \
      -storepass <TRUSTSTORE_PASSWORD>
    ```

1. Create a file named `inference-truststore.options` in the `jvm.options.d` directory of your {{es}} configuration directory, and use absolute paths:

    ```txt
    -Djavax.net.ssl.trustStore=/path/to/config/inference-truststore.p12
    -Djavax.net.ssl.trustStorePassword=<TRUSTSTORE_PASSWORD>
    -Djavax.net.ssl.trustStoreType=PKCS12
    ```

    For more information, refer to [JVM settings](elasticsearch://reference/elasticsearch/jvm-settings.md).

1. Make sure the `elasticsearch` user can read the trust store file.
1. Repeat these steps on every node, then restart each node.

Using a separate trust store, rather than importing your CA into the bundled `cacerts` file directly, means your change survives upgrades. Each {{es}} upgrade ships a new JDK that replaces the bundled `cacerts` file.

:::{tip}
If you run {{es}} in Docker, you can instead build a custom image that adds your CA to the operating system trust anchors. In the official images, the JDK `cacerts` file links to the operating system trust bundle, so the JVM picks up the change:

```dockerfile subs=true
FROM docker.elastic.co/elasticsearch/elasticsearch:{{version.stack}}
USER root
COPY ca.crt /etc/pki/ca-trust/source/anchors/my-internal-ca.crt
RUN update-ca-trust extract
USER elasticsearch
```

For `-wolfi` images, use `update-ca-certificates` instead of `update-ca-trust extract`.
:::
::::

::::{applies-item} deployment: { ece: ga }
Upload a custom JVM trust store as a bundle and add it to your deployment. For the steps, refer to [Add a custom JVM trust store bundle](/deploy-manage/plugins-and-custom-configuration-files/cloud-enterprise/add-custom-bundles-plugins.md#ece-add-custom-bundle-example-cacerts).
::::

::::{applies-item} deployment: { eck: ga }
Store a custom JVM trust store in a Kubernetes secret, mount it into the {{es}} Pods, and point the JVM at it with the `ES_JAVA_OPTS` environment variable. For an example, refer to [Use S3-compatible services](/deploy-manage/tools/snapshot-and-restore/cloud-on-k8s.md#k8s-s3-compatible). The same steps apply to {{infer}} endpoints.
::::

:::::
