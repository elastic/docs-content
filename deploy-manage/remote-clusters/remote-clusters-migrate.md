---
navigation_title: Migrate from certificate to API key authentication
mapped_pages:
  - https://www.elastic.co/guide/en/elasticsearch/reference/current/remote-clusters-migrate.html
applies_to:
  deployment:
    self: ga
products:
  - id: elasticsearch
---



# Migrate from certificate to API key authentication [remote-clusters-migrate]


The API key based security model for remote clusters offers administrators more fine-grained access controls compared to the TLS certificate based security model. For that reason, you may want to migrate from the certificate based security model to the API key based model.

While it is possible to migrate by defining a new remote cluster connection, using a new alias, this has several downsides:

* For {{ccr}}, it’s not possible to change the leader cluster alias for existing tasks. As a result, with a new remote cluster, follower indices would need to be re-created from scratch.
* For {{ccs}}, transform and anomaly detection jobs do allow updating the remote cluster alias. However, if the job was created with wildcards, for example `*:source_index`, and `superuser`, adding a new remote cluster will cause the job to do double the amount of work and potentially skew results with duplications.

For these reasons, you may prefer to migrate a remote cluster in-place, by following these steps:

1. [Review the prerequisites](#remote-clusters-migration-prerequisites)
2. [Reconfigure the remote cluster and generate a cross-cluster API key](#remote-clusters-migration-remote-cluster)
3. [Stop cross-cluster operations](#remote-clusters-migration-stop)
4. [Reconnect to the remote cluster](#remote-clusters-migration-reconnect)
5. [Resume cross-cluster operations](#remote-clusters-migration-resume)
6. [Disable certificate based authentication and authorization](#remote-clusters-migration-disable-cert)

If you run into any issues, refer to [Troubleshooting](/troubleshoot/elasticsearch/remote-clusters.md).

## Prerequisites [remote-clusters-migration-prerequisites]

* The nodes of the local and remote clusters must be on {{stack}} 8.14 or later.
* The local and remote clusters must have an appropriate license. For more information, refer to [https://www.elastic.co/subscriptions](https://www.elastic.co/subscriptions).


## Reconfigure the remote cluster and generate a cross-cluster API key [remote-clusters-migration-remote-cluster]

On the remote cluster:

1. Enable the remote cluster server on every node of the remote cluster. In [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

    1. Set [`remote_cluster_server.enabled`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote-cluster-network-settings) to `true`.
    2. Configure the bind and publish address for remote cluster server traffic, for example using [`remote_cluster.host`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote-cluster-network-settings). Without configuring the address, remote cluster traffic may be bound to the local interface, and remote clusters running on other machines can’t connect.
    3. Optionally, configure the remote server port using [`remote_cluster.port`](elasticsearch://reference/elasticsearch/configuration-reference/networking-settings.md#remote_cluster.port) (defaults to `9443`).

2. Next, generate a certificate authority (CA) and a server certificate/key pair. On one of the nodes of the remote cluster, from the directory where {{es}} has been installed:

    1. Create a CA, if you don’t have a CA already:

        ```sh
        ./bin/elasticsearch-certutil ca --pem --out=cross-cluster-ca.zip --pass CA_PASSWORD
        ```

        Replace `CA_PASSWORD` with the password you want to use for the CA. You can remove the `--pass` option and its argument if you are not deploying to a production environment.

    2. Unzip the generated `cross-cluster-ca.zip` file. This compressed file contains the following content:

        ```txt
        /ca
        |_ ca.crt
        |_ ca.key
        ```

    3. Generate a certificate and private key pair for the nodes in the remote cluster:

        ```sh
        ./bin/elasticsearch-certutil cert --out=cross-cluster.p12 --pass=CERT_PASSWORD --ca-cert=ca/ca.crt --ca-key=ca/ca.key --ca-pass=CA_PASSWORD --dns=example.com --ip=192.0.2.1
        ```

        * Replace `CA_PASSWORD` with the CA password from the previous step.
        * Replace `CERT_PASSWORD` with the password you want to use for the generated private key.
        * Use the `--dns` option to specify the relevant DNS name for the certificate. You can specify it multiple times for multiple DNS.
        * Use the `--ip` option to specify the relevant IP address for the certificate. You can specify it multiple times for multiple IP addresses.

    4. If the remote cluster has multiple nodes, you can either:

        * create a single wildcard certificate for all nodes;
        * or, create separate certificates for each node either manually or in batch with the [silent mode](elasticsearch://reference/elasticsearch/command-line-tools/certutil.md#certutil-silent).

3. On every node of the remote cluster:

    1. Copy the `cross-cluster.p12` file from the earlier step to the `config` directory. If you didn’t create a wildcard certificate, make sure you copy the correct node-specific p12 file.
    2. Add following configuration to [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

        ```yaml
        xpack.security.remote_cluster_server.ssl.enabled: true
        xpack.security.remote_cluster_server.ssl.keystore.path: cross-cluster.p12
        ```

    3. Add the SSL keystore password to the {{es}} keystore:

        ```sh
        ./bin/elasticsearch-keystore add xpack.security.remote_cluster_server.ssl.keystore.secure_password
        ```

        When prompted, enter the `CERT_PASSWORD` from the earlier step.

4. Restart the remote cluster.
5. On the remote cluster, generate a cross-cluster API key that provides access to the indices you want to use for {{ccs}} or {{ccr}}. You can use the [Create Cross-Cluster API key](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-create-cross-cluster-api-key) API or [{{kib}}](../api-keys/elasticsearch-api-keys.md).
6. Copy the encoded key (`encoded` in the response) to a safe location. You will need it to connect to the remote cluster later.


## Stop cross-cluster operations [remote-clusters-migration-stop]

On the local cluster, stop any persistent tasks that refer to the remote cluster:

* Use the [Stop {{transforms}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-stop-transform) API to stop any transforms.
* Use the [Close jobs](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-close-job) API to close any anomaly detection jobs.
* Use the [Pause auto-follow pattern](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-pause-auto-follow-pattern) API to pause any auto-follow {{ccr}}.
* Use the [Pause follower](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-pause-follow) API to pause any manual {{ccr}} or existing indices that were created from the auto-follow pattern.


## Reconnect to the remote cluster [remote-clusters-migration-reconnect]

On the local cluster:

1. Enhance any roles used by local cluster users with the required [remote indices privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-indices-priv) or [remote cluster privileges](/deploy-manage/users-roles/cluster-or-deployment-auth/role-structure.md#roles-remote-cluster-priv) for {{ccr}} and {{ccs}}. Refer to [Configure roles and users](remote-clusters-api-key.md#remote-clusters-privileges-api-key). Note:

    * You only need to assign additional `remote_indices` or `remote_cluster` privileges to existing roles used for cross-cluster operations. You should be able to copy these privileges from the original roles on the remote cluster, where they are defined under the certification based security model.
    * The roles on the local cluster can’t exceed the `access` privilege granted by the cross-cluster API key. Any extra local privileges will be suppressed by the cross-cluster API key’s privileges.
    * No update is needed if the {{ccr}} or {{ccs}} tasks have been configured with a `superuser` role. The `superuser` role is automatically updated to allow access to all remote indices.
    * Tasks that are run as regular users with named roles are immediately updated with the new privileges. A task will load a new definition the next time it runs.
    * You need to restart tasks that are run using an API key (done in a later step).

2. If you’ve dynamically configured the remote cluster (via the cluster settings API):

    1. Retrieve the current remote cluster configuration, and store it in a safe place. You may need it later in case you need to [roll back](#remote-clusters-migration-rollback). Use the cluster settings API:

        ```console
        GET /_cluster/settings?filter_path=persistent.cluster.remote
        ```

    2. Remove the existing remote cluster definition by setting the remote cluster settings to `null`.

3. If you’ve statically configured the remote cluster (via `elasticsearch.yml`), copy the `cluster.remote` settings from `elasticsearch.yml` and store them in a safe place. You may need them later in case you need to [roll back](#remote-clusters-migration-rollback).
4. On every node of the local cluster:

    1. Copy the `ca.crt` file generated on the remote cluster earlier into the `config` directory, renaming the file `remote-cluster-ca.crt`.
    2. Add following configuration to [`elasticsearch.yml`](/deploy-manage/stack-settings.md):

        ```yaml
        xpack.security.remote_cluster_client.ssl.enabled: true
        xpack.security.remote_cluster_client.ssl.certificate_authorities: [ "remote-cluster-ca.crt" ]
        ```

    3. Add the cross-cluster API key, created on the remote cluster earlier, to the keystore:

        ```sh
        ./bin/elasticsearch-keystore add cluster.remote.ALIAS.credentials
        ```

        Replace `ALIAS` with the same alias that was used for cross-cluster operations before the migration. When prompted, enter the encoded cross-cluster API key created on the remote cluster earlier.

5. If you’ve dynamically configured the remote cluster (via the cluster settings API):

    1. Restart the local cluster to load changes to the keystore and settings.
    2. Re-add the remote cluster. Use the same remote cluster alias, and change the transport port into the remote cluster port. For example:

        ```console
        PUT /_cluster/settings
        {
          "persistent" : {
            "cluster" : {
              "remote" : {
                "my_remote" : { <1>
                  "mode": "proxy",
                  "proxy_address": "my.remote.cluster.com:9443" <2>
                }
              }
            }
          }
        }
        ```

        1. The remote cluster alias. Use the same alias that was used before the migration.
        2. The remote cluster address with the remote cluster port, which defaults to `9443`.

6. If you’ve statically configured the remote cluster (via [`elasticsearch.yml`](/deploy-manage/stack-settings.md)):

    1. Update the `cluster.remote` settings in `elasticsearch.yml` on each node of the local cluster. Change the port into the remote cluster port, which defaults to `9443`.
    2. Restart the local cluster to load changes to the keystore and settings.

7. Use the [remote cluster info API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-remote-info) to verify that the local cluster has successfully connected to the remote cluster:

    ```console
    GET /_remote/info
    ```

    The API response should indicate that the local cluster has connected to the remote cluster:

    ```console-result
    {
      "my_remote": {
        "connected": true, <1>
        "mode": "proxy",
        "proxy_address": "my.remote.cluster.com:9443",
        "server_name": "",
        "num_proxy_sockets_connected": 0,
        "max_proxy_socket_connections": 18,
        "initial_connect_timeout": "30s",
        "skip_unavailable": false,
        "cluster_credentials": "::es_redacted::" <2>
      }
    }
    ```

    1. The remote cluster is connected.
    2. If present, indicates the remote cluster has connected using API key authentication.



## Resume cross-cluster operations [remote-clusters-migration-resume]

Resume any persistent tasks that you stopped earlier. Tasks should be restarted by the same user or API key that created the task before the migration. Ensure the roles of this user or API key have been updated with the required `remote_indices` or `remote_cluster` privileges. For users, tasks capture the caller’s credentials when started and run in that user’s security context. For API keys, restarting a task will update the task with the updated API key.

* Use the [Start {{transform}}](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-transform-start-transform) API to start any transforms.
* Use the [Open jobs](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ml-open-job) API to open any anomaly detection jobs.
* Use the [Resume follower](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-resume-follow) API to resume any auto-follow {{ccr}}.
* Use the [Resume auto-follow pattern](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-ccr-resume-auto-follow-pattern) API to resume any manual {{ccr}} or existing indices that were created from the auto-follow pattern.


## Disable certificate based authentication and authorization [remote-clusters-migration-disable-cert]

::::{note}
Only proceed with this step if the migration has been proved successful on the local cluster. If the migration is unsuccessful, either [find out what the problem is and attempt to fix it](/troubleshoot/elasticsearch/remote-clusters.md) or [roll back](#remote-clusters-migration-rollback).
::::


Next, disable the certification based connection. Optionally, you can also revoke the authorization.

1. There is no particular setting to enable or disable a certificate based cross cluster connection, because it shares the same transport protocol with the intra-cluster node-to-node communication.

    One way a remote cluster administrator can stop an existing local cluster from connecting, is by changing TLS trust. The exact steps vary, depending on how the clusters have been configured. A generic solution is to [recreate the CA and certificate/key used by the remote transport interface](../security/secure-cluster-communications.md#encrypt-internode-communication) so that any existing certificate/key, locally or distributed, is no longer trusted.

    Another solution is to apply IP filters to the transport interface, blocking traffic from outside the cluster.

2. Optionally, delete any roles on the remote cluster that were only used for cross-cluster operations. These roles are no longer used under the API key based security model.


## Rollback [remote-clusters-migration-rollback]

If you need to roll back, follow these steps on the local cluster:

1. Stop any persistent tasks that refer to the remote cluster.
2. Remove the remote cluster definition by setting the remote cluster settings to `null`.
3. Remove the `remote_indices` or *remote_cluster* privileges from any roles that were updated during the migration.
4. On each node, remove the `remote_cluster_client.ssl.*` settings from `elasticsearch.yml`.
5. Restart the local cluster to apply changes to the keystore and `elasticsearch.yml`.
6. On the local cluster, apply the original remote cluster settings. If the remote cluster connection has been configured statically (using the `elasticsearch.yml` file), restart the cluster.
7. Use the [remote cluster info API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-cluster-remote-info) to verify that the local cluster has connected to the remote cluster. The response should have `"connected": true` and not have `"cluster_credentials": "::es_redacted::"`.
8. Restart any persistent tasks that you’ve stopped earlier.


