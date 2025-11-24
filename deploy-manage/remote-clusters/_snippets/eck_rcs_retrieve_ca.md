The certificate authority (CA) used by ECK to issue certificates for the remote cluster server interface is stored in the `ca.crt` key of the secret named `<cluster_name>-es-transport-certs-public`.

If the external connections reach the {{es}} Pods on port `9443` without any intermediate TLS termination, you must retrieve this CA, as it will be required in the local cluster configuration to establish trust.

For example, to save the transport CA certificate of a cluster named `quickstart` into a local file, run the following command:

```sh
kubectl get secret quickstart-es-transport-certs-public \
-o go-template='{{index .data "ca.crt" | base64decode}}' > eck_transport_ca.crt
```

You can verify that the file contains a valid CA certificate by running the following command:

```bash
openssl x509 -in eck_transport_ca.crt -noout -text
```

::::{important}
ECK-managed CA certificates are automatically rotated after one year by default, but you can [configure](/deploy-manage/deploy/cloud-on-k8s/configure-eck.md) a different validity period.

When the CA certificate is rotated, ensure that this CA is updated in all environments where it's used to preserve trust.
::::

