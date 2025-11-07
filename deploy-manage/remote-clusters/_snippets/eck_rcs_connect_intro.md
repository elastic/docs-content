On the local deployment, add the remote ECK cluster using {{kib}} or the {{es}} API.

::::{note}
When configuring the remote cluster connection:

* **Remote address**: Use the FQDN or IP address of the LoadBalancer service, or similar resource, you created to expose the remote cluster server interface (for API key authentication) or the transport interface (for certificate-based authentication).

* **TLS server name**: You can try leaving this field empty first. If the connection fails, and your environment is presenting the ECK-managed certificates during the TLS handshake, use `<cluster-name>-es-remote-cluster.<namespace>.svc` as the server name. For example, for a cluster named `quickstart` in the `default` namespace, use `quickstart-es-remote-cluster.default.svc`.
::::

