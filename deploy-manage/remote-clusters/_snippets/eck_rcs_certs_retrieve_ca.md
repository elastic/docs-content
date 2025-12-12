ECK stores the CA used to issue certificates for the {{es}} transport layer in a secret named `<cluster_name>-es-transport-certs-public`.

For example, to save the transport CA certificate of a cluster named `quickstart` into a local file, run the following command:

```sh
kubectl get secret quickstart-es-transport-certs-public \
-o go-template='{{index .data "ca.crt" | base64decode}}' > quickstart_transport_ca.crt
```

::::{note}
Beware of copying the source secret as-is into a different namespace. Refer to [Copying secrets with Owner References](/troubleshoot/deployments/cloud-on-k8s/common-problems.md#k8s-common-problems-owner-refs) for more information.
::::

::::{note}
CA certificates are automatically rotated after one year by default. You can [configure](/deploy-manage/deploy/cloud-on-k8s/configure-eck.md) this period. Make sure to keep the copy of the certificates secret up-to-date.
::::

