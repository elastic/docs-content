---
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-kibana-es.html
applies_to:
  deployment:
    eck: all
products:
  - id: cloud-kubernetes
---

# Connect to an {{es}} cluster [k8s-kibana-es]

You can connect an {{es}} cluster that is either managed by ECK or not managed by ECK.

## {{es}} is managed by ECK [k8s-kibana-eck-managed-es]

It is quite straightforward to connect a {{kib}} instance to an {{es}} cluster managed by ECK:

```yaml subs=true
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: quickstart
spec:
  version: {{version.stack}}
  count: 1
  elasticsearchRef:
    name: quickstart
    namespace: default
```

The use of `namespace` is optional if the {{es}} cluster is running in the same namespace as {{kib}}. An additional `serviceName` attribute can be specified to target a custom Kubernetes service. Refer to [*Traffic Splitting*](requests-routing-to-elasticsearch-nodes.md) for more information. The {{kib}} configuration file is automatically setup by ECK to establish a secure connection to {{es}}.

::::{note} 
Any {{kib}} can reference (and thus access) any {{es}} instance as long as they are both in namespaces that are watched by the same ECK instance. ECK will copy the required Secret from {{es}} to {{kib}} namespace. {{kib}} cannot automatically connect to {{es}} (through `elasticsearchRef`) in a namespace managed by a different ECK instance. For more information, check [Restrict cross-namespace resource associations](restrict-cross-namespace-resource-associations.md).
::::



## {{es}} is not managed by ECK [k8s-kibana-external-es]

You can also configure {{kib}} to connect to an {{es}} cluster that is managed by a different installation of ECK, or runs outside the Kubernetes cluster. In this case, you need the IP address or URL of the {{es}} cluster and a valid username and password pair to access the cluster.


## Using a Secret [k8s_using_a_secret]

Refer to [*Connect to external Elastic resources*](connect-to-external-elastic-resources.md) to automatically configure {{kib}} using connection settings from a [`Secret`](https://kubernetes.io/docs/concepts/configuration/secret/).


## Using secure settings [k8s_using_secure_settings]

For example, use the [secure settings](../../security/k8s-secure-settings.md) mechanism to securely store the default `elastic` user’s `$PASSWORD` credential of the external {{es}} cluster as set under [Deploy an {{es}} cluster](elasticsearch-deployment-quickstart.md):

```shell
kubectl create secret generic kibana-elasticsearch-credentials --from-literal=elasticsearch.password=$PASSWORD
```

```yaml subs=true
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  version: {{version.stack}}
  count: 1
  config:
    elasticsearch.hosts:
      - <ELASTICSEARCH_HOST_URL>:9200
    elasticsearch.username: elastic
  secureSettings:
    - secretName: kibana-elasticsearch-credentials
```

If the external {{es}} cluster is using a self-signed certificate, create a [`Secret`](https://kubernetes.io/docs/concepts/configuration/secret/) containing the CA certificate and mount it to the {{kib}} container as follows:

```yaml subs=true
apiVersion: kibana.k8s.elastic.co/v1
kind: Kibana
metadata:
  name: kibana-sample
spec:
  version: {{version.stack}}
  count: 1
  config:
    elasticsearch.hosts:
      - <ELASTICSEARCH_HOST_URL>-es-http:9200
    elasticsearch.username: elastic
    elasticsearch.ssl.certificateAuthorities: /etc/certs/ca.crt
  secureSettings:
    - secretName: kibana-elasticsearch-credentials
  podTemplate:
    spec:
      volumes:
        - name: elasticsearch-certs
          secret:
            secretName: elasticsearch-certs-secret
      containers:
        - name: kibana
          volumeMounts:
            - name: elasticsearch-certs
              mountPath: /etc/certs
              readOnly: true
```


