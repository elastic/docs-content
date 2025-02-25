# Secure your clusters with SAML [ech-securing-clusters-SAML]

These steps show how you can secure your Elasticsearch clusters and Kibana instances in a deployment by using a Security Assertion Markup Language (SAML) identity provider (IdP) for cross-domain, single sign-on authentication.


## Configure your 8.0 or above cluster to use SAML [echconfigure_your_8_0_or_above_cluster_to_use_saml]

You must edit your cluster configuration, sometimes also referred to as the deployment plan, to point to the SAML IdP before you can complete the configuration in Kibana. If you are using machine learning or a deployment with hot-warm architecture, you must include this SAML IdP configuration in the user settings section for each node type.

1. Create or use an existing deployment that includes a Kibana instance.
2. Copy the Kibana endpoint URL.
3. $$$step-3$$$[Update your Elasticsearch user settings](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) for the `saml` realm and specify your IdP provider configuration:

    ```sh
    xpack:
      security:
        authc:
          realms:
            saml: <1>
              saml-realm-name: <2>
                order: 2 <3>
                attributes.principal: "nameid:persistent" <4>
                attributes.groups: "groups" <5>
                idp.metadata.path: "<check with your identity provider>" <6>
                idp.entity_id: "<check with your identity provider>" <7>
                sp.entity_id: "KIBANA_ENDPOINT_URL/" <8>
                sp.acs: "KIBANA_ENDPOINT_URL/api/security/saml/callback"
                sp.logout: "KIBANA_ENDPOINT_URL/logout"
    ```

    1. Specifies the authentication realm service.
    2. Defines the SAML realm name. The SAML realm name can only contain alphanumeric characters, underscores, and hyphens.
    3. The order of the SAML realm in your authentication chain. Allowed values are between `2` and `100`. Set to `2` unless you plan on configuring multiple SSO realms for this cluster.
    4. Defines the SAML attribute that is going to be mapped to the principal (username) of the authenticated user in Kibana. In this  non-normative example, `nameid:persistent` maps the `NameID` with the `urn:oasis:names:tc:SAML:2.0:nameid-format:persistent` format from the Subject of the SAML Assertion. You can use any SAML attribute that carries the necessary value for your use case in this setting, such as `uid` or `mail`. Refer to [the attribute mapping documentation](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-attributes-mapping) for details and available options.
    5. Defines the SAML attribute used for role mapping when configured in Kibana. Common choices are `groups` or `roles`. The values for both `attributes.principal` and `attributes.groups` depend on the IdP provider, so be sure to review their documentation. Refer to [the attribute mapping documentation](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-attributes-mapping) for details and available options.
    6. The file path or the HTTPS URL where your IdP metadata is available, such as `https://idpurl.com/sso/saml/metadata`. If you configure a URL you need to make ensure that your Elasticsearch cluster can access it.
    7. The SAML EntityID of your IdP. This can be read from the configuration page of the IdP, or its SAML metadata, such as `https://idpurl.com/entity_id`.
    8. Replace `KIBANA_ENDPOINT_URL` with the one noted in the previous step, such as `sp.entity_id: https://eddac6b924f5450c91e6ecc6d247b514.us-east-1.aws.found.io:443/` including the slash at the end.

4. By default, users authenticating through SAML have no roles assigned to them. For example, if you want all your users authenticating with SAML to get access to Kibana, issue the following request to Elasticsearch:

    ```sh
    POST /_security/role_mapping/CLOUD_SAML_TO_KIBANA_ADMIN <1>
    {
       "enabled": true,
        "roles": [ "kibana_admin" ], <2>
        "rules": { <3>
            "field": { "realm.name": "saml-realm-name" } <4>
        },
        "metadata": { "version": 1 }
    }
    ```

    1. The mapping name.
    2. The Elastic Stack role to map to.
    3. A rule specifying the SAML role to map from.
    4. `realm.name` can be any string containing only alphanumeric characters, underscores, and hyphens.

5. Alternatively, if you want the users that belong to the group `elasticadmins` in your identity provider to be assigned the `superuser` role in your Elasticsearch cluster, issue the following request to Elasticsearch:

    ```sh
    POST /_security/role_mapping/CLOUD_SAML_ELASTICADMIN_TO_SUPERUSER <1>
    {
       "enabled": true,
        "roles": [ "superuser" ], <2>
        "rules": { "all" : [ <3>
            { "field": { "realm.name": "saml-realm-name" } }, <4>
            { "field": { "groups": "elasticadmins" } }
        ]},
        "metadata": { "version": 1 }
    }
    ```

    1. The mapping name.
    2. The Elastic Stack role to map to.
    3. A rule specifying the SAML role to map from.
    4. `realm.name` can be any string containing only alphanumeric characters, underscores, and hyphens.


    ::::{note}
    In order to use the field `groups` in the mapping rule, you need to have mapped the SAML Attribute that conveys the group membership to `attributes.groups` in the previous step.
    ::::

6. Update Kibana in the [user settings configuration](../../../deploy-manage/deploy/elastic-cloud/edit-stack-settings.md) to use SAML as the authentication provider:

    ```sh
    xpack.security.authc.providers:
      saml.saml1:
        order: 0
        realm: saml-realm-name <1>
    ```

    1. The name of the SAML realm that you have configured earlier, for instance `saml-realm-name`. The SAML realm name can only contain alphanumeric characters, underscores, and hyphens.


    This configuration disables all other realms and only allows users to authenticate with SAML. If you wish to allow your native realm users to authenticate, you need to also enable the `basic` `provider` like this:

    ```sh
    xpack.security.authc.providers:
      saml.saml1:
        order: 0
        realm: saml-realm-name
        description: "Log in with my SAML" <1>
      basic.basic1:
        order: 1
    ```

    1. This arbitrary string defines how SAML login is titled in the Login Selector UI that is shown when you enable multiple authentication providers in Kibana. You can also configure the optional `icon` and `hint` settings for any authentication provider.



+ . Optional: Generate SAML metadata for the Service Provider.

+ The SAML 2.0 specification provides a mechanism for Service Providers to describe their capabilities and configuration using a metadata file. If your SAML Identity Provider requires or allows you to configure it to trust the Elastic Stack Service Provider through the use of a metadata file, you can generate the SAML metadata by issuing the following request to Elasticsearch:

+

```console
GET /_security/saml/metadata/realm_name <1>
```

+ <1> The name of the SAML realm in Elasticsearch.

+ You can generate the SAML metadata by issuing the API request to Elasticsearch and storing metadata as an XML file using tools like `jq`.

+ The following command, for example, generates the metadata for the SAML realm `saml1` and saves it to `metadata.xml` file:

+

```console
curl -X GET -H "Content-Type: application/json" -u user_name:password https://<elasticsearch_endpoint>:443/_security/saml/metadata/saml1 <1>
|jq -r '.[]' > metadata.xml
```

+ <1> The elasticsearch endpoint for the given deployment where the `saml1` realm is configured.

+

1. Optional: If your Identity Provider doesn’t publish its SAML metadata at an HTTP URL, or if your Elasticsearch cluster cannot reach that URL, you can upload the SAML metadata as a file.

    1. Prepare a ZIP file with a [custom bundle](../../../deploy-manage/deploy/elastic-cloud/upload-custom-plugins-bundles.md) that contains your Identity Provider’s metadata (`metadata.xml`) inside of a `saml` folder.

        This bundle allows all Elasticsearch containers to access the metadata file.

    2. Update your Elasticsearch cluster on the [deployments page](../../../deploy-manage/deploy/elastic-cloud/add-plugins-extensions.md) to use the bundle you prepared in the previous step.


        Custom bundles are unzipped under the path `/app/config/BUNDLE_DIRECTORY_STRUCTURE`, where `BUNDLE_DIRECTORY_STRUCTURE` is the directory structure in the ZIP file. Make sure to save the file location where custom bundles get unzipped, as you will need it in the next step.

        In our example, the SAML metadata file will be located in the path `/app/config/saml/metadata.xml`:

        ```sh
        $ tree .
        .
        └── saml
              └── metadata.xml
        ```

    3. Adjust your `saml` realm configuration accordingly:

        ```sh
            idp.metadata.path: /app/config/saml/metadata.xml <1>
        ```

        1. The path to the SAML metadata file that was uploaded.

2. Use the Kibana endpoint URL to log in.


## Configure your 7.x cluster to use SAML [ech-7x-saml]

For 7.x deployments, the instructions are similar to those for 8.x, but your Elasticsearch request should use `POST /_security/role_mapping/CLOUD_SAML_TO_KIBANA_ADMIN` (for Step 4) or `POST /_security/role_mapping/CLOUD_SAML_ELASTICADMIN_TO_SUPERUSER` (for Step 5).

All of the other steps are the same.


