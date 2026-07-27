---
navigation_title: Fleet Server client certificate authentication
applies_to:
  deployment:
    eck: ga 3.5
products:
  - id: cloud-kubernetes
---

# Fleet Server client certificate authentication on ECK [k8s-fleet-server-client-certificate-auth]

{{fleet-server}} can be configured to require client certificates from connecting {{agents}}, providing mutual TLS (mTLS) on the {{agent}}-to-{{fleet-server}} connection. This is independent of, and can be combined with, [{{es}} client certificate authentication](/deploy-manage/security/k8s-es-client-certificate-auth.md).

:::{note}
* This requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](/deploy-manage/license/manage-your-license-in-eck.md) for more details about managing licenses.
* {{fleet-server}} client certificate authentication requires one of the following {{fleet-server}} versions: 8.19.19+, 9.3.8+, 9.4.4+, or 9.5.0+.
:::

## Enable client authentication [k8s-fleet-server-enable-client-auth]

Set `spec.http.tls.client.authentication` to `true` on the {{fleet-server}} Agent resource:

```yaml subs=true
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: fleet-server
spec:
  version: {{version.stack}}
  mode: fleet
  fleetServerEnabled: true
  http:
    tls:
      client:
        authentication: true
```

When enabled, ECK does the following:

* Sets the `FLEET_SERVER_CLIENT_AUTH` environment variable to `required` on {{fleet-server}} pods.
* Automatically generates and manages client certificates for the {{fleet-server}}'s internal {{agent}} process and for all {{agents}} that reference this {{fleet-server}}.

Connecting {{agents}} require no additional configuration — ECK manages the full certificate lifecycle automatically.

:::{note}
If you have manually set `FLEET_SERVER_CLIENT_AUTH` in the pod template, that value takes precedence over the ECK-managed setting and the mTLS configuration may not apply as expected.
:::

## Use a custom client certificate for an Elastic Agent [k8s-agent-fleet-server-custom-client-cert]

To provide your own client certificate for an {{agent}} connecting to a {{fleet-server}} with client authentication enabled, set `clientCertificateSecretName` in the `fleetServerRef`:

```yaml subs=true
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: elastic-agent
spec:
  version: {{version.stack}}
  mode: fleet
  fleetServerRef:
    name: fleet-server
    clientCertificateSecretName: my-custom-client-cert
```

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
* The secret must be in the same namespace as the resource that references it.
* All components are compatible with PKCS#8 private keys. If you supply a certificate in a different format, verify compatibility with {{fleet-server}} and {{agent}} before use.
:::

## Disable client authentication on Fleet Server [k8s-fleet-server-disable-client-auth]

To turn off client authentication, set `spec.http.tls.client.authentication` to `false` or remove it from the {{fleet-server}} Agent resource:

```yaml
apiVersion: agent.k8s.elastic.co/v1alpha1
kind: Agent
metadata:
  name: fleet-server
spec:
  http:
    tls:
      client:
        authentication: false
```

ECK handles the transition gracefully.
