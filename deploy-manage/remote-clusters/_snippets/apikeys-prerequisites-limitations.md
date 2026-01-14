<!--
This snippet is in use in the following locations:
- self-remote-cluster-eck.md
- eck-remote-clusters-to-other-eck.md
- ece-remote-cluster-self-managed.md
- ece-remote-cluster-same-ece.md
- ece-remote-cluster-other-ece.md
- ece-remote-cluster-ece-ess.md
- ece-enable-ccs-for-eck.md
- ec-remote-cluster-self-managed.md
- ec-remote-cluster-same-ess.md
- ec-remote-cluster-other-ess.md
- ec-remote-cluster-ece.md
- ec-enable-ccs-for-eck.md
-->
* The local and remote deployments must be on {{stack}} 8.14 or later.
* Unlike the certificate-based security model, the API key model does not require mutual trust between clusters; only the local cluster is required to trust the remote cluster's certificate.