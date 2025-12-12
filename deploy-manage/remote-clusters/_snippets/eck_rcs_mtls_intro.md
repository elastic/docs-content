When using TLS certificate–based authentication, the first step is to establish mutual trust between the clusters at the transport layer. This requires exchanging and trusting each cluster’s transport certificate authority (CA):
* The transport CA of the remote cluster must be added as a trusted CA in the local cluster.
* The local cluster’s transport CA must be added as a trusted CA in the remote cluster.


