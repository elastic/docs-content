When using TLS certificate–based authentication, the first step is to establish mutual trust between the clusters at the transport layer. This requires exchanging and trusting each cluster’s transport certificate authority (CA):
* The transport CA of the remote cluster must be added as a trusted CA in the local cluster.
* The local cluster’s transport CA must be added as a trusted CA in the remote cluster.

::::{note}
While it is technically possible to configure remote cluster connections using earlier versions of {{es}}, this guide only covers the setup for {{es}} 7.6 and later. The setup process is significantly simplified in {{es}} 7.6 due to improved support for the indirection of Kubernetes services.
::::

