# Secure your clusters with Active Directory [ece-securing-clusters-ad]

These steps show how you can secure your {{es}} clusters and Kibana instances with the Lightweight Directory Access Protocol (LDAP) using an Active Directory.


## Before you begin [ece_before_you_begin_18]

To learn more about how securing {{es}} clusters with Active Directory works, check [Active Directory user authentication](https://www.elastic.co/guide/en/elasticsearch/reference/current/active-directory-realm.html).

::::{note}
The AD credentials are valid against the deployment, not the ECE platform. You can configure [role-based access control](../../../deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md) for the platform separately.
::::



## Configure authentication with Active Directory [ece-securing-clusters-ad-configuration]

You can configure the deployment to authenticate users by communicating with an Active Directory Domain Controller. To integrate with Active Directory, you need to configure an `active_directory` realm and map Active Directory groups to user roles in {{es}}.

Contrary to the `ldap` realm, the `active_directory` realm only supports a user search mode, but you can choose whether to use a bind user.


### Configure an Active Directory realm without a bind user [ece-ad-configuration-without-bind-user]

The Active Directory realm authenticates users using an LDAP bind request. By default, all LDAP operations run as the authenticated user if you don’t specify a `bind_dn`. Alternatively, you can choose to [configure your realm with a bind user](../../../deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md#ece-ad-configuration-with-bind-user).

1. [Add your user settings](../../../deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) for the `active_directory` realm as follows:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            active_directory:
              my_ad:
                order: 2 <1>
                domain_name: ad.example.com <2>
                url: ldap://ad.example.com:389 <3>
    ```

    1. The order in which the `active_directory` realm is consulted during an authentication attempt.
    2. The primary domain in Active Directory. Binding to Active Directory fails if the domain name is not mapped in DNS.
    3. The LDAP URL pointing to the Active Directory Domain Controller that should handle authentication. If your Domain Controller is configured to use LDAP over TLS and it uses a self-signed certificate or a certificate that is signed by your organization’s CA, refer to [using self-signed certificates](../../../deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md#ece-ad-configuration-encrypt-communications).



### Configure an Active Directory realm with a bind user [ece-ad-configuration-with-bind-user]

You can choose to configure an Active Directory realm using a bind user. When you specify a `bind_dn`, this specific user is used to search for the Distinguished Name (`DN`) of the authenticating user based on the provided username and an LDAP attribute. If found, this user is authenticated by attempting to bind to the LDAP server using the found `DN` and the provided password.

1. [Add your user settings](../../../deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) for the `active_directory` realm as follows:

    ::::{important}
    You must apply the user settings to each [deployment template](../../../deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md).
    ::::


    ```sh
    xpack:
      security:
        authc:
          realms:
            active_directory:
              my_ad:
                order: 2 <1>
                domain_name: ad.example.com <2>
                url: ldap://ad.example.com:389 <3>
                bind_dn: es_svc_user@ad.example.com <4>
    ```

    1. The order in which the `active_directory` realm is consulted during an authentication attempt.
    2. The primary domain in Active Directory. Binding to Active Directory fails if the domain name is not mapped in DNS.
    3. The LDAP URL pointing to the Active Directory Domain Controller that should handle authentication. If your Domain Controller is configured to use LDAP over TLS and it uses a self-signed certificate or a certificate that is signed by your organization’s CA, refer to [using self-signed certificates](../../../deploy-manage/users-roles/cluster-or-deployment-auth/active-directory.md#ece-ad-configuration-encrypt-communications).
    4. The user to run as for all Active Directory search requests.

2. Configure the password for the `bind_dn` user by adding the appropriate `secure_bind_password` setting to the {{es}} keystore.

    1. From the **Deployments** page, select your deployment.

        Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

    2. From your deployment menu, select **Security**.
    3. Under the **{{es}} keystore** section, select **Add settings**.
    4. On the **Create setting** window, select the secret **Type** to be `Secret String`.
    5. Set the **Setting name** to `xpack.security.authc.realms.active_directory.<my_ad>.secure_bind_password` and add the password for the `bind_dn` user in the `secret` field.

        ::::{warning}
        After you configure `secure_bind_password`, any attempt to restart the deployment will fail until you complete the rest of the configuration steps. If you wish to rollback the Active Directory realm related configuration effort, you need to remove the `xpack.security.authc.realms.active_directory.my_ad.secure_bind_password` that was just added by clicking **Remove** by the setting name under `Existing Keystores`.
        ::::



### Using self-signed certificates [ece-ad-configuration-encrypt-communications]

If your LDAP server uses a self-signed certificate or a certificate that is signed by your organization’s CA, you need to enable the deployment to trust this certificate. These steps are required only if TLS is enabled and the Active Directory controller is using self-signed certificates.

You’ll prepare a custom bundle that contains your certificate [in the same way that you would on {{ess}}](https://www.elastic.co/guide/en/cloud/current/ec-custom-bundles.html). Custom bundles are extracted in the path `/app/config/BUNDLE_DIRECTORY_STRUCTURE`, where `BUNDLE_DIRECTORY_STRUCTURE` is the directory structure within the bundle ZIP file itself. For example:

```sh
$ tree .
.
└── adcert
      └── ca.crt
```

In the following example, the keystore file would be extracted to `/app/config/adcert/ca.crt`, where `ca.crt` is the name of the certificate.

::::{admonition} Certificate formats
The following example uses a PEM encoded certificate. If your CA certificate is available as a `JKS` or `PKCS#12` keystore, you can upload that file in a ZIP bundle and reference it in the user settings. For example, you can create a ZIP file from a `truststore` folder that contains a keystore named `ca.p12` and reference that file:

```yaml
xpack.security.authc.realms.active_directory.my_ad.ssl.truststore.path:
"/app/config/truststore/ca.p12"
```

If the keystore is also password protected (which isn’t typical for keystores that only contain CA certificates), you can also provide the password for the keystore by adding `xpack.security.authc.realms.active_directory.my_ad.ssl.truststore.password: password` in the user settings.

::::


1. Create a ZIP file that contains your CA certificate file, such as `adcert.zip`.
2. Update your plan in the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md) so that it uses the bundle you prepared in the previous step. You need to modify the `user_bundles` JSON attribute similar to the following example:

    ::::{note}
    You must specify the `user_bundles` attribute for each [deployment template](../../../deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md). You can alter `7.*` to `8.*` when needed.
    ::::


    ```json
    {
    "cluster_name": "REPLACE_WITH_YOUR_CLUSTER_NAME",
    "plan": {

        ...

        "elasticsearch": {
          "version": "7.*",
          "user_bundles": [
            {
              "name": "adcert",
              "url": "https://www.myurl.com/adcert.zip", <1>
              "elasticsearch_version": "7.*" <2>
            }
          ]
        }
      }
    ```

    1. The URL that points to the `adcert.zip` file must be accessible to the cluster. Uploaded files are stored using Amazon’s highly-available S3 service.
    2. This bundle is compatible with any {{es}} `7.*` version.::::{tip}
    Using a wildcard for the minor version ensures that the bundle is compatible with the specified {{es}} major version, and eliminates the need to upload a new bundle when upgrading to a new minor version.
    ::::

3. Update [your user settings](../../../deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) for the `active_directory` realm as follows:

    ```yaml
    xpack:
      security:
        authc:
          realms:
            active_directory:
              my_ad:
                order: 2
                domain_name: ad.example.com
                url: /app/config/adcert/ca.crt <1>
                bind_dn: es_svc_user@ad.example.com
                ssl:
                  certificate_authorities: ["/app/config/cacerts/ca.crt"]
    ```

    1. The `ldaps` URL pointing to the Active Directory Domain Controller.


    The `ssl.verification_mode` setting (not shown) indicates the type of verification to use when using `ldaps` to protect against man-in-the-middle attacks and certificate forgery. The value for this property defaults to `full`. When you configure {{es}} to connect to a Domain Controller using TLS, it attempts to verify the hostname or IP address specified by the `url` attribute in the realm configuration with the Subject Alternative Names (SAN) in the certificate. If the SAN values in the certificate and realm configuration don’t match, {{es}} does not allow a connection to the Domain Controller. You can disable this behavior by setting the `ssl. verification_mode` property to `certificate`.



## Mapping Active Directory groups to roles [ece-securing-clusters-ad-role-mapping]

You have two ways of mapping Active Directory groups to roles for your users. The preferred one is to use the [role mapping API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-put-role-mapping). If for some reason this is not possible, you can use a [role mapping file](https://www.elastic.co/guide/en/elasticsearch/reference/current/mapping-roles.html) to specify the mappings instead.

::::{important}
Only Active Directory security groups are supported. You cannot map distribution groups to roles.
::::



### Using the Role Mapping API [ece_using_the_role_mapping_api_2]

Let’s assume that you want all your users that authenticate through AD to have read-only access to a certain index `my-index` and the AD users that are members of the `cn=administrators, dc=example, dc=com` group in LDAP, to become superusers in your deployment:

1. Create the read-only role

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

2. Create the relevant role mapping rule for read only users

    ```sh
    POST /_security/role_mapping/ad-read-only <1>
    {
    "enabled": true,
    "roles": [ "read-only-my-index" ], <2>
    "rules": {
    "field": { "realm.name": "my_ad" } <3>
    },
    "metadata": { "version": 1 }
    }
    ```

    1. The name of the role mapping.
    2. The name of the role we created earlier.
    3. The name of our Active Directory realm.

3. Create the relevant role mapping rule for superusers

    ```sh
    POST /_security/role_mapping/ldap-superuser <1>
    {
    "enabled": true,
    "roles": [ "superuser" ], <2>
    "rules": {
    "all" : [
    { "field": { "realm.name": "my_ad" } },<3>
    { "field": { "groups": "cn=administrators, dc=example, dc=com" } }<4>
        ]
    },
    "metadata": { "version": 1 }
    }
    ```

    1. The name of the role mapping.
    2. The name of the role we want to assign, in this case `superuser`.
    3. The name of our active_directory realm.
    4. The DN of the AD group whose members should get the `superuser` role in the deployment.



### Using the Role Mapping files [ece_using_the_role_mapping_files_2]

Let’s assume that you want all your users that authenticate through AD and are members of the `cn=my-users,dc=example, dc=com` group in AD to have read-only access to a certain index `my-index` and only the users `cn=Senior Manager, cn=management, dc=example, dc=com` and `cn=Senior Admin, cn=management, dc=example, dc=com` to become superusers in your deployment:

1. Create a file named `role-mappings.yml` with the following contents:

    ```sh
    superuser:
    - cn=Senior Manager, cn=management, dc=example, dc=com
    - cn=Senior Admin, cn=management, dc=example, dc=com
    read-only-user:
    - cn=my-users, dc=example, dc=com
    ```

2. Prepare the custom bundle ZIP file `mappings.zip`, that contains the `role-mappings.yml` file [in the same way that you would on Elastic Cloud](https://www.elastic.co/guide/en/cloud/current/ec-custom-bundles.html).
3. Custom bundles get unzipped under the path `/app/config/BUNDLE_DIRECTORY_STRUCTURE`, where `BUNDLE_DIRECTORY_STRUCTURE` is the directory structure within the bundle ZIP file itself. For example:

    ```sh
    $ tree .
    .
    └── mappings
          └── role-mappings.yml
    ```

    In our example, the role mappings file is extracted to `/app/config/mappings/role-mappings.yml`

4. Update your plan in the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md) so that it uses the bundle you prepared in the previous step. Modify the `user_bundles` JSON attribute as shown in the following example:

    ::::{note}
    You must specify the `user_bundles` attribute for each [deployment template](../../../deploy-manage/deploy/cloud-enterprise/configure-deployment-templates.md). You can alter `7.*` to `8.*` when needed.
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
            active_directory:
              my_ad:
                order: 2
                domain_name: ad.example.com
                url: ldaps://ad.example.com:636 <1>
                bind_dn: es_svc_user@ad.example.com
                ssl:
                  certificate_authorities: ["/app/config/cacerts/ca.crt"]
                  verification_mode: certificate
                files:
                  role_mapping: "/app/config/mappings/role-mappings.yml" <1>
    ```

    1. The path where our role mappings file is unzipped.


