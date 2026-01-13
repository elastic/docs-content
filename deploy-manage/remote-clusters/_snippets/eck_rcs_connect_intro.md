<!--
This snippet is in use in the following locations:
- self-remote-cluster-eck.md
- eck-remote-clusters-to-other-eck.md
- ece-enable-ccs-for-eck.md
- ec-enable-ccs-for-eck.md

It requires local_type_generic substitution to be defined
-->
On the local {{local_type_generic}}, use {{kib}} or the {{es}} API to add the remote ECK cluster with the following connection settings:

* **Remote address**: Use the FQDN or IP address of the LoadBalancer service or alternative resource that you created to expose the remote cluster.

	* For API key-based authentication, use the server interface address and port.
	* For TLS certificate-based authentication, use the transport interface address and port.

  If you haven't changed the external listening port of the kubernetes service, the port should be `9443` for API key-based authentication, or `9300` for TLS certificate-based authentication.

* **TLS server name**: You can try leaving this field empty first. If the connection fails, and your environment is presenting the ECK-managed certificates during the TLS handshake, use `<cluster-name>-es-remote-cluster.<namespace>.svc` as the server name. For example, for a cluster named `quickstart` in the `default` namespace, use `quickstart-es-remote-cluster.default.svc`.
