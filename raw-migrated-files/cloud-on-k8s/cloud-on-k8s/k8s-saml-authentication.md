# SAML Authentication [k8s-saml-authentication]

The Elastic Stack supports SAML single sign-on (SSO) into Kibana, using Elasticsearch as a backend service.

::::{note}
Elastic Stack SSO requires a valid Enterprise license or Enterprise trial license. Check [the license documentation](../../../deploy-manage/license/manage-your-license-in-eck.md) for more details about managing licenses.
::::


::::{tip}
Make sure you check the complete [Configuring SAML single sign-on on the Elastic Stack](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md) guide before setting up SAML SSO for Kibana and Elasticsearch deployments managed by ECK.
::::


## Add a SAML realm to X-Pack security settings [k8s_add_a_saml_realm_to_x_pack_security_settings]

To enable SAML SSO for the Elastic Stack, you have to configure the SAML realm in Elasticsearch and enable the usage of the SAML realm and authentication provider in Kibana.

### Elasticsearch [k8s_elasticsearch]

To add the SAML realm to Elasticsearch, use the `spec` section of the manifest. The SAML realm configuration contains an `idp.metadata.path` field that should be set to the path where your IdP’s SAML metadata file is located in the Elasticsearch pods.

::::{note}
The `sp.*` SAML settings must point to Kibana endpoints that are accessible from the web browser used to open Kibana.
::::


Check Elastic [Stack SAML documentation](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-guide-idp) for more information on `idp.*` and `sp.*` settings.

Make sure not to disable Elasticsearch’s file realm set by ECK, as ECK relies on the file realm for its operation. Set the `order` setting of the SAML realm to a greater value than the `order` value set for the file and native realms, which is by default -100 and -99 respectively. We recommend setting the priority of SAML realms to be lower than other realms, as shown in the next example.

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
  nodeSets:
  - name: default
    count: 1
    config:
      xpack.security.authc.realms:
        saml:
          saml1:
            attributes.principal: nameid
            idp.entity_id: https://sso.example.com/
            idp.metadata.path: /usr/share/elasticsearch/config/saml/idp-saml-metadata.xml
            order: 2
            sp.acs: https://kibana.example.com/api/security/saml/callback
            sp.entity_id: https://kibana.example.com/
            sp.logout: https://kibana.example.com/logout
```

The `idp.metadata.path` setting should point to your Identity Provider’s metadata file. The metadata file path can either be a path within the Elasticsearch container (full path or relative to Elasticsearch’s config directory), or an HTTPS URL.

If a path is provided, you need to make the metadata file available in the Elasticsearch container by creating a Kubernetes secret, containing the metadata file, and mounting it to the Elasticsearch container.

After saving your Identity Provider’s metadata file, create the secret. For example:

```sh
kubectl create secret generic idp-saml-metadata --from-file=idp-saml-metadata.xml
```

Next, create a volume from the secret and mount it for the Elasticsearch containers. For example:

```yaml
apiVersion: elasticsearch.k8s.elastic.co/v1
kind: Elasticsearch
metadata:
  name: elasticsearch-sample
spec:
  version: 8.16.1
  nodeSets:
  - name: default
    count: 1
    config:
      ...
    podTemplate:
      spec:
        containers:
          - name: elasticsearch
            volumeMounts:
              - name: idp-saml-metadata
                mountPath: /usr/share/elasticsearch/config/saml
        volumes:
          - name: idp-saml-metadata
            secret:
              secretName: idp-saml-metadata
```

::::{note}
To configure Elasticsearch for signing messages and/or for encrypted messages, keys and certificates should be mounted from a Kubernetes secret similar to how the SAML metadata file is mounted in the previous example. Passphrases, if needed, should be added to Elasticsearch’s keystore using ECK’s Secure Settings feature. For more information, check [the Secure Settings documentation](../../../deploy-manage/security/secure-settings.md) and [the Encryption and signing section](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-enc-sign) in the Stack SAML guide.
::::



### Kibana [k8s_kibana]

To enable SAML authentication in Kibana, you have to add SAML as an authentication provider and specify the SAML realm that you used in your Elasticsearch configuration.

::::{tip}
You can configure multiple authentication providers in Kibana and let users choose the provider they want to use. For more information, check [the Kibana authentication documentation](/deploy-manage/users-roles/cluster-or-deployment-auth/user-authentication.md).
::::


For example:

```yaml
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  version: 8.16.1
  count: 1
  elasticsearchRef:
    name: elasticsearch-sample
  config:
    xpack.security.authc.providers:
      saml.saml1:
        order: 0
        realm: "saml1"
```

::::{important}
Your SAML users cannot login to Kibana until they are assigned roles. For more information, refer to [the Configuring role mapping section](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-role-mapping) in the Stack SAML guide.
::::




## Generating Service Provider metadata [k8s_generating_service_provider_metadata]

The Elastic Stack supports generating service provider metadata, that can be imported to the identity provider, and configure many of the integration options between the identity provider and the service provider, automatically. For more information, check [the Generating SP metadata section](/deploy-manage/users-roles/cluster-or-deployment-auth/saml.md#saml-sp-metadata) in the Stack SAML guide.

To generate the Service Provider metadata using [the elasticsearch-saml-metadata command](asciidocalypse://docs/elasticsearch/docs/reference/elasticsearch/command-line-tools/saml-metadata.md), you will have to run the command using `kubectl`, and then copy the generated metadata file to your local machine. For example:

```sh
# Create metadata
kubectl exec -it elasticsearch-sample-es-default-0 -- sh -c "/usr/share/elasticsearch/bin/elasticsearch-saml-metadata --realm saml1"

# Copy metadata file
kubectl cp elasticsearch-sample-es-default-0:/usr/share/elasticsearch/saml-elasticsearch-metadata.xml saml-elasticsearch-metadata.xml
```


