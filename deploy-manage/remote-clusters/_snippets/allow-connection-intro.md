Before you start, consider the [security model](/deploy-manage/remote-clusters/security-models.md) that you would prefer to use for authenticating remote connections between clusters, and follow the corresponding steps.

API key
:   For deployments based on {{stack}} 8.14 or later, you can use an API key to authenticate and authorize cross-cluster operations to a remote cluster. This model uses a dedicated service endpoint, on port `9443` by default, and gives administrators fine-grained control over remote access. The API key is created on the remote cluster and defines the permissions available to all cross-cluster requests, while local user roles can further restrict, but not extend, those permissions.

TLS certificate (deprecated in {{stack}} 9.0.0)
:   This model uses mutual TLS authentication over the {{es}} transport interface for cross-cluster operations. User authentication is performed on the local cluster and a user's role names are passed to the remote cluster for authorization. Because a superuser on the local cluster automatically gains full read access to the remote cluster, this model is only suitable for clusters within the same security domain.
