% Applies switch to identify the endpoint when configuring a remote cluster connection
::::::{applies-switch}

:::::{applies-item} ess:
Obtain the endpoint from the **Security** page of the ECH deployment you want to use as a remote. Copy the **Proxy address** from the **Remote cluster parameters** section, and replace its port with `9443`, which is the port used by the remote cluster server interface.
:::::

:::::{applies-item} ece:
Obtain the endpoint from the **Security** page of the ECE deployment you want to use as a remote. Copy the **Proxy address** from the **Remote cluster parameters**, and replace its port with `9443`, which is the port used by the remote cluster server interface.
:::::

:::::{applies-item} eck:
Use the FQDN or IP address of the LoadBalancer service, or similar resource, you created to [expose the remote cluster server interface](#enable-rcs) on port `9443`.

If your environment presents the ECK-managed certificates during the TLS handshake, configure the server name field as `<cluster-name>-es-remote-cluster.<namespace>.svc`. Otherwise, the local cluster cannot establish the connection due to SSL trust errors.
:::::

:::::{applies-item} self:
The endpoint depends on your network architecture and the selected connection mode (`sniff` or `proxy`). It can be one or more {{es}} nodes, or a TCP (layer 4) load balancer or reverse proxy in front of the cluster, as long as the local cluster can reach them over port `9443`.

If you are configuring `sniff` mode, set the seeds parameter instead of the proxy address. Refer to the [connection modes](/deploy-manage/remote-clusters/connection-modes.md) documentation for details and connectivity requirements of each mode.
:::::
::::::

