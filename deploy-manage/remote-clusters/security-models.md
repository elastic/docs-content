---
navigation_title: Security models
applies_to:
  stack: ga
  serverless: unavailable
products:
  - id: elasticsearch
---
# Remote cluster security models

Remote cluster security models determine how authentication and authorization works between clusters. {{es}} has evolved from a TLS certificate–based model, relying on mutual TLS authentication over the transport interface and duplicated roles across clusters, to a more flexible API key–based model that uses a dedicated service endpoint and supports fine-grained authorization on both local and remote clusters.

TLS certificate–based authentication is now deprecated, and users are encouraged to migrate to the API key–based model.

The following sections describe both models in detail and highlight their key differences.

::::{tip}
Security models work independently of [connection modes](./connection-modes.md). Both security models are compatible with either connection mode.
::::

## API key authentication [api-key]

API key authentication enables a local cluster to authenticate itself with a remote cluster using a [cross-cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key). The API key needs to be created by an administrator of the remote cluster. The local cluster is configured to provide this API key on each request to the remote cluster. The remote cluster verifies the API key, and grants access based on the API key’s privileges.

### Authorization

With this security model, authorization is enforced jointly by the local and remote cluster, as follows:

* All cross-cluster requests from the local cluster are bound by the API key’s privileges, regardless of local users associated with the requests. For example, if the API key only allows read access to `my-index` on the remote cluster, even a superuser from the local cluster is limited by this constraint. This mechanism enables the remote cluster’s administrator to have full control over who can access what data with cross-cluster search or cross-cluster replication. The remote cluster’s administrator can be confident that no access is possible beyond what is explicitly assigned to the API key.

* On the local cluster side, not every local user needs to access every piece of data allowed by the API key. An administrator of the local cluster can further configure additional permission constraints on local users so each user only gets access to the necessary remote data. It is only possible to further reduce the permissions allowed by the API key for individual local users. It is impossible to increase the permissions to go beyond what is allowed by the API key.

  ::::{tip}
  To configure fine-grained authorization for remote resources, use the `remote_indices` and `remote_clusters` fields in [role definitions](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md).
  ::::

### Connection details

In this model, cross-cluster operations use [a dedicated server port](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote_cluster.port), referred to as the remote cluster interface, for communication between clusters. The default port is `9443`. The remote cluster must enable this port for local clusters to connect.

From a TLS perspective, the local cluster must trust the remote cluster on the remote cluster interface. This means the local cluster must trust the certificate authority (CA) that signs the server certificate used by the remote cluster interface. When establishing a connection, all nodes from the local cluster that participate in cross-cluster communication verify certificates from nodes on the other side, based on the TLS trust configuration.

Mutual TLS is not required in this model.

### Setup

Refer to [Remote cluster setup](../remote-clusters.md#setup) for configuration guidance across all deployment types.

## TLS certificate authentication
```{applies_to}
stack: deprecated 9.0
```

TLS certificate authentication requires all connected clusters to trust one another and be mutually authenticated with TLS on the {{es}} transport interface (default port `9300` in self-managed, `9400` in {{ece}} and {{ech}}). This means that the local cluster trusts the certificate authority (CA) of the remote cluster, and the remote cluster trusts the CA of the local cluster. When establishing a connection, all nodes will verify certificates from nodes on the other side. This mutual trust is required to securely connect a remote cluster, because all connected nodes effectively form a single security domain.

### Authorization

With this security model, user authentication is performed on the local cluster, and the user and user’s roles names are passed to the remote cluster. A remote cluster checks the user’s role names against its local role definitions to determine which indices the user is allowed to access. This requires at least a role existing in the remote cluster with the same name as the local cluster for the user to gain privileges.

::::{warning}
In this model, a superuser on the local cluster gains total read access to the remote cluster, so it is only suitable for clusters that are in the same security domain.
::::

### Connection details

The local cluster uses the [transport interface](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md) to establish communication with remote clusters. The coordinating nodes in the local cluster establish [long-lived](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#long-lived-connections) TCP connections with specific nodes in the remote cluster. These connections must remain open, even if the connections are idle for an extended period.

### Setup

Refer to [Remote cluster setup](../remote-clusters.md#setup) for configuration guidance across all deployment types.

### Security models: comparison

| Aspect              | API key–based                                                                 | TLS certificate–based                          |
|---------------------|-------------------------------------------------------------------------------|------------------------------------------------|
| **Status**          | Recommended                                                                   | Deprecated                                     |
| **Service endpoint**| Uses a dedicated remote-cluster-server service endpoint                       | Uses the default transport interface            |
| **Default port**    | 9443                                                                          | 9300 in self-managed, 9400 in {{ech}} or {{ece}}                              |
| **Authentication**  | Client authenticates with an API key and validates the server’s certificate | Requires mutual TLS (both client and server present and validate certificates) |
| **Authorization** | Flexible: privileges can be scoped in the API key and combined with roles on the local cluster; supports fine-grained authorization | Rigid: roles must exist on the remote cluster with exact name matching; all authorization defined remotely |
| **Credential management** | API keys can be created with expiration and revoked without PKI changes        | Requires certificate issuance, distribution, and rotation across clusters |

