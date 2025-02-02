# Bootstrap Checks for {{xpack}} [bootstrap-checks-xpack]

In addition to the [{{es}} bootstrap checks](../../../deploy-manage/deploy/self-managed/bootstrap-checks.md), there are checks that are specific to {{xpack}} features.


## Encrypt sensitive data check [bootstrap-checks-xpack-encrypt-sensitive-data] 

If you use {{watcher}} and have chosen to encrypt sensitive data (by setting `xpack.watcher.encrypt_sensitive_data` to `true`), you must also place a key in the secure settings store.

To pass this bootstrap check, you must set the `xpack.watcher.encryption_key` on each node in the cluster. For more information, see [Encrypting sensitive data in Watcher](../../../explore-analyze/alerts/watcher/encrypting-data.md).


## PKI realm check [bootstrap-checks-xpack-pki-realm] 

If you use {{es}} {security-features} and a Public Key Infrastructure (PKI) realm, you must configure Transport Layer Security (TLS) on your cluster and enable client authentication on the network layers (either transport or http). For more information, see [PKI user authentication](../../../deploy-manage/users-roles/cluster-or-deployment-auth/pki.md) and [Set up basic security plus HTTPS](../../../deploy-manage/security/set-up-basic-security-plus-https.md).

To pass this bootstrap check, if a PKI realm is enabled, you must configure TLS and enable client authentication on at least one network communication layer.


## Role mappings check [bootstrap-checks-xpack-role-mappings] 

If you authenticate users with realms other than `native` or `file` realms, you must create role mappings. These role mappings define which roles are assigned to each user.

If you use files to manage the role mappings, you must configure a YAML file and copy it to each node in the cluster. By default, role mappings are stored in `ES_PATH_CONF/role_mapping.yml`. Alternatively, you can specify a different role mapping file for each type of realm and specify its location in the `elasticsearch.yml` file. For more information, see [Using role mapping files](../../../deploy-manage/users-roles/cluster-or-deployment-auth/mapping-users-groups-to-roles.md#mapping-roles-file).

To pass this bootstrap check, the role mapping files must exist and must be valid. The Distinguished Names (DNs) that are listed in the role mappings files must also be valid.


## SSL/TLS check [bootstrap-checks-tls] 

If you enable {{es}} {security-features}, unless you have a trial license, you must configure SSL/TLS for internode-communication.

::::{note} 
Single-node clusters that use a loopback interface do not have this requirement. For more information, see [*Start the {{stack}} with security enabled automatically*](../../../deploy-manage/security/security-certificates-keys.md).
::::


To pass this bootstrap check, you must [set up SSL/TLS in your cluster](../../../deploy-manage/security/set-up-basic-security.md#encrypt-internode-communication).


## Token SSL check [bootstrap-checks-xpack-token-ssl] 

If you use {{es}} {security-features} and the built-in token service is enabled, you must configure your cluster to use SSL/TLS for the HTTP interface. HTTPS is required in order to use the token service.

In particular, if `xpack.security.authc.token.enabled` is set to `true` in the `elasticsearch.yml` file, you must also set `xpack.security.http.ssl.enabled` to `true`. For more information about these settings, see [Security settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html) and [Advanced HTTP settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/modules-network.html#http-settings).

To pass this bootstrap check, you must enable HTTPS or disable the built-in token service.

