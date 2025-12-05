<!--
This snippet is in use in the following locations:
- eck-remote-clusters-from-external.md
- ec-enable-ccs-for-eck.md
- ece-enable-ccs-for-eck.md

It requires local_type_generic substitution to be defined
-->
On the local {{local_type_generic}}, add the remote ECK cluster using {{kib}} or the {{es}} API with the following connection settings:

* **Remote address**: Use the FQDN or IP address of the LoadBalancer service, or similar resource, you created to expose the remote cluster server interface (for API key-based authentication) or the transport interface (for TLS certificate-based authentication).

* **TLS server name**: You can try leaving this field empty first. If the connection fails, and your environment is presenting the ECK-managed certificates during the TLS handshake, use `<cluster-name>-es-remote-cluster.<namespace>.svc` as the server name. For example, for a cluster named `quickstart` in the `default` namespace, use `quickstart-es-remote-cluster.default.svc`.
