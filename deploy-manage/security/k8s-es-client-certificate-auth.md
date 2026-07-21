---
navigation_title: Elasticsearch client certificate authentication
applies_to:
  deployment:
    eck: ga 3.5
products:
  - id: cloud-kubernetes
---

# Elasticsearch client certificate authentication on ECK [k8s-es-client-certificate-auth]

For how ECK secures HTTP traffic and manages TLS certificates, see [Manage TLS certificates on ECK](/deploy-manage/security/eck-tls.md).

You can configure {{es}} to require client certificates for HTTP authentication, enabling mutual TLS (mTLS) between clients and {{es}}. When enabled, clients must present a valid certificate signed by a trusted CA to communicate with {{es}}.

ECK automatically generates and manages client certificates for all {{stack}} components that connect to {{es}}: {{kib}}, {{apm-server}}, {{beats}}, {{ls}}, {{hosted-ems}}, Enterprise Search, {{agent}}, and {{fleet-server}}. Stack monitoring sidecars and the AutoOps agent are also configured automatically. Each component is issued a certificate by ECK; you can optionally supply a custom certificate instead.

:::{note}
This requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](/deploy-manage/license/manage-your-license-in-eck.md) for more details about managing licenses.
:::

## Enable client certificate authentication [k8s-enable-client-cert-auth]

To enable client certificate authentication on {{es}}, set `spec.http.tls.client.authentication` to `true`:

```yaml subs=true
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  nodeSets:
  - name: default
    count: 3
  http:
    tls:
      client:
        authentication: true
```

When client authentication is enabled, ECK does the following:

* Sets `xpack.security.http.ssl.client_authentication: required` in the {{es}} configuration.
* Automatically generates and manages client certificates for the ECK operator, {{kib}}, {{apm-server}}, {{beats}}, {{ls}}, {{hosted-ems}}, Enterprise Search, standalone and fleet-managed {{agents}}, stack monitoring sidecars ({{metricbeat}} and {{filebeat}}), and the AutoOps agent, configuring each to present its certificate when connecting to {{es}}.

:::{note}
* If you have manually set `xpack.security.http.ssl.client_authentication` in `spec.nodeSets[*].config`, that value takes precedence over the ECK-managed setting and the mTLS configuration may not apply as expected.
* {{fleet-server}} requires version 8.13.0 or later. If the version is below 8.13.0, ECK blocks pod reconciliation and sets the agent status to red with a warning event.
:::

:::{warning}
* {{ls}} versions 8.10–8.18 and 9.0 can crash on startup with some PKCS#8 private keys due to a JRuby runtime bug. This is fixed in {{ls}} 8.19 and 9.1+. If affected, delete the client certificate secret to force ECK to regenerate it.
* Enterprise Search can crash on startup with some PKCS#8 private keys due to a JRuby runtime bug. If affected, delete the client certificate secret to force ECK to regenerate it.
:::

## Use a custom client certificate [k8s-custom-client-cert]

ECK automatically issues a client certificate to each component. To use your own certificate instead, set `clientCertificateSecretName` in the component's `elasticsearchRef`.

The referenced secret must contain `tls.crt` and `tls.key` entries:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: my-custom-client-cert
type: kubernetes.io/tls
data:
  tls.crt: <base64-encoded certificate>
  tls.key: <base64-encoded private key>
```

:::{note}
* `clientCertificateSecretName` can only be used with a named `elasticsearchRef` (not with `secretName`).
* The secret must be in the same namespace as the resource that references it.
* All components are compatible with PKCS#8 private keys. If you supply a certificate in a different format, verify compatibility with both {{es}} and the individual component before use.
:::

### Kibana [k8s-kibana-custom-client-cert]

Set `clientCertificateSecretName` in the `elasticsearchRef` of the {{kib}} resource:

```yaml subs=true
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: quickstart
    clientCertificateSecretName: my-custom-client-cert
```

### APM Server [k8s-apm-custom-client-cert]

Set `clientCertificateSecretName` in the `elasticsearchRef` of the {{apm-server}} resource:

```yaml subs=true
apiVersion: apm.k8s.elastic.co/v1
kind: ApmServer
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: quickstart
    clientCertificateSecretName: my-custom-client-cert
```

### Beats [k8s-beats-custom-client-cert]

Set `clientCertificateSecretName` in the `elasticsearchRef` of the {{beats}} resource:

```yaml subs=true
apiVersion: beat.k8s.elastic.co/v1beta1
kind: Beat
metadata:
  name: quickstart
spec:
  type: filebeat
  version: {{version.stack}}
  elasticsearchRef:
    name: quickstart
    clientCertificateSecretName: my-custom-client-cert
```

### Enterprise Search [k8s-ent-search-custom-client-cert]

Set `clientCertificateSecretName` in the `elasticsearchRef` of the Enterprise Search resource:

```yaml subs=true
apiVersion: enterprisesearch.k8s.elastic.co/v1
kind: EnterpriseSearch
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: quickstart
    clientCertificateSecretName: my-custom-client-cert
```

:::{warning}
A bug in Enterprise Search's JRuby runtime can cause startup failures with some PKCS#8 private keys. If Enterprise Search fails to start after enabling client authentication, for operator-managed certificates delete the affected client certificate secret to force ECK to regenerate it. For custom certificates, regenerate and re-supply the certificate.
:::

### Elastic Maps Server [k8s-maps-custom-client-cert]

Set `clientCertificateSecretName` in the `elasticsearchRef` of the {{hosted-ems}} resource:

```yaml subs=true
apiVersion: maps.k8s.elastic.co/v1alpha1
kind: ElasticMapsServer
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: quickstart
    clientCertificateSecretName: my-custom-client-cert
```

### Logstash [k8s-logstash-custom-client-cert]

{{ls}} supports multiple {{es}} references, so `clientCertificateSecretName` is configured per entry in `elasticsearchRefs`:

```yaml subs=true
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRefs:
    - clusterName: production
      name: quickstart
      clientCertificateSecretName: my-custom-client-cert
```

:::{warning}
{{ls}} versions 8.10–8.18 and 9.0 can crash on startup with some PKCS#8 private keys due to a JRuby runtime bug. This is fixed in {{ls}} 8.19 and 9.1+. If you are running an affected version and {{ls}} fails to start after enabling client authentication, for operator-managed certificates delete the affected client certificate secret to force ECK to regenerate it. For custom certificates, regenerate and re-supply the certificate.
:::

### Elastic Agent [k8s-agent-custom-client-cert]

For standalone {{agent}}, `clientCertificateSecretName` is configured per entry in `elasticsearchRefs`:

```yaml subs=true
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  elasticsearchRefs:
    - name: quickstart
      outputName: default
      clientCertificateSecretName: my-custom-client-cert
```

For fleet-managed {{agents}}, {{fleet-server}} automatically propagates the client certificate information to all connected agents. No additional configuration is required.

### Fleet Server [k8s-fleet-server-es-custom-client-cert]

{{fleet-server}} also connects to {{es}} and can be configured with a custom client certificate via `elasticsearchRefs`:

```yaml subs=true
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: fleet-server
spec:
  version: {{version.stack}}
  mode: fleet
  fleetServerEnabled: true
  elasticsearchRefs:
    - name: quickstart
      outputName: default
      clientCertificateSecretName: my-custom-client-cert
```

:::{note}
{{fleet-server}} requires version 8.13.0 or later to support {{es}} client certificate authentication. If the {{fleet-server}} version is below 8.13.0, ECK blocks pod reconciliation and sets the agent status to red with a warning event.
:::

## Disable client certificate authentication [k8s-disable-client-cert-auth]

To turn off client certificate authentication, set `spec.http.tls.client.authentication` to `false` or remove it from the {{es}} resource:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
spec:
  http:
    tls:
      client:
        authentication: false
```

ECK handles the transition gracefully, deferring cleanup of mTLS resources until all pods have rolled over to ensure connectivity is maintained throughout the configuration change.
