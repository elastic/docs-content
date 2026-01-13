<!--
This snippet is in use in the following locations:
- eck-remote-clusters-to-external.md
-->
% Endpoint identification for multiple deployment types
:::::::{applies-switch}

::::::{applies-item} ess:
Obtain the endpoint from the **Security** page of the ECH deployment you want to use as a remote. Copy the **Proxy address** from the **Remote cluster parameters** section, and replace its port with `9443`, which is the port used by the remote cluster server interface.
::::::

::::::{applies-item} ece:
Obtain the endpoint from the **Security** page of the ECE deployment you want to use as a remote. Copy the **Proxy address** from the **Remote cluster parameters**, and replace its port with `9443`, which is the port used by the remote cluster server interface.
::::::

::::::{applies-item} self:
The endpoint depends on your network architecture and the selected connection mode (`sniff` or `proxy`). It can be one or more {{es}} nodes, or a TCP (layer 4) load balancer or reverse proxy in front of the cluster, as long as the local cluster can reach them over port `9443`.

If you are configuring `sniff` mode, set the seeds parameter instead of the proxy address. Refer to the [connection modes](/deploy-manage/remote-clusters/connection-modes.md) documentation for details and connectivity requirements of each mode.
::::::

:::::::