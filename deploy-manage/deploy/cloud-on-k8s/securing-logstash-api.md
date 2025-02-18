---
applies:
  eck: all
mapped_pages:
  - https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-logstash-securing-api.html
---

# Securing Logstash API [k8s-logstash-securing-api]

## Enable HTTPS [k8s-logstash-https]

Access to the [Logstash Monitoring APIs](https://www.elastic.co/guide/en/logstash/current/monitoring-logstash.html#monitoring-api-security) use HTTPS by default - the operator will set the values  `api.ssl.enabled: true`, `api.ssl.keystore.path` and `api.ssl.keystore.password`.

You can further secure the {{ls}} Monitoring APIs by requiring HTTP Basic authentication by setting `api.auth.type: basic`, and providing the relevant credentials `api.auth.basic.username` and `api.auth.basic.password`:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: logstash-api-secret
stringData:
  API_USERNAME: "AWESOME_USER"   <1>
  API_PASSWORD: "T0p_Secret"     <1>
---
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: logstash-sample
spec:
  version: 8.16.1
  count: 1
  config:
    api.auth.type: basic
    api.auth.basic.username: "${API_USERNAME}"   <3>
    api.auth.basic.password: "${API_PASSWORD}"   <3>
  podTemplate:
    spec:
      containers:
        - name: logstash
          envFrom:
            - secretRef:
                name: logstash-api-secret   <2>
```

1. Store the username and password in a Secret.
2. Map the username and password to the environment variables of the Pod.
3. At Logstash startup, `${API_USERNAME}` and `${API_PASSWORD}` are replaced by the value of environment variables. Check [using environment variables](https://www.elastic.co/guide/en/logstash/current/environment-variables.html) for more details.


An alternative is to set up [keystore](advanced-configuration-logstash.md#k8s-logstash-keystore) to resolve `${API_USERNAME}` and `${API_PASSWORD}`

::::{note}
The variable substitution in `config` does not support the default value syntax.
::::



## TLS keystore [k8s-logstash-http-tls-keystore]

The TLS Keystore is automatically generated and includes a certificate and a private key, with default password protection set to `changeit`. This password can be modified by configuring the `api.ssl.keystore.password` value.

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: logstash-sample
spec:
  count: 1
  version: 8.16.1
  config:
    api.ssl.keystore.password: "${SSL_KEYSTORE_PASSWORD}"
```


## Provide your own certificate [k8s-logstash-http-custom-tls]

If you want to use your own certificate, the required configuration is similar to Elasticsearch. Configure the certificate in `api` Service. Check [Custom HTTP certificate](../../security/secure-http-communications.md).

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: logstash-sample
spec:
  version: 8.16.1
  count: 1
  elasticsearchRef:
    name: "elasticsearch-sample"
  services:
    - name: api   <1>
      tls:
        certificate:
          secretName: my-cert
```

1. The service name `api` is reserved for {{ls}} monitoring endpoint.



## Disable TLS [k8s-logstash-http-disable-tls]

You can disable TLS by disabling the generation of the self-signed certificate in the API service definition

```yaml
apiVersion: logstash.k8s.elastic.co/v1alpha1
kind: Logstash
metadata:
  name: logstash-sample
spec:
  version: 8.16.1
  count: 1
  elasticsearchRef:
    name: "elasticsearch-sample"
  services:
    - name: api
      tls:
        selfSignedCertificate:
          disabled: true
```


