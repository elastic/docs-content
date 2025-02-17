---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-auth-config-using-stack-config-policy.html
---

# Manage authentication for multiple clusters [k8s-auth-config-using-stack-config-policy]

::::{warning}
We have identified an issue with Elasticsearch 8.15.1 and 8.15.2 that prevents security role mappings configured via Stack configuration policies to work correctly. Avoid these versions and upgrade to 8.16.0 to remedy this issue if you are affected.
::::


::::{note}
This requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../../license/manage-your-license-in-eck.md) for more details about managing licenses.
::::


ECK `2.11.0` extends the functionality of [Elastic Stack configuration policies](../../deploy/cloud-on-k8s/elastic-stack-configuration-policies.md) so that it becomes possible to configure Elasticsearch security realms for more than one Elastic stack at once. The authentication will apply to all Elasticsearch clusters and Kibana instances managed by the Elastic Stack configuration policy.

Examples for configuring some of the authentication methods can be found below:

* [LDAP authentication using Elastic Stack configuration policy](#k8s-ldap-using-stack-config-policy)
* [OpenID Connect authentication using Elastic Stack configuration policy](#k8s-oidc-stack-config-policy)
* [JWT authentication using Elastic Stack configuration policy](#k8s-jwt-stack-config-policy)

## LDAP using Elastic stack configuration policy [k8s-ldap-using-stack-config-policy]

::::{warning}
We have identified an issue with Elasticsearch 8.15.1 and 8.15.2 that prevents security role mappings configured via Stack configuration policies to work correctly. Avoid these versions and upgrade to 8.16.0 to remedy this issue if you are affected.
::::


::::{note}
This requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../../license/manage-your-license-in-eck.md) for more details about managing licenses.
::::


::::{tip}
Make sure you check the complete [guide to setting up LDAP with Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/ldap-realm.html).
::::


### To configure LDAP using Elastic Stack configuration policy with user search: [k8s_to_configure_ldap_using_elastic_stack_configuration_policy_with_user_search]

1. Add a realm configuration to the `config` field under `elasticsearch` in the `xpack.security.authc.realms.ldap` namespace. At a minimum, you must specify the URL of the LDAP server and the order of the LDAP realm compared to other configured security realms. You also have to set `user_search.base_dn` to the container DN where the users are searched for. Refer to [LDAP realm settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ref-ldap-settings) for all of the options you can set for an LDAP realm. For example, the following snippet shows an LDAP realm configured with a user search:

    ```yaml
    elasticsearch:
      config:
        xpack.security.authc.realms:
          ldap:
            ldap1:
              order: 0
              url: "ldap://openldap.default.svc.cluster.local:1389"
              bind_dn: "cn=admin,dc=example,dc=org"
              user_search:
                base_dn: "dc=example,dc=org"
                filter: "(cn={0})"
              group_search:
                base_dn: "dc=example,dc=org"
              unmapped_groups_as_roles: false
    ```

2. The password for the `bind_dn` user should be configured by adding the appropriate `secure_bind_password` setting to the Elasticsearch keystore. This can be done using the Elastic Stack configuration policy by following the below steps:

    1. Create a secret that has the `secure_bind_password` in the same namespace as the operator

        ```sh
          kubectl create secret generic ldap-secret --from-literal=xpack.security.authc.realms.ldap.ldap1.secure_bind_password=<password>
        ```

    2. Add the secret name to the `secureSettings` field under `elasticsearch` in the Elastic Stack configuration policy

        ```yaml
          spec:
            resourceSelector:
              matchLabels:
                env: my-label
            elasticsearch:
              secureSettings:
              - secretName: ldap-secret
        ```

3. Map LDAP groups to roles. In the below example, LDAP users get the Elasticsearch `superuser` role. `dn: "cn=users,dc=example,dc=org"` is the LDAP distinguished name (DN) of the users group.

    ```yaml
    securityRoleMappings:
      ldap_role:
        roles: [ "superuser" ]
        rules:
          all:
            - field: { realm.name: "ldap1" }
            - field: { dn: "cn=users,dc=example,dc=org" }
        enabled: true
    ```


Simple full example Elastic Stack config policy to configure LDAP realm with user search

```yaml
apiVersion: stackconfigpolicy.k8s.elastic.co/v1alpha1
kind: StackConfigPolicy
metadata:
  name: test-stack-config-policy
spec:
  resourceSelector:
    matchLabels:
      env: my-label
  elasticsearch:
    secureSettings:
    - secretName: ldap-secret
    securityRoleMappings:
      ldap_role:
        roles: [ "superuser" ]
        rules:
          all:
            - field: { realm.name: "ldap1" }
            - field: { dn: "cn=users,dc=example,dc=org" }
        enabled: true
    config:
      xpack.security.authc.realms:
        ldap:
          ldap1:
            order: 0
            url: "ldap://openldap.default.svc.cluster.local:1389"
            bind_dn: "cn=admin,dc=example,dc=org"
            user_search:
              base_dn: "dc=example,dc=org"
              filter: "(cn={0})"
            group_search:
              base_dn: "dc=example,dc=org"
            unmapped_groups_as_roles: false
```


### To configure an LDAP realm with user DN templates: [k8s_to_configure_an_ldap_realm_with_user_dn_templates]

Add a realm configuration to `elasticsearch.yml` in the xpack.security.authc.realms.ldap namespace. At a minimum, you must specify the url and order of the LDAP server, and specify at least one template with the user_dn_templates option. Check [LDAP realm settings](https://www.elastic.co/guide/en/elasticsearch/reference/current/security-settings.html#ref-ldap-settings)  for all of the options you can set for an ldap realm.

For example, the following snippet shows an LDAP realm configured with user DN templates:

```yaml
xpack:
  security:
    authc:
      realms:
        ldap:
          ldap1:
            order: 0
            url: "ldaps://ldap.example.com:636"
            user_dn_templates:
              - "cn={0}, ou=users, dc=example, dc=org"
            group_search:
              base_dn: "dc=example,dc=org"
            unmapped_groups_as_roles: false
```

Example Elastic Stack config policy to configure LDAP realm with user DN templates:

```yaml
apiVersion: stackconfigpolicy.k8s.elastic.co/v1alpha1
kind: StackConfigPolicy
metadata:
  name: test-stack-config-policy
spec:
  resourceSelector:
    matchLabels:
      env: my-label
  elasticsearch:
    securityRoleMappings:
      ldap_role:
        roles: [ "superuser" ]
        rules:
          all:
            - field: { realm.name: "ldap1" }
            - field: { dn: "*,ou=users,dc=example,dc=org" }
        enabled: true
    config:
      xpack.security.authc.realms:
        ldap:
          ldap1:
            order: 0
            url: "ldaps://ldap.example.com:636"
            user_dn_templates:
              - "cn={0}, ou=users, dc=example, dc=org"
            group_search:
              base_dn: "dc=example,dc=org"
            unmapped_groups_as_roles: false
```

The `bind_dn` setting is not used in template mode. All LDAP operations run as the authenticating user. So there is no need of setting up any additional secrets to be stored in the keystore.



## OIDC using Elastic stack configuration policy [k8s-oidc-stack-config-policy]

::::{warning}
We have identified an issue with Elasticsearch 8.15.1 and 8.15.2 that prevents security role mappings configured via Stack configuration policies to work correctly. Avoid these versions and upgrade to 8.16.0 to remedy this issue if you are affected.
::::


::::{note}
This requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../../license/manage-your-license-in-eck.md) for more details about managing licenses.
::::


::::{tip}
Make sure you check the complete [guide to setting up OpenID Connect with Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/oidc-guide.html).
::::


Configuring OpenID Connect using Elastic Stack configuration policy

1. Add OIDC realm to the `elasticsearch.yml` file using the `config` field under `elasticsearch` in the Elastic Stack configuration policy, also enable token service.

    ::::{note}
    Below snippet is an example of using Google as OpenID provider, the values will change depending on the provider being used.
    ::::


    ```yaml
    elasticsearch:
        config:
           xpack:
             security:
               authc:
                 token.enabled: true
                 realms:
                   oidc:
                     oidc1:
                       order: 2
                       rp.client_id: "<client id>"
                       rp.response_type: "code"
                       rp.requested_scopes: ["openid", "email"]
                       rp.redirect_uri: "${KIBANA_URL}/api/security/oidc/callback"
                       op.issuer: "https://accounts.google.com"
                       op.authorization_endpoint: "https://accounts.google.com/o/oauth2/v2/auth"
                       op.token_endpoint: "https://oauth2.googleapis.com/token"
                       op.userinfo_endpoint: "https://openidconnect.googleapis.com/v1/userinfo"
                       op.jwkset_path: "https://www.googleapis.com/oauth2/v3/certs"
                       claims.principal: email
                       claim_patterns.principal: "^([^@]+)@elastic\\.co$"
    ```

2. Another piece of configuration of the OpenID Connect realm is to set the Client Secret that was assigned to the Relying Parties (RP) during registration in the OpenID Connect Provider (OP). This is a secure setting and as such is not defined in the realm configuration in `elasticsearch.yml` but added to the Elasticsearch keystore. To set this up using Elastic Stack configuration policy, use the following steps.

    1. Create a secret in the operator namespace that has the Client Secret

        ```sh
        kubectl create secret generic oidc-client-secret --from-literal=xpack.security.authc.realms.oidc.oidc1.rp.client_secret=<client_secret>
        ```

    2. Add the secret name to the `secureSettings` field under `elasticsearch`

        ```yaml
        elasticsearch:
            secureSettings:
            - secretName: oidc-client-secret
        ```

3. When a user authenticates using OpenID Connect, they are identified to the Elastic Stack, but this does not automatically grant them access to perform any actions or access any data. Your OpenID Connect users cannot do anything until they are assigned roles. Roles can be assigned by adding role mappings to the Elastic Stack configuration policy. The below example is giving a specific user access as a superuser to Elasticsearch, if you want to assign roles to all users authenticating with OIDC, you can remove the username field.

    ```yaml
    elasticsearch:
        secureSettings:
        - secretName: oidc-client-secret
        securityRoleMappings:
          oidc_kibana:
            roles: [ "superuser" ]
            rules:
              all:
                - field: { realm.name: "oidc1" }
                - field: { username: "<username>" }
            enabled: true
    ```

4. Update Kibana to use OpenID Connect as the authentication provider:

    ```yaml
    kibana:
        config:
          xpack.security.authc.providers:
            oidc.oidc1:
              order: 0
              realm: oidc1
              description: "Log in with GCP"
    ```


Example full Elastic Stack configuration policy to configure oidc

```yaml
apiVersion: stackconfigpolicy.k8s.elastic.co/v1alpha1
kind: StackConfigPolicy
metadata:
  name: test-stack-config-policy
spec:
  resourceSelector:
    matchLabels:
      env: my-label
  elasticsearch:
    secureSettings:
    - secretName: oidc-client-secret
    securityRoleMappings:
      oidc_kibana:
        roles: [ "superuser" ]
        rules:
          all:
            - field: { realm.name: "oidc1" }
            - field: { username: "<username>" }
        enabled: true
    config:
       logger.org.elasticsearch.discovery: DEBUG
       xpack:
         security:
           authc:
             token.enabled: true
             realms:
               oidc:
                 oidc1:
                   order: 2
                   rp.client_id: "<client id>"
                   rp.response_type: "code"
                   rp.requested_scopes: ["openid", "email"]
                   rp.redirect_uri: "${KIBANA_URL}/api/security/oidc/callback" <1>
                   op.issuer: "https://accounts.google.com"
                   op.authorization_endpoint: "https://accounts.google.com/o/oauth2/v2/auth"
                   op.token_endpoint: "https://oauth2.googleapis.com/token"
                   op.userinfo_endpoint: "https://openidconnect.googleapis.com/v1/userinfo"
                   op.jwkset_path: "https://www.googleapis.com/oauth2/v3/certs"
                   claims.principal: email
                   claim_patterns.principal: "^([^@]+)@elastic\\.co$"
  kibana:
    config:
      xpack.security.authc.providers:
        oidc.oidc1:
          order: 0
          realm: oidc1
          description: "Log in with GCP"
        basic.basic1:
          order: 1
```

1. The Kibana URL should be an environment variable that should be configured on the Elasticsearch Clusters managed by the Elastic Stack Configuration policy. This can be done by adding an environment variable to the pod template in the Elasticsearch CR.```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: quickstart
  namespace: kvalliy
  labels:
    env: my-label
spec:
  version: 8.10.3
  nodeSets:
  - name: default
    count: 1
    config:
      node.store.allow_mmap: false
    podTemplate:
      spec:
        containers:
        - name: elasticsearch
          env:
            - name: KIBANA_URL
              value: "https://kibana.eck-ocp.elastic.dev"
```



::::{note}
The OpenID Connect Provider (OP) should have support to configure multiple Redirect URLs, so that the same `rp.client_id` and `client_secret` can be used for all the Elasticsearch clusters managed by the Elastic Stack configuration policy.
::::



## JWT using Elastic Stack configuration policy [k8s-jwt-stack-config-policy]

::::{warning}
We have identified an issue with Elasticsearch 8.15.1 and 8.15.2 that prevents security role mappings configured via Stack configuration policies to work correctly. Avoid these versions and upgrade to 8.16.0 to remedy this issue if you are affected.
::::


::::{note}
This requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../../license/manage-your-license-in-eck.md) for more details about managing licenses.
::::


::::{tip}
Make sure you check the complete [guide to setting up JWT with Elasticsearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/jwt-auth-realm.html).
::::


Configuring JWT with Elastic Stack configuration policy

1. Add your JWT realm to the `elasticsearch.yml` file using the `config` field under `elasticsearch` in the Elastic Stack configuration policy

    ```yaml
    elasticsearch:
        config:
           xpack.security.authc.realms.jwt.jwt1:
             order: -98
             token_type: id_token
             client_authentication.type: shared_secret
             allowed_issuer: "https://es.k8s.elastic.co"
             allowed_audiences: [ "elasticsearch" ]
             allowed_subjects: ["elastic-user"]
             allowed_signature_algorithms: [RS512]
             pkc_jwkset_path: jwks/jwkset.json
             claims.principal: sub
    ```

2. Add the `shared_secret` setting that will be used for client authentication to the Elasticsearch keystore.

    1. Create a secret in the operator namespace containing the shared secret

        ```sh
        kubectl create secret generic shared-secret --from-literal=xpack.security.authc.realms.jwt.jwt1.client_authentication.shared_secret=<sharedsecret>
        ```

    2. Add the secret name to the `secureSettings` field under `elasticsearch` in the Elastic Stack configuration policy

        ```yaml
          elasticsearch:
            secureSettings:
        :   - secretName: shared-secret
        ```

3. Add an additional volume to the Elasticsearch pods that contain the JSON Web Keys, it should be mounted to the path that is configured for the `xpack.security.authc.realms.jwt.jwt1.pkc_jwkset_path` config. The file path is resolved relative to the Elasticsearch configuration directory.

    1. Create a secret in the operator namespace that has the jwk set

        ```sh
        kubectl create secret generic jwks-secret --from-file=jwkset.json
        ```

    2. Add the secret name and mountpath to the `secretMounts` field under `elasticsearch` in the Elastic Stack configuration policy

        ```yaml
        secretMounts:
            - secretName: jwks-secret
              mountPath: "/usr/share/elasticsearch/config/jwks"
        ```

4. You can use the `securityRoleMappings` field under `elasticsearch` in the Elastic Stack configuration policy to define role mappings that determine which roles should be assigned to each user based on their username, groups, or other metadata.

    ```yaml
    securityRoleMappings:
      jwt1-user-role:
        roles: [ "superuser" ]
        rules:
          all:
            - field: { realm.name: "jwt1" }
            - field: { username: "jwt-user" }
        enabled: true
    ```


The following example demonstrates how an Elastic Stack configuration policy can be used to configure a JWT realm:

```yaml
apiVersion: stackconfigpolicy.k8s.elastic.co/v1alpha1
kind: StackConfigPolicy
metadata:
  name: test-stack-config-policy
spec:
  resourceSelector:
    matchLabels:
      env: my-label
  elasticsearch:
    secureSettings:
    - secretName: shared-secret
    securityRoleMappings:
      jwt1-user-role:
        roles: [ "superuser" ]
        rules:
          all:
            - field: { realm.name: "jwt1" }
            - field: { username: "jwt-user" }
        enabled: true
    config:
       xpack.security.authc.realms.jwt.jwt1:
         order: -98
         token_type: id_token
         client_authentication.type: shared_secret
         allowed_issuer: "https://es.k8s.elastic.co"
         allowed_audiences: [ "elasticsearch" ]
         allowed_subjects: ["elastic-user"]
         allowed_signature_algorithms: [RS512]
         pkc_jwkset_path: jwks/jwkset.json
         claims.principal: sub
    secretMounts:
    - secretName: jwks-secret
      mountPath: "/usr/share/elasticsearch/config/jwks"
```


$$$k8s-jwt-stack-config-policy$$$