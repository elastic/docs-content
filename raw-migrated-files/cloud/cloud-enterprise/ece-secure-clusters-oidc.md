# Secure your clusters with OpenID Connect [ece-secure-clusters-oidc]

You can secure your deployment using OpenID Connect for single sign-on. OpenID Connect is an identity layer on top of the OAuth 2.0 protocol. The end user identity gets verified by an authorization server and basic profile information is sent back to the client.

::::{note}
The OpenID Connect credentials are valid against the deployment, not the ECE platform. You can configure [role-based access control](../../../deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md) for the platform separately.
::::



## Before you begin [ece_before_you_begin_19]

To prepare for using OpenID Connect for authentication for deployments:

* Create or use an existing deployment. Make note of the Kibana endpoint URL, it will be referenced as `<KIBANA_ENDPOINT_URL>` in the following steps.
* The steps in this section required a moderate understanding of [OpenID Connect](https://openid.net/specs/openid-connect-core-1_0.md#Authentication) in general and the Authorization Code Grant flow specifically. For more information about OpenID Connect and how it works with the Elastic Stack check:

    * Our [configuration guide for Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/oidc-guide-authentication.html).



## Configure the OpenID Connect Provider [ece-configure-oidc-provider]

The OpenID *Connect Provider* (OP) is the entity in OpenID Connect that is responsible for authenticating the user and for granting the necessary tokens with the authentication and user information to be consumed by the *Relying Parties* (RP).

In order for Elastic Cloud Enterprise (acting as an RP) to be able use your OpenID Connect Provider for authentication, a trust relationship needs to be established between the OP and the RP. In the OpenID Connect Provider, this means registering the RP as a client.

The process for registering the Elastic Cloud Enterprise RP will be different from OP to OP and following the provider’s relevant documentation is prudent. The information for the RP that you commonly need to provide for registration are the following:

`Relying Party Name`
:   An arbitrary identifier for the relying party. Neither the specification nor our implementation impose any constraints on this value.

`Redirect URI`
:   This is the URI where the OP will redirect the user’s browser after authentication. The appropriate value for this is `<KIBANA_ENDPOINT_URL>/api/security/oidc/callback`. This can also be called the `Callback URI`.

At the end of the registration process, the OP assigns a Client Identifier and a Client Secret for the RP (Elastic Cloud Enterprise) to use. Note these two values as they are used in the cluster configuration.


## Configure your cluster to use OpenID Connect [ece-secure-deployment-oidc]

You’ll need to [add the client secret](../../../deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#ece-oidc-client-secret) to the keystore and then [update the Elasticsearch user settings](../../../deploy-manage/users-roles/cluster-or-deployment-auth/openid-connect.md#ece-oidc-user-settings) to refer to that secret and use the OpenID Connect realm.


### Configure the Client Secret [ece-oidc-client-secret]

Configure the Client Secret that was assigned to the PR by the OP during registration to the Elasticsearch keystore.

This is a sensitive setting, it won’t be stored in plaintext in the cluster configuration but rather as a secure setting. In order to do so, follow these steps:

1. On the deployments page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

2. From your deployment menu, select **Security**.
3. Under the **Elasticsearch keystore** section, select **Add settings**.
4. On the **Create setting** window, select the secret **Type** to be `Single string`.
5. Set the **Setting name**` to `xpack.security.authc.realms.oidc.<oidc-realm-name>.rp.client_secret` and add the Client Secret you received from the OP during registration in the `Secret` field.

    ::::{note}
    `<oidc-realm-name>` refers to the name of the OpenID Connect Realm. You can select any name that contains alphanumeric characters, underscores and hyphens. Replace `<oidc-realm-name>` with the realm name you selected.
    ::::


    ::::{note}
    After you configure the Client Secret, any attempt to restart the deployment will fail until you complete the rest of the configuration steps. If you wish to rollback the OpenID Connect related configuration effort, you need to remove the `xpack.security.authc.realms.oidc.<oidc-realm-name>.rp.client_secret` that was just added by using the "remove" button by the setting name under `Security keys`.
    ::::

6. You must also edit your cluster configuration, sometimes also referred to as the deployment plan, in order to add the appropriate settings.


### Configure the user settings [ece-oidc-user-settings]

The Elasticsearch cluster needs to be configured to use the OpenID Connect realm for user authentication and to map the applicable roles to the users. If you are using machine learning or a deployment with hot-warm architecture, you must include this OpenID Connect related configuration in the user settings section for each node type.

1. [Update your Elasticsearch user settings](../../../deploy-manage/deploy/cloud-enterprise/edit-stack-settings.md) for the `oidc` realm and specify the relevant configuration:

    ```sh
    xpack:
      security:
        authc:
          realms:
            oidc:
              oidc1: <1>
                order: 2 <2>
                rp.client_id: "client-id" <3>
                rp.response_type: "code"
                rp.redirect_uri: "<KIBANA_ENDPOINT_URL>/api/security/oidc/callback" <4>
                op.issuer: "<check with your OpenID Connect Provider>" <5>
                op.authorization_endpoint: "<check with your OpenID Connect Provider>" <6>
                op.token_endpoint: "<check with your OpenID Connect Provider>" <7>
                op.userinfo_endpoint: "<check with your OpenID Connect Provider>" <8>
                op.jwkset_path: "<check with your OpenID Connect Provider>" <9>
                claims.principal: sub <10>
                claims.groups: "http://example.info/claims/groups" <11>
    ```

    1. The `oidc` realm name: `cloud-oidc` is reserved for internal use only and can’t be used. Please select another name, as shown here.
    2. The order of the OpenID Connect realm in your authentication chain. Allowed values are between `2` and `100`. Set to `2` unless you plan on configuring multiple SSO realms for this cluster.
    3. This, usually opaque, arbitrary string, is the Client Identifier that was assigned to the Elastic Cloud Enterprise RP by the OP upon registration.
    4. Replace `<KIBANA_ENDPOINT_URL>` with the value noted in the previous step
    5. A url, used as a unique identifier for the OP. The value for this setting should be provided by your OpenID Connect Provider.
    6. The URL for the Authorization Endpoint in the OP. This is where the user’s browser will be redirected to start the authentication process. The value for this setting should be provided by your OpenID Connect Provider.
    7. The URL for the Token Endpoint in the OpenID Connect Provider. This is the endpoint where Elastic Cloud Enterprise will send a request to exchange the code for an ID Token, as part of the Authorization Code flow. The value for this setting should be provided by your OpenID Connect Provider.
    8. (Optional) The URL for the UserInfo Endpoint in the OpenID Connect Provider. This is the endpoint of the OP that can be queried to get further user information, if required. The value for this setting should be provided by your OpenID Connect Provider.
    9. The path to a file or an HTTPS URL pointing to a JSON Web Key Set with the key material that the OpenID Connect Provider uses for signing tokens and claims responses. Your OpenID Connect Provider should provide you with this file.
    10. Defines the OpenID Connect claim that is going to be mapped to the principal (username) of the authenticated user in Kibana. In this example, we map the value of the `sub` claim, but this is not a requirement, other claims can be used too. Check [the claims mapping documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/oidc-guide-authentication.html#oidc-claims-mapping) for details and available options.
    11. Defines the OpenID Connect claim that is going to be used for role mapping. Note that the value `"http://example.info/claims/groups"` that is used here, is an arbitrary example. Check  [the claims mapping documentation](https://www.elastic.co/guide/en/elasticsearch/reference/current/oidc-guide-authentication.html#oidc-claims-mapping) for a very detailed description of how the claim mapping works and how can these be used for role mapping. The name of this claim should be determined by the configuration of your OpenID Connect Provider. NOTE: According to the OpenID Connect specification, the OP should also make their configuration available at a well known URL, which is the concatenation of their `Issuer` value with the `.well-known/openid-configuration` string. To configure the OpenID Connect realm, refer to the `https://op.org.com/.well-known/openid-configuration` documentation.

2. By default, users authenticating through OpenID Connect have no roles assigned to them. For example, if you want all your users authenticating with OpenID Connect to get access to Kibana, issue the following request to Elasticsearch:

    ```sh
    POST /_security/role_mapping/CLOUD_OIDC_TO_KIBANA_ADMIN <1>
    {
       "enabled": true,
        "roles": [ "kibana_admin" ], <2>
        "rules": { <3>
            "field": { "realm.name": "oidc-realm-name" } <4>
        },
        "metadata": { "version": 1 }
    }
    ```

    1. The name of the new role mapping.
    2. The role mapped to the users.
    3. The fields to match against.
    4. The name of the OpenID Connect realm. This needs to be the same value as the one used in the cluster configuration.

3. Update Kibana in the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md) to use OpenID Connect as the authentication provider:

    ```sh
    xpack.security.authc.providers:
      oidc.oidc1:
        order: 0
        realm: oidc-realm-name <1>
    ```

    1. The name of the OpenID Connect realm. This needs to be the same value as the one used in the cluster configuration.


    This configuration disables all other realms and only allows users to authenticate with OpenID Connect. If you wish to allow your native realm users to authenticate, you need to also enable the `basic` `provider` like this:

    ```sh
    xpack.security.authc.providers:
      oidc.oidc1:
        order: 0
        realm: oidc-realm-name
        description: "Log in with my OpenID Connect" <1>
      basic.basic1:
        order: 1
    ```

    1. This arbitrary string defines how OpenID Connect login is titled in the Login Selector UI that is shown when you enable multiple authentication providers in Kibana. If you have a Kibana instance, you can also configure the optional `icon` and `hint` settings for any authentication provider.

4. Optional: If your OpenID Connect Provider doesn’t publish its JWKS at an https URL, or if you want to use a local copy, you can upload the JWKS as a file.

    1. Prepare a ZIP file with a [custom bundle](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-add-plugins.html) that contains your OpenID Connect Provider’s JWKS file (`op_jwks.json`) inside of an `oidc` folder.

        This bundle allows all Elasticsearch containers to access the metadata file.

    2. Update your Elasticsearch cluster configuration using the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md) to use the bundle you prepared in the previous step. You need to modify the `user_bundles` JSON attribute similar to the following example snippet:

        ```sh
        {
          "cluster_name": "REPLACE_WITH_YOUR_CLUSTER_NAME",
          "plan": {

            ...

            "elasticsearch": {
              "version": "8.13.1",
              "user_bundles": [
                {
                  "name": "oidc-keys",
                  "url": "https://www.MYURL.com/oidc-keys.zip",
                  "elasticsearch_version": "8.*"
                }
              ]
            }
          }
        ```

        ::::{note}
        The URLs that point to the ZIP file containing the bundle must be accessible to the deployment. Custom bundles are unzipped under the path `/app/config/BUNDLE_DIRECTORY_STRUCTURE`, where `BUNDLE_DIRECTORY_STRUCTURE` is the directory structure in the ZIP file. Make sure to save the file location where custom bundles get unzipped, as you will need it in the next step.
        ::::


        In our example, the OpenID Connect Provider JWK set file will be located in the path `/app/config/oidc/op_jwks.json`:

        ```sh
        $ tree .
        .
        └── oidc
              └── op_jwks.json
        ```

    3. Adjust your `oidc` realm configuration accordingly:



## Configure SSL [ece-oidc-ssl-configuration]

OpenID Connect depends on TLS to provider security properties such as encryption in transit and endpoint authentication. The RP is required to establish back-channel communication with the OP in order to exchange the code for an ID Token during the Authorization code grant flow and in order to get additional user information from the UserInfo endpoint. As such, it is important that Elastic Cloud Enterprise can validate and trust the server certificate that the OP uses for TLS. Since the system truststore is used for the client context of outgoing https connections, if your OP is using a certificate from a trusted CA, no additional configuration is needed.

However, if your OP uses a certificate that is issued for instance, by a CA used only in your Organization, you must configure Elastic Cloud Enterprise to trust that CA.

1. Prepare a ZIP file with a [custom bundle](https://www.elastic.co/guide/en/cloud-enterprise/current/ece-add-plugins.html) that contains the CA certificate (`company-ca.pem`) that signed the certificate your OpenID Connect Provider uses for TLS inside of an `oidc-tls` folder
2. Update your Elasticsearch cluster configuration using the [advanced configuration editor](../../../deploy-manage/deploy/cloud-enterprise/advanced-cluster-configuration.md) to use the bundle you prepared in the previous step. You need to modify the `user_bundles` JSON attribute similar to the following example snippet:

    ```sh
    {
      "cluster_name": "REPLACE_WITH_YOUR_CLUSTER_NAME",
      "plan": {

        ...

        "elasticsearch": {
          "version": "8.13.1",
          "user_bundles": [
            {
              "name": "oidc-tls-ca",
              "url": "https://www.MYURL.com/oidc-tls-ca.zip",
              "elasticsearch_version": "8.*"
            }
          ]
        }
      }
    ```

    ::::{note}
    The URLs that point to the ZIP file containing the bundle must be accessible to the deployment. Custom bundles are unzipped under the path `/app/config/BUNDLE_DIRECTORY_STRUCTURE`, where `BUNDLE_DIRECTORY_STRUCTURE` is the directory structure in the ZIP file. Make sure to save the file location where custom bundles get unzipped, as you will need it in the next step.
    ::::


    In our example, the CA certificate file will be located in the path `/app/config/oidc-tls/company-ca.pem`:

    ```sh
    $ tree .
    .
    └── oidc-tls
          └── company-ca.pem
    ```

3. Adjust your `oidc` realm configuration accordingly:





## Optional Settings [ece-oidc-optional-settings]

The following optional oidc realm settings are supported and can be set if needed:

* `op.endsession_endpoint` The URL to the End Session Endpoint in the OpenID Connect Provider. This is the endpoint where the user’s browser will be redirected after local logout, if the realm is configured for RP initiated Single Logout and the OP supports it. The value for this setting should be provided by your OpenID Connect Provider.
* `rp.post_logout_redirect_uri` The Redirect URL where the OpenID Connect Provider should redirect the user after a successful Single Logout. This should be set to a value that will not trigger a new OpenID Connect Authentication, `<KIBANA_ENDPOINT_URL>/security/logged_out` is a good choice for this parameter.
* `rp.signature_algorithm` The signature algorithm that will be used by {{es}} in order to verify the signature of the ID tokens it will receive from the OpenID Connect Provider. Defaults to `RSA256`.
* `rp.requested_scopes` The scope values that will be requested by the OpenID Connect Provider as part of the Authentication Request. Defaults to `openid`, which is the only required scope for authentication. If your use case requires that you receive additional claims, you might need to request additional scopes, one of `profile`, `email`, `address`, `phone`. Note that `openid` should always be included in the list of requested scopes.

