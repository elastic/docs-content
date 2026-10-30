---
navigation_title: "{{es}} PKI authentication"
description: Let Elastic Stack components managed by ECK authenticate to Elasticsearch with their TLS client certificate, through a PKI realm that ECK manages, instead of a service account token or a username and password.
applies_to:
  deployment:
    eck: ga 3.6
products:
  - id: cloud-kubernetes
---

# {{es}} PKI authentication on {{eck}} [k8s-es-pki-authentication]

When you enable [{{es}} client certificate authentication](/deploy-manage/security/k8s-es-client-certificate-auth.md) (mTLS), each {{stack}} component that ECK connects to {{es}} presents a client certificate. By default, the component also authenticates with a service account token or a username and password. You can enable PKI authentication so that the component authenticates with its client certificate only, through a [PKI realm](/deploy-manage/users-roles/cluster-or-deployment-auth/pki.md) that ECK manages. With PKI authentication, ECK doesn't create credential secrets for that connection, which reduces the number of secrets in your cluster. ECK also keeps the role mapping in step with the client certificate, so when the certificate rotates, nothing stale is left behind.

You enable PKI authentication on both sides of the connection:

* On the {{es}} resource, `spec.auth.pki.enabled: true` configures the ECK-managed PKI realm.
* On each component, `authenticationMode: PKI` in the `elasticsearchRef` switches that connection to PKI authentication.

For each component that uses PKI authentication, ECK creates an {{es}} role mapping with the same roles that the component gets when it uses credentials. ECK binds the role mapping to the public key of the component's client certificate, not to a username.

:::{note}
This requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](/deploy-manage/license/manage-your-license-in-eck.md) for more details about managing licenses.
:::

## Requirements [k8s-es-pki-requirements]

* {{es}} 9.6.0 or later.
* [Client certificate authentication](/deploy-manage/security/k8s-es-client-certificate-auth.md) enabled on {{es}} with `spec.http.tls.client.authentication: true`.
* A component that supports PKI authentication:

  | Component | PKI authentication support |
  | --- | --- |
  | {{kib}} | Supported |
  | {{apm-server}} | Supported |
  | {{beats}} | Supported |
  | Standalone {{agent}} | Supported |
  | {{ls}} | Supported |
  | {{hosted-ems}} | {applies_to}`stack: ga 9.6` Supported |
  | Fleet-managed {{agent}} and {{fleet-server}} | Not supported |
  | Enterprise Search | Not supported |

  You enable PKI authentication per component, so you can use it for the supported components in your environment while other components continue to authenticate with credentials. ECK rejects `authenticationMode: PKI` for the components that don't support it. Connections that ECK configures for stack monitoring always use credentials.

## Reserved names and settings [k8s-es-pki-reserved]

When `spec.auth.pki.enabled` is `true`, ECK rejects any {{es}} configuration that uses the following names and settings, whether you set it in `spec.nodeSets[*].config` or in a [{{stack}} configuration policy](/deploy-manage/deploy/cloud-on-k8s/elastic-stack-configuration-policies.md) that applies to the cluster:

* The realm name `eck_managed_pki`, in any realm type.
* The realm order `2147483647`, in any realm.
* The node attribute `node.attr.eck_managed_pki_realm`.

ECK also reserves the `eck_managed_pki_` prefix for the names of the role mappings it creates. {{stack}} configuration policies can't add role mappings with this prefix, or any of the names and settings in the previous list, even if their target clusters don't use PKI authentication.

## Enable the PKI realm on {{es}} [k8s-es-pki-enable-realm]

Set `spec.auth.pki.enabled` to `true` on the {{es}} resource, together with `spec.http.tls.client.authentication`:

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
  auth:
    pki:
      enabled: true
```

ECK adds a PKI realm named `eck_managed_pki` to the {{es}} configuration. The realm trusts the client certificates that ECK generates and the custom client certificates that you provide. ECK places the realm last in the realm chain, so it doesn't take precedence over other realms that you might configure, such as JWT or Kerberos.

The PKI realm is a static setting, so enabling or disabling it on an existing cluster triggers a rolling restart of the {{es}} nodes. Enabling the realm alone doesn't change how components authenticate, and components keep their credentials until you switch them to PKI authentication.

## Switch a component to PKI authentication [k8s-es-pki-enable-component]

Set `authenticationMode: PKI` in the `elasticsearchRef` of the component. For example, for {{kib}}:

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
    authenticationMode: PKI
```

The same field applies to {{apm-server}}, {{beats}}, and {{hosted-ems}}. For {{ls}} and standalone {{agent}}, set `authenticationMode` on each entry of `elasticsearchRefs`. 

For {{ls}}, you also need to [update the {{es}} output configuration in your pipelines](#k8s-es-pki-logstash).

The `authenticationMode` field accepts these values:

| Value | Behavior |
| --- | --- |
| `Credentials` | The component authenticates with a service account token or a username and password. If you omit the field, ECK uses this value by default. |
| `PKI` | The component authenticates with its client certificate only. |

`authenticationMode: PKI` requires a named `elasticsearchRef`. You can't use it with `secretName` to connect to an {{es}} cluster that ECK doesn't manage.

### How ECK switches the connection [k8s-es-pki-switch-process]

When you switch a component to PKI authentication, ECK keeps its existing credentials until PKI authentication is ready:

1. ECK creates an {{es}} role mapping for the public key of the component's client certificate, through the file-based settings of the {{es}} cluster.
2. ECK waits until the PKI realm runs on all {{es}} nodes and {{es}} has applied the role mapping.
3. ECK reconfigures the component to authenticate with its client certificate only, and then deletes the credentials it created for that connection.

While ECK waits, the association status of the component is `Pending`, and ECK reports the reason in an event on the component. This status is expected, for example during the rolling restart that loads the PKI realm. It also happens each time the client certificate gets a new public key, such as when ECK rotates the certificate, because ECK updates the role mapping for the new key. If the association stays `Pending`, check the events on the component and on the {{es}} resource:

```sh
kubectl describe kibana quickstart
kubectl describe elasticsearch quickstart
```

The association also stays `Pending` if your configuration doesn't meet all the [requirements](#k8s-es-pki-requirements), for example if `spec.auth.pki.enabled` isn't set on the {{es}} resource.

### Use PKI authentication with {{ls}} [k8s-es-pki-logstash]

{{ls}} pipelines get the {{es}} connection details from environment variables that ECK sets. In PKI mode, ECK doesn't set the `NORMALIZED_CLUSTERNAME_ES_USER` and `NORMALIZED_CLUSTERNAME_ES_PASSWORD` variables. Remove the `user` and `password` options from the {{es}} plugins in your pipelines. Use the client certificate variables instead:

```yaml subs=true
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRefs:
    - clusterName: prod-es
      name: quickstart
      authenticationMode: PKI
  pipelines:
    - pipeline.id: main
      config.string: |
        input {
          beats {
            port => 5044
          }
        }
        output {
          elasticsearch {
            hosts => [ "${PROD_ES_ES_HOSTS}" ]
            ssl_enabled => true
            ssl_certificate_authorities => "${PROD_ES_ES_SSL_CERTIFICATE_AUTHORITY}"
            ssl_certificate => "${PROD_ES_ES_SSL_CERTIFICATE}"
            ssl_key => "${PROD_ES_ES_SSL_KEY}"
          }
        }
```

For more details about these environment variables, refer to [Using {{es}} in {{ls}} pipelines](/deploy-manage/deploy/cloud-on-k8s/configuration-logstash.md#k8s-logstash-pipelines-es).

## Use a custom client certificate [k8s-es-pki-custom-client-cert]

PKI authentication works with the client certificates that ECK generates and with the [custom client certificates](/deploy-manage/security/k8s-es-client-certificate-auth.md#k8s-custom-client-cert) that you provide through `clientCertificateSecretName`. With a custom certificate, ECK binds the role mapping to the public key of your certificate:

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
    authenticationMode: PKI
```

A custom certificate must have a non-empty subject common name (CN), because {{es}} derives the PKI username from it. If the CN is empty, for example in a certificate that only sets subject alternative names, the association stays `Pending`.

Each component needs a certificate with a unique public key, because ECK maps the public key to the component's roles. If two or more components share the same public key but need different roles, ECK can't create a role mapping for any of them, and their associations stay `Pending` with a conflict event. Use a different certificate for each component.

## Switch a component back to credentials [k8s-es-pki-disable]

To switch a component back to credential-based authentication, set `authenticationMode` to `Credentials` or remove it from the `elasticsearchRef`. ECK creates the credentials for the component again and removes its role mapping.

To disable PKI authentication for the whole cluster:

1. Switch all components that use PKI authentication back to credentials.
2. Set `spec.auth.pki.enabled` to `false`, or remove it from the {{es}} resource.

When you disable the PKI realm, ECK removes all the role mappings that it created for PKI authentication. Components that still use `authenticationMode: PKI` can't authenticate to {{es}} after that.
