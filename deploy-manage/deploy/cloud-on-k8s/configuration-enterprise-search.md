---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-enterprise-search-configuration.html
---

# Configuration [k8s-enterprise-search-configuration]

## Upgrade the Enterprise Search specification [k8s-enterprise-search-upgrade-specification]

You can upgrade the Enterprise Search version or change settings by editing the YAML specification. ECK will apply the changes by performing a rolling restart of Enterprise Search pods.


## Customize Enterprise Search configuration [k8s-enterprise-search-custom-configuration]

ECK sets up a default Enterprise Search [configuration](https://www.elastic.co/guide/en/enterprise-search/current/configuration.html#configuration). To customize it, use the `config` element in the specification.

At a minimum, you must set both `ent_search.external_url` and `kibana.host` to the desired URLs.

```yaml
apiVersion: enterprisesearch.k8s.elastic.co/v1
kind: EnterpriseSearch
metadata:
  name: enterprise-search-quickstart
spec:
  version: 8.16.1
  count: 1
  elasticsearchRef:
    name: quickstart
  config:
    # define the exposed URL at which users will reach Enterprise Search
    ent_search.external_url: https://my-custom-domain:3002
    # define the exposed URL at which users will reach Kibana
    kibana.host: https://kibana.my-custom-domain:5601
    # configure app search document size limit
    app_search.engine.document_size.limit: 100kb
```


## Reference Kubernetes Secrets for sensitive settings [k8s-enterprise-search-secret-configuration]

Sensitive settings are best stored in Kubernetes Secrets, referenced in the Enterprise Search specification.

This example sets up a Secret with SMTP credentials:

```yaml
apiVersion: enterprisesearch.k8s.elastic.co/v1
kind: EnterpriseSearch
metadata:
  name: enterprise-search-quickstart
spec:
  version: 8.16.1
  count: 1
  elasticsearchRef:
    name: quickstart
  config:
    ent_search.external_url: https://my-custom-domain:3002
    kibana.host: https://kibana.my-custom-domain:5601
  configRef:
    secretName: smtp-credentials
---
kind: Secret
apiVersion: v1
metadata:
  name: smtp-credentials
stringData:
  enterprise-search.yml: |-
    email.account.enabled: true
    email.account.smtp.auth: plain
    email.account.smtp.starttls.enable: false
    email.account.smtp.host: 127.0.0.1
    email.account.smtp.port: 25
    email.account.smtp.user: myuser
    email.account.smtp.password: mypassword
    email.account.email_defaults.from: my@email.com
```

ECK merges the content of `config` and `configRef` into a single internal Secret. In case of duplicate settings, the `configRef` secret has precedence.


## Customize the Pod template [k8s-enterprise-search-custom-pod-template]

You can override the Enterprise Search Pod’s specification through the `podTemplate` element.

This example overrides the default 4Gi deployment to use 8Gi instead, and makes the deployment highly-available with 3 Pods:

```yaml
apiVersion: enterprisesearch.k8s.elastic.co/v1
kind: EnterpriseSearch
metadata:
  name: enterprise-search-quickstart
spec:
  version: 8.16.1
  count: 3
  elasticsearchRef:
    name: quickstart
  podTemplate:
    spec:
      containers:
      - name: enterprise-search
        resources:
          requests:
            cpu: 3
            memory: 8Gi
          limits:
            memory: 8Gi
        env:
        - name: JAVA_OPTS
          value: -Xms7500m -Xmx7500m
```

### Customize the Pod template security context [k8s-enterprise-search-custom-pod-template-security-context]

The Enterprise Search Pod’s security context can be customized through the `podTemplate` element. However, if `readOnlyRootFilesystem` is set to `true` without additional configuration, the Pod will fail to start. This happens because Enterprise Search (a Ruby service) requires write access to certain directories within `/usr/share/enterprise-search`, which include WAR files and configurations.

To work around this, use an init container to copy the necessary WAR files to a temporary writable location, before starting the Enterprise Search container with mounted writable volumes. Having the temporary directories (`/tmp`) in-memory also ensures Ruby has a temporary directory to work with during startup.

This example demonstrates the workaround:

```yaml
apiVersion: enterprisesearch.k8s.elastic.co/v1
kind: EnterpriseSearch
metadata:
  name: testing
spec:
  version: 8.16.1
  image: docker.elastic.co/enterprise-search/enterprise-search:8.16.1
  count: 1
  elasticsearchRef:
    name: testing
  podTemplate:
    spec:
      containers:
        - name: enterprise-search
          image: docker.elastic.co/enterprise-search/enterprise-search:8.16.1
          securityContext: <1>
            readOnlyRootFilesystem: true
            runAsNonRoot: true
            allowPrivilegeEscalation: false
            runAsUser: 1000 <2>
          volumeMounts: <3>
          - name: search-tmp
            mountPath: /usr/share/enterprise-search/tmp
          - name: tmp
            mountPath: /tmp
          - name: filebeat-data
            mountPath: /usr/share/enterprise-search/filebeat/data
          - name: war-files
            mountPath: /usr/share/enterprise-search/lib/war
          resources:
            requests:
              cpu: 3
              memory: 8Gi
            limits:
              memory: 8Gi
          env: <4>
          - name: JAVA_OPTS
            value: -Xms7500m -Xmx7500m
      initContainers: <5>
      - name: init-war-dir
        image: docker.elastic.co/enterprise-search/enterprise-search:8.16.1
        command: ['sh', '-c', 'cp --verbose -r /usr/share/enterprise-search/lib/war/. /usr/share/enterprise-search-war-tmp']
        volumeMounts:
        - name: war-files
          mountPath: /usr/share/enterprise-search-war-tmp
      volumes: <6>
      - name: war-files
        emptyDir: {}
      - name: filebeat-data
        emptyDir: {}
      - name: search-tmp
        emptyDir:
          medium: Memory
      - name: tmp
        emptyDir:
          medium: Memory
```

1. Adds a security context to define permissions and access control settings for the `enterprise-search` container.
2. Sets the user to random UID `1000` to run the container as a non-root user.
3. Adds volume mounts for `search-tmp`, `tmp`, `filebeat-data`, and `war-files` to the `enterprise-search` container.
4. Adds the variable `JAVA_OPTS` to pass options and configurations to the Java Virtual Machine (JVM).
5. Adds an init container to copy WAR files to a temporary location.
6. Adds volumes for WAR files and adds volumes with in-memory storage for `search-tmp` and `tmp`.




## Expose Enterprise Search [k8s-enterprise-search-expose]

By default ECK manages self-signed TLS certificates to secure the connection to Enterprise Search. It also restricts the Kubernetes service to `ClusterIP` type that cannot be accessed publicly.

Check [how to access Elastic Stack services](accessing-services.md) to customize TLS settings and expose the service.

::::{note}
When exposed outside the scope of `localhost`, make sure to set both `ent_search.external_url`, and `kibana.host` accordingly in the Enterprise Search configuration.
::::



## Customize the connection to an Elasticsearch cluster [k8s-enterprise-search-connect-es]

The `elasticsearchRef` element allows ECK to automatically configure Enterprise Search to establish a secured connection to a managed Elasticsearch cluster. By default it targets all nodes in your cluster. If you want to direct traffic to specific nodes of your Elasticsearch cluster, refer to [*Traffic Splitting*](requests-routing-to-elasticsearch-nodes.md) for more information and examples.


## Connect to an external Elasticsearch cluster [k8s-enterprise-search-connect-non-eck-es]

### Automatically [k8s_automatically]

Refer to [*Connect to external Elastic resources*](connect-to-external-elastic-resources.md) to automatically configure Enterprise Search using connection settings from a `Secret`.


### Manually [k8s_manually]

If you do not want to use the `elasticsearchRef` mechanism you can manually configure Enterprise Search to access any available Elasticsearch cluster:

```yaml
apiVersion: enterprisesearch.k8s.elastic.co/v1
kind: EnterpriseSearch
metadata:
  name: enterprise-search-quickstart
spec:
  version: 8.16.1
  count: 1
  configRef:
    secretName: elasticsearch-credentials
---
kind: Secret
apiVersion: v1
metadata:
  name: elasticsearch-credentials
stringData:
  enterprise-search.yml: |-
    elasticsearch.host: [https://elasticsearch-url:9200](https://elasticsearch-url:9200)
    elasticsearch.username: elastic
    elasticsearch.password: my-password
    elasticsearch.ssl.enabled: true
```



