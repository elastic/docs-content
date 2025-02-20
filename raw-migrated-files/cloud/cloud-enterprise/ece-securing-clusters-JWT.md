# Secure your clusters with JWT [ece-securing-clusters-JWT]

These steps show how you can secure your Elasticsearch clusters instances in a deployment by using a JSON Web Token (JWT) realm for authentication.

::::{note}
The JWT credentials are valid against the deployment, not the ECE platform. You can configure [role-based access control](../../../deploy-manage/users-roles/cloud-enterprise-orchestrator/manage-users-roles.md) for the platform separately.
::::



### Before you begin [ece_before_you_begin_21]

Elastic Cloud Enterprise supports JWT of ID Token format with Elastic Stack version 8.2 and later. Support for JWT of certain access token format is available since 8.7.


### Configure your 8.2 or above cluster to use JWT of ID Token format [ece_configure_your_8_2_or_above_cluster_to_use_jwt_of_id_token_format]

```sh
xpack:
  security:
    authc:
      realms:
        jwt: <1>
          jwt-realm-name: <2>
            order: 2 <3>
            client_authentication.type: "shared_secret" <4>
            allowed_signature_algorithms: "HS256,HS384,HS512,RS256,RS384,RS512,ES256,ES384,ES512,PS256,PS384,PS512" <5>
            allowed_issuer: "issuer1" <6>
            allowed_audiences: "elasticsearch1,elasticsearch2" <7>
            claims.principal: "sub" <8>
            claims.groups: "groups" <9>
```

1. Specifies the authentication realm service.
2. Defines the JWT realm name.
3. The order of the JWT realm in your authentication chain. Allowed values are between `2` and `100`, inclusive.
4. Defines the client authenticate type.
5. Defines the JWT `alg` header values allowed by the realm.
6. Defines the JWT `iss` claim value allowed by the realm.
7. Defines the JWT `aud` claim values allowed by the realm.
8. Defines the JWT claim name used for the principal (username). No default.
9. Defines the JWT claim name used for the groups. No default.


By default, users authenticating through JWT have no roles assigned to them. If you want all users in the group `elasticadmins` in your identity provider to be assigned the `superuser` role in your Elasticsearch cluster, issue the following request to Elasticsearch:

```sh
POST /_security/role_mapping/CLOUD_JWT_ELASTICADMIN_TO_SUPERUSER <1>
{
   "enabled": true,
    "roles": [ "superuser" ], <2>
    "rules": { "all" : [ <3>
        { "field": { "realm.name": "jwt-realm-name" } }, <4>
        { "field": { "groups": "elasticadmins" } }
    ]},
    "metadata": { "version": 1 }
}
```

1. The mapping name.
2. The Elastic Stack role to map to.
3. A rule specifying the JWT role to map from.
4. `realm.name` can be any string containing only alphanumeric characters, underscores, and hyphens.


::::{note}
In order to use the field `groups` in the mapping rule, you need to have mapped the JWT Attribute that conveys the group membership to `claims.groups` in the previous step.
::::



### Configure your 8.7 or above cluster to use JWT of access token format [ece_configure_your_8_7_or_above_cluster_to_use_jwt_of_access_token_format]

```sh
xpack:
  security:
    authc:
      realms:
        jwt:
          jwt-realm-name:
            order: 2
            token_type: "access_token" <1>
            client_authentication.type: "shared_secret"
            allowed_signature_algorithms: [ "RS256", "HS256" ]
            allowed_subjects: [ "123456-compute@developer.example.com" ] <2>
            allowed_issuer: "issuer1"
            allowed_audiences: [ "elasticsearch1", "elasticsearch2" ]
            required_claims: <3>
              token_use: "access"
            fallback_claims.sub: "client_id" <4>
            fallback_claims.aud: "scope" <5>
            claims.principal: "sub" <6>
            claims.groups: "groups"
```

1. Specifies token type accepted by this JWT realm
2. Specifies subjects allowed by the realm. This setting is mandatory for `access_token` JWT realms.
3. Additional claims required for successful authentication. The claim name can be any valid variable names and the claim values must be either string or array of strings.
4. The name of the JWT claim to extract the subject information if the `sub` claim does not exist. This setting is only available for `access_token` JWT realms.
5. The name of the JWT claim to extract the audiences information if the `aud` claim does not exist. This setting is only available for `access_token` JWT realms.
6. Since the fallback claim for `sub` is defined as `client_id`, the principal will also be extracted from `client_id` if the `sub` claim does not exist


::::{note}
Refer to [JWT authentication documentation](/deploy-manage/users-roles/cluster-or-deployment-auth/jwt.md) for more details and examples.
::::



## Update the trust settings of a deployment [ece_update_the_trust_settings_of_a_deployment]

A deployment can be configured to trust all, specific, or no deployments in the same ECE environment, other remote ECE environments, {{ecloud}}, or self-managed environments.

This can be done in the Security page of your deployment:

1. [Log into the Cloud UI](../../../deploy-manage/deploy/cloud-enterprise/log-into-cloud-ui.md).
2. On the deployments page, select your deployment.

    Narrow the list by name, ID, or choose from several other filters. To further define the list, use a combination of filters.

3. From the **Security** menu, find the **Trust Management** section.

:::{image} ../../../images/cloud-enterprise-ce-deployment-trusted-environments.png
:alt: Trusted Environments at the Deployment Level
:class: screenshot
:::

The page shows a list of all the deployments that this deployment trusts, grouped by environment. Initially only the **Local Environment** appears, which represents the current ECE environment, but you can trust deployments in [other ECE environments](../../../deploy-manage/remote-clusters/ece-remote-cluster-other-ece.md#ece-trust-remote-environments), in [{{ecloud}}](../../../deploy-manage/remote-clusters/ece-remote-cluster-ece-ess.md#ece-trust-ec), or any [self-managed environment](../../../deploy-manage/remote-clusters/ece-remote-cluster-self-managed.md#ece-trust-self-managed).

```
page, under *Security* > *Trust Management*:
```
1. Select **Add trusted environment** to configure trust with deployments in another ECE environment whose trust relationship has been created in the previous step.
2. For each trusted ECE environment you can edit the trust level to trust all deployments or just specific ones. For the specific ones option, you can introduce a list of Elasticsearch cluster IDs to trust from that ECE environment. The Elasticsearch `Cluster ID` can be found in the deployment overview page under **Applications**.

:::{image} ../../../images/cloud-enterprise-ce-deployment-trusted-environments.png
:alt: Trusted Environments at the Deployment Level
:class: screenshot
:::

