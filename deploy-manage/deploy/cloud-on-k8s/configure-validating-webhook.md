---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-webhook.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Configure the validating webhook [k8s-webhook]

ECK can be configured to provide a [validating webhook](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/) that validates Elastic custom resources ({{eck_resources_list}}) before they are created or updated. Validating webhooks provide immediate feedback if a submitted manifest contains invalid or illegal configuration — which can help you catch errors early and save time that would otherwise be spent on troubleshooting.

Validating webhooks are defined using a `ValidatingWebhookConfiguration` object that defines the following:

* Type of resource to validate ({{es}}, {{kib}} and so on)
* Type of actions to validate (create, update, delete)
* Connection details to the webhook

    * Kubernetes service name and namespace
    * Request path
    * CA certificate for verifying the server

* Failure policy if the webhook is unavailable (block the operation or continue without validation)


## Defaults provided by ECK [k8s-webhook-defaults]

When using the default `operator.yaml` manifest, ECK is installed with a `ValidatingWebhookConfiguration` configured as follows:

* Validate all known Elastic custom resources ({{eck_resources_list}}) on create and update.
* The operator itself is the webhook server — which is exposed through a service named `elastic-webhook-server` in the `elastic-system` namespace.
* The operator generates a certificate for the webhook and stores it in a secret named `elastic-webhook-server-cert` in the `elastic-system` namespace. This certificate is automatically rotated by the operator when it is due to expire.


## Manual configuration [k8s-webhook-manual-config]

If you installed ECK without the webhook and want to enable it later on, or if you want to customize the configuration such as providing your own certificates, this section describes the options available to you.


### Configuration options [k8s-webhook-config-options]

You can customize almost all aspects of the webhook setup by changing the [operator configuration](configure-eck.md).

| Configuration option | Default value | Description |
| --- | --- | --- |
| `enable-webhook` | false | This must be set to `true` to enable the webhook server. |
| `manage-webhook-certs` | true | Set to `false` to disable auto-generating the certificate for the webhook. If disabled, you must provide your own certificates using one of the methods described later in this document. |
| `webhook-cert-dir` | /tmp/k8s-webhook-server/serving-certs | Path to mount the certificate. |
| `webhook-name` | elastic-webhook.k8s.elastic.co | Name of the `ValidatingWebhookConfiguration` resource. |
| `webhook-secret` | elastic-webhook-server-cert | Name of the secret containing the certificate for the webhook server. |
| `webhook-port` | 9443 | Port to listen for incoming validation requests. |


### Using your own certificates [k8s-webhook-existing-certs]

This section describes how you can use your own certificates for the webhook instead of letting the operator manage them automatically. There are a few important things to be aware of when going down this route:

* You have to keep track of the expiry dates and manage the certificate rotation yourself. Expired certificates may stop the webhook from working.
* The secret containing the custom certificate must be available when the operator starts.
* You must update the `caBundle` fields in the `ValidatingWebhookConfiguration` yourself. This must be done at the beginning and whenever the certificate is rotated.


#### Use a certificate signed by your own CA [k8s-webhook-own-ca]

* The certificate must have a Subject Alternative Name (SAN) of the form `<service_name>.<namespace>.svc` (for example `elastic-webhook-server.elastic-system.svc`). A typical OpenSSL command to generate such a certificate would be as follows:

    ```sh
    openssl req -x509 -sha256 -nodes -newkey rsa:4096 -days 365 -subj "/CN=elastic-webhook-server" -addext "subjectAltName=DNS:elastic-webhook-server.elastic-system.svc" -keyout tls.key -out tls.crt
    ```

* Create a secret in the namespace the operator would be deployed to. This secret must contain the certificate under the `tls.crt` key and the private key under the `tls.key` key.

    ```sh
    kubectl create secret -n elastic-system generic elastic-webhook-server-custom-cert --from-file=tls.crt=tls.crt --from-file=tls.key=tls.key
    ```

* Encode your CA trust chain as base64 and set it as the value of the `caBundle` fields in the `ValidatingWebhookConfiguration`. Note that there are multiple `caBundle` fields in the webhook configuration.
* Install the operator with the following options:

    * Set `manage-webhook-certs` to `false`
    * Set `webhook-secret` to the name of the secret you have just created (`elastic-webhook-server-custom-cert`)


::::{note}
If you are using the [Helm chart installation method](install-using-helm-chart.md), you can install the operator by running this command:

```sh
helm install elastic-operator elastic/eck-operator -n elastic-system --create-namespace \
  --set=webhook.manageCerts=false \
  --set=webhook.certsSecret=elastic-webhook-server-custom-cert \
  --set=webhook.caBundle=$(base64 -w 0 ca.crt)
```

::::



#### Use a certificate from cert-manager [k8s-webhook-cert-manager]

This section describes how to use [cert-manager](https://cert-manager.io/) to manage the webhook certificate. It assumes that there is a `ClusterIssuer` named `self-signing-issuer` available.

* Create a new certificate

    ```yaml
    apiVersion: cert-manager.io/v1
    kind: Certificate
    metadata:
      name: elastic-webhook-server-cert
      namespace: elastic-system
    spec:
      dnsNames:
        - elastic-webhook-server.elastic-system.svc
      issuerRef:
        kind: ClusterIssuer
        name: self-signing-issuer
      secretName: elastic-webhook-server-cert
      subject:
        organizations:
          - example
    ```

* Annotate the `ValidatingWebhookConfiguration` to inject the CA bundle:

    ```yaml
    apiVersion: admissionregistration.k8s.io/v1
    kind: ValidatingWebhookConfiguration
    metadata:
      annotations:
        cert-manager.io/inject-ca-from: elastic-system/elastic-webhook-server-cert
      name: elastic-webhook.k8s.elastic.co
    webhooks:
    [...]
    ```

* Install the operator with the following options:

    * Set `manage-webhook-certs` to `false`
    * Set `webhook-secret` to the name of the certificate secret (`elastic-webhook-server-cert`)


::::{note}
If you are using the [Helm chart installation method](install-using-helm-chart.md), you can install the operator by running the following command:

```sh
helm install elastic-operator elastic/eck-operator -n elastic-system --create-namespace \
  --set=webhook.manageCerts=false \
  --set=webhook.certsSecret=elastic-webhook-server-cert \
  --set=webhook.certManagerCert=elastic-webhook-server-cert
```

::::



## Disable the webhook [k8s-disable-webhook]

To disable the webhook, set the [`enable-webhook`](configure-eck.md) operator configuration flag to `false` and remove the `ValidatingWebhookConfiguration` named `elastic-webhook.k8s.elastic.co`:

```sh
kubectl delete validatingwebhookconfigurations.admissionregistration.k8s.io elastic-webhook.k8s.elastic.co
```


## Troubleshooting [k8s-webhook-troubleshooting]

You might get errors in your Kubernetes API server logs indicating that it cannot reach the operator service (`elastic-webhook-server`). This could be because no operator pods are available to handle request or because a network policy or a firewall rule is preventing the control plane from accessing the service. To help with troubleshooting, you can change the [`failurePolicy`](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#failure-policy) of the webhook configuration to `Fail`. This will cause create or update operations to fail if there is an error contacting the webhook. Usually the error message will contain helpful information about the failure that will allow you to diagnose the root cause.


### Resource creation taking too long or timing out [k8s-webhook-troubleshooting-timeouts]

Webhooks require network connectivity between the Kubernetes API server and the operator. If the creation of an {{es}} resource times out with an error message similar to the following, then the Kubernetes API server might be unable to connect to the webhook to validate the manifest.

```
Error from server (Timeout): error when creating "elasticsearch.yaml": Timeout: request did not complete within requested timeout 30s
```
If you get this error, try re-running the command with a higher request timeout as follows:

```sh
kubectl --request-timeout=1m apply -f elasticsearch.yaml
```

As the default [`failurePolicy`](https://kubernetes.io/docs/reference/access-authn-authz/extensible-admission-controllers/#failure-policy) of the webhook is `Ignore`, this command should succeed after about 30 seconds. This is an indication that the API server cannot contact the webhook server and has foregone validation when creating the resource.

On [GKE private clusters](https://cloud.google.com/kubernetes-engine/docs/concepts/private-cluster-concept), you may have to add a firewall rule allowing access to port 9443 from the API server so that it can contact the webhook. Check the [GKE documentation on firewall rules](https://cloud.google.com/kubernetes-engine/docs/how-to/private-clusters#add_firewall_rules) and the [Kubernetes issue](https://github.com/kubernetes/kubernetes/issues/79739) for more details.

It is possible that a [network policy](https://kubernetes.io/docs/concepts/services-networking/network-policies/) is blocking any incoming requests to the webhook server. Consult your system administrator to determine whether that is the case, and create an appropriate policy to allow communication between the Kubernetes API server and the webhook server. For example, the following network policy simply opens up the webhook port to the world:

```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-webhook-access-from-any
  namespace: elastic-system
spec:
  podSelector:
    matchLabels:
      control-plane: elastic-operator
  ingress:
  - from: []
    ports:
      - port: 9443
```

If you want to restrict the webhook access only to the Kubernetes API server, you must know the IP address of the API server, that you can obtain through this command:

```sh
kubectl cluster-info | grep master
```

Assuming that the API server IP address is `10.1.0.1`, the following policy restricts webhook access to just the API server.

```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: allow-webhook-access-from-apiserver
  namespace: elastic-system
spec:
  podSelector:
    matchLabels:
      control-plane: elastic-operator
  ingress:
  - from:
      - ipBlock:
          cidr: 10.1.0.1/32
    ports:
      - port: 9443
```


### Updates failing due to validation errors [k8s-webhook-troubleshooting-validation-failure]

If your attempts to update a resource fail with an error message similar to the following, you can force the webhook to ignore it by removing the `kubectl.kubernetes.io/last-applied-configuration` annotation from your resource.

```txt subs=true
admission webhook "elastic-es-validation-v1.k8s.elastic.co" denied the request: {{es}}.elasticsearch.k8s.elastic.co "quickstart" is invalid: some-misspelled-field: Invalid value: "some-misspelled-field": some-misspelled-field field found in the kubectl.kubernetes.io/last-applied-configuration annotation is unknown
```
