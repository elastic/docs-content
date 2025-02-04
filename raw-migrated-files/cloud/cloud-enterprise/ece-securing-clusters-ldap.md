# Secure your clusters with LDAP [ece-securing-clusters-ldap]

These steps show how you can secure your {{es}} clusters and Kibana instances with the Lightweight Directory Access Protocol (LDAP) using an LDAP server.


## Before you begin [ece_before_you_begin_17]

To learn more about how securing {{es}} clusters with LDAP works, check [LDAP user authentication](https://www.elastic.co/guide/en/elasticsearch/reference/current/ldap-realm.html).

::::{note}
The LDAP credentials are valid against the deployment, not the ECE platform. You can configure [role-based access control](../../../deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md) for the platform separately.
::::



## Configure authentication with LDAP [ece-securing-clusters-ldap-configuration]

You can configure the deployment to authenticate users by communicating with an LDAP server. To integrate with LDAP, you need to configure an `ldap` realm and map LDAP groups to user roles in {{es}}.

1. Determine which mode you want to use. The `ldap` realm supports two modes of operation, a user search mode and and a mode with specific templates for user DNs.

    LDAP user search is the most common mode of operation. In this mode, a specific user with permission to search the LDAP directory is used to search for the DN of the authenticating user based on the provided username and an LDAP attribute. Once found, the user is authenticated by attempting to bind to the LDAP server using the found DN and the provided password.

    If your LDAP environment uses a few specific standard naming conditions for users, you can use user DN templates to configure the realm. The advantage of this method is that a search does not have to be performed to find the user DN. However, multiple bind operations might be needed to find the correct user DN.

2. To configure an LDAP realm with user search, [add your user settings](../../../deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) for the `ldap` realm as follows:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            ldap:
              ldap1:
                order: 2 <1>
                url: "ldap://ldap.example.com:389" <2>
                bind_dn: "cn=ldapuser, ou=users, o=services, dc=example, dc=com" <3>
                user_search:
                  base_dn: "ou=users, o=services, dc=example, dc=com" <4>
                  filter: "(cn=\{0})" <5>
                group_search:
                  base_dn: "ou=groups, o=services, dc=example, dc=com" <6>
    ```

    1. The order in which the LDAP realm will be consulted during an authentication attempt.
    2. The LDAP URL pointing to the LDAP server that should handle authentication. If your LDAP server is configured to use LDAP over TLS and it uses a self-signed certificate or a certificate that is signed by your organization’s CA, refer to the following configuration instructions.
    3. The DN of the bind user.
    4. The base DN under which your users are located in LDAP.
    5. Optionally specify an additional LDAP filter used to search the directory in attempts to match an entry with the username provided by the user. Defaults to `(uid={{0}})`. `{{0}}` is substituted with the username provided by the user for authentication.
    6. The base DN under which groups are located in LDAP.


::::{warning}
You must apply the user settings to each [deployment template](../../../deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md).
::::


1. The password for the `bind_dn` user should be configured by adding the appropriate `secure_bind_password` setting to the {{es}} keystore.

    1. From the **Deployments** page, select your deployment.

        Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

    2. From your deployment menu, select **Security**.
    3. Under the **Elasticsearch keystore** section, select **Add settings**.
    4. On the **Create setting** window, select the secret **Type** to be `Secret String`.
    5. Set the **Setting name**` to `xpack.security.authc.realms.ldap.ldap1.secure_bind_password` and add the password for the `bind_dn` user in the `secret` field.

        ::::{note}
        After you configure secure_bind_password, any attempt to restart the deployment will fail until you complete the rest of the configuration steps. If you wish to rollback the LDAP realm related configuration effort, you need to remove the `xpack.security.authc.realms.ldap.ldap1.secure_bind_password` that was just added by using the "remove" button by the setting name under `Existing Keystores`.
        ::::

2. Alternatively, to configure an LDAP realm with user user DN templates, [add your user settings](../../../deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) for the `ldap` realm as follows:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            ldap:
              ldap1:
                order: 2 <1>
                url: "ldap://ldap.example.com:389" <2>
                user_dn_templates: <3>
                  - "uid={0}, ou=users, o=engineering, dc=example, dc=com"
                  - "uid={0}, ou=users, o=marketing, dc=example, dc=com"
                group_search:
                  base_dn: ou=groups, o=services, dc=example, dc=com" <4>
    ```

    1. The order in which the LDAP realm will be consulted during an authentication attempt.
    2. The LDAP URL pointing to the LDAP server that should handle authentication. If your LDAP server is configured to use LDAP over TLS and it uses a self-signed certificate or a certificate that is signed by your organization’s CA, refer to the following configuration instructions.
    3. The templates that should be tried for constructing the user DN and authenticating to LDAP. If a user attempts to authenticate with username `user1` and password `password1`, authentication will be attempted with the DN `uid=user1, ou=users, o=engineering, dc=example, dc=com` and if not successful, also with `uid=user1, ou=users, o=marketing, dc=example, dc=com` and the given password. If authentication with one of the constructed DNs is successful, all subsequent LDAP operations are run with this user.
    4. The base DN under which groups are located in LDAP.

3. (Optional) Encrypt communications between the deployment and the LDAP Server. If your LDAP server uses a self-signed certificate or a certificate that is signed by your organization’s CA, you need to enable the deployment to trust this certificate.

    1. Prepare the custom bundle ZIP file `ldapcert.zip`, that contains the CA certificate file (for example `ca.crt`) [in the same way that you would on Elastic Cloud](https://www.elastic.co/guide/en/cloud/current/ec-custom-bundles.html).
    2. Custom bundles are unzipped under the path `/app/config/BUNDLE_DIRECTORY_STRUCTURE`, where `BUNDLE_DIRECTORY_STRUCTURE` is the directory structure within the bundle ZIP file itself. For example:

        ```sh
        $ tree .
        .
        └── ldapcert
              └── ca.crt
        ```

        In our example, the unzipped keystore file is extracted to `/app/config/ldapcert/ca.crt`, where `ca.cert` is the name of the certificate.

    3. Update your plan in the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md) so that it uses the bundle you prepared in the previous step. Modify the `user_bundles` JSON attribute as shown in the following example:

        ::::{note}
        You must specify the `user_bundles` attribute for each [deployment template](../../../deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md). Switch version `7.*` to the version `8.*` if needed.
        ::::


        ```yaml
        {
        "cluster_name": "REPLACE_WITH_YOUR_CLUSTER_NAME",
        "plan": {

            ...

            "elasticsearch": {
              "version": "7.*",
              "user_bundles": [
                {
                  "name": "ldap-cert",
                  "url": "https://www.myurl.com/ldapcert.zip", <1>
                  "elasticsearch_version": "7.*" <2>
                }
              ]
            }
          }
        ```

        1. The URL that points to `ldapcert.zip` must be accessible to the cluster.
        2. The bundle is compatible with any {{es}} `7.*` version.


        ::::{tip}
        Using a wildcard for the minor version ensures bundles are compatible with the stated {{es}} major version to avoid a need to re-upload a new bundle with minor versions upgrades.
        ::::

    4. Update [your user settings](../../../deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) for the `ldap` realm as follows:

        ```yaml
        xpack:
          security:
            authc:
              realms:
                ldap:
                  ldap1:
                    order: 2
                    url: "ldaps://ldap.example.com:636" <1>
                    bind_dn: "cn=ldapuser, ou=users, o=services, dc=example, dc=com"
                    user_search:
                      base_dn: "ou=users, o=services, dc=example, dc=com"
                    group_search:
                      base_dn: ou=groups, o=services, dc=example, dc=com"
                    ssl:
                      verification_mode: certificate <2>
                      certificate_authorities: ["/app/config/cacert/ca.crt"]
        ```

        1. The `ldaps` URL pointing to the LDAP server.
        2. (Optional) By default, when you configure {{es}} to connect to an LDAP server using SSL/TLS, it attempts to verify the hostname or IP address specified with the url attribute in the realm configuration with the values in the certificate. If the values in the certificate and realm configuration do not match, {{es}} does not allow a connection to the LDAP server. This is done to protect against man-in-the-middle attacks. If necessary, you can disable this behavior by setting the `ssl.verification_mode` property to `certificate`.


::::{note}
If your CA certificate is available as a `JKS` or `PKCS#12` keystore, you can upload that file in the ZIP bundle (for example create a ZIP archive from a `truststore` folder that contains a file named `ca.jks`) and then reference it in the user settings with `xpack.security.authc.realms.ldap.ldap1.ssl.truststore.path: "/app/config/truststore/ca.jks"`. If the keystore is also password protected which is unusual for keystores that contain only CA certificates, you can also provide the password for the keystore by adding `xpack.security.authc.realms.ldap.ldap1.ssl.truststore.password: password` in the user settings.
::::



## Mapping LDAP groups to roles [ece-securing-clusters-ldap-role-mapping]

You have two ways of mapping LDAP groups to roles for your users. The preferred one is to use the [role mapping API](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-api-put-role-mapping.html). If for some reason this is not possible, you can use a [role mapping file](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-roles.html) to specify the mappings instead.


### Using the Role Mapping API [ece_using_the_role_mapping_api]

Let’s assume that you want all your users that authenticate through LDAP to have read-only access to a certain index `my-index` and the LDAP users that are members of the `cn=administrators, ou=groups, o=services, dc=example, dc=com` group in LDAP, to become superusers in your deployment:

1. Create the read-only role.

    ```sh
    POST /_security/role/read-only-my-index <1>
    {
      "indices": [
        {
          "names": [ "my-index" ],
          "privileges": [ "read" ]
        }
      ]
    }
    ```

    1. The name of the role.

2. Create the relevant role mapping rule for read-only users.

    ```sh
    POST /_security/role_mapping/ldap-read-only <1>
    {
      "enabled": true,
      "roles": [ "read-only-my-index" ], <2>
      "rules": {
        "field": { "realm.name": "ldap1" } <3>
        },
      "metadata": { "version": 1 }
    }
    ```

    1. The name of the role mapping.
    2. The name of the role we created earlier.
    3. The name of our LDAP realm.

3. Create the relevant role mapping rule for superusers.

    ```sh
    POST /_security/role_mapping/ldap-superuser <1>
    {
      "enabled": true,
      "roles": [ "superuser" ], <2>
      "rules": {
        "all" : [
          { "field": { "realm.name": "ldap1" } },<3>
          { "field": { "groups": "cn=administrators, ou=groups, o=services, dc=example, dc=com" } }<4>
        ]
      },
      "metadata": { "version": 1 }
    }
    ```

    1. The name of the role mapping.
    2. The name of the role we want to assign, in this case `superuser`.
    3. The name of our LDAP realm.
    4. The DN of the LDAP group whose members should get the `superuser` role in the deployment.



### Using the Role Mapping files [ece_using_the_role_mapping_files]

Let’s assume that you want all your users that authenticate through LDAP and are members of the `cn=my-users, ou=groups, o=services, dc=example, dc=com` group in LDAP to have read-only access to a certain index `my-index` and only the users `cn=Senior Manager, ou=users, o=services, dc=example, dc=com` and `cn=Senior Admin, ou=users, o=services, dc=example, dc=com` to become superusers in your deployment:

1. Create a file named `role-mappings.yml` with the following contents:

    ```sh
    superuser:
      - cn=Senior Manager, ou=users, o=services, dc=example, dc=com
      - cn=Senior Admin, ou=users, o=services, dc=example, dc=com
    read-only-user:
      - cn=my-users, ou=groups, o=services, dc=example, dc=com
    ```

2. Prepare the custom bundle ZIP file `mappings.zip`, that contains the `role-mappings.yml` file [in the same way that you would on Elastic Cloud](https://www.elastic.co/guide/en/cloud/current/ec-custom-bundles.html).
3. Custom bundles are unzipped under the path `/app/config/BUNDLE_DIRECTORY_STRUCTURE`, where `BUNDLE_DIRECTORY_STRUCTURE` is the directory structure within the bundle ZIP file itself. For example:

    ```sh
    $ tree .
    .
    └── mappings
          └── role-mappings.yml
    ```

    In our example, the file is extracted to `/app/config/mappings/role-mappings.yml`.

4. Update your plan in the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md) so that it uses the bundle you prepared in the previous step. Modify the `user_bundles` JSON attribute as shown in the following example:

    ::::{note}
    You must specify the `user_bundles` attribute for each [deployment template](../../../deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md). Switch `7.*` to `8.*` if needed.
    ::::


    ```sh
    {
    "cluster_name": "REPLACE_WITH_YOUR_CLUSTER_NAME",
    "plan": {

        ...

        "elasticsearch": {
          "version": "7.*",
          "user_bundles": [
            {
              "name": "role-mappings",
              "url": "https://www.myurl.com/mappings.zip", <1>
              "elasticsearch_version": "7.*" <2>
            }
          ]
        }
      }
    ```

    1. The URL that points to `mappings.zip` must be accessible to the cluster.
    2. The bundle is compatible with any {{es}} `7.*` version.


    ::::{tip}
    Using a wildcard for the minor version ensures bundles are compatible with the stated {{es}} major version to avoid the need to re-upload a new bundle with minor versions upgrades.
    ::::

5. Update [your user settings](../../../deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) for the `ldap` realm as follows:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            ldap:
              ldap1:
                order: 2
                url: "ldaps://ldap.example.com:636"
                bind_dn: "cn=ldapuser, ou=users, o=services, dc=example, dc=com"
                user_search:
                  base_dn: "ou=users, o=services, dc=example, dc=com"
                group_search:
                  base_dn: ou=groups, o=services, dc=example, dc=com"
                ssl:
                  verification_mode: certificate
                  certificate_authorities: ["/app/config/cacerts/ca.crt"]
                files:
                  role_mapping: "/app/config/mappings/role-mappings.yml" <1>
    ```

    1. The path where our role mappings file is unzipped.


